import pandas as pd
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QGraphicsView

from util.fn import attach_timer


class Model:
    def __init__(self,
                 data: pd.DataFrame,
                 view: QGraphicsView):

        self.series = data
        self.view = view

        self.axis_width = 100
        self.default_data_size = 1000
        self.next_data_size = 500
        self.marker_gap = 30
        self.scale_factor = 1
        self.max_data_range = 100_000

        self._init_printing_data()

    def _init_printing_data(self):
        self.series['time_axis'] = (
            self.series['timestamp'].astype('int64') // 10 ** 9 // 60
        )

        for i in ['close', 'open', 'low', 'high']:
            m = self.series[i].max()
            self.series['n_' + i] = m - self.series[i]

    def current_range(self):
        return int(
            self.default_data_size + self.axis_width / self.view.width()*10
        )

    def data(self) -> pd.DataFrame:
        data = self.series[-self.current_range():]

        return data

    def next_data(self, data_range=None) -> pd.DataFrame:
        next_data_size = data_range or self.next_data_size
        v = self.current_range() // next_data_size - 2  # 1001 // 500
        return self.series[
                   -(self.default_data_size + next_data_size * (v+1)):  # 1500
                   -(self.default_data_size + next_data_size * v)       # 1000
               ]

    def scale(self) -> (float, float):
        data_range = self.current_range()
        model_data = self.data()
        scale_x = self.view.width() / data_range
        scale_y = self.view.height() / (model_data['n_open'].max() -
                                        model_data['n_close'].min())
        return scale_x, scale_y

    def add_range(self, factor):
        if self.axis_width + factor > 0:
            self.axis_width += factor

        # Scale view after change x-range to fit view
        trans = QTransform()
        trans.scale(*self.scale())
        self.view.setTransform(trans)

        # Change scene rect to fit view
        model_data = self.data()
        scene = self.view.scene()
        scene.setSceneRect(QRectF(
            model_data['time_axis'].min(),
            model_data['n_open'].min(),
            len(model_data) - 5,
            model_data['n_open'].max() - model_data['n_close'].min()
        ))  # update scene rect


attach_timer(Model)
