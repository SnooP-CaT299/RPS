import sys
from random import randint
from random import random
from bisect import bisect, bisect_left
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMainWindow, QGridLayout, QHBoxLayout
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.uic import loadUi


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main_menu.ui",self)
        self.start_button.clicked.connect(self.openSecondWindow)

        layout = QVBoxLayout()


        layout.addWidget(self.music_start)

        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.player.setSource(QUrl.fromLocalFile("hit.mp3"))
        self.audioOutput.setVolume(50)
        self.player.play()

    def toggle_music(self):
        if self.music_start.isChecked():
            self.player.play()
        else:
            self.player.pause()
    def openSecondWindow(self):
        self.second_window = SecondWindow()
        self.second_window.show()
        self.close()

class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("second_window.ui", self)
        self.back_to_menu.clicked.connect(self.openMainMenu)
    def openMainMenu(self):
        self.mainmenu = MainMenu()
        self.mainmenu.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = MainMenu()
    mainMenu.show()
    sys.exit(app.exec())
