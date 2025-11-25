FUNCTION_MAP = {
        "U": ("U",90), "U'": ("U",-90), "U2": ("U",180),
        "D": ("D",90), "D'": ("D",-90), "D2": ("D",180),
        "L": ("L",90), "L'": ("L",-90), "L2": ("L",180),
        "R": ("R",90), "R'": ("R",-90), "R2": ("R",180),
        "F": ("F",90), "F'": ("F",-90), "F2": ("F",180),
        "B": ("B",90), "B'": ("B",-90), "B2": ("B",180), 
        "X": ("X",0)
}

def rot_R(angle:int):
    # 1: Roboter 4 (Greifer) in korrekte Position fahren (rot nach vorne)

    # 2: Roboter 3 (Dreher) fährt in Vorposition (von vorne)

    # 3: Roboter 3 (Dreher) greift 
    
    # 4: Roboter 3 (Dreher) dreht
    
    # 5: Roboter 3 (Dreher) lässt lost & fährt in Vorposition

    # 6: Roboter 3 (Dreher) fährt in Save-Position
    pass

def rot_L(angle:int):
    # 1: Roboter 3 (Greifer) in korrekte Position fahren (orange nach vorne)

    # 2: Roboter 4 (Dreher) fährt in Vorposition (von vorne)

    # 3: Roboter 4 (Dreher) greift 
    
    # 4: Roboter 4 (Dreher) dreht
    
    # 5: Roboter 4 (Dreher) lässt lost & fährt in Vorposition

    # 6: Roboter 4 (Dreher) fährt in Save-Position
    pass

def rot_F(angle:int):
    # 1: Roboter 4 (Greifer) in korrekte Position fahren (grün nach oben)

    # 2: Roboter 3 (Dreher) fährt in Vorposition (von oben)

    # 3: Roboter 3 (Dreher) greift 
    
    # 4: Roboter 3 (Dreher) dreht
    
    # 5: Roboter 3 (Dreher) lässt lost & fährt in Vorposition

    # 6: Roboter 3 (Dreher) fährt in Save-Position
    pass

def rot_B(angle:int):
    # 1: Roboter 4 (Greifer) in korrekte Position fahren (blau nach oben)

    # 2: Roboter 3 (Dreher) fährt in Vorposition (von oben)

    # 3: Roboter 3 (Dreher) greift 
    
    # 4: Roboter 3 (Dreher) dreht
    
    # 5: Roboter 3 (Dreher) lässt lost & fährt in Vorposition

    # 6: Roboter 3 (Dreher) fährt in Save-Position
    pass

def rot_D(angle:int):
    # 1: Roboter 3 (Greifer) in korrekte Position fahren (gelb nach oben)

    # 2: Roboter 4 (Dreher) fährt in Vorposition (von oben)

    # 3: Roboter 4 (Dreher) greift 

    # 4: Roboter 4 (Dreher) dreht
    
    # 5: Roboter 4 (Dreher) lässt lost & fährt in Vorposition

    # 6: Roboter 4 (Dreher) fährt in Save-Position
    pass

def rot_U(angle:int):
    # 1: Roboter 4 (Greifer) in korrekte Position fahren (weiß nach oben)

    # 2: Roboter 3 (Dreher) fährt in Vorposition (von oben)

    # 3: Roboter 3 (Dreher) greift 
    
    # 4: Roboter 3 (Dreher) dreht
    
    # 5: Roboter 3 (Dreher) lässt lost & fährt in Vorposition

    # 6: Roboter 3 (Dreher) fährt in Save-Position
    pass

def handover():
    # überprüfen welcher Roboter den Würfel gerade hält (ggf. vorher speichern)

    # greifenden Roboter in Position fahren

    # anderen Roboter-Greifer öffnen

    # anderen Roboter in Vorposition fahren

    # anderen Roboter in Greifposition fahren

    # anderen Roboter-Greifer schließen

    # greifenden Roboter-Greifer öffnen

    # alten greifenden Roboter in Vorposition fahren

    # neuen greifenden Roboter in Vorposition fahren

    # beide Roboter in Save-Position fahren
    pass

def initial_grip():
    # Aus GetCubeOrientation die aktuelle Orientierung holen

    # Umgreifoperation berechnen

    # Umgreifoperationen durchführen
    pass

def execute_Solution(solution_str:str):
    """Ruft basierend auf dem Solution String die notwendigen Funktionen des Roboters auf."""

    # initialen Griff durchführen
    initial_grip()

    # über solution string iterieren
    for move in solution_str:
        cmd = FUNCTION_MAP.get(move)
        if cmd[0] == "R":
            rot_R(cmd[1])
        if cmd[0] == "L":
            rot_L(cmd[1])
        if cmd[0] == "F":
            rot_F(cmd[1])
        if cmd[0] == "B":
            rot_B(cmd[1])
        if cmd[0] == "R":
            rot_D(cmd[1])
        if cmd[0] == "R":
            rot_U(cmd[1])
        if cmd[0] == "X":
            handover()