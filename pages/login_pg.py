import dash
from dash import dcc, html, Input, Output, State, dash_table, ALL, Dash
import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate



dash.register_page(__name__, path='/')


layout = dbc.Container([
    dcc.Location(id='url-login', refresh=True),
    dbc.Row([
        dbc.Col([
            dbc.Stack([
                html.Div(className='loginlogo mx-auto'),
                html.H2("Workbench", className='text-center'),
                html.P("Login to your account", className='text-center'),
                dbc.Input(id="username", type="text", placeholder="Enter your username", className='mx-auto logininputs'),
                dbc.Input(id="password", type="password", placeholder="Enter your password", className='mx-auto logininputs'),
                dbc.Button('Login', id='login-button', n_clicks=0, className='loginbtn mx-auto'),
                html.Div(id='login-output', style={'padding': '20px', 'max-width': '500px', 'margin': '0 auto'})
            ], gap=1)
        ], width=6, align='center'),
        dbc.Col(className='loginimg mt-4', width=6, align='center')  # Optionally add content or images here for the right column
    ], justify="around"),  # Centers the columns in the row
], fluid=True, className="h-100")  # Ensure full container height

