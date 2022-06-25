import random
from re import X
from dist import data
from dist.engine import optimise, backtest, abstraction, btv2
from dist.data import *
from dist.strategies import examples

import yfinance as yf

## data abstraction
p = abstraction.piston()
interval = '15m'
spark = p.spark(interval)
data = yf.download("TSLA", period="5d", interval=spark)
data = p.crank(data, interval)

## declare environment
engine = btv2.engine(data)
strategy = btv2.strategy(engine)

#a = btv2.a()

#engine.iterate(a)



def t():
    global x
    print(x)
    x+=random.randint(0,10)


class a:
    x = btv2.Series([1])

    def c(self):
        print(a.x)
        a.x+=random.randint(0,10)