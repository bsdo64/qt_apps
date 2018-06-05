from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView


class MyModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(MyModel, self).__init__(parent)

        self.timer = QTimer()
        self.timer.timeout.connect(self.start_source)
        self.data = [{"hello": "hello", "world": "world"}]
        self.count = 0

        self.start_source()

    def start_source(self):
        index = self.index(0, 0, QModelIndex())

        print(index.column())
        print(index.row())
        print(index.data())
        print(index.isValid())
        print(index.flags())
        print(index.model())
        print(index.parent())

        print(self.data)

        if len(self.data) < 10:
            self.insertRows(index, 1, 0)

        self.setData(index, {"hello": "hello" + str(self.count), "world": "world" + str(self.count)}, Qt.EditRole)

        if len(self.data) >= 10:
            self.removeRows(index, 1, 9)

        self.count += 1
        self.timer.start(1000)

    def rowCount(self, parent: QModelIndex = None):
        if len(self.data) <= 10:
            return len(self.data)
        else:
            return 10

    def columnCount(self, parent: QModelIndex = None):
        return 2

    def data(self, index, role=None):

        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0:
                return self.data[row]["hello"]

            if col == 1:
                return self.data[row]["world"]

        return None

    def insertRows(self, position, rows, index=None):
        self.beginInsertRows(QModelIndex(), index, index + rows - 1)

        for row in range(rows):
            self.data.insert(index, {"hello":"", "world":""})

        self.endInsertRows()
        return True

    def removeRows(self, position, rows, index=None):
        self.beginRemoveRows(QModelIndex(), index, index + rows - 1)

        for row in range(rows):
            self.data.pop(index)

        self.endRemoveRows()
        return True

    def setData(self, index, value, role=None):

        if role == Qt.EditRole:
            row = index.row()

            self.data[row] = value
            self.dataChanged.emit(index, index)

        return False

if __name__ == '__main__':
    app = QApplication([])

    window = QMainWindow()

    center = QTableView()
    model = MyModel()
    center.setModel(model)

    window.setCentralWidget(center)

    window.show()

    app.exec()