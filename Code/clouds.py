from PyQt5 import (QtWidgets, QtCore, QtGui, Qt, QtMultimedia)
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap

class Clouds(QGraphicsPixmapItem):

    def __init__(self, cloudTex, parent=None):
        QGraphicsPixmapItem.__init__(self, parent)
        # Dictionary of cloud pixmap objects
        self.cloud = {"cloud1": QPixmap("Textures/bg/cloud1.png"), "cloud2": QPixmap("Textures/bg/cloud2.png")}
        # Pick the wanted cloud object
        wanted_cloud = self.cloud[cloudTex]
        self.setPixmap(wanted_cloud)

    def move_clouds(self, SCENE_WIDTH):
        # Move clouds
        if self.x() < SCENE_WIDTH:
            self.setPos(self.x()+0.5, self.y())
        if self.x() >= SCENE_WIDTH:
            self.setPos(1, self.y())

