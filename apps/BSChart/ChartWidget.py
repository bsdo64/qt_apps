from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QGraphicsView, QWidget, QGraphicsScene, QSplitter, QMainWindow, QPushButton, \
    QHBoxLayout, QSizePolicy, QVBoxLayout, QFrame


class ChartScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)


class ChartView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 0)
        # self.setFrameStyle(QFrame.NoFrame)

        scene = ChartScene()
        scene.addRect(0, 0, 100, 100)
        scene.addRect(100, 100, 100, 100)
        scene.addRect(500, 500, 100, 100)
        scene.addRect(640, 480, 100, 100)
        self.setScene(scene)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        super().wheelEvent(event)
        # print(event.angleDelta())


class ChartAxisView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.setFixedWidth(56)
        # self.setFrameStyle(QFrame.NoFrame)
        # self.setStyleSheet("""
        #     QGraphicsView { border: 1px solid black }
        # """)


class ChartPane:
    def __init__(self, chart, axis):
        self.chart = chart
        self.axis = axis

    def create(self):
        widget = QWidget()
        hbox = QHBoxLayout()
        hbox.addWidget(self.chart)
        hbox.addWidget(self.axis)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        widget.setLayout(hbox)
        return widget


class ChartLayoutManager:
    def __init__(self):
        self.panes = [ChartPane(ChartView(), ChartAxisView())]

    def add_pane(self, pane):
        self.panes.append(pane)


class BSChart(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.layout_manager = ChartLayoutManager()
        vbox = QVBoxLayout(self)
        vbox.setSpacing(1)
        vbox.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Vertical)
        splitter.setHandleWidth(2)

        splitter.addWidget(ChartPane(ChartView(), ChartAxisView()).create())
        splitter.addWidget(ChartView())

        vbox.addWidget(splitter)


if __name__ == '__main__':
    app = QApplication([])
    win = QMainWindow()
    win.resize(640, 480)
    win.setCentralWidget(BSChart(win))
    win.show()
    app.exec_()