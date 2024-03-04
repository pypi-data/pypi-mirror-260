import os
from copy import deepcopy
from collections import defaultdict
import json

import torch
import numpy as np
from loguru import logger
from operator import itemgetter

from offlinerl.algo.base import BaseAlgo
from offlinerl.utils.exp import setup_seed
from offlinerl.utils.net.terminal_check import get_termination_fn

from offlinerl.outside_utils.nets import MLP
from offlinerl.outside_utils.modules import ActorProb, Critic, TanhDiagGaussian, EnsembleDynamicsModel
from offlinerl.outside_utils.dynamics import EnsembleDynamics
from offlinerl.outside_utils.utils.scaler import StandardScaler
from offlinerl.outside_utils.utils.termination_fns import obs_unnormalization
from offlinerl.outside_utils.buffer import ReplayBuffer


def algo_init(args):
    logger.info('Run algo_init function')

    setup_seed(args['seed'])
    
    if args["obs_shape"] and args["action_shape"]:
        obs_shape, action_shape = args["obs_shape"], args["action_shape"]
    elif "task" in args.keys():
        from offlinerl.utils.env import get_env_shape
        obs_shape, action_shape = get_env_shape(args['task'])
    else:
        raise NotImplementedError
    obs_shape, action_shape = (obs_shape,), (action_shape,)
    args["obs_shape"], args["action_shape"] = obs_shape, action_shape
    action_dim = np.prod(action_shape)

    # create policy model
    actor_backbone = MLP(input_dim=np.prod(obs_shape), hidden_dims=args['hidden_dims'])
    critic1_backbone = MLP(input_dim=np.prod(obs_shape) + action_dim, hidden_dims=args['hidden_dims'])
    critic2_backbone = MLP(input_dim=np.prod(obs_shape) + action_dim, hidden_dims=args['hidden_dims'])
    dist = TanhDiagGaussian(
        latent_dim=getattr(actor_backbone, "output_dim"),
        output_dim=action_dim,
        unbounded=True,
        conditioned_sigma=True
    )
    actor = ActorProb(actor_backbone, dist, args['device'])
    actor_optim = torch.optim.Adam(actor.parameters(), lr=args['actor_lr'])

    critic1 = Critic(critic1_backbone, args['device'])
    critic2 = Critic(critic2_backbone, args['device'])
    critic1_optim = torch.optim.Adam(critic1.parameters(), lr=args['critic_lr'])
    critic2_optim = torch.optim.Adam(critic2.parameters(), lr=args['critic_lr'])

    if args['learnable_alpha']:
        target_entropy = args['target_entropy'] if args['target_entropy'] is not None else -np.prod(action_shape)

        log_alpha = torch.zeros(1, requires_grad=True, device=args['device'])
        alpha_optim = torch.optim.Adam([log_alpha], lr=args['alpha_lr'])
        alpha = (target_entropy, log_alpha, alpha_optim)
    else:
        alpha = args['alpha']
        alpha_optim = None

    # create dynamics
    dynamics_model = EnsembleDynamicsModel(
        obs_dim=np.prod(obs_shape),
        action_dim=action_dim,
        hidden_dims=args['dynamics_hidden_dims'],
        num_ensemble=args['transition_init_num'],
        num_elites=args['transition_select_num'],
        weight_decays=args['dynamics_weight_decay'],
        device=args['device']
    )
    dynamics_optim = torch.optim.Adam(dynamics_model.parameters(), lr=args['transition_lr'])
    dynamics_adv_optim = torch.optim.Adam(dynamics_model.parameters(), lr=args['transition_adv_lr'])
    dynamics_scaler = StandardScaler()

    _termination_fn = get_termination_fn(task=args['task'])

    return {
        "task_info" : {"obs_shape" : obs_shape, "action_shape" : action_shape, "action_dim": action_dim},
        "transition" : {"net" : dynamics_model, "opt" : dynamics_optim, "adv_opt" : dynamics_adv_optim, 
                        "scaler": dynamics_scaler, "_terminal_fn" : _termination_fn},
        "actor" : {"net" : actor, "opt" : actor_optim},
        "alpha" : {"net" : alpha, "opt" : alpha_optim},
        "critic" : {"net" : [critic1, critic2], "opt" : [critic1_optim, critic2_optim]},
    }


class AlgoTrainer(BaseAlgo):
    def __init__(self, algo_init, args):
        super(AlgoTrainer, self).__init__(args)
        self.args = args

        self.obs_shape = algo_init['task_info']['obs_shape']
        self.action_shape = algo_init['task_info']['action_shape']
        self.action_dim = algo_init['task_info']['action_dim']

        self.dynamics_model = algo_init['transition']['net']
        self.dynamics_optim = algo_init['transition']['opt']
        self.dynamics_adv_optim = algo_init['transition']['adv_opt']
        self.dynamics_scaler = algo_init['transition']['scaler']
        self._terminal_fn = algo_init['transition']['_terminal_fn']

        self.actor = algo_init['actor']['net']
        self.actor_optim = algo_init['actor']['opt']

        self._is_auto_alpha = False
        self.alpha_optim = algo_init['alpha']['opt']
        if self.alpha_optim is not None:
            self._is_auto_alpha = True
            self._target_entropy, self._log_alpha, self.alpha_optim = algo_init['alpha']['net']
            self._alpha = self._log_alpha.detach().exp()
        else:
            self._alpha = algo_init['alpha']['net']

        self.critic1, self.critic2 = algo_init['critic']['net']
        self.target_critic1 = deepcopy(self.critic1)
        self.target_critic1.eval()
        self.target_critic2 = deepcopy(self.critic2)
        self.target_critic2.eval()
        self.critic1_optim, self.critic2_optim = algo_init['critic']['opt']

        self.device = args['device']
        self._tau = self.args['soft_target_tau']
        self._gamma = self.args['discount']

    def train_mode(self) -> None:
        self.actor.train()
        self.critic1.train()
        self.critic2.train()

    def eval_mode(self) -> None:
        self.actor.eval()
        self.critic1.eval()
        self.critic2.eval()

    def set_scaler(self, obs_mean, obs_std):
        termination_fn = obs_unnormalization(self._terminal_fn, obs_mean, obs_std)
        dynamics = EnsembleDynamics(self.dynamics_model,
                                    self.dynamics_optim,
                                    self.dynamics_scaler,
                                    termination_fn,
                                    )
        policy_scaler = StandardScaler(mu=obs_mean, std=obs_std)
        return termination_fn, dynamics, policy_scaler

    def set_data_buffer(self, buffer):
        real_buffer = ReplayBuffer(buffer_size=len(buffer["obs"]),
                                   obs_shape=self.args['obs_shape'],
                                   obs_dtype=np.float32,
                                   action_dim=self.action_dim,
                                   action_dtype=np.float32,
                                   device=self.args['device']
                                   )
        real_buffer.load_dataset(buffer)
        self.obs_max = np.concatenate([real_buffer.observations, real_buffer.next_observations], axis=0).max(axis=0)
        self.obs_min = np.concatenate([real_buffer.observations, real_buffer.next_observations], axis=0).min(axis=0)
        self.rew_max = np.concatenate([real_buffer.rewards, real_buffer.rewards], axis=0).max(axis=0)
        self.rew_min = np.concatenate([real_buffer.rewards, real_buffer.rewards], axis=0).min(axis=0)

        obs_mean, obs_std = real_buffer.normalize_obs()
        fake_buffer_size = self.args['steps_per_epoch'] // self.args["rollout_freq"] * \
                            self.args["model_retain_epochs"] * self.args["rollout_batch_size"] * self.args["horizon"]
        fake_buffer = ReplayBuffer(buffer_size=fake_buffer_size, 
                                   obs_shape=self.args['obs_shape'],
                                   obs_dtype=np.float32,
                                   action_dim=self.action_dim,
                                   action_dtype=np.float32,
                                   device=self.args['device']
                                   )
        return real_buffer, fake_buffer, obs_mean, obs_std

    def train(self, train_buffer, val_buffer, callback_fn):
        total_buffer = train_buffer
        if val_buffer is not None:
            for k, v in train_buffer.items():
                total_buffer[k] = np.concatenate([total_buffer[k], val_buffer[k]], axis=0)

        self.real_buffer, self.fake_buffer, obs_mean, obs_std = self.set_data_buffer(total_buffer)
        self.termination_fn, self.dynamics, self.policy_scaler = self.set_scaler(obs_mean, obs_std)
        self.actor.set_scaler(self.policy_scaler)

        if self.args['policy_bc_path'] is not None:
            self.actor = torch.load(os.path.join(self.args['policy_bc_path'], "actor.pt"), map_location='cpu').to(self.device)
            self.actor.scaler.load_scaler(self.args['policy_bc_path'], surfix="policy_")
            self.actor_optim = torch.optim.Adam(self.actor.parameters(), lr=self.args['actor_lr'])
        else:
            self.pretrain_policy(self.real_buffer.sample_all())
            if self.args['policy_bc_save_path'] is not None: 
                torch.save(self.actor, os.path.join(self.args['policy_bc_save_path'], "actor.pt"))
                self.actor.scaler.save_scaler(self.args['policy_bc_save_path'], surfix="policy_")

        if self.args['dynamics_path'] is not None:
            self.dynamics.model = torch.load(os.path.join(self.args['dynamics_path'], "dynamics_model.pt"), map_location='cpu').to(self.device)
            self.dynamics.scaler.load_scaler(self.args['dynamics_path'], surfix="dynamics_")
            self.dynamics_adv_optim = torch.optim.Adam(self.dynamics.model.parameters(), lr=self.args['transition_adv_lr'])
        else:
            self.train_transition(self.real_buffer.sample_all())
            if self.args['dynamics_save_path'] is not None: 
                torch.save(self.dynamics.model, os.path.join(self.args['dynamics_save_path'], "dynamics_model.pt"))
                self.dynamics.scaler.save_scaler(self.args['dynamics_save_path'], surfix="dynamics_")

        self.train_policy(callback_fn)
    
    def get_policy(self):
        return self.actor
    
    def pretrain_policy(self, data) -> None:
        batch_size = self.args['policy_bc_batch_size']
        self._bc_optim = torch.optim.Adam(self.actor.parameters(), lr=self.args['policy_bc_lr'])
        observations = data["observations"]
        actions = data["actions"]
        sample_num = observations.shape[0]
        idxs = np.arange(sample_num)
        print("Pretraining policy")
        self.actor.train()
        for epoch in range(self.args['policy_bc_epoch']):
            np.random.shuffle(idxs)
            sum_loss = 0
            for i_batch in range(sample_num // batch_size):
                batch_obs = observations[i_batch * batch_size: (i_batch + 1) * batch_size]
                batch_act = actions[i_batch * batch_size: (i_batch + 1) * batch_size]
                batch_obs = torch.from_numpy(batch_obs).to(self.device)
                batch_act = torch.from_numpy(batch_act).to(self.device)
                dist = self.actor(batch_obs)
                pred_actions, _ = dist.rsample()
                bc_loss = ((pred_actions - batch_act) ** 2).mean()

                self._bc_optim.zero_grad()
                bc_loss.backward()
                self._bc_optim.step()
                sum_loss += bc_loss.cpu().item()
            print(f"Epoch {epoch}, mean bc loss {sum_loss/i_batch}")
        return  

    def dynamics_learn(self, inputs, targets, batch_size, logvar_loss_coef):
        self.dynamics.model.train()
        train_size = inputs.shape[1]
        losses = []

        for batch_num in range(int(np.ceil(train_size / batch_size))):
            inputs_batch = inputs[:, batch_num * batch_size:(batch_num + 1) * batch_size]
            targets_batch = targets[:, batch_num * batch_size:(batch_num + 1) * batch_size]
            targets_batch = torch.as_tensor(targets_batch).to(self.dynamics.model.device)
            
            mean, logvar = self.dynamics.model(inputs_batch)
            inv_var = torch.exp(-logvar)
            # Average over batch and dim, sum over ensembles.
            mse_loss_inv = (torch.pow(mean - targets_batch, 2) * inv_var).mean(dim=(1, 2))
            var_loss = logvar.mean(dim=(1, 2))
            loss = mse_loss_inv.sum() + var_loss.sum()
            loss = loss + self.dynamics.model.get_decay_loss()
            loss = loss + logvar_loss_coef * \
                    self.dynamics.model.max_logvar.sum() - \
                    logvar_loss_coef * self.dynamics.model.min_logvar.sum()

            self.dynamics_optim.zero_grad()
            loss.backward()
            self.dynamics_optim.step()

            losses.append(loss.item())
        return np.mean(losses).item()

    def train_transition(self, data):
        inputs, targets = self.dynamics.format_samples_for_training(data)
        data_size = inputs.shape[0]
        val_size = min(int(data_size * self.args['val_ratio']), 1000)
        train_size = data_size - val_size
        train_splits, val_splits = torch.utils.data.random_split(range(data_size), (train_size, val_size))
        train_inputs, train_targets = inputs[train_splits.indices], targets[train_splits.indices]
        val_inputs, val_targets = inputs[val_splits.indices], targets[val_splits.indices]

        self.dynamics.scaler.fit(train_inputs)
        train_inputs = self.dynamics.scaler.transform(train_inputs)
        val_inputs = self.dynamics.scaler.transform(val_inputs)
        val_losses = [1e10 for i in range(self.dynamics.model.num_ensemble)]

        data_idxes = np.random.randint(train_size, size=[self.dynamics.model.num_ensemble, train_size])
        def shuffle_rows(arr):
            idxes = np.argsort(np.random.uniform(size=arr.shape), axis=-1)
            return arr[np.arange(arr.shape[0])[:, None], idxes]

        epoch = 0
        cnt = 0
        while True:
            epoch += 1
            train_loss = self.dynamics_learn(train_inputs[data_idxes], train_targets[data_idxes], self.args['transition_batch_size'], self.args['logvar_loss_coef'])
            new_val_losses = self.validate(val_inputs, val_targets)
            print(f"epoch: {epoch}, val loss: {new_val_losses}")

            val_loss = (np.sort(new_val_losses)[:self.dynamics.model.num_elites]).mean().item()
            self.log_res(epoch, {"loss/dynamics_train_loss": train_loss, "loss/dynamics_val_loss": val_loss})

            # shuffle data for each base learner
            data_idxes = shuffle_rows(data_idxes)

            indexes = []
            for i, new_loss, old_loss in zip(range(len(val_losses)), new_val_losses, val_losses):
                improvement = (old_loss - new_loss) / old_loss
                if improvement > 1e-2:
                    indexes.append(i)
                    val_losses[i] = new_loss

            if len(indexes) > 0:
                self.dynamics.model.update_save(indexes)
                cnt = 0
            else:
                cnt += 1

            if (cnt >= self.args['max_epochs_since_update']) or (self.args['transition_max_epochs'] is not None and (epoch >= self.args['transition_max_epochs'])):
                break

        indexes = self.dynamics.select_elites(val_losses)
        self.dynamics.model.set_elites(indexes)
        self.dynamics.model.load_save()
        # self.dynamics.save(logger.model_dir)
        self.dynamics.model.eval()
        print("elites:{} , val loss: {}".format(indexes, (np.sort(val_losses)[:self.dynamics.model.num_elites]).mean()))

    def rollout(self, init_obss, horizon):
        num_transitions = 0
        rewards_arr = np.array([])
        rollout_transitions = defaultdict(list)

        # rollout
        observations = init_obss
        for _ in range(horizon):
            actions = self.select_action(observations)
            next_observations, rewards, terminals, info = self.dynamics.step(observations, actions)
            if self.args['trainsition_clip']:
                next_observations = np.clip(next_observations, self.obs_min, self.obs_max)
                rewards = np.clip(rewards, self.rew_min, self.rew_max)

            rollout_transitions["obss"].append(observations)
            rollout_transitions["next_obss"].append(next_observations)
            rollout_transitions["actions"].append(actions)
            rollout_transitions["rewards"].append(rewards)
            rollout_transitions["terminals"].append(terminals)

            num_transitions += len(observations)
            rewards_arr = np.append(rewards_arr, rewards.flatten())

            nonterm_mask = (~terminals).flatten()
            if nonterm_mask.sum() == 0:
                break

            observations = next_observations[nonterm_mask]
        
        for k, v in rollout_transitions.items():
            rollout_transitions[k] = np.concatenate(v, axis=0)

        return rollout_transitions, {"num_transitions": num_transitions, "reward_mean": rewards_arr.mean().item()}

    def train_policy(self, callback_fn):
        num_timesteps = 0
        for epoch in range(self.args['max_epoch']):

            self.train_mode()

            for _ in range(self.args['steps_per_epoch']):
                if num_timesteps % self.args['rollout_freq'] == 0:
                    # collect data
                    init_obss = self.real_buffer.sample(int(self.args['rollout_batch_size']))["observations"].cpu().numpy()
                    rollout_transitions, rollout_info = self.rollout(init_obss, self.args['horizon'])
                    self.fake_buffer.add_batch(**rollout_transitions)

                real_sample_size = int(self.args['policy_batch_size'] * self.args['real_data_ratio'])
                fake_sample_size = self.args['policy_batch_size'] - real_sample_size
                real_batch = self.real_buffer.sample(batch_size=real_sample_size)
                fake_batch = self.fake_buffer.sample(batch_size=fake_sample_size)
                batch = {"real": real_batch, "fake": fake_batch}
                loss = self.policy_learn(batch)

                log_flag = False
                # update transition
                if self.args['dynamics_update_freq'] > 0 and (num_timesteps+1) % self.args['dynamics_update_freq'] == 0:
                    log_flag = True
                    all_loss_info = self.update_transition(self.real_buffer)

                num_timesteps += 1
            
            self.log_res(epoch, loss)
            if log_flag:
                self.log_res(epoch, all_loss_info)

            val_freq = self.args.get("val_frequency", 1)
            if epoch % val_freq == 0:
                res = callback_fn(self.get_policy())
            else:
                res = {}

            self.log_res(epoch, res)

        return self.get_policy()
    
    def update_transition(self, real_buffer):
        all_loss_info = {"adv_dynamics_update/all_loss": 0, 
                         "adv_dynamics_update/sl_loss": 0, 
                         "adv_dynamics_update/adv_loss": 0, 
                         "adv_dynamics_update/adv_advantage": 0, 
                         "adv_dynamics_update/adv_log_prob": 0, 
                         }
        self.dynamics.model.train()
        steps = 0
        while steps < self.args['adv_train_steps']:
            init_obss = real_buffer.sample(self.args['adv_rollout_batch_size'])["observations"].cpu().numpy()
            observations = init_obss
            for t in range(self.args['adv_rollout_length']):
                actions = self.select_action(observations)
                sl_observations, sl_actions, sl_next_observations, sl_rewards = \
                    itemgetter("observations", "actions", "next_observations", "rewards")(real_buffer.sample(self.args['adv_rollout_batch_size']))
                next_observations, terminals, loss_info = self.dynamics_step_and_forward(observations, actions, sl_observations, sl_actions, sl_next_observations, sl_rewards)
                if self.args['trainsition_clip']:
                    next_observations = np.clip(next_observations, self.obs_min, self.obs_max)
                for _key in loss_info:
                    all_loss_info[_key] += loss_info[_key]
                steps += 1
                observations = next_observations.copy()
                if steps == 1000:
                    break
        self.dynamics.model.eval()
        return {_key: _value / steps for _key, _value in all_loss_info.items()}

    def dynamics_step_and_forward(self, observations, actions, sl_observations, sl_actions, sl_next_observations, sl_rewards):
        obs_act = np.concatenate([observations, actions], axis=-1)
        obs_act = self.dynamics.scaler.transform(obs_act)
        diff_mean, logvar = self.dynamics.model(obs_act)
        observations = torch.from_numpy(observations).to(diff_mean.device)
        diff_obs, diff_reward = torch.split(diff_mean, [diff_mean.shape[-1]-1, 1], dim=-1)
        mean = torch.cat([diff_obs + observations, diff_reward], dim=-1)
        std = torch.sqrt(torch.exp(logvar))
        dist = torch.distributions.Normal(mean, std)
        ensemble_sample = dist.sample()
        ensemble_size, batch_size, _ = ensemble_sample.shape

        # select the next observations
        selected_indexes = self.dynamics.model.random_elite_idxs(batch_size)
        sample = ensemble_sample[selected_indexes, np.arange(batch_size)]
        next_observations = sample[..., :-1]
        rewards = sample[..., -1:]
        terminals = self.dynamics.terminal_fn(observations.detach().cpu().numpy(), actions, next_observations.detach().cpu().numpy())

        # compute logprob
        log_prob = dist.log_prob(sample).sum(-1, keepdim=True)
        log_prob = log_prob[self.dynamics.model.elites.data, ...]
        prob = log_prob.double().exp()
        prob = prob * (1/len(self.dynamics.model.elites.data))
        log_prob = prob.sum(0).log().type(torch.float32)

        # compute the advantage
        with torch.no_grad():
            next_actions, next_policy_log_prob = self.actforward(next_observations, deterministic=True)
            next_q = torch.minimum(
                self.critic1(next_observations, next_actions), 
                self.critic2(next_observations, next_actions)
            )
            if self.args['include_ent_in_adv']:
                next_q = next_q - self._alpha * next_policy_log_prob

            value = rewards + (1-torch.from_numpy(terminals).to(mean.device).float()) * self._gamma * next_q

            value_baseline = torch.minimum(
                self.critic1(observations, actions), 
                self.critic2(observations, actions)
            )
            advantage = value - value_baseline
            advantage = (advantage - advantage.mean()) / (advantage.std()+1e-6)
        adv_loss = (log_prob * advantage).mean()

        # compute the supervised loss
        sl_input = torch.cat([sl_observations, sl_actions], dim=-1).cpu().numpy()
        sl_target = torch.cat([sl_next_observations - sl_observations, sl_rewards], dim=-1)
        sl_input = self.dynamics.scaler.transform(sl_input)
        sl_mean, sl_logvar = self.dynamics.model(sl_input)
        sl_inv_var = torch.exp(-sl_logvar)
        sl_mse_loss_inv = (torch.pow(sl_mean - sl_target, 2) * sl_inv_var).mean(dim=(1, 2))
        sl_var_loss = sl_logvar.mean(dim=(1, 2))
        sl_loss = sl_mse_loss_inv.sum() + sl_var_loss.sum()
        sl_loss = sl_loss + self.dynamics.model.get_decay_loss()
        sl_loss = sl_loss + 0.001 * self.dynamics.model.max_logvar.sum() - 0.001 * self.dynamics.model.min_logvar.sum()

        all_loss = self.args['adv_weight'] * adv_loss + sl_loss

        self.dynamics_adv_optim.zero_grad()
        all_loss.backward()
        self.dynamics_adv_optim.step()

        return next_observations.cpu().numpy(), terminals, {"adv_dynamics_update/adv_loss": adv_loss.cpu().item(), 
                                                            "adv_dynamics_update/sl_loss": sl_loss.cpu().item(),
                                                            "adv_dynamics_update/all_loss": all_loss.cpu().item(),
                                                            "adv_dynamics_update/adv_advantage": advantage.mean().cpu().item(),
                                                            "adv_dynamics_update/adv_log_prob": log_prob.mean().cpu().item()}
        
    @ torch.no_grad()
    def validate(self, inputs: np.ndarray, targets: np.ndarray):
        self.dynamics.model.eval()
        targets = torch.as_tensor(targets).to(self.dynamics.model.device)
        mean, _ = self.dynamics.model(inputs)
        loss = ((mean - targets) ** 2).mean(dim=(1, 2))
        val_loss = list(loss.cpu().numpy())
        return val_loss
        
    def _sync_weight(self) -> None:
        for o, n in zip(self.target_critic1.parameters(), self.critic1.parameters()):
            o.data.copy_(o.data * (1.0 - self._tau) + n.data * self._tau)
        for o, n in zip(self.target_critic2.parameters(), self.critic2.parameters()):
            o.data.copy_(o.data * (1.0 - self._tau) + n.data * self._tau)

    def actforward(self, obs: torch.Tensor, deterministic: bool = False) -> tuple:
        dist = self.actor(obs)
        if deterministic:
            squashed_action, raw_action = dist.mode()
        else:
            squashed_action, raw_action = dist.rsample()
        log_prob = dist.log_prob(squashed_action, raw_action)
        return squashed_action, log_prob
    
    def select_action(self, obs: np.ndarray, deterministic: bool = False) -> np.ndarray:
        with torch.no_grad():
            action, _ = self.actforward(obs, deterministic)
        return action.cpu().numpy()

    def policy_learn(self, batch):
        real_batch, fake_batch = batch["real"], batch["fake"]
        mix_batch = {k: torch.cat([real_batch[k], fake_batch[k]], 0) for k in real_batch.keys()}

        obss, actions, next_obss, rewards, terminals = mix_batch["observations"], mix_batch["actions"], \
            mix_batch["next_observations"], mix_batch["rewards"], mix_batch["terminals"]

        # update critic
        q1, q2 = self.critic1(obss, actions), self.critic2(obss, actions)
        with torch.no_grad():
            next_actions, next_log_probs = self.actforward(next_obss)
            next_q = torch.min(
                self.target_critic1(next_obss, next_actions), self.target_critic2(next_obss, next_actions)
            ) - self._alpha * next_log_probs
            target_q = rewards + self._gamma * (1 - terminals) * next_q

        critic1_loss = ((q1 - target_q).pow(2)).mean()
        self.critic1_optim.zero_grad()
        critic1_loss.backward()
        self.critic1_optim.step()

        critic2_loss = ((q2 - target_q).pow(2)).mean()
        self.critic2_optim.zero_grad()
        critic2_loss.backward()
        self.critic2_optim.step()

        # update actor
        a, log_probs = self.actforward(obss)
        q1a, q2a = self.critic1(obss, a), self.critic2(obss, a)

        actor_loss = - torch.min(q1a, q2a).mean() + self._alpha * log_probs.mean()
        self.actor_optim.zero_grad()
        actor_loss.backward()
        self.actor_optim.step()

        if self._is_auto_alpha:
            log_probs = log_probs.detach() + self._target_entropy
            alpha_loss = -(self._log_alpha * log_probs).mean()
            self.alpha_optim.zero_grad()
            alpha_loss.backward()
            self.alpha_optim.step()
            self._alpha = torch.clamp(self._log_alpha.detach().exp(), 0.0, 1.0)

        self._sync_weight()

        result = {
            "loss/actor": actor_loss.item(),
            "loss/critic1": critic1_loss.item(),
            "loss/critic2": critic2_loss.item(),
        }

        if self._is_auto_alpha:
            result["loss/alpha"] = alpha_loss.item()
            result["alpha"] = self._alpha.item()

        return result
