from PyQt5 import (QtWidgets, QtCore, QtGui, Qt, QtMultimedia)
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap

class Scores():

    def __init__(self):
        self.datetime = QtCore.QDate
        self.curtime = QtCore.QTime

    def create_save_file(self):
        date = self.datetime.currentDate()
        time = self.curtime.currentTime()
        timeString = time.toString()
        timeParsed = timeString.replace(':', ',')
        self.f = open("game_scores_date{}_time{}.txt".format(date.toString(), timeParsed), "w+")
        return "game_scores_date{}_time{}.txt".format(date.toString(), timeParsed)

    def open_save_file(self, filename):
       self.f = open(filename, "w+")

    def save_to_file(self, player_name, minutes, seconds, mseconds):
        self.f.write("{},{},{},{}\n".format(player_name, minutes, seconds, mseconds))

    def close_file(self, filename):
        filename.close()
