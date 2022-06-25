# imports 
import itertools
from struct import pack
from numpy import isin, take
import pandas_ta as ta


# strategy builder class
import functools

from dist import data

# util functions
class Series:
    def __init__(self, l=[]):
        self.arr = l

    def __repr__(self): # return
        return f"{self.arr[-1]}"

    def __str__(self): # print        
        return f"{self.arr[-1]}"

    def __getitem__(self, item):
        item += 1
        if item <= len(self.arr):
            return self.arr[-item]
        else:
            raise IndexError(f"There are only {len(self.arr)} elements in the series")
    
    def __len__(self):
        return len(self.arr)
    
    def __add__(self, other):   
        return self.arr[-1] + float(other)

    def __sub__(self, other):
        return self.arr[-1] - float(other)

    def __mul__(self, other):
        if isinstance(other, (int, float, Series)):  # Scalar multiplication
            return self.arr[-1] * float(other)
        else:
            raise TypeError("operand must be Series, int, or float")

    def __truediv__(self, other):
        if isinstance(other, (int, float, Series)):  # Scalar multiplication
            return self.arr[-1] / float(other)
        else:
            raise TypeError("operand must be Series, int, or float")

    # __lt__, __le__, __gt__, __ge__, __eq__ and __ne__
    def __lt__(self, other):
        if isinstance(other, (int, float)):  # Scalar multiplication
            return self.arr[-1] < float(other)
        elif isinstance(other, Series):
            return self.arr[-1] < other.arr[-1]
        else:
            raise TypeError("operand must be Series, int, or float")

    def __lte__(self, other):
        if isinstance(other, (int, float)):  # Scalar multiplication
            return self.arr[-1] <= other
        elif isinstance(other, Series):
            return self.arr[-1] <= other.arr[-1]
        else:
            raise TypeError("operand must be Series, int, or float")

    def __gt__(self, other):
        if isinstance(other, (int, float)):  # Scalar multiplication
            return self.arr[-1] > float(other)
        elif isinstance(other, Series):
            return self.arr[-1] > other.arr[-1]
        else:
            raise TypeError("operand must be Series, int, or float")

    def __ge__(self, other):
        if isinstance(other, (int, float)):  # Scalar multiplication
            return self.arr[-1] >= float(other)
        elif isinstance(other, Series):
            return self.arr[-1] >= other.arr[-1]
        else:
            raise TypeError("operand must be Series, int, or float")

    def __eq__(self, other):
        if isinstance(other, (int, float)):  # Scalar multiplication
            return self.arr[-1] == float(other)
        elif isinstance(other, Series):
            return self.arr[-1] == other.arr[-1]
        else:
            raise TypeError("operand must be Series, int, or float")

    def __ne__(self, other):
        if isinstance(other, (int, float)):  # Scalar multiplication
            return self.arr[-1] != float(other)
        elif isinstance(other, Series):
            return self.arr[-1] != other.arr[-1]
        else:
            raise TypeError("operand must be Series, int, or float")

    # alternative for :=
    def __iadd__(self, other):
        if isinstance(other, Series):
            self.arr.append(other.arr[-1])
        else:
            self.arr.append(other)
        return Series(self.arr)

    def __pow__(self, other):
        if isinstance(other, (int, float)):  # Scalar multiplication
            return self.arr[-1] ** float(other)
        elif isinstance(other, Series):
            return self.arr[-1] ** other.arr[-1]
        else:
            raise TypeError("operand must be Series, int, or float")        





class engine():
    open = Series([])
    high = Series([])
    low = Series([])
    close = Series([])
    volume = Series([])

    
    def __init__(self, strategy, data):
        self.strategy = strategy()
        self.data = data

        self.open = {}
        self.closed = {}

    def create_order(self, x):
        self.orders[x['id']] = x

    def iterate(self, data):
        engine.open += data['Open']
        engine.high += data['High']
        engine.low += data['Low']
        engine.close += data['Close']
        engine.volume += data['Volume']

        self.strategy.body(engine.open, engine.high, engine.low, engine.close, engine.volume)

    def run(self):
        for row in self.data.iterrows():
            self.iterate(row[1])



    


class strategy:
    def __init__(self, engine):
        self.engine = engine

    def close(self, id, when=True):
        if when:
            if id in self.engine.orders:
                self.engine.closed[self.engine.index] = self.engine.orders[id]
                del self.engine.orders[id]
                self.engine.index += 1

    def entry(self, id="", type="long", when=True, stoploss=0, takeprofit=0, qty=1):
        if when:
            if id in self.engine.orders:
                self.close(id, when=True)
            self.engine.create_order({'id':id, 'type':type, 'stoploss':stoploss, 'takeprofit':takeprofit, 'qty':qty, 'at':engine.close})





def crossover(a,b):
    if (len(a) < 2) or (len(b) < 2): return
    return (a > b) and (a[1] < b[1])

def crossunder(a,b):
    if (len(a) < 2) or (len(b) < 2): return
    return (a < b) and (a[1] > b[1])



# get strategy class
class a:
    def __init__(self):
        self.long_length = 21
        self.short_length = 10

    def body(self, open, high, low, close, volume):

        long_EMA =  Series(ta.ema(close, self.long_length))
        short_EMA = Series(ta.ema(close, self.short_length))
        print(long_EMA)

        strategy.entry(id="long", when=crossover(long_EMA, short_EMA))



        
