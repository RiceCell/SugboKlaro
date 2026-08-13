import pandas as pd
from config import BRCWGS_FILE as FILE
from ingest.parsers.procurement import parse_brcwgs
from rules.procurement_rules import ABCCeilingRule, ZeroVarianceBiddingRule, VendorConcentrationRule
from rules.base import RuleStatus


def get_df():
    return parse_brcwgs(FILE)


def test_abc_ceiling_flags_none_over_budget():
    df = get_df()
    results = ABCCeilingRule().evaluate(df)
    assert len([r for r in results if r.status == RuleStatus.FLAGGED]) == 0


def test_abc_ceiling_catches_missing_data():
    df = get_df()
    results = ABCCeilingRule().evaluate(df)
    assert len([r for r in results if r.status == RuleStatus.MISSING_DATA]) == 3


def test_abc_ceiling_skips_consulting_services():
    df = get_df()
    results = ABCCeilingRule().evaluate(df)
    cs_refs = df[df["doc_type"] == "BRCWGS_CS"]["reference_no"].tolist()
    result_refs = [r.row_ref for r in results]
    assert not any(ref in result_refs for ref in cs_refs)


def test_zero_variance_flags_expected_count():
    df = get_df()
    assert len(ZeroVarianceBiddingRule().evaluate(df)) == 8


def test_zero_variance_only_returns_flagged_status():
    df = get_df()
    results = ZeroVarianceBiddingRule().evaluate(df)
    assert all(r.status == RuleStatus.FLAGGED for r in results)


def test_vendor_concentration_no_flags_this_quarter():
    df = get_df()
    assert len(VendorConcentrationRule().evaluate(df)) == 0


def test_vendor_concentration_flags_when_threshold_met():
    df = pd.DataFrame({
        "doc_type": ["BRCWGS_GS"] * 3,
        "reference_no": ["1", "2", "3"],
        "project_name": ["A", "B", "C"],
        "abc": [1000, 2000, 3000],
        "winning_bidder": ["Same Vendor Inc."] * 3,
        "bidder_address": ["Addr"] * 3,
        "bid_amount": [900, 1900, 2900],
        "bidding_date": ["2026-01-01"] * 3,
    })
    results = VendorConcentrationRule().evaluate(df)
    assert len(results) == 1
    assert "Same Vendor Inc." in results[0].message


def test_full_summary_matches_known_good_run():
    from engine import run_check
    output = run_check("BRCWGS", FILE)
    assert output["summary"] == {"pass": 21, "flagged": 8, "missing_data": 3}