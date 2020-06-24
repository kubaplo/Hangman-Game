from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys, time, string, threading


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

        letters_container = QtWidgets.QWidget(get_word_frame)
        letters_container.setGeometry(0, int(self.height()/1.9), self.width(), 150)

        letters_container_layout = QtWidgets.QHBoxLayout()
        letters_container_layout.setAlignment(QtCore.Qt.AlignCenter)
        letters_container_layout.setSpacing(15)
        letters_container.setLayout(letters_container_layout)
        self.letters_container = letters_container


        def add_letter(char, labels):
            font = QtGui.QFont()
            font.setFamily("Bahnschrift")
            font.setBold(True)
            font.setUnderline(True)
            font.setPointSize(40)

            label = QtWidgets.QLabel()
            label.setText(char)
            label.setFont(font)
            letters_container_layout.addWidget(label)
            letters_container.show()

            labels.append(label)
            return labels

        def remove_letter(label):
            letters_container_layout.removeWidget(label)
            label.deleteLater()


        class CustomLineEdit(QtWidgets.QLineEdit):
            count = 1
            labels = []
            showing_alert = False
            maxCount = 20
            minCount = 3

            def keyPressEvent(self, event):
                key = event.text()
                ord_key = event.key()

                if self.count <= self.maxCount:

                    if key in string.ascii_lowercase and key:
                        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, ord(key.upper()), QtCore.Qt.NoModifier, 0, 0, 0, text=key.upper())
                        self.count += 1
                        add_letter(key.upper(), self.labels)

                        super().keyPressEvent(event)

                    elif key in string.ascii_uppercase and key:
                        self.count += 1
                        add_letter(key, self.labels)

                        super().keyPressEvent(event)

                else:
                    if not self.showing_alert and (key in string.ascii_lowercase or key in string.ascii_uppercase) and key:
                        char_alert_thread = threading.Thread(target=self.too_many_letters, daemon=True)
                        char_alert_thread.start()


                if ord_key == QtCore.Qt.Key_Backspace:
                    if self.text() != "":
                        self.count -= 1
                        remove_letter(self.labels[-1])
                        del self.labels[-1]

                    super().keyPressEvent(event)


                if self.count > self.minCount:
                    next_button.setDisabled(False)

                else:
                    next_button.setDisabled(True)




            def too_many_letters(self):
                self.showing_alert = True
                char_alert.show()
                textinput.setStyleSheet("border: 2px solid red")
                time.sleep(3)
                char_alert.hide()
                textinput.setStyleSheet("border: 2px solid #8f8f8f")
                self.showing_alert = False



            def mousePressEvent(self, event):
                pass

            def mouseDoubleClickEvent(self, event):
                pass



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

        char_alert = QtWidgets.QLabel(get_word_frame)
        char_alert.setText("TOO MANY CHARACTERS! MAX: 20")
        char_alert.resize(460, 50)
        char_alert.move(int((get_word_frame.width() - char_alert.width()) / 2), int(textinput.y()+textinput.height()+5))
        alert_font = QtGui.QFont(font)
        alert_font.setPointSize(20)
        alert_font.setUnderline(False)
        char_alert.setFont(alert_font)
        char_alert.setStyleSheet("color: red")
        char_alert.hide()
        self.char_alert = char_alert


        class CustomNextButton(QtWidgets.QPushButton):
            showing_alert = False
            def enterEvent(self, event):
                if not self.isEnabled() and not self.showing_alert:
                    alert_thread = threading.Thread(target=show_alert_2, daemon=True)
                    alert_thread.start()


        def show_alert_2():
            self.showing_alert = True
            char_alert_2.show()
            time.sleep(3)
            char_alert_2.hide()
            self.showing_alert = False


        next_button = CustomNextButton(get_word_frame)
        next_button.setStyleSheet("background-color: none")
        next_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        next_button.resize(200, 50)
        next_button.move(int((self.width()-next_button.width())/2), self.height()-next_button.height()-20)
        next_button.setText("SUBMIT >>>")
        next_button_font = QtGui.QFont(font)
        next_button_font.setPointSize(20)
        next_button_font.setUnderline(False)
        next_button.setFont(next_button_font)
        next_button.setDisabled(True)
        self.next_button = next_button

        char_alert_2 = QtWidgets.QLabel(get_word_frame)
        char_alert_2.setAlignment(QtCore.Qt.AlignCenter)
        char_alert_2.resize(300, 50)
        char_alert_2.move(int((self.width()-char_alert_2.width())/2), next_button.y()-char_alert_2.height()-5)
        char_alert_2.setText("ENTER AT LEAST 3 CHARS!")
        char_alert_2.setStyleSheet("color: red")
        alert_font_2 = QtGui.QFont(alert_font)
        alert_font_2.setPointSize(15)
        char_alert_2.setFont(alert_font_2)
        char_alert_2.hide()
        self.char_alert_2 = char_alert_2


        get_word_frame.show()





    def resizeEvent(self, event):
        self.start_layout_widget.resize(self.width(), self.height())
        self.start_button.move(int((self.width()-self.start_button.width())/2)-1, int((self.height()-self.start_button.height())/2)+19)

        try:
            self.get_word_frame.resize(self.width(), self.height())
            self.get_word_title.move(int((self.get_word_frame.width()-self.get_word_title.width())/2), 30)
            self.textinput.move(int((self.get_word_frame.width()-self.textinput.width())/2), int(self.get_word_frame.height()/4))
            self.letters_container.setGeometry(0, int(self.height()/1.9), self.width(), 150)
            self.char_alert.move(int((self.get_word_frame.width()-self.char_alert.width())/2), int(self.textinput.y()+self.textinput.height()+5))
            self.next_button.move(int((self.width() - self.next_button.width()) / 2), self.height() - self.next_button.height() - 20)
            self.char_alert_2.move(int((self.width() - self.char_alert_2.width()) / 2), self.next_button.y() - self.char_alert_2.height() - 5)
        except:
            pass

        try:
            self.guess_word_frame.resize(self.width(), self.height())
            self.guess_word_title.move(int((self.width() - self.guess_word_title.width()) / 2), 30)

        except:
            pass

















if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Application()
    game.show()
    sys.exit(app.exec_())