from robot.UR3eRobot import UR3eRobot
from DetectAndSortCube_fixed import CubeColorDetectorLive
import math

def initial_grip(koords:list, gripper_robot: UR3eRobot):
    """Initiales Aufnehmen des Würfels basierend auf der Kameraerkennung
    
    :param koords: Koordinaten des Würfels
    :param gripper_robot: Roboter, der greifen soll"""


def handover(current_holder_robot:UR3eRobot, other_robot: UR3eRobot):
    """Übergabe des Würfels zwischen den Robotern
    
    :param current_holder_robot: Roboter, der den Würfel aktuell hält
    :param other_robot: Roboter, der den Würfel übernehmen soll"""


def image1(robot: UR3eRobot, detector: CubeColorDetectorLive):
    """Roboter 4 hält. Die Seite, die initial nach unten lag, wird fotografiert.
    
    :param robot: Roboter, der den Würfel hält (Roboter 4)
    :param detector: Bilderkauswertungsinstanz"""
    p_zwischen = []
    p_foto = []

    robot.moveJ(p_zwischen)
    robot.moveJ(p_foto)

    image = detector.detect_from_camera()
    return image


def image2(robot: UR3eRobot, detector: CubeColorDetectorLive):
    """Roboter 4 hält. Der Würfel wird um 90° gedreht.
    
    :param robot: Roboter, der den Würfel hält (Roboter 4)
    :param detector: Bilderkauswertungsinstanz"""
    p_zwischen = []
    p_foto = []

    robot.moveJ(p_zwischen)
    robot.moveJ(p_foto)

    image = detector.detect_from_camera()
    return image


def image3(robot: UR3eRobot, detector: CubeColorDetectorLive):
    """Roboter 4 hält. Der Würfel wird um 180° gedreht.
    
    :param robot: Roboter, der den Würfel hält (Roboter 4)
    :param detector: Bilderkauswertungsinstanz"""
    robot.move_joint_axis(5,180)

    image = detector.detect_from_camera()
    return image


def image4(robot: UR3eRobot, detector: CubeColorDetectorLive):
    """Roboter 3 hält. Die Seite, die initial nach oben gezeigt hat, wird fotografiert.
    
    :param robot: Roboter, der den Würfel hält (Roboter 3)
    :param detector: Bilderkauswertungsinstanz"""
    p_zwischen = []
    p_foto = []

    robot.moveJ(p_zwischen)
    robot.moveJ(p_foto)

    image = detector.detect_from_camera()
    return image


def image5(robot: UR3eRobot, detector: CubeColorDetectorLive):
    """Roboter 3 hält. Der Würfel wird um 90° gedreht.
    
    :param robot: Roboter, der den Würfel hält (Roboter 3)
    :param detector: Bilderkauswertungsinstanz"""
    p_zwischen = []
    p_foto = []

    robot.moveJ(p_zwischen)
    robot.moveJ(p_foto)

    image = detector.detect_from_camera()
    return image


def image6(robot: UR3eRobot, detector: CubeColorDetectorLive):
    """Roboter 3 hält. Der Würfel wird um 180° gedreht.
    
    :param robot: Roboter, der den Würfel hält (Roboter 3)
    :param detector: Bilderkauswertungsinstanz"""
    robot.move_joint_axis(5, 180)

    image = detector.detect_from_camera()
    return image


def get_initial_images(koords: list, robot_3: UR3eRobot, robot_4: UR3eRobot)->tuple[list[dict]]:
    """Greift den Roboter basierend auf der Kameraerkennung und fährt eine feste Reihenfolge von Positionen für die Bilder ab.

    :param koords: Koordinaten zum Greifen
    :param robot_3: Roboter 3
    :param robot_4: Roboter 4
    :returns: zwei Listen: (images, rotations). Images und Rotations sind jeweils eine Liste von dictionaries.
    """
    
    model_path = r"C:\Users\heyni\Desktop\Studium\Master\Module\2025_26_WS\RSY\Project\RSY_UR3_ROBOT\data\models\best.pt"
    detector = CubeColorDetectorLive(model_path, cam_index=1)

    initial_grip(koords, robot_4) # todo
    image_1 = image1(robot_4, detector) # to test
    image_2 = image2(robot_4, detector) # to test
    image_3 = image3(robot_4, detector) # to test
    handover(current_holder_robot=robot_4, other_robot=robot_3) # todo
    image_4 = image4(robot_3, detector) # to test
    image_5 = image5(robot_3, detector) # to test
    image_6 = image6(robot_3, detector) # to test

    images = [image_1, image_2, image_3, image_4, image_5, image_6]
    rotations = [] # todo

    return (images, rotations)