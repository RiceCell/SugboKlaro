# THREE: takes parsed stuff and we run the flag checks here through math / logic

import pandas as pd
from rules.base import Rule, RuleResult, RuleStatus

ABC_EXEMPT_DOC_TYPES = {"BRCWGS_CS"}


class ABCCeilingRule(Rule):
    id = "PROC-001"
    legal_basis = {"law": "RA 9184", "section": "Sec. 31", "title": "Ceiling for Bid Prices"}

    def evaluate(self, df: pd.DataFrame) -> list[RuleResult]:
        results = []
        checkable = df[~df["doc_type"].isin(ABC_EXEMPT_DOC_TYPES)]
    
        for _, row in checkable.iterrows():
            # NEW: Skip compliant "NONE FOR THE PERIOD" placeholder rows
            if str(row.reference_no).upper() == "NONE":
                continue

            if pd.isna(row.abc) or pd.isna(row.bid_amount):
                results.append(RuleResult(self.id, RuleStatus.MISSING_DATA,
                    "ABC or bid amount missing — cannot verify ceiling compliance",
                    self.legal_basis, row.reference_no))
            elif row.bid_amount > row.abc:
                results.append(RuleResult(self.id, RuleStatus.FLAGGED,
                    f"Bid ₱{row.bid_amount:,.2f} exceeds ABC ₱{row.abc:,.2f}",
                    self.legal_basis, row.reference_no))
            else:
                results.append(RuleResult(self.id, RuleStatus.PASS,
                    "Bid within ABC ceiling", self.legal_basis, row.reference_no))
        return results


class ZeroVarianceBiddingRule(Rule):
    id = "PROC-002"
    legal_basis = {"law": "RA 9184", "section": "Sec. 3", "title": "Policy — Competitiveness"}
    threshold = 0.01

    def evaluate(self, df: pd.DataFrame) -> list[RuleResult]:
        checkable = df[~df["doc_type"].isin(ABC_EXEMPT_DOC_TYPES)].copy()
        
        # NEW: Skip compliant placeholder rows before doing math
        checkable = checkable[checkable["reference_no"].astype(str).str.upper() != "NONE"]
        
        checkable = checkable.dropna(subset=["abc", "bid_amount"])
        if checkable.empty:
            return []

        checkable["variance"] = (checkable["abc"] - checkable["bid_amount"]).abs() / checkable["abc"]
        flagged = checkable[checkable["variance"] <= self.threshold]

        return [
            RuleResult(self.id, RuleStatus.FLAGGED,
                f"Bid within {self.threshold * 100:.0f}% of ABC — an indicator "
                f"commonly associated with reduced price competition",
                self.legal_basis, row.reference_no)
            for _, row in flagged.iterrows()
        ]


class VendorConcentrationRule(Rule):
    id = "PROC-003"
    legal_basis = {"law": "RA 9184", "section": "Sec. 3", "title": "Policy — Competitiveness"}
    win_threshold = 3

    def evaluate(self, df: pd.DataFrame) -> list[RuleResult]:
        # Filter out empty placeholder rows and unawarded contracts
        valid_df = df[df["reference_no"].astype(str).str.upper() != "NONE"].copy()
        valid_df = valid_df.dropna(subset=["winning_bidder"])
        
        if valid_df.empty:
            return []
            
        counts = valid_df.groupby("winning_bidder").size()
        concentrated = counts[counts >= self.win_threshold]
        
        return [
            RuleResult(self.id, RuleStatus.FLAGGED,
                f"{vendor} won {n} contracts this quarter — an indicator worth reviewing "
                f"for procurement diversity",
                self.legal_basis, None)
            for vendor, n in concentrated.items()
        ]


PROCUREMENT_RULES = [ABCCeilingRule(), ZeroVarianceBiddingRule(), VendorConcentrationRule()]