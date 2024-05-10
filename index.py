# Current App in Progress
import dash
from dash import dcc, html, Input, Output, State, dash_table, ALL, Dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import flask
from dash.dash_table import DataTable
from utilities.data_prep import load_and_prepare_data
from config import freq_choices, sev_choices
from components.claims_analysis_tables import (
    create_claimsreg_pivot, create_validclaims_pivot, create_claimsloss_pivot,
    create_numinj_pivot, create_grossclaims_pivot, create_avgclaimnumclaims_pivot,
    create_avgclaiminj_pivot, create_paidunder_pivot, create_legalclaims_pivot,
    create_legalclaimsnoclaims_pivot, create_amtlegalclaimsnoclaims_pivot,
    create_legalcostpmt_pivot, create_liabcostpmt_pivot
)

from callbacks.login_cbk import login_callback
from callbacks.claims_simulation_cbk import claims_distribution_callback
from callbacks.claims_simulation_cbk import claims_simulation_callback
from callbacks.claims_simulation_cbk import gross_claims_simulation
from callbacks.claims_simulation_cbk import simulation_accordion
from components.claims_analysis_graphs import (
    create_claims_chart, create_avginj_chart,
    create_legalcost_chart, create_avgclaim_chart, create_avgclaiminj_chart,
    create_avglegalcost_chart
)

from callbacks.claims_analysis_cbk import claim_analysis_callbacks
from utilities.data_prep import processed_data

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True, use_pages=True)

server = app.server


df = processed_data()

custom_order = ['10K', '20K', '30K', '50K', '80K', '100K',
                '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']


# Define the main app layout

app.layout = dbc.Container([
    dbc.Row([
            dbc.Col([
                # This creates a header where the image is part of the heading and links to a website.
                html.H1([
                    html.A([
                    ], href="https://www.xivoniactuaries.com"),  # Link to the website
                    "Underwriting Workbench"
                ], className='maintext'),

            ], width=6, className='mx-auto'),
            ], className='mt-4 gray_text'),
    html.Br(),
    html.Hr(),

    dcc.Location(id='url', refresh=False),
    dash.page_container
])


# Login Callback
login_callback(app)

# Claims Analysis Callbacks
claim_analysis_callbacks(app)

# Claims Analysis Graphs Callbacks
create_claims_chart(df)
create_avginj_chart(df)
create_legalcost_chart(df)
create_avgclaim_chart(df)
create_avgclaiminj_chart(df)
create_avglegalcost_chart(df)

# Claims Analysis Pivot Tables Callbacks
create_claimsreg_pivot(df)
create_validclaims_pivot(df)
create_claimsloss_pivot(df)
create_numinj_pivot(df)
create_grossclaims_pivot(df)
create_avgclaimnumclaims_pivot(df)
create_avgclaiminj_pivot(df)
create_paidunder_pivot(df)
create_legalclaims_pivot(df)
create_legalclaimsnoclaims_pivot(df)
create_amtlegalclaimsnoclaims_pivot(df)
create_legalcostpmt_pivot(df)
create_liabcostpmt_pivot(df)

# Claims Distribution Chart
claims_distribution_callback(app)

# Claim Simulation Chart
claims_simulation_callback(app)
gross_claims_simulation(app)
simulation_accordion(app)
