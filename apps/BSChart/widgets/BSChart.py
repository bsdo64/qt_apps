from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QSplitter

from graphic_views import ChartAxisView, ChartView, TimeAxisView
from layouts.panes import ChartPane, ChartTimePane


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
        self.vbox = QVBoxLayout(self)
        self.vbox.setSpacing(1)
        self.vbox.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Vertical)
        splitter.setHandleWidth(2)

        splitter.addWidget(ChartPane(ChartView(), ChartAxisView()).create())
        splitter.addWidget(ChartView())

        self.vbox.addWidget(splitter)
        self.vbox.addWidget(ChartTimePane(TimeAxisView()).create())

