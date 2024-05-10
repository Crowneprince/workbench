import plotly.graph_objects as go

def create_claims_chart(df):
        # Data preparation and processing
        df_chart_1 = df[["Year", "ClaimsID", 'PaidOpenClaims']]
        df_chart_1 = df_chart_1.groupby(by="Year").sum()
        df_chart_1["%ValidClaims"] = (df_chart_1["PaidOpenClaims"] / df_chart_1["ClaimsID"]).round(2)
        df_chart_1 = df_chart_1.reset_index()
        
        # Prepare labels for percentages
        rounded_percentages = (df_chart_1['%ValidClaims'] * 100).round().fillna(0).astype(int)
        percentage_labels = [f"{x}%" for x in rounded_percentages]
        df_chart_1['Percentage Labels'] = percentage_labels
    
        # Create the Plotly figure
        fig = go.Figure()
    
        # Add bar trace for valid claims percentages
        fig.add_trace(
            go.Bar(
                x=df_chart_1['Year'],
                y=df_chart_1['%ValidClaims'],
                name='% Valid Claims',
                yaxis='y1',
                marker_color='#56626F',
                text=percentage_labels,
                textposition='outside',
                textfont=dict(size=10, color='#56626F')
            )
        )
    
        # Add line traces for total and valid claims
        fig.add_trace(
            go.Scatter(
                x=df_chart_1['Year'],
                y=df_chart_1['ClaimsID'],
                name='Claims Registered',
                yaxis='y2',
                marker_color='#ED9547'
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_chart_1['Year'],
                y=df_chart_1['PaidOpenClaims'],
                name='Valid Claims',
                yaxis='y2',
                marker_color='#EDC147'
            )
        )
    
        # Update layout to be responsive and maintain aspect ratio
        fig.update_layout(
            xaxis=dict(
                title="Claim Year",
                tickfont=dict(size=11, color='#56626F'),
                type='category'
            ),
            yaxis=dict(
                showticklabels=False,
                tickfont=dict(size=11),
                tickformat='.0%',
                side='left',
            ),
            yaxis2=dict(
                title='Number of Claims',
                tickfont=dict(size=11),
                overlaying='y', 
                side='right',
                showgrid=True,
                gridcolor='lightgrey',
                gridwidth=0.5,
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1
            ),
            font=dict(
                family="Tw Cen MT",
                size=12,
                color="black"
            ),
            
            title=dict(
                text="Number of Claims",
                y=0.9,
                x=0.5,
                xanchor='center',
                yanchor='top'
            ),
            
            legend=dict(
                x=0.5,
                y=1.1,
                xanchor='center',
                yanchor='top',
                orientation='h'
            ),
    
            
            plot_bgcolor='white',
            autosize=True  # Correct property for responsive layout
        )
    
        return fig
    
    
    #Chart 2
    
def create_distribution_chart(df):
        df_chart_2 = df[["Year", 'ClaimBands', "ClaimsLoss",]]
        
        df_chart_2 = df_chart_2.groupby(['ClaimBands','Year']).sum().reset_index()
        
        # Precompute total claims per year
        total_claims_per_year = df_chart_2.groupby('Year')['ClaimsLoss'].sum()
        
        # Calculate %AnnClaim using vectorized operations
        df_chart_2['%AnnClaim'] = df_chart_2.apply(
            lambda row: round((row['ClaimsLoss'] / total_claims_per_year[row['Year']]),2), axis=1)
        
        df_chart_2_trunc = df_chart_2[(df_chart_2['Year'] >= 2009) & (df_chart_2['Year'] <= 2019)]
        
        
        
        # Precompute total claims for all years
        tot_claims_all_years = df_chart_2['ClaimsLoss'].sum()
        
        # Calculate total claims by band and then calculate proportions
        proportions = (df_chart_2.groupby('ClaimBands')['ClaimsLoss'].sum() / tot_claims_all_years).round(2)
        
        # Map the proportions back to the DataFrame
        df_chart_2['AllYears'] = df_chart_2['ClaimBands'].map(proportions)
        
        four_year_df = df_chart_2[(df_chart_2['Year'] >= 2016) & (df_chart_2['Year'] <= 2019)]
        
        
        # Precompute total claims for 4 years
        tot_claims_4_years = four_year_df['ClaimsLoss'].sum()
        
        # Calculate total claims by band and then calculate proportions
        four_year_proportions = (four_year_df.groupby('ClaimBands')['ClaimsLoss'].sum() / tot_claims_4_years).round(2)
        
        # Map the proportions back to the DataFrame
        df_chart_2['4Years'] = df_chart_2['ClaimBands'].map(four_year_proportions)
        
        df_chart_2_px = df_chart_2
        
        df_chart_2_px = df_chart_2_px[(df_chart_2_px['Year'] >= 2009) & (df_chart_2_px['Year'] <= 2019)]
        
        
        import plotly.graph_objs as go
        import pandas as pd
        import numpy as np
        
        # Assuming df_chart_2_px is a pre-defined DataFrame with correct data
        # Define custom order as a categorical type with defined order
        custom_order = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
        df_chart_2_px['ClaimBands'] = pd.Categorical(df_chart_2_px['ClaimBands'], categories=custom_order, ordered=True)
        
        # Ensure data is sorted
        df_chart_2_px = df_chart_2_px.sort_values(by=['Year', 'ClaimBands'])
        
        # Prepare the plot
        fig = go.Figure()
        
        # Colors for the lines
        colors = {'%AnnClaim': '#56626F', 'AllYears': '#ED9547', '4Years': '#EDC147'}
        
        # Adding %AnnClaim with a loop
        for year in df_chart_2_px['Year'].unique():
            year_data = df_chart_2_px[df_chart_2_px['Year'] == year]
            fig.add_trace(go.Scatter(
                x=year_data['ClaimBands'],
                y=year_data['%AnnClaim'],
                mode='lines',
                name=f'{year}',
                line=dict(color=colors['%AnnClaim'],
                width=0.8),
                yaxis='y1'
            ))
        
        #Add the 4 Year Trace
        fig.add_trace(go.Scatter(
                x=year_data['ClaimBands'],
                y=year_data['4Years'],
                mode='lines',
                name= '4 Years',
                line=dict(color=colors['4Years']),
                yaxis='y1'
            ))
        
        
        #Add the All Years Trace
        fig.add_trace(go.Scatter(
                x=year_data['ClaimBands'],
                y=year_data['AllYears'],
                mode='lines',
                name= 'All Years',
                line=dict(color=colors['AllYears']),
                yaxis='y1'
            ))
        
        
        # Configure axes
        fig.update_layout(
            xaxis=dict(
                type='category',
                categoryorder='array',
                categoryarray=custom_order
            ),
            yaxis=dict(
                tickformat='.0%',
                dtick=0.05,
                showgrid=True,  # Enable the grid lines
                gridcolor='lightgrey',  # Set grid line color
                gridwidth=0.5,  # Set grid line width
                zeroline=True,  # Draw a line at y=0
                zerolinecolor='black',  # Color for the zero line
                zerolinewidth=1  # Width for the zero line
            ),
        
        
         legend=dict(
                x=0.5,   # Centers the legend horizontally
                y=-0.15,   # Position the legend above the top of the plot
                xanchor='center',  # Anchor the x position to the center of the legend
                yanchor='top',      # Anchor the y position to the top of the legend
                orientation='h',
              font=dict(
                    size=10,         # Specify the font size here
                )
            ),
        
                title={
                'text': "Claims Distribution",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },  # Set the main chart title
        
                font=dict(
                family="Tw Cen MT",  # Set the font family
                size=12,                     # Set the font size
                color="black"                # Set the font color
            ),
            
             plot_bgcolor='white',  # Background color
        )
        
        # Show plot
        return fig
    
    
    
    #CHART 3
    
def create_avginj_chart (df):
        df_chart_3 = df[["Year", "Injured", 'ClaimsLoss']]
        
        df_chart_3 = df_chart_3.groupby(by='Year').sum().reset_index()
        
        df_chart_3['avg_inj'] = (df_chart_3['Injured'] / df_chart_3['ClaimsLoss'])
        
        df_chart_3['avg_inj'] = df_chart_3['avg_inj'].fillna(0).apply(lambda x: int(x))
        
        #Plotly Chart
        
        # Correct initialization of the bar chart
        fig = go.Figure(data=[go.Bar(
            x=df_chart_3['Year'],  # Year on x-axis
            y=df_chart_3['avg_inj'],  # avg_inj on y-axis
            text=df_chart_3['avg_inj'],  # Display avg_inj numbers on bars
            textposition='auto',  # Positioning text to be automatically inside the bars
            marker_color='#ED9547'  # Bar color
        )])
        
        # Customize layout
        fig.update_layout(
        
            xaxis=dict(
                tickfont=dict(
                    size=11,         # Set the font size
                    color='Black'),     # Set the font color
                type='category',  # Ensures the labels are treated as discrete categories
                tickangle=0,  # Adjust this to rotate labels if they overlap or for better readability
            ),
        
            
            yaxis=dict(
                zeroline=True,  # Draw a line at y=0
                zerolinecolor='black',  # Color for the zero line
                zerolinewidth=1,  # Width for the zero line
                showticklabels=False  # Hides the tick labels on the y-axis
            ), 
        
        
            font=dict(
                family="Tw Cen MT",  # Set the font family
                size=12,                     # Set the font size
                color="black"                # Set the font color
            ),
        
            title={
                'text': "Average Number of Injured",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },  # Set the main chart title
             plot_bgcolor='white',  # Background color
            showlegend=False,  # Hide legend if not necessary
        )
        
        # Show plot
        return fig
    
    
    #CHART 4
    #Data engineering
    
def create_legalcost_chart(df):
        df_chart_4 = df[['Year', 'GrossClaimValid', 'LiabilityClaimsPaid', 'LegalClaimsPaid']]
        
        df_chart_4 = df_chart_4.groupby(by='Year').sum().reset_index()
        
        df_chart_4['PercLegal'] = (df_chart_4['LegalClaimsPaid']) / (df_chart_4['LiabilityClaimsPaid'] + df_chart_4['LegalClaimsPaid'])
        
        #Plotly Chart
        
        import pandas as pd
        import plotly.graph_objects as go
        
        # Assuming DataFrame 'LegLiab' is already loaded
        perc_conv_c4 = df_chart_4['PercLegal'].fillna(0)*100  # Convert to percentage
        rounded_c4 = perc_conv_c4.round().astype(int)  # Round and convert to int for plotting
        
        # Format these integers as strings with a percentage sign for annotations only
        df_chart_4['PercLegalText'] = [f"{x}%" for x in rounded_c4]
        
        # Assuming DataFrame 'GrossClaimValidPx' is already loaded
        
        
        # Create an empty figure
        fig = go.Figure()
        
        # Add bar chart
        fig.add_trace(go.Bar(
            x=df_chart_4['Year'],  # Year on x-axis
            y=df_chart_4['GrossClaimValid'],  # Gross claims on y-axis
            marker_color='#EDC147',  # Bar color
            name='Gross Claims Incurred'  # Legend entry for the bar chart
        ))
        
        # Add scatter plot on a secondary y-axis
        fig.add_trace(go.Scatter(
            x=df_chart_4['Year'],  # Year on x-axis
            y=df_chart_4['PercLegal'],  # Percentage of legal cases on y-axis
            mode='lines+text',  # Display lines (use 'markers+lines' for markers and lines)
            marker=dict(color='#56626F'),  # Marker color
            text=df_chart_4['PercLegalText'],  # Display year numbers next to markers
            textposition='top center',  # Positioning text above the markers
            textfont=dict(
                size=10,  # Specify the font size for bar text
                color= '#56626F'
            ),
            name='% of Legal Cost from Paid Amount',  # Legend entry for the scatter plot
            yaxis='y2'  # Specifies that this trace uses the second y-axis
        ))
        
        # Customize layout
        fig.update_layout(
            
            xaxis=dict(
                title="Year of Event",
                tickfont=dict(
                    size=11,         # Set the font size
                    color='#56626F'),     # Set the font color
                type='category',  # Ensures the labels are treated as discrete categories
                tickangle=0,  # Adjust this to rotate labels if they overlap or for better readability
            ),
            
            yaxis=dict(
                title='Gross Claims',  # Y-axis label for the bar chart
                side='left',  # Position of the first y-axis
                dtick=100000000,  # Y-axis increases by 0.5
                showgrid=True,  # Enable the grid lines
                gridcolor='lightgrey',  # Set grid line color
                gridwidth=0.5,  # Set grid line width
                zeroline=True,  # Draw a line at y=0
                zerolinecolor='black',  # Color for the zero line
                zerolinewidth=1  # Width for the zero line
        
            ),
            yaxis2=dict(
                title='% Legal Claims',  # Y-axis label for the scatter plot
                tickformat='.0%',  # Format ticks to percentage without decimal places
                side='right',  # Position of the second y-axis
                overlaying='y',  # Indicates that the second y-axis overlays the first
                anchor='x',  # Anchors the y-axis to the x-axis
                showgrid=False  # Optionally turn off the gridlines for the second axis
            ),
            plot_bgcolor='white',  # Background color
            showlegend=True,  # Show legend to differentiate the datasets
        
            title={
                'text': "Total Gross Claims",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },  # Set the main chart title
        
         legend=dict(
                x=0.5,   # Centers the legend horizontally
                y=1.1,   # Position the legend above the top of the plot
                xanchor='center',  # Anchor the x position to the center of the legend
                yanchor='top',      # Anchor the y position to the top of the legend
                orientation='h'
            ),
        
            font=dict(
                family="Tw Cen MT",  # Set the font family
                size=12,                     # Set the font size
                color="black"                # Set the font color
            ),
        
        )
        
        # Show plot
        return fig
        
    
    #CHART 5
    #Data engineering
def create_avgclaim_chart(df):
        
        df_chart_3 = df[["Year", "Injured", 'ClaimsLoss']]
        
        df_chart_3 = df_chart_3.groupby(by='Year').sum().reset_index()
        
        df_chart_3['avg_inj'] = (df_chart_3['Injured'] / df_chart_3['ClaimsLoss'])
        
        df_chart_3['avg_inj'] = df_chart_3['avg_inj'].fillna(0).apply(lambda x: int(x))
        
        df_chart_5 = df[['Year', 'GrossClaimValid', 'ClaimsLoss']]
        
        df_chart_5= df_chart_5.groupby(by='Year').sum().reset_index()
        
        df_chart_5["AvgGrossClaim"] = (df_chart_5['GrossClaimValid'] / df_chart_5['ClaimsLoss'])
        
        #Plotly Chart
    
        # Create an empty figure
        fig = go.Figure()
        
        # Add the bar chart trace for average gross claims
        fig.add_trace(go.Bar(
            x=df_chart_5['Year'],  # Year on x-axis
            y=df_chart_5['AvgGrossClaim'],  # AvgGrossClaim on y-axis
            marker_color='#479CED',  # Bar color
            name='Average Gross Claims',  # Legend name
            yaxis='y1'  # Bind to the primary y-axis
        ))
        
        # Add the line chart trace for yearly injury averages
        fig.add_trace(go.Scatter(
            x=df_chart_3['Year'],  # Year on x-axis
            y=df_chart_3['avg_inj'],  # avg_inj on y-axis
            mode='lines+text',  # Display line with markers at each data point
            text=df_chart_3['avg_inj'],  # Display avg_inj numbers on points
            textposition='top center',  # Positioning text above each marker
            line=dict(color='#ED9547'),  # Line color
            marker=dict(color='blue', size=8),  # Marker settings
            name='Averages Number of Injuries',  # Legend name
            yaxis='y2'  # Bind to the secondary y-axis
        ))
        
        # Update layout to include both y-axes and other customization
        fig.update_layout(
        
            xaxis=dict(
                title="Year of Event",
                tickfont=dict(
                    size=11,         # Set the font size
                    color='#56626F'),     # Set the font color
                type='category',  # Ensures the labels are treated as discrete categories
                tickangle=0,  # Adjust this to rotate labels if they overlap or for better readability
            ),
            
            yaxis=dict(
                title='Average Claims',  # Primary y-axis title
                side='left',  # Primary y-axis on the left
                dtick= 200000,  # Y-axis increases by 0.5
                showgrid=True,  # Enable the grid lines
                gridcolor='lightgrey',  # Set grid line color
                gridwidth=0.5,  # Set grid line width
                zeroline=True,  # Draw a line at y=0
                zerolinecolor='black',  # Color for the zero line
                zerolinewidth=1  # Width for the zero line
            ),
            yaxis2=dict(
                side='right',  # Secondary y-axis on the right
                overlaying='y',  # Overlay secondary y-axis on the primary y-axis
                anchor='x',
                showticklabels=False  # Hides the tick labels on the y-axis
                
            ),
        
            title={
                'text': "Average Claim",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },  # Set the main chart title
        
        
                font=dict(
                family="Tw Cen MT",  # Set the font family
                size=12,                     # Set the font size
                color="black"                # Set the font color
            ),
            
         legend=dict(
                x=0.5,   # Centers the legend horizontally
                y=1.1,   # Position the legend above the top of the plot
                xanchor='center',  # Anchor the x position to the center of the legend
                yanchor='top',      # Anchor the y position to the top of the legend
                orientation='h'
            ),
            
            plot_bgcolor='white',  # Background color
            showlegend=True  # Show legend to differentiate the datasets
        )
        
        # Show plot
        return fig
    
    
    #CHART 6
    #Data prep
    
def create_avgclaiminj_chart(df):
        df_chart_6 = df[['Year', 'Injured', 'GrossClaimValid']]
        
        df_chart_6 = df_chart_6.groupby(by='Year').sum().reset_index()
        
        df_chart_6['AvgClaimInj'] = df_chart_6['GrossClaimValid'] / df_chart_6['Injured']
        
        
        #Plotly Chart
        # Create the figure with the bar chart
        fig = go.Figure(data=[go.Bar(
            x=df_chart_6['Year'],  # Year on x-axis
            y=df_chart_6['AvgClaimInj'],  # AvgClaimInj on y-axis
            marker_color='#56626F',  # Bar color
            showlegend=False  # This hides the trace from the legend
        )])
        
        
        # Customize layout
        fig.update_layout(
            showlegend=True,  # Enable legend to differentiate the bar chart and trendline
        
            xaxis=dict(
                tickfont=dict(
                    size=11,         # Set the font size
                    color='#56626F'),     # Set the font color
                type='category',  # Ensures the labels are treated as discrete categories
                tickangle=0,  # Adjust this to rotate labels if they overlap or for better readability
            ),
            
            yaxis=dict(
                dtick= 100000,  # Y-axis increases by 0.5
                showgrid=True,  # Enable the grid lines
                gridcolor='lightgrey',  # Set grid line color
                gridwidth=0.5,  # Set grid line width
                zeroline=True,  # Draw a line at y=0
                zerolinecolor='black',  # Color for the zero line
                zerolinewidth=1  # Width for the zero line
            ),
        
            title={
                'text': "Average Claims",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },  # Set the main chart title
        
        
                font=dict(
                family="Tw Cen MT",  # Set the font family
                size=12,                     # Set the font size
                color="black"                # Set the font color
            ),
            
         legend=dict(
                x=0.5,   # Centers the legend horizontally
                y=1.25,   # Position the legend above the top of the plot
                xanchor='center',  # Anchor the x position to the center of the legend
                yanchor='top',      # Anchor the y position to the top of the legend
                orientation='h'
            ),
            
             plot_bgcolor='white',  # Background color
        )
        
        # Show plot
        return fig
    
    
    #CHART 7
    #Data engineering
    
def create_avglegalcost_chart(df):
        df_chart_7 = df[['Year', 'ClaimsLoss','OnlyLegalCostAmt', 'LegalClaimsPaid']]
        
        df_chart_7 = df_chart_7.groupby(by='Year').sum().reset_index()
        
        df_chart_7['AvgLegClaim'] = (df_chart_7['LegalClaimsPaid'] / df_chart_7['ClaimsLoss'])
        
        df_chart_7['PercOnlyLegalCost'] =  (df_chart_7['OnlyLegalCostAmt'] / df_chart_7['LegalClaimsPaid'])
        
        
        #Plotly Chart
        
        rounded_c_7 = (df_chart_7['PercOnlyLegalCost'] * 100).fillna(0).astype(int)
        
        # Format these integers as strings with a percentage sign
        perc_labels_7 = [f"{x}%" for x in rounded_c_7]
        
        # Optionally add these to the DataFrame or use directly
        df_chart_7['Percentage Labels'] = perc_labels_7
        
        # Sample data initialization - replace these with your actual data
        # chart_7_grp = {
        #     'Year': [2015, 2016, 2017, 2018, 2019],
        #     'AvgLegClaim': [200, 220, 210, 230, 240],
        #     'PercOnlyLegalCost': [10, 15, 13, 16, 17]
        # }
        
        # Create an empty figure
        fig = go.Figure()
        
        # Add the bar chart for Average Legal Claims
        fig.add_trace(go.Bar(
            x=df_chart_7['Year'],  # Year on x-axis
            y=df_chart_7['AvgLegClaim'],  # AvgLegClaim on y-axis
            textposition='auto',  # Positioning text to be automatically inside the bars
            marker_color='#479CED',  # Bar color
            name='Average Legal Claims',  # Legend name
            yaxis='y',  # Bind to the primary y-axis
        ))
        
        # Add the line chart for Percentage of Only Legal Costs
        fig.add_trace(go.Scatter(
            x=df_chart_7['Year'],  # Year on x-axis
            y=df_chart_7['PercOnlyLegalCost'],  # PercOnlyLegalCost on y-axis
            mode='lines+text',  # Display line with markers
            text=df_chart_7['Percentage Labels'],  # Display the percentage at each point
            textposition='top center',  # Position text above each marker
            line=dict(color='#ED9547'),  # Line color
            name='% Only Legal Costs',  # Legend name
            yaxis='y2',  # Bind to the secondary y-axis
            textfont=dict(
                size=10,  # Specify the font size for bar text
                color= 'black')
        ))
        
        # Update layout with two different y-axes
        fig.update_layout(
            
            xaxis_title='Year of Event',
            yaxis=dict(
                side='left',  # Primary y-axis on the left
                dtick= 50000,  # Y-axis increases by 0.5
            showgrid=True,  # Enable the grid lines
                gridcolor='lightgrey',  # Set grid line color
                gridwidth=0.5,  # Set grid line width
                zeroline=True,  # Draw a line at y=0
                zerolinecolor='black',  # Color for the zero line
                zerolinewidth=1  # Width for the zero line
        
            ),
            yaxis2=dict(
                side='right',  # Secondary y-axis on the right
                overlaying='y',  # Overlay on the primary y-axis
                tickformat='.0%',  # Format ticks to percentage without decimal places
        
            ),
        
            title={
                'text': "Average Legal Cost",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },  # Set the main chart title
        
        
            font=dict(
                family="Tw Cen MT",  # Set the font family
                size=12,                     # Set the font size
                color="black"                # Set the font color
            ),
            
         legend=dict(
                x=0.5,   # Centers the legend horizontally
                y=1.1,   # Position the legend above the top of the plot
                xanchor='center',  # Anchor the x position to the center of the legend
                yanchor='top',      # Anchor the y position to the top of the legend
                orientation='h'
            ),
        
            
            plot_bgcolor='white',  # Background color
            showlegend=True  # Show legend to differentiate the datasets
        
            
        )
        
        # Show plot
        return fig
