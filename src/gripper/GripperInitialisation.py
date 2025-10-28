##################################################
#   GripperInitialisation.py
#   Hiermit wird der Robotergreifer initialisiert
#   02-Mai-2025 17:11:00
##################################################
import os

from robotiq_gripper_simu import RobotiqGripperSimu
from robotiq_gripper_real import RobotiqGripperReal
from Gripper import Gripper

from robot.UR3eRobotInitialisation import robot3Control, robot4Control, ROBOT3_IP, ROBOT4_IP
from manager.ManagerInitialisation import settingsManager



SIMULATION = os.environ.get('SIMULATION', 'False') == 'True'

if SIMULATION:
    gripperTemplate3 = RobotiqGripperSimu(robot3Control)
    gripperTemplate4 = RobotiqGripperSimu(robot4Control)
else:
    gripperTemplate3= RobotiqGripperReal(ROBOT3_IP)
    gripperTemplate4 = RobotiqGripperReal(ROBOT4_IP)
    
# Gripper-Objekt erstellen
robotiqGripper3 = Gripper("robot3", gripperTemplate3, settingsManager)
robotiqGripper4 = Gripper("robot4", gripperTemplate4, settingsManager)

