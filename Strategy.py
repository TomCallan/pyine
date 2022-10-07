import pandas as pd
import configparser
from datetime import datetime
import pandas as pd
from binance.client import Client
from Request import request

class Strategy:

    CONVERSION = {
        't':'time',
        'o':'open',
        'h':'high',
        'l':'low',
        'c':'close',
        'v':'volume',
        't':'time',
        'T':'TIME',
    }
    
    def __init__(self, ticker="BTCUSDT", timeframe="1m", name=''):
        self.data = pd.DataFrame()

        self.cache = pd.DataFrame()

        self.debug = False

        self.ticker = ticker

        self.name = name if name else type(self).__name__

        self.status = "alive"

        self.alerts = []
        
        config = configparser.ConfigParser()
        config.read('config.cfg')
        self.config = config[self.name]
        api = config['BINANCE']
        self.client = Client(api['KEY'], api['SECRET'])

    def calculator(func):
        def inner_function(*args, **kwargs):
            try:
                n = func(*args, **kwargs)
                return n
            except:
                pass
        n = inner_function
        if n: return n
        else: pass

    def reset_data(self):
        self.data = pd.DataFrame({
            'time':[],
            'open':[],
            'high':[],
            'low':[],
            'close':[],
            'volume':[],
            })
    
    def alertcondition(self, when, title="", message=""):
        cond = when.iloc[-1].bool()
        if cond:
            print(datetime.fromtimestamp(self.data.time.iloc[-1]), self.ticker, message)
        l = []
        for i in range(len(when)):
            if when.iloc[i].bool() == True:
                l.append([self.data.time.iloc[i], message, self.ticker])
        self.alerts.append(l)

    def tick(self):
        return "Tick Success"
