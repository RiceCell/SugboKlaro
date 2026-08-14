import pandas as pd


def chunk_brcwgs(df: pd.DataFrame) -> list[dict]:
    chunks = []
    for _, row in df.iterrows():
        if str(row.reference_no).upper() == "NONE":
            chunks.append({
                "id": f"BRCWGS-{row.doc_type}-NONE",
                "text": f"{row.doc_type}: No bidded project was reported for this quarter.",
                "metadata": {"doc_type": row.doc_type, "reference_no": "NONE"},
            })
            continue

        text = (
            f"Procurement record {row.reference_no} ({row.doc_type}): "
            f"project \"{row.project_name}\", "
            f"approved budget for contract (ABC) "
            f"{'₱%.2f' % row.abc if pd.notna(row.abc) else 'not stated'}, "
            f"won by {row.winning_bidder or 'unstated bidder'} "
            f"({row.bidder_address or 'address not stated'}) "
            f"at a bid amount of "
            f"{'₱%.2f' % row.bid_amount if pd.notna(row.bid_amount) else 'not stated'}, "
            f"bidding date {row.bidding_date or 'not stated'}."
        )
        chunks.append({
            "id": f"BRCWGS-{row.reference_no}",
            "text": text,
            "metadata": {
                "doc_type": row.doc_type,
                "reference_no": row.reference_no,
                "winning_bidder": row.winning_bidder,
                "abc": None if pd.isna(row.abc) else float(row.abc),
                "bid_amount": None if pd.isna(row.bid_amount) else float(row.bid_amount),
            },
        })
    return chunks


def chunk_uca(df: pd.DataFrame) -> list[dict]:
    chunks = []
    for i, row in df.iterrows():
        if str(row.name_of_debtor).upper() == "NONE":
            chunks.append({
                "id": "UCA-NONE",
                "text": "UCA: No unliquidated cash advances were reported for this quarter.",
                "metadata": {"doc_type": "UCA"},
            })
            continue

        granted = row.date_granted.strftime("%Y-%m-%d") if pd.notna(row.date_granted) else "not stated"
        text = (
            f"Unliquidated cash advance for {row.name_of_debtor}: "
            f"balance ₱{row.amount_balance:,.2f}, "
            f"granted {granted} for \"{row.purpose or 'unstated purpose'}\", "
            f"fund source {row.fund_source or 'unstated'}, "
            f"type {row.cash_advance_type or 'unstated'}. "
            f"Aging — past due over 1yr: ₱{row.past_due_over_1yr:,.2f}, "
            f"over 2yr: ₱{row.past_due_over_2yr:,.2f}, "
            f"3yr+: ₱{row.past_due_3yr_plus:,.2f}."
        )
        chunks.append({
            "id": f"UCA-{i}",
            "text": text,
            "metadata": {
                "doc_type": "UCA",
                "name_of_debtor": row.name_of_debtor,
                "amount_balance": float(row.amount_balance),
                "fund_source": row.fund_source,
            },
        })
    return chunks


def chunk_qscf(parsed: dict) -> list[dict]:
    chunks = []
    for fund_type, stmt in parsed.items():
        text = (
            f"Quarterly Statement of Cash Flows — {fund_type} fund, "
            f"Q{stmt.get('quarter')} CY{stmt.get('calendar_year')}, {stmt.get('lgu')}: "
            f"total cash inflow ₱{stmt.get('total_cash_inflow'):,.2f}, "
            f"total cash outflow ₱{stmt.get('total_cash_outflow'):,.2f}, "
            f"net cash from operating activities ₱{stmt.get('net_cash_operating'):,.2f}, "
            f"net cash from investing activities ₱{stmt.get('net_cash_investing'):,.2f}, "
            f"net increase in cash ₱{stmt.get('net_increase_cash'):,.2f}, "
            f"beginning balance ₱{stmt.get('beginning_balance'):,.2f}, "
            f"ending balance ₱{stmt.get('ending_balance'):,.2f}."
        )
        chunks.append({
            "id": f"QSCF-{fund_type}",
            "text": text,
            "metadata": {"doc_type": "QSCF", "fund_type": fund_type,
                         "quarter": stmt.get("quarter"), "calendar_year": stmt.get("calendar_year")},
        })
    return chunks
