import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMainWindow,QMenuBar
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
import random

class RockPaperScissorsGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('RPS')
        self.setFixedSize(720,500)
        self.setGeometry(500, 300, 500, 400)
        self.setWindowIcon(QIcon('RPS.png'))

        main_menu = self.menuBar()
        game_menu = QMenuBar()
        game_menu = main_menu.addMenu("Sounds")

        mute_action = game_menu.addAction("Mute")
        mute_action.setCheckable(True)
        mute_action.triggered.connect(self.toggle_mute)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        title_label = QLabel("Rock Paper Scissors")
        layout.addWidget(title_label)

        start_button = QPushButton("Start", self)
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)

        central_widget.setLayout(layout)





    def toggle_mute(self):
        print("Mute toggled")

    def start_game(self):
        game_widget = RockPaperScissorsWidget()
        self.setCentralWidget(game_widget)


class RockPaperScissorsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        rock_button = QPushButton("Rock", self)
        rock_button.clicked.connect(lambda: self.on_button_clicked("Rock"))
        layout.addWidget(rock_button)

        scissors_button = QPushButton("Scissors", self)
        scissors_button.clicked.connect(lambda: self.on_button_clicked("Scissors"))
        layout.addWidget(scissors_button)

        paper_button = QPushButton("Paper", self)
        paper_button.clicked.connect(lambda: self.on_button_clicked("Paper"))
        layout.addWidget(paper_button)

        self.setLayout(layout)

    def on_button_clicked(self, user_choice):
        computer_choice = random.choice(["Rock", "Scissors", "Paper"])
        result = self.determine_result(user_choice, computer_choice)
        self.result_label.setText("Computer chose: " + computer_choice + "\n" + result)

    def determine_result(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a tie!"
        elif (user_choice == "Rock" and computer_choice == "Scissors") or (user_choice == "Scissors" and computer_choice == "Paper") or (user_choice == "Paper" and computer_choice == "Rock"):
            return "You win!"
        else:
            return "You lose!"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = RockPaperScissorsGame()
    game.show()
    sys.exit(app.exec())