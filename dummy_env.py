from dataclasses import dataclass
import numpy as np
from scipy.spatial.transform import Rotation as R
from typing import Dict, Optional, Tuple, Any
import fibre
import ref_tool
from dummy_utils import EEFPose6D, get_dummy_eef_pose6d, convert_eef_to_telemoma_obs, convert_telemoma_action_to_eef

class DummyEnv:
    def __init__(self, arm_serial: str = "395136713233", arm_type:str = "left", init_reset=True):
        # Initialize robot connection
        self.logger = fibre.utils.Logger(verbose=True)
        self.drive = ref_tool.find_any(serial_number=arm_serial, logger=self.logger)
        if init_reset: 
            # Move to initial pose
            self.drive.robot.set_enable(True)
            self.work_pose = (0, 0, 90, 0, 90, 0)
            self.drive.robot.move_j(*self.work_pose)
        self.arm_type = arm_type
        
        # Get initial state
        self.current_pose = get_dummy_eef_pose6d(self.drive)

    def reset(self) -> Dict[str, Optional[np.ndarray]]:
        """Reset robot to work pose and return initial observation"""
        self.drive.robot.move_j(*self.work_pose)
        self.current_pose = get_dummy_eef_pose6d(self.drive)
        return convert_eef_to_telemoma_obs(self.current_pose)

    def step(self, action: Dict[str, np.ndarray]) -> Tuple[Dict[str, Optional[np.ndarray]], float, bool, Dict]:
        """Execute one environment step"""
        # Convert action dict to numpy array (assuming left arm control)
        action_np = np.array(action[self.arm_type])
        
        # Convert action to new target pose
        new_target_pose = convert_telemoma_action_to_eef(self.current_pose, action_np)
        
        # Execute movement
        new_target_pose_tuple = (
            new_target_pose.x, new_target_pose.y, new_target_pose.z,
            new_target_pose.a, new_target_pose.b, new_target_pose.c
        )
        self.drive.robot.move_l(*new_target_pose_tuple)
        
        # Update current pose
        self.current_pose = get_dummy_eef_pose6d(self.drive)
        
        # Get new observation
        obs = convert_eef_to_telemoma_obs(self.current_pose)
        
        # For now, return placeholder values for reward and done
        reward = 0.0
        done = False
        info = {}
        return obs, reward, done, info

    def close(self):
        """Cleanup resources"""
        self.drive.robot.set_enable(False)