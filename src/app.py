from dash import Dash
import dash_bootstrap_components as dbc

import callbacks  # This import is necessary to register the callbacks
from components import title, sidebar, table, histogram, density


print('app file')
# Initialization
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
server = app.server

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
    dbc.Row([
        sidebar,  # Already wrapped in dbc.Col
        dbc.Col([
            table, # Already wrapped in dbc.Col
            dbc.Row([
                dbc.Col(histogram),
                dbc.Col(density),
            ])
        ],
        md=9
        ),
    ])
])


if __name__ == '__main__':
    app.run(debug=True)
