import sys
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMainWindow, QGridLayout, QHBoxLayout
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

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
        self.setStyleSheet("background-color: rgb(38, 35, 43);")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        main_layout = QVBoxLayout(central_widget)

        title_label = QLabel("\n Rock\n Paper\n Scissors", self)
        title_font = QFont("Monotype Corsiva", 70)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: rgb(4, 209, 86);")
        layout.addWidget(title_label)
        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        button_layout = QHBoxLayout()

        start_button = QPushButton("Start", self)
        start_button.setFixedSize(60, 30)
        start_button.setStyleSheet(("color: rgb(4, 209, 86);"))
        button_layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        start_button.clicked.connect(self.start_game)
        main_layout.addLayout(button_layout)

        self.music_button = QPushButton(self)
        self.music_button.setFixedSize(100, 70)
        self.music_button.setCheckable(True)
        self.music_button.setChecked(True)
        self.music_button.clicked.connect(self.toggle_music)
        self.music_button.setIcon(QIcon("music_icon.png"))
        layout.addWidget(self.music_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.music_button)

        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.player.setSource(QUrl.fromLocalFile("hit.mp3"))
        self.audioOutput.setVolume(50)
        self.player.play()

    def toggle_music(self):
        if self.music_button.isChecked():
            self.player.play()
        else:
            self.player.pause()

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
        result_font = QFont("algerian", 20)  # Измените  на желаемый шрифт и на желаемый размер
        self.result_label.setFont(result_font)
        self.result_label.setStyleSheet(("color: rgb(247, 198, 20);"))
        layout.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        # Add win counters
        self.player_wins = 0
        self.computer_wins = 0

        self.player_wins_label = QLabel(f"Player Wins: {self.player_wins}", self)
        self.computer_wins_label = QLabel(f"Computer Wins: {self.computer_wins}", self)
        self.player_wins_label.setStyleSheet("color: rgb(247, 198, 20);")
        self.computer_wins_label.setStyleSheet("color: rgb(247, 198, 20);")
        layout.addWidget(self.player_wins_label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.computer_wins_label, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        images_layout = QVBoxLayout()

        self.player_image_label = QLabel(self)
        self.player_label = QLabel("Player", self)
        self.player_label.setStyleSheet("color: rgb(247, 198, 20);")
        self.player_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.computer_image_label = QLabel(self)
        self.computer_label = QLabel("Computer", self)
        self.computer_label.setStyleSheet("color: rgb(247, 198, 20);")
        self.computer_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)

        images_layout.addWidget(self.player_label)
        images_layout.addWidget(self.player_image_label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)

        images_layout.addWidget(self.computer_label)
        images_layout.addWidget(self.computer_image_label, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)

        buttons_layout = QGridLayout()

        rock_button = QPushButton("Rock", self)
        rock_button.setFixedSize(70, 45)
        rock_button.setStyleSheet("color: rgb(109, 54, 181); font-size: 18px;")
        rock_button.clicked.connect(lambda: self.on_button_clicked("Rock"))
        buttons_layout.addWidget(rock_button, 0, 0)

        scissors_button = QPushButton("Scissors", self)
        scissors_button.setFixedSize(70, 45)
        scissors_button.setStyleSheet("color: rgb(109, 54, 181); font-size: 18px;")
        scissors_button.clicked.connect(lambda: self.on_button_clicked("Scissors"))
        buttons_layout.addWidget(scissors_button, 0, 1)

        paper_button = QPushButton("Paper", self)
        paper_button.setFixedSize(70, 45)
        paper_button.setStyleSheet("color: rgb(109, 54, 181); font-size: 18px;")
        paper_button.clicked.connect(lambda: self.on_button_clicked("Paper"))
        buttons_layout.addWidget(paper_button, 0, 2)

        layout.addLayout(images_layout)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def on_button_clicked(self, user_choice):
        computer_choice = random.choice(["Rock", "Scissors", "Paper"])
        result = self.determine_result(user_choice, computer_choice)

        # Set images based on choices
        self.set_images(user_choice, computer_choice)

        self.result_label.setText("Computer chose: " + computer_choice + "\n" + result)

        # Update win counters
        if result == "You win!":
            self.player_wins += 1
        elif result == "You lose!":
            self.computer_wins += 1

        # Update win counter labels
        self.player_wins_label.setText(f"Player Wins: {self.player_wins}")
        self.computer_wins_label.setText(f"Computer Wins: {self.computer_wins}")

    def determine_result(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a tie!"
        elif (user_choice == "Rock" and computer_choice == "Scissors") or (
                user_choice == "Scissors" and computer_choice == "Paper") or (
                user_choice == "Paper" and computer_choice == "Rock"):
            return "You win!"
        else:
            return "You lose!"

    def set_images(self, player_choice, computer_choice):
        player_image_path = f"{player_choice.lower()}.png"
        computer_image_path = f"{computer_choice.lower()}.png"

        player_pixmap = QPixmap(player_image_path)
        computer_pixmap = QPixmap(computer_image_path)

        self.player_image_label.setPixmap(player_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        self.computer_image_label.setPixmap(computer_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = RockPaperScissorsGame()
    game.show()
    sys.exit(app.exec())
