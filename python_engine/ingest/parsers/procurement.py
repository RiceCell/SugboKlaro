import pandas as pd
from ingest.schema import PROCUREMENT_SCHEMA

def parse_brcwgs_cw(filepath):
    df = pd.read_excel(filepath, sheet_name='FORM 10a - CW', skiprows=10)

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

def parse_brcwgs_gs(filepath):
    df = pd.read_excel(filepath, sheet_name='FORM 10b - GS', skiprows=10)

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

    df['reference_no'] = df['reference_no'].ffill().infer_objects(copy=False)
    df['project_name'] = df['project_name'].ffill().infer_objects(copy=False)

    df['bid_amount'] = df['bid_amount'].astype(str).replace(r'[₱, ]', '', regex=True)
    df['abc'] = pd.to_numeric(df['abc'], errors='coerce')
    df['bid_amount'] = pd.to_numeric(df['bid_amount'], errors='coerce')

    df['bidding_date'] = pd.to_datetime(df['bidding_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['doc_type'] = 'BRCWGS_GS'

    return df[PROCUREMENT_SCHEMA]

def parse_brcwgs_cs(filepath):
    df = pd.read_excel(filepath, sheet_name='FORM 10c - CS', skiprows=10)

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


def parse_brcwgs(filepath):
    """Combines all 3 BRCWGS sub-forms into one tidy DataFrame."""
    dfs = [parse_brcwgs_gs(filepath), parse_brcwgs_cw(filepath), parse_brcwgs_cs(filepath)]
    valid = [d for d in dfs if not d.empty]
    return pd.concat(valid, ignore_index=True) if valid else pd.DataFrame(columns=PROCUREMENT_SCHEMA)


if __name__ == "__main__":
    from config import BRCWGS_FILE
    combined_df = parse_brcwgs(BRCWGS_FILE)
    print(combined_df.to_json(orient="records", indent=2))