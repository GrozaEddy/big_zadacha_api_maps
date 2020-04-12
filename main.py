import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

from mainForm import UiMainWindow


class Example(QMainWindow, UiMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.pushButton.clicked.connect(self.map_chng)

    def initUI(self):
        self.dest_num = 1
        self.dest_list = [0.002, 0.005, 0.02, 0.05, 0.1, 0.3, 0.5, 1, 3, 5, 11, 15, 40]
        self.shir_ch = 37
        self.dol_ch = 55
        self.map = 'map'
        self.run_start()

    def map_chng(self):
        if self.map == 'map':
            self.map = 'sat'
        elif self.map == 'sat':
            self.map = 'skl'
        elif self.map == 'skl':
            self.map = 'map'
        self.run_start()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.dest_num < len(self.dest_list) - 1:
                self.dest_num += 1
            self.run_start()
        elif event.key() == Qt.Key_PageDown:
            if self.dest_num >= 1:
                self.dest_num -= 1
            self.run_start()
        elif event.key() == Qt.Key_Up:
            self.dol_ch += self.dest_list[self.dest_num]
            self.run_start()
        elif event.key() == Qt.Key_Down:
            self.dol_ch -= self.dest_list[self.dest_num]
            self.run_start()
        elif event.key() == Qt.Key_Right:
            self.shir_ch += self.dest_list[self.dest_num]
            self.run_start()
        elif event.key() == Qt.Key_Left:
            self.shir_ch -= self.dest_list[self.dest_num]
            self.run_start()

    def run_start(self):
        try:
            self.our_map.setFocus()
            dest = self.dest_list[self.dest_num]
            map_request = f"http://static-maps.yandex.ru/1.x/?" \
                          f"ll={self.shir_ch},{self.dol_ch}&spn" \
                          f"={dest},{dest}&l={self.map}&size=650,450"
            response = requests.get(map_request)
            if self.map == 'sat':
                self.map_file = "map.jpg"
            else:
                self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                if 'error' in str(response.content):
                    return
                file.write(response.content)
            self.pixmap = QPixmap(self.map_file)
            self.our_map.setPixmap(self.pixmap)
        except Exception:
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
