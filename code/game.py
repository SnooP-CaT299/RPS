import sys
import random
from random import randint
from bisect import bisect_left
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.uic import loadUi



def weighted_choice(values, weights):
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random.random() * total
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
        self.consecutive_wins = 0
        self.com_consecutive_wins = 0
        self.round_result = ""

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
        if self.prevres == 2:
            self.player_wins += 5
        elif self.prevres == 0:
            self.computer_wins += 5
        elif self.prevres != 1 and self.prevres != 2:
            self.consecutive_wins = 0
            self.com_consecutive_wins = 0


        # Убедимся, что счет не отрицательный
        self.player_wins = max(0, self.player_wins)
        self.computer_wins = max(0, self.computer_wins)

class AdvancedTreePredictor(treePredictor):
    def __init__(self):
        super().__init__()
        self.advanced_feature_active = False
        self.random_switch_used = False
    def weighted_choice(self,choices,weights):
        return random.choices(choices,weights)[0]

    def predict(self):
        if not self.random_switch_used and random.random() < 0.1:
            self.random_switch_used = True
            choice = randint(0, 2)
            self.prevmove = self.choices[choice]
            return self.choices[choice]
        else:
            return super().predict()
        self.random_switch_used = False

    def store(self, c):
        super().store(c)
        i1 = self.choices.index(c)

        if not (self.prevchoice is None or self.prevres is None):
            roll = self.getRollbyInd(self.prevchoice, i1)
            for i in range(3):
                for j in range(3):
                    self.dataarr[i][j] *= 0.9
            self.dataarr[self.prevres][roll] += 1

        self.prevchoice = i1
        self.prevres = self.gameRes(c, self.prevmove)

        if self.prevres == 2:
            self.player_wins += 5
            self.consecutive_wins += 1
            self.com_consecutive_wins = 0

            if self.consecutive_wins == 3:
                self.player_wins += 10
                self.consecutive_wins = 0
            elif self.computer_wins > 0:
                self.computer_wins -= 5

        elif self.prevres == 0:
            self.computer_wins += 5
            self.com_consecutive_wins += 1
            self.consecutive_wins = 0

            if self.com_consecutive_wins == 2:
                self.player_wins -= 10
            elif self.com_consecutive_wins == 3:
                self.computer_wins += 10

            if self.com_consecutive_wins == 4:
                self.com_consecutive_wins = 0
            else:
                if self.player_wins > 0:
                    self.player_wins -= 5

        else:  # Tie or other result
            self.consecutive_wins = 0
            self.com_consecutive_wins = 0

        self.player_wins = max(0, self.player_wins)
        self.computer_wins = max(0, self.computer_wins)


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("../gui/main_menu.ui", self)

        self.start_button.clicked.connect(self.openSecondWindow)
        self.radio_classic.clicked.connect(self.setMode)
        self.radio_advanced.clicked.connect(self.setMode)
        self.help_button.clicked.connect(self.showHelp)
        self.exit_button.clicked.connect(self.exit_game)
        self.info.hide()
        self.mode = 'classic'
        self.tree_predictor = None
    def exit_game(self):
        self.close()

    def closeEvent(self, event):
        self.start_button.clicked.disconnect()
        self.radio_classic.clicked.disconnect()
        self.radio_advanced.clicked.disconnect()
        self.help_button.clicked.disconnect()
        self.exit_button.clicked.disconnect()

        if self.tree_predictor:
            self.tree_predictor = None
        self.deleteLater()
        event.accept()

    def setMode(self):
        if self.radio_classic.isChecked():
            self.mode = 'classic'
        elif self.radio_advanced.isChecked():
            self.mode = 'extended'

    def openSecondWindow(self):
        if self.mode == 'classic':
            self.tree_predictor = treePredictor()
            mode_text = "Classic"
        elif self.mode == 'extended':
            self.tree_predictor = AdvancedTreePredictor()
            mode_text = "Advanced"
        self.second_window = SecondWindow(self.tree_predictor, mode_text)
        self.second_window.show()
        self.close()

    def showHelp(self):
        self.info.show()
        self.setWidgetsEnabled(False)

    def hideHelp(self):
        self.info.hide()
        self.setWidgetsEnabled(True)

    def setWidgetsEnabled(self, enabled):
        # Блокировка/разблокировка всех виджетов
        self.start_button.setEnabled(enabled)
        self.radio_classic.setEnabled(enabled)
        self.radio_advanced.setEnabled(enabled)
        self.exit_button.setEnabled(enabled)
        self.help_button.setEnabled(enabled)

    def keyPressEvent(self, event):
        if self.info.isVisible():
            self.hideHelp()


class SecondWindow(QMainWindow):
    def __init__(self, tree_predictor, mode_text):
        super().__init__()
        loadUi("../gui/second_window.ui", self)
        self.tree_predictor = tree_predictor
        self.mode.setText(f"{mode_text}")
        self.menu.clicked.connect(self.openMainMenu)
        self.rock_button.clicked.connect(lambda: self.make_choice('Rock'))
        self.paper_button.clicked.connect(lambda: self.make_choice('Paper'))
        self.scissors_button.clicked.connect(lambda: self.make_choice('Scissors'))
        self.result.setText("")
        self.player.setText("0")
        self.computer.setText("0")
        self.round_counter = 0

        # Таймеры
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)

        # Таймер для хода игрока
        self.move_timer = QTimer(self)
        self.move_timer.setSingleShot(True)
        self.move_timer.timeout.connect(self.on_timeout)
        self.start_countdown(3)

    def closeEvent(self, event):
        if self.countdown_timer.isActive():
            self.countdown_timer.stop()
        self.countdown_timer.deleteLater()

        if self.move_timer.isActive():
            self.move_timer.stop()
        self.move_timer.deleteLater()
        self.tree_predictor = None
        self.deleteLater()
        event.accept()


    def start_move_timer(self, duration_ms):
         self.move_timer.start(duration_ms)
    def start_countdown(self, seconds):
        self.remaining_time = seconds
        self.countdown_label.setText(str(self.remaining_time))
        self.countdown_label.show()
        self.rock_button.setEnabled(False)
        self.paper_button.setEnabled(False)
        self.scissors_button.setEnabled(False)
        self.countdown_timer.start(1000)

    def openMainMenu(self):
        self.mainmenu = MainMenu()
        self.mainmenu.show()
        self.close()

    def update_countdown(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.countdown_label.setText(str(self.remaining_time))
        else:
            self.countdown_timer.stop()  # Останавливаем таймер обратного отсчета
            self.countdown_label.hide()  # Скрываем label
            self.rock_button.setEnabled(True)  # кнопки доступные
            self.paper_button.setEnabled(True)
            self.scissors_button.setEnabled(True)

            if isinstance(self.tree_predictor, AdvancedTreePredictor):
                self.start_move_timer(1 * 15 * 1000)  # Таймер на 15 сек

    def on_timeout(self):
        self.tree_predictor.player_wins = max(0, self.tree_predictor.player_wins - 2)  #
        self.update_score_labels()

    def make_choice(self, player_choice):
        if self.move_timer.isActive():
            self.move_timer.stop()

        # Компьютер делает свой выбор
        computer_choice = self.tree_predictor.predict()

        if isinstance(self.tree_predictor, AdvancedTreePredictor) and self.tree_predictor.random_switch_used:
            player_choice = random.choice(self.tree_predictor.choices)  # случайный выбор для игрока
            self.tree_predictor.random_switch_used = False  # Сброс флага после использования

        self.tree_predictor.store(player_choice)

        winner = self.determine_winner(player_choice, computer_choice)
        self.round_counter += 1

        result_text = f"Player: {player_choice}\nComputer: {computer_choice}\nResult: {winner}"
        self.result.setText(result_text)

        self.update_score_labels()

        if self.round_counter >= 15:
            self.open_result_window()
        else:
            self.start_new_round()

    def start_new_round(self):
        self.start_countdown(3)

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

    def open_result_window(self):
        player_wins = self.tree_predictor.player_wins
        computer_wins = self.tree_predictor.computer_wins
        self.result_window = ResultWindow(player_wins, computer_wins)
        self.result_window.show()
        self.close()


class ResultWindow(QMainWindow):
    def __init__(self, player_wins, computer_wins):
        super().__init__()
        loadUi("../gui/result.ui", self)

        if player_wins > computer_wins:
            result_text = f"Player wins\nScore: Player: {player_wins} \n Computer: {computer_wins}"
        elif computer_wins > player_wins:
            result_text = f"Computer wins\nScore: Player: {player_wins} \n Computer: {computer_wins}"
        else:
            result_text = f"Tie\nScore: Player: {player_wins} \n Computer: {computer_wins}"
        self.reslabel.setText(result_text)
        self.bttm.clicked.connect(self.restart_game)

    def closeEvent(self, event):
        self.bttm.clicked.disconnect()
        self.deleteLater()
        event.accept()

    def restart_game(self):
        self.close()
        self.main_menu = MainMenu()
        self.main_menu.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = MainMenu()
    mainMenu.show()
    sys.exit(app.exec())
