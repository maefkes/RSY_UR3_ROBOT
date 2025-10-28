import sys
import rtde_control  
import rtde_receive
import rtde_io

import socket
import time

# --- Netzwerkkonfiguration ---
ROBOT3_IP = "192.168.0.17"
ROBOT4_IP = "192.168.0.3"

robot3Control = rtde_control.RTDEControlInterface(ROBOT3_IP)
robot4Control = rtde_control.RTDEControlInterface(ROBOT4_IP)

robot3Receive = rtde_receive.RTDEReceiveInterface(ROBOT3_IP)
robot4Receive = rtde_receive.RTDEReceiveInterface(ROBOT4_IP)



def testMain():

    posRobot3 = robot3Receive.getActualTCPPose()
    posRobot3[0] -=  0.01
    posRobot3[1] -=  0.01
    posRobot3[2] -=  0.01
    posRobot3[3] -=  0.01
    posRobot3[4] -=  0.01
    posRobot3[5] -=  0.01
    robot3Control.moveL(posRobot3)
    
    posRobot4 = robot3Receive.getActualTCPPose()
    posRobot4[0] -= 0.01
    posRobot4[1] -= 0.01
    posRobot4[2] -= 0.01
    posRobot4[3] -= 0.01
    posRobot4[4] -= 0.01
    posRobot4[5] -= 0.01
    robot4Control.moveL(posRobot4)
    
    
    

############################################################################################
#   STARTE PROGRAMM
############################################################################################
if __name__ == "__main__":
    testMain()