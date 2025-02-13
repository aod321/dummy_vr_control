# %%
import fibre
import ref_tool
from __future__ import print_function
# logger verbose=True
logger = fibre.utils.Logger(verbose=True)
logger.info("Finding teach arm...")
teach_arm = ref_tool.find_any(serial_number="3950366E3233", logger=logger)
logger.info("Finding follow arm...")
follow_arm = ref_tool.find_any(serial_number="395D36713233", logger=logger)
logger.info(f"Teach arm found: {teach_arm}")
logger.info(f"Follow arm found: {follow_arm}")

# %%
logger.info("Moving Teach Arm to Home Position")
teach_arm.robot.set_enable(True)
teach_arm.robot.homing()

logger.info("Moving Follow Arm to Home Position")
follow_arm.robot.set_enable(True)
follow_arm.robot.homing()

logger.info("Moving Teach Arm to Push_T Pose")
teach_arm.robot.move_j(0, 0, 90, 0, 90, 0)

logger.info("Moving Lead Arm to Push_T Pose")
follow_arm.robot.move_j(0, 0, 90, 0, 90, 0)

logger.info("Teach Arm and Lead Arm are at Push_T Pose")

#%% Calculate joint angle offset of Teach Arm and Follow Arm
fixed_home_joint_angle = [0, 0, 90, 0, 90, 0]
teach_arm_joint1_angle_offset = teach_arm.robot.joint_1.angle - fixed_home_joint_angle[0]
teach_arm_joint2_angle_offset = teach_arm.robot.joint_2.angle - fixed_home_joint_angle[1]
teach_arm_joint3_angle_offset = teach_arm.robot.joint_3.angle - fixed_home_joint_angle[2]
teach_arm_joint4_angle_offset = teach_arm.robot.joint_4.angle - fixed_home_joint_angle[3]
teach_arm_joint5_angle_offset = teach_arm.robot.joint_5.angle - fixed_home_joint_angle[4]
teach_arm_joint6_angle_offset = teach_arm.robot.joint_6.angle - fixed_home_joint_angle[5]

lead_arm_joint1_angle_offset = follow_arm.robot.joint_1.angle - fixed_home_joint_angle[0]
lead_arm_joint2_angle_offset = follow_arm.robot.joint_2.angle - fixed_home_joint_angle[1]
lead_arm_joint3_angle_offset = follow_arm.robot.joint_3.angle - fixed_home_joint_angle[2]
lead_arm_joint4_angle_offset = follow_arm.robot.joint_4.angle - fixed_home_joint_angle[3]
lead_arm_joint5_angle_offset = follow_arm.robot.joint_5.angle - fixed_home_joint_angle[4]
lead_arm_joint6_angle_offset = follow_arm.robot.joint_6.angle - fixed_home_joint_angle[5]
logger.info(f"Teach Arm Joint Angle Offsets: {teach_arm_joint1_angle_offset}, {teach_arm_joint2_angle_offset}, {teach_arm_joint3_angle_offset}, {teach_arm_joint4_angle_offset}, {teach_arm_joint5_angle_offset}, {teach_arm_joint6_angle_offset}")
logger.info(f"Lead Arm Joint Angle Offsets: {lead_arm_joint1_angle_offset}, {lead_arm_joint2_angle_offset}, {lead_arm_joint3_angle_offset}, {lead_arm_joint4_angle_offset}, {lead_arm_joint5_angle_offset}, {lead_arm_joint6_angle_offset}")
# %%
teach_arm.robot.set_enable(False)
stop = False
import time
rate = 0.1  # 10Hz = 0.1s period
while not stop:
    start_time = time.time()
    joint1_angle = teach_arm.robot.joint_1.angle
    joint2_angle = teach_arm.robot.joint_2.angle
    joint3_angle = teach_arm.robot.joint_3.angle
    joint4_angle = teach_arm.robot.joint_4.angle
    joint5_angle = teach_arm.robot.joint_5.angle
    joint6_angle = teach_arm.robot.joint_6.angle
    print(f"Current Joints: {joint1_angle}, {joint2_angle}, {joint3_angle}, {joint4_angle}, {joint5_angle}, {joint6_angle}")
    follow_arm.robot.move_j(joint1_angle - lead_arm_joint1_angle_offset, joint2_angle - lead_arm_joint2_angle_offset, joint3_angle - lead_arm_joint3_angle_offset, joint4_angle - lead_arm_joint4_angle_offset, joint5_angle - lead_arm_joint5_angle_offset, joint6_angle - lead_arm_joint6_angle_offset)
    # Sleep precisely to maintain 10Hz
    elapsed = time.time() - start_time
    if elapsed < rate:
        time.sleep(rate - elapsed)
    
    # Calculate and print actual loop frequency
    loop_time = time.time() - start_time
    actual_freq = 1.0 / loop_time if loop_time > 0 else 0
    print(f"Current loop frequency: {actual_freq:.2f} Hz")

#%%
teach_arm.robot.set_enable(False)
# %%
teach_arm.robot.move_j(0, 70, 90, 0, 90, 0)

# %%

# %%
import cv2
import json
import numpy as np
import mediapy as mp
from datetime import datetime
import os
import cv2
hand_cam = cv2.VideoCapture("http://192.168.65.115:8080/?action=stream")
ext_cam = cv2.VideoCapture("http://192.168.65.110:8080/?action=stream")
fixed_home_joint_angle = [0, 0, 90, 0, 90, 0]
teach_arm_joint1_angle_offset = teach_arm.robot.joint_1.angle - fixed_home_joint_angle[0]
teach_arm_joint2_angle_offset = teach_arm.robot.joint_2.angle - fixed_home_joint_angle[1]
teach_arm_joint3_angle_offset = teach_arm.robot.joint_3.angle - fixed_home_joint_angle[2]
teach_arm_joint4_angle_offset = teach_arm.robot.joint_4.angle - fixed_home_joint_angle[3]
teach_arm_joint5_angle_offset = teach_arm.robot.joint_5.angle - fixed_home_joint_angle[4]
teach_arm_joint6_angle_offset = teach_arm.robot.joint_6.angle - fixed_home_joint_angle[5]

lead_arm_joint1_angle_offset = follow_arm.robot.joint_1.angle - fixed_home_joint_angle[0]
lead_arm_joint2_angle_offset = follow_arm.robot.joint_2.angle - fixed_home_joint_angle[1]
lead_arm_joint3_angle_offset = follow_arm.robot.joint_3.angle - fixed_home_joint_angle[2]
lead_arm_joint4_angle_offset = follow_arm.robot.joint_4.angle - fixed_home_joint_angle[3]
lead_arm_joint5_angle_offset = follow_arm.robot.joint_5.angle - fixed_home_joint_angle[4]
lead_arm_joint6_angle_offset = follow_arm.robot.joint_6.angle - fixed_home_joint_angle[5]
logger.info(f"Teach Arm Joint Angle Offsets: {teach_arm_joint1_angle_offset}, {teach_arm_joint2_angle_offset}, {teach_arm_joint3_angle_offset}, {teach_arm_joint4_angle_offset}, {teach_arm_joint5_angle_offset}, {teach_arm_joint6_angle_offset}")
logger.info(f"Lead Arm Joint Angle Offsets: {lead_arm_joint1_angle_offset}, {lead_arm_joint2_angle_offset}, {lead_arm_joint3_angle_offset}, {lead_arm_joint4_angle_offset}, {lead_arm_joint5_angle_offset}, {lead_arm_joint6_angle_offset}")
# Create output directory with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"data_collection_{timestamp}"
os.makedirs(output_dir, exist_ok=True)

# Initialize video writers and data storage
hand_frames = []
ext_frames = []
eef_poses = []

teach_arm.robot.set_enable(False)
stop = False
import time
rate = 0.1  # 10Hz = 0.1s period

try:
    while not stop:
        start_time = time.time()
        
        # Get current joint angles
        joint1_angle = teach_arm.robot.joint_1.angle
        joint2_angle = teach_arm.robot.joint_2.angle
        joint3_angle = teach_arm.robot.joint_3.angle
        joint4_angle = teach_arm.robot.joint_4.angle
        joint5_angle = teach_arm.robot.joint_5.angle
        joint6_angle = teach_arm.robot.joint_6.angle
        
        # Get current end-effector pose
        teach_eef_pose = teach_arm.robot.eef_pose.update_pose_6D()
        teach_eef_pose = teach_arm.robot.eef_pose.x, teach_arm.robot.eef_pose.y, teach_arm.robot.eef_pose.z, teach_arm.robot.eef_pose.a, teach_arm.robot.eef_pose.b, teach_arm.robot.eef_pose.c
        eef_poses.append({
            'timestamp': time.time(),
            'position': list(teach_eef_pose[:3]),
            'orientation': list(teach_eef_pose[3:])
        })
        
        # Capture frames from both cameras
        ret_hand, hand_frame = hand_cam.read()
        ret_ext, ext_frame = ext_cam.read()
        
        if ret_hand and ret_ext:
            hand_frames.append(hand_frame)
            ext_frames.append(ext_frame)
        
        # Move follow arm
        follow_arm.robot.move_j(
            joint1_angle - lead_arm_joint1_angle_offset,
            joint2_angle - lead_arm_joint2_angle_offset,
            joint3_angle - lead_arm_joint3_angle_offset,
            joint4_angle - lead_arm_joint4_angle_offset,
            joint5_angle - lead_arm_joint5_angle_offset,
            joint6_angle - lead_arm_joint6_angle_offset
        )
        
        # Print status
        print(f"Current Joints: {joint1_angle}, {joint2_angle}, {joint3_angle}, {joint4_angle}, {joint5_angle}, {joint6_angle}")
        
        # Maintain loop rate
        elapsed = time.time() - start_time
        if elapsed < rate:
            time.sleep(rate - elapsed)
        
        loop_time = time.time() - start_time
        actual_freq = 1.0 / loop_time if loop_time > 0 else 0
        print(f"Current loop frequency: {actual_freq:.2f} Hz")

except KeyboardInterrupt:
    print("\nStopping data collection...")
finally:
    # Save collected data
    print("Saving data...")
    
    # Save videos
    if hand_frames and ext_frames:
        mp.write_video(
            f"{output_dir}/hand_camera.mp4",
            np.array(hand_frames),
            fps=1/rate
        )
        mp.write_video(
            f"{output_dir}/external_camera.mp4",
            np.array(ext_frames),
            fps=1/rate
        )
    
    # Save EEF poses
    with open(f"{output_dir}/eef_poses.json", 'w') as f:
        json.dump(eef_poses, f, indent=2)
    
    # Cleanup
    hand_cam.release()
    ext_cam.release()
    teach_arm.robot.set_enable(False)
    follow_arm.robot.set_enable(False)
    print("Data collection completed!")
# %%
