from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QToolBar

from widgets import BSChart


if __name__ == '__main__':
    app = QApplication([])
    win = QMainWindow()
    win.resize(640, 480)

    test_layout = QHBoxLayout()

    bs_chart = BSChart(win)
    win.setCentralWidget(bs_chart)

    win.addToolBar(QToolBar())
    win.show()
    app.exec_()
