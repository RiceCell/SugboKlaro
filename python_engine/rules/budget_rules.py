from rules.base import Rule, RuleResult, RuleStatus

QSCF_LEGAL_BASIS = {
    "law": "BLGF Memorandum Circular No. 09-2012",
    "section": "Annex 2",
    "title": "Statement of Cash Flows Format and Guidelines",
}

TOLERANCE = 1.00


def _close_enough(a, b, tolerance=TOLERANCE) -> bool:
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerance


class OperatingActivityIntegrityRule(Rule):
    id = "BUD-001"
    legal_basis = QSCF_LEGAL_BASIS

    def evaluate(self, parsed: dict) -> list[RuleResult]:
        results = []
        for fund_type, stmt in parsed.items():
            inflow = stmt.get("total_cash_inflow")
            outflow = stmt.get("total_cash_outflow")
            net_op = stmt.get("net_cash_operating")

            if inflow is None or outflow is None or net_op is None:
                results.append(RuleResult(self.id, RuleStatus.MISSING_DATA,
                    "Missing inflow, outflow, or net operating cash figure",
                    self.legal_basis, fund_type, {"fund_type": fund_type}))
                continue

            expected = inflow - outflow
            details = {"fund_type": fund_type, "total_cash_inflow": inflow,
                       "total_cash_outflow": outflow, "stated_net_operating": net_op,
                       "computed_net_operating": expected}

            if _close_enough(expected, net_op):
                results.append(RuleResult(self.id, RuleStatus.PASS,
                    "Total Inflow − Total Outflow matches stated Net Cash from Operating Activities",
                    self.legal_basis, fund_type, details))
            else:
                results.append(RuleResult(self.id, RuleStatus.FLAGGED,
                    f"Inflow (₱{inflow:,.2f}) minus Outflow (₱{outflow:,.2f}) = "
                    f"₱{expected:,.2f}, but the statement reports Net Cash from "
                    f"Operating Activities as ₱{net_op:,.2f} — figures do not reconcile",
                    self.legal_basis, fund_type, details))
        return results


class NetIncreaseIntegrityRule(Rule):
    id = "BUD-002"
    legal_basis = QSCF_LEGAL_BASIS

    def evaluate(self, parsed: dict) -> list[RuleResult]:
        results = []
        for fund_type, stmt in parsed.items():
            net_op = stmt.get("net_cash_operating")
            net_inv = stmt.get("net_cash_investing")
            net_increase = stmt.get("net_increase_cash")

            if net_op is None or net_inv is None or net_increase is None:
                results.append(RuleResult(self.id, RuleStatus.MISSING_DATA,
                    "Missing net operating, net investing, or net increase figure",
                    self.legal_basis, fund_type, {"fund_type": fund_type}))
                continue

            expected = net_op + net_inv
            details = {"fund_type": fund_type, "net_cash_operating": net_op,
                       "net_cash_investing": net_inv, "stated_net_increase": net_increase,
                       "computed_net_increase": expected}

            if _close_enough(expected, net_increase):
                results.append(RuleResult(self.id, RuleStatus.PASS,
                    "Net Operating + Net Investing matches stated Net Increase in Cash",
                    self.legal_basis, fund_type, details))
            else:
                results.append(RuleResult(self.id, RuleStatus.FLAGGED,
                    f"Net Operating (₱{net_op:,.2f}) + Net Investing (₱{net_inv:,.2f}) = "
                    f"₱{expected:,.2f}, but the statement reports Net Increase in Cash "
                    f"as ₱{net_increase:,.2f} — figures do not reconcile",
                    self.legal_basis, fund_type, details))
        return results


class CashBalanceIntegrityRule(Rule):
    id = "BUD-003"
    legal_basis = QSCF_LEGAL_BASIS

    def evaluate(self, parsed: dict) -> list[RuleResult]:
        results = []
        for fund_type, stmt in parsed.items():
            begin = stmt.get("beginning_balance")
            net_increase = stmt.get("net_increase_cash")
            end = stmt.get("ending_balance")

            if begin is None or net_increase is None or end is None:
                results.append(RuleResult(self.id, RuleStatus.MISSING_DATA,
                    "Missing beginning balance, net increase, or ending balance",
                    self.legal_basis, fund_type, {"fund_type": fund_type}))
                continue

            expected = begin + net_increase
            details = {"fund_type": fund_type, "beginning_balance": begin,
                       "net_increase_cash": net_increase, "stated_ending_balance": end,
                       "computed_ending_balance": expected}

            if _close_enough(expected, end):
                results.append(RuleResult(self.id, RuleStatus.PASS,
                    "Beginning Balance + Net Increase matches stated Ending Balance",
                    self.legal_basis, fund_type, details))
            else:
                results.append(RuleResult(self.id, RuleStatus.FLAGGED,
                    f"Beginning Balance (₱{begin:,.2f}) + Net Increase (₱{net_increase:,.2f}) "
                    f"= ₱{expected:,.2f}, but the statement reports Ending Balance as "
                    f"₱{end:,.2f} — figures do not reconcile",
                    self.legal_basis, fund_type, details))
        return results


class FundReconciliationRule(Rule):
    id = "BUD-004"
    legal_basis = QSCF_LEGAL_BASIS

    def evaluate(self, parsed: dict) -> list[RuleResult]:
        required = ["COMBINED", "GEN FUND", "SEF", "TRUST FUND"]
        if not all(k in parsed for k in required):
            return [RuleResult(self.id, RuleStatus.MISSING_DATA,
                "One or more fund tabs (COMBINED, GEN FUND, SEF, TRUST FUND) missing — cannot reconcile",
                self.legal_basis, None, {})]

        combined = parsed["COMBINED"]
        components = [parsed["GEN FUND"], parsed["SEF"], parsed["TRUST FUND"]]

        results = []
        for field, label in [("total_cash_inflow", "Total Cash Inflow"),
                              ("total_cash_outflow", "Total Cash Outflow")]:
            combined_val = combined.get(field)
            component_vals = [c.get(field) for c in components]

            if combined_val is None or any(v is None for v in component_vals):
                results.append(RuleResult(self.id, RuleStatus.MISSING_DATA,
                    f"Missing {label} in COMBINED or one of the fund tabs",
                    self.legal_basis, None, {"field": field}))
                continue

            summed = sum(component_vals)
            details = {"field": field, "combined_stated": combined_val,
                       "gen_fund": component_vals[0], "sef": component_vals[1],
                       "trust_fund": component_vals[2], "sum_of_funds": summed}

            if _close_enough(summed, combined_val):
                results.append(RuleResult(self.id, RuleStatus.PASS,
                    f"COMBINED {label} matches the sum of GEN FUND + SEF + TRUST FUND",
                    self.legal_basis, None, details))
            else:
                results.append(RuleResult(self.id, RuleStatus.FLAGGED,
                    f"COMBINED {label} is ₱{combined_val:,.2f}, but GEN FUND + SEF + "
                    f"TRUST FUND sums to ₱{summed:,.2f} — the reported totals do not reconcile",
                    self.legal_basis, None, details))
        return results


BUDGET_RULES = [
    OperatingActivityIntegrityRule(),
    NetIncreaseIntegrityRule(),
    CashBalanceIntegrityRule(),
    FundReconciliationRule(),
]