import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from mainwindow import MainWindow

import resource

if __name__ == '__main__':
    app = QApplication([])
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
