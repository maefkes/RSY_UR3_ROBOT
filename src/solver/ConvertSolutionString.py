def Convert_Solution_String(solution_string: str)->str:
    """Nimmt den aktuellen Solution String und konvertiert ihn so, dass der Roboter ihn direkt als Befehlskette verwenden kann."""

    """
    Beispiel:
    Solution String: R U L U2 D R2 D' F R' F' L' F2 L2 B U2 L2 B' B2 D2 U'

    config 1: Roboter 3 greift, 4 dreht: U U' U2 D D' D2 L L' L2
    config 2: Roboter 4 greift, 3 dreht: R R' R2 F F' F2 B B' B2

    - Jedem Befehl eine config zuweisen
    - Immer die aktuelle config speichern
    """

    grip_config = {
        "U": 1, "U'": 1, "U2": 1,
        "D": 1, "D'": 1, "D2": 1,
        "L": 1, "L'": 1, "L2": 1,

        "R": 2, "R'": 2, "R2": 2,
        "F": 2, "F'": 2, "F2": 2,
        "B": 2, "B'": 2, "B2": 2, 
    }

    # 1: Befehle in config Liste umwandeln
    moves_seperated = solution_string.split(" ")
    config_arr = []
    for move in moves_seperated:
        config_arr.append(grip_config.get(move))

    # 2: Auf Wechsel überprüfen
    insertion_list = []
    for i in range(len(config_arr)):
        if i > 0:
            if config_arr[i-1] != config_arr[i]:
                insertion_list.append(i)

    # 3: Wechsel eintragen
    for i in range(len(insertion_list)):
        config_arr.insert(i+insertion_list[i], "X")
        moves_seperated.insert(i+insertion_list[i], "X")

    return moves_seperated

if __name__ == "__main__":
    solution_string = "R U L U2 D R2 D' F R' F' L' F2 L2 B U2 L2 B' B2 D2 U'"
    new_solution_string = Convert_Solution_String(solution_string)
    print(new_solution_string)
