def crossover(a,b):
    if a[len(a)-1] > b[len(b)-1] and a[len(a)-2] < b[len(b)-2]:
        return True


def mktbuy():
    return 1

def mktsell():
    return -1