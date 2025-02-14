from dataclasses import dataclass
from typing import Dict, Optional
import numpy as np
from scipy.spatial.transform import Rotation as R


@dataclass
class EEFPose6D:
    x: float  # mm
    y: float
    z: float
    a: float  # deg
    b: float
    c: float

def get_dummy_eef_pose6d(drive):
    drive.robot.eef_pose.update_pose_6D()
    pose = EEFPose6D(
        x=drive.robot.eef_pose.x,
        y=drive.robot.eef_pose.y,
        z=drive.robot.eef_pose.z,
        a=drive.robot.eef_pose.a,
        b=drive.robot.eef_pose.b,
        c=drive.robot.eef_pose.c
    )
    return pose

def convert_eef_to_telemoma_obs(eef_pose: EEFPose6D) -> Dict[str, Optional[np.ndarray]]:
    """将EEF 6D姿态转换为telemoma格式的observation
    
    Args:
        eef_pose: 机器人末端6D姿态 (x,y,z in mm, a,b,c in deg)
        
    Returns:
        telemoma格式的observation字典:
        {
            'left/right': np.array([x,y,z, qx,qy,qz,qw, gripper]) # 位置(m),四元数,夹持器
            'base': None,
            'torso': None
        }
    """
    # 1. 位置转换 (mm -> m)
    pos = np.array([
        eef_pose.x/1000.0,
        eef_pose.y/1000.0,
        eef_pose.z/1000.0
    ])
    
    # 2. 欧拉角(deg)转四元数
    # 注意:可能需要调整欧拉角顺序和符号以匹配您的机器人坐标系
    r = R.from_euler('xyz', [eef_pose.a, eef_pose.b, eef_pose.c], degrees=True)
    quat = r.as_quat()  # [qx, qy, qz, qw]
    
    # 3. 组合成完整的EEF状态 [pos(3), quat(4), gripper(1)]
    gripper = 0.0  # 假设夹持器关闭
    eef_state = np.concatenate([pos, quat, [gripper]])
    
    # 4. 构建完整的observation字典
    obs = {
        'left': eef_state,  # 如果控制左臂
        'right': None,      # 如果控制右臂则交换
        'base': None,
        'torso': None
    }
    
    return obs

def convert_telemoma_action_to_eef(current_pose: EEFPose6D, action: np.ndarray) -> EEFPose6D:
    """将telemoma的action转换为新的EEF目标位姿
    
    Args:
        current_pose: 当前EEF位姿
        action: telemoma格式的action [dx,dy,dz, rx,ry,rz, gripper]
               位置增量(m),欧拉角增量(rad),夹持器
               
    Returns:
        新的目标EEF位姿
    """
    # 1. 位置增量转换 (m -> mm)
    pos_delta = action[:3] * 1000.0
    
    # 2. 处理旋转
    # 当前欧拉角
    current_r = R.from_euler('xyz', [current_pose.a, current_pose.b, current_pose.c], degrees=True)
    
    # 增量旋转(rad -> deg)
    delta_r = R.from_euler('xyz', action[3:6], degrees=False)
    
    # 组合旋转
    new_r = delta_r * current_r
    new_euler = new_r.as_euler('xyz', degrees=True)
    
    # 3. 构建新的目标位姿
    new_pose = EEFPose6D(
        x=current_pose.x + pos_delta[0],
        y=current_pose.y + pos_delta[1],
        z=current_pose.z + pos_delta[2],
        a=new_euler[0],
        b=new_euler[1],
        c=new_euler[2]
    )
    
    return new_pose