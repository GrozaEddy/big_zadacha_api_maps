import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        self.map_request = "http://static-maps.yandex.ru/1.x/"
        self.map_x, self.map_y = '37.530887', '55.703118'
        self.map_delta = '0.002'
        self.map_type = 'map'
        self.params = {'ll': ','.join([self.map_x, self.map_y]),
                       'spn': ','.join([self.map_delta, self.map_delta]),
                       'l': self.map_type
                       }
        response = requests.get(self.map_request, params=self.params)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.map_delta = str(float(self.map_delta) + 0.002)
        elif event.key() == Qt.Key_PageDown and float(self.map_delta) > 0.002:
            self.map_delta = str(float(self.map_delta) - 0.002)
        self.params['spn'] = ','.join([self.map_delta, self.map_delta])
        response = requests.get(self.map_request, params=self.params)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        os.remove(self.map_file)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
