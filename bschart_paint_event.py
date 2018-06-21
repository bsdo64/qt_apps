from PyQt5.QtWidgets import QApplication, QGraphicsView, QMainWindow, QHBoxLayout, QPushButton, QWidget, QGraphicsScene
import numpy as np
import pandas as pd


class PlotScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)


class Window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setup_ui()

    def setup_ui(self):
        self.layout = QHBoxLayout()

        scene = PlotScene()
        view = QGraphicsView(scene)

        button = QPushButton()
        button.setText('import')
        self.layout.addWidget(view)
        self.layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)


if __name__ == '__main__':
    app = QApplication([])

    win = Window()
    df = pd.read_pickle('bitmex_1m_2018.pkl')

    df['timestamp'] = df['timestamp'].astype('datetime64[ns]')

    df.to_feather('bitmex_1m_2018.feather')

    df = pd.read_feather('bitmex_1m_2018.feather')

    print(df.dtypes)

    win.show()

    app.exec_()