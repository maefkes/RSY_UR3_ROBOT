import numpy as np

FACE_AXIS = {
    "R": "y", "O": "-y",
    "W": "z", "Y": "-z",
    "G": "x", "B": "-x",
}

GLOBAL_KSYS = {
    "x": np.array([1, 0, 0]),
    "y": np.array([0, 1, 0]),
    "z": np.array([0, 0, 1]),
}

def get_rotation_matrix(axis:str, steps:int)->np.ndarray:
    """Ermittelt die Rotationsmatrix aus 90° Schritten um die gegebene Achse
    
    :param: axis: x, y oder z bzw. -x, -y oder -z
    :param: steps: 1, 2 oder 3 Schritte, die jeweils 90° um die gegebene Achse beschreiben 
    :returns: Rotationsmatrix"""
    if axis[0] == "-":
        steps *= -1
        axis = axis[1]

    angle = steps * (np.pi / 2)
    c, s = np.cos(angle), np.sin(angle)
    if axis == "x":
        return np.array([[1,0,0],[0,c,-s],[0,s,c]])
    if axis == "y":
        return np.array([[c,0,s],[0,1,0],[-s,0,c]])
    if axis == "z":
        return np.array([[c,-s,0],[s,c,0],[0,0,1]])
    
def rotate_axis(axis:np.ndarray, Mrot:np.ndarray)->np.ndarray:
    """Wendet eine Rotation um eine einzelne Achse an
    
    :param: axis: Wert der Achse, z.B. [1,0,0], die rotiert werden soll.
    :param: Mrot: 3x3 Rotationsmatrix
    :returns: Rotierte Achse"""
    return Mrot @ axis

def get_cube_ksys(image1:dict, image2:dict)->dict:
    """Ermittelt das Würfelkoordinatensystem aus den ersten beiden Bildern
    
    :param: image1, image2: Bild-Dictionaries, die 
    :returns: Dictionary mit den keys x, y und z, die die Rotation des Würfels beschreiben"""
    cube_ksys = {}
    if image1["axis"][0] == "-":
        cube_ksys[image1["axis"][1]] = -image1["orientation"].astype(int)
        val1 = -image1["orientation"]
        ax_1 = image1["axis"][1]
    else:
        cube_ksys[image1["axis"]] = +image1["orientation"].astype(int) 
        val1 = +image1["orientation"]   
        ax_1 = image1["axis"]
    
    if image2["axis"][0] == "-":
        cube_ksys[image2["axis"][1]] = -image2["orientation"].astype(int)
        val2 = -image2["orientation"]
        ax_2 = image2["axis"][1]
    else:
        cube_ksys[image2["axis"]] = +image2["orientation"].astype(int)
        val2 = +image2["orientation"]
        ax_2 = image2["axis"]

    # letzte Achse über Kreuzprodukt berechnen - Reihenfolge bestimmt über Vorzeichen
    if (ax_1 == "x" and ax_2 == "y") or (ax_1 == "y" and ax_2 == "z") or (ax_1 == "z" and ax_2 == "x"):
        val3 = np.cross(val1,val2) 
    elif (ax_1 == "x" and ax_2 == "z") or (ax_1 == "y" and ax_2 == "x") or (ax_1 == "z" and ax_2 == "y"):
        val3 = np.cross(val2,val1)

    if cube_ksys.get("x") is None:
        cube_ksys["x"] = val3.astype(int)
    elif cube_ksys.get("y") is None:
        cube_ksys["y"] = val3.astype(int)
    elif cube_ksys.get("z") is None:
        cube_ksys["z"] = val3.astype(int)

    return cube_ksys

def rotate_cube_ksys(cube_ksys:dict, rotation: dict)->dict:
    """Rotiert das gesamte Würfel KSYS um die angegebene Rotation
    
    :param: cube_ksys: aktuelles Würfelkoordinatensystem des 
    :param: rotation: Beschreibt die anzuwendende Rotation in Form eines dicts
    :returns: rotiertes Würfelkoordinatensystem als dict"""
    x = cube_ksys["x"]
    y = cube_ksys["y"]
    z = cube_ksys["z"]
    
    M_rot = get_rotation_matrix(rotation["axis"], rotation["steps"])

    x_new = rotate_axis(x, M_rot).astype(int)
    y_new = rotate_axis(y, M_rot).astype(int)
    z_new = rotate_axis(z, M_rot).astype(int)

    cube_ksys_new = {
        "x": x_new,
        "y": y_new,
        "z": z_new
    }

    return cube_ksys_new

def get_corrected_color_matrix(cube_ksys:dict, image:dict):

    color_string = image["matrix"]
    color_matrix = np.array(list(color_string)).reshape((3, 3))

    print("Image axis: ", image["axis"])

    if image["axis"] == "x" or image["axis"] == "-x":
        # so weit drehen, dass z = [-1,0,0]
        z = cube_ksys["z"]
        if (z == [-1,0,0]).all():
            print("Keine Rotation nötig")
            corrected_matrix = color_matrix
        elif (z == [0,1,0]).all():
            # eine Drehung um 90° nach links nötig
            corrected_matrix = np.rot90(color_matrix, k=1)
        elif (z == [1,0,0]).all():
            # zwei Drehungen um 90° nach links nötig
            corrected_matrix = np.rot90(color_matrix, k=2)
        elif (z == [0,-1,0]).all():
            # drei Drehungen um 90° nach links nötig
            corrected_matrix = np.rot90(color_matrix, k=3)

    elif image["axis"] == "y" or image["axis"] == "-y":
        # so weit drehen, dass z = [-1,0,0]
        z = cube_ksys["z"]
        if (z == [-1,0,0]).all():
            # passt schon, keine Drehung nötig
            print("Keine Rotation nötig")
            corrected_matrix = color_matrix
        elif (z == [0,1,0]).all():
            # eine Drehung um 90° nach links nötig
            corrected_matrix = np.rot90(color_matrix, k=1)
        elif (z == [1,0,0]).all():
            # zwei Drehungen um 90° nach links nötig
            corrected_matrix = np.rot90(color_matrix, k=2)
        elif (z == [0,-1,0]).all():
            # eine Drehung um 90° nach rechts nötig
            corrected_matrix = np.rot90(color_matrix, k=3)

    elif image["axis"] == "z" or image["axis"] == "-z":
        # so weit drehen, dass y = [0,1,0]
        y = cube_ksys["y"]
        if (y == [0,1,0]).all():
            # passt schon
            print("Keine Rotation nötig")
            corrected_matrix = color_matrix
        elif (y == [-1,0,0]).all():
            # eine Drehung um 90° nach rechts nötig
            corrected_matrix = np.rot90(color_matrix, k=3)
        elif (y == [1,0,0]).all():
            # eine Drehung um 90° nach links nötig
            corrected_matrix = np.rot90(color_matrix, k=1)
        elif (y == [0,-1,0]).all():
            # zwei Drehungen um 90° nach links nötig
            corrected_matrix = np.rot90(color_matrix, k=2)

    corrected_color_string = ''.join(corrected_matrix.flatten())
    return corrected_color_string

def get_final_color_string(images:list[dict], rotations:list[dict])->str:
    result = list("WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY")

    image1 = images[0]
    rotation1 = rotations[0]
    image2 = images[1]
    rotation2 = rotations[1]
    image3 = images[2]
    rotation3 = rotations[2]
    image4 = images[3]
    rotation4 = rotations[3]
    image5 = images[4]
    rotation5 = rotations[4]
    image6 = images[5]

    # 1: Bild 1 auswerten
    image1["axis"] = FACE_AXIS.get(image1["parentcolor"])
    image1["orientation"] = GLOBAL_KSYS.get("z")

    # 2: Erste Rotation anwenden
    M_rot_1 = get_rotation_matrix(rotation1["axis"], rotation1["steps"])
    image1["orientation"] = rotate_axis(image1["orientation"], M_rot_1)

    # 3: Bild 2 auswerten
    image2["axis"] = FACE_AXIS.get(image2["parentcolor"])
    image2["orientation"] = GLOBAL_KSYS.get("z")

    # 4: Orientierung ermitteln
    cube_ksys = get_cube_ksys(image1, image2)

    # 5: Farbmatrix von Bild 1 korrigieren
    backwards_rotation1 = {
        "axis": rotation1["axis"],
        "steps": -rotation1["steps"]
    }
    M_rot_1_inverted = get_rotation_matrix(backwards_rotation1["axis"], backwards_rotation1["steps"])
    previous_cube_x = rotate_axis(cube_ksys["x"], M_rot_1_inverted).astype(int)
    previous_cube_y = rotate_axis(cube_ksys["y"], M_rot_1_inverted).astype(int)
    previous_cube_z = rotate_axis(cube_ksys["z"], M_rot_1_inverted).astype(int)
    previous_cube_ksys = {
        "x": previous_cube_x,
        "y": previous_cube_y,
        "z": previous_cube_z
    }
    corrected_color_matrix_1 = get_corrected_color_matrix(previous_cube_ksys, image1)
    image1["matrix"] = corrected_color_matrix_1

    # 6: Farbmatrix für Bild 2 korrigieren
    corrected_color_matrix_2 = get_corrected_color_matrix(cube_ksys, image2)
    image2["matrix"] = corrected_color_matrix_2

    # 7: Rotation 2 anwenden
    cube_ksys = rotate_cube_ksys(cube_ksys, rotation2)

    # 8: nächstes Bild auswerten
    image3["axis"] = FACE_AXIS.get(image3["parentcolor"])
    corrected_color_matrix_3 = get_corrected_color_matrix(cube_ksys, image3)
    image3["matrix"] = corrected_color_matrix_3

    # 9: Rotation 3 + Bild 4
    cube_ksys = rotate_cube_ksys(cube_ksys, rotation3)
    image4["axis"] = FACE_AXIS.get(image4["parentcolor"])
    corrected_color_matrix_4 = get_corrected_color_matrix(cube_ksys, image4)
    image4["matrix"] = corrected_color_matrix_4

    # 10: Rotation 4 + Bild 5
    cube_ksys = rotate_cube_ksys(cube_ksys, rotation4)
    image5["axis"] = FACE_AXIS.get(image5["parentcolor"])
    corrected_color_matrix_5 = get_corrected_color_matrix(cube_ksys, image5)
    image5["matrix"] = corrected_color_matrix_5

    # 11: Rotation 5 + Bild 6
    cube_ksys = rotate_cube_ksys(cube_ksys, rotation5)
    image6["axis"] = FACE_AXIS.get(image6["parentcolor"])
    corrected_color_matrix_6 = get_corrected_color_matrix(cube_ksys, image6)
    image6["matrix"] = corrected_color_matrix_6

    # 12 Auf Array mappen
    for image in images:
        # print(image["matrix"])
        if image["parentcolor"] == "W":
            # print(result[0:9], " to ", image["matrix"])
            result[0:9] = image["matrix"]
        elif image["parentcolor"] == "O":
            # print(result[9:18], " to ", image["matrix"])
            result[9:18] = image["matrix"]
        elif image["parentcolor"] == "G":
            # print(result[18:27], " to ", image["matrix"])
            result[18:27] = image["matrix"]
        elif image["parentcolor"] == "R":
            # print(result[27:36], " to ", image["matrix"])
            result[27:36] = image["matrix"]
        elif image["parentcolor"] == "B":
            # print(result[36:45], " to ", image["matrix"])
            result[36:45] = image["matrix"]
        elif image["parentcolor"] == "Y":
            # print(result[45:54], " to ", image["matrix"])
            result[45:54] = image["matrix"]

    result = "".join(result)
    return result