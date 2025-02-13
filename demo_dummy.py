import numpy as np
from telemoma.robot_interface.igibson import *
from telemoma.human_interface.teleop_policy import TeleopPolicy
from importlib.machinery import SourceFileLoader

download_assets()
download_demo_data()
env = FetchEnv() if args.robot=='fetch' else TiagoEnv()

teleop_config = SourceFileLoader('conf', args.teleop_config).load_module().teleop_config
teleop = TeleopPolicy(teleop_config)
teleop.start()

obs = env.reset()
for i in range(1000):
    action = teleop.get_action(obs) # get_random_action()
    print(action)
    buttons = action.extra['buttons'] if 'buttons' in action.extra else {}

    if buttons.get('A', False) or buttons.get('B', False):
        break

    obs, _, _, _ = env.step(action)
    
teleop.stop()
env.close()
