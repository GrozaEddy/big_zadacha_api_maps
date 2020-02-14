import os
import sys
from PyQt5.QtCore import Qt
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [300, 300]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.x = 0
        self.y = 0
        self.image.resize(250, 250)
        self.image.move(25, 25)
        self.image.setPixmap(self.pixmap)

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
        if not response:
            print("Ошибка выполнения запроса:")
            print(self.map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.map_y += float(self.map_delta) * 250
        elif event.key() == Qt.Key_Down:
            self.map_y -= float(self.map_delta) * 250
        elif event.key() == Qt.Key_Left:
            self.map_x -= float(self.map_delta) * 250
        elif event.key() == Qt.Key_Right:
            self.map_x += float(self.map_delta) * 250
        print(self.map_x, self.map_y)
        self.params['ll'] = ','.join([str(self.map_x), str(self.map_y)])


    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
