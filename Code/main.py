import sys
from gui import GUI
from PyQt5 import (QtWidgets, QtMultimedia, QtCore)

def main():
    # Main function from where the program is ran
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    playlist = QtMultimedia.QMediaPlaylist()
    url = QtCore.QUrl.fromLocalFile("Audio/Music/bg_lofiBeat.mp3")
    playlist.addMedia(QtMultimedia.QMediaContent(url))
    playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)

    media_player = QtMultimedia.QMediaPlayer()
    media_player.setPlaylist(playlist)
    media_player.setVolume(50)
    media_player.play()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
