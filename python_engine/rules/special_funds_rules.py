# THREE: takes parsed stuff and we run the flag checks here through math / logic
# (SPECIAL PURPOSE FUND REPORTS — Pipeline C, starting with UCA)

from datetime import date, timedelta

import pandas as pd
from rules.base import Rule, RuleResult, RuleStatus

UCA_LEGAL_BASIS = {
    "law": "COA Circular No. 97-002",
    "section": "Liquidation Deadlines",
    "title": "Guidelines on the Grant, Utilization, and Liquidation of Cash Advances",
}


def _base_details(row) -> dict:
    """Every result carries these so the frontend never has to cross-reference
    back to the raw parsed data separately (same pattern as Pipeline B)."""
    return {
        "name_of_debtor": row.name_of_debtor,
        "amount_balance": None if pd.isna(row.amount_balance) else float(row.amount_balance),
        "purpose": None if pd.isna(row.purpose) else row.purpose,
        "date_granted": None if pd.isna(row.date_granted) else row.date_granted.strftime("%Y-%m-%d"),
        "fund_source": row.fund_source,
        "cash_advance_type": row.cash_advance_type,
    }


def _checkable(df: pd.DataFrame) -> pd.DataFrame:
    """Excludes the 'NONE' placeholder row used when a quarter has zero
    unliquidated cash advances (parser's compliant-empty-form case)."""
    return df[df["name_of_debtor"].astype(str).str.upper() != "NONE"]


class UCAPastDueRule(Rule):
    id = "UCA-001"
    legal_basis = UCA_LEGAL_BASIS
    PAST_DUE_COLS = ["past_due_over_1yr", "past_due_over_2yr", "past_due_3yr_plus"]

    def evaluate(self, df: pd.DataFrame) -> list[RuleResult]:
        results = []
        for _, row in _checkable(df).iterrows():
            details = _base_details(row)
            past_due_total = sum(getattr(row, c) for c in self.PAST_DUE_COLS)

            if past_due_total > 0:
                # Debtor genuinely owes an unliquidated balance sitting past 1 year.
                results.append(RuleResult(self.id, RuleStatus.FLAGGED,
                    f"₱{past_due_total:,.2f} of this cash advance is unliquidated "
                    f"past 1 year — exceeds COA Circular 97-002 liquidation deadlines",
                    self.legal_basis, row.name_of_debtor,
                    {**details, "balance_direction": "debt"}))
            elif past_due_total < 0:
                # Negative aging-bucket value = a credit/overpayment balance, not
                # debt owed by the person. ~1/3 of rows in this file are negative
                # (confirmed against real data) — flagging these as "unliquidated
                # debt" would misrepresent a real, named person's record. Still
                # worth surfacing (an unresolved credit sitting >1 year is its own
                # accounting/data-quality issue) but the message must not imply
                # the debtor owes money.
                results.append(RuleResult(self.id, RuleStatus.FLAGGED,
                    f"₱{abs(past_due_total):,.2f} credit/overpayment balance has been "
                    f"sitting unresolved past 1 year — recommend accounting review, "
                    f"this is not debt owed by the payee",
                    self.legal_basis, row.name_of_debtor,
                    {**details, "balance_direction": "credit"}))
            else:
                results.append(RuleResult(self.id, RuleStatus.PASS,
                    "No past-due balance", self.legal_basis, row.name_of_debtor,
                    {**details, "balance_direction": "none"}))
        return results


class UCAAgingThresholdRule(Rule):
    id = "UCA-002"
    legal_basis = UCA_LEGAL_BASIS 
    # Q1 2026 end-of-period reference date, per the form's declared CY/Quarter.
    #  Check against the declared quarter-end per the
    # original spec; MISSING_DATA/FLAGGED results should note this caveat is
    # a human-review item, not silently resolved one way or the other.
    REFERENCE_DATE = date(2026, 3, 31)
    LIQUIDATION_WINDOW_DAYS = 60

    def evaluate(self, df: pd.DataFrame) -> list[RuleResult]:
        results = []
        cutoff = self.REFERENCE_DATE - timedelta(days=self.LIQUIDATION_WINDOW_DAYS)

        for _, row in _checkable(df).iterrows():
            details = _base_details(row)

            if pd.isna(row.date_granted):
                results.append(RuleResult(self.id, RuleStatus.MISSING_DATA,
                    "Date Granted missing — cannot verify liquidation window",
                    self.legal_basis, row.name_of_debtor, details))
                continue

            granted = row.date_granted.date()
            if granted.year != self.REFERENCE_DATE.year:
                continue  # out of scope: rule targets current-year (CY2026) grants only

            if granted < cutoff:
                days_out = (self.REFERENCE_DATE - granted).days
                results.append(RuleResult(self.id, RuleStatus.FLAGGED,
                    f"Cash advance granted {granted.isoformat()} — {days_out} days before "
                    f"quarter-end, exceeding the {self.LIQUIDATION_WINDOW_DAYS}-day standard "
                    f"liquidation window under COA Circular 97-002",
                    self.legal_basis, row.name_of_debtor, details))
            else:
                results.append(RuleResult(self.id, RuleStatus.PASS,
                    "Within standard liquidation window", self.legal_basis,
                    row.name_of_debtor, details))
        return results


UCA_RULES = [UCAPastDueRule(), UCAAgingThresholdRule()]