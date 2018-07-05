import datetime
import os

import dateutil
from PyQt5.QtCore import QTimer, Qt, QThread, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from lib.source_clients.bitmexhttpclient import BitmexHttpClient
from lib.source_clients.auth import bitmex

import pandas as pd


class Request:
    def __init__(self, start=0, data=pd.DataFrame()):
        self.client = BitmexHttpClient(test=False,
                                       api_key=bitmex.api_keys['real']['order']['key'],
                                       api_secret=bitmex.api_keys['real']['order']['secret'])

        self.now = datetime.datetime.now(tz=datetime.timezone.utc)
        self.one_year_min = 525600
        self.rate_limit = 300
        self.df = data
        self.requested = 0
        self.count = 500
        # self.start = 0  # 2017 - 01- 01
        self.start = start

        self.year_first = datetime.datetime(self.now.year, 1, 1, tzinfo=datetime.timezone.utc)
        self.now_to_min = (self.now - self.year_first).total_seconds() / 60
        self.now_from_start = (self.now - (self.year_first + datetime.timedelta(minutes=self.start))).total_seconds() / 60

        self.client.sig_ended.connect(self.get_data)

    def request_data(self):
        start = self.start
        n = self.requested
        s = self.count

        self.client.Trade.get_bucketed('1m', symbol='XBTUSD', count=500, start=n * s + start)
        self.requested += 1

    def get_data(self):
        start = self.start
        n = self.requested
        s = self.count
        j = self.client.json()
        self.rate_limit = self.client.headers()['x-ratelimit-remaining']

        if len(j) > 0:
            self.df = self.df.append(j, ignore_index=True)
        elif len(j) == 0:
            self.df.to_pickle('bitmex_1m_2018.pkl')
            print('saved !')
            print("Last index : {}".format(self.df.shape[0]))
            QCoreApplication.quit()

        print('now: {}, current: {}, percent: {:.2f}%, rate_limit: {}'
              .format(self.now_to_min + self.one_year_min * (self.now.year - 2017), n * s + start,
                      n * s / self.now_from_start * 100, self.rate_limit))

        if s * n >= 525600 * 2:
            self.df.to_pickle('bitmex_1m_2018_end.pkl')
            print('saved to the end of {}!'.format(self.now.year))
            QCoreApplication.quit()


class Requester:
    def __init__(self):

        start, data = self.check_current_data()

        self.timer = QTimer()
        self.thread = QThread()
        self.r = Request(start=start, data=data)

        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.r.request_data)

    def exec(self):
        self.timer.start()
        self.timer.moveToThread(self.thread)
        self.thread.start()

    def check_current_data(self):
        now = datetime.datetime.now()
        total_min = 525600 # 1 - year
        filename = 'bitmex_1m_{}.pkl'.format(now.year)

        if os.path.isfile(filename):

            df = pd.read_pickle('bitmex_1m_{}.pkl'.format(now.year))
            last_time = df['timestamp'][df.shape[0] - 1]
            expect_last_time = datetime.datetime(now.year, 1, 1, tzinfo=datetime.timezone.utc) + \
                         datetime.timedelta(minutes=df.shape[0] - 1)

            if expect_last_time == dateutil.parser.parse(last_time):
                start_from = df.shape[0] + total_min * (now.year - 2017)
                print("Now : ", now)
                print("Last time : ", last_time)
                print("Start from ...{}".format(start_from))
                print()
            else:
                raise Exception("Not correct expected last time")
        else:
            df = pd.DataFrame()
            start_from = total_min * (now.year - 2017)
            print("Now : ", now)
            print("Start from ...{}".format(start_from))
            print()

        return start_from, df


if __name__ == '__main__':
    app = QCoreApplication([])

    handler = Requester()
    handler.exec()

    app.exec()
