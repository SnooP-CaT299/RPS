import sys
from random import randint, random
from bisect import bisect_left
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QMainWindow
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.uic import loadUi

def weighted_choice(values, weights):
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random() * total
    i = bisect_left(cum_weights, x)
    return values[i]

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

        self.player_wins = 0
        self.computer_wins = 0
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
        if self.prevres == 1:
            self.player_wins += 1
        elif self.prevres == 2:
            self.computer_wins += 1

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("D:\Project\RPS\gui\main_menu.ui", self)
        self.start_button.clicked.connect(self.openSecondWindow)
        self.tree_predictor = treePredictor()

        layout = QVBoxLayout()
        layout.addWidget(self.music_start)

        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.player.setSource(QUrl.fromLocalFile("D:\Project\RPS\scr\hit.mp3"))
        self.audioOutput.setVolume(50)
        self.player.play()

    def toggle_music(self):
        if self.music_start.isChecked():
            self.player.play()
        else:
            self.player.pause()

    def openSecondWindow(self):
        self.second_window = SecondWindow(self.tree_predictor)
        self.second_window.show()
        self.close()

class SecondWindow(QMainWindow):
    def __init__(self, tree_predictor):
        super().__init__()
        loadUi("D:\Project\RPS\gui\second_window.ui", self)
        self.tree_predictor = tree_predictor
        self.menu.clicked.connect(self.openMainMenu)
        self.rock_button.clicked.connect(lambda: self.make_choice('Rock'))
        self.paper_button.clicked.connect(lambda: self.make_choice('Paper'))
        self.scissors_button.clicked.connect(lambda: self.make_choice('Scissors'))
        self.result.setText("")
        self.player.setText("0")
        self.computer.setText("0")

    def openMainMenu(self):
        self.mainmenu = MainMenu()
        self.mainmenu.show()
        self.close()

    def make_choice(self, choice):
        computer_choice = self.tree_predictor.predict()
        self.tree_predictor.store(choice)
        winner = self.determine_winner(choice, computer_choice)
        result_text = f"Player: {choice}\nComputer: {computer_choice}\nResult: {winner}"
        self.result.setText(result_text)
        self.update_score_labels()

    def determine_winner(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            return "It's a tie!"
        elif (player_choice == 'Rock' and computer_choice == 'Scissors') or \
             (player_choice == 'Paper' and computer_choice == 'Rock') or \
             (player_choice == 'Scissors' and computer_choice == 'Paper'):
            return "Player wins!"
        else:
            return "Computer wins!"

    def update_score_labels(self):
        self.player.setText(f" {self.tree_predictor.player_wins}")
        self.computer.setText(f" {self.tree_predictor.computer_wins}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = MainMenu()
    mainMenu.show()
    sys.exit(app.exec())
