from PyQt5 import (QtWidgets, QtCore, QtGui, Qt)
from PyQt5.Qt import Qt
from player import Player
from world_textures import WorldTextures
import math


FRAME_TIME_MS = 16

class GUI(QtWidgets.QMainWindow):
    """Class that handles the graphical user interface"""
    def __init__(self):
        super().__init__()

        # Set timer
        self.timer = QtCore.QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        # Initiate the game window
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

    def timerEvent(self, event):
        self.update()

    """def collision(self):
        collision = False
        player_pos = (self.player.x(), self.player.y())
        ground_pos = (self.ground.x(), self.ground.y(), self.ground.x()+800, self.ground.y())
        print(player_pos, ground_pos)
        if player_pos[1] >= ground_pos[1]:
            collision = True
            return collision"""

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


        background_size = 256
        bg_tiles = math.ceil(800/background_size)
        for x in range(bg_tiles):
            for y in range(bg_tiles):
                background = WorldTextures("backgroundTex")
                background.setPos((0+x*background_size), (0+y*background_size))
                self.scene.addItem(background)

        # Add player item to the scene.
        self.player = Player()
        self.player.setPos((800-self.player.pixmap().width())/2, 568)
        self.scene.addItem(self.player)
        self.player.grabKeyboard()
        self.player.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.player.setFocus()


        width_ground = 70
        i = 12
        for x in range(i):
            grassMid = WorldTextures("grassMidTex")
            grassMid.setPos((0+x*width_ground), 660)
            self.scene.addItem(grassMid)
            grassCenter = WorldTextures("grassCenterTex")
            grassCenter.setPos((0+x*width_ground), 730)
            self.scene.addItem(grassCenter)

        #self.ground = QtWidgets.QGraphicsRectItem(0, 0, 800, 200)
        #self.ground.setPos(0, 600)
        #self.ground.setBrush(QtGui.QColor(20, 20, 20))
        #self.scene.addItem(self.ground)

        # Draw the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()



