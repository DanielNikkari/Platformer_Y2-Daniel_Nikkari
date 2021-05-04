from PyQt5 import QtCore


class Scores:

    # Create and save to a file

    def __init__(self):
        # Initiate save file
        self.datetime = QtCore.QDate
        self.curtime = QtCore.QTime

    def create_save_file(self):
        # Create the file into folder SavedScores
        date = self.datetime.currentDate()
        time = self.curtime.currentTime()
        timeString = time.toString()
        timeParsed = timeString.replace(':', ',')
        self.f = open("SavedScores//game_scores_date{}_time{}.txt".format(date.toString(), timeParsed), "w+")
        return "game_scores_date{}_time{}.txt".format(date.toString(), timeParsed)

    def open_save_file(self, filename):
        # Open save file
       self.f = open(filename, "w+")

    def save_to_file(self, player_name, minutes, seconds, mseconds):
        # Write the core to the save file
        self.f.write("{},{},{},{}\n".format(player_name, minutes, seconds, mseconds))

    def close_file(self):
        # Close the save file
        self.f.close()
