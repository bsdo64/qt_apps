from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGraphicsView


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


class ChartTimePane:
    def __init__(self, axis):
        self.axis = axis
        self.empty_view = QGraphicsView()
        self.empty_view.setFixedHeight(56)

    def create(self):
        return self.axis