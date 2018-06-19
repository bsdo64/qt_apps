import datetime

from PyQt5.QtCore import QTimer, Qt, QThread, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from lib.source_clients.bitmexhttpclient import BitmexHttpClient
from lib.source_clients.auth import bitmex

import pandas as pd


class Request:
    def __init__(self):
        self.client = BitmexHttpClient(test=False,
                                       api_key=bitmex.api_keys['real']['order']['key'],
                                       api_secret=bitmex.api_keys['real']['order']['secret'])

        self.rate_limit = 300
        self.df = pd.DataFrame()
        self.n = 0
        self.s = 500
        # self.start = 0  # 2017 - 01- 01
        self.start = 525600  # 2018 - 01- 01
        # self.start = 730000  # 2018 - 01- 01

        self.from_2018 = (datetime.datetime.now() - datetime.datetime(2018, 1, 1)).total_seconds() / 60

        self.client.sig_ended.connect(self.get_data)

    def request_data(self):
        start = self.start
        n = self.n
        s = self.s

        self.client.Trade.get_bucketed('1m', symbol='XBTUSD', count=500, start=n * s + start)
        self.n += 1

    def get_data(self):
        start = self.start
        n = self.n
        s = self.s
        j = self.client.json()
        self.rate_limit = self.client.headers()['x-ratelimit-remaining']

        if len(j) > 0:
            self.df = self.df.append(j, ignore_index=True)
        elif len(j) == 0:
            self.df.to_pickle('bitmex_1m_2018.pkl')
            print('saved !')
            QCoreApplication.quit()

        print('n * s + start: {}, percent: {:.2f}%, rate_limit: {}'
              .format(n * s + start, n * s / (self.from_2018 - start) * 100, self.rate_limit))

        if s * n >= 525600 * 2:
            self.df.to_pickle('bitmex_1m_2018.pkl')
            print('saved !')
            QCoreApplication.quit()




class Handler:
    def __init__(self):
        self.timer = QTimer()
        self.thread = QThread()
        self.r = Request()

        self.timer.setInterval(1000)

        self.timer.timeout.connect(self.r.request_data)

    def exec(self):
        self.timer.start()
        self.timer.moveToThread(self.thread)
        self.thread.start()


if __name__ == '__main__':
    app = QCoreApplication([])

    handler = Handler()
    handler.exec()

    app.exec()
