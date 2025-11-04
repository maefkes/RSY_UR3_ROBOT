import sys
import rtde_control  
import rtde_receive
import rtde_io

import socket
import time

from glob import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from DetectAndSortCube_fixed import CubeColorDetectorLive 
import GetCubeOrientation as CubeOrientation

# --- Netzwerkkonfiguration ---
ROBOT3_IP = "192.168.0.17"
ROBOT4_IP = "192.168.0.3"

# robot3Control = rtde_control.RTDEControlInterface(ROBOT3_IP)
# robot4Control = rtde_control.RTDEControlInterface(ROBOT4_IP)

# robot3Receive = rtde_receive.RTDEReceiveInterface(ROBOT3_IP)
# robot4Receive = rtde_receive.RTDEReceiveInterface(ROBOT4_IP)

def IR_test():
    # Schritt 1 Fotos machen und speichern
    image_path = r"C:\Users\heyni\Desktop\Studium\Master\Module\2025_26_WS\RSY\Project\RSY_UR3_ROBOT\data\Nahaufnahme\test1\*.jpg"
    print("Loading images")
    imgs = glob(image_path)

    model_path = r"C:\Users\heyni\Desktop\Studium\Master\Module\2025_26_WS\RSY\Project\RSY_UR3_ROBOT\data\models\best.pt"
    detector = CubeColorDetectorLive(model_path, cam_index=1)

    image1 = detector.detect_from_image(imgs[0])
    image2 = detector.detect_from_image(imgs[1])
    image3 = detector.detect_from_image(imgs[2])
    image4 = detector.detect_from_image(imgs[3])
    image5 = detector.detect_from_image(imgs[4])
    image6 = detector.detect_from_image(imgs[5])
    print(image1)
    print(image2)
    print(image3)
    print(image4)
    print(image5)
    print(image6) 

    # Schritt 2 Bilder auswerten



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
    # testMain()
    IR_test()