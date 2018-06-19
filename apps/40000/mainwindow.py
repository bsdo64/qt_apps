from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QImage, QColor
from PyQt5.QtWidgets import QWidget, QSplitter, QGraphicsScene, QHBoxLayout

from chip import Chip
from view import View


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = QGraphicsScene()
        self.h1Splitter = QSplitter()
        self.h2Splitter = QSplitter()

        self._populate_scene()

        vSplitter = QSplitter()
        vSplitter.setOrientation(Qt.Vertical)
        vSplitter.addWidget(self.h1Splitter)
        vSplitter.addWidget(self.h2Splitter)

        view = View("Top left view")
        view.view().setScene(self.scene)
        self.h1Splitter.addWidget(view)

        view = View("Top right view")
        view.view().setScene(self.scene)
        self.h1Splitter.addWidget(view)

        view = View("Bottom left view")
        view.view().setScene(self.scene)
        self.h2Splitter.addWidget(view)

        view = View("Bottom right view")
        view.view().setScene(self.scene)
        self.h2Splitter.addWidget(view)

        layout = QHBoxLayout()
        layout.addWidget(vSplitter)
        self.setLayout(layout)

        self.setWindowTitle("Chip Example")

    def _setup_matrix(self):
        pass

    def _populate_scene(self):
        self.scene = QGraphicsScene(self)

        image = QImage(':/images/qt4logo.png')

        xx = 0
        for i in range(-10000, 11000, 110):
            xx += 1
            yy = 0
            for j in range(-7000, 7000, 70):
                yy += 1
                x = (i + 11000) / 22000.0
                y = (j + 7000) / 14000

                color = QColor(image.pixel(int(image.width() * x), int(image.height() * y)))
                item = Chip(color, xx, yy)
                item.setPos(QPointF(i, j))
                self.scene.addItem(item)



