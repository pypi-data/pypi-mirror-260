# MOBILE: Model-Bellman Inconsistency Penalized Policy Optimization
# https://proceedings.mlr.press/v202/sun23q.html
# https://github.com/yihaosun1124/mobile

import torch
import numpy as np
from copy import deepcopy
from loguru import logger

from offlinerl.algo.base import BaseAlgo
from offlinerl.utils.data import Batch
from offlinerl.utils.net.common import MLP, Net
from offlinerl.utils.net.tanhpolicy import TanhGaussianPolicy
from offlinerl.utils.exp import setup_seed

from offlinerl.utils.data import ModelBuffer
# from offlinerl.utils.net.model.ensemble import EnsembleTransition
from offlinerl.utils.net.model.new_ensemble import EnsembleTransition, StandardScaler
from offlinerl.utils.net.terminal_check import get_termination_fn


def algo_init(args):
    logger.info('Run algo_init function')

    setup_seed(args['seed'])
    
    if args["obs_shape"] and args["action_shape"]:
        obs_shape, action_shape = args["obs_shape"], args["action_shape"]
    elif "task" in args.keys():
        from offlinerl.utils.env import get_env_shape, get_env_action_range
        obs_shape, action_shape = get_env_shape(args['task'])
        args["max_action"] = get_env_action_range(args['task'])[0]
        args["obs_shape"], args["action_shape"] = obs_shape, action_shape
    else:
        raise NotImplementedError
    
    transition = EnsembleTransition(
        obs_shape, 
        action_shape,
        hidden_dims=[200, 200, 200, 200], 
        weight_decays=[2.5e-5, 5e-5, 7.5e-5, 7.5e-5, 1e-4],device=args['device']).to(args['device'])
    transition_optim = torch.optim.Adam(transition.parameters(), lr=args['transition_lr'])
    terminal_fn = get_termination_fn(args['task'])

    net_a = Net(layer_num=args['hidden_layers'], 
                state_shape=obs_shape, 
                hidden_layer_size=args['hidden_layer_size'])

    actor = TanhGaussianPolicy(preprocess_net=net_a,
                               action_shape=action_shape,
                               max_action=args['max_action'],
                               hidden_layer_size=args['hidden_layer_size'],
                               conditioned_sigma=True).to(args['device'])

    actor_optim = torch.optim.Adam(actor.parameters(), lr=args['actor_lr'])

    log_alpha = torch.zeros(1, requires_grad=True, device=args['device'])
    alpha_optimizer = torch.optim.Adam([log_alpha], lr=args["actor_lr"])
    
    critics = [
        MLP(obs_shape + action_shape, 1, args['hidden_layer_size'], args['hidden_layers'], norm=None, hidden_activation='relu').to(args['device'])
        for _ in range(args["num_q_ensemble"])
    ]
    critics = torch.nn.ModuleList(critics)
    critics_optim = torch.optim.Adam(critics.parameters(), lr=args["critic_lr"])

    if args['lr_scheduler']:
        lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(actor_optim, args['max_epoch'])
    else:
        lr_scheduler = None

    return {
        "transition" : {"net" : transition, "opt" : transition_optim, "terminal_fn" : terminal_fn},
        "actor" : {"net" : actor, "opt" : actor_optim},
        "log_alpha" : {"net" : log_alpha, "opt" : alpha_optimizer},
        "critics" : {"net" : critics, "opt" : critics_optim},
        'lr_scheduler' : lr_scheduler
    }


class AlgoTrainer(BaseAlgo):
    def __init__(self, algo_init, args):
        super(AlgoTrainer, self).__init__(args)
        self.args = args

        self.transition = algo_init['transition']['net']
        self.transition_optim = algo_init['transition']['opt']
        self.terminal_fn = algo_init['transition']['terminal_fn']
        self.selected_transitions = None

        self.actor = algo_init['actor']['net']
        self.actor_optim = algo_init['actor']['opt']

        self.log_alpha = algo_init['log_alpha']['net']
        self.log_alpha_optim = algo_init['log_alpha']['opt']
        
        self.critics = algo_init['critics']['net']
        self.target_critics = deepcopy(self.critics)
        self.critic_optim = algo_init['critics']['opt']
        self.lr_scheduler = algo_init['lr_scheduler']

        self.device = args['device']

        self.args['buffer_size'] = int(self.args['data_collection_per_epoch']) * self.args['horizon'] * 5
        self.args['target_entropy'] = - self.args['action_shape']

        self.scaler = StandardScaler()
        
    def train(self, train_buffer, val_buffer, callback_fn):
        if self.args['dynamics_path'] is not None:
            self.transition.load(self.args['dynamics_path'])
        else:
            self.train_transition(train_buffer)
            if self.args['dynamics_save_path'] is not None: self.transition.save(self.args['dynamics_save_path'])
        self.transition.requires_grad_(False) 
        self.train_policy(train_buffer, val_buffer, self.transition, callback_fn)
    
    def get_policy(self):
        return self.actor

    def train_transition(self, buffer):
        inputs, targets = self.format_samples_for_training(buffer)
        data_size = inputs.shape[0]
        holdout_size = min(int(data_size * 0.2), 1000)
        train_size = data_size - holdout_size
        train_splits, holdout_splits = torch.utils.data.random_split(range(data_size), (train_size, holdout_size))
        train_inputs, train_targets = inputs[train_splits.indices], targets[train_splits.indices]
        holdout_inputs, holdout_targets = inputs[holdout_splits.indices], targets[holdout_splits.indices]

        self.scaler.fit(train_inputs)
        train_inputs = self.scaler.transform(train_inputs)
        holdout_inputs = self.scaler.transform(holdout_inputs)
        holdout_losses = [1e10 for i in range(self.transition.num_ensemble)]

        data_idxes = np.random.randint(train_size, size=[self.transition.num_ensemble, train_size])
        def shuffle_rows(arr):
            idxes = np.argsort(np.random.uniform(size=arr.shape), axis=-1)
            return arr[np.arange(arr.shape[0])[:, None], idxes]

        epoch = 0
        cnt = 0
        while True:
            epoch += 1
            train_loss = self._train_transition(train_inputs[data_idxes], train_targets[data_idxes], batch_size = self.args['transition_batch_size'])
            new_holdout_losses = self._eval_transition(holdout_inputs, holdout_targets)
            holdout_loss = (np.sort(new_holdout_losses)[:self.transition.num_elites]).mean()
            print(f"dynamics_train_loss: {train_loss:.2f}")
            print(f"dynamics_holdout_loss: {holdout_loss:.2f}")

            # shuffle data for each base learner
            data_idxes = shuffle_rows(data_idxes)

            indexes = []
            for i, new_loss, old_loss in zip(range(len(holdout_losses)), new_holdout_losses, holdout_losses):
                improvement = (old_loss - new_loss) / old_loss
                if improvement > 0.01:
                    indexes.append(i)
                    holdout_losses[i] = new_loss
            
            if len(indexes) > 0:
                self.transition.update_save(indexes)
                cnt = 0
            else:
                cnt += 1
            
            if cnt >= 5:
                break

        indexes = self.select_elites(holdout_losses)
        self.transition.set_elites(indexes)
        self.transition.load_save()

    def train_policy(self, train_buffer, val_buffer, transition, callback_fn):
        real_batch_size = int(self.args['policy_batch_size'] * self.args['real_data_ratio'])
        model_batch_size = self.args['policy_batch_size']  - real_batch_size
        
        model_buffer = ModelBuffer(self.args['buffer_size'])

        obs_max = torch.as_tensor(train_buffer['obs'].max(axis=0)).to(self.device)
        obs_min = torch.as_tensor(train_buffer['obs'].min(axis=0)).to(self.device)
        rew_max = train_buffer['rew'].max()
        rew_min = train_buffer['rew'].min()

        for epoch in range(self.args['max_epoch']):
            # collect data
            with torch.no_grad():
                obs = train_buffer.sample(int(self.args['data_collection_per_epoch']))['obs']
                obs = torch.tensor(obs, device=self.device)
                for t in range(self.args['horizon']):
                    action = self.actor(obs).sample()
                    obs_action = torch.cat([obs, action], dim=-1)
                    obs_action = self.scaler.transform_tensor(obs_action)
                    mean, logvar = transition(obs_action)
                    mean, logvar = mean[self.transition.elites.cpu().numpy()], logvar[self.transition.elites.cpu().numpy()]
                    mean[..., :-1] += obs
                    std = torch.sqrt(torch.exp(logvar))
                    next_obs_dists = torch.distributions.Normal(mean, std)

                    next_obses = next_obs_dists.sample()
                    rewards = next_obses[..., -1:]
                    next_obses = next_obses[..., :-1]

                    # compute model-bellman inconcistency
                    next_obes_ = torch.stack([next_obs_dists.sample()[...,:-1] for i in range(10)], 0)
                    num_samples, num_ensembles, batch_size, obs_dim = next_obes_.shape
                    next_obes_ = next_obes_.reshape(-1, obs_dim)
                    next_actions_ = self.actor(next_obes_).sample()
                    next_obs_acts_ = torch.cat([next_obes_, next_actions_], dim=-1)
                    next_qs_ =  torch.cat([target_critic(next_obs_acts_) for target_critic in self.target_critics], 1)
                    next_qs_ = torch.min(next_qs_, 1)[0].reshape(num_samples, num_ensembles, batch_size, 1)
                    uncertainty = next_qs_.mean(0).std(0)

                    model_indexes = np.random.randint(0, next_obses.shape[0], size=(obs.shape[0]))
                    next_obs = next_obses[model_indexes, np.arange(obs.shape[0])]
                    reward = rewards[model_indexes, np.arange(obs.shape[0])]

                    next_obs = torch.max(torch.min(next_obs, obs_max), obs_min)
                    reward = torch.clamp(reward, rew_min, rew_max)
                    
                    print('average reward:', reward.mean().item())
                    print('average uncertainty:', uncertainty.mean().item())

                    penalized_reward = reward - self.args['lam'] * uncertainty
                    # dones = torch.zeros_like(reward)
                    terminals = self.terminal_fn(obs.cpu().numpy(), action.cpu().numpy(), next_obs.cpu().numpy())
                    nonterm_mask = (~terminals).flatten()

                    batch_data = Batch({
                        "obs" : obs.cpu(),
                        "act" : action.cpu(),
                        "rew" : penalized_reward.cpu(),
                        "done" : terminals,
                        "obs_next" : next_obs.cpu(),
                    })

                    model_buffer.put(batch_data)

                    if nonterm_mask.sum() == 0:
                        break

                    obs = next_obs[nonterm_mask]

            # update
            for _ in range(self.args['steps_per_epoch']):
                batch = train_buffer.sample(real_batch_size)
                model_batch = model_buffer.sample(model_batch_size)
                batch = Batch.cat([Batch({k: v.reshape(-1, 1) if len(v.shape) == 1 else v for k, v in batch.items()}), model_batch], axis=0)
                batch.to_torch(device=self.device)

                loss = self._sac_update(batch)

            if self.lr_scheduler is not None:
                self.lr_scheduler.step()
                
            val_frequency = self.args.get("val_frequency",1)
            
            if epoch % val_frequency == 0:
                res = callback_fn(self.get_policy())
            else:
                res = {}
                
            res.update(loss)
            
            res['uncertainty'] = uncertainty.mean().item()
            res['reward'] = reward.mean().item()
            self.log_res(epoch, res)

        return self.get_policy()

    def _sac_update(self, batch_data):
        obs = batch_data['obs']
        action = batch_data['act']
        next_obs = batch_data['obs_next']
        reward = batch_data['rew']
        done = batch_data['done']

        # update critic
        obs_action = torch.cat([obs, action], dim=-1)
        qs = torch.stack([critic(obs_action) for critic in self.critics], 0)

        with torch.no_grad():
            if self.args['max_q_backup']:
                batch_size = obs.shape[0]
                tmp_next_obs = next_obs.unsqueeze(1) \
                    .repeat(1, 10, 1) \
                    .view(batch_size * 10, next_obs.shape[-1])
                tmp_next_action = self.actor(tmp_next_obs).sample()
                tmp_next_obs_action = torch.cat([tmp_next_obs, tmp_next_action], dim=-1)
                tmp_next_qs = torch.cat([target_critic(tmp_next_obs_action) for target_critic in self.target_critics], 1)
                tmp_next_qs = tmp_next_qs.view(batch_size, 10, len(self.target_critics)).max(1)[0].view(-1, len(self.target_critics))
                next_q = torch.min(tmp_next_qs, 1)[0].reshape(-1, 1)
            else:
                next_action_dist = self.actor(next_obs)
                next_action = next_action_dist.sample()
                log_prob = next_action_dist.log_prob(next_action).sum(dim=-1, keepdim=True)
                next_obs_action = torch.cat([next_obs, next_action], dim=-1)
                next_qs = torch.cat([target_critic(next_obs_action) for target_critic in self.target_critics], 1)
                next_q = torch.min(next_qs, 1)[0].reshape(-1, 1)
                if not self.args['deterministic_backup']:
                    alpha = torch.exp(self.log_alpha)
                    next_q -= alpha * log_prob
            y = reward + self.args['discount'] * (1 - done) * next_q
            y = torch.clamp(y, 0, None)

        critic_loss = ((qs - y) ** 2).mean()

        self.critic_optim.zero_grad()
        critic_loss.backward()
        self.critic_optim.step()

        # soft target update
        for target_critic, critic in zip(self.target_critics, self.critics):
            self._sync_weight(target_critic, critic, soft_target_tau=self.args['soft_target_tau'])

        if self.args['learnable_alpha']:
            # update alpha
            alpha_loss = - torch.mean(self.log_alpha * (log_prob + self.args['target_entropy']).detach())

            self.log_alpha_optim.zero_grad()
            alpha_loss.backward()
            self.log_alpha_optim.step()

        # update actor
        action_dist = self.actor(obs)
        new_action = action_dist.rsample()
        action_log_prob = action_dist.log_prob(new_action)
        new_obs_action = torch.cat([obs, new_action], dim=-1)
        q = torch.cat([critic(new_obs_action) for critic in self.critics], 1)
        actor_loss = - torch.min(q, 1)[0].mean() + torch.exp(self.log_alpha) * action_log_prob.sum(dim=-1).mean()

        self.actor_optim.zero_grad()
        actor_loss.backward()
        self.actor_optim.step()
        
        loss = {
            "actor_loss" : actor_loss.item(),
            "critic_loss" : critic_loss.item(),
            "alpha_loss" : alpha_loss.item(),
            "alpha_loss" : alpha_loss.item(),
            "alpha" : torch.exp(self.log_alpha).item(),
        }
        
        return loss

    def select_elites(self, metrics):
        pairs = [(metric, index) for metric, index in zip(metrics, range(len(metrics)))]
        pairs = sorted(pairs, key=lambda x: x[0])
        elites = [pairs[i][1] for i in range(self.transition.num_elites)]
        return elites
    
    def format_samples_for_training(self, data):
        obss = data["obs"]
        actions = data["act"]
        next_obss = data["obs_next"]
        rewards = data["rew"]
        delta_obss = next_obss - obss
        inputs = np.concatenate((obss, actions), axis=-1)
        targets = np.concatenate((delta_obss, rewards.reshape(-1,1)), axis=-1)
        return inputs, targets

    def _train_transition(self, inputs, targets, batch_size):
        self.transition.train()
        train_size = inputs.shape[1]
        losses = []

        for batch_num in range(int(np.ceil(train_size / batch_size))):
            inputs_batch = inputs[:, batch_num * batch_size:(batch_num + 1) * batch_size]
            targets_batch = targets[:, batch_num * batch_size:(batch_num + 1) * batch_size]
            targets_batch = torch.as_tensor(targets_batch).to(self.transition.device)
            mean, logvar = self.transition(inputs_batch)
            inv_var = torch.exp(-logvar)
            # Average over batch and dim, sum over ensembles.
            mse_loss_inv = (torch.pow(mean - targets_batch, 2) * inv_var).mean(dim=(1, 2))
            var_loss = logvar.mean(dim=(1, 2))
            loss = mse_loss_inv.sum() + var_loss.sum()
            loss = loss + self.transition.get_decay_loss()
            loss = loss + 0.01 * self.transition.max_logvar.sum() - 0.01 * self.transition.min_logvar.sum()

            self.transition_optim.zero_grad()
            loss.backward()
            self.transition_optim.step()

            losses.append(loss.item())
        return np.mean(losses)
    
    @torch.no_grad()
    def _eval_transition(self, inputs, targets):
        self.transition.eval()
        targets = torch.as_tensor(targets).to(self.transition.device)
        mean, _ = self.transition(inputs)
        loss = ((mean - targets) ** 2).mean(dim=(1, 2))
        val_loss = list(loss.cpu().numpy())
        return val_loss