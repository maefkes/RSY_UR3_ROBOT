


class UR3eRobot:

    def __init__(self, rtdeControl, rtdeReceive, robotiqGripper, homePosition):

        self.rtdeControl = rtdeControl
        self.rtdeReceive = rtdeReceive
        self.robotiqGripper = robotiqGripper
        self.homePosition = homePosition
        
        self.moveL(self.homePosition, 0.3, 0.1)

    def getActualTCPPose(self):
        return  self.rtdeReceive.getActualTCPPose()
    
    def moveL(self, position, speed, acc):
        self.rtdeControl.moveL(position, speed, acc)
        


