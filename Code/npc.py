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
        self.NPCs = {"ghost": QPixmap("Textures/NPC_Textures/ghost.png"),
                     "bee": QPixmap("Textures/NPC_Textures/Bee/bee.png"),
                     "frog": QPixmap("Textures/NPC_Textures/Frog/frog.png"),
                     "snakeSlime": QPixmap("Textures/NPC_Textures/snakeSlime/snakeSlime.png")}
        # Pick the NPC with the key NPC_name
        wantedNPC = self.NPCs[NPC_name]
        self.setPixmap(wantedNPC)
        self.pointFlag = True
        self.start_x = 0
        self.start_y = 0

        # Bee sprite animation
        self.bee_sprites = []
        self.bee_sprites.append(QPixmap("Textures/NPC_Textures/Bee/bee.png"))
        self.bee_sprites.append(QPixmap("Textures/NPC_Textures/Bee/bee_fly.png"))
        self.current_bee_sprite = 0
        self.bee_image = self.bee_sprites[self.current_bee_sprite]

        # Frog sprite animation and death
        self.frog_sprites = []
        self.frog_sprites.append(QPixmap("Textures/NPC_Textures/Frog/frog.png"))
        self.frog_sprites.append(QPixmap("Textures/NPC_Textures/Frog/frog_leap.png"))
        self.frog_dead = QPixmap("Textures/NPC_Textures/Frog/frog_dead.png")
        self.current_frog_sprite = 0
        self.frog_image = self.frog_sprites[self.current_frog_sprite]
        self.frogDeadFlag = False

        # Snakeslime sprite
        self.snakeslime_sprite = []
        self.snakeslime_sprite.append(QPixmap("Textures/NPC_Textures/snakeSlime/snakeSlime_ani.png"))
        self.snakeslime_sprite.append(QPixmap("Textures/NPC_Textures/snakeSlime/snakeSlime.png"))
        self.current_snakeslime_sprite = 0
        self.snakeslime_image = self.snakeslime_sprite[self.current_snakeslime_sprite]

    def start_pos(self):
        # Get the ghosts start x pos to anchor the ghosts movement around it.
        self.start_x = self.x()
        self.start_y = self.y()

    def sprite_bee(self):
        # Produce the bee flying animation using sprite animation.
        # Slow down the animation by adding only 0.5
        self.current_bee_sprite += 0.5
        if int(self.current_bee_sprite) >= len(self.bee_sprites):
            self.current_bee_sprite = 0
        self.bee_image = self.bee_sprites[int(self.current_bee_sprite)]
        return self.bee_image

    def sprite_frog(self):
        # Produce the frog leaping animation using sprite animation.
        # Slow down the animation by adding only 0.5
        self.current_frog_sprite += 0.05
        if int(self.current_frog_sprite) >= len(self.frog_sprites):
            self.current_frog_sprite = 0
        self.frog_image = self.frog_sprites[int(self.current_frog_sprite)]
        # If frog is leaping make frogs y smaller
        if self.frog_image == self.frog_sprites[1]:
            self.setPos(self.x(), self.y()-2.5)
        # If frog is not leaping make frogs y back to original
        if self.frog_image == self.frog_sprites[0]:
            self.setPos(self.x(), self.start_y)
        return self.frog_image

    def sprite_snakeSlime(self):
        # Produce the snakeslime wobble using sprite animation.
        # Slow down the animation by adding only 0.5
        self.current_snakeslime_sprite += 0.1
        if int(self.current_snakeslime_sprite) >= len(self.snakeslime_sprite):
            self.current_snakeslime_sprite = 0
        self.snakeslime_image = self.snakeslime_sprite[int(self.current_snakeslime_sprite)]
        return self.snakeslime_image

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

    def game_update_bee(self):
        # Make bee move back and forth
        dx = 0
        if self.pointFlag:
            dx -= 6
            self.setPos(self.x() + dx, self.y())
            if self.x() < (self.start_x - 150):
                self.pointFlag = False

        if not self.pointFlag:
            dx += 6
            self.setPos(self.x() + dx, self.y())
            if self.x() > (self.start_x + 150):
                self.pointFlag = True
        # Update bee sprite
        pic = self.sprite_bee()
        self.setPixmap(pic)

    def frog_deadFunc(self):
        self.frogDeadFlag = True

    def game_update_frog(self):
        # Make frog leap back and forth

        # Check if frog is dead or not
        if self.frogDeadFlag:
            self.setPixmap(self.frog_dead)
            self.setPos(self.x(), self.start_y+20)
        else:
            dx = 0
            if self.pointFlag:
                # check if frog is leaping and if it is, move the frog
                if self.frog_image == self.frog_sprites[1]:
                    dx -= 4
                    self.setPos(self.x() + dx, self.y())
                    if self.x() < (self.start_x - 400):
                        self.pointFlag = False

            if not self.pointFlag:
                # check if frog is leaping and if it is, move the frog
                if self.frog_image == self.frog_sprites[1]:
                    dx += 4
                    self.setPos(self.x() + dx, self.y())
                    if self.x() > (self.start_x + 400):
                        self.pointFlag = True
            # Update frog sprite
            pic2 = self.sprite_frog()
            self.setPixmap(pic2)

    def game_update_snakeSlime(self):
        pic = self.sprite_snakeSlime()
        self.setPixmap(pic)
