from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.Qt import Qt

class WorldTextures(QGraphicsPixmapItem):

    #Class that holds the textures needed for the platformer world

    def __init__(self, texture, parent = None):
        QGraphicsPixmapItem.__init__(self, parent)
        self.grassTextures = {"grassMidTex": QPixmap("Textures/Ground_Textures/grassMid.png"),
                              "grassCenterTex": QPixmap("Textures/Ground_Textures/grassCenter.png"),
                              "backgroundTex": QPixmap("Textures/bg/bg.png")}
        wanted_texture = self.grassTextures[texture]
        self.setPixmap(wanted_texture)



