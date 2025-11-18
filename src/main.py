import sys
import os
from PyQt6 import QtWidgets
from gui import MainWindow


SIMULATION = os.environ.get('SIMULATION', 'False') == 'True'

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
    
############################################################################################
#   STARTE PROGRAMM
############################################################################################
if __name__ == "__main__":
    main()
