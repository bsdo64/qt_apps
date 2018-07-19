import typing

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF, QThreadPool
from PyQt5.QtGui import QPen, QPainterPath, QColor
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyleOptionGraphicsItem, \
    QGraphicsSceneWheelEvent

from data.model import Model
from util.fn import attach_timer
from util.thread import Thread


class CandleStickItem(QGraphicsItem):
    def __init__(self, model, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.model: Model = model
        self.max_x_range = self.model.current_x_range()  # 2 <

        self.plus_line_path = QPainterPath()
        self.minus_line_path = QPainterPath()
        self.plus_bar_path = QPainterPath()
        self.plus_bar_path.setFillRule(Qt.WindingFill)
        self.minus_bar_path = QPainterPath()
        self.minus_bar_path.setFillRule(Qt.WindingFill)

        self.cache = {
            'plus_line_path': QPainterPath(),
            'minus_line_path': QPainterPath(),
            'plus_bar_path': QPainterPath(),
            'minus_bar_path': QPainterPath()
        }

        self.thread = Thread()
        self.make_path()

    def paint(self,
              painter: QtGui.QPainter,
              option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...):

        # Set level of detail
        # print(option.levelOfDetailFromTransform(painter.worldTransform()))

        # rect = self.model.make_scene_rect()
        # rect_path = QPainterPath()
        # rect_path.addRect(rect)



        # draw plus line
        painter.save()
        pen = QPen()
        pen.setColor(QColor("#496856"))
        pen.setCosmetic(True)
        painter.setPen(pen)
        # painter.setRenderHint(painter.Antialiasing)
        self.print_cache_path(painter, 'drawPath', 'plus_line_path', 1000)

        # draw minus line
        pen.setColor(QColor("#6F3541"))
        painter.setPen(pen)
        self.print_cache_path(painter, 'drawPath', 'minus_line_path', 1000)

        # draw plus bar
        self.print_cache_path(painter, 'fillPath',
                              'plus_bar_path', 1000, QColor('#7BB888'))
        # painter.fillPath(self.plus_bar_path, Qt.green)  # draw plus bar

        # draw minus bar
        self.print_cache_path(painter, 'fillPath',
                              'minus_bar_path', 1000, QColor('#CC4E5C'))
        # painter.fillPath(self.minus_bar_path, Qt.red)  # draw minus bar
        painter.restore()

    def print_cache_path(self, painter, fn, name, cache_len, *args):
        r = self.model.current_x_range()
        l = self.cache[name].length()
        p = getattr(painter, fn)

        if 0 < r <= cache_len:
            if l > 0:
                p(self.cache[name], *args)  # draw cache
            else:
                p(self.__getattribute__(name), *args)

        else:
            if l == 0:
                self.cache[name] = QPainterPath(self.__getattribute__(name))

            p(self.__getattribute__(name),  *args)  # draw non-cache

    def wheelEvent(self, event: 'QGraphicsSceneWheelEvent'):
        self.make_path()

    def make_path(self):
        df = self.model.current_data()
        plus_cond = 'close > open'

        if self.plus_bar_path.length() == 0.0:  # path.length == 0.0
            # draw new initial path
            print('draw new initial path')
            plus_df = df[df.eval(plus_cond)]
            minus_df = df[~df.eval(plus_cond)]

            self.create_in_thread(self.draw_path,
                                  plus_df,
                                  self.plus_line_path)
            self.create_in_thread(self.draw_path,
                                  minus_df,
                                  self.minus_line_path)
            self.create_in_thread(self.draw_rect,
                                  plus_df,
                                  self.plus_bar_path)
            self.create_in_thread(self.draw_rect,
                                  minus_df,
                                  self.minus_bar_path)

        else:
            if len(df) > self.max_x_range:  # 3 > 2
                self.max_x_range += self.model.next_x_range()  # 2 += 500

                next_df = self.model.next_data()
                plus_df = next_df[next_df.eval(plus_cond)]
                minus_df = next_df[~next_df.eval(plus_cond)]
                print('draw next path')
                self.create_in_thread(self.draw_path,
                                      plus_df,
                                      self.plus_line_path)
                self.create_in_thread(self.draw_path,
                                      minus_df,
                                      self.minus_line_path)
                self.create_in_thread(self.draw_rect,
                                      plus_df,
                                      self.plus_bar_path)
                self.create_in_thread(self.draw_rect,
                                      minus_df,
                                      self.minus_bar_path)

    def create_in_thread(self, fn, *args):
        w = self.thread.make_worker(fn, *args)
        w.sig.finished.connect(self.update)
        self.thread.start(w)

    def draw_path(self, data, path):
        new_path = QPainterPath()
        for i, row in data.iterrows():
            new_path.moveTo(row['time_axis_scaled'], row['r_high'])
            new_path.lineTo(row['time_axis_scaled'], row['r_low'])

        path.addPath(new_path)

    def draw_rect(self, data, path: QPainterPath):
        new_path = QPainterPath()
        for i, row in data.iterrows():
            new_path.addRect(
                row['time_axis_scaled'] - 15,  # x
                row['r_open'],  # y
                30,  # width
                row['r_close'] - row['r_open'],  # height
            )

        path.addPath(new_path)

    def boundingRect(self):
        return self.model.make_scene_rect()


attach_timer(CandleStickItem)
