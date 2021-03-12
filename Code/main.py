import sys
from GUI import GUI
from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
