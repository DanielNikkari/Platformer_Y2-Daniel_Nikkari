from PyQt5 import (QtWidgets, QtCore, QtGui, Qt, QtMultimedia)
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap

player_speed = 6
SCENE_WIDTH = 5000

class Player(QGraphicsPixmapItem):

    # Player class that initiates the player graphics, processes key press information, produces walking animation,
    # makes the player jump and duck

    def __init__(self, parent = None):
        self.name = ""
        """self.score = 0
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

    def game_update(self, keys_pressed, collision_x, collision_y, name):
        # Read the keys pressed and make the player object react to them.
        self.c_y = collision_y
        self.name = name
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
