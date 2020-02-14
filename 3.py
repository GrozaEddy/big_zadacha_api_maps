import os
from sys import argv

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        self.map_request = "http://static-maps.yandex.ru/1.x/"
        self.map_x, self.map_y = 37.530887, 55.703118
        self.map_delta = '0.002'
        self.map_type = 'map'
        self.params = {'ll': ','.join([str(self.map_x), str(self.map_y)]),
                       'spn': ','.join([self.map_delta, self.map_delta]),
                       'l': self.map_type
                       }
        response = requests.get(self.map_request, params=self.params)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap(self.map_file)
        os.remove(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.setPixmap(self.pixmap)

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
        self.params['ll'] = ','.join([str(self.map_x), str(self.map_y)])
        self.params['spn'] = ','.join([self.map_delta, self.map_delta])
        response = requests.get(self.map_request, params=self.params)
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        os.remove(self.map_file)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(argv)
    ex = Example()
    ex.show()
    exit(app.exec())
