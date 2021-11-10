import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QPushButton, QInputDialog,
                             QCheckBox, QScrollArea, QFormLayout, QHBoxLayout, QLabel)
from PyQt5 import uic
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtGui import QIcon
from sqlite3 import connect

towns = {'Абиджан': 2, 'Аддис-Абеба': 0, 'Аккра': 21, 'Актау': 2, 'Алжир': 22, 'Алма-Ата': 3,
         'Альбукерке': 15, 'Амман': 23, 'Амстердам': 22, 'Анадырь': 9, 'Андорра': 22, 'Анкара': 0,
         'Анкоридж': 13, 'Анн-Арбор': 17, 'Антанариву': 0, 'Антигуа': 17, 'Аруба': 17, 'Асмэра': 0,
         'Асунсьон': 18, 'Атланта': 17, 'Афины': 23, 'Ашхабад': 2, 'Багдад': 0, 'Баку': 1,
         'Балтимор': 17, 'Банги': 22, 'Бангкок': 4, 'Бандар-Сери-Бегаван': 5, 'Банжул': 21,
         'Барбадос': 17, 'Барселона': 22, 'Бахрейн': 0, 'Бейрут': 23, 'Белград': 22, 'Белиз': 15,
         'Белу-Оризонти': 18, 'Белфаст': 21, 'Берлин': 22, 'Бермудские острова': 18, 'Бисау': 21,
         'Бишкек': 3, 'Блантайр': 23, 'Блэк-Рок-Сити': 14, 'Богота': 16, 'Бойла': 16, 'Бостон': 17,
         'Боулдер': 15, 'Браззавиль': 22, 'Бразилиа': 18, 'Братислава': 22, 'Брисбен': 7,
         'Брюссель': 22, 'Будапешт': 22, 'Бужумбура': 23, 'Бухарест': 23, 'Буэнос-Айрес': 18,
         'Вадуц': 22, 'Ванкувер': 14, 'Варшава': 22, 'Ватикан': 22, 'Вашингтон': 17, 'Вавей': 17,
         'Вена': 22, 'Венсен': 17, 'Виктория': 8, 'Вильнюс': 23, 'Виндхук': 23, 'Виннипег': 16,
         'Вроцлав': 22, 'Вьентьян': 4, 'Габороне': 23, 'Гавана': 17, 'Газа': 23, 'Гайана': 17,
         'Галифакс': 18, 'Гамбург': 22, 'Гватемала': 15, 'Гибралтар': 22, 'Гонконг': 5,
         'Гонолулу': 11, 'Гранд-Терк': 17, 'Гренада': 17, 'Гуам': 7, 'Гуанчжоу': 5, 'Дакар': 17,
         'Дакка': 3, 'Даллас': 16, 'Дамаск': 23, 'Дар-эс-Салам': 0, 'Денвер': 15, 'Детройт': 17,
         'Джакарта': 4, 'Джибути': 0, 'Джуба': 0, 'Джэксонвилл': 17, 'Дили': 6, 'Доминика': 17,
         'Досон-Крик': 14, 'Доха': 0, 'Дубай': 1, 'Дублин': 21, 'Душанбе': 2, 'Ереван': 1,
         'Загреб': 22, 'Иерусалим': 23, 'Индианополис': 17, 'Исламабад': 2, 'Йоханнесбург': 23,
         'Кабо-Верде': 20, 'Каир': 23, 'Каймановы острова': 16, 'Калгари': 15, 'Кампала': 0,
         'Канарские острова': 21, 'Канберра': 8, 'Канкун': 16, 'Каракас': 17, 'Карачи': 2,
         'Касабланка': 22, 'Квинсленд': 7, 'Кейптаун': 23, 'Кембридж': 17, 'Кигали': 23,
         'Киев': 23, 'Кингстон': 16, 'Киншаса': 22, 'Киркленд': 14, 'Кито': 16, 'Кишинёв': 23,
         'Кливленд': 17, 'Колумбус': 17, 'Конакри': 21, 'Копенгаген': 22, 'Краков': 22,
         'Куала-Лумпур': 5, 'Кувейт': 0, 'Кюрасао': 17, 'Ла-Пас': 17, 'Лагос': 22, 'Лас-Вегас': 14,
         'Лахор': 2, 'Либревиль': 22, 'Лима': 16, 'Лиссабон': 21, 'Ломе': 21, 'Лонгйир': 22,
         'Лондон': 21, 'Лос-Анджелес': 14, 'Луанда': 22, 'Луисвилл': 17, 'Лусака': 23, 'Любляна': 22,
         'Люксембург': 22, 'Маврикий': 1, 'Маджуро': 9, 'Мадрид': 22, 'Майами': 17, 'Макао': 5,
         'Малабо': 22, 'Мальта': 22, 'Манагуа': 15, 'Манила': 5, 'Манчестер': 21, 'Мапуту': 23,
         'Маренго': 17, 'Мартиника': 17, 'Масеру': 23, 'Маскат': 1, 'Маунтин-Вью': 14, 'Мбабане': 23,
         'Мельбурн': 8, 'Мемфис': 16, 'Мендоса': 18, 'Метлакатла': 13, 'Мехико': 15, 'Милан': 22,
         'Милоуки': 16, 'Миннеаполис': 16, 'Минск': 0, 'Могадишо': 0, 'Монако': 22, 'Монреаль': 17,
         'Монровия': 21, 'Монтевидео': 18, 'Монтеррей': 15, 'Морони': 0, 'Москва': 0, 'Мэдисон': 16,
         'Мюнхен': 22, 'Найроби': 0, 'Нассау': 17, 'Нашвилл': 16, 'Нгерулмуд': 6, 'Нджамена': 22,
         'Ниамей': 22, 'Никосия': 23, 'Новый Орлеан': 16, 'Новый Южный Уэльс': 8, 'Нокс': 16,
         'Ноксвил': 17, 'Нуакшот': 21, 'Нукуалофа': 10, 'Нумеа': 8, 'Нью-Йорк': 17, 'Нью-Селейм': 16,
         'Оклахома-Сити': 16, 'Окленд': 10, 'Осака': 6, 'Осло': 22, 'Остин': 16, 'Остров Мэн': 21,
         'Остров Пасхи': 16, 'Остров Рождества': 11, 'Оттава': 17, 'Оулу': 23, 'Паликир': 8,
         'Панама': 16, 'Парамарибо': 18, 'Париж': 22, 'Пекин': 5, 'Перт': 5, 'Питерсберг': 17,
         'Питтсбург': 17, 'Пномпень': 4, 'Подгорица': 22, 'Порт-Вила': 8, 'Порт-Морсби': 6,
         'Порт-о-Пренс': 17, 'Порт-оф-Спейн': 17, 'Портленд': 14, 'Порто-Ново': 22, 'Прага': 22,
         'Приштина': 22, 'Пуэрто-Рико': 17, 'Пхеньян': 6, 'Рейкьявик': 21, 'Рестон': 17, 'Рига': 23,
         'Рим': 22, 'Рино': 14, 'Рио-де-Жанейро': 18, 'Розо': 17, 'Сакраменто': 14, 'Сальводор': 15,
         'Сан-Антонио': 16, 'Сан-Диего': 14, 'Сан-Марино': 22, 'Сан-Паулу': 18, 'Сан-Сальвадор': 15,
         'Сан-Томе': 21, 'Сан-Франциско': 14, 'Сан-Хосе': 14, 'Сан-Хуан': 17, 'Сана': 0,
         'Санкт-Петербург': 0, 'Санто-Доминго': 17, 'Сантьяго': 18, 'Сарево': 22, 'Саскачеван': 15,
         'Сент-Китс': 17, 'Сент-Луис': 16, 'Сент-Люсия': 17, 'Сент-Томас': 17, 'Сентер': 16,
         'Сеул': 6, 'Сидней': 8, 'Симферополь': 0, 'Сингапур': 5, 'Сиэтл': 14, 'Скопье': 22,
         'Солт-Лейк-Сити': 15, 'София': 23, 'Стамбул': 0, 'Стокгольм': 22, 'Стэнли': 14, 'Тайбэй': 5,
         'Таллин': 23, 'Тампа': 17, 'Ташкент': 2, 'Тбилиси': 1, 'Тегусигальпа': 17, 'Телл-Сити': 17,
         'Тель-Авив': 23, 'Тирана': 22, 'Тихуана': 14, 'Токио': 6, 'Томбукту': 21, 'Торонто': 17,
         'Триполи': 23, 'Тунис': 22, 'Тусон': 14, 'Тхимпху': 3, 'Уагадугу': 21, 'Уинамак': 17,
         'Улан-Батор': 5, 'Фиджи': 9, 'Филадельфия': 17, 'Филипсбург': 17, 'Финикс': 14,
         'Форталеза': 18, 'Франкфурт-на-Майне': 22, 'Фритаун': 21, 'Фунафути': 9, 'Хайфа': 23,
         'Ханой': 4, 'Хараре': 23, 'Хартум': 23, 'Хеврон': 23, 'Хельсинки': 23, 'Хониара': 8,
         'Хошимин': 4, 'Хьюстон': 16, 'Цинциннати': 17, 'Цюрих': 22, 'Чикаго': 16, 'Чиуауа': 14,
         'Шанхай': 5, 'Эдмонтон': 15, 'Эр-Рияд': 0, 'Южный полюс': 10, 'Ярен': 9, 'Яунде': 22,
}


class AddClock(QWidget):
    def __init__(self, added_towns: list[str], main_window):
        super(AddClock, self).__init__()
        uic.loadUi(r'..\ui_files\add_clock.ui', self)
        self.added_towns = added_towns
        self.main_window = main_window
        self.center()
        self.initUI()

    def initUI(self):
        self.setStyleSheet('background-color: #192480;')

        self.come_back.setIcon(QIcon(r'..\images\come_back.jpg'))
        self.come_back.clicked.connect(self.come_back_clicked)

        self.town_list = list()

        self.scroll_layout = QFormLayout()

        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.scroll_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.verticalScrollBar().setStyleSheet('QScrollBar:vertical{'
                                                           '    background-color: grey;'
                                                           '}'
                                                           'QScrollBar::handle:vertical{'
                                                           '    background-color: white;'
                                                           '}')
        self.scroll_area.setStyleSheet('border: 0px')
        self.scroll_area.setWidget(self.scroll_widget)

        self.towns.addWidget(self.scroll_area)

        for i, town in enumerate(towns):
            check_box = QCheckBox(town, self)
            check_box.setChecked(town in self.added_towns)
            check_box.setStyleSheet('color: grey; font: 14pt')
            self.scroll_layout.addWidget(check_box)
            self.town_list.append(check_box)

    def come_back_clicked(self):
        self.main_window.clock_list_changed([self.town_list[i].text() for i in range(len(towns))
                                            if self.town_list[i].isChecked()])

        self.close()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())


class Clock(QWidget):
    def __init__(self):
        super(Clock, self).__init__()
        uic.loadUi(r'..\ui_files\clock.ui', self)
        self.center()
        self.initUI()

    def initUI(self):
        self.setStyleSheet('background-color: #192480;')

        self.con = connect(r'..\data\clocks_db.sqlite')
        self.cur = self.con.cursor()

        self.added_towns = [town[0] for town in
                            self.cur.execute('SELECT title FROM added_towns').fetchall()]

        self.current_time.setText(QTime.currentTime().toString('hh:mm'))
        self.current_time.setStyleSheet('color: grey')

        timer = QTimer(self)
        timer.timeout.connect(self.check_time)
        timer.start(1000)

        self.add_clock = QPushButton(self)
        self.add_clock.move(150, 860)
        self.add_clock.resize(40, 40)
        self.add_clock.setIcon(QIcon('C:/not_clock/images/add.jpg'))
        self.add_clock.setStyleSheet('border: none; min-width: 40px; max-width: 40px;'
                                     'min-height: 40px; max-height: 40px; border-radius: 20px;'
                                     'background-color: red;')
        self.add_clock.clicked.connect(self.add_clock_clicked)

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

        self.clocks.addWidget(self.scroll_area)

        self.clock_list_changed(self.added_towns)

    def add_clock_clicked(self):
        self.add_clock_window = AddClock(self.added_towns, self)
        self.add_clock_window.show()

    def clock_list_changed(self, added_towns: list[str]):
        self.added_towns = added_towns
        self.time_set = set()

        current_time = self.current_time.text().split(':')
        current_time[0] = int(current_time[0])

        while self.scroll_layout.count():
            self.scroll_layout.itemAt(0).widget().setParent(None)

        for town in added_towns:
            town_time = QHBoxLayout()
            town_label = QLabel(town)
            town_label.setStyleSheet('color: grey; font: 16pt')
            town_time.addWidget(town_label, Qt.AlignLeft)
            time_label = QLabel(str((current_time[0] + towns[town]) % 24).zfill(2) +
                                f':{current_time[1]}')
            time_label.setStyleSheet('color: grey; font: 16pt')
            time_label.setMaximumWidth(50)
            town_time.addWidget(time_label, Qt.AlignRight)

            clock = QWidget()
            clock.setLayout(town_time)
            self.scroll_layout.addWidget(clock)

            self.time_set.add(time_label)

    def check_time(self):
        current_time = QTime.currentTime().toString('hh:mm')
        if current_time != self.current_time.text():
            self.current_time.setText(current_time)

            if current_time[3:] == '00':
                for time in self.time_set:
                    time.setText(str((int(time.text()[:2]) + 1) % 24).zfill(2) + ':00')
            else:
                for time in self.time_set:
                    time.setText(time.text()[:2] + current_time[2:])

    def closeEvent(self, a0):
        self.cur.execute('DELETE FROM added_towns')
        for town in self.added_towns:
            self.cur.execute(f'INSERT INTO added_towns(title) VALUES ("{town}")')
        self.con.commit()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())


def start():
    app = QApplication(sys.argv)
    clock = Clock()
    clock.show()
    sys.exit(app.exec_())

start()