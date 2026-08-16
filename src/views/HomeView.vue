<script setup lang="ts">
import { ref } from 'vue';
import ReportDetails from '../components/ReportDetails.vue';

const sample = ref({
      "rule_id": "UCA-001",
      "status": "flagged",
      "message": "₱100.00 of this cash advance is unliquidated past 1 year — exceeds COA Circular 97-002 liquidation deadlines",
      "legal_basis": {
        "law": "COA Circular No. 97-002",
        "section": "Liquidation Deadlines",
        "title": "Guidelines on the Grant, Utilization, and Liquidation of Cash Advances"
      },
      "row_ref": "ANDRES,GUILLERMO .",
      "details": {
        "name_of_debtor": "ANDRES,GUILLERMO .",
        "amount_balance": 100.0,
        "purpose": "Beg Bal",
        "date_granted": "2006-02-28",
        "fund_source": "GENERAL FUND",
        "cash_advance_type": "Cash Advance - Disbursing Officer (10305030-001)",
        "balance_direction": "debt"
      }
});

import Chatbot from '../components/Chatbot.vue';
</script>

<template>
    <ReportDetails :data="sample" />
    <Chatbot />
</template>
