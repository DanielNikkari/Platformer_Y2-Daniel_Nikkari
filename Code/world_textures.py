from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5 import QtWidgets, QtGui, QtCore

class WorldTextures(QGraphicsPixmapItem):

    #Class that holds the textures needed for the platformer world

    def __init__(self, texture, parent = None):
        QGraphicsPixmapItem.__init__(self, parent)
        # Create a dictionary which holds different world textures
        self.worldTextures = {"grassMidTex": QPixmap("Textures/Ground_Textures/grassMid.png"),
                              "grassCenterTex": QPixmap("Textures/Ground_Textures/grassCenter.png"),
                              "backgroundTex": QPixmap("Textures/bg/bg.png"),
                              "start_button": QPixmap("Textures/Menu_Textures/start_button.png"),
                              "quit_button": QPixmap("Textures/Menu_Textures/quit_button.png"),
                              "wasd": QPixmap("Textures/Menu_Textures/wasd_keys_withoutbg.png"),
                              "ghost_menu": QPixmap("Textures/NPC_Textures/ghost_normal.png"),
                              "menu_player": QPixmap("Textures/Menu_Textures/alienGreen.png"),
                              "box": QPixmap("Textures/Obstacle_Textures/box.png"),
                              "bush": QPixmap("Textures/bg/bush.png"),
                              "cloud1": QPixmap("Textures/bg/cloud1.png"),
                              "cloud2": QPixmap("Textures/bg/cloud2.png")}
        # Pick the wanted texture from the dictionary
        wanted_texture = self.worldTextures[texture]
        self.setPixmap(wanted_texture)


