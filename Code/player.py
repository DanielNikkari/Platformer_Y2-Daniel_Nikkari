from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.Qt import Qt

player_speed = 10

class Player(QGraphicsPixmapItem):


    def __init__(self, parent = None):
        """self.name = name
        self.score = 0
        self.savedScore = []"""
        QGraphicsPixmapItem.__init__(self, parent)
        self.setPixmap(QPixmap("playerShip1_blue.png"))
        self.setTransformOriginPoint(50, 38)


    def keyPressEvent(self, event):
        dx = 0
        dy = 0
        if event.key() == Qt.Key_A:
            self.setRotation(270)
            dx -= player_speed
        if event.key() == Qt.Key_D:
            self.setRotation(90)
            dx += player_speed
        if event.key() == Qt.Key_W:
            self.setRotation(0)
            dy -= player_speed
        if event.key() == Qt.Key_S:
            self.setRotation(180)
            dy += player_speed
        print(self.x(), self.y())
        self.setPos(self.x()+dx, self.y()+dy)

