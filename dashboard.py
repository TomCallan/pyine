# home page, background ticker loading and such

from dash import Dash, dcc, html, Input, Output, callback
from pages import backtest, optimise


app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content',
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
                        html.Div(children="Backtester", className="menu-title"),
                        html.Button('', id='submit-val', n_clicks=0),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Optimiser", className="menu-title"),
                        html.Button('', id='optimiser', n_clicks=0),
                    ]
                ),
            ],
            className="menu",
        ),
        ],
    ),
])


@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/optimiser':
        return optimise.layout
    elif pathname == '/backtester':
        return backtest.layout
    else:
        return app.layout

if __name__ == '__main__':
    app.run_server(debug=True)