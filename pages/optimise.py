import dash
from dash import * 
from dash.dependencies import Output, Input

import math
import json 
import pandas as pd
import numpy as np

from dist import strategies
from dist import data
from dist.engine import backtest, optimise, abstraction
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
                    children="optimiser", className="header-title"
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
                            id="o-ticker-filter",
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
                            id="o-interval-filter",
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
                            id="o-strategy-filter",
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
                            id="o-param-filter",
                            className="dropdown"
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Input", className="menu-title"),
                        dcc.Input(
                            id="o-param-input",
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
                                id="o-params-output",
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
                        id="o-price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=[
                        html.Div(
                            html.P(
                                id="o_profit",
                            ),
                            className="output card stats"
                        ),
                        html.Div(
                            html.P(
                                id="o_drawdown",
                            ),
                            className="output card stats"
                        ),
                        html.Div(
                            html.P(
                                id="o_sharpe",
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
    [Output("o-param-filter", "options")],
    [
        Input("o-strategy-filter", "value")
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
    [Output("o-price-chart", "figure"), Output("o-param-input", "value"), Output("o-params-output", "children"), Output("o_profit", "children"), Output("o_drawdown", "children"), Output("o_sharpe", "children")],
    [
       Input("o-ticker-filter", "value"),
       Input("o-interval-filter", "value"),
       Input("o-strategy-filter", "value"),
       Input("o-param-filter", "value"),
       Input("o-param-input", "value"),
    ],
)
def update_charts(ticker, interval, strat, param, paramval):
    global d

    strategy = eval(h[-1][strat])
    strat = strategy()

    if paramval and param: d[param] = paramval
    
    params = strat.params

    for param in d:
        params[param] = [int(i) for i in d[param].split(',')]
    
    print(params)

    strat = ''

    ## data abstraction
    p = abstraction.piston()
    spark = p.spark(interval)
    data = yf.download(ticker, period="5d", interval=spark)
    data = p.crank(data, interval)

    ## backtest
    par = [i for i in params]

    op = optimise.piston(strategy, params)
    optimise_result = op.crank(data, num_threads=4, status=False)

    
    best = optimise_result[0][-1]['param']


    bt = backtest.piston(strategy, data)
    out = bt.run(best)


    o_sharpe = 0
    o_profit = optimise_result[-1] - optimise_result[0][-1]['hist'][0]
    o_drawdown = min(optimise_result[0][-1]['hist']) - optimise_result[0][-1]['hist'][0]

    price_chart_figure = {
        "data": [
            {
                "x": [str(i) for i in range(len(res['hist']))],
                "y": res['hist'],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra> : "+str(res['param']),
            } for res in optimise_result[0][-10::]
        ],
        "layout": {
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return [price_chart_figure, '', ["{}".format(best)] if best else '',["Total Profit : ${}".format(round(o_profit, 2))],["Max Drawdown : ${}".format(round(o_drawdown),2)],["Sharpe Ratio : {}".format(o_sharpe)]]
