import sys
from PyQt6 import QtWidgets
from ihm_domino import DominoIHMManager


def main():
    app = QtWidgets.QApplication(sys.argv)
    fenetre = DominoIHMManager()
    fenetre.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()