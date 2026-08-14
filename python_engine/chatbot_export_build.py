# python_engine/chatbot_export_build.py

import json
from config import BRCWGS_FILE, UCA_FILE, QSCF_FILE, CHATBOT_SOURCES_FILE
from ingest.parsers.procurement import parse_brcwgs
from ingest.parsers.special_funds import parse_uca
from ingest.parsers.budget import parse_qscf
from ingest.chatbot_export import chunk_brcwgs, chunk_uca, chunk_qscf

JOBS = [
    ("BRCWGS", lambda: chunk_brcwgs(parse_brcwgs(BRCWGS_FILE))),
    ("UCA", lambda: chunk_uca(parse_uca(UCA_FILE))),
    ("QSCF", lambda: chunk_qscf(parse_qscf(QSCF_FILE))),
]


def build_all():
    all_chunks = []
    for doc_type, fn in JOBS:
        chunks = fn()
        all_chunks.extend(chunks)
        print(f"{doc_type}: {len(chunks)} chunks")

    with open(CHATBOT_SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    print(f"Wrote {CHATBOT_SOURCES_FILE} — {len(all_chunks)} total chunks")


if __name__ == "__main__":
    build_all()