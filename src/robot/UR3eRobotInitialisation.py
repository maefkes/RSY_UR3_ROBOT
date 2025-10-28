import rtde_control  
import rtde_receive
import os

from rtde_control_simu import RTDEControlInterfaceSimu
from rtde_receive_simu import RTDEReceiveInterfaceSimu
from gripper.GripperInitialisation import robotiqGripper3, robotiqGripper4
from robot.UR3eRobot import UR3eRobot

homePosRobot3 = [-0.3348824484632403, -0.13811531146380698, 0.2610392430112353, 1.0415257012533956, 2.9503966505304193, 0.024981329326417064]
homePosRobot4 = [-0.3348824484632403, -0.13811531146380698, 0.2610392430112353, -1.0415257012533956, -2.9503966505304193, 0.024981329326417064]

SIMULATION = os.environ.get('SIMULATION', 'False') == 'True'


if SIMULATION:
    ROBOT3_IP = ""
    ROBOT4_IP = "127.0.0.1"
    
    robot3Control = RTDEControlInterfaceSimu(ROBOT3_IP)
    robot3Receive = RTDEReceiveInterfaceSimu(ROBOT3_IP)
    
    robot4Control = RTDEControlInterfaceSimu(ROBOT4_IP)
    robot4Receive = RTDEReceiveInterfaceSimu(ROBOT4_IP)
  
else:
    ROBOT3_IP = "192.168.0.3"
    ROBOT4_IP = "192.168.0.17"
    robot3Control = rtde_control.RTDEControlInterface(ROBOT3_IP)
    robot4Control = rtde_control.RTDEControlInterface(ROBOT4_IP)

    robot3Receive = rtde_receive.RTDEReceiveInterface(ROBOT3_IP)
    robot4Receive = rtde_receive.RTDEReceiveInterface(ROBOT4_IP)

robot3 = UR3eRobot(robot3Control, robot3Receive, robotiqGripper3, homePosRobot3)
robot4 = UR3eRobot(robot4Control, robot4Receive, robotiqGripper4, homePosRobot4)