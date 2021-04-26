import requests
import time
import datetime

class finnhub():
    def __init__(self):
        self.token = ''
        self.baseurl = 'https://finnhub.io/api/v1/'


    ## fundementals
    def getSymbol(self, query):
        url = self.baseurl + 'search?q={0}&token={1}'.format(query, self.token)
        result = requests.get(url)
        symbol = result.json()["result"][0]["symbol"]
        return symbol
 
    def marketNews(self, category):
        url = self.baseurl + '/news?category={0}&minId=0&token={1}'.format(category, self.token)
        return requests.get(url).json()
    
    def companyNews(self, symbol, period=365):
        to = time.strftime("%Y-%m-%d")
        period = datetime.timedelta(days = period)
        fromX = (datetime.datetime.now() - period).strftime("%Y-%m-%d")
        url = self.baseurl + '/company-news?symbol={0}&from={1}&to={2}&token={3}'.format(symbol, fromX, to, self.token)
        result = requests.get(url).json()
        return result

    def newsSentiment(self, symbol):
        url = self.baseurl + '/news-sentiment?symbol={0}&token={1}'.format(symbol, self.token)
        result = requests.get(url).json()
        return result

    def peers(self, symbol):
        url = self.baseurl + '/stock/peers?symbol={0}&token={1}'.format(symbol, self.token)
        result = requests.get(url).json()
        return result
    
    def basicFinancials(self, symbol, metric='all'):
        url = self.baseurl + '/stock/metric?symbol={0}&metric={1}&token={2}'.format(symbol, metric, self.token)
        result = requests.get(url).json()
        return result
    
    def insiderTransactions(self, symbol, limit=100):
        url = self.baseurl + '/stock/insider-transactions?symbol={0}&limit={1}&token={2}'.format(symbol, limit, self.token)
        result = requests.get(url).json()
        return result

    def financialsAsReported(self, symbol):
        url = self.baseurl + '/stock/financials-reported?symbol={0}&token={1}'.format(symbol, self.token)
        result = requests.get(url).json()
        return result

    def secFilings(self, symbol):
        url = self.baseurl + '/stock/filings?symbol={0}&token={1}'.format(symbol, self.token)
        result = requests.get(url).json()
        return result
    

    ## Stock Estimates
    def recommendationTrends(self, symbol):
        url = self.baseurl + '/stock/recommendation?symbol={0}&token={1}'.format(symbol, self.token)
        result = requests.get(url).json()
        return result
    
    def earningSurprises(self, symbol):
        url = self.baseurl + '/stock/earnings?symbol={0}&token={1}'.format(symbol, self.token)
        result = requests.get(url).json()
        return result
    

    ## Stock Price
    def stockQuote(self, symbol):
        url = self.baseurl + '/quote?symbol={0}&token={1}'.format(symbol, self.token)
        result = requests.get(url).json()
        return result
    
    def stockCandles(self, symbol, resolution, period):
        to = str(time.time()).split('.')[0]
        period = datetime.timedelta(days = period)
        fromX = str((datetime.datetime.now() - period).timestamp()).split('.')[0]
        url = self.baseurl + '/stock/candle?symbol={0}&resolution={1}&from={2}&to={3}&token={4}'.format(symbol, resolution, fromX, to, self.token)
        result = requests.get(url).json()
        return result

    
    ## ETFS & Indices
    def indicesConstituents(self, index):
        url = self.baseurl + '/index/constituents?symbol={0}&token={1}'.format(index, self.token)
        result = requests.get(url).json()
        return result

    
    ## Forex
    def forexExchanges(self):
        url = self.baseurl + '/forex/exchange&token={0}'.format(self.token)
        result = requests.get(url).json()
        return result
    
    def forexSymbol(self, exchange):
        url = self.baseurl + '/forex/symbol?exchange={0}&token={1}'.format(exchange, self.token)
        result = requests.get(url).json()
        return result
    
    def forexCandles(self, symbol, resolution, period):
        to = str(time.time()).split('.')[0]
        period = datetime.timedelta(days = period)
        fromX = str((datetime.datetime.now() - period).timestamp()).split('.')[0]
        url = self.baseurl + '/stock/candle?symbol={0}&resolution={1}&from={2}&to={3}&token={4}'.format(symbol, resolution, fromX, to, self.token)
        result = requests.get(url).json()
        return result
    
    def forexRates(self, base):
        url = self.baseurl + '/forex/rates?base={0}&token={1}'.format(base, self.token)
        result = requests.get(url).json()
        return result
    

    ## crypto
    def cryptoExchanges(self):
        url = self.baseurl + '/crypto/exchange&token={0}'.format(self.token)
        result = requests.get(url).json()
        return result
    
    def cryptoSymbol(self, exchange):
        url = self.baseurl + '/crypto/symbol?exchange={0}&token={1}'.format(exchange, self.token)
        result = requests.get(url).json()
        return result
    
    def cryptoCandles(self, symbol, resolution, period):
        to = str(time.time()).split('.')[0]
        period = datetime.timedelta(days = period)
        fromX = str((datetime.datetime.now() - period).timestamp()).split('.')[0]
        url = self.baseurl + '/crypto/candle?symbol={0}&resolution={1}&from={2}&to={3}&token={4}'.format(symbol, resolution, fromX, to, self.token)
        result = requests.get(url).json()
        return result

    
    ## technical analysis
    def patternRecognition(self, symbol, resolution):
        url = self.baseurl + '/scan/pattern?symbol={0}&resolution={1}&token{2}'.format(symbol, resolution, self.token)
        result = requests.get(url).json()
        return result
    
    def supportResistance(self, symbol, resolution):
        url = self.baseurl + '/scan/support-resistance?symbol={0}&resolution={1}&token{2}'.format(symbol, resolution, self.token)
        result = requests.get(url).json()
        return result
    
    def aggregateIndicators(self, symbol, resolution):
        url = self.baseurl + '/scan/technical-indicator?symbol={0}&resolution={1}&token{2}'.format(symbol, resolution, self.token)
        result = requests.get(url).json()
        return result
    
    def technicalIndicators(self, symbol, resolution, fromX, to, indicator, period):
        to = str(time.time()).split('.')[0]
        period = datetime.timedelta(days = period)
        fromX = str((datetime.datetime.now() - period).timestamp()).split('.')[0]
        url = self.baseurl + '/indicator?symbol=symbol={0}&resolution={1}&from={2}&to={3}&indicator={4}&timeperiod={5}&token={6}'.format(symbol, resolution, fromX, to, indicator, period ,self.token)
        result = requests.get(url).json()
        return result

    
    ## alternative data
    def covid19(self):
        url = self.baseurl + '/covid19/us&token{0}'.format(self.token)
        result = requests.get(url).json()
        return result

    
    ## economic data
    def country(self):
        url = self.baseurl + '/country?&token{0}'.format(self.token)
        result = requests.get(url).json()
        return result

    def calender(self):
        url = self.baseurl + '/calender/economic?&token{0}'.format(self.token)
        result = requests.get(url).json()
        return result