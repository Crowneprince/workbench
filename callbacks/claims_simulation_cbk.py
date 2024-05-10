from dash import dcc, html, Input, Output
import matplotlib.pyplot as plt
from utilities.data_prep import processed_data
import dash
from dash import dcc, html, Input, Output, State, dash_table, ALL, Dash, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import pandas as pd

df = processed_data()


def claims_distribution_callback(app):
    @app.callback(
        Output('claims-distribution-graph', 'figure'),
        Input('run_distr', 'n_clicks')
    )
    def update_graph(n_clicks):
        if n_clicks is None:
            # Optionally prevent the function from running until the button has been clicked
            return dash.no_update
        return create_distribution_chart(df)

    def create_distribution_chart(df):
        df_chart_2 = df[["Year", 'ClaimBands', "ClaimsLoss"]]
        df_chart_2 = df_chart_2.groupby(
            ['ClaimBands', 'Year']).sum().reset_index()
        total_claims_per_year = df_chart_2.groupby('Year')['ClaimsLoss'].sum()
        df_chart_2['%AnnClaim'] = df_chart_2.apply(lambda row: round(
            (row['ClaimsLoss'] / total_claims_per_year[row['Year']]), 2), axis=1)

        df_chart_2_trunc = df_chart_2[(df_chart_2['Year'] >= 2009) & (
            df_chart_2['Year'] <= 2019)]
        tot_claims_all_years = df_chart_2['ClaimsLoss'].sum()
        proportions = (df_chart_2.groupby('ClaimBands')[
                       'ClaimsLoss'].sum() / tot_claims_all_years).round(2)
        df_chart_2['AllYears'] = df_chart_2['ClaimBands'].map(proportions)

        four_year_df = df_chart_2[(df_chart_2['Year'] >= 2016) & (
            df_chart_2['Year'] <= 2019)]
        tot_claims_4_years = four_year_df['ClaimsLoss'].sum()
        four_year_proportions = (four_year_df.groupby('ClaimBands')[
                                 'ClaimsLoss'].sum() / tot_claims_4_years).round(2)
        df_chart_2['4Years'] = df_chart_2['ClaimBands'].map(
            four_year_proportions)

        df_chart_2_px = df_chart_2[(df_chart_2['Year'] >= 2009) & (
            df_chart_2['Year'] <= 2019)]
        custom_order = ['10K', '20K', '30K', '50K', '80K', '100K',
                        '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
        df_chart_2_px['ClaimBands'] = pd.Categorical(
            df_chart_2_px['ClaimBands'], categories=custom_order, ordered=True)
        df_chart_2_px = df_chart_2_px.sort_values(by=['Year', 'ClaimBands'])

        fig = go.Figure()
        colors = {'%AnnClaim': '#56626F',
                  'AllYears': '#ED9547', '4Years': '#EDC147'}
        for year in df_chart_2_px['Year'].unique():
            year_data = df_chart_2_px[df_chart_2_px['Year'] == year]
            fig.add_trace(go.Scatter(
                x=year_data['ClaimBands'],
                y=year_data['%AnnClaim'],
                mode='lines',
                name=f'{year}',
                line=dict(color=colors['%AnnClaim'], width=0.8),
                yaxis='y1'
            ))

        fig.add_trace(go.Scatter(
            x=year_data['ClaimBands'],
            y=year_data['4Years'],
            mode='lines',
            name='4 Years',
            line=dict(color=colors['4Years']),
            yaxis='y1'
        ))

        fig.add_trace(go.Scatter(
            x=year_data['ClaimBands'],
            y=year_data['AllYears'],
            mode='lines',
            name='All Years',
            line=dict(color=colors['AllYears']),
            yaxis='y1'
        ))

        fig.update_layout(
            xaxis=dict(type='category', categoryorder='array',
                       categoryarray=custom_order),
            yaxis=dict(tickformat='.0%', dtick=0.05, showgrid=True, gridcolor='lightgrey',
                       gridwidth=0.5, zeroline=True, zerolinecolor='black', zerolinewidth=1),
            legend=dict(x=0.5, y=-0.15, xanchor='center',
                        yanchor='top', orientation='h'),
            plot_bgcolor='white', font=dict(family="Tw Cen MT", size=12, color="black")
        )

        return fig


# Claim Simulation


def claims_simulation_callback(app):
    @app.callback(
        Output('claims-simulation-graph', 'figure'),
        Input('run_claimsim', 'n_clicks')
    )
    def update_graph(n_clicks):
        if n_clicks is None:
            # Prevent the function from running until the button has been clicked
            return dash.no_update

        df_sim, stats, total_claims = main(600)
        fig = create_claims_chart(df_sim)
        return fig

    def claim_bands():
        bands = [
            (0, 10000, '10K'), (10000, 20000, '20K'), (20000, 30000, '30K'),
            (30000, 50000, '50K'), (50000, 80000, '80K'), (80000, 100000, '100K'),
            (100000, 150000, '150K'), (150000, 250000,
                                       '250K'), (250000, 500000, '500K'),
            (500000, 750000, '750K'), (750000,
                                       1000000, '1M'), (1000000, 2000000, '2M'),
            (2000000, 5000000, '5M'), (5000000, 10000000,
                                       '10M'), (10000000, 100000000, '100M')
        ]
        probabilities = {
            '10K': 0.014, '20K': 0.023, '30K': 0.026, '50K': 0.039, '80K': 0.048,
            '100K': 0.015, '150K': 0.046, '250K': 0.082, '500K': 0.304, '750K': 0.204,
            '1M': 0.068, '2M': 0.061, '5M': 0.032, '10M': 0.033, '100M': 0.005
        }
        return bands, probabilities

    def simulate_claims_with_band_probability(n_simulations, bands, band_probabilities):
        claims = []
        band_labels = [band[2] for band in bands]
        probabilities = [band_probabilities[label] for label in band_labels]

        for _ in range(n_simulations):
            selected_band_label = np.random.choice(
                band_labels, p=probabilities)
            selected_band = next(
                band for band in bands if band[2] == selected_band_label)
            min_val, max_val = selected_band[0], selected_band[1]
            claim = np.random.uniform(min_val, max_val)
            claims.append((selected_band_label, claim))

        return claims

    def main(n_simulations=600):
        bands, probabilities = claim_bands()
        simulated_claims = simulate_claims_with_band_probability(
            n_simulations, bands, probabilities)

        label_categories = [band[2] for band in bands]
        labels = [claim[0] for claim in simulated_claims]
        counts = {label: labels.count(label) for label in label_categories}
        total_claims = [claim[1] for claim in simulated_claims]

        df_sim = pd.DataFrame({
            'Category': list(counts.keys()),
            'Frequency': list(counts.values())
        })

        return df_sim, None, None  # Stats and total_claims are not used in the plotting

    def create_claims_chart(df_sim):
        claim_band_order = ['10K', '20K', '30K', '50K', '80K', '100K',
                            '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
        df_sim['Category'] = pd.Categorical(
            df_sim['Category'], categories=claim_band_order, ordered=True)
        df_sim = df_sim.sort_values('Category')

        fig = go.Figure(data=[
            go.Bar(x=df_sim['Category'], y=df_sim['Frequency'],
                   text=df_sim['Frequency'],  # Set text equal to values
                   textposition='auto',  # 'auto' places the text inside the bars automatically
                   marker_color='#1F1F74')  # You can customize the bar color
        ])

        fig.update_layout(
            xaxis_title='Claim Band',
            plot_bgcolor='white'
        )
        return fig


# Gross Claims Simulation


def gross_claims_simulation(app):
    @app.callback(
        Output('gross-simulation-graph', 'figure'),
        Input('run_gross_sim', 'n_clicks')
    )
    def update_graph(n_clicks):
        if n_clicks is None:
            # Prevent the function from running until the button has been clicked
            return dash.no_update
        fig, stats = main()
        print(f"Max Gross Claim Incurred: {stats['max_claim']:,.2f}")
        print(f"Min Gross Claim Incurred: {stats['min_claim']:,.2f}")
        print(f"Avg Gross Claim Incurred: {stats['avg_claim']:,.2f}")
        return fig

    def claim_bands():
        bands = [
            (0, 10000, '10K'), (10000, 20000, '20K'), (20000, 30000, '30K'),
            (30000, 50000, '50K'), (50000, 80000, '80K'), (80000, 100000, '100K'),
            (100000, 150000, '150K'), (150000, 250000,
                                       '250K'), (250000, 500000, '500K'),
            (500000, 750000, '750K'), (750000,
                                       1000000, '1M'), (1000000, 2000000, '2M'),
            (2000000, 5000000, '5M'), (5000000, 10000000,
                                       '10M'), (10000000, 100000000, '100M')
        ]
        probabilities = {
            '10K': 0.014, '20K': 0.023, '30K': 0.026, '50K': 0.039, '80K': 0.048,
            '100K': 0.015, '150K': 0.046, '250K': 0.082, '500K': 0.304, '750K': 0.204,
            '1M': 0.068, '2M': 0.061, '5M': 0.032, '10M': 0.033, '100M': 0.005
        }
        return bands, probabilities

    def simulate_claims_with_band_probability(n_simulations, bands, band_probabilities):
        claims = []
        band_labels = [band[2] for band in bands]
        probabilities = [band_probabilities[label] for label in band_labels]

        for _ in range(n_simulations):
            selected_band_label = np.random.choice(
                band_labels, p=probabilities)
            selected_band = next(
                band for band in bands if band[2] == selected_band_label)
            claim = np.random.uniform(selected_band[0], selected_band[1])
            claims.append(claim)

        return claims

    def main():
        bands, probabilities = claim_bands()
        n_iterations = 100
        n_simulations = 600

        results_df = pd.DataFrame(
            columns=['SimulationYear', 'GrossClaimIncurred'])
        for year in range(1, n_iterations + 1):
            simulated_claims = simulate_claims_with_band_probability(
                n_simulations, bands, probabilities)
            gross_claim_incurred = np.sum(simulated_claims)
            results_df.loc[year - 1] = [year, gross_claim_incurred]

        fig = go.Figure(data=[
            go.Scatter(
                x=results_df['SimulationYear'],
                y=results_df['GrossClaimIncurred'],
                mode='markers',
                marker=dict(color='blue'),
                name='Gross Claims'
            )
        ])
        fig.update_layout(
            xaxis_title='Simulation Year',
            yaxis_title='Gross Claim Incurred',
            plot_bgcolor='white',
            legend_title="Legend"
        )

        # Calculate stats
        stats = {
            'max_claim': results_df['GrossClaimIncurred'].max(),
            'min_claim': results_df['GrossClaimIncurred'].min(),
            'avg_claim': results_df['GrossClaimIncurred'].mean()
        }

        return fig, stats


def simulation_accordion(app):
    @app.callback(
        Output("accordion-contents-open-ids", "children"),
        [Input("accordion-always-open", "active_item")],
    )
    def change_item(item):
        return f"Item(s) selected: {item}"
