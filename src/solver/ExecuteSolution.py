import time
import math
from robot.UR3eRobot import UR3eRobot
from robot.positions import positions
from robot.pose import pose

FUNCTION_MAP = {
        "U": ("U",90), "U'": ("U",-90), "U2": ("U",180),
        "D": ("D",90), "D'": ("D",-90), "D2": ("D",180),
        "L": ("L",90), "L'": ("L",-90), "L2": ("L",180),
        "R": ("R",90), "R'": ("R",-90), "R2": ("R",180),
        "F": ("F",90), "F'": ("F",-90), "F2": ("F",180),
        "B": ("B",90), "B'": ("B",-90), "B2": ("B",180), 
        "X": ("X",0)
}

def rot_U(positions:positions, angle:int, robot_3: UR3eRobot, robot_4: UR3eRobot):
    """Dreht die Würfel-Oberseite um den angegebenen Winkel.
    
    :param positions: Enthält alle notwendigen Positionen
    :param angle: Winkel um den die Oberseite gedreht werden soll
    :param robot_3: Greifender Roboter
    :param robot_4: Drehender Roboter
    """
    p_Gripper = positions.pose_rotU_rob3.getJoint()  # Position in der sich der Greifer zum Drehen befindet
    p_preRot = positions.pose_rotU_rob4_pre.getJoint()   # Vorposition des Drehers
    p_preRot_tcp = positions.pose_rotU_rob4_pre.getCartesian()   # Vorposition des Drehers
    p_gripRot_tcp = positions.pose_rotU_rob4.getCartesian()  # Greifposition des Drehers

    # 1: Roboter 3 (Greifer) in korrekte Position fahren (weiß nach oben)
    robot_3.moveJ(p_Gripper)

    # 2: Roboter 4 (Dreher) fährt in Vorposition (von oben)
    robot_4.moveJ(p_preRot)

    # 3: Roboter 4 (Dreher) greift 
    robot_4.moveL(p_gripRot_tcp)
    input("Greifposition erreicht?")
    robot_4.closeGripper()
    input("Greifer 4 geschlossen?")
    
    # 4: Roboter 4 (Dreher) dreht
    robot_4.move_joint_axis(5, math.radians(angle))
    
    # 5: Roboter 4 (Dreher) lässt lost & fährt in Vorposition
    robot_4.openGripper()
    input("Greifer 4 geöffnet?")
    robot_4.moveL(p_preRot_tcp)

    # 6: Roboter 4 (Dreher) fährt in Save-Position
    robot_4.moveHome()
    print("Fertig")

def rot_D(angle:int, robot_3: UR3eRobot, robot_4: UR3eRobot):
    """Dreht die Würfel-Unterseite um den angegebenen Winkel.
    
    :param angle: Winkel um den die Rückseite gedreht werden soll
    :param robot_3: Greifender Roboter
    :param robot_4: Drehender Roboter
    """
    p_Gripper = []  # Position in der sich der Greifer zum Drehen befindet
    p_preRot = []   # Vorposition des Drehers
    p_gripRot = []  # Greifposition des Drehers
    p_Save3 = []    # Save-Position des dritten Roboters
    p_Save4 = []    # Save-Position des vierten Roboters

    # 1: Roboter 3 (Greifer) in korrekte Position fahren (gelb nach oben)
    robot_3.moveJ(p_Gripper)

    # 2: Roboter 4 (Dreher) fährt in Vorposition (von oben)
    robot_4.moveJ(p_preRot)

    # 3: Roboter 4 (Dreher) greift 
    robot_4.moveL(p_gripRot)
    # Gripper schließen

    # 4: Roboter 4 (Dreher) dreht
    robot_4.move_joint_axis(5, math.radians(angle))
    
    # 5: Roboter 4 (Dreher) lässt lost & fährt in Vorposition
    # Gripper öffnen
    robot_4.moveL(p_preRot)

    # 6: Roboter 4 (Dreher) fährt in Save-Position
    robot_4.moveJ(p_Save4)
   
def rot_L(positions:positions, angle:int, robot_3: UR3eRobot, robot_4: UR3eRobot):
    """Führt eine Rotation des Würfels nach links aus
    
    :param positions: Klassenobjekt mit allen notwendigen Positionen
    :param angle: Der Winkel, um den der Würfel nach links gedreht werden soll.
    :param robot_3: der greifende Roboter
    :param robot_4: der drehende Roboter
    """
    p_Gripper = positions.pose_rotL_rob3.getJoint()  # Position in der sich der Greifer zum Drehen befindet
    p_preRot = positions.pose_rotL_rob4_pre.getJoint()   # Vorposition des Drehers
    p_preRot_tcp = positions.pose_rotL_rob4_pre.getCartesian()
    p_gripRot = positions.pose_rotL_rob4.getJoint()  # Greifposition des Drehers
    p_gripRot_tcp = positions.pose_rotL_rob4.getCartesian()

    # 1: Roboter 3 (Greifer) in korrekte Position fahren (orange nach vorne)
    robot_3.moveJ(p_Gripper)

    # 2: Roboter 4 (Dreher) fährt in Vorposition (von vorne)
    robot_4.moveJ(p_preRot)

    # 3: Roboter 4 (Dreher) greift 
    robot_4.moveL(p_gripRot_tcp)
    robot_4.closeGripper()
    input("Greifer geschlossen?")

    # 4: Roboter 4 (Dreher) dreht
    robot_4.move_joint_axis(5, math.radians(angle))

    # 5: Roboter 4 (Dreher) lässt lost & fährt in Vorposition
    robot_4.openGripper()
    input("Greifer 4 geöffnet?")
    robot_4.moveL(p_preRot_tcp)

    # 6: Roboter 4 (Dreher) fährt in Save-Position
    robot_4.moveHome()

def rot_R(positions:positions, angle:int, robot_3:UR3eRobot, robot_4:UR3eRobot):
    """Führt eine Rotation des Würfels nach rechts aus

    :param positions: Klassenobjekt mit allen Positionen
    :param angle: Der Winkel, um den der Würfel gedreht werden soll.
    :param robot_3: Der greifende Roboter
    :param robot_4: Der drehende Roboter
    """
    p_Gripper = positions.pose_rotR_rob3.getJoint()  # Position in der sich der Greifer zum Drehen befindet
    p_preRot = positions.pose_rotR_rob4_pre.getJoint()   # Vorposition des Drehers
    p_preRot_tcp = positions.pose_rotR_rob4_pre.getCartesian()
    p_gripRot = positions.pose_rotR_rob4.getJoint()  # Greifposition des Drehers
    p_gripRot_tcp = positions.pose_rotR_rob4.getCartesian()

    # 1: Roboter 3 (Greifer) in korrekte Position fahren (orange nach vorne)
    robot_3.moveJ(p_Gripper)

    # 2: Roboter 4 (Dreher) fährt in Vorposition (von vorne)
    robot_4.moveJ(p_preRot)

    # 3: Roboter 4 (Dreher) greift 
    robot_4.moveL(p_gripRot_tcp)
    robot_4.closeGripper()
    input("Greifer 4 geschlossen?")

    # 4: Roboter 4 (Dreher) dreht
    robot_4.move_joint_axis(5, math.radians(angle))

    # 5: Roboter 4 (Dreher) lässt lost & fährt in Vorposition
    robot_4.openGripper()
    input("Greifer geöffnet?")
    robot_4.moveL(p_preRot_tcp)

    # 6: Roboter 4 (Dreher) fährt in Save-Position
    robot_4.moveHome()

def rot_F(angle:int, robot_3: UR3eRobot, robot_4: UR3eRobot):
    """Dreht die Frontseite des Würfels um den angegebenen Winkel
    
    :param angle: Winkel um den der Würfel gedreht werden soll
    :param robot_3: Drehender Roboter
    :param robot_4: Greifender Roboter"""
    p_Gripper = []  # Position in der sich der Greifer zum Drehen befindet
    p_preRot = []   # Vorposition des Drehers
    p_gripRot = []  # Greifposition des Drehers
    p_Save3 = []    # Save-Position des dritten Roboters
    p_Save4 = []    # Save-Position des vierten Roboters

    # 1: Roboter 4 (Greifer) in korrekte Position fahren (grün nach oben)
    robot_4.moveJ(p_Gripper)

    # 2: Roboter 3 (Dreher) fährt in Vorposition (von oben)
    robot_3.moveJ(p_preRot)

    # 3: Roboter 3 (Dreher) greift
    robot_3.moveL(p_gripRot)
    # Gripper schließen
    
    # 4: Roboter 3 (Dreher) dreht
    robot_3.move_joint_axis(5, math.radians(angle))
    
    # 5: Roboter 3 (Dreher) lässt lost & fährt in Vorposition
    # Gripper öffnen
    robot_3.moveL(p_preRot)

    # 6: Roboter 3 (Dreher) fährt in Save-Position
    robot_3.moveJ(p_Save3)

def rot_B(angle:int, robot_3: UR3eRobot, robot_4: UR3eRobot):
    """Dreht die Würfel-Rückseite um den angegebenen Winkel.
    
    :param angle: Winkel um den die Rückseite gedreht werden soll
    :param robot_3: Drehender Roboter
    :param robot_4: Greifender Roboter
    """
    p_Gripper = []  # Position in der sich der Greifer zum Drehen befindet
    p_preRot = []   # Vorposition des Drehers
    p_gripRot = []  # Greifposition des Drehers
    p_Save3 = []    # Save-Position des dritten Roboters
    p_Save4 = []    # Save-Position des vierten Roboters
    
    # 1: Roboter 4 (Greifer) in korrekte Position fahren (blau nach oben)
    robot_4.moveJ(p_Gripper)

    # 2: Roboter 3 (Dreher) fährt in Vorposition (von oben)
    robot_3.moveJ(p_preRot)

    # 3: Roboter 3 (Dreher) greift 
    robot_3.moveL(p_gripRot)
    # Gripper schließen
    
    # 4: Roboter 3 (Dreher) dreht
    robot_3.move_joint_axis(5, math.radians(angle))

    # 5: Roboter 3 (Dreher) lässt lost & fährt in Vorposition
    # Gripper öffnen
    robot_3.moveL(p_preRot)

    # 6: Roboter 3 (Dreher) fährt in Save-Position
    robot_3.moveJ(p_Save3)

def handover(current_holder_robot: UR3eRobot, other_robot: UR3eRobot, direction: tuple[int]):
    """Führt ein Handover zwischen dem aktuell haltenden Roboter und dem anderen Roboter durch.
    
    :param current_holder_robot: Roboter, der den Würfel aktuell noch hält
    :param other_robot: anderer Roboter, der den Würfel übernehmen soll
    :param direction: Richtung der Übergabe. Muss entweder (3,4), also (3 zu 4) oder (4,3), also (4 zu 3) sein.
    """
    # überprüfen welcher Roboter den Würfel gerade hält (ggf. vorher speichern)
    if direction[0] == 3 and direction[1] == 4:
        p_preHolder = []
        p_Holder = []
        p_holderSave = []
        p_preHandshake = []
        p_Handshake = []
        p_otherSave = []
    elif direction[0] == 4 and direction[1] == 3:
        p_preHolder = []
        p_Holder = []
        p_holderSave = []
        p_preHandshake = []
        p_Handshake = []
        p_otherSave = []
    else:
        raise Exception("Die angegebene Direction ist ungültig.")
    
    # greifenden Roboter in Position fahren
    current_holder_robot.moveJ(p_preHolder)
    current_holder_robot.moveL(p_Holder)

    # anderen Roboter-Greifer öffnen

    # anderen Roboter in Vorposition fahren
    other_robot.moveJ(p_preHandshake)

    # anderen Roboter in Greifposition fahren
    other_robot.moveL(p_Handshake)

    # anderen Roboter-Greifer schließen

    # greifenden Roboter-Greifer öffnen

    # alten greifenden Roboter in Vorposition fahren
    current_holder_robot.moveL(p_preHolder)

    # neuen greifenden Roboter in Vorposition fahren
    other_robot.moveL(p_preHandshake)

    # beide Roboter in Save-Position fahren
    current_holder_robot.moveJ(p_holderSave)
    other_robot.moveJ(p_otherSave)

def initial_grip():
    # Aus GetCubeOrientation die aktuelle Orientierung holen

    # Umgreifoperation berechnen

    # Umgreifoperationen durchführen
    pass

def execute_Solution(solution_str:str, robot_3:UR3eRobot, robot_4:UR3eRobot):
    """Ruft basierend auf dem Solution String die notwendigen Funktionen des Roboters auf."""

    # initialen Griff durchführen
    initial_grip()

    # über solution string iterieren
    for move in solution_str:
        cmd = FUNCTION_MAP.get(move)
        if cmd[0] == "R":
            rot_R(cmd[1])
            _cmd = cmd
        if cmd[0] == "L":
            rot_L(cmd[1])
            _cmd = cmd
        if cmd[0] == "F":
            rot_F(cmd[1])
            _cmd = cmd
        if cmd[0] == "B":
            rot_B(cmd[1])
            _cmd = cmd
        if cmd[0] == "D":
            rot_D(cmd[1])
            _cmd = cmd
        if cmd[0] == "U":
            rot_U(cmd[1])
            _cmd = cmd
        if cmd[0] == "X":
            # hier muss noch irgendwo ein Fehler sein
            if _cmd == "R" or _cmd == "F" or _cmd == "B":
                direction = (4,3)
                handover(robot_3, robot_4, direction)
            elif  _cmd == "U" or _cmd =="L" or _cmd == "D":
                direction = (3,4)
                handover(robot_3, robot_4, direction)