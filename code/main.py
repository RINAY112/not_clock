import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QVBoxLayout
from clock import Clock
from alarm_clock import AlarmClock
from timer import Timer
from stopwatch import Stopwatch


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet('background-color: rgb(25, 36, 128);')
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(Clock())
        self.resize(360, 923)
        self.center()

    def open_other_window(self, open_widget: str):
        while self.layout().count():
            self.layout().itemAt(0).widget().setParent(None)
        if open_widget == 'open_clock':
            self.layout().addWidget(Clock(self))
        elif open_widget == 'open_timer':
            self.layout().addWidget(Timer(self))
        elif open_widget == 'open_alarm_clock':
            self.layout().addWidget(AlarmClock(self))
        else:
            self.layout().addWidget(Stopwatch(self))

    def closeEvent(self, a0):
        self.layout().itemAt(0).widget().close()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())