import pandas as pd
from binance.client import Client
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')
api = config['BINANCE']

class request:
    client = Client(api['KEY'], api['SECRET'])
    constants = {
        '1m':client.KLINE_INTERVAL_1MINUTE  ,
        '3m':client.KLINE_INTERVAL_3MINUTE  ,
        '5m':client.KLINE_INTERVAL_5MINUTE  ,
        '15m':client.KLINE_INTERVAL_15MINUTE ,
        '30m':client.KLINE_INTERVAL_30MINUTE ,
        '1h':client.KLINE_INTERVAL_1HOUR    ,
        '2h':client.KLINE_INTERVAL_2HOUR    ,
        '4h':client.KLINE_INTERVAL_4HOUR    ,
        '6h':client.KLINE_INTERVAL_6HOUR    ,
        '8h':client.KLINE_INTERVAL_8HOUR    ,
        '12h':client.KLINE_INTERVAL_12HOUR   ,
        '1d':client.KLINE_INTERVAL_1DAY     ,
        '3d':client.KLINE_INTERVAL_3DAY     ,
        '1w':client.KLINE_INTERVAL_1WEEK    ,
        '1M':client.KLINE_INTERVAL_1MONTH   ,
    }

    def __init__(self) -> None:
        pass

    def security(symbol, timeframe):
        data = request.client.get_historical_klines(f"{symbol}", request.constants[timeframe])
        d = pd.DataFrame({
            'time':[int(i[0])/1000 for i in data][:-1],
            'open':[float(i[1]) for i in data][:-1],
            'high':[float(i[2]) for i in data][:-1],
            'low':[float(i[3]) for i in data][:-1],
            'close':[float(i[4]) for i in data][:-1],
            'volume':[float(i[5]) for i in data][:-1],
            'hl2':[(float(i[2])+float(i[3]))/2 for i in data][:-1],
            'hlc3':[(float(i[2])+float(i[3])+float(i[4]))/3 for i in data][:-1],
            'ohlc4':[(float(i[1])+float(i[2])+float(i[3])+float(i[4]))/4 for i in data][:-1],
        })
        return d