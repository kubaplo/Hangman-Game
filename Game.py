from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys, time, string, threading, random


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

        self.start_page()


    def start_page(self):
        start_frame = QtWidgets.QFrame(self)
        start_frame.setGeometry(0, 0, self.width(), self.height())
        self.start_frame = start_frame

        game_title = QtWidgets.QLabel(start_frame)
        game_title.setAlignment(QtCore.Qt.AlignHCenter)
        game_title.setText("Hangman Game")
        title_font = QtGui.QFont()
        title_font.setFamily("Bahnschrift")
        title_font.setPointSize(40)
        title_font.setBold(True)
        title_font.setUnderline(True)
        game_title.setFont(title_font)
        game_title.adjustSize()
        game_title.move(int((self.width()-game_title.width())/2), 20)
        self.game_title = game_title

        background_image = QtWidgets.QLabel(start_frame)
        background_pixmap = QtGui.QPixmap("Images/start.png")
        background_image.setPixmap(background_pixmap)
        background_image.adjustSize()
        background_image.move(int((self.width()-background_image.width())/2), game_title.y()+game_title.height()+30)
        self.background_image = background_image

        start_button = QtWidgets.QPushButton(start_frame)
        start_button.setText("START GAME")
        start_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button_font = QtGui.QFont(title_font)
        button_font.setPointSize(20)
        start_button.setFont(button_font)
        start_button.setStyleSheet("background-color: none")
        start_button.resize(300, 80)
        start_button.move(int((self.width()-start_button.width())/2), int((self.height()-start_button.height())/2)+10)
        def next_page():
            self.start_frame.deleteLater()
            self.get_word()

        start_button.clicked.connect(next_page)
        self.start_button = start_button

        start_frame.show()


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

        dice_button = QtWidgets.QPushButton(get_word_frame)
        dice_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        dice_button.resize(50, 50)
        dice_button.move(textinput.x()+textinput.width()+20, textinput.y()+int((textinput.height()-dice_button.height())/2))
        dice_button.setIcon(QtGui.QIcon("Images/dice.png"))
        dice_button.setIconSize(QtCore.QSize(40, 40))

        with open("database.data", "r") as file:
            data = file.read()
        data = data.split("\n")

        def random_word():
            random_generated_word = random.choice(data)
            for _ in range(len(textinput.text())):
                key_event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Backspace, QtCore.Qt.NoModifier, 0, 0, 0)
                textinput.keyPressEvent(key_event)

            for letter in random_generated_word:
                key_event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, ord(letter), QtCore.Qt.NoModifier, 0, 0, 0, text=letter.upper())
                textinput.keyPressEvent(key_event)


        dice_button.clicked.connect(random_word)
        self.dice_button = dice_button


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
        def next_page():
            self.get_word_frame.deleteLater()
            self.word_guessing_page(textinput.text())
        next_button.clicked.connect(next_page)
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



    def word_guessing_page(self, word):
        self.word = word
        self.guessing_time = time.time()

        guess_word_frame = QtWidgets.QFrame(self)
        guess_word_frame.setGeometry(0, 0, self.width(), self.height())
        self.guess_word_frame = guess_word_frame

        title = QtWidgets.QLabel(guess_word_frame)
        title.setText("GUESS THE WORD!")
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(35)
        font.setBold(True)
        font.setUnderline(True)
        title.setFont(font)
        title.adjustSize()
        title.move(int((self.width() - title.width()) / 2), 30)
        self.guess_word_title = title

        word_widget = QtWidgets.QWidget(guess_word_frame)
        word_widget.setGeometry(0, int(self.height()/4), self.width(), 100)
        word_widget_layout = QtWidgets.QHBoxLayout()
        word_widget_layout.setAlignment(QtCore.Qt.AlignCenter)
        word_widget_layout.setSpacing(15)
        word_widget.setLayout(word_widget_layout)
        self.word_widget = word_widget

        label_font = QtGui.QFont(font)
        label_font.setPointSize(40)
        all_labels = {}
        for char in word:
            label = QtWidgets.QLabel()
            label.setText("  ")   #Two spaces
            label.setFont(label_font)
            word_widget_layout.addWidget(label)
            try:
                all_labels[char].append(label)
            except:
                all_labels[char] = [label]


        letters_widget = QtWidgets.QWidget(guess_word_frame)
        letters_widget.setGeometry(int(self.width()/2), int(self.height()/2), int(self.width()/2), int(self.height()/2))
        letters_widget_layout = QtWidgets.QGridLayout()
        letters_widget.setLayout(letters_widget_layout)
        self.letters_widget = letters_widget

        button_font = QtGui.QFont(label_font)
        button_font.setPointSize(20)
        button_font.setUnderline(False)
        column = 0
        row = 0

        self.wrong_guess = 0
        self.correct_letters = []
        def char_button_function(button):
            char = button.text()
            if char in word:
                for label in all_labels[char]:
                    label.setText(char)
                    self.correct_letters.append(char)
                del all_labels[char]

                if not all_labels:
                    self.guessing_time = round(time.time() - self.guessing_time, 0)
                    self.guess_word_frame.deleteLater()
                    self.end_page(True)

            else:
                if self.wrong_guess < 10:
                    self.wrong_guess += 1
                    pixmap = QtGui.QPixmap(f"Images/Hangman{self.wrong_guess}.png")
                    hangman_label.setPixmap(pixmap)
                    hangman_label.adjustSize()
                    hangman_label.move(self.hangman_spacing, self.height()-hangman_label.height()-self.hangman_spacing)
                    hangman_label.show()
                else:
                    self.wrong_guess += 1
                    pixmap = QtGui.QPixmap(f"Images/Hangman11.png")
                    hangman_label.setPixmap(pixmap)
                    hangman_label.adjustSize()

                    self.guessing_time = round(time.time() - self.guessing_time, 0)
                    self.guess_word_frame.deleteLater()
                    self.end_page(False)

            button.setDisabled(True)

        for char in string.ascii_uppercase:
            if column == 6:
                row += 1
                column = 0
            button = QtWidgets.QPushButton()
            button.setStyleSheet("background-color: none")
            button.setFixedSize(65, 65)
            button.setFont(button_font)
            button.setText(char)
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            button.clicked.connect(lambda b, btn=button: char_button_function(btn))  #'b' argument in lambda is for receiving boolean from .connect()
            if row == 4 and column == 0:
                column = 2
            letters_widget_layout.addWidget(button, row, column)
            column += 1


            hangman_label = QtWidgets.QLabel(guess_word_frame)
            hangman_label.setAlignment(QtCore.Qt.AlignBottom)
            hangman_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.hangman_spacing = 10
            self.hangman_label = hangman_label


        guess_word_frame.show()




    def end_page(self, win: bool, details=[]):
        end_frame = QtWidgets.QFrame(self)
        end_frame.setGeometry(0, 0, self.width(), self.height())
        self.end_frame = end_frame

        if win:
            image = "Images/victory.png"
        else:
            image = "Images/defeat.png"

        result_label = QtWidgets.QLabel(end_frame)
        result_label.setPixmap(QtGui.QPixmap(image))
        result_label.adjustSize()
        result_label.move(int((self.width()-result_label.width())/2), int((self.height()-result_label.height())/2))
        self.result_label = result_label

        details_label = QtWidgets.QLabel(end_frame)
        details_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        details_label.setAlignment(QtCore.Qt.AlignTop)
        details_label_font = QtGui.QFont()
        details_label_font.setFamily("Bahnschrift")
        details_label_font.setBold(True)
        details_label_font.setPointSize(17)
        details_label.setFont(details_label_font)
        details_label.setText(f"- Chosen word: {self.word}\n"
                              f"- You guessed {round((len(self.correct_letters)/len(self.word))*100, 2)}% of given word\n"
                              f"- You made {self.wrong_guess} / 11 mistakes\n"
                              f"- You were playing for: {int(self.guessing_time)} seconds")

        details_label.adjustSize()
        details_label.move(10, int(self.height()/1.7))
        self.details_label = details_label


        new_game_button = QtWidgets.QPushButton(end_frame)
        new_game_button.setStyleSheet("background-color: none")
        new_game_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_margin = 50
        new_game_button.resize(200, 50)
        new_game_button.move(int((details_label.width()-new_game_button.width())/2), details_label.y()+details_label.height()+self.button_margin)
        new_game_button_font = QtGui.QFont(details_label_font)
        new_game_button_font.setPointSize(20)
        new_game_button.setFont(new_game_button_font)
        new_game_button.setText("PLAY AGAIN")
        def new_game():
            self.end_frame.deleteLater()
            self.start_page()

        new_game_button.clicked.connect(new_game)
        self.new_game_button = new_game_button



        end_frame.show()







    def resizeEvent(self, event):
        try:
            self.game_title.move(int((self.width()-self.game_title.width())/2), 20)
            self.background_image.move(int((self.width() - self.background_image.width()) / 2), self.game_title.y() + self.game_title.height() + 30)
            self.start_button.move(int((self.width() - self.start_button.width()) / 2), self.start_button.y())
        except:
            pass

        try:
            self.get_word_frame.resize(self.width(), self.height())
            self.get_word_title.move(int((self.get_word_frame.width()-self.get_word_title.width())/2), 30)
            self.textinput.move(int((self.get_word_frame.width()-self.textinput.width())/2), int(self.get_word_frame.height()/4))
            self.dice_button.move(self.textinput.x() + self.textinput.width() + 20, self.textinput.y() + int((self.textinput.height() - self.dice_button.height()) / 2))

            self.letters_container.setGeometry(0, int(self.height()/1.9), self.width(), 150)
            self.char_alert.move(int((self.get_word_frame.width()-self.char_alert.width())/2), int(self.textinput.y()+self.textinput.height()+5))
            self.next_button.move(int((self.width() - self.next_button.width()) / 2), self.height() - self.next_button.height() - 20)
            self.char_alert_2.move(int((self.width() - self.char_alert_2.width()) / 2), self.next_button.y() - self.char_alert_2.height() - 5)
        except:
            pass

        try:
            self.guess_word_frame.resize(self.width(), self.height())
            self.guess_word_title.move(int((self.width() - self.guess_word_title.width()) / 2), 30)
            self.word_widget.setGeometry(0, int(self.height()/4), self.width(), 100)
            self.letters_widget.setGeometry(int(self.width()/2), int(self.height()/2), int(self.width()/2), int(self.height()/2))
            self.hangman_label.move(self.hangman_spacing, self.height()-self.hangman_label.height()-self.hangman_spacing)
        except:
            pass

        try:
            self.end_frame.resize(self.width(), self.height())
            self.result_label.move(int((self.width()-self.result_label.width())/2), int((self.height()-self.result_label.height())/2))
            self.details_label.move(10, int(self.height()/1.7))
            self.new_game_button.move(int((self.details_label.width()-self.new_game_button.width())/2), self.details_label.y()+self.details_label.height()+self.button_margin)

        except:
            pass

















if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Application()
    game.show()
    sys.exit(app.exec_())