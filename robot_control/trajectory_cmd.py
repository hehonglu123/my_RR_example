##
# Command the first UR5 robot using the jog_freespace function
#

from RobotRaconteur.Client import *
import time
import numpy as np

# Connect to the first UR5 robot
c = RRN.ConnectService('rr+tcp://localhost:58651?service=robot')

# Get the robot_info data from the driver
robot_info = c.robot_info

# Get the joint names from the robot_info data structure
joint_names = [j.joint_identifier.name for j in robot_info.joint_info]

# Retrieve the current robot state and print the current command mode
print(c.robot_state.PeekInValue()[0].command_mode)

# Retrieve the constants for the com.robotraconteur.robotics.robot service definition
robot_const = RRN.GetConstants("com.robotraconteur.robotics.robot", c)

# Retrieve the "halt" and "trajectory" enum values
halt_mode = robot_const["RobotCommandMode"]["halt"]
trajectory_mode = robot_const["RobotCommandMode"]["trajectory"]

# Retreive the structure type to create JointTrajectory and JointTrajectoryWaypoint objects
JointTrajectoryWaypoint = RRN.GetStructureType("com.robotraconteur.robotics.trajectory.JointTrajectoryWaypoint",c)
JointTrajectory = RRN.GetStructureType("com.robotraconteur.robotics.trajectory.JointTrajectory",c)

# Change the robot command mode, first to halt, then to trajectory mode
c.command_mode = halt_mode
time.sleep(0.1)
c.command_mode = trajectory_mode

# Connect to the robot_state wire to get real-time streaming state data
state_w = c.robot_state.Connect()

# Wait for the state_w wire to receive valid data
state_w.WaitInValueValid()
state1 = state_w.InValue


# Build up JointTrajectoryWaypoint(s) to move the robot to specified joint angles
waypoints = []

j_start = state1.joint_position
j_end = [0, 0, 0, 0, 0, 0]

for i in range(11):
    wp = JointTrajectoryWaypoint()
    wp.joint_position = (j_end - j_start)*(float(i)/10.0) + j_start
    wp.time_from_start = i
    waypoints.append(wp)

# Fill in the JointTrajectory structure
traj = JointTrajectory()
traj.joint_names = joint_names
traj.waypoints = waypoints

c.speed_ratio = 1

# Execute the trajectory function to get the generator object
traj_gen = c.execute_trajectory(traj)

# Loop to monitor the motion
while (True):
    t = time.time()

    # Check the state
    robot_state = state_w.InValue

    # Run traj_gen.Next(), and catch RR.StopIterationException thrown when motion is complete
    try:
        res = traj_gen.Next()
        print(res)
    except RR.StopIterationException:
        break

    print(hex(c.robot_state.PeekInValue()[0].robot_state_flags))

# Execute more trajectories. Trajectories are queued if executed concurrently

waypoints = []

for i in range(101):
    t = float(i)/10.0
    wp = JointTrajectoryWaypoint()
    cmd = np.deg2rad(15)*np.sin(2*np.pi*(t/10.0))*np.array([1,0,0,0,0.5,-1])
    cmd = cmd + j_end
    wp.joint_position = cmd
    wp.time_from_start = t
    waypoints.append(wp)

traj = JointTrajectory()
traj.joint_names = joint_names
traj.waypoints = waypoints

c.speed_ratio = 0.5

traj_gen = c.execute_trajectory(traj)

c.speed_ratio = 2
traj_gen2 = c.execute_trajectory(traj)

res = traj_gen2.Next()
print(res.action_status)

while (True):
    t = time.time()

    robot_state = state_w.InValue
    try:
        res = traj_gen.Next()        
        print(res.action_status)
    except RR.StopIterationException:
        break
while (True):
    t = time.time()

    robot_state = state_w.InValue
    try:
        res = traj_gen2.Next()
        print(res.action_status)
    except RR.StopIterationException:
        break