<script setup lang="ts">
import { ref } from 'vue';
import ReportDetails from '../components/ReportDetails.vue';

const sample = ref({
      "rule_id": "PROC-001",
      "status": "missing_data",
      "message": "ABC or bid amount missing — cannot verify ceiling compliance",
      "legal_basis": {
        "law": "RA 9184",
        "section": "Sec. 31",
        "title": "Ceiling for Bid Prices"
      },
      "row_ref": 795,
      "details": {
        "project_name": "Procurement of Printing Services",
        "abc": null,
        "bid_amount": 398000.0,
        "winning_bidder": "F.F. Sibi Enterprises Incorporated"
      }
    });
</script>

<template>
  <main class="flex w-full h-full bg-linear-to-b from-dark-blue-gr-start to-dark-blue-gr-end overflow-hidden">
    <ReportDetails :data="sample" />
  </main>
</template>
