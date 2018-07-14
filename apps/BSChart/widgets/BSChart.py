from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QSplitter

from graphic_views import ChartAxisView, ChartView, TimeAxisView
from layouts.panes import ChartPane, ChartTimePane
from utils import attach_timer


class ChartLayoutManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.chart_panes = [
            ChartPane(ChartView(), ChartAxisView()),
        ]
        self.time_axis_pane = ChartTimePane(TimeAxisView())

        self.splitter = QSplitter(parent)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setHandleWidth(2)
        self.splitter.setContentsMargins(0, 0, 0, 0)

        self.init_layout()

    def init_layout(self):
        # init chart panes
        for pane in self.chart_panes:
            self.splitter.addWidget(pane.create(self.parent))

    def del_last_pane(self, checked=False):
        count = self.splitter.count()
        if count > 1:
            self.chart_panes.pop(count - 1)
            self.splitter.widget(count - 1).deleteLater()

    def del_pane(self, index):
        if index == 0:
            return False

        self.chart_panes.pop(index)
        self.splitter.widget(index).deleteLater()

    def add_pane(self, pane=None):
        if not pane:
            pane = ChartPane(ChartView(), ChartAxisView())

        self.chart_panes.append(pane)
        self.splitter.addWidget(pane.create(self.parent))

    def get_panes(self) -> QSplitter:
        return self.splitter

    def get_time_axis(self) -> QWidget:
        return self.time_axis_pane.create(self.parent)


attach_timer(ChartLayoutManager)


class BSChart(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.vbox = QVBoxLayout(self)
        self.vbox.setSpacing(1)
        self.vbox.setContentsMargins(0, 0, 0, 0)

        self.layout = ChartLayoutManager(self)
        self.vbox.addWidget(self.layout.get_panes())
        self.vbox.addWidget(self.layout.get_time_axis())


attach_timer(BSChart)