import pandas_ta as ta

from dist.utils.calculators import *


class s:
    def __init__(self, params):
        self.params = params
        self.src = 'Close'

    def A(self, data):
        if data[self.src] >= 17: return True
    
    def B(self, data, O, params={}):
        a = data[self.src]
        O = O['Close']
        tp = O + self.params['tp']
        sl = O - self.params['sl']
        #print(a, tp)
        if a >= tp:
            return 'PROFIT'
        elif a <= sl:
            return 'STOP'
