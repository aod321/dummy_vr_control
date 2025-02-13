# %%
import time
import fibre
import ref_tool
from __future__ import print_function
# logger verbose=True
logger = fibre.utils.Logger(verbose=True)
logger.info("Finding teach arm...")
teach_arm = ref_tool.find_any(serial_number="3950366E3233", logger=logger)
# logger.info("Finding follow arm...")
# follow_arm = ref_tool.find_any(serial_number="395D36713233", logger=logger)
logger.info(f"Teach arm found: {teach_arm}")
# logger.info("Follow arm found: %s", follow_arm)
logger.info("Moving Teach Arm to Home Position")
# to home
teach_arm.robot.set_enable(True)
teach_arm.robot.homing()
logger.info("Moving Teach Arm to Push_T Pose")
teach_arm.robot.move_j(0, 0, 90, 0, 90, 0)
#%%
teach_arm.robot.set_enable(False)
stop = False
import time
rate = 0.1  # 10Hz = 0.1s period
while not stop:
    start_time = time.time()
    teach_arm.robot.eef_pose.update_pose_6D()
    current_pose = teach_arm.robot.eef_pose.x, teach_arm.robot.eef_pose.y, teach_arm.robot.eef_pose.z, teach_arm.robot.eef_pose.a, teach_arm.robot.eef_pose.b, teach_arm.robot.eef_pose.c
    print(f"Current Pose: {current_pose}")
    # Sleep precisely to maintain 10Hz
    elapsed = time.time() - start_time
    if elapsed < rate:
        time.sleep(rate - elapsed)
    
    # Calculate and print actual loop frequency
    loop_time = time.time() - start_time
    actual_freq = 1.0 / loop_time if loop_time > 0 else 0
    print(f"Current loop frequency: {actual_freq:.2f} Hz")
# %%
