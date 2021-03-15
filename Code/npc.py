from PyQt5 import (QtWidgets, QtCore, QtGui, Qt, QtMultimedia)
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap

class NPC(QGraphicsPixmapItem):

    # NPC ghost class that initiates ghost graphics and processes movement algorithm.

    def __init__(self, NPC_name, parent = None):

        # Initiate the Pixmap graphics item
        QGraphicsPixmapItem.__init__(self, parent)
        # Set a Pixmap dictionary for the graphics items of the NPCs
        self.NPCs = {"ghost": QPixmap("Textures/NPC_Textures/ghost.png")}
        # Pick the NPC with the key NPC_name
        wantedNPC = self.NPCs[NPC_name]
        self.setPixmap(wantedNPC)
        self.pointFlag = True
        self.start_x = 0
        #self.setPixmap(QPixmap("Textures/NPC_Textures/ghost.png"))
        #self.setTransformOriginPoint(33, 45)

    def start_pos(self):
        # Get the ghosts start x pos to anchor the ghosts movement around it.
        self.start_x = self.x()

    def game_update_ghost(self):
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
                self.pointFlag = True
