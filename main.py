import random
from dist import data
from dist.engine import optimise, backtest, abstraction
from dist.data import *
from dist.strategies import examples

import yfinance as yf

strategy = examples.MovingAverageCrossover

## data abstraction
p = abstraction.piston()
interval = '15m'
spark = p.spark(interval)
data = yf.download("TSLA", period="5d", interval=spark)
data = p.crank(data, interval)

## backtest
bt = backtest.piston(strategy, data)
backtest_result = bt.run({'tp':3, 'sl':2})

opp  = [backtest.piston(strategy, data).__class__(strategy,data).run({'tp':i+1, 'sl':2}) for i in range(3)]

## optimise
op = optimise.piston(strategy, {'tp':[1,3,1]})
optimise_result = op.crank(data, num_threads=4, status=False)
