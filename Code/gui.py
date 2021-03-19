from PyQt5 import (QtWidgets, QtCore, QtGui, Qt, QtMultimedia)
from PyQt5.Qt import Qt
from world_textures import WorldTextures
from npc import NPC
from clouds import Clouds
import math
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap


FRAME_TIME_MS = 16
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCENE_WIDTH = 5000
BOX_DIM = 70
GROUND_LEVEL = 660

class GUI(QtWidgets.QMainWindow):
    """Class that handles the graphical user interface"""
    def __init__(self):
        #super().__init__()
        QtWidgets.QMainWindow.__init__(self)

        # Delete all widgets on close
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Hold the set of keys pressed
        self.keys_pressed = set()

        # Set timer
        self.timer = QtCore.QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        # Initiate player and NPCs
        self.player = Player()
        self.ghost = NPC("ghost")
        self.ghost2 = NPC("ghost")
        self.ghost_menu = WorldTextures("ghost_menu")
        self.bee1 = NPC("bee")
        self.bee2 = NPC("bee")
        self.frog1 = NPC("frog")

        # Initiate clouds
        self.cloud1, self.cloud2, self.cloud3, self.cloud4 = Clouds("cloud1"), Clouds("cloud2"), Clouds("cloud1"), Clouds("cloud2")
        self.cloud5 = Clouds("cloud2")

        # Init world textures
        self.background1 = WorldTextures("backgroundTex")
        self.title_text = QtWidgets.QGraphicsTextItem("PLATFORMER Y2\n       653088")
        self.tut_text = QtWidgets.QGraphicsTextItem("A: lEFT   D: RIGHT\nW: JUMP S: DUCK")
        self.wasd = WorldTextures("wasd")
        self.start_button = QtWidgets.QPushButton()
        self.quit_button = QtWidgets.QPushButton()
        self.play_button = WorldTextures("start_button")
        self.quit_button_tex = WorldTextures("quit_button")


        # Initiate the game window, player and NPCs
        #self.init_player_and_NPCs()
        self.init_window()
        self.init_scene()

        # Initiate media player and click sound effect location
        self.media_player = QtMultimedia.QMediaPlayer()
        self.click_sound_url = QtCore.QUrl.fromLocalFile("Audio/SoundEffects/click_sound_effect.mp3")

        # Variables
        self.menuFlag = True
        self.death = False
        self.collision_x = None
        self.collision_y = None

    def init_window(self):
        # Initiate a window
        #self.setStyleSheet("background-color: blue")
        self.setGeometry(200, 200, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setWindowTitle('Platformer Y2, 653088')
        self.show()

    def init_player_and_NPCs(self):
        # Initiate player and NPCs
        self.player = Player()
        #self.ghost = NPC_ghost()
        #self.ghost2 = NPC_ghost()
        self.ghost = NPC("ghost")
        self.ghost2 = NPC("ghost")
        self.ghost_menu = WorldTextures("ghost_menu")
        self.bee1 = NPC("bee")
        self.bee2 = NPC("bee")
        self.frog1 = NPC("frog")

    """def init_world_items(self):
        self.background1 = WorldTextures("backgroundTex")
        self.title_text = QtWidgets.QGraphicsTextItem("PLATFORMER Y2\n       653088")
        self.tut_text = QtWidgets.QGraphicsTextItem("A: lEFT   D: RIGHT\nW: JUMP S: DUCK")
        self.wasd = WorldTextures("wasd")
        self.start_button = QtWidgets.QPushButton()
        self.play_button = WorldTextures("start_button")
        self.quit_button = QtWidgets.QPushButton()
        self.quit_button_tex = WorldTextures("quit_button")"""


    def init_scene(self):

        # Initiate a scene to where graphic objects are added
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, SCENE_WIDTH, 800)

        # Call the function for drawing the map and adding the player
        #self.draw_map()
        self.display_main_menu()

        # Draw the scene by QGraphicsView
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.view.adjustSize()
        self.view.show()
        self.view.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.view.setSceneRect(0, 0, SCENE_WIDTH, SCREEN_HEIGHT)
        self.view.centerOn(self.player.x(), self.player.y())
        #self.view.centerOn(self.play_button.x(), self.play_button.y())

    def display_main_menu(self):
        # Draw a background for the menu
        background_size = 256
        #bg_tiles = math.ceil(SCENE_WIDTH/background_size)
        bg_tiles_x = math.ceil(SCREEN_WIDTH/background_size)
        bg_tiles_y = math.ceil(SCREEN_HEIGHT/background_size)
        for x in range(bg_tiles_x):
            for y in range(bg_tiles_y):
                self.background1 = WorldTextures("backgroundTex")
                self.background1.setPos((0+x*background_size), (0+y*background_size))
                self.scene.addItem(self.background1)

        # Add menu clouds
        self.cloud1, self.cloud2, self.cloud3, self.cloud4 = Clouds("cloud1"), Clouds("cloud2"), Clouds("cloud1"), Clouds("cloud2")
        self.cloud1.setPos(10, 650), self.cloud2.setPos(600, 250), self.cloud3.setPos(150, 400), self.cloud4.setPos(500, 150)
        self.scene.addItem(self.cloud1), self.scene.addItem(self.cloud2), self.scene.addItem(self.cloud3), self.scene.addItem(self.cloud4)


        # Add a ghost NPC on the menu
        self.ghost_menu = WorldTextures("ghost_menu")
        scaled_ghost_pixmap = self.ghost_menu.pixmap().scaled(350, 100, QtCore.Qt.KeepAspectRatio)
        self.ghost_menu.setPixmap(scaled_ghost_pixmap)
        self.ghost_menu.setPos(500, 680)
        self.scene.addItem(self.ghost_menu)

        # Add title text for the menu
        self.title_text = QtWidgets.QGraphicsTextItem("PLATFORMER Y2\n       653088")
        self.title_text.setFont(QtGui.QFont("comic sans MS", 50))
        self.title_text.setDefaultTextColor(QtGui.QColor(255, 0, 0))
        self.title_text.setPos((SCREEN_WIDTH/2)-(self.title_text.boundingRect().width()/2), 90)
        self.scene.addItem(self.title_text)

        # Add instruction text on the menu
        self.tut_text = QtWidgets.QGraphicsTextItem("A: lEFT   D: RIGHT\nW: JUMP S: DUCK")
        self.tut_text.setFont(QtGui.QFont("comic sans", 20))
        self.tut_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        self.tut_text.setPos(35, 570)
        self.scene.addItem(self.tut_text)

        # Add PNG of keyboard keys W, A, S and D
        self.wasd = WorldTextures("wasd")
        scaled_wasd_pixmap = self.wasd.pixmap().scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.wasd.setPixmap(scaled_wasd_pixmap)
        self.wasd.setPos(75, 400)
        self.scene.addItem(self.wasd)

        # Add a push button that will be used to start up the map
        self.start_button = QtWidgets.QPushButton()
        self.start_button.setGeometry(QtCore.QRect(0, 0, 280, 80))
        self.start_button.move(SCREEN_WIDTH/2-140, SCREEN_HEIGHT/2-40)
        self.scene.addWidget(self.start_button)
        self.start_button.clicked.connect(self.clickMethod)

        # Add a push button to quit the game from the menu
        self.quit_button = QtWidgets.QPushButton()
        self.quit_button.setGeometry(QtCore.QRect(0, 0, 280, 80))
        self.quit_button.move((SCREEN_WIDTH/2)-130, 510)
        self.scene.addWidget(self.quit_button)
        self.quit_button.clicked.connect(self.clickMethodQuit)

        # Add texture for the start push button (just adds PNG over the push button)
        self.play_button = WorldTextures("start_button")
        scaled_play_button_pixmap = self.play_button.pixmap().scaled(300, 100, QtCore.Qt.KeepAspectRatio)
        self.play_button.setPixmap(scaled_play_button_pixmap)
        self.play_button.setPos((SCREEN_WIDTH/2)-150, 350)
        self.scene.addItem(self.play_button)

        # Add texture for the quit push button (just adds PNG over the push button)
        self.quit_button_tex = WorldTextures("quit_button")
        scaled_quit_button_pixmap = self.quit_button_tex.pixmap().scaled(350, 100, QtCore.Qt.KeepAspectRatio)
        self.quit_button_tex.setPixmap(scaled_quit_button_pixmap)
        self.quit_button_tex.setPos((SCREEN_WIDTH/2)-150, 500)
        self.scene.addItem(self.quit_button_tex)

    def draw_map(self):
        # Draw a background
        background_size = 256
        #bg_tiles = math.ceil(SCENE_WIDTH/background_size)
        bg_tiles_x = math.ceil(SCENE_WIDTH/background_size)
        bg_tiles_y = math.ceil(SCREEN_HEIGHT/background_size)
        for x in range(bg_tiles_x):
            for y in range(bg_tiles_y):
                self.background1 = WorldTextures("backgroundTex")
                self.background1.setPos((0+x*background_size), (0+y*background_size))
                self.scene.addItem(self.background1)

        # Add clouds
        self.cloud1, self.cloud2, self.cloud3, self.cloud4, self.cloud5 = Clouds("cloud1"), Clouds("cloud2"), Clouds("cloud1"), Clouds("cloud2"), Clouds("cloud2")
        self.cloud1.setPos(500, 150), self.cloud2.setPos(200, 250), self.cloud3.setPos(1500, 200), self.cloud4.setPos(2500, 300), self.cloud5.setPos(3500, 100)
        self.scene.addItem(self.cloud1), self.scene.addItem(self.cloud2), self.scene.addItem(self.cloud3), self.scene.addItem(self.cloud4), self.scene.addItem(self.cloud5)

        # Add ground textures to the scene
        grassTiles = math.ceil(SCENE_WIDTH/BOX_DIM)
        #grassMidPix = WorldTextures("grassMidTex")
        for x in range(grassTiles):
            self.grassMid = WorldTextures("grassMidTex")
            self.grassMid.setPos((0+x*BOX_DIM), 660)
            self.scene.addItem(self.grassMid)
            self.grassCenter = WorldTextures("grassCenterTex")
            self.grassCenter.setPos((0+x*BOX_DIM), 730)
            self.scene.addItem(self.grassCenter)

        # Add obstacles
        self.box1 = WorldTextures("box")
        self.box1.setPos(500, 660-BOX_DIM)
        self.scene.addItem(self.box1)
        self.box2 = WorldTextures("box")
        self.box2.setPos(500, 660-2*BOX_DIM)
        self.scene.addItem(self.box2)


        # Add NPC ghost 1
        self.ghost.setPos(1000, 590)
        self.scene.addItem(self.ghost)
        self.ghost.start_pos()

        # Add NPC ghost 2
        self.ghost2.setPos(1500, 590)
        self.scene.addItem(self.ghost2)
        self.ghost2.start_pos()

        # Add NPC bee 1
        self.bee1.setPos(1700, 510)
        self.scene.addItem(self.bee1)
        self.bee1.start_pos()

        # Add NPC bee 2
        self.bee2.setPos(2500, 540)
        self.scene.addItem(self.bee2)
        self.bee2.start_pos()

        # Add NPC frog
        self.frog1.setPos(2000, 621)
        self.scene.addItem(self.frog1)
        self.frog1.start_pos()

        # Add player item to the scene.
        self.player.setPos((800-self.player.pixmap().width())/2, 568)
        self.scene.addItem(self.player)
        self.player.grabKeyboard()
        self.player.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.player.setFocus()

    def keyPressEvent(self, event):
        # Log the pressed key to keys_pressed
        self.keys_pressed.add(event.key())


    def keyReleaseEvent(self, event):
        # Remove a logged key from the keys_pressed after releasing the key
        self.keys_pressed.remove(event.key())
        #self.player.setPixmap(QPixmap("PlayerTextures/p1_stand.png"))

    def timerEvent(self, event):
        # Update the given functions
        self.game_update()
        self.update()
        # Make the view follow the players position
        self.view.centerOn(self.player.x(), self.player.y())

    def game_update(self):
        # Update the class Player game_update function
        self.player.game_update(self.keys_pressed, self.collision_x, self.collision_y)
        self.checkColliding()
        # Update some NPC functions
        self.ghost_menu_movement()
        self.ghost.game_update_ghost()
        self.ghost2.game_update_ghost()
        self.bee1.game_update_bee()
        self.bee2.game_update_bee()
        self.frog1.game_update_frog()
        # Update cloud movement
        #self.move_clouds()
        self.cloud1.move_clouds(SCENE_WIDTH), self.cloud2.move_clouds(SCENE_WIDTH)
        self.cloud3.move_clouds(SCENE_WIDTH), self.cloud4.move_clouds(SCENE_WIDTH)

    def checkColliding(self):
        if QtWidgets.QGraphicsItem.collidingItems(self.player):
            if self.ghost in QtWidgets.QGraphicsItem.collidingItems(self.player):
                print("COLLISION WITH ghost 1")
                self.player.player_death()
                self.death = True
                self.pause_game()

            if self.ghost2 in QtWidgets.QGraphicsItem.collidingItems(self.player):
                print("COLLISION WITH ghost 2")
                self.player.player_death()
                self.death = True
                self.pause_game()

            if self.bee1 in QtWidgets.QGraphicsItem.collidingItems(self.player):
                print("COLLISION WITH bee 1")
                self.player.player_death()
                self.death = True
                self.pause_game()

            if self.frog1 in QtWidgets.QGraphicsItem.collidingItems(self.player):
                print("COLLISION WITH frog 1")
                if self.player.y() < self.frog1.y()-52:
                    print(self.player.y(), self.frog1.y())
                    self.frog1.frog_deadFunc()
                else:
                    self.player.player_death()
                    self.death = True
                    self.pause_game()

            if self.bee2 in QtWidgets.QGraphicsItem.collidingItems(self.player):
                self.player.player_death()
                self.death = True
                self.pause_game()

            if self.box1 in QtWidgets.QGraphicsItem.collidingItems(self.player):
                print("COLLISION WITH box1")
                #self.collision = True
                distance = self.getDistance(self.player.x()+self.player.boundingRect().width()/2,
                                            self.player.y()+self.player.boundingRect().height()/2,
                                            self.box1.x()+self.box1.boundingRect().width()/2,
                                            self.box1.y()+self.box1.boundingRect().height()/2)
                print(distance[2])
                if distance[2] < 142:
                    if distance[0] > 0:
                        self.collision_x = "R"
                    if distance[0] < 0:
                        self.collision_x = "L"
                if distance[2] < 167:
                    if distance[1] > 0:
                        self.collision_y = "U"
                    if distance[1] < 0:
                        self.collision_y = "D"

            if self.box2 in QtWidgets.QGraphicsItem.collidingItems(self.player):
                print("COLLISION WITH box2")
                #self.collision = True

            if self.box1 not in QtWidgets.QGraphicsItem.collidingItems(self.player):
                self.collision_x = None
                self.collision_y = None
            if self.box2 not in QtWidgets.QGraphicsItem.collidingItems(self.player):
                self.collision_x = None
                self.collision_y = None


        if self.death:
            # Add game over text
            self.title_text = QtWidgets.QGraphicsTextItem("GAME OVER")
            self.title_text.setFont(QtGui.QFont("comic sans MS", 50))
            self.title_text.setDefaultTextColor(QtGui.QColor(255, 0, 0))
            self.title_text.setPos(self.player.x()-250, self.player.y()-300)
            self.scene.addItem(self.title_text)

            # Add a push button that will be used to restart the map
            self.restart = QtWidgets.QPushButton()
            self.restart.setGeometry(QtCore.QRect(0, 0, 280, 80))
            self.restart.setText("RESTART")
            self.restart.move(self.player.x()-140, self.player.y()-100)
            self.scene.addWidget(self.restart)
            self.restart.clicked.connect(self.clickMethodRestart)

            # Add a push button that will be used to go back to main menu
            self.backMenu = QtWidgets.QPushButton()
            self.backMenu.setGeometry(QtCore.QRect(0, 0, 280, 80))
            self.backMenu.setText("BACK TO MENU")
            self.backMenu.move(self.player.x()-140, self.player.y()+50)
            self.scene.addWidget(self.backMenu)
            self.backMenu.clicked.connect(self.clickMethodBackMenu)

    def getDistance(self, x1, y1, x2, y2):
        xDistance = x2 - x1
        yDistance = y2 - y1
        return xDistance, yDistance, math.sqrt(math.pow(xDistance, 2) + math.pow(yDistance, 2))

    def pause_game(self):
        if self.timer.isActive():
            self.timer.stop()

    def clickMethodRestart(self):
        # PLay click sound effect
        self.media_player.setMedia(QtMultimedia.QMediaContent(self.click_sound_url))
        self.media_player.setVolume(30)
        self.media_player.play()
        self.death = False
        #self.scene.clear()
        self.init_player_and_NPCs()
        self.draw_map()
        self.timer.start(FRAME_TIME_MS, self)

    def clickMethodBackMenu(self):
        # PLay click sound effect
        self.media_player.setMedia(QtMultimedia.QMediaContent(self.click_sound_url))
        self.media_player.setVolume(30)
        self.media_player.play()
        self.death = False
        #self.scene.clear()
        self.init_player_and_NPCs()
        self.display_main_menu()
        self.timer.start(FRAME_TIME_MS, self)

    def clickMethod(self):
        # PLay click sound effect
        self.media_player.setMedia(QtMultimedia.QMediaContent(self.click_sound_url))
        self.media_player.setVolume(30)
        self.media_player.play()
        # Draw the map
        self.draw_map()

    def clickMethodQuit(self):
        # Exit the game
        QtWidgets.QApplication.quit()


    def ghost_menu_movement(self):
        # Algo for the menu ghost to move
        dx = 0
        if self.menuFlag:
            dx -= 4
            self.ghost_menu.setPos(self.ghost_menu.x() + dx, self.ghost_menu.y())
            if self.ghost_menu.x() < 100:
                self.menuFlag = False

        if not self.menuFlag:
            dx += 4
            self.ghost_menu.setPos(self.ghost_menu.x() + dx, self.ghost_menu.y())
            if self.ghost_menu.x() > 900:
                self.menuFlag = True

player_speed = 6

class Player(QGraphicsPixmapItem):

    # Player class that initiates the player graphics, processes key press information, produces walking animation,
    # makes the player jump and duck

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
        self.hurt = QPixmap("PlayerTextures/p1_hurt.png")
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        # Initiate needed variables and timer for the jumping and ducking and in case of death
        self.jumpFlag = False
        self.duckFlag = False
        self.jump_speed = 7
        self.mass = 1
        self.duck_time = 15
        self.timer()
        self.hurtFlag = False

        # Initiate media player
        self.media_player = QtMultimedia.QMediaPlayer()
        self.jumpHeight = 428


    def timer(self):
        self.timer_player = QtCore.QTimer()
        self.timer_player.start(60)
        self.timer_player.timeout.connect(self.show_time)


    def sprite(self):
        # Produce the running animation using sprite animation.
        # Slow down the animation by adding only 0.5
        self.current_sprite += 0.5
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        return self.image

    def game_update(self, keys_pressed, collision_x, collision_y):
        # Read the keys pressed and make the player object react to them.
        self.c_y = collision_y
        dx = 0
        dy = 0
        if Qt.Key_A in keys_pressed:
            # Prevent player walking off the scene by checking the x position of the player is greater than 0
            if self.x() > 0 and collision_x != "L":
                dx -= player_speed
            pic = self.sprite()
            self.setPixmap(pic)

        if Qt.Key_D in keys_pressed:
            # Prevent player walking off the screen by checking x position of the player is smaller than scene width
            if (self.x()+66) < SCENE_WIDTH and collision_x != "R":  # 66pix is the width of the player png img
                dx += player_speed
            pic = self.sprite()
            self.setPixmap(pic)

        if Qt.Key_W in keys_pressed:
            # Set the flag for the jump to True.
            self.jumpFlag = True
            jump_sound_url = QtCore.QUrl.fromLocalFile("Audio/SoundEffects/jump_sound_effect_cut.mp3")
            self.media_player.setMedia(QtMultimedia.QMediaContent(jump_sound_url))
            self.media_player.setVolume(50)
            self.media_player.play()
            # Call for the jumping function.
            self.show_time()

        if Qt.Key_S in keys_pressed:
            self.duckFlag = True
            self.show_time()

        # Update the position of the player in x and y axis.
        self.setPos(self.x()+dx, self.y()+dy)
        """if self.c_y != "U" and self.y() < 428:
            self.setPos(self.x(), 568)"""


    def player_death(self):
        self.setPixmap(self.hurt)
        self.hurtFlag = True
        self.setPos(self.x(), self.y()+20)
        # Play death sound effect
        death_sound_url = QtCore.QUrl.fromLocalFile("Audio/SoundEffects/death_sound_effect.mp3")
        self.media_player.setMedia(QtMultimedia.QMediaContent(death_sound_url))
        self.media_player.setVolume(35)
        self.media_player.play()

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
            print(self.y())

            """if self.c_y == "U":
                # making jump equal to false
                self.jumpFlag = False

                # setting original values to
                # speed  and mass
                self.jump_speed = 7
                self.mass = 1
                # Switch back to stand pixmap image
                self.setPixmap(QPixmap("PlayerTextures/p1_stand.png"))"""

            # object reached its maximum height
            if self.jump_speed < 0:
                # negative sign is added to
                # counter negative velocity
                self.mass = -1

            # objected reaches its original state
            if self.jump_speed == -8:
                # making jump equal to false
                self.jumpFlag = False

                # setting original values to
                # speed  and mass
                self.jump_speed = 7
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

"""class NPC_ghost(QGraphicsPixmapItem):

    # NPC ghost class that initiates ghost graphics and processes movement algorithm.

    def __init__(self, parent = None):

        # Initiate the Pixmap graphics item
        QGraphicsPixmapItem.__init__(self, parent)
        # Set a png file to the graphics item.
        self.setPixmap(QPixmap("Textures/NPC_Textures/ghost.png"))
        self.setTransformOriginPoint(33, 45)
        self.pointFlag = True
        self.start_x = 0

    def start_pos(self):
        # Get the ghosts start x pos to anchor the ghosts movement around it.
        self.start_x = self.x()

    def game_update(self):
        # Make ghost move back and forth
        dx = 0
        if self.pointFlag:
            dx -= 3
            self.setPos(self.x() + dx, self.y())
            if self.x() < (self.start_x - 150):
                self.pointFlag = False

        if not self.pointFlag:
            dx += 5
            self.setPos(self.x() + dx, self.y())
            if self.x() > (self.start_x + 150):
                self.pointFlag = True"""



