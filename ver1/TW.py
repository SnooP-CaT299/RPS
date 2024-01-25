import sys

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer


def main():
    app = QGuiApplication(sys.argv)

    filename = "sound.mp3"
    player = QMediaPlayer()
    audio_output = QAudioOutput()
    player.setAudioOutput(audio_output)
    player.setSource(QUrl.fromLocalFile(filename))
    audio_output.setVolume(50)
    player.play()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()