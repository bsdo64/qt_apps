import typing

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QPainterPath, QTransform
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyleOptionGraphicsItem

from data.model import Model
from utils import attach_timer


class CandleStickItem(QGraphicsItem):
    def __init__(self, model, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.model: Model = model
        self.path: QPainterPath = None
        self.max_data_length = 1000

    def paint(self,
              painter: QtGui.QPainter,
              option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...):

        # Set level of detail
        # print(option.levelOfDetailFromTransform(painter.worldTransform()))
        self.make_path()

        painter.save()
        pen = QPen()
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.fillPath(self.path, Qt.green)
        painter.restore()

    def make_path(self):
        data = self.model.data()

        if not self.path:
            # draw new initial path
            path = QPainterPath()
            CandleStickItem.draw_path(data, path)

            self.path = path

        else:

            if len(data) > self.max_data_length:  # 1500 > 1000
                self.max_data_length += 500

                # draw uncached path
                next_data = self.model.next_data()
                path = QPainterPath()
                CandleStickItem.draw_path(next_data, path)

                self.path.addPath(path)

    @staticmethod
    def draw_path(data, path):
        for i, row in data.iterrows():
            path.addRect(
                row['time_axis'],  # x
                row['n_open'],  # y
                1,  # width
                row['n_open'] - row['n_close'],  # height
            )

    def boundingRect(self):
        model_data = self.model.data()
        rect = QRectF(model_data['time_axis'].min(),
                      model_data['n_open'].min(),
                      len(model_data),
                      model_data['n_open'].max() - model_data['n_close'].min())

        return rect


attach_timer(CandleStickItem)