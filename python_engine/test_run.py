import pandas as pd
import json

PROCUREMENT_SCHEMA = [
    "doc_type", 
    "reference_no", 
    "project_name", 
    "abc", 
    "winning_bidder", 
    "bidder_address", 
    "bid_amount", 
    "bidding_date"
]

def parse_brcwgs_gs(filepath):
    df = pd.read_excel(filepath, sheet_name='FORM 10b - GS', skiprows=10)
    
    # Cut off sa footer
    certify_index = df[df.iloc[:, 0].astype(str).str.contains('certify', case=False, na=False)].index
    if not certify_index.empty:
        df = df.loc[:certify_index[0] - 1]

    
    df = df.dropna(subset=['Reference \nNo.'])
    df = df.rename(columns={
        'Reference \nNo.': 'reference_no',
        'Item Description': 'project_name',
        'Approved Budget for \nContract': 'abc',
        'Winning Bidder': 'winning_bidder',
        'Name and Address Of \nBidder': 'bidder_address',
        'Bid Amount': 'bid_amount',
        'Date of Bidding': 'bidding_date'
    })
    df = df.dropna(subset=['abc', 'winning_bidder'], how='all')
    
    df['reference_no'] = df['reference_no'].ffill()
    df['project_name'] = df['project_name'].ffill()
 
    df['bid_amount'] = df['bid_amount'].astype(str).replace(r'[₱, ]', '', regex=True)
    df['abc'] = pd.to_numeric(df['abc'], errors='coerce')
    df['bid_amount'] = pd.to_numeric(df['bid_amount'], errors='coerce')

    df['bidding_date'] = pd.to_datetime(df['bidding_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['doc_type'] = 'BRCWGS_GS'
    
    return df[PROCUREMENT_SCHEMA]


def parse_brcwgs_cw(filepath):
    df = pd.read_excel(filepath, sheet_name='FORM 10a - CW', skiprows=10)
    
    # Cutoff!
    certify_index = df[df.iloc[:, 0].astype(str).str.contains('certify', case=False, na=False)].index
    if not certify_index.empty:
        df = df.loc[:certify_index[0] - 1]
   
    
    first_row_check = df.dropna(how='all', subset=['Reference No.', 'Name of Project'])
    if not first_row_check.empty:
        ref_val = str(first_row_check.iloc[0]['Reference No.']).upper()
        if "NONE" in ref_val:
            return pd.DataFrame(columns=PROCUREMENT_SCHEMA)

    df = df.rename(columns={
        'Reference No.': 'reference_no',
        'Name of Project': 'project_name',
        'Approved Budget for Contract': 'abc',
        'Winning\nBidder': 'winning_bidder',
        'Name and\nAddress': 'bidder_address',
        'Bid\nAmount': 'bid_amount',
        'Bidding Date': 'bidding_date'
    })
    
    df = df.dropna(subset=['abc', 'winning_bidder'], how='all')
    
    if not df.empty:
        df['bid_amount'] = df['bid_amount'].astype(str).replace(r'[₱, ]', '', regex=True)
        df['abc'] = pd.to_numeric(df['abc'], errors='coerce')
        df['bid_amount'] = pd.to_numeric(df['bid_amount'], errors='coerce')
        df['bidding_date'] = pd.to_datetime(df['bidding_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    
    df['doc_type'] = 'BRCWGS_CW'
    return df[PROCUREMENT_SCHEMA]


def parse_brcwgs_cs(filepath):
    df = pd.read_excel(filepath, sheet_name='FORM 10c - CS', skiprows=10)
    
    # Cut off!
    certify_index = df[df.iloc[:, 0].astype(str).str.contains('certify', case=False, na=False)].index
    if not certify_index.empty:
        df = df.loc[:certify_index[0] - 1]

    first_row_check = df.dropna(how='all', subset=['Reference\nNo.'])
    if not first_row_check.empty:
        ref_val = str(first_row_check.iloc[0]['Reference\nNo.']).upper()
        if "NONE" in ref_val:
            return pd.DataFrame(columns=PROCUREMENT_SCHEMA)

    df = df.rename(columns={
        'Reference\nNo.': 'reference_no',
        'Services': 'project_name',
        'Name of Consultant': 'winning_bidder',
        'Monthly remuneration': 'bid_amount'
    })
    
    df['abc'] = None
    df['bidder_address'] = None
    df['bidding_date'] = None
    
    df = df.dropna(subset=['winning_bidder'], how='all')
    
    if not df.empty:
        df['bid_amount'] = df['bid_amount'].astype(str).replace(r'[₱, ]', '', regex=True)
        df['bid_amount'] = pd.to_numeric(df['bid_amount'], errors='coerce')
        
    df['doc_type'] = 'BRCWGS_CS'
    return df[PROCUREMENT_SCHEMA]


if __name__ == "__main__":
    file_path = "data/raw_2026_excel/brcwgs_2026.xlsx"
    
    try:
        gs_df = parse_brcwgs_gs(file_path)
        cw_df = parse_brcwgs_cw(file_path)
        cs_df = parse_brcwgs_cs(file_path)
        
        all_dfs = [gs_df, cw_df, cs_df]
        valid_dfs = [df for df in all_dfs if not df.empty]
        
        if valid_dfs:
            combined_df = pd.concat(valid_dfs, ignore_index=True)
        else:
            combined_df = pd.DataFrame(columns=PROCUREMENT_SCHEMA)
            
        json_output = combined_df.to_json(orient="records", indent=2)
        print(json_output)
        
    except Exception as e:
        print(f"Error: {e}")