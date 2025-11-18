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


class MainWindow(QTabWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Homepositionen
        self.homePosRobot3 = [-0.3348824484632403, -0.13811531146380698, 0.2610392430112353,
                              1.0415257012533956, 2.9503966505304193, 0.024981329326417064]

        self.homePosRobot4 = [-0.3348824484632403, -0.13811531146380698, 0.2610392430112353,
                             -1.0415257012533956, -2.9503966505304193, 0.024981329326417064]

        # Managers
        self.settingsManager = SettingsManager()
        self.teachPositionManager = TeachPositionManager(self.homePosRobot3, self.homePosRobot4)
        
        # Controller timer
        self.controllerTimer = QtCore.QTimer()
        self.controllerTimer.timeout.connect(self.pollController)
        self.teachModeRunning = False

        # GUI Tabs
        self.start = QWidget()
        self.teachMode = QWidget()
        self.settingsMode = QWidget()

        self.addTab(self.start, "Start")
        self.addTab(self.teachMode, "Teach-Modus")
        self.addTab(self.settingsMode, "Einstellungen")

        # Build tabs
        self.startTab()
        self.teachModeTab()
        self.settingsTab()

        self.setWindowTitle('UR3e - Magic Cube')
        self.setMinimumSize(QSize(300, 650))

        # Robot instances
        self.robot3 = None
        self.robot4 = None
        self.controller = None
        self.gripper = None


    # ------------------------------------------------------------
    # Start Tab
    # ------------------------------------------------------------
    def startTab(self):
        layout = QVBoxLayout()

        groupRobots = QGroupBox("UR3e Roboter – Initialisierung")
        layoutRobots = QGridLayout()

        # Buttons
        self.btn_init_r3 = QPushButton("Roboter 3 initialisieren")
        self.btn_init_r4 = QPushButton("Roboter 4 initialisieren")

        self.btn_init_r3.clicked.connect(lambda: self.initializeRobot(3))
        self.btn_init_r4.clicked.connect(lambda: self.initializeRobot(4))

        layoutRobots.addWidget(self.btn_init_r3, 0, 0)
        layoutRobots.addWidget(self.btn_init_r4, 0, 1)

        # Status Label
        self.label_robot_status = QLabel("Status: Keine Roboter initialisiert")
        layoutRobots.addWidget(self.label_robot_status, 1, 0, 1, 2)

        groupRobots.setLayout(layoutRobots)
        layout.addWidget(groupRobots)
        
        # ------------------------------------------
        # Controller Initialisierung
        # ------------------------------------------
        groupController = QGroupBox("Controller – Initialisierung")
        layoutController = QGridLayout()

        self.btn_init_controller = QPushButton("Controller verbinden")
        self.btn_init_controller.clicked.connect(self.initializeController)

        self.label_controller_status = QLabel("Status: Kein Controller verbunden")

        layoutController.addWidget(self.btn_init_controller, 0, 0)
        layoutController.addWidget(self.label_controller_status, 1, 0)

        groupController.setLayout(layoutController)
        layout.addWidget(groupController)


        self.start.setLayout(layout)

    # ------------------------------------------------------------
    # Robot Initialization
    # ------------------------------------------------------------
    def initializeRobot(self, robotNumber):

        if robotNumber == 3:
            ip = "192.168.0.3"
            homePos = self.homePosRobot3
        else:
            ip = "192.168.0.17"
            homePos = self.homePosRobot4

        try:
            gripperTemplate = RobotiqGripperReal(ip)
            robotControl = rtde_control.RTDEControlInterface(ip)
            robotReceive = rtde_receive.RTDEReceiveInterface(ip)

            robotiqGripper = Gripper(
                f"robot{robotNumber}",
                gripperTemplate,
                self.settingsManager
            )

            robot = UR3eRobot(robotControl, robotReceive, robotiqGripper,
                              self.settingsManager, homePos)

        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Roboter {robotNumber} konnte nicht initialisiert werden:\n{e}")
            return

        # Save Robot Instance
        if robotNumber == 3:
            self.robot3 = robot
        else:
            self.robot4 = robot

        self.moveRobot = robot
        self.gripper = robotiqGripper

        self.label_robot_status.setText(f"Status: Roboter {robotNumber} erfolgreich initialisiert")
        print(f"Roboter {robotNumber} initialisiert.")
        
    def initializeController(self):
            try:
                self.controller = Controller()
                self.label_controller_status.setText("Status: Controller erfolgreich verbunden")
                print("Controller erfolgreich verbunden.")
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Controller konnte nicht verbunden werden:\n{e}")



    # ------------------------------------------------------------
    # Teach Mode Tab
    # ------------------------------------------------------------
    def teachModeTab(self):
        mainLayout = QVBoxLayout()

        # Teach Mode
        groupTeach = QGroupBox("Teach Mode Steuerung")
        layoutTeach = QVBoxLayout()

        label_teach = QLabel("Teach Mode:")
        label_teach.setStyleSheet("font-weight: bold; padding-top: 10px;")
        layoutTeach.addWidget(label_teach)

        self.btn_teachOn = QPushButton("Teach Mode ON")
        self.btn_teachOn.clicked.connect(self.teachOnSlot)
        self.btn_teachOn.setStyleSheet("background-color: green; font-weight: bold; padding: 6px;")
        layoutTeach.addWidget(self.btn_teachOn)

        self.btn_teachOff = QPushButton("Teach Mode OFF")
        self.btn_teachOff.setEnabled(False)
        self.btn_teachOff.clicked.connect(self.teachOffSlot)
        layoutTeach.addWidget(self.btn_teachOff)

        # Axis
        label_axis = QLabel("Achsen Steuerung:")
        label_axis.setStyleSheet("font-weight: bold; padding-top: 10px;")
        layoutTeach.addWidget(label_axis)

        self.btn_axisFree = QPushButton("Achsen lösen")
        self.btn_axisFree.clicked.connect(self.axisFree)
        self.btn_axisFree.setStyleSheet("background-color: green; font-weight: bold; padding: 6px;")
        layoutTeach.addWidget(self.btn_axisFree)

        self.btn_axisClose = QPushButton("Achsen schließen")
        self.btn_axisClose.setEnabled(False)
        self.btn_axisClose.clicked.connect(self.axisClose)
        layoutTeach.addWidget(self.btn_axisClose)

        self.btn_initialPose = QPushButton("Initialposition anfahren")
        self.btn_initialPose.clicked.connect(self.gotoInitial)
        layoutTeach.addWidget(self.btn_initialPose)

        groupTeach.setLayout(layoutTeach)
        mainLayout.addWidget(groupTeach)

        # Positionen
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
        mainLayout.addWidget(groupPositions)

        # Greifer
        groupGripper = QGroupBox("Greifer Steuerung")
        gripLayout = QHBoxLayout()

        self.btn_gripperOpen = QPushButton("Greifer öffnen")
        self.btn_gripperOpen.clicked.connect(lambda: self.gripper.open() if self.gripper else None)
        gripLayout.addWidget(self.btn_gripperOpen)

        self.btn_gripperClose = QPushButton("Greifer schließen")
        self.btn_gripperClose.clicked.connect(lambda: self.gripper.close() if self.gripper else None)
        gripLayout.addWidget(self.btn_gripperClose)

        groupGripper.setLayout(gripLayout)
        mainLayout.addWidget(groupGripper)

        self.teachMode.setLayout(mainLayout)

    # ------------------------------------------------------------
    # Einstellungen Tab
    # ------------------------------------------------------------
    def settingsTab(self):
        pass


    # ------------------------------------------------------------
    # Teach Mode Funktionen (unverändert außer self-Fixes)
    # ------------------------------------------------------------
    def savePosition(self):
        if not self.moveRobot:
            print("Kein Roboter initialisiert!")
            return

        name = self.lineEdit_Save.text().strip()
        if not name:
            print("Positionsname fehlt.")
            return

        pose = self.moveRobot.getActualTCPPose()
        self.teachPositionManager.addPosition(name, pose)
        print(f"Position '{name}' gespeichert.")

    def gotoInitial(self):
        if not self.moveRobot:
            return
        self.moveRobot.moveL([-0.33643942345, -0.33467429034, 0.10161903614,
                              -0.05630442655, -3.12760190627, -0.0315903004])
        print(self.moveRobot.getActualTCPPose())

    def goToPositionSlot(self):
        if not self.moveRobot:
            return

        name = self.lineEdit_GoTo.text().strip()
        pose = self.teachPositionManager.getSavedPosition(name)
        if not pose:
            print("Position nicht gefunden.")
            return

        self.moveRobot.moveL(pose)

    def updatePositionList(self):
        self.listWidget_Positions.clear()
        positions = self.teachPositionManager.listPositions()
        self.listWidget_Positions.addItems(positions)

    def teachOnSlot(self):
        if not self.moveRobot:
            print("Kein Roboter initialisiert!")
            return

        self.teachModeRunning = True
        self.controllerTimer.start(10)
        self.btn_teachOn.setEnabled(False)
        self.btn_teachOff.setEnabled(True)

    def teachOffSlot(self):
        self.teachModeRunning = False
        self.controllerTimer.stop()

        if self.moveRobot:
            self.moveRobot.disconnect()
            self.moveRobot.reconnect()

        self.btn_teachOn.setEnabled(True)
        self.btn_teachOff.setEnabled(False)

    def axisFree(self):
        self.teachPositionManager.enableTeachMode()
        self.btn_axisFree.setEnabled(False)
        self.btn_axisClose.setEnabled(True)

    def axisClose(self):
        self.teachPositionManager.disableTeachMode()
        self.btn_axisFree.setEnabled(True)
        self.btn_axisClose.setEnabled(False)
        if self.moveRobot:
            print(self.moveRobot.getActualTCPPose())

    def pollController(self):

        if not self.moveRobot:
            return

        if self.teachModeRunning:
            axes = self.controller.get_axes()

            dx = axes.get("x", 0.0) * 0.1
            dy = axes.get("y", 0.0) * 0.1
            dz = axes.get("ry", 0.0) * 0.1
            d_rx = 0.0
            d_ry = 0.0
            d_rz = axes.get("rx", 0.0) * 0.1

            velocity = [dx, dy, dz, d_rx, d_ry, d_rz]
            self.moveRobot.speedL(velocity)

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
