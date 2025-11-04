import rtde_control  
import rtde_receive
import os

from gripper.robotiq_gripper_simu import RobotiqGripperSimu
from gripper.robotiq_gripper_real import RobotiqGripperReal
from gripper.Gripper import Gripper
from robot.rtde_control_simu import RTDEControlInterfaceSimu
from robot.rtde_receive_simu import RTDEReceiveInterfaceSimu
from robot.UR3eRobot import UR3eRobot
from manager.SettingsManager import SettingsManager
from manager.TeachPositionManager import TeachPositionManager

#--- set homepositions for the robots-----------------------------------------------------------------------------------------------------------#
homePosRobot3 = [-0.3348824484632403, -0.13811531146380698, 0.2610392430112353, 1.0415257012533956, 2.9503966505304193, 0.024981329326417064]
homePosRobot4 = [-0.3348824484632403, -0.13811531146380698, 0.2610392430112353, -1.0415257012533956, -2.9503966505304193, 0.024981329326417064]

#--- create manager objects --------------------------------------------------------------------------------------------------------------------#
settingsManager = SettingsManager()
teachPositionManager = TeachPositionManager(homePosRobot3, homePosRobot4)

SIMULATION = os.environ.get('SIMULATION', 'False') == 'True'

#--- create objects for the simulation robots-------------------------------------------------------#
if SIMULATION:
    ROBOT3_IP = ""
    ROBOT4_IP = "127.0.0.1"
    
    robot3Control = RTDEControlInterfaceSimu(ROBOT3_IP)
    robot3Receive = RTDEReceiveInterfaceSimu(ROBOT3_IP)
    
    robot4Control = RTDEControlInterfaceSimu(ROBOT4_IP)
    robot4Receive = RTDEReceiveInterfaceSimu(ROBOT4_IP)
    
    gripperTemplate3 = RobotiqGripperSimu(robot3Control)
    gripperTemplate4 = RobotiqGripperSimu(robot4Control)

#--- create objects for the real robots -----------------------------------------------------------#  
else:
    ROBOT3_IP = "192.168.0.3"
    ROBOT4_IP = "192.168.0.17"
    
    gripperTemplate3= RobotiqGripperReal(ROBOT3_IP)
    gripperTemplate4 = RobotiqGripperReal(ROBOT4_IP)
    
    robot3Control = rtde_control.RTDEControlInterface(ROBOT3_IP)
    robot4Control = rtde_control.RTDEControlInterface(ROBOT4_IP)

    robot3Receive = rtde_receive.RTDEReceiveInterface(ROBOT3_IP)
    robot4Receive = rtde_receive.RTDEReceiveInterface(ROBOT4_IP)
    
#--- create the gripper objects -----------------------------------------------------------------#
robotiqGripper3 = Gripper("robot3", gripperTemplate3, settingsManager)
robotiqGripper4 = Gripper("robot4", gripperTemplate4, settingsManager)

#--- create the robot objects -------------------------------------------------------------------#
robot3 = UR3eRobot(robot3Control, robot3Receive, robotiqGripper3, settingsManager, homePosRobot3)
robot4 = UR3eRobot(robot4Control, robot4Receive, robotiqGripper4, settingsManager, homePosRobot4)