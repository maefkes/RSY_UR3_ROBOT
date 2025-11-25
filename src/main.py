import sys
import os
from PyQt6 import QtWidgets
from testgui import TestGui


SIMULATION = os.environ.get('SIMULATION', 'False') == 'True'

# Homepositionen
homePosRobot3 = [-0.3348824484632403, -0.13811531146380698, 0.2610392430112353, 1.0415257012533956, 2.9503966505304193, 0.024981329326417064]
homePosRobot4 = [-0.3348824484632403, -0.13811531146380698, 0.2610392430112353, -1.0415257012533956, -2.9503966505304193, 0.024981329326417064]

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWin = TestGui(homePosRobot3, homePosRobot4)
    mainWin.show()
    sys.exit(app.exec())
    
############################################################################################
#   STARTE PROGRAMM
############################################################################################
if __name__ == "__main__":
    main()
