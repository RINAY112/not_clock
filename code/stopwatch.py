import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton


class Stopwatch(QWidget):
    def __init__(self):
        pass

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())


app = QApplication(sys.argv)
clock = Stopwatch()
clock.show()
sys.exit(app.exec_())