import pandas as pd
import numpy as np


def claimbands(GrossClaims):
    # Your full function logic for banding claims
    if GrossClaims >= 0 and GrossClaims < 10000:
        return "10K"
    elif GrossClaims >= 10000 and GrossClaims < 20000:
        return "20K"
    elif GrossClaims >= 20000 and GrossClaims < 30000:
        return "30K"
    elif GrossClaims >= 30000 and GrossClaims < 50000:
        return "50K"
    elif GrossClaims >= 50000 and GrossClaims < 80000:
        return "80K"
    elif GrossClaims >= 80000 and GrossClaims < 100000:
        return "100K"
    elif GrossClaims >= 100000 and GrossClaims < 150000:
        return "150K"
    elif GrossClaims >= 150000 and GrossClaims < 250000:
        return "250K"
    elif GrossClaims >= 250000 and GrossClaims < 500000:
        return "500K"
    elif GrossClaims >= 500000 and GrossClaims < 750000:
        return "750K"
    elif GrossClaims >= 750000 and GrossClaims < 1000000:
        return "1M"
    elif GrossClaims >= 1000000 and GrossClaims < 2000000:
        return "2M"
    elif GrossClaims >= 2000000 and GrossClaims < 5000000:
        return "5M"
    elif GrossClaims >= 5000000 and GrossClaims < 10000000:
        return "10M"
    elif GrossClaims >= 10000000 and GrossClaims < 100000000:
        return "100M"
    else:
        return "Above 100M"


def load_and_prepare_data(file_path, sheet_name):
    try:
        # Load the data into a DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
        print("Data loaded successfully")

        # Perform Initial Data Prep on the Excel file
        df = df.set_index('Reference')
        print("Index set to 'Reference'")

        # Data transformation steps
        df["Year"] = df["Year"].astype(float).fillna(0).astype(int)
        df["No. injured"] = df["No. injured"].fillna(0).astype(int)
        df["Total Claims Paid"] = df["Total Claims Paid"].astype(
            str).str.replace('-', '0').str.replace(' ', '').astype(float)
        df["Underwriter"] = df["Underwriter"].astype(str).str.replace(
            '-', '0').str.replace(' ', '').astype(float)
        df["LegalCostOnly"] = df["LegalCostOnly"].replace(
            '-', '0').astype(str).str.replace(' ', '').astype(int)
        df["Injured"] = df["Injured"].replace(
            '-', '0').astype(str).str.replace(' ', '').astype(int)
        df['ClaimsLoss'] = df['ClaimsLoss'].replace(
            '-', '0').fillna(0).astype(int)
        df["Gross = Total Reserves + Total Claims Paid"] = df["Gross = Total Reserves + Total Claims Paid"].astype(
            str).str.replace(" ", "").astype(float).fillna(0.0)

        # Renaming and recalculating fields
        df = df.rename(
            columns={"Gross = Total Reserves + Total Claims Paid": "Gross"})
        df["ClaimBands"] = np.vectorize(claimbands)(df["Gross"])
        print("Claim bands calculated")

        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Define the path and sheet name
file_path = "Premium_Model_Data.xlsx"
sheet_name = 'Data'

df = load_and_prepare_data(file_path, sheet_name)


def processed_data():
    return df.copy()
