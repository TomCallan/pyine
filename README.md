# pyine
A simple package for the conversion of tradingview's .pine to python script. 

## This version is deprecated and will soon be replaced by pyine v2 which hopes to add far more functionality & pine v5 support

## Currently does not support pyine v4 


Currently Supports
 - Variable Decleration ```a = 1```
 - Dynamic Value Assignment ```a = b > c```
 - If statements
 - Alert functions (will act as a print statement but will have full support in the future)
 - Comments

**Warning**
The current version (1.1.2) will auto comment any strategy calls so it is advised that a study is used instead.
The most up to date version is not listed on pypi and won't be for a while.


## Usage
Pyine currently supports partial file conversion (good for simple pine script files) and the below indicators (based on their pine script equivelants)

Indicators
 - Simple Moving Average
 - Exponential Moving Average


### Converter
```
from pyine import convert
_ = convert(filename)
```

### Indicators
```
from pyine.indicators import *
ema = ema(close, period)
```

### Data Providers
```
from pyine.data import *
finnhub = finnhub()
finnhub.token = 'YOUR API TOKEN'
finnhub.stockCandles('TSLA', resolution=5, period=1)
```
Full documentation will be added
