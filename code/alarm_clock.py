import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QPushButton, QCheckBox,
                             QFormLayout, QScrollArea, QHBoxLayout)
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QTime, QSize
from PyQt5.QtGui import QIcon
from sqlite3 import connect
from plyer import notification


class GetTime(QWidget):
    def __init__(self, parent):
        super(GetTime, self).__init__()
        uic.loadUi(r'..\ui_files\get_time.ui', self)
        self.parent = parent
        self.center()
        self.initUI()

    def initUI(self):
        self.ok.setStyleSheet('border: none; color: red; font: 18pt;')
        self.ok.clicked.connect(self.ok_clicked)

        self.time.setStyleSheet('border: none; color: grey; font: 24pt;')

        self.setStyleSheet('background-color: #192480;')

    def ok_clicked(self):
        self.parent.added_alarm_clocks[self.time.text()] = 1
        self.parent.time_list_changed(self)

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())


class AlarmClock(QWidget):
    def __init__(self, parent=None):
        super(AlarmClock, self).__init__(parent)
        uic.loadUi(r'..\ui_files\alarm_clock.ui', self)
        self.center()
        self.initUI()

    def initUI(self):
        self.setStyleSheet('background-color: #192480;')

        for name in ('clock', 'alarm_clock', 'timer', 'stopwatch'):
            exec(rf"self.open_{name}.setIcon(QIcon(r'..\images\{name}.jpg'))")
            exec(f"self.open_{name}.setStyleSheet('border: none;')")
            exec(f"self.open_{name}.setIconSize(QSize(81, 61))")
            exec(f'self.open_{name}.clicked.connect(self.open_other_window)')
        
        self.toast = notification

        self.con = connect(r'..\data\alarm_clocks_db.sqlite')
        self.cur = self.con.cursor()

        self.added_alarm_clocks = dict(self.cur.execute('SELECT time, is_enable '
                                                    'FROM alarm_clocks').fetchall())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_time)
        self.timer.start(1000)

        self.current_time = QTime.currentTime()

        self.add_alarm_clock = QPushButton(self)
        self.add_alarm_clock.move(150, 860)
        self.add_alarm_clock.resize(40, 40)
        self.add_alarm_clock.setIcon(QIcon('C:/not_clock/images/add.jpg'))
        self.add_alarm_clock.setStyleSheet('border: none; min-width: 40px; max-width: 40px;'
                                           'min-height: 40px; max-height: 40px; border-radius: 20px;'
                                           'background-color: red;')
        self.add_alarm_clock.clicked.connect(self.add_alarm_clock_clicked)

        self.scroll_layout = QFormLayout()

        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.scroll_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.verticalScrollBar().setStyleSheet('QScrollBar:vertical{'
                                                           '    background-color: grey;'
                                                           '    border-radius: 0px'
                                                           '}'
                                                           'QScrollBar::handle:vertical{'
                                                           '    background-color: white;'
                                                           '}')
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setStyleSheet('border: 0px')
        self.scroll_area.horizontalScrollBar().close()

        self.alarm_clocks.addWidget(self.scroll_area)

        self.time_list_changed()

    def add_alarm_clock_clicked(self):
        self.dlg = GetTime(self)
        self.dlg.show()

    def open_other_window(self):
        sender = self.sender().objectName()
        if sender != 'open_alarm_clock':
            self.close()
            self.parent().open_other_window(sender)

    def check_time(self):
        current_time = QTime.currentTime().toString('hh:mm')
        if current_time != self.current_time:
            self.current_time = current_time
            for widget in self.alarm_clock_list.values():
                time = widget.layout().itemAt(0).widget()
                if time.isChecked() and time.text() == current_time:
                    time.setChecked(False)
                    self.toast.notify(title='Дррриииинь-Дрррриинь',
                                      message='Будильник сработал',
                                      timeout=10)

    def time_list_changed(self, add_time_window=None):
        if add_time_window is not None:
            add_time_window.close()
        self.alarm_clock_list = dict()

        while self.scroll_layout.count():
            self.scroll_layout.itemAt(0).widget().setParent(None)

        for time, is_checked in self.added_alarm_clocks.items():
            alarm_clock = QHBoxLayout()
            time = QCheckBox(time)
            time.setStyleSheet(r'QCheckBox::indicator:unchecked {'
                               r'   image: url(../images/switch_off.jpg);'
                               r'}'
                               r'QCheckBox::indicator:checked {'
                               r'   image: url(../images/switch_on.jpg);'
                               r'}'
                               r'QCheckBox {'
                               r'   color: grey;'
                               r'   font: 17pt;'
                               r'}')
            time.clicked.connect(self.checked_changed)
            time.setChecked(is_checked)
            alarm_clock.addWidget(time)

            delete = QPushButton()
            delete.setMaximumWidth(30)
            delete.setIcon(QIcon(r'..\images\delete.jpg'))
            delete.clicked.connect(self.delete_alarm_clock)

            alarm_clock.addWidget(delete)
            widget = QWidget()
            widget.setLayout(alarm_clock)

            self.scroll_layout.addWidget(widget)

            self.alarm_clock_list[delete] = widget

    def closeEvent(self, a0):
        self.cur.execute('DELETE FROM alarm_clocks')
        for id, widget in enumerate(self.alarm_clock_list.values(), 1):
            time = widget.layout().itemAt(0).widget()
            self.cur.execute(f'INSERT INTO alarm_clocks VALUES ({id}, "{time.text()}",'
                             f' {int(time.isChecked())})')

        self.con.commit()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())

    def checked_changed(self):
        self.added_alarm_clocks[self.sender().text()] = self.sender().isChecked()

    def delete_alarm_clock(self):
        widget = self.alarm_clock_list[self.sender()]
        del self.added_alarm_clocks[widget.layout().itemAt(0).widget().text()]
        widget.setParent(None)
        del self.alarm_clock_list[self.sender()]