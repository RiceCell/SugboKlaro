from config import UCA_FILE
from engine import run_check

# Locked-in known-good run, verified against the real Q1 2026 Cebu City UCA
# file (data/raw_2026_excel/uca_2026.xlsx). If this ever breaks, it means
# either the source file changed or a rule/parser change had a side effect
# nobody intended — same pattern as Pipeline B's BRCWGS regression test.
EXPECTED_SUMMARY = {"pass": 128, "flagged": 683, "missing_data": 4}
EXPECTED_ROW_COUNT = 810


def test_uca_known_good_run():
    result = run_check("UCA", UCA_FILE)
    assert result["row_count"] == EXPECTED_ROW_COUNT
    assert result["summary"] == EXPECTED_SUMMARY
    assert len(result["results"]) == sum(EXPECTED_SUMMARY.values())