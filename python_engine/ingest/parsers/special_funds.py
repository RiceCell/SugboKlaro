# TWO: opens Excel file, chops off signature, fixes merged cells and puts into shape
# (FOR SPECIAL PURPOSE FUND REPORTS — Pipeline C, starting with UCA)

import pandas as pd
from ingest.schema import UCA_SCHEMA

UCA_SHEET_NAME = "Form 12 - UCA"

UCA_HEADER_ROWS = 11

_AGING_COLS = [
    "negative_balance",
    "current_lt_30",
    "current_31_90",
    "current_91_365",
    "past_due_over_1yr",
    "past_due_over_2yr",
    "past_due_3yr_plus",
]

# position (0-indexed) -> schema column name, for the aging/balance bucket columns
_AGING_COL_POSITIONS = {
    7: "negative_balance",     # col H — "Negative Balance"
    8: "current_lt_30",        # col I — Current, Less than 30 days
    9: "current_31_90",        # col J — Current, 31-90 days
    10: "current_91_365",      # col K — Current, 91-365 days
    11: "past_due_over_1yr",   # col L — Past Due, Over 1 year
    12: "past_due_over_2yr",   # col M — Past Due, Over 2 years
    13: "past_due_3yr_plus",   # col N — Past Due, 3 years and above
}


_FUND_SOURCE_LABELS = {"GENERAL FUND", "SPECIAL EDUCATION FUND", "TRUST FUND"}

_NON_DEBTOR_LABELS = {"SUBTOTAL", "GRAND TOTAL"}


def _clean_dash(val):
    """The UCA template uses '-' for a zero-value aging bucket instead of
    leaving the cell blank; some cells are genuinely blank (None) instead of
    '-' too (seen in the real file). Treat both as 0.0."""
    if pd.isna(val) or val == "-":
        return 0.0
    return float(val)


def parse_uca(filepath):
    raw = pd.read_excel(filepath, sheet_name=UCA_SHEET_NAME, header=None, skiprows=UCA_HEADER_ROWS)

    fund_source = None
    cash_advance_type = None
    records = []

    for _, row in raw.iterrows():
        name_cell = row[0]
        balance_cell = row[1] if len(row) > 1 else None

        if pd.isna(name_cell):
            continue  # fully blank separator row

        name_text = str(name_cell).strip()

        if pd.isna(balance_cell):
            # Category row (fund-level or sub-account-level), or footer/signature
            # text, or a stray annotation. Update tracked context, then drop the row.
            upper = name_text.upper()
            if upper in _FUND_SOURCE_LABELS:
                fund_source = name_text
            elif name_text.lower().startswith("cash advance"):
                cash_advance_type = name_text
            continue

        if name_text.upper() in _NON_DEBTOR_LABELS:
            continue  # SUBTOTAL / GRAND TOTAL — has a balance value but isn't a debtor

        record = {
            "name_of_debtor": name_text,
            "amount_balance": float(balance_cell),
            "date_granted": row[2] if pd.notna(row[2]) else pd.NaT,
            "purpose": row[3] if pd.notna(row[3]) else None,
            "fund_source": fund_source,
            "cash_advance_type": cash_advance_type,
        }
        for pos, col_name in _AGING_COL_POSITIONS.items():
            record[col_name] = _clean_dash(row[pos] if pos < len(row) else None)

        record["doc_type"] = "UCA"
        records.append(record)

    if not records:
        compliant_row = {
            "doc_type": "UCA",
            "name_of_debtor": "NONE",
            "amount_balance": None,
            "date_granted": None,
            "purpose": "No unliquidated cash advances for this quarter - Submitted accordingly",
            "fund_source": None,
            "cash_advance_type": None,
            **{c: 0.0 for c in _AGING_COLS},
        }
        return pd.DataFrame([compliant_row])[UCA_SCHEMA]

    df = pd.DataFrame(records)
    df["date_granted"] = pd.to_datetime(df["date_granted"], errors="coerce")
    return df[UCA_SCHEMA]


if __name__ == "__main__":
    from config import UCA_FILE
    df = parse_uca(UCA_FILE)
    print(df.to_json(orient="records", indent=2, date_format="iso"))