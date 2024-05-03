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
dash.register_page(__name__, path='/claims_analysis')

nav = dbc.Row([
dbc.Col(html.Img(src="https://www.xivoniactuaries.com/images/Xivoni%20Logo%20No%20Text.png", height="30px"), width=1),
dbc.Col(
dbc.Nav(
    [   
     dbc.NavLink("Claims Analysis", active=True, href="/claims_analysis"),
     dbc.NavLink("Claims Distribution", href="/claims_distribution")
    ],pills=True,
))
], align='center', className='my-3')

layout = dbc.Container([
    nav,

    dbc.Row([
         
        #Charts and tabs to the right
        dbc.Col([
            
            
            dbc.Row(
            dcc.Tabs(id='tabs-example', children=[
                
                dcc.Tab(label='Claims Analysis Graphs', children=[
                    dcc.Dropdown(
                        id='charts-dropdown',
                        options=[
                            {'label': 'Number of Claims', 'value': 'claims_chart'},
                            {'label': 'Claims Distribution', 'value': 'distribution_chart'},
                            {'label': 'Average Number of Injured', 'value': 'avginj_chart'},
                            {'label': 'Total Gross Claims', 'value': 'legalcost_chart'},
                            {'label': 'Average Claim', 'value': 'avgclaim_chart'},
                            {'label': 'Average Claims', 'value': 'avgclaiminj_chart'},
                            {'label': 'Average Legal Cost', 'value': 'avglegalcost_chart'}
                        ],
                        multi=True,
                        value=[]  # Default selection
                    ),
                    html.Div(id='charts-content')
                ]),
                dcc.Tab(label='Pivot Tables', children=[
                    dcc.Dropdown(
                        id='tables-dropdown',
                        options=[
                            {'label': 'Claims Registered', 'value': 'claimsreg_piv'},
                            {'label': 'Valid Claims', 'value': 'validclaims_piv'},
                            {'label': 'Claims Loss', 'value': 'claimsloss_piv'},
                            {'label': 'Number of Injured', 'value': 'numinj_piv'},
                            {'label': 'Gross Claims', 'value': 'grossclaims_piv'},
                            {'label': 'Average Claim per Number of Claims', 'value': 'avgclaimnumclaims_piv'},
                            {'label': 'Average Claim per Injured', 'value': 'avgclaiminj_piv'},
                            {'label': 'Paid by Underwriter', 'value': 'paidunder_piv'},
                            {'label': 'Legal Claims', 'value': 'legalclaims_piv'},
                            {'label': 'Legal Claims where there were no claims', 'value': 'legalclaimsnoclaims_piv'},
                            {'label': 'Amount of legal claims where there were no claims', 'value': 'amtlegalclaimsnoclaims_piv'},
                            {'label': 'Legal cost payment', 'value': 'legalcostpmt_piv'},
                            {'label': 'Liability Cost payment', 'value': 'liabcostpmt_piv'}
                        ],
                        multi=True,
                        value=[]  # Default no selection
                    ),
                    html.Div(id='tables-content')
                ]),
                
                
                dcc.Tab(label="Download", children=[
                    html.Button("Download Claims", id="download_claims"),
                    dcc.Download(id="download_data")
                ])
                
            ]))
        ])
    ]),
    
    
], fluid=True)