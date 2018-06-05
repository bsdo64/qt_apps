import pandas as pd
import bitmex

client = bitmex.bitmex(test=False,
                       api_key="FET28WgQOItvUlOqfgOEBGIG",
                       api_secret="Fq7kxxLhrIWoxIyMi6sZ-GsQ7mKQlW1f98FDVIJ5BP8BqdOI")

data = client.Trade.Trade_getBucketed(symbol='XBTUSD', binSize="1m", count=500, reverse=True).result()[0]

df = pd.DataFrame(data, dtype={'timestamp': 'datetime64[ns]'})

print(df.dtypes)
