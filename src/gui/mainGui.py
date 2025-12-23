import time
import json
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QGridLayout, QLabel,
    QTabWidget, QLineEdit, QFileDialog,
    QVBoxLayout, QHBoxLayout, QGroupBox, QMessageBox
)
from PyQt6.QtCore import QSize

from manager.SettingsManager import SettingsManager
from manager.TeachPositionManager import TeachPositionManager
from robot.UR3eRobot import UR3eRobot
from camera.DetectAndSortCube_fixed import CubeColorDetectorLive
from rubiks_cube_execution import *


# ==================== Farb-Mapping ====================
CUBE_COLOR_MAP = {
    "w": "#FFFFFF",
    "r": "#FF0000",
    "b": "#0000FF",
    "o": "#FFA500",
    "g": "#00FF00",
    "y": "#FFFF00",
}


# ==================== Cube Widgets ====================
class CubeFaceWidget(QWidget):
    def __init__(self, face_data, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(2, 2, 2, 2)

        for i in range(9):
            row, col = divmod(i, 3)
            label = QLabel()
            label.setFixedSize(24, 24)
            color = CUBE_COLOR_MAP.get(face_data[i], "#000000")
            label.setStyleSheet(
                f"background-color: {color}; border: 1px solid black;"
            )
            layout.addWidget(label, row, col)

        self.setLayout(layout)


class CubeWidget(QWidget):
    def __init__(self, faces: dict, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        layout.setSpacing(8)

        layout.addWidget(CubeFaceWidget(faces["+z"]), 0, 1)
        layout.addWidget(CubeFaceWidget(faces["-x"]), 1, 0)
        layout.addWidget(CubeFaceWidget(faces["+x"]), 1, 1)
        layout.addWidget(CubeFaceWidget(faces["-y"]), 1, 2)
        layout.addWidget(CubeFaceWidget(faces["+y"]), 2, 1)
        layout.addWidget(CubeFaceWidget(faces["-z"]), 1, 3)

        self.setLayout(layout)


# ==================== Main GUI ====================
class MainGui(QTabWidget):
    def __init__(self, homePosRobot3, homePosRobot4, parent=None):
        super().__init__(parent)

        self.homePosRobot3 = homePosRobot3
        self.homePosRobot4 = homePosRobot4

        self.settingsManager = SettingsManager()
        self.teachPositionManager = TeachPositionManager(
            self.homePosRobot3, self.homePosRobot4
        )

        self.robot3 = None
        self.robot4 = None
        #self.initializeRobot(3)
        #self.initializeRobot(4)
        rubiksCubeExe_init(self.robot3, self.robot4)

        self.cubeColorDetetctor = CubeColorDetectorLive("best.pt")

        self.start = QWidget()
        self.settingsMode = QWidget()

        self.addTab(self.start, "Start")
        self.addTab(self.settingsMode, "Einstellungen")

        self.startTab()
        self.settingsTab()

        self.setWindowTitle("UR3e – Rubik's Cube")
        self.setMinimumSize(QSize(420, 720))


    # ==================== START TAB ====================
    def startTab(self):
        layout = QVBoxLayout()

        # ---------- TCP Gruppe ----------
        groupTCP = QGroupBox("TCP – Position abrufen")
        layoutTCP = QGridLayout()

        self.btn_get_tcp_r3 = QPushButton("TCP Robot 3")
        self.btn_get_tcp_r4 = QPushButton("TCP Robot 4")
        self.label_tcp_r3 = QLabel("Robot 3 TCP: ---")
        self.label_tcp_r4 = QLabel("Robot 4 TCP: ---")

        layoutTCP.addWidget(self.btn_get_tcp_r3, 0, 0)
        layoutTCP.addWidget(self.btn_get_tcp_r4, 0, 1)
        layoutTCP.addWidget(self.label_tcp_r3, 1, 0)
        layoutTCP.addWidget(self.label_tcp_r4, 1, 1)

        groupTCP.setLayout(layoutTCP)
        layout.addWidget(groupTCP)

        # ---------- Cube Anzeige ----------
        groupCube = QGroupBox("Rubik's Cube")
        cubeLayout = QVBoxLayout()

        #test_string = (
         
         #"wwwwwwwww"  # +z
         #"rrrrrrrrr"  # -y
         #"ggggggggg"  # +x
         #"bbbbbbbbb"  # +y
         #"ooooooooo"  # -x
         #"yyyyyyyyy"  # -z
         #)
        string = rubiksCubeExe_getColorString()
        faces = self.decodeColorString(string)

        self.cubeWidget = CubeWidget(faces)
        cubeLayout.addWidget(self.cubeWidget)

        groupCube.setLayout(cubeLayout)
        layout.addWidget(groupCube)

        layout.addStretch()
        self.start.setLayout(layout)


    # ==================== Cube Logik ====================
    def decodeColorString(self, colors: str):
        if len(colors) != 54:
            raise ValueError("Der Farbstring muss exakt 54 Zeichen lang sein")

        return {
            "+z": list(colors[0:9]),
            "-y": list(colors[9:18]),
            "+x": list(colors[18:27]),
            "+y": list(colors[27:36]),
            "-x": list(colors[36:45]),
            "-z": list(colors[45:54]),
        }


    def updateCube(self, color_string: str):
        faces = self.decodeColorString(color_string)
        self.cubeWidget.setParent(None)
        self.cubeWidget = CubeWidget(faces)
        self.start.layout().itemAt(1).widget().layout().addWidget(self.cubeWidget)


    # ==================== ROBOT INIT ====================
    def initializeRobot(self, robotNumber):
        ip = "192.168.0.3" if robotNumber == 3 else "192.168.0.17"
        homePos = self.homePosRobot3 if robotNumber == 3 else self.homePosRobot4
        robotName = f"robot{robotNumber}"

        try:
            robot = UR3eRobot(ip, self.settingsManager, homePos, robotName)
            robot.name = robotName
        except Exception as e:
            QMessageBox.critical(
                self, "Fehler",
                f"Roboter {robotNumber} konnte nicht initialisiert werden:\n{e}"
            )
            return

        if robotNumber == 3:
            self.robot3 = robot
        else:
            self.robot4 = robot


    # ==================== SETTINGS TAB ====================
    def settingsTab(self):
        mainLayout = QVBoxLayout()

        # ---------- Robot 3 ----------
        groupRobot3 = QGroupBox("Roboter 3 Einstellungen")
        layoutR3 = QGridLayout()

        self.spin_r3_axis_speed = QtWidgets.QDoubleSpinBox()
        self.spin_r3_axis_speed.setRange(0.0, 1.0)
        self.spin_r3_axis_speed.setValue(
            self.settingsManager.get("robot3", "axis", "SPEED")
        )

        self.spin_r3_axis_acc = QtWidgets.QDoubleSpinBox()
        self.spin_r3_axis_acc.setRange(0.0, 1.0)
        self.spin_r3_axis_acc.setValue(
            self.settingsManager.get("robot3", "axis", "ACCELERATION")
        )

        layoutR3.addWidget(QLabel("Achsen Geschwindigkeit"), 0, 0)
        layoutR3.addWidget(self.spin_r3_axis_speed, 0, 1)
        layoutR3.addWidget(QLabel("Achsen Beschleunigung"), 1, 0)
        layoutR3.addWidget(self.spin_r3_axis_acc, 1, 1)

        groupRobot3.setLayout(layoutR3)
        mainLayout.addWidget(groupRobot3)

        # ---------- Robot 4 ----------
        groupRobot4 = QGroupBox("Roboter 4 Einstellungen")
        layoutR4 = QGridLayout()

        self.spin_r4_axis_speed = QtWidgets.QDoubleSpinBox()
        self.spin_r4_axis_speed.setRange(0.0, 1.0)
        self.spin_r4_axis_speed.setValue(
            self.settingsManager.get("robot4", "axis", "SPEED")
        )

        self.spin_r4_axis_acc = QtWidgets.QDoubleSpinBox()
        self.spin_r4_axis_acc.setRange(0.0, 1.0)
        self.spin_r4_axis_acc.setValue(
            self.settingsManager.get("robot4", "axis", "ACCELERATION")
        )

        layoutR4.addWidget(QLabel("Achsen Geschwindigkeit"), 0, 0)
        layoutR4.addWidget(self.spin_r4_axis_speed, 0, 1)
        layoutR4.addWidget(QLabel("Achsen Beschleunigung"), 1, 0)
        layoutR4.addWidget(self.spin_r4_axis_acc, 1, 1)

        groupRobot4.setLayout(layoutR4)
        mainLayout.addWidget(groupRobot4)

        mainLayout.addStretch()
        self.settingsMode.setLayout(mainLayout)
