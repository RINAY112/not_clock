import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton
from PyQt5.QtCore import QTimer, QTime, QSize
from PyQt5.QtGui import QIcon
from PyQt5 import uic


class Stopwatch(QWidget):
    def __init__(self, parent=None):
        super(Stopwatch, self).__init__(parent)
        uic.loadUi(r'..\ui_files\stopwatch.ui', self)
        self.center()
        self.initUI()

    def initUI(self):
        self.setStyleSheet('background-color: #192480;')

        self.time.setReadOnly(True)
        self.time.setStyleSheet('border: none; color: grey;')

        self.timer = QTimer()
        self.timer.timeout.connect(self.show_time)

        for name in ('clock', 'alarm_clock', 'timer', 'stopwatch'):
            exec(rf"self.open_{name}.setIcon(QIcon(r'..\images\{name}.jpg'))")
            exec(f"self.open_{name}.setStyleSheet('border: none;')")
            exec(f"self.open_{name}.setIconSize(QSize(81, 61))")
            exec(f'self.open_{name}.clicked.connect(self.open_other_window)')

        self.icons = [QIcon(r'..\images\stop.jpg'), QIcon(r'..\images\start.jpg')]
        self.current_icon = True

        self.start_stop = QPushButton(self)
        self.start_stop.move(133, 860)
        self.start_stop.resize(40, 40)
        self.start_stop.setIcon(self.icons[1])
        self.start_stop.setStyleSheet('border: none; min-width: 40px; max-width: 40px;'
                                      'min-height: 40px; max-height: 40px; border-radius: 20px;'
                                      'background-color: red;')
        self.start_stop.clicked.connect(self.start_stop_timer)

        self.terminate = QPushButton(self)
        self.terminate.move(177, 860)
        self.terminate.resize(40, 40)
        self.terminate.setIcon(QIcon(r'../images/terminate.jpg'))
        self.terminate.setStyleSheet('border: none; min-width: 40px; max-width: 40px;'
                                     'min-height: 40px; max-height: 40px; border-radius: 20px;'
                                     'background-color: red;')
        self.terminate.clicked.connect(self.terminate_timer)

    def open_other_window(self):
        sender = self.sender().objectName()
        if sender != 'open_stopwatch':
            self.close()
            self.parent().open_other_window(sender)

    def start_stop_timer(self):
        if self.current_icon:
            self.timer.start(1000)
        else:
            self.timer.stop()
        self.current_icon = not self.current_icon
        self.start_stop.setIcon(self.icons[self.current_icon])

    def terminate_timer(self):
        self.time.setTime(QTime(0, 0, 0))
        if not self.current_icon:
            self.start_stop_timer()

    def show_time(self):
        self.time.setTime(self.time.time().addSecs(1))

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())