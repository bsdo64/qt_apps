import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Worker(QtCore.QThread):
    message = QtCore.pyqtSignal(object)

    def run(self):
        batch = []
        for index in range(50000):
            if len(batch) < 200:
                batch.append(index)
                continue
            self.message.emit(batch)
            batch = []


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setUniformItemSizes(True)
        self.button = QtWidgets.QPushButton('Start')
        self.button.clicked.connect(self.handleButton)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.listWidget)
        layout.addWidget(self.button)
        self.worker = Worker()
        self.worker.message.connect(self.handleMessages)

    def handleMessages(self, batch):
        for message in batch:
            self.listWidget.addItem('Item (%s)' % message)

    def handleButton(self):
        if not self.worker.isRunning():
            self.worker.start()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(600, 50, 200, 400)
    window.show()
    sys.exit(app.exec_())