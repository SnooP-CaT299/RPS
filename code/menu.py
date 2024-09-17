import sys
import random
from random import randint
from bisect import bisect_left
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
from PyQt6.uic import loadUi


def weighted_choice(values, weights):
    cum_weights = []
    total = sum(weights)
    cum_weights = [sum(weights[:i+1]) for i in range(len(weights))]
    return values[bisect_left(cum_weights, random.random() * total)]


class TreePredictor:
    def __init__(self):
        self.choices = ['Rock', 'Paper', 'Scissors']
        self.prev_choice = self.prev_move = self.prev_res = None
        self.data_arr = [[0.0] * 3 for _ in range(3)]

        self.game_mat = [[1, 0, 2], [2, 1, 0], [0, 2, 1]]
        self.beat_mat = [1, 2, 0]
        self.roll_mat = [[0, 1, 2], [2, 0, 1], [1, 2, 0]]

        self.player_wins = self.computer_wins = 0
        self.consecutive_wins = self.com_consecutive_wins = 0

    def game_res(self, c1, c2):
        return self.game_mat[self.choices.index(c1)][self.choices.index(c2)]

    def get_roll_by_index(self, i1, i2):
        return self.roll_mat[i1][i2]

    def predict(self):
        if not self.prev_choice or not self.prev_res:
            self.prev_move = random.choice(self.choices)
            return self.prev_move

        arr = self.data_arr[self.prev_res]
        predicted_roll = weighted_choice([0, 1, 2], arr)
        predicted_choice = self.roll_mat[self.prev_choice].index(predicted_roll)
        self.prev_move = self.choices[self.beat_mat[predicted_choice]]
        return self.prev_move

    def store(self, player_choice):
        player_index = self.choices.index(player_choice)
        if self.prev_choice is not None and self.prev_res is not None:
            roll = self.get_roll_by_index(self.prev_choice, player_index)
            self.data_arr[self.prev_res][roll] += 1
            self.data_arr = [[w * 0.9 for w in row] for row in self.data_arr]

        self.prev_choice = player_index
        self.prev_res = self.game_res(player_choice, self.prev_move)

        if self.prev_res == 2:  # Player wins
            self.player_wins += 5
            self.consecutive_wins += 1
            self.com_consecutive_wins = 0
        elif self.prev_res == 0:  # Computer wins
            self.computer_wins += 5
            self.com_consecutive_wins += 1
            self.consecutive_wins = 0

        # Ensure scores are non-negative
        self.player_wins = max(0, self.player_wins)
        self.computer_wins = max(0, self.computer_wins)


class AdvancedTreePredictor(TreePredictor):
    def predict(self):
        if random.random() < 0.1:
            self.prev_move = random.choice(self.choices)
            return self.prev_move
        return super().predict()

    def store(self, player_choice):
        super().store(player_choice)

        if self.prev_res == 2:  # Player wins
            if self.consecutive_wins == 3:
                self.player_wins += 10
                self.consecutive_wins = 0
            elif self.computer_wins > 0:
                self.computer_wins -= 5

        elif self.prev_res == 0:  # Computer wins
            if self.com_consecutive_wins == 2:
                self.player_wins -= 10
            elif self.com_consecutive_wins == 3:
                self.computer_wins += 10
            if self.com_consecutive_wins == 4:
                self.com_consecutive_wins = 0
            elif self.player_wins > 0:
                self.player_wins -= 5


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("../gui/main_menu.ui", self)

        self.start_button.clicked.connect(self.open_second_window)
        self.radio_classic.clicked.connect(self.set_mode)
        self.radio_advanced.clicked.connect(self.set_mode)
        self.help_button.clicked.connect(self.show_help)
        self.exit_button.clicked.connect(self.close)

        self.info.hide()
        self.mode = 'classic'
        self.tree_predictor = None

    def set_mode(self):
        self.mode = 'classic' if self.radio_classic.isChecked() else 'extended'

    def open_second_window(self):
        predictor = TreePredictor() if self.mode == 'classic' else AdvancedTreePredictor()
        self.second_window = SecondWindow(predictor, self.mode.capitalize())
        self.second_window.show()
        self.close()

    def show_help(self):
        self.info.show()
        self.set_widgets_enabled(False)

    def hide_help(self):
        self.info.hide()
        self.set_widgets_enabled(True)

    def set_widgets_enabled(self, enabled):
        for widget in [self.start_button, self.radio_classic, self.radio_advanced, self.exit_button]:
            widget.setEnabled(enabled)


class SecondWindow(QMainWindow):
    def __init__(self, tree_predictor, mode_text):
        super().__init__()
        loadUi("../gui/second_window.ui", self)
        self.tree_predictor = tree_predictor
        self.mode.setText(f"{mode_text}")
        self.menu.clicked.connect(self.open_main_menu)
        self.rock_button.clicked.connect(lambda: self.make_choice('Rock'))
        self.paper_button.clicked.connect(lambda: self.make_choice('Paper'))
        self.scissors_button.clicked.connect(lambda: self.make_choice('Scissors'))

        self.round_counter = 0
        self.start_countdown(3)

    def open_main_menu(self):
        self.mainmenu = MainMenu()
        self.mainmenu.show()
        self.close()

    def start_countdown(self, seconds):
        self.remaining_time = seconds
        self.countdown_label.setText(str(self.remaining_time))
        self.countdown_label.show()
        self.set_buttons_enabled(False)
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

    def set_buttons_enabled(self, enabled):
        self.rock_button.setEnabled(enabled)
        self.paper_button.setEnabled(enabled)
        self.scissors_button.setEnabled(enabled)

    def update_countdown(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.countdown_label.setText(str(self.remaining_time))
        else:
            self.countdown_timer.stop()
            self.countdown_label.hide()
            self.set_buttons_enabled(True)

    def make_choice(self, player_choice):
        computer_choice = self.tree_predictor.predict()
        self.tree_predictor.store(player_choice)
        result_text = f"Player: {player_choice}\nComputer: {computer_choice}\nResult: {self.determine_winner(player_choice, computer_choice)}"
        self.result.setText(result_text)

        self.update_score_labels()
        self.round_counter += 1

        if self.round_counter >= 3:
            self.open_result_window()
        else:
            self.start_countdown(3)

    def determine_winner(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            return "It's a tie!"
        elif (player_choice == 'Rock' and computer_choice == 'Scissors') or \
                (player_choice == 'Paper' and computer_choice == 'Rock') or \
                (player_choice == 'Scissors' and computer_choice == 'Paper'):
            return "Player wins!"
        return "Computer wins!"

    def update_score_labels(self):
        self.player.setText(f"{self.tree_predictor.player_wins}")
        self.computer.setText(f"{self.tree_predictor.computer_wins}")

    def open_result_window(self):
        self.result_window = ResultWindow(self.tree_predictor.player_wins, self.tree_predictor.computer_wins)
        self.result_window.show()
        self.close()


class ResultWindow(QMainWindow):
    def __init__(self, player_wins, computer_wins):
        super().__init__()
        loadUi("../gui/result.ui", self)
        result_text = f"{'Player wins' if player_wins > computer_wins else 'Computer wins' if computer_wins > player_wins else 'Tie'}\nScore: Player: {player_wins} \n Computer: {computer_wins}"
        self.reslabel.setText(result_text)
        self.bttm.clicked.connect(self.restart_game)

    def restart_game(self):
        self.main_menu = MainMenu()
        self.main_menu.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = MainMenu()
    mainMenu.show()
    sys.exit(app.exec())
