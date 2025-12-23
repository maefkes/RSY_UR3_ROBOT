from robot.pose import pose
from robot.UR3eRobot import UR3eRobot
import math
from copy import copy, deepcopy

# initiales Greifen
p_initialGrip_pre = [
    math.radians(-141.17),
    math.radians(-90.51),
    math.radians(-115.97),
    math.radians(-29.21),
    math.radians(67.23),
    math.radians(77.47),
]
p_initialGrip = [
    math.radians(-142.07),
    math.radians(-105.08),
    math.radians(-120.45),
    math.radians(-4.17),
    math.radians(63.31),
    math.radians(74.23),
]

# Einlesepositionen
p_image_1 = [
    math.radians(-131.6),
    math.radians(-130.69),
    math.radians(-103.97),
    math.radians(-35.45),
    math.radians(-90.04),
    math.radians(311.29),    
]
p_image_2 = [
    math.radians(-72.27),
    math.radians(-84.09),
    math.radians(-63.4),
    math.radians(147.06),
    math.radians(17.3),
    math.radians(0.84),  
]
p_image_3 = [
    math.radians(-72.29),
    math.radians(-77.74),
    math.radians(-114.2),
    math.radians(15.74),
    math.radians(-16.99),
    math.radians(357.38),  
]
p_image_6 = [
    math.radians(-131.96),
    math.radians(-140.58),
    math.radians(-82.25),
    math.radians(-47.27),
    math.radians(-89.85),
    math.radians(311.97),
]
p_image_4 = [
    math.radians(-87.5),
    math.radians(-103.96),
    math.radians(-83.6),
    math.radians(42.36),
    math.radians(-1.84),
    math.radians(326.27),
]
p_image_5 = [
    math.radians(-87.53),
    math.radians(-88.73),
    math.radians(-106.05),
    math.radians(-1),
    math.radians(-1.98),
    math.radians(196.28),    
]

# Umgreifpositionen
p_umgreifen_rob4 =      [
    math.radians(-72.29),    
    math.radians(-77.74),
    math.radians(-114.2),
    math.radians(15.74),
    math.radians(-16.99),
    math.radians(357.38),
]
p_umgreifen_rob3_pre =  [
    math.radians(-72.57),    
    math.radians(-87.92),
    math.radians(-106.73),
    math.radians(15.54),
    math.radians(-16.3),
    math.radians(89.58),
]
p_umgreifen_rob3 =      [
    math.radians(-87.5),    
    math.radians(-96.73),
    math.radians(-97.15),
    math.radians(23.73),
    math.radians(-1.4),
    math.radians(80.53),
]

# Drehoperationen
p_rotU_rob4 = copy()
p_rotU_rob3 = copy()
p_rotR_rob4 = copy()
p_rotR_rob3 = copy()
p_rotL_rob4 = copy()
p_rotL_rob3 = copy()


class positions:
    """Klasse, die alle notwendigen Positionen enthält"""
    def __init__(self, robot_3:UR3eRobot, robot_4:UR3eRobot):
        # initial Grip
        self.pose_initialGrip_pre = pose(robot_4.rtdeControl)
        self.pose_initialGrip_pre.setJoint(p_initialGrip_pre)
        self.pose_initialGrip = pose(robot_4.rtdeControl)
        self.pose_initialGrip.setJoint(p_initialGrip)

        # Bilder mit Roboter 4
        self.pose_image_1 = pose(robot_4.rtdeControl)
        self.pose_image_1.setJoint(p_image_1)
        self.pose_image_1.setRotEuler([0,0,-90])
        self.pose_image_2 = pose(robot_4.rtdeControl)
        self.pose_image_2.setJoint(p_image_2)
        self.pose_image_2.setRotEuler([90,0,-90])
        self.pose_image_3 = pose(robot_4.rtdeControl)
        self.pose_image_3.setJoint(p_image_3)
        self.pose_image_3.setRotEuler([-90,0,90])
        
        # Bilder mit Roboter 3
        self.pose_image_4 = pose(robot_3.rtdeControl)
        self.pose_image_4.setJoint(p_image_4)
        self.pose_image_4.setRotEuler([-90,0,90])
        self.pose_image_5 = pose(robot_3.rtdeControl)
        self.pose_image_5.setJoint(p_image_5)
        self.pose_image_5.setRotEuler([90,0,-90])
        self.pose_image_6 = pose(robot_3.rtdeControl)
        self.pose_image_6.setJoint(p_image_6)
        self.pose_image_6.setRotEuler([0,0,-90])

        # Umgreifoperationen
        self.pose_umgreifen_rob4 = pose(robot_4.rtdeControl)
        self.pose_umgreifen_rob4.setJoint(copy(p_umgreifen_rob4))
        self.pose_umgreifen_rob4.setRotEuler([-90,0,90])
        self.pose_umgreifen_rob3_pre = pose(robot_3.rtdeControl)
        self.pose_umgreifen_rob3_pre.setJoint(copy(p_umgreifen_rob3_pre))
        self.pose_umgreifen_rob3_pre.setRotEuler([0,-90,0])
        self.pose_umgreifen_rob3 = pose(robot_3.rtdeControl)
        self.pose_umgreifen_rob3.setJoint(copy(p_umgreifen_rob3))
        self.pose_umgreifen_rob3.setRotEuler([0,-90,0])

        # Vorposition für rob4 aus Position ermitteln
        self.pose_umgreifen_rob4_pre = pose(robot_4.rtdeControl)
        self.pose_umgreifen_rob4_pre.setJoint(copy(p_umgreifen_rob4))
        self.pose_umgreifen_rob4_pre.transInMeters[0] = self.pose_umgreifen_rob4_pre.transInMeters[0] + 50/1000
        self.pose_umgreifen_rob4_pre.setRotEuler([-90,0,90])

        # Positionen für die Operationen

        # rot U
        self.pose_rotU_rob3 = pose(robot_3.rtdeControl)
        self.pose_rotU_rob3.setJoint(copy(p_umgreifen_rob3))
        self.pose_rotU_rob3.setRotEuler([0,-90,0])

        self.pose_rotU_rob4 = pose(robot_4.rtdeControl)
        self.pose_rotU_rob4.setJoint(copy(p_umgreifen_rob4))
        self.pose_rotU_rob4.setRotEuler([90,0,-90])
        self.pose_rotU_rob4.transInMeters[0] = self.pose_rotU_rob4.transInMeters[0] + 16/1000

        self.pose_rotU_rob4_pre = pose(robot_4.rtdeControl)
        self.pose_rotU_rob4_pre.setJoint(copy(p_umgreifen_rob4))
        self.pose_rotU_rob4_pre.transInMeters[0] = self.pose_rotU_rob4.transInMeters[0] + 35/1000
        self.pose_rotU_rob4_pre.setRotEuler([90,0,-90])

        # rot L
        self.pose_rotL_rob3 = pose(robot_3.rtdeControl)
        self.pose_rotL_rob3.setJoint(copy(p_umgreifen_rob3))
        self.pose_rotL_rob3.setRotEuler([0,0,90])

        self.pose_rotL_rob4 = pose(robot_4.rtdeControl)
        self.pose_rotL_rob4.setJoint(copy(p_umgreifen_rob4))
        self.pose_rotL_rob4.setRotEuler([90,0,-90])
        self.pose_rotL_rob4.transInMeters[0] = self.pose_rotL_rob4.transInMeters[0] + 16/1000

        self.pose_rotL_rob4_pre = pose(robot_4.rtdeControl)
        self.pose_rotL_rob4_pre.setJoint(copy(p_umgreifen_rob4))
        self.pose_rotL_rob4_pre.transInMeters[0] = self.pose_rotL_rob4.transInMeters[0] + 35/1000
        self.pose_rotL_rob4_pre.setRotEuler([90,0,-90])

        # rot R
        self.pose_rotR_rob3 = pose(robot_3.rtdeControl)
        self.pose_rotR_rob3.setJoint(copy(p_umgreifen_rob3))
        self.pose_rotR_rob3.setRotEuler([0,0,-90])

        self.pose_rotR_rob4 = pose(robot_4.rtdeControl)
        self.pose_rotR_rob4.setJoint(copy(p_umgreifen_rob4))
        self.pose_rotR_rob4.setRotEuler([90,0,-90])
        self.pose_rotR_rob4.transInMeters[0] = self.pose_rotR_rob4.transInMeters[0] + 16/1000

        self.pose_rotR_rob4_pre = pose(robot_4.rtdeControl)
        self.pose_rotR_rob4_pre.setJoint(copy(p_umgreifen_rob4))
        self.pose_rotR_rob4_pre.transInMeters[0] = self.pose_rotR_rob4.transInMeters[0] + 35/1000
        self.pose_rotR_rob4_pre.setRotEuler([90,0,-90])
