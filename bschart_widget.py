import random

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets


class Chart(QWidget):
    sig = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self.painted = False
        self.df = pd.DataFrame()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        self.drawLines(qp)
        qp.end()

    def drawPoints(self, qp):

        qp.setPen(QtCore.Qt.red)
        size = self.size()

        if not self.painted:
            for i in range(100000):
                x = random.randint(1, size.width() - 1)
                y = random.randint(1, size.height() - 1)
                qp.drawPoint(x, y)

            self.painted = True

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        df = pd.read_pickle('bitmex_1m_2018.pkl')
        self.df = df

    def drawLines(self, qp):
        print(self.df)
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(20, 40, 250, 40)

        pen.setStyle(QtCore.Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(20, 80, 250, 80)

        pen.setStyle(QtCore.Qt.DashDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 120, 250, 120)

        pen.setStyle(QtCore.Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(20, 160, 250, 160)

        pen.setStyle(QtCore.Qt.DashDotDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 200, 250, 200)

        pen.setStyle(QtCore.Qt.CustomDashLine)
        pen.setDashPattern([1, 4, 5, 4])
        qp.setPen(pen)
        qp.drawLine(20, 240, 250, 240)


class Ui_bschart(QWidget):
    def setupUi(self, bschart):
        bschart.setObjectName("bschart")
        bschart.resize(1124, 808)
        self.verticalLayout = QtWidgets.QVBoxLayout(bschart)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chart = Chart(bschart)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chart.sizePolicy().hasHeightForWidth())
        self.chart.setSizePolicy(sizePolicy)
        self.chart.setStyleSheet("QWidget{\n"
"border-bottom: 1px solid black; \n"
"border-right: 1px solid black; \n"
"}")
        self.chart.setObjectName("chart")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.chart)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(self.chart)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 30))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(10, 0, 81, 31))
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.widget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.chart)
        self.axis = QtWidgets.QWidget(bschart)
        self.axis.setMinimumSize(QtCore.QSize(50, 0))
        self.axis.setMaximumSize(QtCore.QSize(50, 16777215))
        self.axis.setObjectName("axis")
        self.horizontalLayout.addWidget(self.axis)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(bschart)
        QtCore.QMetaObject.connectSlotsByName(bschart)

    def retranslateUi(self, bschart):
        _translate = QtCore.QCoreApplication.translate
        bschart.setWindowTitle(_translate("bschart", "Form"))
        self.label.setText(_translate("bschart", "Hello world"))


if __name__ == '__main__':
    app = QApplication([])

    win = QWidget()

    ui = Ui_bschart()
    ui.setupUi(win)

    win.show()

    app.exec_()