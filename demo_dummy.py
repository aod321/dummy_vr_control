
#%%
from dummy_env import DummyEnv

left_arm_env = DummyEnv(arm_type='left', arm_serial='395D36713233')
right_arm_env = DummyEnv(arm_type='right', arm_serial='395136713233')
obs = left_arm_env.reset()
right_obs = right_arm_env.reset()
obs['right'] = right_obs['right']
# %%
import numpy as np
from telemoma.human_interface.teleop_policy import TeleopPolicy
from importlib.machinery import SourceFileLoader

def get_random_action():
    return {
        'base': np.random.uniform(-1, 1, 3),
        'torso': np.random.uniform(-1, 1, 1),
        'left': np.random.uniform(-1, 1, 7),
        'right': np.random.uniform(-1, 1, 7),
    }

teleop_config = SourceFileLoader('conf', 'vr_config.py').load_module().teleop_config
teleop = TeleopPolicy(teleop_config)
teleop.start()

for i in range(1000):
    action = teleop.get_action(obs)
    print(action)
    buttons = action.extra['buttons'] if 'buttons' in action.extra else {}

    if buttons.get('A', False) or buttons.get('B', False):
        break
        
    obs, _, _, _ = left_arm_env.step(action)
    obs, _, _, _ = right_arm_env.step(action)

teleop.stop()
left_arm_env.close()
# %%
