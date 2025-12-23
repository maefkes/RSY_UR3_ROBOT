from robot.UR3eRobot import UR3eRobot
from robot.positions import positions
from robot.pose import pose

from camera.DetectAndSortCube_fixed import CubeColorDetectorLive
import math
import time

def initial_grip(pre_koords:list, koords:list, gripper_robot: UR3eRobot):
    """Initiales Aufnehmen des Würfels basierend auf der Kameraerkennung
    
    :param pre_koords_tcp: Vorposition zum Greifen des Würfels in TCP Koordinaten
    :param pre_koords: Vorposition zum Greifen des Würfels
    :param koords: Koordinaten des Würfels in radiant
    :param gripper_robot: Roboter, der greifen soll"""
    p_initialGrip_pre = pre_koords
    p_initialGrip_tcp = koords

    gripper_robot.openGripper()
    gripper_robot.moveJ(p_initialGrip_pre)
    print("Aktuelle TCP-Position: ", gripper_robot.getActualTCPPose())

    gripper_robot.moveL(p_initialGrip_tcp)
    gripper_robot.closeGripper()
    input("Drücke eine beliebige Taste um fortzufahren...")
    gripper_robot.moveJ(p_initialGrip_pre) # eigentlich besser 


def handover(current_holder_robot:UR3eRobot, positions:positions, other_robot: UR3eRobot):
    """Übergabe des Würfels zwischen den Robotern
    
    :param current_holder_robot: Roboter, der den Würfel aktuell hält
    :param positions: Objekt mit allen notwendigen Positionen
    :param other_robot: Roboter, der den Würfel übernehmen soll"""
    robot4 = current_holder_robot
    robot3 = other_robot

    p_handover_rob3_pre = positions.pose_umgreifen_rob3_pre.getJoint()
    p_handover_rob3 = positions.pose_umgreifen_rob3.getJoint()
    p_handover_rob4_pre = positions.pose_umgreifen_rob4_pre.getJoint()

    robot3.openGripper()
    input("Greifer 3 geöffnet? Drücke eine beliebige Taste um fortzufahren... ")
    robot3.moveJ(p_handover_rob3_pre)
    robot3.moveL_FK(p_handover_rob3)

    robot3.closeGripper()
    input("Greifer 3 geschlossen? Drücke eine beliebige Taste um fortzufahren... ")
    robot4.openGripper()
    input("Greifer 4 geöffnet? Drücke eine beliebige Taste um fortzufahren... ")
    robot4.moveL_FK(p_handover_rob4_pre)
    robot4.moveHome()
    input("Fertig mit Handover. Drücke eine beliebige Taste um mit Roboter 4 fortzufahren...")

def image1(robot: UR3eRobot, position:list, detector: CubeColorDetectorLive):
    """Roboter 4 hält. Die Seite, die initial nach unten lag, wird fotografiert.
    "Einlesen_Down" in Excel_Tabelle
    
    :param robot: Roboter, der den Würfel hält (Roboter 4)
    :param position: Position für das Bild in Joint-Werten
    :param detector: Bilderkauswertungsinstanz"""
    # p_foto = [
    #     math.radians(-131.6), 
    #     math.radians(-130.69),
    #     math.radians(-103.97),
    #     math.radians(-35.45),
    #     math.radians(-90.04),
    #     math.radians(311.29)
    # ]
    robot.moveJ(position)

    image = detector.detect_from_camera()
    return image

def image2(robot: UR3eRobot, position:list, detector: CubeColorDetectorLive):
    """Roboter 4 hält. Der Würfel wird um 90° gedreht.
    
    :param robot: Roboter, der den Würfel hält (Roboter 4)
    :param position: Position für das Bild in Joint-Werten
    :param detector: Bilderkauswertungsinstanz"""
    # p_zwischen = [
    #     math.radians(-122.17),
    #     math.radians(-102.82),
    #     math.radians(-97.79),
    #     math.radians(-38.3),
    #     math.radians(0.78),
    #     math.radians(311.25)
    # ]
    # p_foto = [
    #     math.radians(-72.27), 
    #     math.radians(-84.09),
    #     math.radians(-63.4),
    #     math.radians(147.06),
    #     math.radians(17.3),
    #     math.radians(0.84)       
    # ]
    # robot.moveJ(p_zwischen)
    robot.moveJ(position)

    image = detector.detect_from_camera()
    return image

def image3(robot: UR3eRobot, detector: CubeColorDetectorLive):
    """Roboter 4 hält. Der Würfel wird um 180° gedreht.
    
    :param robot: Roboter, der den Würfel hält (Roboter 4)
    :param detector: Bilderkauswertungsinstanz"""
    robot.move_joint_axis(5,math.radians(180))

    image = detector.detect_from_camera()
    return image

def image4(robot: UR3eRobot, position:list, detector: CubeColorDetectorLive):
    """Roboter 3 hält. Die Seite, die initial nach oben gezeigt hat, wird fotografiert.
    
    :param robot: Roboter, der den Würfel hält (Roboter 3)
    :param position: Joint-Werte des Roboters für Bild 4
    :param detector: Bilderkauswertungsinstanz"""
    # p_foto = [
    #     math.radians(-131.96),	
    #     math.radians(-140.58),	
    #     math.radians(-82.25),
    #     math.radians(-47.27),
    #     math.radians(-89.85),
    #     math.radians(311.97)
    # ]
    robot.moveJ(position)

    image = detector.detect_from_camera()
    return image

def image5(robot: UR3eRobot, position:list, detector: CubeColorDetectorLive):
    """Roboter 3 hält. Der Würfel wird um 90° gedreht.
    
    :param robot: Roboter, der den Würfel hält (Roboter 3)
    :param position: Joint-Werte des Roboters für Bild 5
    :param detector: Bilderkauswertungsinstanz"""
    # robot.moveJ(position)
    robot.move_joint_axis(5, math.radians(180))

    image = detector.detect_from_camera()
    return image

def image6(robot: UR3eRobot, position:list, detector: CubeColorDetectorLive):
    """Roboter 3 hält. Der Würfel wird um 180° gedreht.
    
    :param robot: Roboter, der den Würfel hält (Roboter 3)
    :param position: Joint-Werte des Roboters für das Bild
    :param detector: Bilderkauswertungsinstanz"""
    # robot.move_joint_axis(5, math.radians(180))
    robot.moveJ(position)

    image = detector.detect_from_camera()
    return image

def get_robot4_images(robot_4:UR3eRobot, positions:positions, detector: CubeColorDetectorLive)->list[dict]:
    """Macht die Bilder und die Auswertung für die ersten drei Seiten (Roboter 4)
    
    :param robot_4: Roboter 4, der den Würfel aktuell hält
    :param positions: Klasse, die alle Positionen enthält
    :param detector: Bildauswertungsinstanz
    :returns: Eine Liste mit den Bildauswertungen, jeweils als dictionary."""
    p_image_1 = positions.pose_image_1.getJoint()
    image_1 = image1(robot_4, p_image_1, detector)
    input("Position 1 fertig. Drücke eine Taste um mit Position 2 fortzufahren...")
    p_image_2 = positions.pose_image_2.getJoint()
    image_2 = image2(robot_4, p_image_2, detector)
    input("Position 2 fertig. Drücke eine Taste um mit Position 3 fortzufahren...")
    image_3 = image3(robot_4, detector)
    input("Position 3 fertig. Drücke eine Taste um mit Roboter 4 abzuschließen...")
    images = [image_1, image_2, image_3]
    return images

def get_robot3_images(robot_3:UR3eRobot, positions:positions, detector: CubeColorDetectorLive)->tuple[list[dict]]:
    """Macht die Bilder und die Auswertung für die ersten drei Seiten (Roboter 4)
    
    :param robot_3: Roboter 3, der den Würfel aktuell hält
    :param positions: Klasse, die alle Positionsdaten enthält
    :param detector: Bildauswertungsinstanz
    :returns: Eine Liste mit den Bildauswertungen, jeweils als dictionary."""
    p_image_4 = positions.pose_image_4.getJoint()
    image_4 = image4(robot_3, p_image_4, detector)
    input("Position 1 fertig. Drücke eine Taste um mit Position 2 fortzufahren...")
    p_image_5 = positions.pose_image_5.getJoint()
    image_5 = image5(robot_3, p_image_5, detector)
    input("Position 2 fertig. Drücke eine Taste um mit Position 3 fortzufahren...")
    p_image_6 = positions.pose_image_6.getJoint()
    image_6 = image6(robot_3, p_image_6, detector)
    input("Position 3 fertig. Drücke eine Taste um mit Roboter 3 abzuschließen...")
    images = [image_4, image_5, image_6]
    return images

def get_initial_images(positions: positions, robot_3: UR3eRobot, robot_4: UR3eRobot)->tuple[list[dict]]:
    """Greift den Roboter basierend auf der Kameraerkennung und fährt eine feste Reihenfolge von Positionen für die Bilder ab.

    :param positions: Koordinaten zum Greifen
    :param robot_3: Roboter 3
    :param robot_4: Roboter 4
    :returns: zwei Listen: (images, rotations). Images und Rotations sind jeweils eine Liste von dictionaries.
    """
    
    # Detektor initialisieren
    model_path = r"C:\Users\heyni\Desktop\Studium\Master\Module\2025_26_WS\RSY\Project\RSY_UR3_ROBOT\data\models\20251223.pt"
    detector = CubeColorDetectorLive(model_path, cam_index=1)
    images = []

    # initial Grip
    p_ausrichten_greifen_pre = positions.pose_initialGrip_pre.getJoint()
    p_ausrichten_greifen_tcp = positions.pose_initialGrip.getCartesian()
    initial_grip(p_ausrichten_greifen_pre, p_ausrichten_greifen_tcp, robot_4)

    # Bilder machen
    images.append(get_robot4_images(robot_4, positions, detector))
    handover(current_holder_robot=robot_4, positions=positions, other_robot=robot_3)
    images.append(get_robot3_images(robot_3, positions, detector))

    # Rotationen sind fix
    rotations = [] # todo

    return (images, rotations)