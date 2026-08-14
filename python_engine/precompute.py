# python_engine/precompute.py
import json
from pathlib import Path
from config import BRCWGS_FILE, UCA_FILE, REPO_ROOT
from engine import run_check

OUTPUT_DIR = REPO_ROOT / "data" / "compliance_results"

def precompute_all():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    jobs = [
        ("BRCWGS", BRCWGS_FILE),
        ("UCA", UCA_FILE),
    ]

    for doc_type, filepath in jobs:
        result = run_check(doc_type, filepath)
        out_path = OUTPUT_DIR / f"{doc_type.lower()}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Wrote {out_path} — {result['summary']}")

if __name__ == "__main__":
    precompute_all()