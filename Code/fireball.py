from PyQt5 import (QtWidgets, QtCore, QtGui, Qt, QtMultimedia)
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap

class FireBall(QGraphicsPixmapItem):

    def __init__(self, parent=None):
        QGraphicsPixmapItem.__init__(self, parent)
        self.setPixmap(QPixmap("PlayerTextures/Items/fireball.png"))

    def fireball_startpos(self):
        self.start_x = self.x()

    def fireBallFly(self):
        if self.x() < self.start_x+400:
            self.setPos(self.x()+20, self.y())
        else:
            self.setPixmap(QPixmap(None))
