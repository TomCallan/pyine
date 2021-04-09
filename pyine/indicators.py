# utils
def change(src): # simple subtraction
    return src[-1] - src[-2]

def crossover(x, y, z):
    return x < y < z
def crossunder(x, y, z):
    return x > y > z


## Moving Averages
# Simple Moving Average
def sma(src, length):
    if len(src) < length:
        return None
    return sum(src[-length:]) / float(length)

# Exponential Moving Average
EMA = []
def ema(src, length, reset = False):
    global EMA
    if reset: EMA = []; return  
    if len(src) < length: return  
    alpha = 2 / (length + 1)  
    if len(EMA) == 0:
        EMA.append(sma(src, length))
    else:
        EMA.append(alpha * src[-1] + (1 - alpha) * EMA[-1])
    return EMA[-1]

# Rolling Moving Average
RMA = []
def rma(src, length, reset = False):
    global RMA
    if reset: RMA = []; return  
    if len(src) < length: return  
    alpha = 1 / length 
    if len(RMA) == 0:
        RMA.append(sma(src, length))
    else:
        RMA.append(alpha * src[-1] + (1 - alpha) * RMA[-1])
    return RMA[-1]

# Smoothed Moving Average
SMMA = []
def smma(src, length, reset = False):
    global SMMA
    if reset: EMA = []; return 
    if len(src) < length: return 
    # if n[1] not valid return sma, else calculate
    # if not na(smma[1]) ? sma(src, len) : (smma[1] * (len - 1) + src) / len
    if len(SMMA) == 0:
        SMMA.append(sma(src, length))
    else:
        calculation = (SMMA[-1] * (length - 1) + src[-1]) / length
        SMMA.append(calculation)
    return SMMA[-1]



# Relative Strength Index
def rsi(src, length, avg = rma):
    UP = []
    DOWN = []
    if len(src) < length + 1:
        return [0], [0]
    for i in range(length+1):
        i += 1
        if src[-i] > src[-(i+1)]:
            UP.append(src[-i])
            DOWN.append(0)
        elif src[-i] < src[-(i+1)]:
            UP.append(0)
            DOWN.append(src[-i])
    try:
        # return 100 - (100 / (1 + avg(UP, length)/avg(DOWN, length)))   
        return UP, DOWN
    except:
        return -1


# MACD
def MACD(src, signal_length, fast_length, slow_length, sma_source = False, sma_signal = False):
    if sma_source:
        fast_ma, slow_ma = sma(src, fast_length), sma(src, slow_length)
    else:
        fast_ma, slow_ma = ema(src, fast_length), ema(src, slow_length)
      
    macd = fast_ma - slow_ma
    if sma_signal:
        signal = sma(macd, signal_length)
    else:
        signal = ema(macd, signal_length)
 
    hist = macd - signal
    return hist




