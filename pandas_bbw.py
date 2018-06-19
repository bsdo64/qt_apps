import pandas as pd

df = pd.read_pickle('bitmex_1m_2017.pkl')
df1 = pd.read_pickle('bitmex_1m_2018.pkl')

df = df.append(df1)
df.timestamp = df.timestamp.astype('datetime64[ns]')
df = df.drop_duplicates(subset=['timestamp'])

df = df.set_index('timestamp')
df.plot(y='close')

df.close.rolling(1 * 20).mean()
df.close.rolling(2 * 20).mean()
df.close.rolling(3 * 20).mean()
df.close.rolling(3 * 20).mean()
df.close.rolling(4 * 20).mean()
df.close.rolling(5 * 20).mean()

df.close.rolling(1 * 20).mean()
df.close.rolling(2 * 20).mean()
df.close.rolling(3 * 20).mean()
df.close.rolling(3 * 20).mean()
df.close.rolling(4 * 20).mean()
df.close.rolling(5 * 20).mean()

df.close.rolling(1 * 20).mean()
df.close.rolling(2 * 20).mean()
df.close.rolling(3 * 20).mean()
df.close.rolling(3 * 20).mean()
df.close.rolling(4 * 20).mean()
df.close.rolling(5 * 20).mean()

df.close.rolling(1 * 20).mean()
df.close.rolling(2 * 20).mean()
df.close.rolling(3 * 20).mean()
df.close.rolling(3 * 20).mean()
df.close.rolling(4 * 20).mean()
df.close.rolling(5 * 20).mean()

df.close.rolling(1 * 20).mean()
df.close.rolling(2 * 20).mean()
df.close.rolling(3 * 20).mean()
df.close.rolling(3 * 20).mean()
df.close.rolling(4 * 20).mean()
df.close.rolling(5 * 20).mean()