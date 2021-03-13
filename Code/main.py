import sys
from gui import GUI
from PyQt5 import QtWidgets

def main():
    # Main function from where the program is ran
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
