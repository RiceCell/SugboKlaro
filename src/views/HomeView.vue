<script setup lang="ts">
import { ref } from 'vue';
import HelloWorld from './Landing.vue/index.js'
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
  "row_ref": 1298,
  "details": {
    "project_name": "Procurement of Toners & Cartridges",
    "abc": null,
    "bid_amount": 1244796.0,
    "winning_bidder": "SO Photo Print Trading"
  }
});

import Chatbot from '../components/Chatbot.vue';
</script>

<template>
    <ReportDetails :data="sample" />
    <Chatbot />
</template>
