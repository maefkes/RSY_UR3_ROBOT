#################################################################
#  SettingsManager.py
#  Diese Klasse verwaltet die Enums für Einstellungen und fungiert
#  als Schnittstelle zur GUI, um die Werte für mehrere Roboter
#  (z. B. UR3e und UR4e) zu ändern.
#  12-Mai-2025 10:31:00
#################################################################
from enum import Enum


# ==============================================================
#   ENUM-DEFINITIONEN
# ==============================================================

class AxisSettingsRobot3(Enum):
    SPEED        = 0.5
    ACCELERATION = 0.2


class AxisSettingsRobot4(Enum):
    SPEED        = 0.5
    ACCELERATION = 0.2


class GripperSettings3(Enum):
    FORCE    = 1
    SPEED    = 50
    POSITION = 3


class GripperSettings4(Enum):
    FORCE    = 1
    SPEED    = 50
    POSITION = 3

class SettingsManager:
    def __init__(self):
        
        self.settings = {
            "robot3": {
                "axis": {s.name: s.value for s in AxisSettingsRobot3},
                "gripper": {s.name: s.value for s in GripperSettings3}
            },
            "robot4": {
                "axis": {s.name: s.value for s in AxisSettingsRobot4},
                "gripper": {s.name: s.value for s in GripperSettings4}
            }
        }

    # ----------------------------------------------------------
    def get(self, robot, group, name):
        """
        Gibt den Wert einer Einstellung zurück.
        @param robot: 'robot3' oder 'robot4'
        @param group: 'axis' oder 'gripper'
        @param name:  Enum-Name (z. B. 'SPEED')
        @returns: Wert oder 0.0, falls nicht vorhanden
        """
        try:
            return self.settings[robot][group].get(name, 0.0)
        except KeyError:
            raise KeyError(f"Ungültiger Zugriff: {robot}/{group}/{name}")

    # ----------------------------------------------------------
    def set(self, robot, group, name, value):
        """
        Ändert einen bestehenden Wert.
        @param robot: 'robot3' oder 'robot4'
        @param group: 'axis' oder 'gripper'
        @param name:  Enum-Name
        @param value: Neuer Wert
        """
        if robot not in self.settings:
            raise KeyError(f"Unbekannter Roboter: {robot}")
        if group not in self.settings[robot]:
            raise KeyError(f"Unbekannte Gruppe: {group}")
        if name not in self.settings[robot][group]:
            raise KeyError(f"{name} ist kein gültiger Eintrag in {group} für {robot}")

        self.settings[robot][group][name] = value

    # ----------------------------------------------------------
    def all(self):
        """
        Gibt alle bekannten Settings zurück.
        """
        return self.settings


