import pandas as pd
import numpy as np

#Claims Registered Pivot Table

def create_claimsreg_pivot(df):
    tb_claims_reg = df[['ClaimBands', "Year", 'ClaimsID']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_claims_reg = tb_claims_reg.pivot_table(index='ClaimBands', columns='Year', values='ClaimsID', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')  # Custom name for the margins row/column)
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_claims_reg = tb_claims_reg.reindex(custom_order_columns)
    
    tb_claims_reg = tb_claims_reg.astype(int).reset_index()
    
    return tb_claims_reg


#Valid Claims Pivot table
def create_validclaims_pivot(df):
    tb_valid_claims = df[['ClaimBands', "Year", 'PaidOpenClaims']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_valid_claims = tb_valid_claims.pivot_table(index='ClaimBands', columns='Year', values='PaidOpenClaims', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_valid_claims = tb_valid_claims.reindex(custom_order_columns)
    
    tb_valid_claims = tb_valid_claims.astype(int).reset_index()
    
    return tb_valid_claims


#Claims where payment made - legal cost
def create_claimsloss_pivot(df):
    tb_claims_loss = df[['ClaimBands', "Year", 'ClaimsLoss']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_claims_loss = tb_claims_loss.pivot_table(index='ClaimBands', columns='Year', values='ClaimsLoss', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_claims_loss = tb_claims_loss.reindex(custom_order_columns)
    
    tb_claims_loss = tb_claims_loss.astype(int).reset_index()
    
    return tb_claims_loss


# Number of Injured
def create_numinj_pivot(df):
    tb_no_injured = df[['ClaimBands', "Year", 'Injured']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_no_injured = tb_no_injured.pivot_table(index='ClaimBands', columns='Year', values='Injured', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_no_injured = tb_no_injured.reindex(custom_order_columns)
    
    tb_no_injured = tb_no_injured.astype(int).reset_index()
    
    return tb_no_injured


#Gross Claims
def create_grossclaims_pivot(df):
    tb_gross_claim_valid = df[['ClaimBands', "Year", 'GrossClaimValid']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_gross_claim_valid = tb_gross_claim_valid.pivot_table(index='ClaimBands', columns='Year', values='GrossClaimValid', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_gross_claim_valid = tb_gross_claim_valid.reindex(custom_order_columns)
    
    tb_gross_claim_valid = tb_gross_claim_valid.astype(int).reset_index()
    
    return tb_gross_claim_valid


#Average CLaims per number of claims

def create_avgclaimnumclaims_pivot(df):
    tb_gross_claim_valid = df[['ClaimBands', "Year", 'GrossClaimValid']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_gross_claim_valid = tb_gross_claim_valid.pivot_table(index='ClaimBands', columns='Year', values='GrossClaimValid', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_gross_claim_valid = tb_gross_claim_valid.reindex(custom_order_columns)
    
    tb_gross_claim_valid = tb_gross_claim_valid.astype(int)
    
    tb_gross_claim_valid
    
    
    tb_claims_loss = df[['ClaimBands', "Year", 'ClaimsLoss']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_claims_loss = tb_claims_loss.pivot_table(index='ClaimBands', columns='Year', values='ClaimsLoss', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_claims_loss = tb_claims_loss.reindex(custom_order_columns)
    
    tb_claims_loss = tb_claims_loss.astype(int)
    
    tb_claims_loss
    
    
    tb_avg_claims = tb_gross_claim_valid / tb_claims_loss
    
    tb_avg_claims = tb_avg_claims.fillna(0).astype(int).reset_index()
    
    return tb_avg_claims


def create_avgclaiminj_pivot(df):
    #Average Claim per Injury
    tb_gross_claim_valid = df[['ClaimBands', "Year", 'GrossClaimValid']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_gross_claim_valid = tb_gross_claim_valid.pivot_table(index='ClaimBands', columns='Year', values='GrossClaimValid', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_gross_claim_valid = tb_gross_claim_valid.reindex(custom_order_columns)
    
    tb_gross_claim_valid = tb_gross_claim_valid.astype(int)
    
    tb_gross_claim_valid
    
    
    tb_no_injured = df[['ClaimBands', "Year", 'Injured']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_no_injured = tb_no_injured.pivot_table(index='ClaimBands', columns='Year', values='Injured', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_no_injured = tb_no_injured.reindex(custom_order_columns)
    
    tb_no_injured = tb_no_injured.astype(int)
    
    tb_no_injured
    
    
    tb_avg_claim_inj = tb_gross_claim_valid / tb_no_injured
    
    tb_avg_claim_inj = tb_avg_claim_inj.replace([np.inf, -np.inf], np.nan).fillna(0).astype(int).reset_index()
    
    return tb_avg_claim_inj



#Paid by Underwriter

def create_paidunder_pivot(df):
    tb_paid_under = df[['ClaimBands', "Year", 'Underwriter']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_paid_under = tb_paid_under.pivot_table(index='ClaimBands', columns='Year', values='Underwriter', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_paid_under = tb_paid_under.reindex(custom_order_columns)
    
    tb_paid_under = tb_paid_under.astype(int).reset_index()
    
    return tb_paid_under



# Legal Claims

def create_legalclaims_pivot(df):
    tb_leg_claims = df[['ClaimBands', "Year", 'Total Claims Paid']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_leg_claims = tb_leg_claims.pivot_table(index='ClaimBands', columns='Year', values='Total Claims Paid', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_leg_claims = tb_leg_claims.reindex(custom_order_columns)
    
    tb_leg_claims = tb_leg_claims.astype(int).reset_index()
    
    return tb_leg_claims


# Numberof legal claims where no claims
def create_legalclaimsnoclaims_pivot(df):
    tb_leg_cost_only = df[['ClaimBands', "Year", 'LegalCostOnly']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_leg_cost_only = tb_leg_cost_only.pivot_table(index='ClaimBands', columns='Year', values='LegalCostOnly', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_leg_cost_only = tb_leg_cost_only.reindex(custom_order_columns)
    
    tb_leg_cost_only = tb_leg_cost_only.astype(int).reset_index()
    
    return tb_leg_cost_only


#Amount of legals claims where there were no claims
def create_amtlegalclaimsnoclaims_pivot(df):
    tb_only_leg_cost_amt = df[['ClaimBands', "Year", 'OnlyLegalCostAmt']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_only_leg_cost_amt = tb_only_leg_cost_amt.pivot_table(index='ClaimBands', columns='Year', values='OnlyLegalCostAmt', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_only_leg_cost_amt = tb_only_leg_cost_amt.reindex(custom_order_columns)
    
    tb_only_leg_cost_amt = tb_only_leg_cost_amt.astype(int).reset_index()
    
    return tb_only_leg_cost_amt



# Legal cost payment
def create_legalcostpmt_pivot(df):
    tb_leg_cost_pmt = df[['ClaimBands', "Year", 'LegalClaimsPaid']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_leg_cost_pmt = tb_leg_cost_pmt.pivot_table(index='ClaimBands', columns='Year', values='LegalClaimsPaid', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_leg_cost_pmt = tb_leg_cost_pmt.reindex(custom_order_columns)
    
    tb_leg_cost_pmt = tb_leg_cost_pmt.astype(int).reset_index()
    
    return tb_leg_cost_pmt


#Legal cost payment (Liability)
def create_liabcostpmt_pivot(df):
    tb_liab_cost_pmt = df[['ClaimBands', "Year", 'LiabilityClaimsPaid']]
    
    # Using pivot_table to transpose the DataFrame by 'Product'
    tb_liab_cost_pmt = tb_liab_cost_pmt.pivot_table(index='ClaimBands', columns='Year', values='LiabilityClaimsPaid', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
    
    # Define custom order for columns
    custom_order_columns = ['10K', '20K', '30K', '50K', '80K', '100K', '150K', '250K', '500K', '750K', '1M', '2M', '5M', '10M', '100M']
    tb_liab_cost_pmt = tb_liab_cost_pmt.reindex(custom_order_columns)
    
    tb_liab_cost_pmt = tb_liab_cost_pmt.astype(int).reset_index()
    
    return tb_liab_cost_pmt