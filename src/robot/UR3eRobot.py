


class UR3eRobot:

    def __init__(self, rtdeControl, rtdeReceive, robotiqGripper, settingsManager, homePosition):

        self.rtdeControl = rtdeControl
        self.rtdeReceive = rtdeReceive
        self.robotiqGripper = robotiqGripper
        self.manager = settingsManager
        self.homePosition = homePosition
        
        self.moveL(self.homePosition, 0.3, 0.1)

    def getActualTCPPose(self):
        return  self.rtdeReceive.getActualTCPPose()
    
    def moveL(self, position, speed, acc):
        self.rtdeControl.moveL(position, speed, acc)
        
    def disconnect(self):
        self.rtdeControl.disconnect()
        self.rtdeReceive.disconnect()
        
    def reconnect(self):
        self.rtdeControl.reconnect()
        self.rtdeReceive.reconnect()


