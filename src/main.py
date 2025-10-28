import sys
import socket
import time

from robot.UR3eRobotInitialisation import robot3, robot4





def testMain():

    speed = 0.3
    acc = 0.1
    
    posRobot3 = robot3.getActualTCPPose()
    '''
    posRobot3[0] -=  0.001
    posRobot3[1] -=  0.001
    posRobot3[2] -=  0.001
    posRobot3[3] -=  0.001
    posRobot3[4] -=  0.001
    posRobot3[5] -=  0.001
    '''
    robot3.moveL(posRobot3, speed, acc)
    
    posRobot4 = robot4.getActualTCPPose()
    
    '''
    posRobot4[0] -= 0.001
    posRobot4[1] -= 0.001
    posRobot4[2] -= 0.001
    posRobot4[3] -= 0.001
    posRobot4[4] -= 0.001
    posRobot4[5] -= 0.
    '''
    robot4.moveL(posRobot4, speed, acc)
    
    
    

############################################################################################
#   STARTE PROGRAMM
############################################################################################
if __name__ == "__main__":
    testMain()