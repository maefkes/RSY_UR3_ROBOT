import sys
import socket
import time
import math

from UR3eRobotInitialisation import robot3, robot4





def testMain():
    
        # === Bewegungsparameter ===
    speed = 0.3         # rad/s
    acceleration = 0.8  # rad/s²

    # === Aktuelle Gelenkposition holen ===
    joints = robot3.getActualQ()
    print("Aktuelle Gelenkwinkel [rad]:", [round(j, 3) for j in joints])

        # === Beispielbewegungen ===
    # +10° auf Achse 1
    robot3.move_joint_axis(0, math.radians(5))

    # -5° auf Achse 2
    robot3.move_joint_axis(1, math.radians(5))

    # +15° auf Achse 6
    robot3.move_joint_axis(5, math.radians(5))

    home_joints = [0, -1.5708, 0, -1.5708, 0, 0]
    robot3.moveJ(home_joints, speed, acceleration)

    robot3.move_joint_axis(5, math.radians(90))

    robot3.move_joint_axis(5, math.radians(-90))

    # === Zur Ausgangsposition zurückkehren ===
    print("Zur Ausgangsposition zurückkehren...")
    robot3.moveJ(joints, speed, acceleration)

    
    
    
    

############################################################################################
#   STARTE PROGRAMM
############################################################################################
if __name__ == "__main__":
    testMain()