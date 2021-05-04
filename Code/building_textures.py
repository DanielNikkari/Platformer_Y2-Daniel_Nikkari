from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem


class BuildingTextures(QGraphicsPixmapItem):

    def __init__(self, texture, parent=None):
        QGraphicsPixmapItem.__init__(self, parent)

        self.building_textures = {"houseGray": QPixmap("Textures/Building_Textures/Wall_Textures/houseGray.png"),
                                  "houseGrayAlt": QPixmap("Textures/Building_Textures/Wall_Textures/houseGrayAlt.png"),
                                  "houseGrayAlt2": QPixmap("Textures/Building_Textures/Wall_Textures/houseGrayAlt2.png"),
                                  "houseGrayBottomLeft": QPixmap("Textures/Building_Textures/Wall_Textures/houseGrayBottomLeft.png"),
                                  "houseGrayBottomMid": QPixmap("Textures/Building_Textures/Wall_Textures/houseGrayBottomMid.png"),
                                  "houseGrayBottomRight": QPixmap("Textures/Building_Textures/Wall_Textures/houseGrayBottomRight.png"),
                                  "houseGrayMidLeft": QPixmap("Textures/Building_Textures/Wall_Textures/houseGrayMidLeft.png"),
                                  "houseGrayMidRight": QPixmap("Textures/Building_Textures/Wall_Textures/houseGrayMidRight.png"),
                                  "houseGrayTopLeft": QPixmap("Textures/Building_Textures/Wall_Textures/houseGrayTopLeft.png"),
                                  "houseGrayTopMid": QPixmap("Textures/Building_Textures/Wall_Textures/houseGrayTopMid.png"),
                                  "houseGrayTopRight": QPixmap("Textures/Building_Textures/Wall_Textures/houseGrayTopRight.png"),
                                  "windowHighCheckeredBottom": QPixmap("Textures/Building_Textures/Window_Textures/windowHighCheckeredBottom.png"),
                                  "windowHighCheckeredMid": QPixmap("Textures/Building_Textures/Window_Textures/windowHighCheckeredMid.png"),
                                  "windowHighCheckeredTop": QPixmap("Textures/Building_Textures/Window_Textures/windowHighCheckeredTop.png"),
                                  "windowLowCheckered": QPixmap("Textures/Building_Textures/Window_Textures/windowLowCheckered.png"),
                                  "roofRedLeft": QPixmap("Textures/Building_Textures/Roof_Textures/roofRedLeft.png"),
                                  "roofRedMid": QPixmap("Textures/Building_Textures/Roof_Textures/roofRedMid.png"),
                                  "roofRedRight": QPixmap("Textures/Building_Textures/Roof_Textures/roofRedRight.png"),
                                  "doorLock": QPixmap("Textures/Building_Textures/Door_Textures/doorLock.png"),
                                  "doorOpen": QPixmap("Textures/Building_Textures/Door_Textures/doorOpen.png"),
                                  "doorPlateTop": QPixmap("Textures/Building_Textures/Door_Textures/doorPlateTop.png"),
                                  "doorOpenTop": QPixmap("Textures/Building_Textures/Door_Textures/doorOpenTop.png"),
                                  "anemometer": QPixmap("Textures/Building_Textures/Building_Misc/anemometer.png"),
                                  "signHangingBed": QPixmap("Textures/Building_Textures/Building_Misc/signHangingBed.png")}
        wanted_texture = self.building_textures[texture]
        self.setPixmap(wanted_texture)
