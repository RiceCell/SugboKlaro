from config import BRCWGS_FILE as FILE
from ingest.parsers.procurement import parse_brcwgs_gs, parse_brcwgs_cw, parse_brcwgs_cs


def test_gs_parses_expected_row_count():
    df = parse_brcwgs_gs(FILE)
    assert len(df) == 24


def test_cw_none_for_period_returns_empty():
    df = parse_brcwgs_cw(FILE)
    assert not df.empty
    assert df.iloc[0]["reference_no"] == "NONE"
    assert "No bidded project" in df.iloc[0]["project_name"]

def test_gs_catches_missing_abc():
    df = parse_brcwgs_gs(FILE)
    assert df['abc'].isna().sum() == 3