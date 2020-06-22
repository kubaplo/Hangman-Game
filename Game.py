from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys


class Application(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup()


    def setup(self):
        self.setWindowTitle("Hangman Game")
        width = 1200
        height = 800
        self.setGeometry(int((1920-width)/2), int((1080-height)/2), width, height)
        self.setStyleSheet("background-color: #777")

        start_layout = QtWidgets.QVBoxLayout()
        start_layout.setAlignment(QtCore.Qt.AlignTop)
        start_layout_widget = QtWidgets.QWidget(self)
        start_layout_widget.setLayout(start_layout)
        start_layout_widget.setGeometry(0, 0, self.width(), self.height())
        self.start_layout_widget = start_layout_widget

        game_title = QtWidgets.QLabel()
        game_title.setAlignment(QtCore.Qt.AlignHCenter)
        game_title.setText("Hangman Game")
        title_font = QtGui.QFont()
        title_font.setFamily("Bahnschrift")
        title_font.setPointSize(40)
        title_font.setBold(True)
        title_font.setUnderline(True)
        game_title.setFont(title_font)
        start_layout.addWidget(game_title)

        background_image = QtWidgets.QLabel(self)
        background_image.setGeometry(-70, 100, 900, 660)
        background_pixmap = QtGui.QPixmap("Images/start.png")
        background_image.setPixmap(background_pixmap)

        start_button = QtWidgets.QPushButton(self)
        start_button.setText("START GAME")
        button_font = QtGui.QFont(title_font)
        button_font.setPointSize(20)
        start_button.setFont(button_font)
        start_button.setStyleSheet("background-color: none")
        w = 300
        h = 80
        start_button.setGeometry(int((self.width()-w)/2), int((self.height()-h)/2), w, h)
        self.start_button = start_button










    def resizeEvent(self, event):
        self.start_layout_widget.resize(self.width(), self.height())
        self.start_button.move(int((self.width()-self.start_button.width())/2)-1, int((self.height()-self.start_button.height())/2)+19)















if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Application()
    game.show()
    sys.exit(app.exec_())