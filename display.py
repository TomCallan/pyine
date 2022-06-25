import dash
from dash import * 
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
from dist import strategies
from pyfinviz.screener import Screener

from dist import data
from dist.engine import optimise, backtest, abstraction
from dist.data import *
from dist.strategies import examples
from dist.utils import listclasses

from threading import Thread

import yfinance as yf

t = []

options = [Screener.IndexOption.SANDP_500]
screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION, pages=[x for x in range(1, 30)])
k = screener.data_frames
l = pd.concat([k[i] for i in k])

f = listclasses.get_file_list('dist/strategies')
h = listclasses.get_classes('dist/strategies', f)
g = h[0]

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "pyine"


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="pyine dashboard", className="header-title"
                ),
                html.P(
                    children="Analyse & optimise your trading strategies, powered by pyine",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Ticker", className="menu-title"),
                        dcc.Dropdown(
                            id="ticker-filter",
                            options=[
                                {"label": ticker, "value": ticker}
                                for ticker in np.sort(list(l['Ticker']))
                            ],
                            value="AAPL",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Interval", className="menu-title"),
                        dcc.Dropdown(
                            id="interval-filter",
                            options=[
                                {"label": interval, "value": interval}
                                for interval in ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']],
                            value='5m',
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Strategy", className="menu-title"),
                        dcc.Dropdown(
                            id="strategy-filter",
                            options=[
                                {"label": strategy, "value": strategy}
                                for strategy in g
                            ],
                            value = g[0],
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("price-chart", "figure"),],
    [
       Input("ticker-filter", "value"),
       Input("interval-filter", "value"),
       Input("strategy-filter", "value"),
    ],
)
def update_charts(ticker, interval, strategy):
    strategy = eval(h[-1][strategy])

    ## data abstraction
    #p = abstraction.piston()
    #spark = p.spark(interval)
    #data = yf.download(ticker, period="5d", interval=spark)
    #data = p.crank(data, interval)

    data = pd.read_csv('MNQ 03-22.Last.txt', sep=";", header=None)
    data.columns = ["Time", "Open", "High", "Low", "Close", "Volume"]
    l = [True for i in range(len(data['Close']))]
    data['ABS'] = l

    ## backtest
    bt = backtest.piston(strategy, data)
    bt.run({'tp':3, 'sl':2})
    
    price_chart_figure = {
        "data": [
            {
                "x": [str(i) for i in range(len(bt.balance_history))],
                "y": [i for i in bt.balance_history],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return [price_chart_figure]


if __name__ == "__main__":
    app.run_server(debug=True)