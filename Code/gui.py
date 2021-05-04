from PyQt5 import (QtWidgets, QtCore, QtGui, Qt, QtMultimedia)
from PyQt5.Qt import Qt
from player import Player
from world_textures import WorldTextures
from npc import NPC
from clouds import Clouds
from fireball import FireBall
from building_textures import BuildingTextures
from scores import Scores
import math

FRAME_TIME_MS = 16
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCENE_WIDTH = 5000
BOX_DIM = 70
GROUND_LEVEL = 660


class GUI(QtWidgets.QMainWindow):
    """Class that handles the graphical user interface"""
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        # Delete all widgets on close
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Initiate score file
        self.scores = Scores()
        self.save_file_name = self.scores.create_save_file()

        # Hold the set of keys pressed
        self.keys_pressed = set()

        # Set score board
        self.score_board = [[None, None, None], [None, None, None], [None, None, None], [None, None, None], [None, None, None]]

        # Set timers
        self.timer = QtCore.QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)
        self.curr_time_ms = 0
        self.curr_time_s = 0
        self.curr_time_m = 0
        self.game_timer = QtCore.QTimer()
        self.game_timer.timeout.connect(self.time)
        self.time_text = QtWidgets.QGraphicsTextItem("Time: 00:00:00")
        self.time_text.setFont(QtGui.QFont("comic sans MS", 30))
        self.time_text.setDefaultTextColor(QtGui.QColor(255, 0, 0))

        # Initiate player and NPCs and fire ball and key
        self.player = Player()
        self.player_name = QtWidgets.QGraphicsTextItem("")
        self.key = WorldTextures("key")
        self.keyFlag = False
        self.fire_ball_count = 2
        self.fire_ball_flag = False
        self.fireball_hud1 = FireBall()
        self.fireball_hud2 = FireBall()
        self.fire_ball = FireBall()
        self.key_hud = WorldTextures("key")
        self.ghost = NPC("ghost")
        self.ghost2 = NPC("ghost")
        self.ghost_menu = WorldTextures("ghost_menu")
        self.bee1 = NPC("bee")
        self.bee2 = NPC("bee")
        self.frog1 = NPC("frog")
        self.snakeSlime = NPC("snakeSlime")

        # Initiate clouds
        self.cloud1, self.cloud2, self.cloud3, self.cloud4 = Clouds("cloud1"), Clouds("cloud2"), Clouds("cloud1"), Clouds("cloud2")
        self.cloud5 = Clouds("cloud2")

        # Init world textures
        self.background1 = WorldTextures("backgroundTex")
        self.title_text = QtWidgets.QGraphicsTextItem("PLATFORMER Y2\n       653088")
        self.tut_text = QtWidgets.QGraphicsTextItem("A: lEFT   D: RIGHT\nW: JUMP S: DUCK\nE: FIREBALL F: USE")
        self.wasd = WorldTextures("wasd")
        self.start_button = QtWidgets.QPushButton()
        self.quit_button = QtWidgets.QPushButton()
        self.play_button = WorldTextures("start_button")
        self.quit_button_tex = WorldTextures("quit_button")

        # Initiate the game window and scene
        self.init_window()
        self.init_scene()

        # Initiate media player and click sound effect location
        self.media_player = QtMultimedia.QMediaPlayer()
        self.click_sound_url = QtCore.QUrl.fromLocalFile("Audio/SoundEffects/click_sound_effect.mp3")
        self.fireball_sound_url = QtCore.QUrl.fromLocalFile("Audio/SoundEffects/fireBall_soundeffect.mp3")
        self.victory_sound_url = QtCore.QUrl.fromLocalFile("Audio/SoundEffects/victory_sound_effect.mp3")

        # Variables
        self.victoryFlag = False
        self.menuFlag = True
        self.death = False
        self.collision_x = None
        self.collision_y = None

        # Collision with box object
        #self.collision_list_box = [self.box1, self.box2]

    def init_window(self):
        # Initiate a window
        self.setGeometry(200, 200, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setWindowTitle('Platformer Y2, 653088')
        self.show()

    def init_player_and_NPCs(self):
        # Initiate player and NPCs
        self.player = Player()
        self.ghost = NPC("ghost")
        self.ghost2 = NPC("ghost")
        self.ghost_menu = WorldTextures("ghost_menu")
        self.bee1 = NPC("bee")
        self.bee2 = NPC("bee")
        self.frog1 = NPC("frog")
        self.snakeSlime = NPC("snakeSlime")

    def init_scene(self):
        # Initiate a scene to where graphic objects are added
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, SCENE_WIDTH, 800)

        #self.display_main_menu()
        self.display_name_menu()

        # Draw the scene by QGraphicsView
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.show()
        self.view.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.view.setSceneRect(0, 0, SCENE_WIDTH, SCREEN_HEIGHT)
        self.view.centerOn(self.player.x(), self.player.y())

    def display_name_menu(self):
        # Display menu where player can name their character
        background_size = 256
        bg_tiles_x = math.ceil(SCREEN_WIDTH/background_size)
        bg_tiles_y = math.ceil(SCREEN_HEIGHT/background_size)
        for x in range(bg_tiles_x):
            for y in range(bg_tiles_y):
                self.background1 = WorldTextures("backgroundTex")
                self.background1.setPos((0+x*background_size), (0+y*background_size))
                self.scene.addItem(self.background1)

        # Add text for the name menu
        self.nameLabel = QtWidgets.QGraphicsTextItem("Write your name in the other window\n                    and close it.")
        self.nameLabel.setFont(QtGui.QFont("comic sans MS", 30))
        self.nameLabel.setDefaultTextColor(QtGui.QColor(255, 0, 0))
        self.nameLabel.setPos((SCREEN_WIDTH/2)-(self.nameLabel.boundingRect().width()/2), 200)
        self.scene.addItem(self.nameLabel)

        # Add line edit to write the name of the player
        self.line = QtWidgets.QLineEdit()
        self.line.move(SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2)
        self.line.resize(200, 32)
        self.line.show()

        # Add ok button to go to the main menu
        self.pybutton = QtWidgets.QPushButton('OK')
        self.pybutton.clicked.connect(self.clickMethodToMenu)
        self.pybutton.resize(200, 32)
        self.pybutton.move(SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2+50)
        self.pybutton.resize(200,32)
        self.scene.addWidget(self.pybutton)

    def display_main_menu(self):
        # Draw a background for the menu
        background_size = 256
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
        self.tut_text = QtWidgets.QGraphicsTextItem("A: lEFT   D: RIGHT\nW: JUMP S: DUCK\nE: FIREBALL F: USE")
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

        # Add score board
        self.score_text = QtWidgets.QGraphicsTextItem("TOP SCORE:\n{}\n{}m {}s {}ms\n".format(self.line.text(), self.score_board[0][0],
                                                                                    self.score_board[0][1], self.score_board[0][2]))
        self.score_text.setPos(SCREEN_WIDTH-self.score_text.boundingRect().width()-180, 350)
        self.score_text.setFont(QtGui.QFont("comic sans", 20))
        self.score_text.setDefaultTextColor(QtGui.QColor(255, 0, 0))
        if None not in self.score_board[0]:
            self.scene.addItem(self.score_text)


    def draw_map(self):
        # Draw a background
        background_size = 256
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
        for x in range(grassTiles):
            self.grassMid = WorldTextures("grassMidTex")
            self.grassMid.setPos((0+x*BOX_DIM), 660)
            self.scene.addItem(self.grassMid)
            self.grassCenter = WorldTextures("grassCenterTex")
            self.grassCenter.setPos((0+x*BOX_DIM), 730)
            self.scene.addItem(self.grassCenter)

        # Draw the end building
        self.houseGrayBottomLeft, self.houseGrayBottomMid, self.houseGrayBottomRight = BuildingTextures("houseGrayBottomLeft"), BuildingTextures("houseGrayBottomMid"), BuildingTextures("houseGrayBottomRight")
        self.houseGrayBottomLeft.setPos(SCENE_WIDTH-5*BOX_DIM, GROUND_LEVEL-BOX_DIM), self.houseGrayBottomRight.setPos(SCENE_WIDTH-BOX_DIM, GROUND_LEVEL-BOX_DIM)
        self.scene.addItem(self.houseGrayBottomRight), self.scene.addItem(self.houseGrayBottomLeft)
        for x in range(3):
            self.houseGrayBottomMid = BuildingTextures("houseGrayBottomMid")
            self.houseGrayBottomMid.setPos(SCENE_WIDTH-(x+2)*BOX_DIM, GROUND_LEVEL-BOX_DIM)
            self.scene.addItem(self.houseGrayBottomMid)
        self.houseGray = BuildingTextures("houseGray")
        self.houseGrayMidLeft, self.houseGrayMidRight, self.houseGrayAlt, self.houseGrayAlt2 =\
            BuildingTextures("houseGrayMidLeft"), BuildingTextures("houseGrayMidRight"), BuildingTextures("houseGrayAlt"), BuildingTextures("houseGrayAlt2")
        for y in range(4):
            for x in range(3):
                self.houseGrayMidLeft = BuildingTextures("houseGrayMidLeft")
                self.houseGrayMidRight = BuildingTextures("houseGrayMidRight")
                self.houseGray = BuildingTextures("houseGray")
                self.houseGrayAlt = BuildingTextures("houseGrayAlt")
                self.houseGrayMidLeft.setPos(SCENE_WIDTH-5*BOX_DIM, GROUND_LEVEL-(y+2)*BOX_DIM)
                self.houseGrayMidRight.setPos(SCENE_WIDTH-BOX_DIM, GROUND_LEVEL-(y+2)*BOX_DIM)
                self.scene.addItem(self.houseGrayMidRight), self.scene.addItem(self.houseGrayMidLeft)
                self.houseGray.setPos(SCENE_WIDTH-(x+2)*BOX_DIM, GROUND_LEVEL-(y+2)*BOX_DIM)
                self.scene.addItem(self.houseGray)
                if y % 2 == 0:
                    self.houseGrayAlt.setPos(4860, GROUND_LEVEL-(y+2)*BOX_DIM)
                else:
                    self.houseGrayAlt.setPos(4720, GROUND_LEVEL-(y+2)*BOX_DIM)
                self.scene.addItem(self.houseGrayAlt)
        self.houseGrayTopLeft, self.houseGrayTopRight, self.houseGrayTopMid =\
            BuildingTextures("houseGrayTopLeft"), BuildingTextures("houseGrayTopRight"), BuildingTextures("houseGrayTopMid")
        self.houseGrayTopLeft.setPos(SCENE_WIDTH-5*BOX_DIM, GROUND_LEVEL-BOX_DIM*6), self.houseGrayTopRight.setPos(SCENE_WIDTH-BOX_DIM, GROUND_LEVEL-BOX_DIM*6)
        self.scene.addItem(self.houseGrayTopRight), self.scene.addItem(self.houseGrayTopLeft)
        for x in range(3):
            self.houseGrayTopMid = BuildingTextures("houseGrayTopMid")
            self.houseGrayTopMid.setPos(SCENE_WIDTH-(x+2)*BOX_DIM, GROUND_LEVEL-BOX_DIM*6)
            self.scene.addItem(self.houseGrayTopMid)
        self.roofRedLeft, self.roofRedRight, self.roofRedMid =\
            BuildingTextures("roofRedLeft"), BuildingTextures("roofRedRight"), BuildingTextures("roofRedMid")
        self.roofRedRight.setPos(SCENE_WIDTH-6*BOX_DIM, GROUND_LEVEL-BOX_DIM*7), self.roofRedLeft.setPos(SCENE_WIDTH, GROUND_LEVEL-BOX_DIM*7)
        self.scene.addItem(self.roofRedRight), self.scene.addItem(self.roofRedLeft)
        for x in range(5):
            self.roofRedMid = BuildingTextures("roofRedMid")
            self.roofRedMid.setPos(SCENE_WIDTH-(x+1)*BOX_DIM, GROUND_LEVEL-BOX_DIM*7)
            self.scene.addItem(self.roofRedMid)
        for y in range(3):
            self.windowHighCheckeredBottom, self.windowHighCheckeredMid, self.windowHighCheckeredTop =\
            BuildingTextures("windowHighCheckeredBottom"), BuildingTextures("windowHighCheckeredMid"), BuildingTextures("windowHighCheckeredTop")
            if y == 0:
                self.windowHighCheckeredBottom.setPos(SCENE_WIDTH-4*BOX_DIM, GROUND_LEVEL-BOX_DIM*(y+2))
                self.scene.addItem(self.windowHighCheckeredBottom)
            if y == 1:
                self.windowHighCheckeredMid.setPos(SCENE_WIDTH-4*BOX_DIM, GROUND_LEVEL-BOX_DIM*(y+2))
                self.scene.addItem(self.windowHighCheckeredMid)
            if y == 2:
                self.windowLowCheckered = BuildingTextures("windowLowCheckered")
                self.windowLowCheckered.setPos(SCENE_WIDTH-3*BOX_DIM, GROUND_LEVEL-BOX_DIM*(y+4))
                self.scene.addItem(self.windowLowCheckered)
                self.windowHighCheckeredTop.setPos(SCENE_WIDTH-4*BOX_DIM, GROUND_LEVEL-BOX_DIM*(y+2))
                self.scene.addItem(self.windowHighCheckeredTop)
            self.windowHighCheckeredBottom, self.windowHighCheckeredMid, self.windowHighCheckeredTop =\
            BuildingTextures("windowHighCheckeredBottom"), BuildingTextures("windowHighCheckeredMid"), BuildingTextures("windowHighCheckeredTop")
            if y == 0:
                self.windowHighCheckeredBottom.setPos(SCENE_WIDTH-2*BOX_DIM, GROUND_LEVEL-BOX_DIM*(y+2))
                self.scene.addItem(self.windowHighCheckeredBottom)
                self.signHangingBed = BuildingTextures("signHangingBed")
                self.signHangingBed.setPos(SCENE_WIDTH-6*BOX_DIM, GROUND_LEVEL-BOX_DIM*(y+3))
                self.scene.addItem(self.signHangingBed)
            if y == 1:
                self.windowHighCheckeredMid.setPos(SCENE_WIDTH-2*BOX_DIM, GROUND_LEVEL-BOX_DIM*(y+2))
                self.scene.addItem(self.windowHighCheckeredMid)
            if y == 2:
                self.windowHighCheckeredTop.setPos(SCENE_WIDTH-2*BOX_DIM, GROUND_LEVEL-BOX_DIM*(y+2))
                self.scene.addItem(self.windowHighCheckeredTop)
                self.anemometer = BuildingTextures("anemometer")
                self.anemometer.setPos(SCENE_WIDTH-3*BOX_DIM, GROUND_LEVEL-BOX_DIM*8)
                self.scene.addItem(self.anemometer)
        self.doorLock, self.doorPlateTop = BuildingTextures("doorLock"), BuildingTextures("doorPlateTop")
        self.doorLock.setPos(SCENE_WIDTH-3*BOX_DIM, GROUND_LEVEL-BOX_DIM), self.doorPlateTop.setPos(SCENE_WIDTH-3*BOX_DIM, GROUND_LEVEL-BOX_DIM*2)
        self.scene.addItem(self.doorLock), self.scene.addItem(self.doorPlateTop)

        """# Add obstacles
        self.box1 = WorldTextures("box")
        self.box1.setPos(500, 660-BOX_DIM)
        self.scene.addItem(self.box1)
        self.box2 = WorldTextures("box")
        self.box2.setPos(500, 660-2*BOX_DIM)
        self.scene.addItem(self.box2)"""

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

        # Add NPC snakeSlime
        self.snakeSlime.setPos(3000, GROUND_LEVEL-self.snakeSlime.boundingRect().height())
        self.scene.addItem(self.snakeSlime)

        # Add player item to the scene.
        self.player.setPos((800-self.player.pixmap().width())/2, 568)
        self.scene.addItem(self.player)
        self.player.grabKeyboard()
        self.player.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.player.setFocus()

        # start the timer and add the timer to the scene
        self.gameTimer()
        self.time_text.setPos(self.player.x()+100, 30)
        self.scene.addItem(self.time_text)

        # Show how many fire balls are left
        self.fireball_hud1, self.fireball_hud2 = FireBall(), FireBall()
        scaled_fireball_pixmap = self.fireball_hud1.pixmap().scaled(150, 150, QtCore.Qt.KeepAspectRatio)
        self.fireball_hud1.setPixmap(scaled_fireball_pixmap)
        self.fireball_hud2.setPixmap(scaled_fireball_pixmap)
        self.fireball_hud1.setPos(10, 20), self.fireball_hud2.setPos(65, 20)
        self.scene.addItem(self.fireball_hud1), self.scene.addItem(self.fireball_hud2)

        # Add player name
        self.player_name = QtWidgets.QGraphicsTextItem(self.line.text())
        self.player_name.setFont(QtGui.QFont("comic sans MS", 20))
        self.player_name.setDefaultTextColor(QtGui.QColor(255, 0, 0))
        self.player_name.setPos(self.player.x()-(self.player_name.boundingRect().width()/2+30), self.player.y()-50)
        self.scene.addItem(self.player_name)


    def keyPressEvent(self, event):
        # Log the pressed key to keys_pressed
        self.keys_pressed.add(event.key())


    def keyReleaseEvent(self, event):
        # Remove a logged key from the keys_pressed after releasing the key
        self.keys_pressed.remove(event.key())

    def timerEvent(self, event):
        # Update the given functions
        self.game_update()
        self.update()
        # Make the view follow the players position
        self.view.centerOn(self.player.x(), self.player.y())
        # Make timer and fire ball and key hud elements follow players position
        if self.time_text.x()+self.time_text.boundingRect().width() < SCENE_WIDTH-100:
            self.time_text.setPos(self.player.x()+100, 30)
        else:
            self.time_text.setPos(5000-100-self.time_text.boundingRect().width(), 30)
        self.fireball_hud1.setPos(self.player.x()-450, 5), self.fireball_hud2.setPos(self.player.x()-390, 5)
        self.key_hud.setPos(self.player.x()-350, 5)
        # Make player name follow players position
        self.player_name.setPos(self.player.x()-(self.player_name.boundingRect().width()/2)+40, self.player.y()-65)

    def game_update(self):
        # Update the class Player game_update function
        self.player.game_update(self.keys_pressed, self.collision_x, self.collision_y, self.line.text())
        # If E key is pressed create fireball
        if Qt.Key_E in self.keys_pressed:
            # Check that player has fire balls left
            if self.fire_ball_count > 0:
                self.media_player.setMedia(QtMultimedia.QMediaContent(self.fireball_sound_url))
                self.media_player.setVolume(70)
                self.media_player.play()
                self.scene.removeItem(self.fire_ball)
                self.fire_ball = FireBall()
                self.fire_ball.setPos(self.player.x(), self.player.y()+30)
                self.fire_ball.fireball_startpos()
                self.scene.addItem(self.fire_ball)
                self.fire_ball_flag = True
                self.fire_ball_count -= 0.2
                if self.fire_ball_count > 0.3:
                    self.scene.removeItem(self.fireball_hud2)
                if self.fire_ball_count < 0.3:
                    self.scene.removeItem(self.fireball_hud1)
        self.checkColliding()
        # Update some NPC functions
        self.ghost_menu_movement()
        self.ghost.game_update_ghost()
        self.ghost2.game_update_ghost()
        self.bee1.game_update_bee()
        self.bee2.game_update_bee()
        self.frog1.game_update_frog()
        self.snakeSlime.game_update_snakeSlime()
        # Update cloud movement
        self.cloud1.move_clouds(SCENE_WIDTH), self.cloud2.move_clouds(SCENE_WIDTH)
        self.cloud3.move_clouds(SCENE_WIDTH), self.cloud4.move_clouds(SCENE_WIDTH)
        # Move the fireball
        if self.fire_ball_flag:
            self.fire_ball.fireBallFly()

    def checkColliding(self):
        if self.ghost in QtWidgets.QGraphicsItem.collidingItems(self.fire_ball):
            self.scene.removeItem(self.ghost)
        if self.ghost2 in QtWidgets.QGraphicsItem.collidingItems(self.fire_ball):
            self.scene.removeItem(self.ghost2)
        if self.bee1 in QtWidgets.QGraphicsItem.collidingItems(self.fire_ball):
            self.scene.removeItem(self.bee1)
        if self.bee2 in QtWidgets.QGraphicsItem.collidingItems(self.fire_ball):
            self.scene.removeItem(self.bee2)
        if self.snakeSlime in QtWidgets.QGraphicsItem.collidingItems(self.fire_ball):
            self.key.setPos(3000, GROUND_LEVEL-self.key.boundingRect().height())
            self.scene.addItem(self.key)
            self.scene.removeItem(self.snakeSlime)
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

            if self.snakeSlime in QtWidgets.QGraphicsItem.collidingItems(self.player):
                self.player.player_death()
                self.death = True
                self.pause_game()

            if self.key in QtWidgets.QGraphicsItem.collidingItems(self.player):
                if Qt.Key_F in self.keys_pressed:
                    self.scene.removeItem(self.key)
                    self.keyFlag = True
                    self.media_player.setMedia(QtMultimedia.QMediaContent(self.click_sound_url))
                    self.media_player.setVolume(30)
                    self.media_player.play()
                    self.key_hud = WorldTextures("key")
                    self.key_hud.setPos(self.player.x()-350, 5)
                    self.scene.addItem(self.key_hud)

            if self.doorLock in QtWidgets.QGraphicsItem.collidingItems(self.player) and self.keyFlag:
                if Qt.Key_F in self.keys_pressed:
                    self.doorOpen, self.doorOpenTop = BuildingTextures("doorOpen"), BuildingTextures("doorOpenTop")
                    self.doorOpen.setPos(SCENE_WIDTH-3*BOX_DIM, GROUND_LEVEL-BOX_DIM), self.doorOpenTop.setPos(SCENE_WIDTH-3*BOX_DIM, GROUND_LEVEL-BOX_DIM*2)
                    self.scene.addItem(self.doorOpen), self.scene.addItem(self.doorOpenTop)
                    playerPosX, playerPosY = self.player.x(), self.player.y()
                    self.scene.removeItem(self.player)
                    self.player = Player()
                    self.player.setPos(playerPosX, playerPosY)
                    self.scene.addItem(self.player)
                    if self.doorOpen in QtWidgets.QGraphicsItem.collidingItems(self.player) and self.keyFlag:
                        if Qt.Key_F in self.keys_pressed:
                            self.victoryFlag = True
                            self.pause_game()


            """if self.box1 in QtWidgets.QGraphicsItem.collidingItems(self.player):
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
                self.collision_y = None"""

        if self.victoryFlag:
            # Play victory sound effect
            self.media_player.setMedia(QtMultimedia.QMediaContent(self.victory_sound_url))
            self.media_player.setVolume(30)
            self.media_player.play()

            self.gameTimerStop()
            # Add complete text
            self.title_text = QtWidgets.QGraphicsTextItem("THANKS FOR PLAYING!")
            self.title_text.setFont(QtGui.QFont("comic sans MS", 50))
            self.title_text.setDefaultTextColor(QtGui.QColor(255, 0, 0))
            self.title_text.setPos(self.player.x()-750, self.player.y()-300)
            self.scene.addItem(self.title_text)

            # Add timer text
            self.scene.removeItem(self.time_text)
            self.time_text = QtWidgets.QGraphicsTextItem("Your time: {}:{}:{}".format(self.curr_time_m, self.curr_time_s, self.curr_time_ms))
            self.time_text.setFont(QtGui.QFont("comic sans MS", 30))
            self.time_text.setDefaultTextColor(QtGui.QColor(255, 0, 0))
            self.time_text.setPos(self.player.x(), self.player.y())
            self.scene.addItem(self.time_text)

            # Add a push button that will be used to restart the map
            self.restart = QtWidgets.QPushButton()
            self.restart.setGeometry(QtCore.QRect(0, 0, 280, 80))
            self.restart.setText("RESTART")
            self.restart.move(self.player.x()-400, self.player.y()-100)
            self.scene.addWidget(self.restart)
            self.restart.clicked.connect(self.clickMethodRestart)

            # Add a push button that will be used to go back to main menu
            self.backMenu = QtWidgets.QPushButton()
            self.backMenu.setGeometry(QtCore.QRect(0, 0, 280, 80))
            self.backMenu.setText("BACK TO MENU")
            self.backMenu.move(self.player.x()-400, self.player.y()+50)
            self.scene.addWidget(self.backMenu)
            self.backMenu.clicked.connect(self.clickMethodBackMenu)

            # Save score
            self.scores.save_to_file(self.line.text(), self.curr_time_m, self.curr_time_s, self.curr_time_ms)
            i = 0
            for score in self.score_board:
                if None in score:
                    self.score_board[i] = [self.curr_time_m, self.curr_time_s, self.curr_time_ms]
                    break
                else:
                    print("A")
                    print(i)
                    print(score[0], score[1], score[2])
                    print(self.curr_time_m)
                    if self.curr_time_m < score[0]:
                        self.score_board[i] = [self.curr_time_m, self.curr_time_s, self.curr_time_ms]
                        break
                    if self.curr_time_m == score[0]:
                        if self.curr_time_s < score[1]:
                            self.score_board[i] = [self.curr_time_m, self.curr_time_s, self.curr_time_ms]
                            break
                        elif self.curr_time_s == score[1]:
                            if self.curr_time_ms < score[2]:
                                self.score_board[i] = [self.curr_time_m, self.curr_time_s, self.curr_time_ms]
                                break
                i += 1
            print(self.score_board)

        if self.death:
            # Stop game timer
            self.gameTimerStop()

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
        self.curr_time_ms, self.curr_time_s, self.curr_time_m = 0, 0, 0
        self.media_player.setMedia(QtMultimedia.QMediaContent(self.click_sound_url))
        self.media_player.setVolume(30)
        self.media_player.play()
        self.death = False
        self.victoryFlag = False
        # Replenish fire balls
        self.fire_ball_count = 2
        self.init_player_and_NPCs()
        self.draw_map()
        self.timer.start(FRAME_TIME_MS, self)

    def clickMethodBackMenu(self):
        # PLay click sound effect
        self.curr_time_ms, self.curr_time_s, self.curr_time_m = 0, 0, 0
        self.media_player.setMedia(QtMultimedia.QMediaContent(self.click_sound_url))
        self.media_player.setVolume(30)
        self.media_player.play()
        self.death = False
        self.victoryFlag = False
        # Replenish fire balls
        self.fire_ball_count = 2
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
        self.scores.close_file()
        QtWidgets.QApplication.quit()

    def clickMethodToMenu(self):
        # Display main menu
        self.display_main_menu()


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

    def gameTimer(self):
        self.game_timer.start(100)

    def gameTimerStop(self):
        self.game_timer.stop()

    def time(self):
        # Add to the timer and draw the timer
        self.curr_time_ms += 10
        if self.curr_time_ms == 60:
            self.curr_time_s += 1
            self.curr_time_ms = 0
        if self.curr_time_s == 60:
            self.curr_time_m += 1
            self.curr_time_s = 0
        y_pos = self.time_text.y()
        x_pos = self.time_text.x()
        self.scene.removeItem(self.time_text)
        self.time_text = QtWidgets.QGraphicsTextItem("Time: {}:{}:{}".format(self.curr_time_m, self.curr_time_s, self.curr_time_ms))
        self.time_text.setFont(QtGui.QFont("comic sans MS", 30))
        self.time_text.setDefaultTextColor(QtGui.QColor(255, 0, 0))
        if x_pos+self.time_text.boundingRect().width() <= 5000:
            self.time_text.setPos(x_pos, y_pos)
        else:
            self.time_text.setPos(SCENE_WIDTH-self.time_text.boundingRect().width(), y_pos)
        self.scene.addItem(self.time_text)

    def closeEvent(self, event):
        # Create close event where the game asks if the player is sure that they want to quit by pressing the X
        reply = QtWidgets.QMessageBox.question(self, 'Game Close', 'Are you sure you want to quit the game?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.scores.close_file()
        else:
            event.ignore()
