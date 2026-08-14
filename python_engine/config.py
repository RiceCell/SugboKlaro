from pathlib import Path
PYTHON_ENGINE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PYTHON_ENGINE_DIR.parent
DATA_DIR = REPO_ROOT / "data"
BRCWGS_FILE = str(DATA_DIR / "raw_2026_excel" / "brcwgs_2026.xlsx")
UCA_FILE = str(DATA_DIR / "raw_2026_excel" / "uca_2026.xlsx")