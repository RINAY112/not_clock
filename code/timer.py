import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from plyer import notification


class Timer(QWidget):
    def __init__(self):
        super(Timer, self).__init__()
        uic.loadUi(r'..\ui_files\timer.ui', self)
        self.center()
        self.initUI()

    def initUI(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_time)

        self.setStyleSheet('background-color: #192480;')
        self.time.setStyleSheet('color: grey; border: none;')

        self.icons = [QIcon(r'..\images\stop.jpg'), QIcon(r'..\images\start.jpg')]
        self.current_icon = True

        self.start_stop = QPushButton(self)
        self.start_stop.move(150, 860)
        self.start_stop.resize(40, 40)
        self.start_stop.setIcon(self.icons[1])
        self.start_stop.setStyleSheet('border: none; min-width: 40px; max-width: 40px;'
                                      'min-height: 40px; max-height: 40px; border-radius: 20px;'
                                      'background-color: red;')
        self.start_stop.clicked.connect(self.start_stop_timer)

        self.toast = notification

    def show_time(self):
        if self.time.text() != '00:00:00':
            self.time.setTime(self.time.time().addSecs(-1))
        else:
            self.toast.notify(title='Дззззиииинь-Дзззиинь', message='Таймер сработал', timeout=10)
            self.start_stop_timer()

    def start_stop_timer(self):
        if self.current_icon:
            self.timer.start(1000)
        else:
            self.timer.stop()
        self.current_icon = not self.current_icon
        self.start_stop.setIcon(self.icons[self.current_icon])

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())


app = QApplication(sys.argv)
clock = Timer()
clock.show()
sys.exit(app.exec_())