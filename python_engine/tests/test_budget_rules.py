from config import QSCF_FILE as FILE
from ingest.parsers.budget import parse_qscf
from rules.budget_rules import (
    OperatingActivityIntegrityRule,
    NetIncreaseIntegrityRule,
    CashBalanceIntegrityRule,
    FundReconciliationRule,
)
from rules.base import RuleStatus


def get_parsed():
    return parse_qscf(FILE)


def test_parser_returns_all_four_tabs():
    parsed = get_parsed()
    assert set(parsed.keys()) == {"COMBINED", "GEN FUND", "SEF", "TRUST FUND"}


def test_parser_captures_expected_combined_totals():
    parsed = get_parsed()
    combined = parsed["COMBINED"]
    assert combined["total_cash_inflow"] == 1060079146.69
    assert combined["total_cash_outflow"] == 1427755884.29
    assert combined["quarter"] == 1
    assert combined["calendar_year"] == 2026


def test_operating_activity_rule_passes_on_real_data():
    parsed = get_parsed()
    results = OperatingActivityIntegrityRule().evaluate(parsed)
    assert len(results) == 4
    assert all(r.status == RuleStatus.PASS for r in results)


def test_net_increase_rule_passes_on_real_data():
    parsed = get_parsed()
    results = NetIncreaseIntegrityRule().evaluate(parsed)
    assert len(results) == 4
    assert all(r.status == RuleStatus.PASS for r in results)


def test_cash_balance_rule_passes_on_real_data():
    parsed = get_parsed()
    results = CashBalanceIntegrityRule().evaluate(parsed)
    assert len(results) == 4
    assert all(r.status == RuleStatus.PASS for r in results)


def test_fund_reconciliation_rule_passes_on_real_data():
    parsed = get_parsed()
    results = FundReconciliationRule().evaluate(parsed)
    assert len(results) == 2
    assert all(r.status == RuleStatus.PASS for r in results)


def test_operating_activity_rule_catches_intentional_break():
    parsed = get_parsed()
    tampered = {**parsed}
    tampered["COMBINED"] = {**parsed["COMBINED"], "net_cash_operating": 999999999}
    results = OperatingActivityIntegrityRule().evaluate(tampered)
    combined_result = next(r for r in results if r.row_ref == "COMBINED")
    assert combined_result.status == RuleStatus.FLAGGED


def test_full_summary_matches_known_good_run():
    from engine import run_check
    output = run_check("QSCF", FILE)
    assert output["summary"] == {"pass": 14, "flagged": 0, "missing_data": 0}