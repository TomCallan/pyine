#from data import *
import random
import math

from numpy import NaN


class cylinder:
    def __init__(self, strategy):
        self.strategy = strategy
        self.contract = {'O':'', 'C':'', 'R':0}
        self.state = 'NEW'
        self.res = ''

    def prime(self, data, hist, ABS=True):
        if ABS:
            x = self.strategy.A(data, hist)
            if x:
                self.contract = {'O':data, 'C':'', 'R':0, 'D':x}
                self.state = 'PRIMED'

    def rotate(self, data, O, params={}):
        x = self.strategy.B(data, O, self.contract)
        if x:
            self.state = 'CLOSED'
            self.res = x
            self.contract['C'] = data
            if self.contract['D'] == 1:
                self.contract['R'] = data['Close'] - self.contract['O']['Close']
            elif self.contract['D'] == -1:
                self.contract['R'] = self.contract['O']['Close'] - data['Close']
            return True

class piston:
    def __init__(self, strategy, data, balance = 100, target='Close'):
        self.strategy = strategy
        self.balance = balance
        self.data = data
        self.target = target
        self.history = []
        self.balance_history = []

    def value(self, portfolio):
        b = 0
        for i in portfolio:
            b += i['R']
        return b

    def run(self, params={}):
        c = cylinder

        portfolio = []
        closed = [{'R':0}]

        hist = self.data

        for row in self.data.iterrows():
            #print(row[1])
            d = row[1]
            ABS = row[1]['ABS']

            try:
                if portfolio[-1].state != 'NEW':
                    portfolio.append(c(self.strategy(params)))
            except:
                portfolio.append(c(self.strategy(params))) 
            
            #print(balance)
            if d['Close'] > self.balance: pass

            for i in portfolio:
                if i.state == 'NEW':
                    i.prime(d, hist, ABS)
                elif i.state == 'PRIMED':
                    O = i.contract['O']
                    i.rotate(d, O)
            
        closed = [i.contract for i in portfolio if i.state == 'CLOSED']
        
        self.balance_history.append(self.balance)

        for i in closed:
            self.balance += i['R']
            self.balance = round(self.balance, 2)
            i['BAL'] = round(self.balance,2)
            self.history.append(i)
            self.balance_history.append(round(self.balance,2))
            
        return round(self.balance, 2)



#print([i.contract for i in portfolio])

    
    