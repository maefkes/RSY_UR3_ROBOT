##################################################
#   ManagerInitialisation.py
#   Hiermit werden die Manager initialisiert
#   12-Mai-2025 11:08:00
##################################################
from manager.SettingsManager import SettingsManager
from manager.TeachPositionManager import TeachPositionManager
from robot.UR3eRobotInitialisation import homePosRobot3, homePosRobot4

settingsManager = SettingsManager()
teachPositionManager = TeachPositionManager(homePosRobot3, homePosRobot4)