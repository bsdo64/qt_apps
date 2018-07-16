import typing

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF, QThreadPool
from PyQt5.QtGui import QPen, QPainterPath
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyleOptionGraphicsItem, QGraphicsSceneWheelEvent

from data.model import Model
from util.fn import attach_timer
from util.thread import Worker, Thread


class CandleStickItem(QGraphicsItem):
    def __init__(self, model, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.model: Model = model
        self.path = QPainterPath()
        self.max_data_length = 1000

        self.thread = Thread()
        self.make_path()

    def paint(self,
              painter: QtGui.QPainter,
              option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...):

        # Set level of detail
        # print(option.levelOfDetailFromTransform(painter.worldTransform()))
        # self.make_path()

        painter.save()
        pen = QPen()
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.fillPath(self.path, Qt.green)
        painter.restore()

    def wheelEvent(self, event: 'QGraphicsSceneWheelEvent'):
        self.make_path()

    def make_path(self):
        data = self.model.data()

        if self.path.length() == 0.0:  # path.length == 0.0
            # draw new initial path
            print('draw new initial path')
            w = self.thread.make_worker(self.draw_path, data)
            w.sig.finished.connect(self.update)
            self.thread.start(w)

        else:
            if len(data) > self.max_data_length:  # 1500 > 1000
                self.max_data_length += 500

                print('draw next path')
                next_data = self.model.next_data()
                w = self.thread.make_worker(self.draw_path, next_data)
                w.sig.finished.connect(self.update)
                self.thread.start(w)

    def draw_path(self, data):
        path = QPainterPath()
        for i, row in data.iterrows():
            path.addRect(
                row['time_axis'],  # x
                row['n_open'],  # y
                1,  # width
                row['n_open'] - row['n_close'],  # height
            )

        self.path.addPath(path)

    def boundingRect(self):
        model_data = self.model.data()
        rect = QRectF(model_data['time_axis'].min(),
                      model_data['n_open'].min(),
                      len(model_data),
                      model_data['n_open'].max() - model_data['n_close'].min())

        return rect


attach_timer(CandleStickItem)