##################################################
#   Gripper.py
#   Diese Klasse bildet den Robotergreifer als 
#   virtuellen Zwilling ab
#   02-Mai-2025 17:11:00
##################################################
from manager.SettingsManager import GripperSettings3, GripperSettings4

class Gripper:
    def __init__(self, robot_id: str, gripperTemplate, settingsManager):
        """
        @param gripperTemplate: Simulierter oder realer Greifer
        @param settingsManager: Instanz von SettingsManager
        @param robot_id: 'robot3' oder 'robot4'
        """
        self.gripper = gripperTemplate
        self.manager = settingsManager
        self.robot_id = robot_id

        if robot_id == "robot3":
            self.enum = GripperSettings3
        elif robot_id == "robot4":
            self.enum = GripperSettings4
        else:
            raise ValueError(f"Unbekannter Roboter: {robot_id}")

    # ----------------------------------------------------------
    def activate(self):
        return self.gripper.activate()

    # ----------------------------------------------------------
    def open(self):
        speed = self.manager.get(self.robot_id, "gripper", self.enum.SPEED.name)
        force = self.manager.get(self.robot_id, "gripper", self.enum.FORCE.name)

        if hasattr(self.gripper, "open"):
            return self.gripper.open(speed, force)
        else:
            open_pos = self.gripper.get_open_position()
            return self.gripper.move(open_pos, speed, force)

    # ----------------------------------------------------------
    def close(self):
        speed = self.manager.get(self.robot_id, "gripper", self.enum.SPEED.name)
        force = self.manager.get(self.robot_id, "gripper", self.enum.FORCE.name)

        if hasattr(self.gripper, "close"):
            return self.gripper.close(speed, force)
        else:
            closed_pos = self.gripper.get_closed_position()
            return self.gripper.move(closed_pos, speed, force)

    # ----------------------------------------------------------
    def move(self):
        speed = self.manager.get(self.robot_id, "gripper", self.enum.SPEED.name)
        force = self.manager.get(self.robot_id, "gripper", self.enum.FORCE.name)
        position = self.manager.get(self.robot_id, "gripper", self.enum.POSITION.name)

        if hasattr(self.gripper, "move") and "speed" in self.gripper.move.__code__.co_varnames:
            return self.gripper.move(position, speed, force)
        else:
            return self.gripper.move(position)

    # ----------------------------------------------------------
    def isActive(self):
        if hasattr(self.gripper, "is_active"):
            return self.gripper.is_active()
        return True

    def getPosition(self):
        if hasattr(self.gripper, "get_current_position"):
            return self.gripper.get_current_position()
        return None

    # ----------------------------------------------------------
    # Methoden ausschließlich für den realen Greifer
    # ----------------------------------------------------------
    def isOpen(self):
        return self.gripper.is_open()

    def isClosed(self):
        return self.gripper.is_closed()

    def connect(self):
        self.gripper.connect()

    def moveAndWaitForPosition(self, v1, v2, v3):
        self.gripper.move_and_wait_for_pos(v1, v2, v3)

    def disconnect(self):
        self.gripper.disconnect()

    def initialise(self):
        print("Connecting to gripper...")
        self.connect()
        print("Activating gripper...")
        #self.activate()
        self.moveAndWaitForPosition(255, 255, 255)
        self.moveAndWaitForPosition(0, 255, 255)
