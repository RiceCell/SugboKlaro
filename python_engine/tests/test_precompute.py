# tests/test_precompute.py
import json
from config import REPO_ROOT

def test_precompute_output_exists_and_matches_known_summary():
    output_path = REPO_ROOT / "data" / "compliance_results" / "brcwgs.json"
    assert output_path.exists(), "Run precompute.py first"

    with open(output_path) as f:
        data = json.load(f)

    assert data["summary"] == {"pass": 21, "flagged": 8, "missing_data": 3}
    assert data["row_count"] == 26

    # Every flagged/missing_data result should have real details, not empty
    for r in data["results"]:
        if r["status"] in ("flagged", "missing_data"):
            assert r["details"], f"Result {r['rule_id']} has empty details"