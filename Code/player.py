from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.Qt import Qt

player_speed = 15

class Player(QGraphicsPixmapItem):


    def __init__(self, parent = None):
        """self.name = name
        self.score = 0
        self.savedScore = []"""
        QGraphicsPixmapItem.__init__(self, parent)
        self.setPixmap(QPixmap("p1_stand.png"))
        self.setTransformOriginPoint(33, 45)
        self.sprites = []
        self.sprites.append(QPixmap("Player_sprite/p1_walk01.png"))
        self.sprites.append(QPixmap("Player_sprite/p1_walk02.png"))
        self.sprites.append(QPixmap("Player_sprite/p1_walk03.png"))
        self.sprites.append(QPixmap("Player_sprite/p1_walk04.png"))
        self.sprites.append(QPixmap("Player_sprite/p1_walk05.png"))
        self.sprites.append(QPixmap("Player_sprite/p1_walk06.png"))
        self.sprites.append(QPixmap("Player_sprite/p1_walk07.png"))
        self.sprites.append(QPixmap("Player_sprite/p1_walk08.png"))
        self.sprites.append(QPixmap("Player_sprite/p1_walk09.png"))
        self.sprites.append(QPixmap("Player_sprite/p1_walk10.png"))
        self.sprites.append(QPixmap("Player_sprite/p1_walk11.png"))
        self.jump = QPixmap("Player_sprite/p1_jump.png")
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        #self.jump = 0
        self.jump_speed = 5
        self.mass = 1

    def sprite(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        return self.image


    def keyPressEvent(self, event):
        dx = 0
        dy = 0
        if event.key() == Qt.Key_A:
            #self.setRotation(270)
            dx -= player_speed
            pic = self.sprite()
            self.setPixmap(pic)
        if event.key() == Qt.Key_D:
            dx += player_speed
            pic = self.sprite()
            self.setPixmap(pic)
        if event.key() == Qt.Key_W:
            self.setPixmap(self.jump)
            y = self.y()
            force = self.mass * (self.jump_speed**2)
            y -= force
            self.setPos(self.x(), y)
            self.jump_speed = self.jump_speed - 1
            if self.jump_speed < 0:
                self.mass = -1
            if self.jump_speed == -6:
                self.jump_speed = 5
                self.mass = 1

            #self.jump = True
            #self.jump()
            #self.setPixmap(self.jump)
        #if event.key() == Qt.Key_S:
            #dy += player_speed
        #pic = self.sprite()
        #self.setPixmap(pic)
        self.setPos(self.x()+dx, self.y()+dy)

    """def jump(self):
        y = self.y()
        print(y)
        force = self.mass * (self.jump_speed**2)
        y -= force
        self.setPos(self.x(), self.y()+y)
        self.jump_speed = self.jump_speed - 1
        if self.jump_speed < 0:
            self.mass = -1
        if self.jump_speed == -6:
            self.jump = False
            self.jump_speed = 5
            self.mass = 1"""


    def keyReleaseEvent(self, event):
        self.setPixmap(QPixmap("p1_stand.png"))

