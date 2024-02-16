import sys
from random import randint, random
from bisect import bisect_left
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMainWindow, QGridLayout, QHBoxLayout
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.uic import loadUi


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main_menu.ui", self)
        self.start_button.clicked.connect(self.openGameWindow)

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

    def openGameWindow(self):
        self.game_window = RockPaperScissorsGame()
        self.game_window.show()
        self.close()


class RockPaperScissorsGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tp = treePredictor()
        self.initUI()

    def initUI(self):
        # (Оставьте код для создания интерфейса из первого кода без изменений)

    def start_game(self):
        game_widget = RockPaperScissorsWidget(self.tp)
        self.setCentralWidget(game_widget)


class RockPaperScissorsWidget(QWidget):
    def __init__(self, tree_predictor):
        super().__init__()
        self.tp = tree_predictor
        self.initUI()

    def initUI(self):
        # (Оставьте код для создания интерфейса из первого кода без изменений)

    def on_button_clicked(self, user_choice):
        # (Оставьте код для обработки нажатий кнопок из первого кода без изменений)
        computer_choice = self.tp.predict()
        result = self.determine_result(user_choice, computer_choice)
        self.set_images(user_choice, computer_choice)
        self.result_label.setText("Computer chose: " + computer_choice + "\n" + result)
        if result == "You win!":
            self.player_wins += 1
        elif result == "You lose!":
            self.computer_wins += 1
        self.player_wins_label.setText(f"Player Wins: {self.player_wins}")
        self.computer_wins_label.setText(f"Computer Wins: {self.computer_wins}")


class treePredictor():
    def __init__(self):
        self.choices = ['Rock', 'Paper', 'Scissors']
        self.prevchoice = None  # computer move
        self.prevmove = None  # my move
        self.prevres = None
        self.dataarr = [[0. for _ in range(3)] for _ in range(3)]  # result, roll

        self.gameMat = []
        self.gameMat.append([1, 0, 2])
        self.gameMat.append([2, 1, 0])
        self.gameMat.append([0, 2, 1])
        self.beatMat = [1, 2, 0]

        self.rollMat = []
        self.rollMat.append([0, 1, 2])
        self.rollMat.append([2, 0, 1])
        self.rollMat.append([1, 2, 0])

        self.losecount = 0;
        self.playrand = False
        self.mult = 1.0

    def gameRes(self, c1, c2):
        i1 = self.choices.index(c1)
        i2 = self.choices.index(c2)

        return self.gameMat[i1][i2]

    def getRoll(self, c1, c2):
        i1 = self.choices.index(c1)
        i2 = self.choices.index(c2)
        return self.rollMat[i1][i2]

    def getRollbyInd(self, i1, i2):
        # i1 = self.choices.index(c1)
        # i2 = self.choices.index(c2)
        return self.rollMat[i1][i2]

    def rollInd(self, i1, inc):

        row = self.rollMat[i1]
        ind = row.index(inc)
        return ind

    def predict(self):
        if self.prevchoice is None or self.prevres is None:
            ret = self.choices[randint(0, 2)]
            self.prevmove = ret
            return ret
        arr = self.dataarr[self.prevres]

        predictedroll = weighted_choice([0, 1, 2], arr)
        predictedchoice = self.rollInd(self.prevchoice, predictedroll)

        choice = self.beatMat[predictedchoice]
        if self.playrand:
            self.playrand = False

            choice = randint(0, 2)

        self.prevmove = self.choices[choice]
        return self.choices[choice]

    def store(self, c):

        i1 = self.choices.index(c)

        if not (self.prevchoice is None or self.prevres is None):
            roll = self.getRollbyInd(self.prevchoice, i1)
            for i in range(3):
                for j in range(3):
                    self.dataarr[i][j] *= 0.9
            self.dataarr[self.prevres][roll] += 1

        self.prevchoice = i1
        self.prevres = self.gameRes(c, self.prevmove)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = MainMenu()
    mainMenu.show()
    sys.exit(app.exec())
