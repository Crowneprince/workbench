# Current App in Progress
import dash
from dash import dcc, html, Input, Output, State, dash_table, ALL, Dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
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
from components.claims_analysis_graphs import (
    create_claims_chart, create_distribution_chart, create_avginj_chart,
    create_legalcost_chart, create_avgclaim_chart, create_avgclaiminj_chart,
    create_avglegalcost_chart
)

# Define the path and sheet name
file_path = "Premium_Model_Data.xlsx"
sheet_name = 'Data'

# Load and prepare the data
df = load_and_prepare_data(file_path, sheet_name)


def claim_analysis_callbacks(app):
    @app.callback(
        Output('charts-content', 'children'),
        Input('charts-dropdown', 'value')
    )
    def update_charts(selected_charts):
        charts = {
            'claims_chart': dcc.Graph(figure=create_claims_chart(df)),
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
                # Ensure column names are strings
                df_table.columns = [str(col) for col in df_table.columns]
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
                table_title = table_key.replace(
                    '_piv', '').replace('_', ' ').title()
                children.append(html.H3(table_title, style={
                                'textAlign': 'center', 'marginTop': 20}))
                children.append(table_component)
        return children
