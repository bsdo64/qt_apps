import pandas as pd
from PyQt5.QtCore import QRectF, QRect
from PyQt5.QtWidgets import QGraphicsView


class Model:
    def __init__(self,
                 data: pd.DataFrame,
                 view: QGraphicsView):
        data['timestamp'] = data['timestamp'].astype('datetime64')
        data['time_axis'] = data['timestamp'].astype('int64') // 10 ** 9 // 60

        self.series = data
        data_length = len(data)
        self.data_range = data_length if data_length < 100 else 100
        self.view = view
        self.marker_gap = 30
        self.scale_factor = 1

    def data(self) -> pd.DataFrame:
        return self.series[-self.data_range:]

    # def

    def set_range(self, data_range):
        self.data_range = data_range

    def increase_range(self, factor):
        self.data_range += factor

    def decrease_range(self, factor):
        self.data_range -= factor

    def add_range(self, factor):
        if self.data_range + factor > 0:
            self.data_range += factor

        model_data = self.data()
        rect = QRectF(model_data['time_axis'].min(),
                      model_data['open'].min(),
                      len(model_data),
                      model_data['open'].max() - model_data['close'].min())

        trans = self.view.transform()
        self.scale_factor = (self.view.width() / self.data_range)
        # self.view.scale(scale_x, 1)

        self.view.setSceneRect(rect)
