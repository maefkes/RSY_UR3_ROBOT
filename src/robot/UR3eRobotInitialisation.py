import rtde_control  
import rtde_receive
from robot.RobotiqGrippper import RobotiqGripper
from robot.UR3eRobot import UR3eRobot


# --- Netzwerkkonfiguration ---
ROBOT3_IP = "192.168.0.17"
ROBOT4_IP = "192.168.0.3"

robot3Control = rtde_control.RTDEControlInterface(ROBOT3_IP)
robot4Control = rtde_control.RTDEControlInterface(ROBOT4_IP)

robot3Receive = rtde_receive.RTDEReceiveInterface(ROBOT3_IP)
robot4Receive = rtde_receive.RTDEReceiveInterface(ROBOT4_IP)

gripper3 = RobotiqGripper()
gripper4 = RobotiqGripper()


robot3 = UR3eRobot(robot3Control, robot3Receive, gripper3)
robot4 = UR3eRobot(robot4Control, robot4Receive, gripper4)