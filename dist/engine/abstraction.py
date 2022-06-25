from datetime import datetime
from numpy import invert

import yfinance as yf

class piston:
    def __init__(self, abstraction=1):
        self.conversion = {
            '1m':60,
            '2m':120,
            '5m':300,
            '15m':900,
            '30m':1800,
            '60m':3600,
            '90m':5400,
            '1h':3600,
            '1d':86400,
            '5d':432000,
            '1wk':604800,
            '1mo':2592000,
            '3mo':7776000,
        }
        
        self.valid = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']
        self.abstraction = abstraction

        self.data = {}
    
    def crank(self, d, interval):
        r = list(d.index.values)
        l = lambda x: True if datetime.timestamp(datetime.utcfromtimestamp(x.tolist()/1e9)) % self.conversion[interval] == 0 else False
        d['ABS'] = [True if l(r[i]) else False for i in range(len(list(d.index.values)))]
        return d

    def _nz(self, x):
        return 0 if x <= 0 else x

    def _ab(self, interval):
        t = self.valid.index(interval)
        return self.valid[self._nz(t-self.abstraction)]

    def spark(self, interval='5m'):
        return self._ab(interval)

