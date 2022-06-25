class abstract:
    def __init__(self, abstraction):
        self.conversion
        self.valid = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']
        self.abstraction = abstraction
    
    def _nz(self, x):
        return 0 if x <= 0 else x

    def _ab(self, interval):
        t = self.valid.index(interval)
        return self.valid[self._nz(t-self.abstraction)]

    def download(self, ticker):
        pass