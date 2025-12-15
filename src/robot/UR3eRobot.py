import time
import math
import rtde_control  
import rtde_receive

from gripper.robotiq_gripper_real import RobotiqGripperReal
from gripper.Gripper import Gripper

class UR3eRobot:

    def __init__(self, ip, settingsManager, homePosition, robotName):

        self.manager = settingsManager
        self.homePosition = homePosition
        self.robotName = robotName
    
        self.rtdeControl = rtde_control.RTDEControlInterface(ip)
        self.rtdeReceive = rtde_receive.RTDEReceiveInterface(ip)
        
        gripperTemplate = RobotiqGripperReal(ip)
        self.robotiqGripper = Gripper(robotName, gripperTemplate, self.manager)
        self.robotiqGripper.initialise()

        # move to home position
        #jointHomePosition = self.poseToJoints(self.homePosition)
        self.moveJ(homePosition)

    def move_joint_axis(self, axis_index, delta_angle):
    
        speed = self.manager.get(self.robotName, "axis", "SPEED")
        acc = self.manager.get(self.robotName, "axis", "ACCELERATION")
        
        current_joints = self.getActualQ()
        
        target_joints = list(current_joints)
        target_joints[axis_index] += delta_angle

        print(f"Fahre Achse {axis_index+1} um {math.degrees(delta_angle):.1f}°...")
        self.moveJ(target_joints)
        time.sleep(0.5)
        
    def poseToJoints(self, tcpPose):
        """
        Wandelt eine TCP-Pose [x, y, z, rx, ry, rz] in Gelenkwinkel [q1, q2, q3, q4, q5, q6] um.
        """
        # Nutzung der eingebauten Inversen Kinematik der RTDE-Schnittstelle
        joint_angles = self.rtdeControl.getInverseKinematics(tcpPose)
        
        if joint_angles is None:
            raise ValueError("Inverse Kinematik konnte für die gegebene Pose nicht berechnet werden.")
        
        return joint_angles

    def getActualTCPPose(self):
        return  self.rtdeReceive.getActualTCPPose()
    
    def moveL(self, position):
        speed = self.manager.get(self.robotName, "axis", "SPEED")
        acc = self.manager.get(self.robotName, "axis", "ACCELERATION")

        self.rtdeControl.moveL(position, speed, acc)

    def moveJ(self, position):
        speed = self.manager.get(self.robotName, "axis", "SPEED")
        acc = self.manager.get(self.robotName, "axis", "ACCELERATION")

        self.rtdeControl.moveJ(position, speed, acc)
        
    def speedL(self, velocity_vector):
        speed = self.manager.get(self.robotName, "axis", "SPEED")
        acc = self.manager.get(self.robotName, "axis", "ACCELERATION")

        self.rtdeControl.speedL(velocity_vector, speed, acc)

    def getActualQ(self):
        return self.rtdeReceive.getActualQ()

    def disconnect(self):
        self.rtdeControl.disconnect()
        self.rtdeReceive.disconnect()
        
    def reconnect(self):
        self.rtdeControl.reconnect()
        self.rtdeReceive.reconnect()
        
    def openGripper(self):
        self.robotiqGripper.open()

    def closeGripper(self):
        self.robotiqGripper.close()
        
    
     


