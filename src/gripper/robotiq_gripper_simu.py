############################################################
#  robotiq_gripper_simu.py
#  Greiferklasse für die Simulation
#  02-Mai-2025 09:58:00
############################################################

class RobotiqGripperSimu:
    def __init__(self, rtde_control):
        self.rtde = rtde_control

    def activate(self):
        return self.rtde.sendCommand("activate")

    def open(self, speed, force):
        self.set_speed(speed)
        self.set_force(force)
        return self.rtde.sendCommand("openGripper")

    def close(self, speed, force):
        self.set_speed(speed)
        self.set_force(force)
        return self.rtde.sendCommand("closeGripper")

    def move(self, value):  # mm
        return self.rtde.sendCommand("move", {"value": value})

    '''
    Hilfsmethoden
    '''
    def set_force(self, value):
        return self.rtde.sendCommand("set_force", {"value": value})

    def set_speed(self, value):
        return self.rtde.sendCommand("set_speed", {"value": value})
