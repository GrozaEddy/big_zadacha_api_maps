import os
from sys import argv

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox

SCREEN_SIZE = [700, 580]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.map_request = "http://static-maps.yandex.ru/1.x/"
        self.map_x, self.map_y = 37.530887, 55.703118
        self.map_delta = '0.002'
        self.map_type = 'map'
        self.params = {'ll': ','.join([str(self.map_x), str(self.map_y)]),
                       'spn': ','.join([self.map_delta, self.map_delta]),
                       'l': self.map_type
                       }
        self.map_file = "map."
        self.format = 'png'
        self.image = QLabel(self)
        self.text = QLineEdit(self)
        self.address = QLabel(self)
        self.button_map = QPushButton('map', self)
        self.button_sat = QPushButton('sat', self)
        self.button_skl = QPushButton('skl', self)
        self.button_seek = QPushButton('Искать', self)
        self.button_search = QPushButton('Поиск', self)
        self.button_reset = QPushButton('Сброс', self)
        self.index = QCheckBox('Индекс', self)
        response = requests.get(self.map_request, params=self.params)
        with open(self.map_file + self.format, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file + self.format)
        os.remove(self.map_file + self.format)
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.button_map.clicked.connect(self.change_map)
        self.button_sat.clicked.connect(self.change_map)
        self.button_skl.clicked.connect(self.change_map)
        self.button_map.resize(70, 50)
        self.button_sat.resize(70, 50)
        self.button_skl.resize(70, 50)
        self.button_map.move(620, 30)
        self.button_sat.move(620, 90)
        self.button_skl.move(620, 150)
        self.image.move(0, 0)
        self.image.setPixmap(self.pixmap)
        self.text.move(50, 460)
        self.text.resize(350, 30)
        self.text.hide()
        self.index.move(270, 460)
        self.index.resize(100, 30)
        self.index.stateChanged.connect(self.add_index)
        self.button_seek.move(450, 460)
        self.button_seek.resize(100, 30)
        self.button_seek.clicked.connect(self.seek)
        self.button_seek.hide()
        self.button_search.move(140, 460)
        self.button_search.resize(100, 30)
        self.button_search.clicked.connect(self.search)
        self.button_reset.move(360, 460)
        self.button_reset.resize(100, 30)
        self.button_reset.clicked.connect(self.reset)
        self.address.setWordWrap(True)
        self.address.move(50, 500)
        self.address.resize(500, 50)
        self.address.setWordWrap(True)
        font = QFont()
        font.setPointSize(10)
        self.address.setFont(font)
        self.image.setFocus()

    def change_map(self):
        if self.sender().text() == 'map':
            self.map_type = 'map'
            self.format = 'png'
        elif self.sender().text() == 'sat':
            self.map_type = 'sat'
            self.format = 'jpg'
        elif self.sender().text() == 'skl':
            self.map_type = 'skl'
            self.format = 'png'
        self.params['l'] = self.map_type
        self.params['ll'] = ','.join([str(self.map_x), str(self.map_y)])
        self.params['spn'] = ','.join([self.map_delta, self.map_delta])
        response = requests.get(self.map_request, params=self.params)
        with open(self.map_file + self.format, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file + self.format)
        os.remove(self.map_file + self.format)
        self.image.setPixmap(self.pixmap)

    def add_index(self, state):
        try:
            self.address.setText(self.geocode["metaDataProperty"]["GeocoderMetaData"]["text"])
            if state == Qt.Checked:
                self.address.setText(self.address.text() + ' | ' + self.geocode["metaDataProperty"][
                    "GeocoderMetaData"]["Address"]["postal_code"])
        except Exception:
            self.index.setCheckState(False)
        self.image.setFocus()

    def reset(self):
        self.map_x, self.map_y = 37.530887, 55.703118
        self.map_delta = '0.002'
        self.map_type = 'map'
        self.params = {'ll': ','.join([str(self.map_x), str(self.map_y)]),
                       'spn': ','.join([self.map_delta, self.map_delta]),
                       'l': self.map_type
                       }
        self.map_file = 'map'
        self.format = 'png'
        response = requests.get(self.map_request, params=self.params)
        with open(self.map_file + self.format, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file + self.format)
        os.remove(self.map_file + self.format)
        self.address.setText('')

    def search(self):
        self.button_search.hide()
        self.button_reset.hide()
        self.index.hide()
        self.text.show()
        self.button_seek.show()

    def seek(self):
        try:
            params = {'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                      'geocode': self.text.text(),
                      'format': 'json'
                      }
            self.geocode = requests.get("http://geocode-maps.yandex.ru/1.x/", params=params).json()
            self.geocode = self.geocode["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]
            self.map_x, self.map_y = map(float, self.geocode["Point"]["pos"].split())
            self.params['ll'] = ','.join([str(self.map_x), str(self.map_y)])
            self.params['pt'] = ','.join([str(self.map_x), str(self.map_y), 'flag'])
            self.address.setText(self.geocode["metaDataProperty"]["GeocoderMetaData"]["text"])
            if self.index.checkState():
                self.address.setText(self.address.text() + '|' + self.geocode["metaDataProperty"][
                    "GeocoderMetaData"]["Address"]["postal_code"])
                response = requests.get(self.map_request, params=self.params)
                with open(self.map_file + self.format, "wb") as file:
                    file.write(response.content)
                self.pixmap = QPixmap(self.map_file + self.format)
                os.remove(self.map_file + self.format)
                self.image.setPixmap(self.pixmap)
            else:
                response = requests.get(self.map_request, params=self.params)
                with open(self.map_file + self.format, "wb") as file:
                    file.write(response.content)
                self.pixmap = QPixmap(self.map_file + self.format)
                os.remove(self.map_file + self.format)
                self.image.setPixmap(self.pixmap)
        except Exception:
            pass
        self.text.clear()
        self.text.hide()
        self.index.show()
        self.button_seek.hide()
        self.button_search.show()
        self.button_reset.show()
        self.image.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and float(self.map_delta) < 0.01:
            self.map_delta = str(float(self.map_delta) + 0.001)
        elif event.key() == Qt.Key_PageDown and float(self.map_delta) > 0.001:
            self.map_delta = str(float(self.map_delta) - 0.001)
        elif event.key() == Qt.Key_Up:
            self.map_y += float(self.map_delta)
        elif event.key() == Qt.Key_Down:
            self.map_y -= float(self.map_delta)
        elif event.key() == Qt.Key_Left:
            self.map_x -= float(self.map_delta)
        elif event.key() == Qt.Key_Right:
            self.map_x += float(self.map_delta)
        self.params['l'] = self.map_type
        self.params['ll'] = ','.join([str(self.map_x), str(self.map_y)])
        self.params['spn'] = ','.join([self.map_delta, self.map_delta])
        response = requests.get(self.map_request, params=self.params)
        with open(self.map_file + self.format, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file + self.format)
        os.remove(self.map_file + self.format)
        self.image.setPixmap(self.pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.image.move(600 - event.x(), 600 - event.y())
            self.params['ll'] = ','.join([str(self.map_x), str(self.map_y)])
            self.params['pt'] = ','.join([str(self.map_x), str(self.map_y), 'flag'])
            response = requests.get(self.map_request, params=self.params)
            with open(self.map_file + self.format, "wb") as file:
                file.write(response.content)
            self.pixmap = QPixmap(self.map_file + self.format)
            os.remove(self.map_file + self.format)
            self.initUI()


if __name__ == '__main__':
    app = QApplication(argv)
    ex = Example()
    ex.show()
    exit(app.exec())
