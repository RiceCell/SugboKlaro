from dataclasses import dataclass
from enum import Enum


class RuleStatus(str, Enum):
    PASS = "pass"
    FLAGGED = "flagged"
    MISSING_DATA = "missing_data"


@dataclass
class RuleResult:
    rule_id: str
    status: RuleStatus
    message: str
    legal_basis: dict
    row_ref: str | None = None

    def to_dict(self):
        return {
            "rule_id": self.rule_id,
            "status": self.status.value,
            "message": self.message,
            "legal_basis": self.legal_basis,
            "row_ref": self.row_ref,
        }


class Rule:
    id: str = "BASE"
    legal_basis: dict = {}

    def evaluate(self, df) -> list[RuleResult]:
        raise NotImplementedError(f"{self.__class__.__name__} must implement evaluate()")