import sys
import os
from PyQt6 import QtWidgets
from gui.testgui import TestGui


SIMULATION = os.environ.get('SIMULATION', 'False') == 'True'

# Homepositionen
homePosRobot3 = [-0.3348824484632403, -0.13811531146380698, 0.2610392430112353, 1.0415257012533956, 2.9503966505304193, 0.024981329326417064]
homePosRobot4 = [-0.3348824484632403, -0.13811531146380698, 0.2610392430112353, -1.0415257012533956, -2.9503966505304193, 0.024981329326417064]

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWin = TestGui(homePosRobot3, homePosRobot4)
    mainWin.show()
    sys.exit(app.exec())
    
<<<<<<< HEAD
# import rtde_control  
# import rtde_receive
# import rtde_io

# import socket
# import time

from glob import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from DetectAndSortCube_fixed import CubeColorDetectorLive 
import GetCubeOrientation as CubeOrientation
import CubeSolver
import ConvertSolutionString as SolutionConverter

# --- Netzwerkkonfiguration ---
ROBOT3_IP = "192.168.0.17"
ROBOT4_IP = "192.168.0.3"

# robot3Control = rtde_control.RTDEControlInterface(ROBOT3_IP)
# robot4Control = rtde_control.RTDEControlInterface(ROBOT4_IP)

# robot3Receive = rtde_receive.RTDEReceiveInterface(ROBOT3_IP)
# robot4Receive = rtde_receive.RTDEReceiveInterface(ROBOT4_IP)

def IR_test():
    # 1: Fotos laden
    image_path = r"C:\Users\heyni\Desktop\Studium\Master\Module\2025_26_WS\RSY\Project\RSY_UR3_ROBOT\data\Nahaufnahme\test3\*.jpg"
    print("Loading images")
    imgs = glob(image_path)

    # 2: Cube Detector initialisieren
    model_path = r"C:\Users\heyni\Desktop\Studium\Master\Module\2025_26_WS\RSY\Project\RSY_UR3_ROBOT\data\models\best.pt"
    detector = CubeColorDetectorLive(model_path, cam_index=1)

    # 3: Detector Ergebnisse speichern
    image1 = detector.detect_from_image(imgs[0])
    image2 = detector.detect_from_image(imgs[1])
    image3 = detector.detect_from_image(imgs[2])
    image4 = detector.detect_from_image(imgs[3])
    image5 = detector.detect_from_image(imgs[4])
    image6 = detector.detect_from_image(imgs[5])
    # print(image1.keys())
    images = [image1, image2, image3, image4, image5, image6]

    # 4: Rotationen speichern
    rotation1 = {"axis": "y", "steps": 1}
    rotation2 = {"axis": "x", "steps": 2}
    rotation3 = {"axis": "y", "steps": 1}
    rotation4 = {"axis": "x", "steps": 1}
    rotation5 = {"axis": "y", "steps": 2}
    rotations = [rotation1, rotation2, rotation3, rotation4, rotation5]

    # 5: Cube String ermitteln
    cube = CubeOrientation.get_final_color_string(images, rotations)

    # 6: Cube Lösung ermitteln
    solution = CubeSolver.get_Cube_Solution(cube.upper())
    print(solution)

    # 7: Lösung für die Roboter konvertieren
    converted_solution = SolutionConverter.Convert_Solution_String(solution)
    print(converted_solution)


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
    
    
    

=======
>>>>>>> main
############################################################################################
#   STARTE PROGRAMM
############################################################################################
if __name__ == "__main__":
    main()
