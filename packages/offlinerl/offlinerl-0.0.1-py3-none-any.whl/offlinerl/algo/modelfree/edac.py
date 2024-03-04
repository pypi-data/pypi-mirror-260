# Conservative Q-Learning for Offline Reinforcement Learning
# https://arxiv.org/abs/2006.04779
# https://github.com/aviralkumar2907/CQL
import copy
from datetime import datetime
from copy import deepcopy
import time

import torch
import numpy as np
from torch import nn
from torch import optim
from loguru import logger

from offlinerl.algo.base import BaseAlgo
from offlinerl.utils.net.common import Net

from offlinerl.utils.net.continuous import EnsembleCritic
from offlinerl.utils.net.tanhpolicy import TanhGaussianPolicy
from offlinerl.utils.exp import setup_seed
# from torch.utils.tensorboard import SummaryWriter

from typing import Tuple, Dict, List

import os
from collections import deque
from tqdm import tqdm


def algo_init(args):
    logger.info('Run algo_init function')

    setup_seed(args['seed'])
    _temp_time =str(datetime.now().strftime("%Y%m%d-%H:%M"))
    args['current_time'] = _temp_time
    logger.info(f'current_time: {_temp_time}')

    if args["obs_shape"] and args["action_shape"]:
        obs_shape, action_shape = args["obs_shape"], args["action_shape"]
    elif "task" in args.keys():
        from offlinerl.utils.env import get_env_shape
        obs_shape, action_shape = get_env_shape(args['task'])
        args["obs_shape"], args["action_shape"] = obs_shape, action_shape
    else:
        raise NotImplementedError
    
    args['hidden_dims'] = [args['hidden_layer_size']]*(1+args['layer_num'])
    # actor_backbone = EDAC_MLP(input_dim=np.prod(args['obs_shape']), hidden_dims=args['hidden_dims'])
    actor_backbone = Net(layer_num = args['layer_num'], 
                     state_shape = args["obs_shape"], 
                     hidden_layer_size = args['hidden_layer_size'])
    # breakpoint()
    
    # dist = TanhDiagGaussian(
    #     latent_dim=args['hidden_layer_size'],# getattr(actor_backbone, "output_dim"),
    #     output_dim=args['action_shape'],
    #     unbounded=True,
    #     conditioned_sigma=True
    # )
    # actor = ActorProb(actor_backbone, dist, args['device'])
    actor = TanhGaussianPolicy(preprocess_net = actor_backbone,
                                action_shape = action_shape,
                                hidden_layer_size = args['hidden_layer_size'],
                                conditioned_sigma = True,
                                unbounded = True
                              ).to(args['device'])
    
    actor_optim = torch.optim.Adam(actor.parameters(), lr=args['actor_lr'])
    critics = EnsembleCritic(
        np.prod(args['obs_shape']), args['action_shape'], \
        args['hidden_dims'], num_ensemble=args['num_critics'], \
        device=args['device']
    )
    _temp_num_critics = args['num_critics']
    logger.info(f'num_critics: {_temp_num_critics}')
    # init as in the EDAC paper
    for layer in critics.model[::2]:
        torch.nn.init.constant_(layer.bias, 0.1)
    torch.nn.init.uniform_(critics.model[-1].weight, -3e-3, 3e-3)
    torch.nn.init.uniform_(critics.model[-1].bias, -3e-3, 3e-3)
    critics_optim = torch.optim.Adam(critics.parameters(), lr=args['critic_lr'])

    # if args['auto_alpha']:
    #     target_entropy = args['target_entropy'] if args['target_entropy'] \
    #         else -np.prod(args['action_shape'])
    #     args['target_entropy'] = target_entropy
    #     log_alpha = torch.zeros(1, requires_grad=True, device=args['device'])
    #     alpha_optim = torch.optim.Adam([log_alpha], lr=args['alpha_lr'])
    #     alpha = (target_entropy, log_alpha, alpha_optim)
    # else:
    #     alpha = args.alpha

        
    nets =  {
        "actor" : {"net" : actor, "opt" : actor_optim},
        "critics" : {"net" : critics, "opt" : critics_optim},
        "tau" : args['tau'],
        "gamma": args['gamma'],
        # "alpha" : alpha,
        "max_q_backup": args['max_q_backup'],
        "deterministic_backup": args['deterministic_backup'],
        "eta": args['eta'],
    }
                
    return nets


class AlgoTrainer(BaseAlgo):
    def __init__(self, algo_init, args):
        super(AlgoTrainer, self).__init__(args)
        self.args = args
        self.actor = algo_init['actor']['net']
        self.critics = algo_init['critics']['net']
        self.critics_old = deepcopy(self.critics)
        self.critics_old.eval()

        self.actor_optim = algo_init['actor']['opt']
        self.critics_optim = algo_init['critics']['opt']

        self._tau = algo_init['tau']
        self._gamma = algo_init['gamma']
        
        if args['auto_alpha']:
            target_entropy = args['target_entropy'] if args['target_entropy'] \
                else -np.prod(args['action_shape'])
            args['target_entropy'] = target_entropy
            log_alpha = torch.zeros(1, requires_grad=True, device=args['device'])
            alpha_optim = torch.optim.Adam([log_alpha], lr=args['alpha_lr'])
            algo_init['alpha'] = (target_entropy, log_alpha, alpha_optim)
        else:
            algo_init['alpha'] = args['alpha']
        
        self._is_auto_alpha = False
        if isinstance(algo_init['alpha'], tuple):
            self._is_auto_alpha = True
            self._target_entropy, self._log_alpha, self.alpha_optim = algo_init['alpha']
            self._alpha = self._log_alpha.detach().exp()
        else:
            self._alpha = algo_init['alpha']

        self._max_q_backup = algo_init['max_q_backup']
        self._deterministic_backup = algo_init['deterministic_backup']
        self._eta = algo_init['eta']
        self._num_critics = self.critics._num_ensemble

        # self.current_time = datetime.now().strftime("%Y%m%d%H%M")
        # logger.info(f'current_time: {self.current_time}')
        # self.writer = SummaryWriter(os.path.join(self.index_path, f"testing_tb_logs_{self.current_time}"))

        self._epoch = args['epoch']
        self._step_per_epoch = args['step_per_epoch']
        self._batch_size = args['batch_size']
        

    def net_train(self) -> None:
        self.actor.train()
        self.critics.train()

    def net_eval(self) -> None:
        self.actor.eval()
        self.critics.eval()

    def _sync_weight(self) -> None:
        for o, n in zip(self.critics_old.parameters(), self.critics.parameters()):
            o.data.copy_(o.data * (1.0 - self._tau) + n.data * self._tau)
    
    def actforward(
        self,
        obs: torch.Tensor,
        deterministic: bool = False
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        dist = self.actor(obs)
        if deterministic:
            # squashed_action, raw_action = dist.mode()
            squashed_action = dist.mode()

        else:
            squashed_action, raw_action = dist.rsample(return_pretanh_value=True)
        # log_prob = dist.log_prob(squashed_action, raw_action)
        log_prob = dist.log_prob(squashed_action, raw_action).sum(-1, keepdim=True)

        return squashed_action, log_prob


    def learn(self, batch: Dict) -> Dict:
        obss, actions, next_obss, rewards, terminals = \
            batch["obs"], batch["act"], batch["obs_next"], batch["rew"], batch["done"]
        
        if self._eta > 0:
            actions.requires_grad_(True)

        # update actor
        a, log_probs = self.actforward(obss)
        # qas: [num_critics, batch_size, 1]
        qas = self.critics(obss, a)
        actor_loss = -torch.min(qas, 0)[0].mean() + self._alpha * log_probs.mean()
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

        # update critic
        if self._max_q_backup:
            with torch.no_grad():
                batch_size = obss.shape[0]
                tmp_next_obss = next_obss.unsqueeze(1).repeat(1, 10, 1) \
                    .view(batch_size * 10, next_obss.shape[-1])
                tmp_next_actions, _ = self.actforward(tmp_next_obss)
                tmp_next_qs = self.critics_old(tmp_next_obss, tmp_next_actions) \
                    .view(self._num_critics, batch_size, 10, 1).max(2)[0] \
                    .view(self._num_critics, batch_size, 1)
                next_q = tmp_next_qs.min(0)[0]
        else:
            with torch.no_grad():
                next_actions, next_log_probs = self.actforward(next_obss)
                next_q = self.critics_old(next_obss, next_actions).min(0)[0]
                if not self._deterministic_backup:
                    next_q -= self._alpha * next_log_probs

        # target_q: [batch_size, 1]
        target_q = rewards + self._gamma * (1 - terminals) * next_q
        # qs: [num_critics, batch_size, 1]
        qs = self.critics(obss, actions)
        critics_loss = ((qs - target_q.unsqueeze(0)).pow(2)).mean(dim=(1, 2)).sum()

        if self._eta > 0:
            obss_tile = obss.unsqueeze(0).repeat(self._num_critics, 1, 1)
            actions_tile = actions.unsqueeze(0).repeat(self._num_critics, 1, 1).requires_grad_(True)
            qs_preds_tile = self.critics(obss_tile, actions_tile)
            qs_pred_grads, = torch.autograd.grad(qs_preds_tile.sum(), actions_tile, retain_graph=True, create_graph=True)
            qs_pred_grads = qs_pred_grads / (torch.norm(qs_pred_grads, p=2, dim=2).unsqueeze(-1) + 1e-10)
            qs_pred_grads = qs_pred_grads.transpose(0, 1)
            
            qs_pred_grads = torch.einsum('bik,bjk->bij', qs_pred_grads, qs_pred_grads)
            masks = torch.eye(self._num_critics, device=obss.device).unsqueeze(dim=0).repeat(qs_pred_grads.size(0), 1, 1)
            qs_pred_grads = (1 - masks) * qs_pred_grads
            grad_loss = torch.mean(torch.sum(qs_pred_grads, dim=(1, 2))) / (self._num_critics - 1)

            critics_loss += self._eta * grad_loss

        self.critics_optim.zero_grad()
        critics_loss.backward()
        self.critics_optim.step()

        self._sync_weight()

        result =  {
            "loss/actor": actor_loss.item(),
            "loss/critics": critics_loss.item()
        }

        if self._is_auto_alpha:
            result["loss/alpha"] = alpha_loss.item()
            result["alpha"] = self._alpha.item()
        
        return result

    def train(self, train_buffer, val_buffer, callback_fn):
        start_time = time.time()

        num_timesteps = 0
        last_10_performance = deque(maxlen=10)
        # train loop
        for e in range(1, self._epoch + 1):
            self.net_train()

            pbar = tqdm(range(self._step_per_epoch), desc=f"Epoch #{e}/{self._epoch}")
            for it in pbar:
                batch = train_buffer.sample(self._batch_size)
                batch = batch.to_torch(device=self.args['device'])
                loss = self.learn(batch)
                pbar.set_postfix(**loss)

                # for k, v in loss.items():
                #     self.writer.add_scalar(k, v, (e-1)*self.args["step_per_epoch"]+it)
                
                # num_timesteps += 1

            
            # evaluate current policy
            
            val_frequency = self.args.get("val_frequency",1)
            if (e+1) % val_frequency == 0:
                self.net_eval()
                res = callback_fn(self.get_policy())
                ep_reward_mean, ep_reward_std = res['Reward_Mean_Env'], res['Reward_Std_Env']
                ep_length_mean, ep_length_std = res['Length_Mean_Env'], res['Length_Std_Env']
                
                norm_ep_rew_mean = ep_reward_mean
                norm_ep_rew_std = ep_reward_std

                last_10_performance.append(norm_ep_rew_mean)
            else:
                res = {}

            res.update(loss)
            self.log_res(e, res)

            
            # self.writer.add_scalar("eval/normalized_episode_reward", norm_ep_rew_mean, e)
            # self.writer.add_scalar("eval/normalized_episode_reward_std", norm_ep_rew_std, e)
            # self.writer.add_scalar("eval/episode_length", ep_length_mean, e)
            # self.writer.add_scalar("eval/episode_length_std", ep_length_std, e)        
            # save checkpoint
            # torch.save(self.actor.state_dict(), os.path.join(self.index_path, f"testing_tb_logs_{self.current_time}", f"ep_{e}_policy.pth"))
            # logger.info("eval reward: {:.2f} +- {:.2f}".format(norm_ep_rew_mean, norm_ep_rew_std))

        logger.info("total time: {:.2f}s".format(time.time() - start_time))
        # torch.save(self.actor.state_dict(), os.path.join(self.index_path, f"testing_tb_logs_{self.current_time}", "last_step_policy.pth"))
        print({"last_10_performance": np.mean(last_10_performance)})
        return self.get_policy()

    # def _evaluate(self) -> Dict[str, List[float]]:
    #     self.net_eval.eval()
    #     obs,_ = self.eval_env.reset()
    #     eval_ep_info_buffer = []
    #     num_episodes = 0
    #     episode_reward, episode_length = 0, 0

    #     while num_episodes < self._eval_episodes:
    #         action = self.policy.select_action(obs.reshape(1,-1), deterministic=True)
    #         next_obs, reward, terminal, timeout,_ = self.eval_env.step(action.flatten())
    #         terminal = terminal or timeout
    #         episode_reward += reward
    #         episode_length += 1

    #         obs = next_obs

    #         if terminal:
    #             eval_ep_info_buffer.append(
    #                 {"episode_reward": episode_reward, "episode_length": episode_length}
    #             )
    #             num_episodes +=1
    #             episode_reward, episode_length = 0, 0
    #             obs,_ = self.eval_env.reset()
        
    #     return {
    #         "eval/episode_reward": [ep_info["episode_reward"] for ep_info in eval_ep_info_buffer],
    #         "eval/episode_length": [ep_info["episode_length"] for ep_info in eval_ep_info_buffer]
    #     }
    
        
    def get_model(self):
        return self.actor
    
    #def save_model(self, model_save_path):
    #    torch.save(self.actor, model_save_path)
        
    def get_policy(self):
        return self.actor
    
    # def train(self, train_buffer, val_buffer, callback_fn):
    #     for epoch in range(1,self.args["max_epoch"]+1):
    #         for step in range(1,self.args["steps_per_epoch"]+1):
    #             train_data = train_buffer.sample(self.args["batch_size"])
    #             self._train(train_data)
            
    #         res = callback_fn(self.get_policy())

    #         self.log_res(epoch, res)
            
    #     return self.get_policy()