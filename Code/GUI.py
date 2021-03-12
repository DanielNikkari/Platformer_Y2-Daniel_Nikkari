import sys
from PyQt5 import (QtWidgets, QtCore, QtGui, Qt)
from PyQt5.Qt import Qt
from player import Player

class GUI(QtWidgets.QMainWindow):
    """Class that handles the graphical user interface"""
    def __init__(self):
        super().__init__()

        self.init_window()

    """def keyPressEvent(self, event):
        dx = 0
        dy = 0
        if event.key() == Qt.Key_A:
            dx -= 10
        if event.key() == Qt.Key_D:
            dx += 10
        if event.key() == Qt.Key_W:
            dy -= 10
        if event.key() == Qt.Key_S:
            dy += 10
        print("KEY PRESSED")
        print(self.x(), self.y())
        self.rect.setPos(self.rect.x()+dx, self.rect.y()+dy)"""

    def init_window(self):
        self.setGeometry(200, 200, 800, 800)
        self.setWindowTitle('Space Merc')
        self.show()

        self.scene =QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 800, 800)

        """self.rect = QtWidgets.QGraphicsRectItem(0, 0, 200, 200)
        self.scene.addItem(self.rect)
        self.rect.grabKeyboard()
        self.rect.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.rect.setFocus()"""

        self.player = Player()
        self.player.setPos((800-self.player.pixmap().width())/2, (800-self.player.pixmap().height())/2)
        self.scene.addItem(self.player)
        self.player.grabKeyboard()
        self.player.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.player.setFocus()


        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()




"""if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    scene = GUI()
    sys.exit(app.exec_())"""
