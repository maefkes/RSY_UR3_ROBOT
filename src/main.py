import sys
import os
from PyQt6 import QtWidgets
from gui.Testgui import TestGui
from gui.MainGui import MainGui 


SIMULATION = os.environ.get('SIMULATION', 'False') == 'True'

# Homepositionen
homePosRobot3 = [0, -1.5708, 0, -1.5708, 0, 0]
homePosRobot4 = [0, -1.5708, 0, -1.5708, 0, 0]

def mainTest():
    app = QtWidgets.QApplication(sys.argv)
    mainWin = TestGui(homePosRobot3, homePosRobot4)
    mainWin.show()
    sys.exit(app.exec())
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainGui(homePosRobot3, homePosRobot4)
    mainWin.show()
    sys.exit(app.exec())
    
    
############################################################################################
#   STARTE PROGRAMM
############################################################################################
if __name__ == "__main__":
    main()
