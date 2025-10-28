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
