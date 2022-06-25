import itertools
from itertools import permutations, islice
from os import X_OK
import threading
import math
import random
import tqdm

try:
    import backtest as bt
except:
    import dist.engine.backtest as bt



class piston():
    def __init__(self, strategy, params={}):
        self.strategy = strategy
        s_params = strategy().params
        
        l = [i for i in params]
        for i in l:
            s_params[i] = params[i]

        self.params = s_params

        for i in self.params:
            if not isinstance(self.params[i], list):
                self.params[i] = [self.params[i]]
            if len(self.params[i]) < 3:
                self.params[i] = self._util(self.params[i])

        for i in self.params:
            self.params[i] = self._a(self.params[i])
        
        self.basis = [i for i in self.params]
        self.d = {}
        for i in self.basis:
            self.d[i] = self.basis.index(i)
        self.par = list(itertools.product(*[self.params[i] for i in self.params]))
            
        self.results = []

    def _util(self, l):
        x = l[0]
        return [x,x,x]

    def _a(self, l):
        x = l[0]
        y = l[1]
        z = l[2]
        l = [i for i in range(x, y+1, z)]
        return l

    def cp(self, lsts):
        return list(itertools.product(*lsts))

    def chunks(self, l, n):
        out = []
        a = len(l)
        n = a if n > a else n
        x = math.floor(a/n)
        ##print(x)
        for i in range(n-1):
            out.append(l[i*x:(i+1)*x])
            ##print(out)
        out.append(l[(n-1)*x:])
        return out

    def check_engine(self):
        d = [i for i in self.results if type(i) is dict]
        srt = sorted(d, key=lambda x: x['result'])
        return srt, srt[-1]['result']

    def motor(self, data, q, status=False):
        ##print('#####', q)
        if status:
            for params in tqdm.tqdm(q):
                ##print(params)
                BT = bt.piston(self.strategy, data, balance = 100)
                res = BT.run(params=params[1])
                results = {}
                results['result'] = res
                results['hist'] = BT.balance_history
                results['param'] = params
                self.results.append(results)
        else:
            for params in q:
                #print(params)
                BT = bt.piston(self.strategy, data, balance = 100)
                res = BT.run(params)
                results = {}
                results['result'] = res
                results['hist'] = BT.balance_history
                results['param'] = params
                self.results.append(results)


    def crank(self, data=[], num_threads=4, status=False):
        g = []
        k = self.d
        for b in range(len(self.par)):
            p = {}
            ##print(b)
            j = self.par[b]
            ##print(j)
            for i in k:
                ##print(j[i])
                p[i] = j[k[i]]
            ##print(p)
            g.append(p)

        ##print(g)
        param = self.chunks(g, 4)
        ##print(param)

        oil = [threading.Thread(target=self.motor, args=(data, i, status)) for i in param]
        ##print(len(oil))

        for spark in oil:
            spark.start()
        for spark in oil:
            spark.join()

        return self.check_engine()


