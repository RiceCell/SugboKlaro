<script setup lang="ts">
import { ref } from 'vue';
import ReportDetails from '../components/ReportDetails.vue';

const sample = ref({
      "rule_id": "UCA-001",
      "status": "pass",
      "message": "No past-due balance",
      "legal_basis": {
        "law": "COA Circular No. 97-002",
        "section": "Liquidation Deadlines",
        "title": "Guidelines on the Grant, Utilization, and Liquidation of Cash Advances"
      },
      "row_ref": "AMAHAN, ALJUN . [OTH82514]",
      "details": {
        "name_of_debtor": "AMAHAN, ALJUN . [OTH82514]",
        "amount_balance": -6000.0,
        "purpose": "Payment of Approved Payrolls",
        "date_granted": "2026-02-28",
        "fund_source": "GENERAL FUND",
        "cash_advance_type": "Cash Advance - Disbursing Officer (10305030-001)",
        "balance_direction": "none"
      }
});

import Chatbot from '../components/Chatbot.vue';
</script>

<template>
    <ReportDetails :data="sample" />
    <Chatbot />
</template>
