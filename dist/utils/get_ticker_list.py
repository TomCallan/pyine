from pyfinviz.screener import Screener
import pandas as pd

def SANDP500():
    options = [Screener.IndexOption.SANDP_500]
    screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION, pages=[x for x in range(1, 30)])
    k = screener.data_frames
    l = pd.concat([k[i] for i in k])
    l.to_csv('assets/tickers.csv', encoding='utf-8', index=False)


