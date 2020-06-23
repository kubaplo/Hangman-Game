from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys, string


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
        start_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button_font = QtGui.QFont(title_font)
        button_font.setPointSize(20)
        start_button.setFont(button_font)
        start_button.setStyleSheet("background-color: none")
        w = 300
        h = 80
        start_button.setGeometry(int((self.width()-w)/2), int((self.height()-h)/2), w, h)
        start_button.clicked.connect(self.get_word)
        self.start_button = start_button


    def get_word(self):
        get_word_frame = QtWidgets.QFrame(self)
        get_word_frame.setGeometry(0, 0, self.width(), self.height())
        self.get_word_frame = get_word_frame

        title = QtWidgets.QLabel(get_word_frame)
        title.setText("CHOOSE WORD FOR YOUR OPPONENT")
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(35)
        font.setBold(True)
        font.setUnderline(True)
        title.setFont(font)
        title.adjustSize()
        title.move(int((get_word_frame.width()-title.width())/2), 30)
        self.get_word_title = title


        class CustomLineEdit(QtWidgets.QLineEdit):
            count = 1
            def keyPressEvent(self, event):
                key = event.text()
                ord_key = event.key()

                if self.count <= 20:

                    if key in string.ascii_lowercase:
                        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, ord(key.upper()), QtCore.Qt.NoModifier, 0, 0, 0, text=key.upper())
                        self.count += 1
                        super().keyPressEvent(event)

                    elif key in string.ascii_uppercase:
                        self.count += 1
                        super().keyPressEvent(event)

                if ord_key == QtCore.Qt.Key_Backspace:
                    if self.text() != "":
                        self.count -= 1
                    super().keyPressEvent(event)



        textinput = CustomLineEdit(get_word_frame)
        textinput.setFocus(True)
        textinput.setAlignment(QtCore.Qt.AlignCenter)
        textinput.setStyleSheet("border: 2px solid #8f8f8f")
        textinput.resize(800, 76)
        textinput.move(int((get_word_frame.width()-textinput.width())/2), int(get_word_frame.height()/4))

        textinput_font = QtGui.QFont(font)
        textinput_font.setPointSize(32)
        textinput_font.setUnderline(False)
        textinput.setFont(textinput_font)
        self.textinput = textinput



        get_word_frame.show()



    def resizeEvent(self, event):
        self.start_layout_widget.resize(self.width(), self.height())
        self.start_button.move(int((self.width()-self.start_button.width())/2)-1, int((self.height()-self.start_button.height())/2)+19)

        try:
            self.get_word_frame.resize(self.width(), self.height())
            self.get_word_title.move(int((self.get_word_frame.width()-self.get_word_title.width())/2), 30)
            self.textinput.move(int((self.get_word_frame.width()-self.textinput.width())/2), int(self.get_word_frame.height()/4))
        except:
            pass

















if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Application()
    game.show()
    sys.exit(app.exec_())