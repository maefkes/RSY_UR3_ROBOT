import rtde_control  
import rtde_receive
from robot.RobotiqGrippper import RobotiqGripper
from robot.UR3eRobot import UR3eRobot


# --- Netzwerkkonfiguration ---
ROBOT3_IP = "192.168.0.3"
ROBOT4_IP = "192.168.0.17"

homePosRobot3 = [-0.3348824484632403, -0.13811531146380698, 0.2610392430112353, 1.0415257012533956, 2.9503966505304193, 0.024981329326417064]
homePosRobot4 = [-0.3173642660495336, -0.2345891541412941, 0.2606208160299016, -2.470623361107635, -1.8532092772072544, 0.10757393241186974]


robot3Control = rtde_control.RTDEControlInterface(ROBOT3_IP)
robot4Control = rtde_control.RTDEControlInterface(ROBOT4_IP)

robot3Receive = rtde_receive.RTDEReceiveInterface(ROBOT3_IP)
robot4Receive = rtde_receive.RTDEReceiveInterface(ROBOT4_IP)

gripper3 = RobotiqGripper(ROBOT3_IP)
gripper4 = RobotiqGripper(ROBOT4_IP)


robot3 = UR3eRobot(robot3Control, robot3Receive, gripper3, homePosRobot3)
robot4 = UR3eRobot(robot4Control, robot4Receive, gripper4, homePosRobot4)