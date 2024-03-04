import torch
from offlinerl.utils.exp import select_free_cuda

task = "Simglucose"
task_data_type = "medium"
task_train_num = 99

seed = 42

device = 'cuda'+":"+str(select_free_cuda()) if torch.cuda.is_available() else 'cpu'
obs_shape = None
act_shape = None
max_action = None
mode = "normalize"

# model save path
policy_bc_path = None
policy_bc_save_path = None
dynamics_path = None
dynamics_save_path = None

# transition model train
transition_init_num = 7
transition_select_num = 5
val_ratio = 0.1
max_epochs_since_update = 10
transition_max_epochs = None


# network strtucture
hidden_layer_size = 256
hidden_layers = 4
transition_layers = 4

real_data_ratio = 0.5

policy_bc_batch_size = 256
transition_batch_size = 256
rollout_batch_size = 50000
policy_batch_size = 256

policy_bc_epoch = 50

steps_per_epoch = 1000
max_epoch = 2000

actor_lr = 1e-4
alpha_lr = 1e-4
transition_lr = 1e-3
transition_adv_lr = 3e-4
critic_lr = 3e-4
policy_bc_lr = 1e-4
dynamics_weight_decay = [2.5e-5, 5e-5, 7.5e-5, 7.5e-5, 1e-4]
logvar_loss_coef = 1e-3

learnable_alpha = True
alpha = 0.15

discount = 0.99
soft_target_tau = 0.005
target_entropy = None

horizon = 5

val_frequency = 10
eval_episodes = 100
rollout_freq = 250

# rambo config
dynamics_update_freq = 1000
adv_train_steps = 1000
adv_rollout_batch_size = 256
adv_rollout_length = 5
include_ent_in_adv = False
adv_weight = 3e-4

# ???
model_retain_epochs = 5

#tune
params_tune = {
    "buffer_size" : {"type" : "discrete", "value": [1e6, 2e6]},
    "real_data_ratio" : {"type" : "discrete", "value": [0.05, 0.1, 0.2]},
    "horzion" : {"type" : "discrete", "value": [1, 2, 5]},
    "lam" : {"type" : "continuous", "value": [0.1, 10]},
    "learnable_alpha" : {"type" : "discrete", "value": [True, False]},
}

#tune
grid_tune = {
    "horizon" : [2, 5],
    "adv_weight" : [0, 3e-4],
}