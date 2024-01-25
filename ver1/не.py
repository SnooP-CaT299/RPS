import sys
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMainWindow, QMenuBar, QGridLayout
from PyQt6.QtCore import Qt
import random

class RockPaperScissorsGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('RPS')
        self.setFixedSize(1000, 600)
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

        main_layout = QVBoxLayout(central_widget)

        title_label = QLabel("\n Rock\n Paper\n Scissors", self)
        title_font = QFont("Monotype Corsiva", 70)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: rgb(0, 0, 255);")
        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        button_layout = QHBoxLayout()

        start_button = QPushButton("Start", self)
        start_button.setFixedSize(150, 50)
        button_layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Set alignment
        start_button.clicked.connect(self.start_game)

        main_layout.addLayout(button_layout)

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

        self.result_label = QLabel("", self)
        result_font = QFont("algerian", 20)
        self.result_label.setFont(result_font)
        self.result_label.setStyleSheet("color: rgb(0, 128, 0);")
        layout.addWidget(self.result_label)

        buttons_layout = QGridLayout()

        rock_button = QPushButton("Rock", self)
        rock_button.setFixedSize(100, 50)
        rock_button.clicked.connect(lambda: self.on_button_clicked("Rock"))
        buttons_layout.addWidget(rock_button, 0, 0)

        scissors_button = QPushButton("Scissors", self)
        scissors_button.setFixedSize(100, 50)
        scissors_button.clicked.connect(lambda: self.on_button_clicked("Scissors"))
        buttons_layout.addWidget(scissors_button, 0, 1)

        paper_button = QPushButton("Paper", self)
        paper_button.setFixedSize(100, 50)
        paper_button.clicked.connect(lambda: self.on_button_clicked("Paper"))
        buttons_layout.addWidget(paper_button, 0, 2)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def on_button_clicked(self, user_choice):
        computer_choice = random.choice(["Rock", "Scissors", "Paper"])
        result = self.determine_result(user_choice, computer_choice)
        self.result_label.setText("Computer chose: " + computer_choice + "\n" + result)

    def determine_result(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a tie!"
        elif (user_choice == "Rock" and computer_choice == "Scissors") or (
                user_choice == "Scissors" and computer_choice == "Paper") or (
                user_choice == "Paper" and computer_choice == "Rock"):
            return "You win!"
        else:
            return "You lose!"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = RockPaperScissorsGame()
    game.show()
    sys.exit(app.exec())
