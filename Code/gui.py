from PyQt5 import (QtWidgets, QtCore, QtGui, Qt)
from PyQt5.Qt import Qt
#from player import Player
from world_textures import WorldTextures
import math
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap


FRAME_TIME_MS = 16
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCENE_WIDTH = 3000

class GUI(QtWidgets.QMainWindow):
    """Class that handles the graphical user interface"""
    def __init__(self):
        super().__init__()

        # Hold the set of keys pressed
        self.keys_pressed = set()

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


    """def collision(self):
        collision = False
        player_pos = (self.player.x(), self.player.y())
        ground_pos = (self.ground.x(), self.ground.y(), self.ground.x()+800, self.ground.y())
        print(player_pos, ground_pos)
        if player_pos[1] >= ground_pos[1]:
            collision = True
            return collision"""

    def init_window(self):
        # Initiate a window
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle('Platformer Y2, 653088')
        self.show()

        # Initiate a scene to where graphic objects are added
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, SCENE_WIDTH, 800)


        """self.rect = QtWidgets.QGraphicsRectItem(0, 0, 200, 200)
        self.scene.addItem(self.rect)
        self.rect.grabKeyboard()
        self.rect.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.rect.setFocus()"""

        # Draw a background
        background_size = 256
        bg_tiles = math.ceil(SCENE_WIDTH/background_size)
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

        # Add ground textures to the scene
        width_ground = 70
        grassTiles = math.ceil(SCENE_WIDTH/width_ground)
        for x in range(grassTiles):
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
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.view.translate(1000, 1000)
        #self.view.adjustSize()
        self.view.show()
        self.view.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.view.setSceneRect(0, 0, SCENE_WIDTH, SCREEN_HEIGHT)
        #self.view.centerOn(self.scene.sceneRect().x(), self.scene.sceneRect().y())
        self.view.centerOn(self.player.x(), self.player.y())


    def keyPressEvent(self, event):
        # Log the pressed key to keys_pressed
        self.keys_pressed.add(event.key())


    def keyReleaseEvent(self, event):
        # Remove a logged key from the keys_pressed after releasing the key
        self.keys_pressed.remove(event.key())
        self.player.setPixmap(QPixmap("PlayerTextures/p1_stand.png"))

    def timerEvent(self, event):
        # Update the given functions
        self.game_update()
        self.update()
        self.view.centerOn(self.player.x(), self.player.y())

    def game_update(self):
        # Update the class Player game_update function
        self.player.game_update(self.keys_pressed)

player_speed = 6

class Player(QGraphicsPixmapItem):


    def __init__(self, parent = None):
        """self.name = name
        self.score = 0
        self.savedScore = []"""

        # Initiate the Pixmap graphics item
        QGraphicsPixmapItem.__init__(self, parent)
        # Set a png file to the graphics item.
        self.setPixmap(QPixmap("PlayerTextures/p1_stand.png"))
        self.setTransformOriginPoint(33, 45)

        # Make a list of images to produce running animation.
        self.sprites = []
        self.sprites.append(QPixmap("PlayerTextures/Player_sprite/p1_walk01.png"))
        self.sprites.append(QPixmap("PlayerTextures/Player_sprite/p1_walk02.png"))
        self.sprites.append(QPixmap("PlayerTextures/Player_sprite/p1_walk03.png"))
        self.sprites.append(QPixmap("PlayerTextures/Player_sprite/p1_walk04.png"))
        self.sprites.append(QPixmap("PlayerTextures/Player_sprite/p1_walk05.png"))
        self.sprites.append(QPixmap("PlayerTextures/Player_sprite/p1_walk06.png"))
        self.sprites.append(QPixmap("PlayerTextures/Player_sprite/p1_walk07.png"))
        self.sprites.append(QPixmap("PlayerTextures/Player_sprite/p1_walk08.png"))
        self.sprites.append(QPixmap("PlayerTextures/Player_sprite/p1_walk09.png"))
        self.sprites.append(QPixmap("PlayerTextures/Player_sprite/p1_walk10.png"))
        self.sprites.append(QPixmap("PlayerTextures/Player_sprite/p1_walk11.png"))
        self.jump = QPixmap("PlayerTextures/Player_sprite/p1_jump.png")
        self.duck = QPixmap("PlayerTextures/p1_duck.png")
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        # Initiate needed variables and timer for the jumping
        self.jumpFlag = False
        self.duckFlag = False
        self.jump_speed = 6
        self.mass = 1
        self.duck_time = 15
        self.timer()

    def timer(self):
        self.timer_player = QtCore.QTimer()
        self.timer_player.start(60)
        self.timer_player.timeout.connect(self.show_time)


    def sprite(self):
        # Produce the running animation.
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        return self.image

    def game_update(self, keys_pressed):
        # Read the keys pressed and make the player object react to them.
        dx = 0
        dy = 0
        if Qt.Key_A in keys_pressed:
            dx -= player_speed
            pic = self.sprite()
            self.setPixmap(pic)
            #GUI.scroll_view("Left")
        if Qt.Key_D in keys_pressed:
            dx += player_speed
            pic = self.sprite()
            self.setPixmap(pic)
            #GUI.scroll_view("Right")
        if Qt.Key_W in keys_pressed:
            # Set the flag for the jump to True.
            self.jumpFlag = True
            # Call for the jumping function.
            self.show_time()

        if Qt.Key_S in keys_pressed:
            self.duckFlag = True
            self.show_time()

        # Update the position of the player in x and y axis.
        self.setPos(self.x()+dx, self.y()+dy)

    def show_time(self):
        if self.jumpFlag:
            # Switch the current pixmap image to jumping.
            self.setPixmap(self.jump)
            y = self.y()

            # calculate force (F).
            # F = 1 / 2 * mass * velocity ^ 2.
            # here we are not using  ( 1/2 )
            Force = self.mass * (self.jump_speed ** 2)

            # change in the y co-ordinate
            y -= Force

            self.setPos(self.x(), y)

            # decreasing velocity while going up
            # and become negative while coming down
            self.jump_speed = self.jump_speed - 1

            # object reached its maximum height
            if self.jump_speed < 0:
                # negative sign is added to
                # counter negative velocity
                self.mass = -1

            # objected reaches its original state
            if self.jump_speed == -7:
                # making jump equal to false
                self.jumpFlag = False

                # setting original values to
                # speed  and mass
                self.jump_speed = 6
                self.mass = 1
                # Switch back to stand pixmap image
                self.setPixmap(QPixmap("PlayerTextures/p1_stand.png"))

        # Check if the duck Flag is True
        if self.duckFlag:
            # Use duck_time as a time indicator, and duck on the 15 and stand up on 0
            self.setPixmap(self.duck)
            if self.duck_time == 15:
                # set position so the player is in duck
                self.setPos(self.x(), self.y()+20)
            # Count down time
            self.duck_time -= 1
            if self.duck_time == 0:
                # Reset variables and position
                self.setPos(self.x(), self.y()-20)
                self.duckFlag = False
                self.duck_time = 15
                self.setPixmap(QPixmap("PlayerTextures/p1_stand.png"))



