
import time
import math

class UR3eRobot:

    def __init__(self, rtdeControl, rtdeReceive, robotiqGripper, settingsManager, homePosition):

        self.rtdeControl = rtdeControl
        self.rtdeReceive = rtdeReceive
        self.robotiqGripper = robotiqGripper
        self.manager = settingsManager
        self.homePosition = homePosition
        
        self.moveL(self.homePosition, 0.3, 0.1)

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

    def getActualTCPPose(self):
        return  self.rtdeReceive.getActualTCPPose()
    
    def moveL(self, position, speed, acc):
        self.rtdeControl.moveL(position, speed, acc)

    def moveJ(self, position, speed, acc):
        self.rtdeControl.moveJ(position, speed, acc)

    def getActualQ(self):
        return self.rtdeReceive.getActualQ()

    def disconnect(self):
        self.rtdeControl.disconnect()
        self.rtdeReceive.disconnect()
        
    def reconnect(self):
        self.rtdeControl.reconnect()
        self.rtdeReceive.reconnect()
        
    
        
    def disconnect(self):
        self.rtdeControl.disconnect()
        self.rtdeReceive.disconnect()
        
    def reconnect(self):
        self.rtdeControl.reconnect()
        self.rtdeReceive.reconnect()


