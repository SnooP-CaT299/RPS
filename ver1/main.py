import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import random

class RockPaperScissorsGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        rock_button = QPushButton("Камень", self)
        rock_button.clicked.connect(lambda: self.on_button_clicked("Камень"))
        layout.addWidget(rock_button)

        scissors_button = QPushButton("Ножницы", self)
        scissors_button.clicked.connect(lambda: self.on_button_clicked("Ножницы"))
        layout.addWidget(scissors_button)

        paper_button = QPushButton("Бумага", self)
        paper_button.clicked.connect(lambda: self.on_button_clicked("Бумага"))
        layout.addWidget(paper_button)

        self.setLayout(layout)
        self.setWindowTitle('Камень, ножницы, бумага')

    def on_button_clicked(self, user_choice):
        computer_choice = random.choice(["Камень", "Ножницы", "Бумага"])
        result = self.determine_result(user_choice, computer_choice)
        self.result_label.setText("Компьютер выбрал: " + computer_choice + "\n" + result)

    def determine_result(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "Ничья!"
        elif (user_choice == "Камень" and computer_choice == "Ножницы") or (user_choice == "Ножницы" and computer_choice == "Бумага") or (user_choice == "Бумага" and computer_choice == "Камень"):
            return "Вы победили!"
        else:
            return "Вы проиграли!"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = RockPaperScissorsGame()
    game.show()
    sys.exit(app.exec())