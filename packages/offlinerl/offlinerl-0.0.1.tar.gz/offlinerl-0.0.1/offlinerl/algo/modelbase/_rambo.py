import os
import torch
import numpy as np
from copy import deepcopy
from loguru import logger
from operator import itemgetter

from offlinerl.algo.base import BaseAlgo
from offlinerl.utils.data import Batch
from offlinerl.utils.net.common import MLP, Net
from offlinerl.utils.net.tanhpolicy import TanhGaussianPolicy
from offlinerl.utils.exp import setup_seed

from offlinerl.utils.data import ModelBuffer
from offlinerl.utils.net.model.ensemble import EnsembleTransition
from offlinerl.utils.net.terminal_check import get_termination_fn

def algo_init(args):
    logger.info('Run algo_init function')

    setup_seed(args['seed'])
    
    if args["obs_shape"] and args["action_shape"]:
        obs_shape, action_shape = args["obs_shape"], args["action_shape"]
    elif "task" in args.keys():
        from offlinerl.utils.env import get_env_shape
        obs_shape, action_shape = get_env_shape(args['task'])
        args["obs_shape"], args["action_shape"] = obs_shape, action_shape
    else:
        raise NotImplementedError
    
    transition = EnsembleTransition(obs_shape, action_shape, args['hidden_layer_size'], args['transition_layers'], args['transition_init_num']).to(args['device'])
    transition_optim = torch.optim.AdamW(transition.parameters(), lr=args['transition_lr'], weight_decay=0.000075)
    transition_adv_optim = torch.optim.Adam(transition.parameters(), lr=args['transition_adv_lr'], weight_decay=7.5e-5)
    terminal_fn = get_termination_fn(args['task'])

    net_a = Net(layer_num=args['hidden_layers'], 
                state_shape=obs_shape, 
                hidden_layer_size=args['hidden_layer_size'])

    actor = TanhGaussianPolicy(preprocess_net=net_a,
                               action_shape=action_shape,
                               hidden_layer_size=args['hidden_layer_size'],
                               conditioned_sigma=True).to(args['device'])

    actor_optim = torch.optim.Adam(actor.parameters(), lr=args['actor_lr'])

    log_alpha = torch.zeros(1, requires_grad=True, device=args['device'])
    alpha_optimizer = torch.optim.Adam([log_alpha], lr=args["alpha_lr"])

    q1 = MLP(obs_shape + action_shape, 1, args['hidden_layer_size'], args['hidden_layers'], norm=None, hidden_activation='swish').to(args['device'])
    q2 = MLP(obs_shape + action_shape, 1, args['hidden_layer_size'], args['hidden_layers'], norm=None, hidden_activation='swish').to(args['device'])
    critic_optim = torch.optim.Adam([*q1.parameters(), *q2.parameters()], lr=args['critic_lr'])

    return {
        "transition" : {"net" : transition, "opt" : transition_optim, "adv_opt" : transition_adv_optim, "terminal_fn" : terminal_fn},
        "actor" : {"net" : actor, "opt" : actor_optim},
        "log_alpha" : {"net" : log_alpha, "opt" : alpha_optimizer},
        "critic" : {"net" : [q1, q2], "opt" : critic_optim},
    }


class AlgoTrainer(BaseAlgo):
    def __init__(self, algo_init, args):
        super(AlgoTrainer, self).__init__(args)
        self.args = args

        self.transition = algo_init['transition']['net']
        self.transition_optim = algo_init['transition']['opt']
        self.transition_adv_optim = algo_init['transition']['adv_opt']
        self.terminal_fn = algo_init['transition']['terminal_fn']
        self.selected_transitions = None

        self.actor = algo_init['actor']['net']
        self.actor_optim = algo_init['actor']['opt']

        self.log_alpha = algo_init['log_alpha']['net']
        self.log_alpha_optim = algo_init['log_alpha']['opt']

        self.q1, self.q2 = algo_init['critic']['net']
        self.target_q1 = deepcopy(self.q1)
        self.target_q2 = deepcopy(self.q2)
        self.critic_optim = algo_init['critic']['opt']

        self.device = args['device']

        # # 1250000
        # self.args['buffer_size'] = int(self.args['data_collection_per_epoch']) * self.args['horizon'] * 5
        # 51200
        self.args['buffer_size'] = self.args['steps_per_epoch'] // self.args["rollout_freq"] * \
                                    self.args["model_retain_epochs"] * self.args["rollout_batch_size"] * self.args["horizon"]
        self.args['target_entropy'] = - self.args['action_shape']

    def train(self, train_buffer, val_buffer, callback_fn):
        if self.args['policy_bc_path'] is not None:
            self.actor = torch.load(os.path.join(self.args['policy_bc_path'], "policy_bc.pt"), map_location='cpu').to(self.device)
            self.actor_optim = torch.optim.Adam(self.actor.parameters(), lr=self.args['actor_lr'])
        else:
            self.pretrain_policy(train_buffer.sample_all())
            if self.args['policy_bc_save_path'] is not None: 
                torch.save(self.actor, os.path.join(self.args['policy_bc_save_path'], "policy_bc.pt"))

        self.transition.update_self(torch.cat((torch.Tensor(train_buffer["obs"]), torch.Tensor(train_buffer["obs_next"])), 0))
        if self.args['dynamics_path'] is not None:
            self.transition = torch.load(os.path.join(self.args['dynamics_path'], "dynamics.pt"), map_location='cpu').to(self.device)
            self.transition_adv_optim = torch.optim.Adam(self.transition.parameters(), lr=self.args['transition_adv_lr'], weight_decay=7.5e-5)
        else:
            self.train_transition(train_buffer)
            if self.args['dynamics_save_path'] is not None: 
                torch.save(self.transition, os.path.join(self.args['dynamics_save_path'], "dynamics.pt"))

        self.transition.requires_grad_(False)
        self.train_policy(train_buffer, val_buffer, self.transition, callback_fn)
    
    def get_policy(self):
        return self.actor
    
    def pretrain_policy(self, data) -> None:
        batch_size = self.args['policy_bc_batch_size']
        self._bc_optim = torch.optim.Adam(self.actor.parameters(), lr=self.args['policy_bc_lr'])
        observations = data["obs"]
        actions = data["act"]
        sample_num = observations.shape[0]
        idxs = np.arange(sample_num)
        print("Pretraining policy")
        for epoch in range(self.args['policy_bc_epoch']):
            np.random.shuffle(idxs)
            sum_loss = 0
            for i_batch in range(sample_num // batch_size):
                batch_obs = observations[i_batch * batch_size: (i_batch + 1) * batch_size]
                batch_act = actions[i_batch * batch_size: (i_batch + 1) * batch_size]
                batch_obs = torch.from_numpy(batch_obs).to(self.device)
                batch_act = torch.from_numpy(batch_act).to(self.device)
                dist = self.actor(batch_obs)
                pred_actions = dist.rsample()
                bc_loss = ((pred_actions - batch_act) ** 2).mean()

                self._bc_optim.zero_grad()
                bc_loss.backward()
                self._bc_optim.step()
                sum_loss += bc_loss.cpu().item()
            print(f"Epoch {epoch}, mean bc loss {sum_loss/i_batch}")
        return  

    def train_transition(self, buffer):
        data_size = len(buffer)
        val_size = min(int(data_size * self.args['val_ratio']) + 1, 1000)
        train_size = data_size - val_size
        train_splits, val_splits = torch.utils.data.random_split(range(data_size), (train_size, val_size))
        train_buffer = buffer[train_splits.indices]
        valdata = buffer[val_splits.indices]
        batch_size = self.args['transition_batch_size']

        val_losses = [1e+8 for i in range(self.transition.ensemble_size)]

        epoch = 0
        cnt = 0
        while True:
            epoch += 1
            idxs = np.random.randint(train_buffer.shape[0], size=[self.transition.ensemble_size, train_buffer.shape[0]])
            for batch_num in range(int(np.ceil(idxs.shape[-1] / batch_size))):
                batch_idxs = idxs[:, batch_num * batch_size:(batch_num + 1) * batch_size]
                batch = train_buffer[batch_idxs]
                self._train_transition(batch)
            new_val_losses = self._eval_transition(valdata)
            print(f"epoch: {epoch}, val loss: {new_val_losses}")

            indexes = []
            for i, new_loss, old_loss in zip(range(len(val_losses)), new_val_losses, val_losses):
                improvement = (old_loss - new_loss) / old_loss
                if improvement > 1e-4:
                    indexes.append(i)
                    val_losses[i] = new_loss

            if len(indexes) > 0:
                self.transition.update_save(indexes)
                cnt = 0
            else:
                cnt += 1

            if (cnt >= self.args['max_epochs_since_update']) or (self.args['transition_max_epochs'] is not None and (epoch >= self.args['transition_max_epochs'])):
                break
        
        indexes = self._select_best_indexes(val_losses, n=self.args['transition_select_num'])
        self.transition.set_select(indexes)
        return self.transition

    def train_policy(self, train_buffer, val_buffer, transition, callback_fn):
        real_batch_size = int(self.args['policy_batch_size'] * self.args['real_data_ratio'])
        model_batch_size = self.args['policy_batch_size']  - real_batch_size
        
        model_buffer = ModelBuffer(self.args['buffer_size'])

        obs_max = torch.as_tensor(train_buffer['obs'].max(axis=0)).to(self.device)
        obs_min = torch.as_tensor(train_buffer['obs'].min(axis=0)).to(self.device)
        rew_max = train_buffer['rew'].max()
        rew_min = train_buffer['rew'].min()

        num_timesteps = 0

        for epoch in range(self.args['max_epoch']):
            if num_timesteps % self.args['rollout_freq'] == 0:
                # collect data
                with torch.no_grad():
                    obs = train_buffer.sample(int(self.args['rollout_batch_size']))['obs']
                    obs = torch.tensor(obs, device=self.device)
                    for t in range(self.args['horizon']):
                        action = self.actor(obs).sample()
                        obs_action = torch.cat([obs, action], dim=-1)
                        next_obs_dists = transition(obs_action)
                        next_obses = next_obs_dists.sample()
                        rewards = next_obses[:, :, -1:]
                        next_obses = next_obses[:, :, :-1]

                        model_indexes = np.random.randint(0, next_obses.shape[0], size=(obs.shape[0]))
                        next_obs = next_obses[model_indexes, np.arange(obs.shape[0])]
                        reward = rewards[model_indexes, np.arange(obs.shape[0])]

                        next_obs = torch.max(torch.min(next_obs, obs_max), obs_min)
                        reward = torch.clamp(reward, rew_min, rew_max)
                        print('average reward:', reward.mean().item())

                        terminals = self.terminal_fn(obs.cpu().numpy(), action.cpu().numpy(), next_obs.cpu().numpy())
                        nonterm_mask = (~terminals).flatten()

                        batch_data = Batch({
                            "obs" : obs.cpu().numpy(),
                            "obs_next" : next_obs.cpu().numpy(),
                            "act" : action.cpu().numpy(),
                            "rew" : reward.cpu().numpy(),
                            "done" : terminals,
                        })

                        model_buffer.put(batch_data)

                        if nonterm_mask.sum() == 0:
                            break

                        obs = next_obs

            # update
            for _ in range(self.args['steps_per_epoch']):
                batch = train_buffer.sample(real_batch_size)
                model_batch = model_buffer.sample(model_batch_size)
                batch = Batch.cat([batch, model_batch], axis=0)
                batch.to_torch(device=self.device)

                self._sac_update(batch)

                # update transition
                if self.args['dynamics_update_freq'] > 0 and (num_timesteps+1) % self.args['dynamics_update_freq'] == 0:
                    all_loss_info = self.update_transition(train_buffer)
                    self.log_res(epoch, all_loss_info)

                num_timesteps += 1

            val_freq = self.args.get("val_frequency", 1)
            if epoch % val_freq == 0:
                res = callback_fn(self.get_policy())
            else:
                res = {}

            res['reward'] = reward.mean().item()
            self.log_res(epoch, res)

        return self.get_policy()
    
    def update_transition(self, real_buffer):
        all_loss_info = {"adv_dynamics_update/all_loss": 0, 
                         "adv_dynamics_update/sl_loss": 0, 
                         "adv_dynamics_update/adv_loss": 0, 
                         "adv_dynamics_update/adv_advantage": 0, 
                         "adv_dynamics_update/adv_log_prob": 0, 
                         }
        self.transition.requires_grad_(True)
        steps = 0
        while steps < self.args['adv_train_steps']:
            init_obss = real_buffer.sample(self.args['adv_rollout_batch_size'])["obs"]
            obs = init_obss
            for t in range(self.args['adv_rollout_length']):
                act = self.actor(torch.as_tensor(obs, dtype=torch.float32).to(self.device)).sample()
                sl_obs, sl_act, sl_next_obs, sl_rew = \
                    itemgetter("obs", "act", "obs_next", "rew")(real_buffer.sample(self.args['adv_rollout_batch_size']))
                obs_next, terminals, loss_info = self.transition_step_and_forward(obs, 
                                                                                  act.detach().cpu().numpy(), 
                                                                                  sl_obs, 
                                                                                  sl_act, 
                                                                                  sl_next_obs, 
                                                                                  sl_rew)
                for _key in loss_info:
                    all_loss_info[_key] += loss_info[_key]
                steps += 1
                obs = obs_next.copy()
                if steps == 1000:
                    break
        self.transition.requires_grad_(False)
        return {_key: _value/steps for _key, _value in all_loss_info.items()}
    
    def transition_step_and_forward(self, obs, act, sl_obs, sl_act, sl_next_obs, sl_rew):
        obs_act = np.concatenate([obs, act], axis=-1)
        obs_act = torch.as_tensor(obs_act, dtype=torch.float32).to(self.device)
        dist = self.transition(obs_act)
        ensemble_sample = dist.sample()  # [ensemble_size(elite), batch_size, obs_dim + rew_dim]
        ensemble_size, batch_size, _ = ensemble_sample.shape

        # select the next observations
        selected_indexes = self.transition.random_elite_idxs(batch_size)
        sample = ensemble_sample[selected_indexes, np.arange(batch_size)]
        next_obs = sample[..., :-1]
        rew = sample[..., -1:]
        terminals = self.terminal_fn(obs, act, next_obs.cpu().numpy())

        # compute logprob
        log_prob = dist.log_prob(sample).sum(-1, keepdim=True)
        prob = log_prob.double().exp()
        prob = prob * (1 / len(self.transition.elites))
        log_prob = prob.sum(0).log().type(torch.float32)

        # compute the advantage
        with torch.no_grad():
            next_act_dist = self.actor(next_obs)
            next_act = next_act_dist.mode
            next_act_log_prob = next_act_dist.log_prob(next_act).sum(dim=-1, keepdim=True)
            next_obs_action = torch.cat([next_obs, next_act], dim=-1)
            next_q = torch.minimum(self.target_q1(next_obs_action), 
                                   self.target_q2(next_obs_action)
                                   )
            if self.args['include_ent_in_adv']:
                alpha = torch.exp(self.log_alpha)
                next_q = next_q - alpha * next_act_log_prob

            value = rew + (1 - torch.from_numpy(terminals).to(next_obs.device).float()) * self.args['discount'] * next_q

            value_baseline = torch.minimum(self.target_q1(obs_act), 
                                           self.target_q2(obs_act)
                                           )
            advantage = value - value_baseline
            advantage = (advantage - advantage.mean()) / (advantage.std()+1e-6)
        adv_loss = (log_prob * advantage).mean()

        # compute the supervised loss
        sl_obs, sl_act, sl_next_obs, sl_rew = torch.as_tensor(sl_obs, dtype=torch.float32, device=self.device), \
                                                torch.as_tensor(sl_act, dtype=torch.float32, device=self.device), \
                                                torch.as_tensor(sl_next_obs, dtype=torch.float32, device=self.device), \
                                                torch.as_tensor(sl_rew, dtype=torch.float32, device=self.device)
        sl_input = torch.cat([sl_obs, sl_act], dim=-1)
        sl_target = torch.cat([sl_next_obs, sl_rew], dim=-1)

        sl_dist = self.transition(sl_input)
        sl_loss = - sl_dist.log_prob(sl_target).mean()
        sl_loss = sl_loss + 0.001 * self.transition.max_logstd.mean() - 0.001 * self.transition.min_logstd.mean()

        all_loss = self.args['adv_weight'] * adv_loss + sl_loss

        self.transition_adv_optim.zero_grad()
        all_loss.backward()
        self.transition_adv_optim.step()

        return next_obs.detach().cpu().numpy(), terminals, {"adv_dynamics_update/adv_loss": adv_loss.cpu().item(), 
                                                            "adv_dynamics_update/sl_loss": sl_loss.cpu().item(),
                                                            "adv_dynamics_update/all_loss": all_loss.cpu().item(),
                                                            "adv_dynamics_update/adv_advantage": advantage.mean().cpu().item(),
                                                            "adv_dynamics_update/adv_log_prob": log_prob.mean().cpu().item()}

    def _sac_update(self, batch_data):
        obs = batch_data['obs']
        action = batch_data['act']
        next_obs = batch_data['obs_next']
        reward = batch_data['rew']
        done = batch_data['done']

        # update critic
        obs_action = torch.cat([obs, action], dim=-1)
        _q1 = self.q1(obs_action)
        _q2 = self.q2(obs_action)

        with torch.no_grad():
            next_action_dist = self.actor(next_obs)
            next_action = next_action_dist.sample()
            log_prob = next_action_dist.log_prob(next_action).sum(dim=-1, keepdim=True)
            next_obs_action = torch.cat([next_obs, next_action], dim=-1)
            _target_q1 = self.target_q1(next_obs_action)
            _target_q2 = self.target_q2(next_obs_action)
            alpha = torch.exp(self.log_alpha)
            y = reward + self.args['discount'] * (1 - done) * (torch.min(_target_q1, _target_q2) - alpha * log_prob)

        critic_loss = ((y - _q1) ** 2).mean() + ((y - _q2) ** 2).mean()

        self.critic_optim.zero_grad()
        critic_loss.backward()
        self.critic_optim.step()

        # soft target update
        self._sync_weight(self.target_q1, self.q1, soft_target_tau=self.args['soft_target_tau'])
        self._sync_weight(self.target_q2, self.q2, soft_target_tau=self.args['soft_target_tau'])

        if self.args['learnable_alpha']:
            # update alpha
            alpha_loss = - torch.mean(self.log_alpha * (log_prob + self.args['target_entropy']).detach())

            self.log_alpha_optim.zero_grad()
            alpha_loss.backward()
            self.log_alpha_optim.step()
        else:
            self.log_alpha = torch.ones(1, requires_grad=True, device=self.args['device']) * self.args['alpha']

        # update actor
        action_dist = self.actor(obs)
        new_action = action_dist.rsample()
        action_log_prob = action_dist.log_prob(new_action)
        new_obs_action = torch.cat([obs, new_action], dim=-1)
        q = torch.min(self.q1(new_obs_action), self.q2(new_obs_action))
        actor_loss = - q.mean() + torch.exp(self.log_alpha) * action_log_prob.sum(dim=-1).mean()

        self.actor_optim.zero_grad()
        actor_loss.backward()
        self.actor_optim.step()

    def _select_best_indexes(self, metrics, n):
        pairs = [(metric, index) for metric, index in zip(metrics, range(len(metrics)))]
        pairs = sorted(pairs, key=lambda x: x[0])
        selected_indexes = [pairs[i][1] for i in range(n)]
        return selected_indexes

    def _train_transition(self, data):
        data.to_torch(device=self.device)
        dist = self.transition(torch.cat([data['obs'], data['act']], dim=-1))
        loss = - dist.log_prob(torch.cat([data['obs_next'], data['rew']], dim=-1))
        loss = loss.mean()

        loss = loss + 0.001 * self.transition.max_logstd.mean() - 0.001 * self.transition.min_logstd.mean()

        self.transition_optim.zero_grad()
        loss.backward()
        self.transition_optim.step()
        
    def _eval_transition(self, valdata):
        with torch.no_grad():
            valdata.to_torch(device=self.device)
            dist = self.transition(torch.cat([valdata['obs'], valdata['act']], dim=-1))
            loss = ((dist.mean - torch.cat([valdata['obs_next'], valdata['rew']], dim=-1)) ** 2).mean(dim=(1,2))
            return list(loss.cpu().numpy())
        