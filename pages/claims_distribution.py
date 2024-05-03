import dash
from dash import dcc, html, Input, Output, State, dash_table, ALL, Dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from dash.dash_table import DataTable
from DataPrep import load_and_prepare_data
from simulation import run_freq_sev_simulation
from config import freq_choices, sev_choices
from Graphs import (
    create_claims_chart, create_distribution_chart, create_avginj_chart,
    create_legalcost_chart, create_avgclaim_chart, create_avgclaiminj_chart,
    create_avglegalcost_chart
)
from Tables import (
    create_claimsreg_pivot, create_validclaims_pivot, create_claimsloss_pivot,
    create_numinj_pivot, create_grossclaims_pivot, create_avgclaimnumclaims_pivot,
    create_avgclaiminj_pivot, create_paidunder_pivot, create_legalclaims_pivot,
    create_legalclaimsnoclaims_pivot, create_amtlegalclaimsnoclaims_pivot,
    create_legalcostpmt_pivot, create_liabcostpmt_pivot
)



# Register this page in the app
dash.register_page(__name__, path='/claims_distribution')


nav = dbc.Row([
dbc.Col(html.Img(src="https://www.xivoniactuaries.com/images/Xivoni%20Logo%20No%20Text.png", height="30px"), width=1),
dbc.Col(
dbc.Nav(
    [   
     dbc.NavLink("Claims Analysis", href="/claims_analysis"),
     dbc.NavLink("Claims Distribution", active=True, href="/claims_distribution")
    ],pills=True,
))
], align='center', className='my-3')


layout = dbc.Container([
    nav,


    dbc.Row([
        #Add Code for simulation interface here
        dbc.Col(width=3, children=[
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                    dbc.Button("Run Simulation", id="run_freq", color="primary", className="btn-block nobreak runsim"), justify='center'),
                    html.Br(),
                    html.Br(),
                    html.Label("Number of Observations:", className="form-label"),
                    dcc.Slider(id="obs", min=1000, max=10000, value=2000, step=1000, marks=None, tooltip={"placement": "bottom", "always_visible": True}),
                    html.Br(),
                    html.Hr(),
                    html.H5("Frequency", className='text-center mb-4'),
                    html.Label("Frequency Distribution:", className="form-label"),
                    dcc.Dropdown(
                        id='freq_dist_dropdown',
                        options=[{'label': k, 'value': v} for k, v in freq_choices.items()],
                        value='poisson',
                        clearable=False
                    ),
                    html.Br(),
                    html.Div(id='freq_param_inputs'),
                    html.Br(),
                    html.Div(id="freq_summary_stats"),
                    html.Br(),
                    html.Hr(),
                    html.H5("Severity", className='text-center mb-4'),
                    html.Label("Severity Distribution:", className="form-label"),
                    dcc.Dropdown(
                        id='sev_dist_dropdown',
                        options=[{'label': k, 'value': v} for k, v in sev_choices.items()],
                        value='lognormal',
                        clearable=False
                    ),
                    html.Br(),
                    html.Div(id='sev_param_inputs'),
                    html.Br(),
                    html.Div(id="sev_summary_stats"),
                ])
            ])
        ]),       


        
        #Charts and tabs to the right
        dbc.Col([
            
# Add code for retention limits here

    dbc.Row([
        html.H4("Retention Limits", className='text-center mb-4 white_text'),
            dbc.Col([
            html.Label("Per Claim Retention Limit:", className="form-label white_text"),
            dbc.Input(id="specific_lim", type="number", placeholder="Per Claim Limit", value=250000)], width=4),
            #html.Br(),
            dbc.Col([
            html.Label("Aggregate Retention Limit:", className="form-label white_text"),
            dbc.Input(id="agg_lim", type="number", placeholder="Aggregate Limit", value=750000)], width=4),
    ], className='mb-4 bg_colour py-3 rounded', justify='center'),
            

            
            
            dbc.Row(
            dcc.Tabs(id='tabs-example', children=[
                
                dcc.Tab(label="Histograms", children=[
                    dcc.Graph(id="hist_plot"),
                    html.Label("Confidence Interval:", className="form-label"),
                    dcc.Slider(id="ci", min=0.25, max=1.0, value=0.95, step=0.01, marks={i/100: str(i/100) for i in range(25, 101, 5)}, tooltip={"placement": "bottom", "always_visible": True}),
                    dcc.Graph(id="hist_plot_total"),
                    dcc.Graph(id="hist_plot_ceded")
                ]),
                
                dcc.Tab(label="Confidence Levels", children=[
                    DataTable(
                        id='confidence_table',
                        columns=[
                            {'name': 'Confidence Level', 'id': 'conf_level'},
                            {'name': 'Value at Risk', 'id': 'value_at_risk'}
                        ],
                        data=[],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left'},
                    )
                ]),
                
                dcc.Tab(label="Download", children=[
                    html.Button("Download Claims", id="download_claims"),
                    dcc.Download(id="download_data")
                ])
                
            ]))
        ], width=9)
    ]),
    
], fluid=True)
