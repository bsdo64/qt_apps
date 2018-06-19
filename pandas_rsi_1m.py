import pandas as pd
import datetime
import matplotlib.pyplot as plt

import pyqtgraph

df = pd.read_pickle('bitmex_1m_2017.pkl')
df1 = pd.read_pickle('bitmex_1m_2018.pkl')

df = df.append(df1)
df.timestamp = df.timestamp.astype('datetime64[ns]')
df = df.drop_duplicates(subset=['timestamp'])

df = df.set_index('timestamp')
df.plot(y='close')

close = df['close']
delta = close.diff()

up, down = delta.copy(), delta.copy()

up[up < 0] = 0
down[down > 0] = 0

roll_up1 = up.ewm(span=14).mean()
roll_down1 = down.abs().ewm(span=14).mean()

RS1 = roll_up1 / roll_down1
RSI1 = 100.0 - (100.0 / (1.0 + RS1))

# Calculate the SMA
roll_up2 = up.rolling(14).mean()
roll_down2 = down.abs().rolling(14).mean()

# Calculate the RSI based on SMA
RS2 = roll_up2 / roll_down2
RSI2 = 100.0 - (100.0 / (1.0 + RS2))

# RSI1 vs RSI2
# Compare graphically
plt.figure()
RSI1.plot()
RSI2.plot()
plt.legend(['RSI via EWMA', 'RSI via SMA'])
plt.show()