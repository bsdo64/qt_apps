import pandas as pd

df = pd.read_pickle('bitmex_1m_2017.pkl')
df1 = pd.read_pickle('bitmex_1m_2018.pkl')
df2 = pd.read_pickle('bitmex_1m_2018_tmp.pkl')

df = df.append(df1)
df = df.append(df2)

df.timestamp = df.timestamp.astype('datetime64[ns]')
df = df.drop_duplicates(subset=['timestamp'])

df = df.set_index('timestamp')


def last():
    c = []
    for i in range(30000):
        b = 20 * (1 + i)
        a = 2 * df.close[-b:].std()
        c.append((df.close[-1] - (df.close[-b:].mean() - a)) / (2 * a))
    return pd.Series(c)

l = last()
l.plot()

print(l)