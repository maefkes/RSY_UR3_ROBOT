import json
import copy

class TeachPositionManager:
    def __init__(self, homePose3, homePose4):
        self.positions = {}
        self.addPosition("Home_Robot3", homePose3)
        self.addPosition("Home_Robot4", homePose4)

    def addPosition(self, name, pose):
        
        self.positions[name] = copy.deepcopy(pose)

    def getSavedPosition(self, name):
        return self.positions.get(name, None)

    def listPositions(self):
        return list(self.positions.keys())

    def enableTeachMode(self):
        self.communication.teachMode()

    def disableTeachMode(self):
        self.communication.endTeachMode()

    def exportPositions(self):
        try:
            return json.dumps(self.positions, indent=4)
        except Exception as e:
            print(f"Fehler beim Export: {e}")
            return None

    def setAllPositions(self, positions):
        if isinstance(positions, dict):
            self.positions.update(positions)
            print("Positionen wurden erfolgreich importiert.")
        else:
            print("Fehler: Ungültige Datenstruktur beim Import.")
