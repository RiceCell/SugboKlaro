import json
from config import BRCWGS_FILE
from ingest.parsers.procurement import parse_brcwgs
from rules.procurement_rules import PROCUREMENT_RULES

RULESETS = {
    "BRCWGS": (parse_brcwgs, PROCUREMENT_RULES),
}


def run_check(doc_type: str, filepath: str) -> dict:
    if doc_type not in RULESETS:
        raise ValueError(f"No ruleset registered for doc_type '{doc_type}'")

    parser_fn, rules = RULESETS[doc_type]
    df = parser_fn(filepath)

    all_results = []
    for rule in rules:
        all_results.extend(rule.evaluate(df))

    summary = {"pass": 0, "flagged": 0, "missing_data": 0}
    for r in all_results:
        summary[r.status.value] += 1

    return {
        "doc_type": doc_type,
        "row_count": len(df),
        "results": [r.to_dict() for r in all_results],
        "summary": summary,
    }


if __name__ == "__main__":
    output = run_check("BRCWGS", BRCWGS_FILE)
    print(json.dumps(output, indent=2, ensure_ascii=False))