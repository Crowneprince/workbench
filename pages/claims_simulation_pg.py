from utilities.data_prep import processed_data
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from dash.exceptions import PreventUpdate

# Import statistical tools if needed
from scipy.stats import poisson, binom, nbinom, lognorm, gamma, expon, weibull_min

# Register this page in the app
dash.register_page(__name__, path='/claims_simulation_pg')

nav = dbc.Row(
    [
        dbc.Col(html.Img(
            src="https://www.xivoniactuaries.com/images/Xivoni%20Logo%20No%20Text.png", height="30px"), width=1),
        dbc.Col(
            dbc.Nav(
                [
                    dbc.NavLink("Claims Analysis", href="/claims_analysis_pg"),
                    dbc.NavLink("Claims Simulation", active=True,
                                href="/claims_simulation_pg"),
                    dbc.NavLink("Frequency/Severity", href="/freq_sev_pg")
                ], pills=True,
            )
        )
    ], align='center', className='my-3'
)

layout = dbc.Container(
    [
        nav,
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dbc.Row(
                            dbc.Col(
                                [
                                    html.H2("Claims Distribution Chart"),
                                    dbc.Button(
                                        "Run", id="run_distr", color="primary", className="btn-block nobreak rundistsim"),
                                    dcc.Graph(id='claims-distribution-graph')
                                ],
                                width=12, className='text-center'
                            )
                        )
                    ],
                    title="Claims Distribution"
                ),

                dbc.AccordionItem(
                    [
                        dbc.Row(
                            dbc.Col(
                                [
                                    html.H2("Claims Simulation"),
                                    dbc.Button(
                                        "Run", id="run_claimsim", color="primary", className="btn-block nobreak rundistsim"),
                                    dcc.Graph(id='claims-simulation-graph')
                                ],
                                width=12, className='text-center'
                            )
                        )
                    ],
                    title="Claims Simulation"
                ),

                dbc.AccordionItem(
                    [
                        dbc.Row(
                            dbc.Col(
                                [
                                    html.H2("Gross Claims Simulation"),
                                    dbc.Button(
                                        "Run", id="run_gross_sim", color="primary", className="btn-block nobreak rundistsim"),
                                    dcc.Graph(id='gross-simulation-graph')
                                ],
                                width=12, className='text-center'
                            )
                        )
                    ],
                    title="Gross Claims Simulation"
                )
            ],
            start_collapsed=True  # Start with all accordion items collapsed
        )
    ], fluid=True
)
