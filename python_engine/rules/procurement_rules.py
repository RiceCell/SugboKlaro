# THREE: takes parsed stuff and we run the flag checks here through math / logic

import pandas as pd
from rules.base import Rule, RuleResult, RuleStatus

ABC_EXEMPT_DOC_TYPES = {"BRCWGS_CS"}


def _base_details(row) -> dict:
    """Every result carries these so the frontend never has to
    cross-reference back to the raw parsed data separately."""
    return {
        "project_name": row.project_name,
        "abc": None if pd.isna(row.abc) else float(row.abc),
        "bid_amount": None if pd.isna(row.bid_amount) else float(row.bid_amount),
        "winning_bidder": row.winning_bidder,
    }


class ABCCeilingRule(Rule):
    id = "PROC-001"
    legal_basis = {"law": "RA 9184", "section": "Sec. 31", "title": "Ceiling for Bid Prices"}

    def evaluate(self, df: pd.DataFrame) -> list[RuleResult]:
        results = []
        checkable = df[~df["doc_type"].isin(ABC_EXEMPT_DOC_TYPES)]

        for _, row in checkable.iterrows():
            if str(row.reference_no).upper() == "NONE":
                continue

            details = _base_details(row)

            if pd.isna(row.abc) or pd.isna(row.bid_amount):
                results.append(RuleResult(self.id, RuleStatus.MISSING_DATA,
                    "ABC or bid amount missing — cannot verify ceiling compliance",
                    self.legal_basis, row.reference_no, details))
            elif row.bid_amount > row.abc:
                results.append(RuleResult(self.id, RuleStatus.FLAGGED,
                    f"Bid ₱{row.bid_amount:,.2f} exceeds ABC ₱{row.abc:,.2f}",
                    self.legal_basis, row.reference_no, details))
            else:
                results.append(RuleResult(self.id, RuleStatus.PASS,
                    "Bid within ABC ceiling", self.legal_basis, row.reference_no, details))
        return results


class ZeroVarianceBiddingRule(Rule):
    id = "PROC-002"
    legal_basis = {"law": "RA 9184", "section": "Sec. 3", "title": "Policy — Competitiveness"}
    threshold = 0.01

    def evaluate(self, df: pd.DataFrame) -> list[RuleResult]:
        checkable = df[~df["doc_type"].isin(ABC_EXEMPT_DOC_TYPES)].copy()
        checkable = checkable[checkable["reference_no"].astype(str).str.upper() != "NONE"]
        checkable = checkable.dropna(subset=["abc", "bid_amount"])
        if checkable.empty:
            return []

        checkable["variance"] = (checkable["abc"] - checkable["bid_amount"]).abs() / checkable["abc"]
        flagged = checkable[checkable["variance"] <= self.threshold]

        return [
            RuleResult(self.id, RuleStatus.FLAGGED,
                f"Bid ₱{row.bid_amount:,.2f} is within {self.threshold * 100:.0f}% of "
                f"ABC ₱{row.abc:,.2f} — an indicator commonly associated with "
                f"reduced price competition",
                self.legal_basis, row.reference_no, _base_details(row))
            for _, row in flagged.iterrows()
        ]


class VendorConcentrationRule(Rule):
    id = "PROC-003"
    legal_basis = {"law": "RA 9184", "section": "Sec. 3", "title": "Policy — Competitiveness"}
    win_threshold = 3

    def evaluate(self, df: pd.DataFrame) -> list[RuleResult]:
        valid_df = df[df["reference_no"].astype(str).str.upper() != "NONE"].copy()
        valid_df = valid_df.dropna(subset=["winning_bidder"])

        if valid_df.empty:
            return []

        counts = valid_df.groupby("winning_bidder").size()
        concentrated = counts[counts >= self.win_threshold]

        results = []
        for vendor, n in concentrated.items():
            won_refs = valid_df[valid_df["winning_bidder"] == vendor]["reference_no"].tolist()
            results.append(RuleResult(self.id, RuleStatus.FLAGGED,
                f"{vendor} won {n} contracts this quarter — an indicator worth reviewing "
                f"for procurement diversity",
                self.legal_basis, None,
                {"winning_bidder": vendor, "contract_count": n, "reference_nos": won_refs}))
        return results


PROCUREMENT_RULES = [ABCCeilingRule(), ZeroVarianceBiddingRule(), VendorConcentrationRule()]