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

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem, widget: typing.Optional[QWidget] = ...):

        # print(option.levelOfDetailFromTransform(painter.worldTransform()))
        painter.save()
        # painter.setRenderHint(painter.Antialiasing)

        pen = QPen()
        pen.setCosmetic(True)
        painter.setPen(pen)

        self._make_path()

        painter.fillPath(self.path, Qt.green)
        # painter.drawRect(QRectF(model_data['time_axis'].min(),
        #                         model_data['n_open'].min(),
        #                         len(model_data),
        #                         model_data['n_open'].max() - model_data['n_close'].min()))

        painter.restore()

    def _make_path(self):
        if not self.path:
            data = self.model.data()
            path = QPainterPath()
            for i, row in data.iterrows():
                path.addRect(row['time_axis'], row['n_open'], 1, row['n_close'] - row['n_open'])

            self.path = path

        else:
            data = self.model.data()
            len_data = len(data)

            if len_data > self.max_data_length:  # 1500 > 1000
                self.max_data_length += 500

                next_data = self.model.next_data()
                # draw uncached path
                path = QPainterPath()
                for i, row in next_data.iterrows():
                    path.addRect(row['time_axis'], row['n_open'], 1,
                                 row['n_close'] - row['n_open'])

                self.path.addPath(path)

    def boundingRect(self):
        model_data = self.model.data()
        rect = QRectF(model_data['time_axis'].min(),
                      model_data['n_open'].min(),
                      len(model_data),
                      model_data['n_open'].max() - model_data['n_close'].min())

        return rect


attach_timer(CandleStickItem)