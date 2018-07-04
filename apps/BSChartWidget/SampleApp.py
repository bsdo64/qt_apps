import pandas as pd
from PyQt5.QtWidgets import QApplication
from Chart import Chart


class App:
    def __init__(self):
        data = pd.read_pickle('../../bitmex_1m_2018.pkl')
        self.app = QApplication([])
        self.chart = Chart(data=data[-800:].reset_index())

    def start(self):
        print('App started!')
        self.chart.show()
        self.app.exec_()


if __name__ == '__main__':
    app = App()
    app.start()
