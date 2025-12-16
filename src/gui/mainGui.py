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


class MainGui(QTabWidget):
    def __init__(self, homePosRobot3, homePosRobot4, parent=None):
        super().__init__(parent)

        # Home-Pos für Roboter
        self.homePosRobot3 = homePosRobot3
        self.homePosRobot4 = homePosRobot4

        # Manager
        self.settingsManager = SettingsManager()
        self.teachPositionManager = TeachPositionManager(self.homePosRobot3, self.homePosRobot4)

        # Roboter Initialisierung
        self.robot3 = None
        self.robot4 = None
        self.initializeRobot(3)
        self.initializeRobot(4)
        
        # Kamera / Detector
        self.cubeColorDetetctor = CubeColorDetectorLive("best.pt")
        self.selected_image_path = None

        # Tabs
        self.start = QWidget()
        self.settingsMode = QWidget()

        self.addTab(self.start, "Start")
        self.addTab(self.settingsMode, "Einstellungen")

        # initialisiere GUI-Contents
        self.startTab()
        self.settingsTab()

        self.setWindowTitle('UR3e - Rubics Cube')
        self.setMinimumSize(QSize(320, 720))


    # -------------------- Start Tab ------------------------------------------------------------------------------------------------------------
    def startTab(self):
        layout = QVBoxLayout()

        # -----------------------------------------
        # TCP Positionen – Roboter 3 & 4
        # -----------------------------------------
        groupTCP = QGroupBox("TCP – Position abrufen")
        layoutTCP = QGridLayout()

        layoutTCP.addWidget(self.btn_get_tcp_r3, 0, 0)
        layoutTCP.addWidget(self.btn_get_tcp_r4, 0, 1)
        layoutTCP.addWidget(self.label_tcp_r3, 1, 0)
        layoutTCP.addWidget(self.label_tcp_r4, 1, 1)

        groupTCP.setLayout(layoutTCP)
        layout.addWidget(groupTCP)

        # Layout anwenden
        self.start.setLayout(layout)


    def initializeRobot(self, robotNumber):
        ip = "192.168.0.3" if robotNumber == 3 else "192.168.0.17"
        homePos = self.homePosRobot3 if robotNumber == 3 else self.homePosRobot4
        robotName = f"robot{robotNumber}"

        try:
            robot = UR3eRobot(ip, self.settingsManager, homePos, robotName)
            robot.name = robotName
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Roboter {robotNumber} konnte nicht initialisiert werden:\n{e}")
            return

        if robotNumber == 3:
            self.robot3 = robot
        else:
            self.robot4 = robot

        self.label_robot_status.setText(f"Status: Roboter {robotNumber} erfolgreich initialisiert")
        print(f"Roboter {robotNumber} initialisiert.")


    def toggleAutoMode(self):
        if self.btn_auto_mode.isChecked():
            self.btn_auto_mode.setText("Automatikmodus an")
            try:
                self.cubeColorDetetctor.detect_from_camera()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Automatik-Kamera konnte nicht gestartet werden:\n{e}")
                self.btn_auto_mode.setChecked(False)
                self.btn_auto_mode.setText("Automatikmodus aus")
        else:
            self.btn_auto_mode.setText("Automatikmodus aus")
            # Falls detect_from_camera einen Thread/Loop startet, das Stoppen dort implementieren.
            # Wir versuchen, falls vorhanden, eine stop-Funktion aufzurufen.
            stop_fn = getattr(self.cubeColorDetetctor, "stop_camera_loop", None)
            if callable(stop_fn):
                stop_fn()


    # -------------------- Einstellungen --------------------
    def settingsTab(self):
        mainLayout = QVBoxLayout()

        # ================= Roboter 3 =================
        groupRobot3 = QGroupBox("Roboter 3 Einstellungen")
        layoutR3 = QGridLayout()

        # Achsen
        layoutR3.addWidget(QLabel("Achsen - Geschwindigkeit:"), 0, 0)
        self.spin_r3_axis_speed = QtWidgets.QDoubleSpinBox()
        self.spin_r3_axis_speed.setRange(0.0, 1.0)
        self.spin_r3_axis_speed.setSingleStep(0.01)
        self.spin_r3_axis_speed.setValue(self.settingsManager.get("robot3", "axis", "SPEED"))
        self.spin_r3_axis_speed.valueChanged.connect(
            lambda val: self.settingsManager.set("robot3", "axis", "SPEED", val)
        )
        layoutR3.addWidget(self.spin_r3_axis_speed, 0, 1)

        layoutR3.addWidget(QLabel("Achsen - Beschleunigung:"), 1, 0)
        self.spin_r3_axis_acc = QtWidgets.QDoubleSpinBox()
        self.spin_r3_axis_acc.setRange(0.0, 1.0)
        self.spin_r3_axis_acc.setSingleStep(0.01)
        self.spin_r3_axis_acc.setValue(self.settingsManager.get("robot3", "axis", "ACCELERATION"))
        self.spin_r3_axis_acc.valueChanged.connect(
            lambda val: self.settingsManager.set("robot3", "axis", "ACCELERATION", val)
        )
        layoutR3.addWidget(self.spin_r3_axis_acc, 1, 1)

        # Greifer
        layoutR3.addWidget(QLabel("Greifer - Kraft:"), 2, 0)
        self.slider_r3_force = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_r3_force.setRange(0, 255)
        self.slider_r3_force.setValue(self.settingsManager.get("robot3", "gripper", "FORCE"))
        self.slider_r3_force.valueChanged.connect(
            lambda val: self.settingsManager.set("robot3", "gripper", "FORCE", val)
        )
        layoutR3.addWidget(self.slider_r3_force, 2, 1)

        layoutR3.addWidget(QLabel("Greifer - Geschwindigkeit:"), 3, 0)
        self.slider_r3_speed = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_r3_speed.setRange(0, 255)
        self.slider_r3_speed.setValue(self.settingsManager.get("robot3", "gripper", "SPEED"))
        self.slider_r3_speed.valueChanged.connect(
            lambda val: self.settingsManager.set("robot3", "gripper", "SPEED", val)
        )
        layoutR3.addWidget(self.slider_r3_speed, 3, 1)

        layoutR3.addWidget(QLabel("Greifer - Position:"), 4, 0)
        self.slider_r3_position = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_r3_position.setRange(0, 255)
        self.slider_r3_position.setValue(self.settingsManager.get("robot3", "gripper", "POSITION"))
        self.slider_r3_position.valueChanged.connect(
            lambda val: self.settingsManager.set("robot3", "gripper", "POSITION", val)
        )
        layoutR3.addWidget(self.slider_r3_position, 4, 1)

        groupRobot3.setLayout(layoutR3)
        mainLayout.addWidget(groupRobot3)

        # ================= Roboter 4 =================
        groupRobot4 = QGroupBox("Roboter 4 Einstellungen")
        layoutR4 = QGridLayout()

        # Achsen
        layoutR4.addWidget(QLabel("Achsen - Geschwindigkeit:"), 0, 0)
        self.spin_r4_axis_speed = QtWidgets.QDoubleSpinBox()
        self.spin_r4_axis_speed.setRange(0.0, 1.0)
        self.spin_r4_axis_speed.setSingleStep(0.01)
        self.spin_r4_axis_speed.setValue(self.settingsManager.get("robot4", "axis", "SPEED"))
        self.spin_r4_axis_speed.valueChanged.connect(
            lambda val: self.settingsManager.set("robot4", "axis", "SPEED", val)
        )
        layoutR4.addWidget(self.spin_r4_axis_speed, 0, 1)

        layoutR4.addWidget(QLabel("Achsen - Beschleunigung:"), 1, 0)
        self.spin_r4_axis_acc = QtWidgets.QDoubleSpinBox()
        self.spin_r4_axis_acc.setRange(0.0, 1.0)
        self.spin_r4_axis_acc.setSingleStep(0.01)
        self.spin_r4_axis_acc.setValue(self.settingsManager.get("robot4", "axis", "ACCELERATION"))
        self.spin_r4_axis_acc.valueChanged.connect(
            lambda val: self.settingsManager.set("robot4", "axis", "ACCELERATION", val)
        )
        layoutR4.addWidget(self.spin_r4_axis_acc, 1, 1)

        # Greifer
        layoutR4.addWidget(QLabel("Greifer - Kraft:"), 2, 0)
        self.slider_r4_force = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_r4_force.setRange(0, 255)
        self.slider_r4_force.setValue(self.settingsManager.get("robot4", "gripper", "FORCE"))
        self.slider_r4_force.valueChanged.connect(
            lambda val: self.settingsManager.set("robot4", "gripper", "FORCE", val)
        )
        layoutR4.addWidget(self.slider_r4_force, 2, 1)

        layoutR4.addWidget(QLabel("Greifer - Geschwindigkeit:"), 3, 0)
        self.slider_r4_speed = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_r4_speed.setRange(0, 255)
        self.slider_r4_speed.setValue(self.settingsManager.get("robot4", "gripper", "SPEED"))
        self.slider_r4_speed.valueChanged.connect(
            lambda val: self.settingsManager.set("robot4", "gripper", "SPEED", val)
        )
        layoutR4.addWidget(self.slider_r4_speed, 3, 1)

        layoutR4.addWidget(QLabel("Greifer - Position:"), 4, 0)
        self.slider_r4_position = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_r4_position.setRange(0, 255)
        self.slider_r4_position.setValue(self.settingsManager.get("robot4", "gripper", "POSITION"))
        self.slider_r4_position.valueChanged.connect(
            lambda val: self.settingsManager.set("robot4", "gripper", "POSITION", val)
        )
        layoutR4.addWidget(self.slider_r4_position, 4, 1)

        groupRobot4.setLayout(layoutR4)
        mainLayout.addWidget(groupRobot4)

        # Layout anwenden
        self.settingsMode.setLayout(mainLayout)

    # -------------------- Hilfsmethoden für Settings (roboterabhängig) --------------------
    def updateSettingsWidgets(self, robotName):
        """
        Lädt die aktuellen Werte des gewählten Roboters in die Widgets.
        robotName erwartet 'robot3' oder 'robot4'.
        """
        if robotName == "robot3":
            self.spin_r3_axis_speed.blockSignals(True)
            self.spin_r3_axis_acc.blockSignals(True)
            self.slider_r3_force.blockSignals(True)
            self.slider_r3_speed.blockSignals(True)
            self.slider_r3_position.blockSignals(True)

            self.spin_r3_axis_speed.setValue(self.settingsManager.get("robot3", 'axis', 'SPEED'))
            self.spin_r3_axis_acc.setValue(self.settingsManager.get("robot3", 'axis', 'ACCELERATION'))
            self.slider_r3_force.setValue(self.settingsManager.get("robot3", 'gripper', 'FORCE'))
            self.slider_r3_speed.setValue(self.settingsManager.get("robot3", 'gripper', 'SPEED'))
            self.slider_r3_position.setValue(self.settingsManager.get("robot3", 'gripper', 'POSITION'))

            self.spin_r3_axis_speed.blockSignals(False)
            self.spin_r3_axis_acc.blockSignals(False)
            self.slider_r3_force.blockSignals(False)
            self.slider_r3_speed.blockSignals(False)
            self.slider_r3_position.blockSignals(False)

        elif robotName == "robot4":
            self.spin_r4_axis_speed.blockSignals(True)
            self.spin_r4_axis_acc.blockSignals(True)
            self.slider_r4_force.blockSignals(True)
            self.slider_r4_speed.blockSignals(True)
            self.slider_r4_position.blockSignals(True)

            self.spin_r4_axis_speed.setValue(self.settingsManager.get("robot4", 'axis', 'SPEED'))
            self.spin_r4_axis_acc.setValue(self.settingsManager.get("robot4", 'axis', 'ACCELERATION'))
            self.slider_r4_force.setValue(self.settingsManager.get("robot4", 'gripper', 'FORCE'))
            self.slider_r4_speed.setValue(self.settingsManager.get("robot4", 'gripper', 'SPEED'))
            self.slider_r4_position.setValue(self.settingsManager.get("robot4", 'gripper', 'POSITION'))

            self.spin_r4_axis_speed.blockSignals(False)
            self.spin_r4_axis_acc.blockSignals(False)
            self.slider_r4_force.blockSignals(False)
            self.slider_r4_speed.blockSignals(False)
            self.slider_r4_position.blockSignals(False)

    def updateSetting(self, robotName, group, name, value):
        """
        Speichert einen Wert in SettingsManager für den angegebenen Roboter.
        robotName: 'robot3' oder 'robot4'
        """
        try:
            self.settingsManager.set(robotName, group, name, value)
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Setting konnte nicht gespeichert werden:\n{e}")
