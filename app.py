import dash
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
from DataPrep import load_and_prepare_data
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
        ], className='mt-3 mb-5'),
    
    #Create the simulation interface column
    

    dbc.Row([
        #Simulaiton interface to the left
        dbc.Col([
            dbc.Button("Run simulation", color="dark", className="me-1 mb-4"),
            html.P('Number of observations', className='text-center'),
            dcc.Slider(0, 20, 5, value=10, id='my-slider'),
            html.Hr(),
            html.H4('Frequency', className='text-center'),
            dbc.Row(html.Div([dbc.Label("Distribution"), dbc.Input(placeholder="Input goes here...", type="text")])),
            html.Hr(),
            html.H4('Severity', className='text-center'),
            dbc.Row(html.Div([dbc.Label("Distribution"), dbc.Input(placeholder="Input goes here...", type="text")])),

            ], className='bg_colour pt-4 text-center'),
        
        #Charts and tabs to the right
        dbc.Col([
            
            dbc.Row([
                dbc.Row(html.H4('Retention', className='text-center')),
                dbc.Col(html.Div([dbc.Label("Per Claim"),
                                  dbc.Input(placeholder="Input goes here...", type="text")]), width=4),
                dbc.Col(html.Div([dbc.Label("Aggregate (per observation"),
                                  dbc.Input(placeholder="Input goes here...", type="text")]), width=4)

                    
                    ], className='mb-5 bg_colour pb-4 pt-3 gx-3', justify='center'),
            
            dbc.Row(
            dcc.Tabs(id='tabs-example', children=[
                dcc.Tab(label='Charts', children=[
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
                        value=['distribution_chart']  # Default selection
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
                        value=['claimsreg_piv']  # Default no selection
                    ),
                    html.Div(id='tables-content')
                ])
            ]))
        ], width=9)
    ])
])

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
                page_size=15
            )
            table_title = table_key.replace('_piv', '').replace('_', ' ').title()
            children.append(html.H3(table_title, style={'textAlign': 'center', 'marginTop': 20}))
            children.append(table_component)
    return children

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
