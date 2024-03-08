# Gradient Boosting Reinforcement Learning (GBRL)
GBRL is a Python-based GBT library designed and optimized for reinforcement learning (RL). GBRL is implemented in C++/CUDA aimed to seamlessly integrate within popular RL libraries. 

### Key Features:
- GBTs Tailored for RL: GBRL adapts the power of Gradient Boosting Trees to the unique challenges of RL environments, including non-stationarity and delayed feedback.
- Optimized Actor-Critic Architecture: GBRL features a shared tree-based structure for policy and value functions. This significantly reduces memory and computational overhead, enabling it to tackle complex, high-dimensional RL problems.
- Hardware Acceleration: GBRL leverages CUDA for hardware-accelerated computation, ensuring efficiency and speed.
- Seamless Integration: GBRL is designed for easy integration with popular RL libraries, making it readily accessible for practitioners.


## Getting started

```
pip install gbrl
```  

For GPU support GBRL looks for `CUDA_PATH` or `CUDA_HOME` environment variables. Unless found, GBRL will automatically compile only for CPU.

Verify that GPU is visible by running
```
import gbrl

gbrl.cuda_available()
```

*OPTIONAL*  
For tree visualization make sure graphviz is installed before compilation. 

## Usage Example in an RL library
```
import torch as th
from gbrl import ActorCriticGBRL
from stable_baselines3.common.distributions import CategoricalDistribution

### initialize model ###
# define tree structure parameters
tree_struct = {'max_depth': 4, 'min_data_in_leaf': 0, 'n_bins': 256, 'grow_policy': 'oblivious'}
# define gbrl parameters
gbrl_params = {'control_variates': False, 'split_score_func': 'cosine', 'generator_type': 'Quantile'}
# actor and critic optimizers
policy_optimizer = {'algo': 'SGD', 'lr': 0.05}
value_optimizer = {'algo': 'SGD', lr: '0.25'}

# Given action_space instance of gym.spaces.Space

model = ActorCriticGBRL(tree_struct=tree_struct, output_dim=action_space.n, pg_optimizer=policy_optimizer, value_optimizer=value_optimizer, shared_tree_struct=True, gbrl_params=gbrl_params, device='cuda')
model.init_model() 

action_dist = CategoricalDistribution(action_space.n)
### Training loop ### 
logits, values = model(obs) # returns numpy arrays
logits = th.tensor(logits, requires_grad=True)
values = th.tensor(values, requires_grad=True)

distribution = action_dist.proba_distribution(logits)
log_prob = distribution.log_prob(actions)

loss = ... calculate loss according to RL algorithm

loss.backward()

self.policy.fit(rollout_data., theta_grad, values_grad)

# calculate grads (GBRL fits numpy arrays)
logits_grads = logits.grad.detach().cpu().numpy() * len(obs) # gradients w.r.t to the *each sample
value_grads = values.grad.detach().cpu().numpy() * len(obs)

model.fit(obs, logits_grads, value_grads)
```

## Current Supported Features
### Tree Fitting
- Greedy (Depth-wise) tree building - (CPU/GPU)  
- Oblivious (Symmetric) tree building - (CPU/GPU)  
- L2 split score - (CPU/GPU)  
- Cosine split score - (CPU/GPU) 
- Uniform based candidate generation - (CPU/GPU)
- Quantile based candidate generation - (CPU/GPU)
- Supervised learning fitting / Multi-iteration fitting - (CPU/GPU)
    - MultiRMSE loss (only)
- Categorical Inputs
### GBT Inference
- SGD optimizer - (CPU/GPU)
- ADAM optimizer - (CPU only)
- Control Variates (gradient variance reduction technique) - (CPU only)
- Shared Tree for policy and value function - (CPU/GPU)
- Linear and constant learning rate scheduler - (CPU/GPU only constant)
- Support for up to two different optimizers (e.g, policy/value) - **(CPU/GPU if both are SGD)

## Citing 

