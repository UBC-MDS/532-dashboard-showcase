import dash_vega_components as dvc
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table

from data import cars

print('comp file')
# Components
title = html.H1(
    'My splashboard demo',
    style={
        'backgroundColor': 'steelblue',
        'padding': 20,
        'color': 'white',
        'margin-top': 20,
        'margin-bottom': 20,
        'text-align': 'center',
        'font-size': '48px',
        'border-radius': 3,
        'margin-left': -10,  # Align with sidebar
    }
)

table = dbc.Col(
    dash_table.DataTable(
        id='table',
        # The data and columns parameters are set in the callback instead
        column_selectable="single",
        selected_columns=['Miles_per_Gallon'], 
        page_size=8,
        sort_action='native',
        filter_action='native',
        style_data_conditional=[{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }],
         style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_as_list_view=True,
        editable=True,
    ),
)

dropdown = dcc.Dropdown(
    id='dropdown',
    options=cars.columns,
    value=['Name', 'Miles_per_Gallon', 'Horsepower'],
    multi=True
)

density = dbc.Card([
    dbc.CardHeader('Density', style={'fontWeight': 'bold'}),
    dbc.CardBody(
        dvc.Vega(
            id='scatter',
            opt={'actions': False},  # Remove the three dots button
            style={'width': '100%'}
        )
    )
])

histogram = dbc.Card([
    dbc.CardHeader('Histrogram', style={'fontWeight': 'bold'}),
    dbc.CardBody(
        dvc.Vega(
            id='histogram',
            opt={'actions': False},  # Remove the three dots button
            style={'width': '100%'}
        )
    )
])

sidebar = dbc.Col([
    html.H5('Global controls'),
    html.Br(),
    dropdown,
    html.Br(),
    dcc.Dropdown(),
    html.Br(),
    dcc.Dropdown(),
    ],
    md=3,
    style={
        'background-color': '#e6e6e6',
        'padding': 10,
        'border-radius': 3,
    }
) 


