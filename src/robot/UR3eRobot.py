
import time
import math

class UR3eRobot:

    def __init__(self, rtdeControl, rtdeReceive, robotiqGripper, settingsManager, homePosition):

        self.rtdeControl = rtdeControl
        self.rtdeReceive = rtdeReceive
        self.robotiqGripper = robotiqGripper  
        self.gripper = robotiqGripper         
        self.manager = settingsManager
        self.homePosition = homePosition
        
        # move to home position
        jointHomePosition = self.pose_to_joints(self.homePosition)
        self.moveJ(jointHomePosition, 0.3, 0.8)

    def move_joint_axis(self, axis_index, delta_angle):
    
        """
        SPAETER ENTFERNEN
        """
        speed = 0.3
        acc = 0.8
        
        
        current_joints = self.getActualQ()
        
        target_joints = list(current_joints)
        target_joints[axis_index] += delta_angle

        print(f"Fahre Achse {axis_index+1} um {math.degrees(delta_angle):.1f}°...")
        self.moveJ(target_joints, speed, acc)
        time.sleep(0.5)
        
    def pose_to_joints(self, tcp_pose):
        """
        Wandelt eine TCP-Pose [x, y, z, rx, ry, rz] in Gelenkwinkel [q1, q2, q3, q4, q5, q6] um.
        """
        # Nutzung der eingebauten Inversen Kinematik der RTDE-Schnittstelle
        joint_angles = self.rtdeControl.getInverseKinematics(tcp_pose)
        
        if joint_angles is None:
            raise ValueError("Inverse Kinematik konnte für die gegebene Pose nicht berechnet werden.")
        
        return joint_angles

    def getActualTCPPose(self):
        return  self.rtdeReceive.getActualTCPPose()
    
    def moveL(self, position, speed, acc):
        self.rtdeControl.moveL(position, speed, acc)

    def moveJ(self, position, speed, acc):
        self.rtdeControl.moveJ(position, speed, acc)
        
    def speedL(self, velocity_vector):
        self.rtdeControl.speedL(velocity_vector, 0.6, 0.1)

    def getActualQ(self):
        return self.rtdeReceive.getActualQ()

    def disconnect(self):
        self.rtdeControl.disconnect()
        self.rtdeReceive.disconnect()
        
    def reconnect(self):
        self.rtdeControl.reconnect()
        self.rtdeReceive.reconnect()
        
    
     


