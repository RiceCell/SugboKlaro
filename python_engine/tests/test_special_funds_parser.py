import pandas as pd
import pytest

from config import UCA_FILE
from ingest.parsers.special_funds import parse_uca
from ingest.schema import UCA_SCHEMA

# Known-good numbers, verified against the real Q1 2026 Cebu City UCA file.
# If these ever change, it should be because the source .xlsx changed —
# not because the parser silently started dropping/duplicating rows.
KNOWN_GOOD_ROW_COUNT = 810
KNOWN_GOOD_GRAND_TOTAL = 59119357.60


@pytest.fixture(scope="module")
def uca_df():
    return parse_uca(UCA_FILE)


def test_parse_uca_returns_correct_schema_and_shape(uca_df):
    assert list(uca_df.columns) == UCA_SCHEMA
    assert len(uca_df) == KNOWN_GOOD_ROW_COUNT
    assert uca_df["doc_type"].eq("UCA").all()


def test_parse_uca_excludes_subtotal_and_grand_total_rows(uca_df):
    # SUBTOTAL / GRAND TOTAL rows have a non-null Amount Balance (unlike
    # category rows), so a naive "balance is not null" filter would let
    # 16 phantom debtor rows through. Confirm none leaked in, and that the
    # real debtor rows still sum to the sheet's own GRAND TOTAL.
    names_upper = uca_df["name_of_debtor"].astype(str).str.upper()
    assert not names_upper.isin(["SUBTOTAL", "GRAND TOTAL"]).any()
    assert uca_df["amount_balance"].sum() == pytest.approx(KNOWN_GOOD_GRAND_TOTAL, abs=0.01)


def test_parse_uca_keeps_genuine_missing_data_rows(uca_df):
    # RECALDE, EDEN BATUIGAS (row 329 in the raw sheet) is a real debtor with
    # a balance but a blank Date Granted / Purpose — must be KEPT (not dropped
    # like a category row) so downstream rules can flag it as missing_data
    # rather than the row silently vanishing.
    recalde = uca_df[
        (uca_df["name_of_debtor"] == "RECALDE, EDEN BATUIGAS")
        & (uca_df["amount_balance"] == 4445.14)
    ]
    assert len(recalde) == 1
    assert pd.isna(recalde.iloc[0]["date_granted"])
    assert recalde.iloc[0]["purpose"] is None


def test_parse_uca_cleans_dash_and_blank_aging_buckets_to_zero(uca_df):
    aging_cols = [
        "negative_balance", "current_lt_30", "current_31_90", "current_91_365",
        "past_due_over_1yr", "past_due_over_2yr", "past_due_3yr_plus",
    ]
    for col in aging_cols:
        assert uca_df[col].isna().sum() == 0
        assert (uca_df[col] == "-").sum() == 0


def test_parse_uca_aging_buckets_reconcile_with_amount_balance(uca_df):
    bucket_cols = [
        "current_lt_30", "current_31_90", "current_91_365",
        "past_due_over_1yr", "past_due_over_2yr", "past_due_3yr_plus",
    ]
    bucket_sum = uca_df[bucket_cols].sum(axis=1)
    mismatches = (bucket_sum - uca_df["amount_balance"]).abs() > 0.02
    assert mismatches.sum() == 0