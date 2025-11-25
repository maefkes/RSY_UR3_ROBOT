import time, json
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QGridLayout, QLabel,
    QTabWidget, QLineEdit, QFileDialog,
    QVBoxLayout, QHBoxLayout, QGroupBox, QMessageBox
)
from PyQt6.QtCore import QSize
import rtde_control  
import rtde_receive

from gripper.robotiq_gripper_real import RobotiqGripperReal
from manager.SettingsManager import SettingsManager
from manager.TeachPositionManager import TeachPositionManager
from gripper.Gripper import Gripper
from robot.UR3eRobot import UR3eRobot
from sensor.Controller import Controller


class TestGui(QTabWidget):
    def __init__(self, homePosRobot3, homePosRobot4, parent=None):
        super().__init__(parent)

        self.homePosRobot3 = homePosRobot3
        self.homePosRobot4 = homePosRobot4

        # Manager
        self.settingsManager = SettingsManager()
        self.teachPositionManager = TeachPositionManager(self.homePosRobot3, self.homePosRobot4)

        # Controller Timer
        self.controllerTimer = QtCore.QTimer()
        self.controllerTimer.timeout.connect(self.pollController)
        self.teachModeRunning = False
        self.activeRobot = None  # Aktuell steuerbarer Roboter

        # Tabs
        self.start = QWidget()
        self.teachMode = QWidget()
        self.settingsMode = QWidget()

        self.addTab(self.start, "Start")
        self.addTab(self.teachMode, "Teach-Modus")
        self.addTab(self.settingsMode, "Einstellungen")

        self.startTab()
        self.teachModeTab()
        self.settingsTab()

        self.setWindowTitle('UR3e - Magic Cube')
        self.setMinimumSize(QSize(300, 650))

        # Roboter & Controller
        self.robot3 = None
        self.robot4 = None
        self.controller = None
        self.gripper = None

    # -------------------- Start Tab --------------------
    def startTab(self):
        layout = QVBoxLayout()

        # Roboter Initialisierung
        groupRobots = QGroupBox("UR3e Roboter – Initialisierung")
        layoutRobots = QGridLayout()
        self.btn_init_r3 = QPushButton("Roboter 3 initialisieren")
        self.btn_init_r4 = QPushButton("Roboter 4 initialisieren")
        self.btn_init_r3.clicked.connect(lambda: self.initializeRobot(3))
        self.btn_init_r4.clicked.connect(lambda: self.initializeRobot(4))
        layoutRobots.addWidget(self.btn_init_r3, 0, 0)
        layoutRobots.addWidget(self.btn_init_r4, 0, 1)
        self.label_robot_status = QLabel("Status: Keine Roboter initialisiert")
        layoutRobots.addWidget(self.label_robot_status, 1, 0, 1, 2)
        groupRobots.setLayout(layoutRobots)
        layout.addWidget(groupRobots)

        # Controller Initialisierung
        groupController = QGroupBox("Controller – Initialisierung")
        layoutController = QGridLayout()
        self.btn_init_controller = QPushButton("Controller verbinden")
        self.btn_init_controller.clicked.connect(self.initializeController)
        self.label_controller_status = QLabel("Status: Kein Controller verbunden")
        layoutController.addWidget(self.btn_init_controller, 0, 0)
        layoutController.addWidget(self.label_controller_status, 1, 0)
        groupController.setLayout(layoutController)
        layout.addWidget(groupController)

        # TCP-Position anzeigen (Roboter 3 & 4 – Buttons nebeneinander)
        groupTCP = QGroupBox("TCP – Position abrufen")
        layoutTCP = QGridLayout()

        # Button Roboter 3
        self.btn_get_tcp_r3 = QPushButton("TCP Roboter 3 anzeigen")
        self.btn_get_tcp_r3.clicked.connect(
            lambda: self.label_tcp_r3.setText(f"TCP R3: {self.robot3.getActualTCPPose()}")
        )
        self.label_tcp_r3 = QLabel("TCP R3: Noch nicht abgefragt")

        # Button Roboter 4
        self.btn_get_tcp_r4 = QPushButton("TCP Roboter 4 anzeigen")
        self.btn_get_tcp_r4.clicked.connect(
            lambda: self.label_tcp_r4.setText(f"TCP R4: {self.robot4.getActualTCPPose()}")
        )
        self.label_tcp_r4 = QLabel("TCP R4: Noch nicht abgefragt")

        layoutTCP.addWidget(self.btn_get_tcp_r3, 0, 0)
        layoutTCP.addWidget(self.btn_get_tcp_r4, 0, 1)

        layoutTCP.addWidget(self.label_tcp_r3, 1, 0)
        layoutTCP.addWidget(self.label_tcp_r4, 1, 1)

        groupTCP.setLayout(layoutTCP)
        layout.addWidget(groupTCP)

        self.start.setLayout(layout)



    # -------------------- Roboter / Controller --------------------
    def initializeRobot(self, robotNumber):
        ip = "192.168.0.3" if robotNumber == 3 else "192.168.0.17"
        homePos = self.homePosRobot3 if robotNumber == 3 else self.homePosRobot4

        try:
            gripperTemplate = RobotiqGripperReal(ip)
            robotControl = rtde_control.RTDEControlInterface(ip)
            robotReceive = rtde_receive.RTDEReceiveInterface(ip)

            robotiqGripper = Gripper(f"robot{robotNumber}", gripperTemplate, self.settingsManager)
            robotiqGripper.initialise()

            robot = UR3eRobot(robotControl, robotReceive, robotiqGripper, self.settingsManager, homePos)
            robot.name = f"robot{robotNumber}"
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Roboter {robotNumber} konnte nicht initialisiert werden:\n{e}")
            return

        if robotNumber == 3:
            self.robot3 = robot
        else:
            self.robot4 = robot

        self.label_robot_status.setText(f"Status: Roboter {robotNumber} erfolgreich initialisiert")
        print(f"Roboter {robotNumber} initialisiert.")

    def initializeController(self):
        try:
            self.controller = Controller()
            self.label_controller_status.setText("Status: Controller verbunden")
            print("Controller erfolgreich verbunden.")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Controller konnte nicht verbunden werden:\n{e}")

    # -------------------- Teach Mode Tab --------------------
    def teachModeTab(self):
        layout = QVBoxLayout()

        groupTeach = QGroupBox("Teach Mode Steuerung")
        layoutTeach = QVBoxLayout()
        label_teach = QLabel("Teach Mode auswählen:")
        label_teach.setStyleSheet("font-weight: bold;")
        layoutTeach.addWidget(label_teach)

        # Roboter Auswahl
        self.btn_teach_r3 = QPushButton("Roboter 3 auswählen")
        self.btn_teach_r3.clicked.connect(lambda: self.setActiveRobot(3))
        self.btn_teach_r4 = QPushButton("Roboter 4 auswählen")
        self.btn_teach_r4.clicked.connect(lambda: self.setActiveRobot(4))
        layoutTeach.addWidget(self.btn_teach_r3)
        layoutTeach.addWidget(self.btn_teach_r4)

        # Teach On / Off
        self.btn_teachOn = QPushButton("Teach Mode ON")
        self.btn_teachOn.clicked.connect(self.teachOnSlot)
        layoutTeach.addWidget(self.btn_teachOn)
        self.btn_teachOff = QPushButton("Teach Mode OFF")
        self.btn_teachOff.setEnabled(False)
        self.btn_teachOff.clicked.connect(self.teachOffSlot)
        layoutTeach.addWidget(self.btn_teachOff)

        # Achsensteuerung
        self.btn_axisFree = QPushButton("Achsen lösen")
        self.btn_axisFree.clicked.connect(self.axisFree)
        layoutTeach.addWidget(self.btn_axisFree)
        self.btn_axisClose = QPushButton("Achsen schließen")
        self.btn_axisClose.setEnabled(False)
        self.btn_axisClose.clicked.connect(self.axisClose)
        layoutTeach.addWidget(self.btn_axisClose)

        self.btn_initialPose = QPushButton("Initialposition anfahren")
        self.btn_initialPose.clicked.connect(self.gotoInitial)
        layoutTeach.addWidget(self.btn_initialPose)

        groupTeach.setLayout(layoutTeach)
        layout.addWidget(groupTeach)

        # Positionen verwalten
        groupPositions = QGroupBox("Positionen verwalten")
        posLayout = QGridLayout()
        posLayout.addWidget(QLabel("Speichere Position:"), 0, 0)
        self.lineEdit_Save = QLineEdit()
        posLayout.addWidget(self.lineEdit_Save, 0, 1)
        self.btn_savePose = QPushButton("Speichern")
        self.btn_savePose.clicked.connect(self.savePosition)
        posLayout.addWidget(self.btn_savePose, 0, 2)

        posLayout.addWidget(QLabel("Gehe zu Position:"), 1, 0)
        self.lineEdit_GoTo = QLineEdit()
        posLayout.addWidget(self.lineEdit_GoTo, 1, 1)
        self.btnMoveSavePos = QPushButton("Anfahren")
        self.btnMoveSavePos.clicked.connect(self.goToPositionSlot)
        posLayout.addWidget(self.btnMoveSavePos, 1, 2)

        self.listWidget_Positions = QtWidgets.QListWidget()
        posLayout.addWidget(self.listWidget_Positions, 2, 0, 1, 3)
        self.btn_refreshPositions = QPushButton("Liste aktualisieren")
        self.btn_refreshPositions.clicked.connect(self.updatePositionList)
        posLayout.addWidget(self.btn_refreshPositions, 3, 0, 1, 3)
        self.btn_exportPositions = QPushButton("Positionen exportieren")
        self.btn_exportPositions.clicked.connect(self.exportPositions)
        posLayout.addWidget(self.btn_exportPositions, 4, 0, 1, 3)
        self.btn_importPositions = QPushButton("Positionen importieren")
        self.btn_importPositions.clicked.connect(self.importPositions)
        posLayout.addWidget(self.btn_importPositions, 5, 0, 1, 3)
        groupPositions.setLayout(posLayout)
        layout.addWidget(groupPositions)

        # Greifersteuerung
        groupGripper = QGroupBox("Greifer Steuerung")
        gripLayout = QHBoxLayout()
        self.btn_gripperOpen = QPushButton("Greifer öffnen")
        self.btn_gripperOpen.clicked.connect(self.openGripper)
        gripLayout.addWidget(self.btn_gripperOpen)
        self.btn_gripperClose = QPushButton("Greifer schließen")
        self.btn_gripperClose.clicked.connect(self.closeGripper)
        gripLayout.addWidget(self.btn_gripperClose)
        groupGripper.setLayout(gripLayout)
        layout.addWidget(groupGripper)

        self.teachMode.setLayout(layout)

    # -------------------- Active Robot --------------------
    def setActiveRobot(self, robotNumber):
        if robotNumber == 3 and self.robot3:
            self.activeRobot = self.robot3
            self.gripper = self.robot3.gripper
            print("Roboter 3 aktiv")
        elif robotNumber == 4 and self.robot4:
            self.activeRobot = self.robot4
            self.gripper = self.robot4.gripper
            print("Roboter 4 aktiv")
        else:
            print(f"Roboter {robotNumber} nicht initialisiert!")

    # -------------------- Teach Mode Funktionen --------------------
    def teachOnSlot(self):
        if not self.activeRobot or not self.controller:
            print("Kein Roboter oder Controller aktiv!")
            return
        self.teachModeRunning = True
        self.controllerTimer.start(10)
        self.btn_teachOn.setEnabled(False)
        self.btn_teachOff.setEnabled(True)

    def teachOffSlot(self):
        self.teachModeRunning = False
        self.controllerTimer.stop()
        if self.activeRobot:
            self.activeRobot.disconnect()
            self.activeRobot.reconnect()
        self.btn_teachOn.setEnabled(True)
        self.btn_teachOff.setEnabled(False)

    def axisFree(self):
        if self.activeRobot:
            self.teachPositionManager.enableTeachMode()
            self.btn_axisFree.setEnabled(False)
            self.btn_axisClose.setEnabled(True)

    def axisClose(self):
        if self.activeRobot:
            self.teachPositionManager.disableTeachMode()
            self.btn_axisFree.setEnabled(True)
            self.btn_axisClose.setEnabled(False)
            print(self.activeRobot.getActualTCPPose())

    def pollController(self):
        if not self.activeRobot or not self.teachModeRunning:
            return
        axes = self.controller.get_axes()
        dx = axes.get("x", 0.0) * 0.1
        dy = axes.get("y", 0.0) * 0.1
        dz = axes.get("ry", 0.0) * 0.1
        d_rx = 0.0
        d_ry = 0.0
        d_rz = axes.get("rx", 0.0) * 0.1
        velocity = [dx, dy, dz, d_rx, d_ry, d_rz]
        self.activeRobot.speedL(velocity)

    # -------------------- Greifer --------------------
    def openGripper(self):
        if self.activeRobot and self.gripper:
            self.gripper.open()

    def closeGripper(self):
        if self.activeRobot and self.gripper:
            self.gripper.close()

    # -------------------- Positionen --------------------
    def savePosition(self):
        if not self.activeRobot:
            print("Kein Roboter aktiv!")
            return
        name = self.lineEdit_Save.text().strip()
        if not name:
            print("Positionsname fehlt.")
            return
        pose = self.activeRobot.getActualTCPPose()
        self.teachPositionManager.addPosition(f"R{self.activeRobot.name[-1]}_{name}", pose)
        print(f"Position '{name}' gespeichert für {self.activeRobot.name}")

    def gotoInitial(self):
        if not self.activeRobot:
            return
        home = self.homePosRobot3 if self.activeRobot.name.endswith("3") else self.homePosRobot4
        self.activeRobot.moveL(home)
        print(self.activeRobot.getActualTCPPose())

    def goToPositionSlot(self):
        if not self.activeRobot:
            return
        name = self.lineEdit_GoTo.text().strip()
        pose = self.teachPositionManager.getSavedPosition(f"R{self.activeRobot.name[-1]}_{name}")
        if pose:
            self.activeRobot.moveL(pose)
        else:
            print("Position nicht gefunden.")

    def updatePositionList(self):
        self.listWidget_Positions.clear()
        self.listWidget_Positions.addItems(self.teachPositionManager.listPositions())

    def exportPositions(self):
        try:
            data = self.teachPositionManager.exportPositions()
            filename, _ = QFileDialog.getSaveFileName(self, "Positionen exportieren", "", "JSON (*.json)")
            if filename:
                with open(filename, "w") as f:
                    f.write(data)
        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))

    def importPositions(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Positionen importieren", "", "JSON (*.json)")
            if filename:
                with open(filename, "r") as f:
                    positions = json.load(f)
                self.teachPositionManager.setAllPositions(positions)
                self.updatePositionList()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))

    # -------------------- Einstellungen --------------------
    def settingsTab(self):
        pass
