import sys
import random
from random import randint
from bisect import bisect_left
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QMainWindow
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
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

        if self.prevres == 2:  # Player wins
            self.player_wins += 5  # Base points for win
            self.consecutive_wins += 1
            self.com_consecutive_wins = 0

            if self.consecutive_wins == 3:
                self.player_wins += 10  # Additional points for three consecutive wins
                self.consecutive_wins = 0
            elif self.computer_wins > 0:
                self.computer_wins -= 3  # Deduct points from computer's score

        elif self.prevres == 0:  # Computer wins
            self.computer_wins += 5  # Base points for win
            self.com_consecutive_wins += 1
            self.consecutive_wins = 0

            if self.com_consecutive_wins == 2:
                self.player_wins -= 10  # Deduct points from player's score
            elif self.com_consecutive_wins == 3:
                self.computer_wins += 10  # Additional points for three consecutive wins

            # Сюда добавляем условие для 4-х побед
            if self.com_consecutive_wins == 4:
                self.com_consecutive_wins = 0
            else:
                # Если не 4 победы подряд, то отнимаем очки у игрока
                if self.player_wins > 0:
                    self.player_wins -= 3

        else:  # Tie or other result
            self.consecutive_wins = 0
            self.com_consecutive_wins = 0

        # Ensure scores are not negative
        self.player_wins = max(0, self.player_wins)
        self.computer_wins = max(0, self.computer_wins)


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("../gui/main_menu.ui", self)

        # Подключаем кнопки к соответствующим действиям
        self.start_button.clicked.connect(self.openSecondWindow)
        self.radio_classic.clicked.connect(self.setMode)
        self.radio_advanced.clicked.connect(self.setMode)
        self.help_button.clicked.connect(self.showHelp)

        # Изначально скрываем поле info
        self.info.hide()

        # Изначальные значения
        self.mode = 'classic'
        self.tree_predictor = None

    def closeEvent(self, event):
        """Очистка ресурсов при закрытии окна"""
        # Разрываем соединения сигналов и слотов
        self.start_button.clicked.disconnect()
        self.radio_classic.clicked.disconnect()
        self.radio_advanced.clicked.disconnect()
        self.help_button.clicked.disconnect()

        # Очищаем дерево предсказателя, если оно было создано
        if self.tree_predictor:
            self.tree_predictor = None

        # Уничтожаем окно и его виджеты
        self.deleteLater()
        event.accept()

    def setMode(self):
        if self.radio_classic.isChecked():
            self.mode = 'classic'
        elif self.radio_advanced.isChecked():
            self.mode = 'extended'

        # Включение музыки
        layout = QVBoxLayout()
        layout.addWidget(self.music_start)

        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.player.setSource(QUrl.fromLocalFile("D:/Pyt 3.12/RPS/scr/hit.mp3"))
        self.audioOutput.setVolume(50)
        self.player.play()

    def toggle_music(self):
        if self.music_start.isChecked():
            self.player.play()
        else:
            self.player.pause()

    def openSecondWindow(self):
        if self.mode == 'classic':
            self.tree_predictor = treePredictor()
        elif self.mode == 'extended':
            self.tree_predictor = AdvancedTreePredictor()
        self.second_window = SecondWindow(self.tree_predictor)
        self.second_window.show()
        self.close()

    def showHelp(self):
        # Показываем текстовое поле info и блокируем остальные элементы
        self.info.show()
        self.setWidgetsEnabled(False)

    def hideHelp(self):
        # Скрываем текстовое поле info и разблокируем остальные элементы
        self.info.hide()
        self.setWidgetsEnabled(True)

    def setWidgetsEnabled(self, enabled):
        # Блокировка/разблокировка всех виджетов, кроме help
        self.start_button.setEnabled(enabled)
        self.radio_classic.setEnabled(enabled)
        self.radio_advanced.setEnabled(enabled)
        self.music_start.setEnabled(enabled)
        self.help_button.setEnabled(enabled)  # Не блокируем кнопку Help

    def keyPressEvent(self, event):
        # Проверяем, отображается ли info, и скрываем его при нажатии любой клавиши
        if self.info.isVisible():
            self.hideHelp()  # Скрываем info и разблокируем виджеты


class SecondWindow(QMainWindow):
    def __init__(self, tree_predictor):
        super().__init__()
        loadUi("../gui/second_window.ui", self)
        self.tree_predictor = tree_predictor
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

        # Таймер на 3 минуты для хода игрока
        self.move_timer = QTimer(self)
        self.move_timer.setSingleShot(True)
        self.move_timer.timeout.connect(self.on_timeout)

        self.start_countdown(3)  # Начало отсчета с 3 секунд

    def closeEvent(self, event):
        """Очистка ресурсов при закрытии окна"""
        # Остановка всех таймеров
        if self.countdown_timer.isActive():
            self.countdown_timer.stop()
        self.countdown_timer.deleteLater()

        if self.move_timer.isActive():
            self.move_timer.stop()
        self.move_timer.deleteLater()

        # Очищаем дерево предсказателя
        self.tree_predictor = None

        # Уничтожаем окно и его виджеты
        self.deleteLater()
        event.accept()


    def start_move_timer(self, duration_ms):
         """Запускает таймер на заданное количество миллисекунд (duration_ms)."""
         self.move_timer.start(duration_ms)  # Запускаем таймер на заданное время

    def start_countdown(self, seconds):
        self.remaining_time = seconds
        self.countdown_label.setText(str(self.remaining_time))  # Установка начального значения
        self.countdown_label.show()  # Показываем label
        self.rock_button.setEnabled(False)  # Делаем кнопки недоступными
        self.paper_button.setEnabled(False)
        self.scissors_button.setEnabled(False)
        self.countdown_timer.start(1000)  # Устанавливаем таймер на 1 секунду

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
            self.rock_button.setEnabled(True)  # Делаем кнопки доступными
            self.paper_button.setEnabled(True)
            self.scissors_button.setEnabled(True)

            # Запускаем таймер на 3 минуты после обратного отсчета
            if isinstance(self.tree_predictor, AdvancedTreePredictor):
                self.start_move_timer(1 * 15 * 1000)  # Таймер на 3 минуты

    def on_timeout(self):
        """Вызывается, если игрок не сделал ход за 3 минуты"""
        self.tree_predictor.player_wins = max(0, self.tree_predictor.player_wins - 1)  # Вычитаем одно очко у игрока
        self.update_score_labels()  # Обновляем счет


    def make_choice(self, player_choice):
        """Игрок сделал выбор, таймер сбрасывается"""
        if self.move_timer.isActive():
            self.move_timer.stop()  # Останавливаем таймер на 3 минуты

        # Компьютер делает свой выбор
        computer_choice = self.tree_predictor.predict()

        # Проверяем случайный выбор
        if isinstance(self.tree_predictor, AdvancedTreePredictor) and self.tree_predictor.random_switch_used:
            player_choice = random.choice(self.tree_predictor.choices)  # Выбираем случайный выбор для игрока
            self.tree_predictor.random_switch_used = False  # Сброс флага после использования

        # Сохраняем данные для анализа
        self.tree_predictor.store(player_choice)

        # Определяем победителя
        winner = self.determine_winner(player_choice, computer_choice)
        self.round_counter += 1

        # Вывод результата с указанием оригинального и измененного выбора игрока
        result_text = f"Player: {player_choice}\nComputer: {computer_choice}\nResult: {winner}"
        self.result.setText(result_text)

        self.update_score_labels()

        if self.round_counter >= 15:
            self.open_result_window()
        else:
            self.start_new_round()

    def start_new_round(self):
        """Запуск нового раунда после хода"""
        self.start_countdown(3)  # Начинаем отсчет перед следующим раундом

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

            # Устанавливаем текст в label res
        self.reslabel.setText(result_text)

        # Подключаем кнопки
        self.bttm.clicked.connect(self.restart_game)  # Кнопка перезапуска игры

    def closeEvent(self, event):
        """Очистка ресурсов при закрытии окна"""
        # Разрываем соединения сигналов и слотов
        self.bttm.clicked.disconnect()

        # Уничтожаем окно и его виджеты
        self.deleteLater()
        event.accept()

    def restart_game(self):
        # Реализация перезапуска игры
        self.close()  # Закрываем окно результатов

        # Здесь можно добавить логику для перезапуска игры, например, открытие главного меню
        self.main_menu = MainMenu()  # Предполагается, что есть класс MainMenu
        self.main_menu.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = MainMenu()
    mainMenu.show()
    sys.exit(app.exec())
