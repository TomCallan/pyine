# pyine
A simple package for the conversion of tradingview's .pine to python script. 

Currently Supports
 - Variable Decleration ```a = 1```
 - Dynamic Value Assignment ```a = b > c```
 - If statements
 - Alert functions (will act as a print statement but will have full support in the future)
 - Comments

**Warning**
The current version (1.1.2) will auto comment any strategy calls so it is advised that a study is used instead.


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