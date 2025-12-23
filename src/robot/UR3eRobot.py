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
        self.moveJ(homePosition, asynchronous=True)

    def move_joint_axis(self, axis_index, delta_angle):        
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
    
    def moveL(self, position, asynchronous:bool=False):
        speed = self.manager.get(self.robotName, "axis", "SPEED")
        acc = self.manager.get(self.robotName, "axis", "ACCELERATION")

        self.rtdeControl.moveL(position, speed, acc, asynchronous)

    def moveJ(self, position, asynchronous:bool=False):
        speed = self.manager.get(self.robotName, "axis", "SPEED")
        acc = self.manager.get(self.robotName, "axis", "ACCELERATION")

        self.rtdeControl.moveJ(position, speed, acc, asynchronous)
        
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
        
    def getGripperState(self):
        """Gibt den aktuellen Status des Greifers.
        
        :returns: 0, wenn der Gripper offen ist und 1, wenn der Gripper geschlossen ist"""
        if self.robotiqGripper.isOpen():
            return 0
        elif self.robotiqGripper.isClosed():
            return 1
     
    def moveL_FK(self, position:list, asynchronous:bool=False):
        """Macht eine MoveL-Bewegung unter Angabe der Achswerte des Ziels.
        
        :param position: Achskoordinaten in radiant als Liste"""
        speed = self.manager.get(self.robotName, "axis", "SPEED")
        acc = self.manager.get(self.robotName, "axis", "ACCELERATION")

        self.rtdeControl.moveL_FK(position, speed, acc, asynchronous) 

    def moveJ_IK(self, position:list, asynchronous:bool=False):
        """Macht eine MoveJ-Bewegung unter Angabe der TCP Koordinaten.
        
        :param position: TCP-Koordinaten und Rotation (x,y,z, rx, ry, rz)"""
        speed = self.manager.get(self.robotName, "axis", "SPEED")
        acc = self.manager.get(self.robotName, "axis", "ACCELERATION")

        self.rtdeControl.moveJ_IK(position, speed, acc, asynchronous)

    def moveHome(self):
        self.moveJ(self.homePosition)

    def isSteady(self)->bool:
        return self.rtdeControl.isSteady()