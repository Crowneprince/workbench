

def claims_distribution_data(df):

    df_chart_2 = df[["Year", 'ClaimBands', "ClaimsLoss",]]

    df_chart_2 = df_chart_2.groupby(['ClaimBands', 'Year']).sum().reset_index()

    # Precompute total claims per year
    total_claims_per_year = df_chart_2.groupby('Year')['ClaimsLoss'].sum()

    # Calculate %AnnClaim using vectorized operations
    df_chart_2['%AnnClaim'] = df_chart_2.apply(
        lambda row: round((row['ClaimsLoss'] / total_claims_per_year[row['Year']]), 2), axis=1)

    # Precompute total claims for all years
    tot_claims_all_years = df_chart_2['ClaimsLoss'].sum()

    # Calculate total claims by band and then calculate proportions
    proportions = (df_chart_2.groupby('ClaimBands')[
                   'ClaimsLoss'].sum() / tot_claims_all_years).round(2)

    # Map the proportions back to the DataFrame
    df_chart_2['AllYears'] = df_chart_2['ClaimBands'].map(proportions)

    four_year_df = df_chart_2[(df_chart_2['Year'] >= 2016)
                              & (df_chart_2['Year'] <= 2019)]

    # Precompute total claims for 4 years
    tot_claims_4_years = four_year_df['ClaimsLoss'].sum()

    # Calculate total claims by band and then calculate proportions
    four_year_proportions = (four_year_df.groupby('ClaimBands')[
                             'ClaimsLoss'].sum() / tot_claims_4_years).round(2)

    # Map the proportions back to the DataFrame
    df_chart_2['4Years'] = df_chart_2['ClaimBands'].map(four_year_proportions)

    df_chart_2_px = df_chart_2

    df_chart_2_px = df_chart_2_px[(df_chart_2_px['Year'] >= 2009) & (
        df_chart_2_px['Year'] <= 2019)]
