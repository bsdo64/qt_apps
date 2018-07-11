from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QHBoxLayout, QToolBar, QPushButton)

from widgets import BSChart


if __name__ == '__main__':
    app = QApplication([])
    win = QMainWindow()
    win.resize(640, 480)

    test_layout = QHBoxLayout()

    bs_chart = BSChart(win)
    win.setCentralWidget(bs_chart)

    toolbar = QToolBar()
    btn_add_pane = QPushButton('add')
    btn_del_pane = QPushButton('del')
    btn_add_pane.clicked.connect(bs_chart.layout.add_pane)
    btn_del_pane.clicked.connect(bs_chart.layout.del_last_pane)
    toolbar.addWidget(btn_add_pane)
    toolbar.addWidget(btn_del_pane)
    win.addToolBar(toolbar)
    win.show()
    app.exec_()
