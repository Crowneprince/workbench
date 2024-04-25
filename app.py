#Current App in Progress
import dash
from dash import Dash, html, dcc, Input, Output, dash_table, State
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

# Define the path and sheet name
file_path = "Premium_Model_Data.xlsx"
sheet_name = 'Data'

# Load and prepare the data
df = load_and_prepare_data(file_path, sheet_name)

# Initialize the Dash app with Bootstrap stylesheet
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server =app.server


# App layout
app.layout = dbc.Container([
   
        dbc.Row([
            dbc.Col([
                # This creates a header where the image is part of the heading and links to a website.
                html.H1([
                    html.A([
                        html.Img(
                            src="https://www.xivoniactuaries.com/images/Xivoni%20Logo%20No%20Text.png",  # Replace with your image URL
                            style={'height': '50px'}  # Adjust dimensions as needed
                        )
                    ], href="https://www.xivoniactuaries.com"),  # Link to the website
                    "Underwriting Workbench"
                ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'})
            ])
        ], className='mt-4 mb-5 gray_text'),
    
    #Create the simulation interface column
    

    dbc.Row([
        #Add Code for simulation interface here
        dbc.Col(width=3, children=[
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                    dbc.Button("Run Simulation", id="run_freq", color="primary", className="btn-block"), width=5 ), justify='center'),
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
    ])
], fluid=True)

@app.callback(
    Output('charts-content', 'children'),
    Input('charts-dropdown', 'value')
)
def update_charts(selected_charts):
    charts = {
        'claims_chart': dcc.Graph(figure=create_claims_chart(df)),
        'distribution_chart': dcc.Graph(figure=create_distribution_chart(df)),
        'avginj_chart': dcc.Graph(figure=create_avginj_chart(df)),
        'legalcost_chart': dcc.Graph(figure=create_legalcost_chart(df)),
        'avgclaim_chart': dcc.Graph(figure=create_avgclaim_chart(df)),
        'avgclaiminj_chart': dcc.Graph(figure=create_avgclaiminj_chart(df)),
        'avglegalcost_chart': dcc.Graph(figure=create_avglegalcost_chart(df))
    }
    return [charts[chart] for chart in selected_charts if chart in charts]

@app.callback(
    Output('tables-content', 'children'),
    Input('tables-dropdown', 'value')
)
def update_tables(selected_tables):
    tables_functions = {
        'claimsreg_piv': create_claimsreg_pivot,
        'validclaims_piv': create_validclaims_pivot,
        'claimsloss_piv': create_claimsloss_pivot,
        'numinj_piv': create_numinj_pivot,
        'grossclaims_piv': create_grossclaims_pivot,
        'avgclaimnumclaims_piv': create_avgclaimnumclaims_pivot,
        'avgclaiminj_piv': create_avgclaiminj_pivot,
        'paidunder_piv': create_paidunder_pivot,
        'legalclaims_piv': create_legalclaims_pivot,
        'legalclaimsnoclaims_piv': create_legalclaimsnoclaims_pivot,
        'amtlegalclaimsnoclaims_piv': create_amtlegalclaimsnoclaims_pivot,
        'legalcostpmt_piv': create_legalcostpmt_pivot,
        'liabcostpmt_piv': create_liabcostpmt_pivot
    }
    children = []
    for table_key in selected_tables:
        if table_key in tables_functions:
            df_table = tables_functions[table_key](df)
            df_table.columns = [str(col) for col in df_table.columns]  # Ensure column names are strings
            table_component = dash_table.DataTable(
                data=df_table.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df_table.columns],
                page_size=15,
                style_table={'overflowX': 'auto'},
                style_data={
                    'textAlign': 'center',
                    'border-bottom': '1px',
                    'border-right': '0px'
                },
                style_header={
                    'textAlign': 'center',
                    'border-bottom': '1px'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgba(0,0,0,.05)'
                    }
                ]
            )
            table_title = table_key.replace('_piv', '').replace('_', ' ').title()
            children.append(html.H3(table_title, style={'textAlign': 'center', 'marginTop': 20}))
            children.append(table_component)
    return children



# Callback for frequency summary statistics
@app.callback(
    Output('freq_summary_stats', 'children'),
    [Input('freq_dist_dropdown', 'value')],
    [State('obs', 'value')]
)
def update_freq_summary_stats(freq_dist, obs):
    # Hardcoded parameters for testing
    freq_params = {'lambda': 10} if freq_dist == 'poisson' else {'n': 10, 'p': 0.5}

    # Calculate summary statistics
    if freq_dist == 'poisson':
        mean = round(freq_params['lambda'], 2)
        std_dev = round(np.sqrt(freq_params['lambda']), 2)
    elif freq_dist == 'binomial':
        mean = round(freq_params['n'] * freq_params['p'], 2)
        std_dev = round(np.sqrt(freq_params['n'] * freq_params['p'] * (1 - freq_params['p'])), 2)
    elif freq_dist == 'nbinomial':
        mean = round(freq_params['n'] * (1 - freq_params['p']) / freq_params['p'], 2)
        std_dev = round(np.sqrt(freq_params['n'] * (1 - freq_params['p']) / (freq_params['p'] ** 2)), 2)

    return html.Div([
        html.P(f"Mean: {mean}"),
        html.P(f"Standard Deviation: {std_dev}")
    ])

# Callback for severity summary statistics
@app.callback(
    Output('sev_summary_stats', 'children'),
    [Input('sev_dist_dropdown', 'value')],
    [State('obs', 'value')]
)
def update_sev_summary_stats(sev_dist, obs):
    # Hardcoded parameters for testing
    sev_params = {'mu': 2, 'sigma': 1} if sev_dist == 'lognormal' else {'alpha': 3, 'scale': 1}

    # Calculate summary statistics
    if sev_dist == 'lognormal':
        mean = round(np.exp(sev_params['mu'] + (sev_params['sigma'] ** 2) / 2), 2)
        std_dev = round(np.sqrt((np.exp(sev_params['sigma'] ** 2) - 1) * np.exp(2 * sev_params['mu'] + sev_params['sigma'] ** 2)), 2)
    elif sev_dist == 'pareto':
        mean = round(sev_params['scale'] * sev_params['alpha'] / (sev_params['alpha'] - 1), 2)
        std_dev = round(sev_params['scale'] * np.sqrt(sev_params['alpha'] / ((sev_params['alpha'] - 2) * (sev_params['alpha'] - 1) ** 2)), 2)
    elif sev_dist == 'weibull':
        mean = round(sev_params['scale'] * np.gamma(1 + 1 / sev_params['a']), 2)
        std_dev = round(sev_params['scale'] * np.sqrt(np.gamma(1 + 2 / sev_params['a']) - (np.gamma(1 + 1 / sev_params['a']) ** 2)), 2)
    elif sev_dist == 'gamma':
        mean = round(sev_params['shape'] * sev_params['scale'], 2)
        std_dev = round(np.sqrt(sev_params['shape']) * sev_params['scale'], 2)
    elif sev_dist == 'exponential':
        mean = round(sev_params['scale'], 2)
        std_dev = round(sev_params['scale'], 2)

    return html.Div([
        html.P(f"Mean: {mean}"),
        html.P(f"Standard Deviation: {std_dev}")
    ])


# Callback for updating severity parameters
@app.callback(
    Output('sev_param_inputs', 'children'),
    [Input('sev_dist_dropdown', 'value')]
)
def update_sev_params(sev_dist):
    if sev_dist == "lognormal":
        return [
            html.Div([
                html.Label("Mu (Mean of log):", className="form-label"),
                dbc.Input(id="mu", type="number", placeholder="Mu", value=2)
            ]),
            html.Div([
                html.Label("Sigma (Standard deviation of log):", className="form-label"),
                dbc.Input(id="sigma", type="number", placeholder="Sigma", value=1)
            ])
        ]
    elif sev_dist == "pareto":
        return [
            # Inputs for Pareto distribution parameters
        ]
    elif sev_dist == "weibull":
        return [
            # Inputs for Weibull distribution parameters
        ]
    elif sev_dist == "gamma":
        return [
            # Inputs for Gamma distribution parameters
        ]
    elif sev_dist == "exponential":
        return [
            # Inputs for Exponential distribution parameters
        ]

# Callback for updating frequency parameters
@app.callback(
    Output('freq_param_inputs', 'children'),
    [Input('freq_dist_dropdown', 'value')]
)
def update_freq_params(freq_dist):
    if freq_dist == "poisson":
        return [
            html.Div([
                html.Label("Lambda (Rate parameter):", className="form-label"),
                dbc.Input(id="lambda", type="number", placeholder="Lambda", value=10)
            ])
        ]
    elif freq_dist == "binomial":
        return [
            # Inputs for Binomial distribution parameters
        ]
    elif freq_dist == "nbinomial":
        return [
            # Inputs for Negative Binomial distribution parameters
        ]



@app.callback(
    [Output('hist_plot', 'figure'),
     Output('hist_plot_total', 'figure'),
     Output('hist_plot_ceded', 'figure'),
     Output('confidence_table', 'data')],
    [Input('run_freq', 'n_clicks')],
    [State('obs', 'value'),
     State('freq_dist_dropdown', 'value'),
     State('sev_dist_dropdown', 'value'),
     State('specific_lim', 'value'),
     State('agg_lim', 'value')]
)
def update_plots_and_table(n_clicks, obs, freq_dist, sev_dist, specific_lim, agg_lim):
    if n_clicks is None:
        return go.Figure(), go.Figure(), go.Figure(), []

    # Run the simulation
    total_losses = run_freq_sev_simulation(obs, freq_dist, sev_dist, {}, {})

    # Calculate retained losses (net of excess recoveries)
    retained_losses = [min(loss, specific_lim) for loss in total_losses]
    retained_losses = [loss if sum(retained_losses) <= agg_lim else 0 for loss in retained_losses]

    # Calculate gross losses (gross of excess recoveries)
    gross_losses = total_losses

    # Calculate ceded losses (excess recoveries)
    ceded_losses = [max(0, loss - specific_lim) for loss in total_losses]
    ceded_losses = [loss if sum(ceded_losses) <= agg_lim else 0 for loss in ceded_losses]

    # Create histogram plots
    hist_retained = go.Figure(data=[go.Histogram(x=retained_losses, xbins=dict(size=30))])
    hist_gross = go.Figure(data=[go.Histogram(x=gross_losses, xbins=dict(size=30))])
    hist_ceded = go.Figure(data=[go.Histogram(x=ceded_losses, xbins=dict(size=30))])

    # Define a common update layout function for all histograms
    def update_layout(figure, title, xaxis_title, yaxis_title):
        figure.update_traces(marker_color='#D1CC7B', marker_line_color='white', marker_line_width=1)
        figure.update_layout(
            title=title,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
            xaxis_showgrid=True,
            yaxis_showgrid=True,  # Only show horizontal gridlines
        )

    # Apply layout updates
    update_layout(hist_retained, 'Retained Losses: Net of Excess Recoveries', 'Net Loss', 'Number of Observations')
    update_layout(hist_gross, 'Gross Losses: Gross of Excess Recoveries', 'Gross Loss', 'Number of Observations')
    update_layout(hist_ceded, 'Ceded Losses: Excess Recoveries', 'Ceded Loss', 'Number of Observations')

    # Calculate confidence levels and value at risk
    confidence_levels = [0.75, 0.9, 0.95, 0.99]
    data = []
    for conf_level in confidence_levels:
        value_at_risk = np.quantile(total_losses, 1 - conf_level)
        data.append({'conf_level': f'{conf_level * 100}%', 'value_at_risk': value_at_risk})

    return hist_retained, hist_gross, hist_ceded, data


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
