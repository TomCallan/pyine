import dash
from dash import * 
from dash.dependencies import Output, Input

import math
import json 
import pandas as pd
import numpy as np

from dist import strategies
from dist import data
from dist.engine import backtest, abstraction
from dist.utils import listclasses
from dist.strategies import *

import yfinance as yf


l = pd.read_csv('assets/tickers.csv')

f = listclasses.get_file_list('dist/strategies')
h = listclasses.get_classes('dist/strategies', f)
g = h[0]

d = {}

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="backtester", className="header-title"
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
                    children=[
                        html.Div(children="Parameters", className="menu-title"),
                        dcc.Dropdown(
                            id="param-filter",
                            className="dropdown"
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Input", className="menu-title"),
                        dcc.Input(
                            id="param-input",
                            className="input",
                            debounce=True,
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Out", className="menu-title"),
                        html.Div(
                            html.P(
                                id="params-output",
                            ),
                            className="output"
                        ),
                    ],
                ),
            ],
            className="menu2",
        ),

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=[
                        html.Div(
                            html.P(
                                id="profit",
                            ),
                            className="output card stats"
                        ),
                        html.Div(
                            html.P(
                                id="drawdown",
                            ),
                            className="output card stats"
                        ),
                        html.Div(
                            html.P(
                                id="sharpe",
                            ),
                            className="output card stats"
                        ),
                    ],
                className="menu3",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@callback(
    [Output("param-filter", "options")],
    [
        Input("strategy-filter", "value")
    ]
)
def update_params(strat):
    global d
    d = {}
    strategy = eval(h[-1][strat])()
    params = [i for i in strategy.params]
    fig = [{"label":i, "value":i} for i in params]
    return [fig]



@callback(
    [Output("price-chart", "figure"), Output("param-input", "value"), Output("params-output", "children"), Output("profit", "children"), Output("drawdown", "children"), Output("sharpe", "children")],
    [
       Input("ticker-filter", "value"),
       Input("interval-filter", "value"),
       Input("strategy-filter", "value"),
       Input("param-filter", "value"),
       Input("param-input", "value"),
    ],
)
def update_charts(ticker, interval, strat, param, paramval):
    global d

    strategy = eval(h[-1][strat])
    strat = strategy()

    if paramval and param: d[param] = paramval
    
    params = strat.params

    for param in d:
        params[param] = d[param]
    
    print(params)

    strat = ''

    ## data abstraction
    p = abstraction.piston()
    spark = p.spark(interval)
    data = yf.download(ticker, period="5d", interval=spark)
    data = p.crank(data, interval)

    ## backtest
    bt = backtest.piston(strategy, data)
    out = bt.run(params)
    
    drawdown=abs(min(bt.balance_history))
    profit=out
    sharpe=0


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
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return [price_chart_figure, '', ["{} : {} | ".format(i, d[i]) for i in d] if d else '',["Total Profit : {}".format(profit)],["Max Drawdown : {}".format(drawdown)],["Sharpe Ratio : {}".format(sharpe)]]
