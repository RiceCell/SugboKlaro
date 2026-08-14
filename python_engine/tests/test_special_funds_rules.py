from datetime import date

import pandas as pd
import pytest

from ingest.schema import UCA_SCHEMA
from rules.base import RuleStatus
from rules.special_funds_rules import UCAAgingThresholdRule, UCAPastDueRule


def _row(
    name="TEST, DEBTOR",
    amount_balance=1000.0,
    date_granted=pd.Timestamp("2026-02-01"),
    purpose="Travel",
    fund_source="GENERAL FUND",
    cash_advance_type="Cash Advance - Travel",
    negative_balance=0.0,
    current_lt_30=0.0,
    current_31_90=0.0,
    current_91_365=0.0,
    past_due_over_1yr=0.0,
    past_due_over_2yr=0.0,
    past_due_3yr_plus=0.0,
):
    """Builds a single-row DataFrame matching UCA_SCHEMA so each rule can be
    tested in isolation against a controlled scenario, instead of only ever
    being exercised via the full real-file integration test."""
    return pd.DataFrame([{
        "doc_type": "UCA",
        "name_of_debtor": name,
        "amount_balance": amount_balance,
        "date_granted": date_granted,
        "purpose": purpose,
        "fund_source": fund_source,
        "cash_advance_type": cash_advance_type,
        "negative_balance": negative_balance,
        "current_lt_30": current_lt_30,
        "current_31_90": current_31_90,
        "current_91_365": current_91_365,
        "past_due_over_1yr": past_due_over_1yr,
        "past_due_over_2yr": past_due_over_2yr,
        "past_due_3yr_plus": past_due_3yr_plus,
    }])[UCA_SCHEMA]


# ---- UCAPastDueRule -------------------------------------------------------

def test_past_due_rule_flags_debt():
    df = _row(past_due_over_1yr=500.0)
    results = UCAPastDueRule().evaluate(df)
    assert len(results) == 1
    assert results[0].status == RuleStatus.FLAGGED
    assert results[0].details["balance_direction"] == "debt"


def test_past_due_rule_flags_credit_without_calling_it_debt():
    # Negative aging-bucket value = overpayment/credit sitting unresolved,
    # not money owed by the named person. Message and details must reflect
    # that direction, never phrase it as debt.
    df = _row(amount_balance=-400.0, past_due_over_1yr=-400.0)
    results = UCAPastDueRule().evaluate(df)
    assert len(results) == 1
    assert results[0].status == RuleStatus.FLAGGED
    assert results[0].details["balance_direction"] == "credit"
    # The message may still use the word "debt" as an explicit denial
    # ("...not debt owed by the payee") — that's fine. What must NOT happen
    # is a positive claim that the payee owes something.
    assert "is unliquidated" not in results[0].message.lower()
    assert "not debt owed" in results[0].message.lower()


def test_past_due_rule_passes_when_no_past_due_balance():
    df = _row(current_lt_30=1000.0)
    results = UCAPastDueRule().evaluate(df)
    assert len(results) == 1
    assert results[0].status == RuleStatus.PASS
    assert results[0].details["balance_direction"] == "none"


def test_past_due_rule_skips_none_placeholder_row():
    df = _row(
        name="NONE",
        amount_balance=None,
        date_granted=None,
        purpose="No unliquidated cash advances for this quarter - Submitted accordingly",
    )
    results = UCAPastDueRule().evaluate(df)
    assert results == []


# ---- UCAAgingThresholdRule --------------------------------------------------

def test_aging_threshold_rule_flags_grant_older_than_60_days_in_current_year():
    # More than 60 days before the Mar 31, 2026 reference date.
    df = _row(date_granted=pd.Timestamp("2026-01-15"))
    results = UCAAgingThresholdRule().evaluate(df)
    assert len(results) == 1
    assert results[0].status == RuleStatus.FLAGGED


def test_aging_threshold_rule_passes_recent_grant_in_current_year():
    # Within 60 days of the Mar 31, 2026 reference date.
    df = _row(date_granted=pd.Timestamp("2026-03-01"))
    results = UCAAgingThresholdRule().evaluate(df)
    assert len(results) == 1
    assert results[0].status == RuleStatus.PASS


def test_aging_threshold_rule_flags_missing_data_when_date_granted_is_missing():
    df = _row(date_granted=pd.NaT, purpose=None)
    results = UCAAgingThresholdRule().evaluate(df)
    assert len(results) == 1
    assert results[0].status == RuleStatus.MISSING_DATA


def test_aging_threshold_rule_skips_rows_outside_current_year():
    # A 2006 grant is genuinely old but out of scope for THIS rule — it's
    # already covered by UCAPastDueRule via the aging buckets. This rule
    # only concerns current-year (CY2026) grants per spec.
    df = _row(date_granted=pd.Timestamp("2006-02-28"), past_due_3yr_plus=461.47)
    results = UCAAgingThresholdRule().evaluate(df)
    assert results == []