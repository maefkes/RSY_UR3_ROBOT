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
from sensor.Controller import Controller
from camera.DetectAndSortCube_fixed import CubeColorDetectorLive


class TestGui(QTabWidget):
    def __init__(self, homePosRobot3, homePosRobot4, parent=None):
        super().__init__(parent)

        # Home-Pos für Roboter
        self.homePosRobot3 = homePosRobot3
        self.homePosRobot4 = homePosRobot4

        # Manager
        self.settingsManager = SettingsManager()
        self.teachPositionManager = TeachPositionManager(self.homePosRobot3, self.homePosRobot4)

        # Timer für Controller-Polling
        self.controllerTimer = QtCore.QTimer()
        self.controllerTimer.timeout.connect(self.pollController)
        self.teachModeRunning = False
        self.activeRobot = None  # aktuell steuerbarer Roboter

        # Kamera / Detector
        self.cubeColorDetetctor = CubeColorDetectorLive("best.pt")
        self.selected_image_path = None

        # Tabs
        self.start = QWidget()
        self.teachMode = QWidget()
        self.settingsMode = QWidget()

        self.addTab(self.start, "Start")
        self.addTab(self.teachMode, "Teach-Modus")
        self.addTab(self.settingsMode, "Einstellungen")

        # initialisiere GUI-Contents
        self.startTab()
        self.teachModeTab()
        self.settingsTab()

        self.setWindowTitle('UR3e - Magic Cube')
        self.setMinimumSize(QSize(320, 720))

        # Roboter & Controller (erst nach Init vorhanden)
        self.robot3 = None
        self.robot4 = None
        self.controller = None

    # -------------------- Start Tab ------------------------------------------------------------------------------------------------------------
    def startTab(self):
        layout = QVBoxLayout()

        # -----------------------------------------
        # Roboter Initialisierung
        # -----------------------------------------
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

        # -----------------------------------------
        # Controller Initialisierung
        # -----------------------------------------
        groupController = QGroupBox("Controller – Initialisierung")
        layoutController = QGridLayout()

        self.btn_init_controller = QPushButton("Controller verbinden")
        self.btn_init_controller.clicked.connect(self.initializeController)

        self.label_controller_status = QLabel("Status: Kein Controller verbunden")

        layoutController.addWidget(self.btn_init_controller, 0, 0)
        layoutController.addWidget(self.label_controller_status, 1, 0)

        groupController.setLayout(layoutController)
        layout.addWidget(groupController)

        # -----------------------------------------
        # TCP Positionen – Roboter 3 & 4
        # -----------------------------------------
        groupTCP = QGroupBox("TCP – Position abrufen")
        layoutTCP = QGridLayout()

        # TCP R3
        self.btn_get_tcp_r3 = QPushButton("TCP Roboter 3 anzeigen")
        self.btn_get_tcp_r3.clicked.connect(self.show_tcp_r3)
        self.label_tcp_r3 = QLabel("TCP R3: Noch nicht abgefragt")

        # TCP R4
        self.btn_get_tcp_r4 = QPushButton("TCP Roboter 4 anzeigen")
        self.btn_get_tcp_r4.clicked.connect(self.show_tcp_r4)
        self.label_tcp_r4 = QLabel("TCP R4: Noch nicht abgefragt")

        layoutTCP.addWidget(self.btn_get_tcp_r3, 0, 0)
        layoutTCP.addWidget(self.btn_get_tcp_r4, 0, 1)
        layoutTCP.addWidget(self.label_tcp_r3, 1, 0)
        layoutTCP.addWidget(self.label_tcp_r4, 1, 1)

        groupTCP.setLayout(layoutTCP)
        layout.addWidget(groupTCP)

        # -----------------------------------------
        # Kamera – Bildauswahl, Auswertung & Automatikmodus
        # -----------------------------------------
        groupCamera = QGroupBox("Kamera – Steuerung")
        layoutCamera = QGridLayout()

        # Bild auswählen
        self.btn_select_image = QPushButton("Bild auswählen")
        self.btn_select_image.clicked.connect(self.selectImage)

        # Bild auswerten
        self.btn_eval_image = QPushButton("Bild auswerten")
        self.btn_eval_image.clicked.connect(self.evaluateImage)

        # Automatikmodus (toggle)
        self.btn_auto_mode = QPushButton("Automatikmodus aus")
        self.btn_auto_mode.setCheckable(True)
        self.btn_auto_mode.clicked.connect(self.toggleAutoMode)

        # Statusanzeige
        self.label_camera_status = QLabel("Status: Kein Bild geladen")

        layoutCamera.addWidget(self.btn_select_image, 0, 0)
        layoutCamera.addWidget(self.btn_eval_image, 0, 1)
        layoutCamera.addWidget(self.btn_auto_mode, 1, 0, 1, 2)
        layoutCamera.addWidget(self.label_camera_status, 2, 0, 1, 2)

        groupCamera.setLayout(layoutCamera)
        layout.addWidget(groupCamera)

        # Layout anwenden
        self.start.setLayout(layout)

    def show_tcp_r3(self):
        if self.robot3:
            try:
                self.label_tcp_r3.setText(f"TCP R3: {self.robot3.getActualTCPPose()}")
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Fehler beim Lesen TCP R3:\n{e}")
        else:
            self.label_tcp_r3.setText("TCP R3: Roboter 3 nicht initialisiert")

    def show_tcp_r4(self):
        if self.robot4:
            try:
                self.label_tcp_r4.setText(f"TCP R4: {self.robot4.getActualTCPPose()}")
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Fehler beim Lesen TCP R4:\n{e}")
        else:
            self.label_tcp_r4.setText("TCP R4: Roboter 4 nicht initialisiert")

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

    def initializeController(self):
        try:
            self.controller = Controller()
            self.label_controller_status.setText("Status: Controller verbunden")
            print("Controller erfolgreich verbunden.")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Controller konnte nicht verbunden werden:\n{e}")

    def selectImage(self):
        path, _ = QFileDialog.getOpenFileName(
            None, "Bild auswählen", "", "Bilder (*.png *.jpg *.jpeg *.bmp)"
        )
        if path:
            self.selected_image_path = path
            self.label_camera_status.setText(f"Bild geladen: {path}")
        else:
            self.label_camera_status.setText("Kein Bild ausgewählt")

    def evaluateImage(self):
        if not self.selected_image_path:
            QMessageBox.warning(self, "Warnung", "Kein Bild ausgewählt.")
            return
        try:
            self.cubeColorDetetctor.detect_from_image(self.selected_image_path)
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler bei Bildauswertung:\n{e}")

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

        # Achsensteuerung (Free/Close)
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
            print("Roboter 3 aktiv")
        elif robotNumber == 4 and self.robot4:
            self.activeRobot = self.robot4
            print("Roboter 4 aktiv")
        else:
            QMessageBox.warning(self, "Warnung", f"Roboter {robotNumber} nicht initialisiert!")

    # -------------------- Teach Mode Funktionen --------------------
    def teachOnSlot(self):
        if not self.activeRobot or not self.controller:
            QMessageBox.warning(self, "Warnung", "Kein Roboter oder Controller aktiv!")
            return
        self.teachModeRunning = True
        # Polling-Intervall: 20 ms (50 Hz) — anpassbar
        self.controllerTimer.start(20)
        self.btn_teachOn.setEnabled(False)
        self.btn_teachOff.setEnabled(True)

    def teachOffSlot(self):
        self.teachModeRunning = False
        self.controllerTimer.stop()
        # Versuche Verbindung kurz neu aufzubauen (sicherstellen, dass Roboter nicht im Teach bleibt)
        try:
            if self.activeRobot:
                self.activeRobot.disconnect()
                time.sleep(0.1)
                self.activeRobot.reconnect()
        except Exception:
            pass
        self.btn_teachOn.setEnabled(True)
        self.btn_teachOff.setEnabled(False)

    def axisFree(self):
        if self.activeRobot:
            try:
                self.teachPositionManager.enableTeachMode()
                self.btn_axisFree.setEnabled(False)
                self.btn_axisClose.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Achsen konnten nicht gelöst werden:\n{e}")

    def axisClose(self):
        if self.activeRobot:
            try:
                self.teachPositionManager.disableTeachMode()
                self.btn_axisFree.setEnabled(True)
                self.btn_axisClose.setEnabled(False)
                print(self.activeRobot.getActualTCPPose())
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Achsen konnten nicht geschlossen werden:\n{e}")

    # -------------------- Controller Polling (JOINT BASED) --------------------
    def pollController(self):
        """
        Liest Achsen & Buttons vom Controller und berechnet inkrementelle Joint-Winkel.
        R1 -> Greifer öffnen, R2 -> Greifer schließen.
        """

        if not self.activeRobot or not self.teachModeRunning or not self.controller:
            return

        try:
            axes = self.controller.get_axes() or {}
        except Exception as e:
            print(f"Controller Achsen-Lese-Fehler: {e}")
            return

        try:
            buttons = self.controller.get_buttons() or {}
        except Exception:
            buttons = {}

        # helper: Deadzone
        def deadzone(val, dz=0.12):
            return 0.0 if abs(val) < dz else val

        # unterstützte Achskeys: "x","y","z","rx","ry","rz" oder joystick-layout "lx,ly,rx,ry"
        ax_x = deadzone(axes.get("x", axes.get("lx", 0.0)))
        ax_y = deadzone(axes.get("y", axes.get("ly", 0.0)))
        ax_z = deadzone(axes.get("ry", axes.get("z", 0.0)))   # benutze 'ry' bevorzugt
        ax_rz = deadzone(axes.get("rx", axes.get("rz", 0.0)))

        # Schrittweiten in Radiant pro Poll
        step_base = 0.01     # Basis/Schulter/Elbow grobe Skalierung
        step_wrist = 0.02    # kleinere Schritte für Handgelenk

        # Lese aktuelle Gelenkwinkel (getActualQ) erwartet Liste [q1..q6] in rad
        try:
            joints = list(self.activeRobot.getActualQ())  # kopieren
            if len(joints) < 6:
                # Guard: falls andere Form zurückkommt
                raise ValueError("getActualQ liefert keine 6 Gelenkwerte")
        except Exception as e:
            print(f"Fehler beim Lesen der Gelenkwinkel: {e}")
            return

        # Mapping Controller -> Joint-Inkremente (anpassbar)
        # Hier: Stick X -> J1 (Base), Stick Y -> J2 (Shoulder), Stick Z/ry -> J3 (Elbow),
        # RX -> J4 (Wrist1). J5/J6 unverändert.
        joints[0] += ax_x * step_base
        joints[1] += ax_y * step_base
        joints[2] += ax_z * step_base
        joints[3] += ax_rz * step_wrist

        # Grenzen (sichere Clamping - typisch ±pi)
        for i in range(6):
            if joints[i] is None:
                joints[i] = 0.0
            if joints[i] > 3.14159:
                joints[i] = 3.14159
            if joints[i] < -3.14159:
                joints[i] = -3.14159

        # Führe Bewegung aus (moveJ)
        try:
            self.activeRobot.moveJ(joints)
        except Exception as e:
            print(f"Fehler bei moveJ: {e}")

        # ---------------- Greifer via Buttons ----------------
        # Flexible Erkennung: Buttons kann dict mit Namen oder Indices sein.
        def btn_pressed(name_or_idx):
            # name_or_idx kann "R1" oder 5 etc. buttons kann beides enthalten
            if isinstance(buttons, dict):
                # direkte Keys
                if name_or_idx in buttons:
                    return bool(buttons.get(name_or_idx))
                # alternative Keys
                alt_map = {
                    "R1": ["R1", "rb", "RB", "button5", 5],
                    "R2": ["R2", "rt", "RT", "button6", 6]
                }
                for k in alt_map.get(name_or_idx, []):
                    if k in buttons:
                        return bool(buttons.get(k))
                # numeric-like keys
                try:
                    if isinstance(name_or_idx, int):
                        return bool(buttons.get(name_or_idx, False))
                except Exception:
                    pass
                return False
            else:
                # falls buttons z.B. Liste ist
                try:
                    if isinstance(name_or_idx, int):
                        return bool(buttons[name_or_idx])
                except Exception:
                    return False

        if btn_pressed("R1"):
            try:
                self.activeRobot.openGripper()
            except Exception as e:
                print(f"Fehler Greifer öffnen: {e}")

        if btn_pressed("R2"):
            try:
                self.activeRobot.closeGripper()
            except Exception as e:
                print(f"Fehler Greifer schließen: {e}")

    # -------------------- Greifer --------------------
    def openGripper(self):
        if self.activeRobot:
            try:
                self.activeRobot.openGripper()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Greifer konnte nicht geöffnet werden:\n{e}")
        else:
            QMessageBox.warning(self, "Warnung", "Kein aktiver Roboter.")

    def closeGripper(self):
        if self.activeRobot:
            try:
                self.activeRobot.closeGripper()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Greifer konnte nicht geschlossen werden:\n{e}")
        else:
            QMessageBox.warning(self, "Warnung", "Kein aktiver Roboter.")

    # -------------------- Positionen --------------------
    def savePosition(self):
        if not self.activeRobot:
            QMessageBox.warning(self, "Warnung", "Kein Roboter aktiv!")
            return
        name = self.lineEdit_Save.text().strip()
        if not name:
            QMessageBox.warning(self, "Warnung", "Positionsname fehlt.")
            return
        try:
            pose = self.activeRobot.getActualTCPPose()
            key = f"R{self.activeRobot.name[-1]}_{name}"
            self.teachPositionManager.addPosition(key, pose)
            print(f"Position '{name}' gespeichert für {self.activeRobot.name}")
            self.updatePositionList()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Position konnte nicht gespeichert werden:\n{e}")

    def gotoInitial(self):
        if not self.activeRobot:
            QMessageBox.warning(self, "Warnung", "Kein Roboter aktiv!")
            return
        try:
            home = self.homePosRobot3 if self.activeRobot.name.endswith("3") else self.homePosRobot4
            self.activeRobot.moveL(home)
            print(self.activeRobot.getActualTCPPose())
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Initialposition konnte nicht angefahren werden:\n{e}")

    def goToPositionSlot(self):
        if not self.activeRobot:
            QMessageBox.warning(self, "Warnung", "Kein Roboter aktiv!")
            return
        name = self.lineEdit_GoTo.text().strip()
        key = f"R{self.activeRobot.name[-1]}_{name}"
        pose = self.teachPositionManager.getSavedPosition(key)
        if pose:
            try:
                self.activeRobot.moveL(pose)
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Position konnte nicht angefahren werden:\n{e}")
        else:
            QMessageBox.warning(self, "Warnung", "Position nicht gefunden.")

    def updatePositionList(self):
        self.listWidget_Positions.clear()
        try:
            self.listWidget_Positions.addItems(self.teachPositionManager.listPositions())
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Positionen konnten nicht geladen werden:\n{e}")

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
