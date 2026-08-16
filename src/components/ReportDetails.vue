<template>
  <div class="absolute z-10 bg-linear-to-b from-dark-blue-gr-start to-dark-blue-gr-end border border-slate-200 rounded-lg shadow-md font-sans overflow-hidden">
    
    <!-- HEADER -->
    <div class="flex justify-between items-center px-5 py-4 border-b border-slate-200">
      <h3 class="m-0 text-lg text-white font-semibold">{{ data.rule_id }}</h3>
      
      <!-- Check Trigger Button -->
      <button 
        type="button"
        @click="isModalOpen = true"
        class="border-cyan-gr-start border px-3.5 py-1 rounded-full text-xs font-bold text-cyan-gr-start tracking-wide uppercase transition-all duration-150 cursor-pointer shadow-xs hover:brightness-70 active:scale-95"
      >
        Check
      </button>
    </div>

    <!-- DETAILS (Starts here directly) -->
    <div class="px-5 py-4">
      <div class="flex justify-between items-center mb-3">
        <h4 class="m-0 text-sm text-white uppercase tracking-wide font-semibold">
          {{ getSectionTitle() }}
        </h4>
        <!-- Dynamic Composite Identifier Badge -->
        <span class="text-xs text-slate-600 bg-slate-100 px-2 py-0.5 rounded font-medium">
          {{ getReportBadge() }}
        </span>
      </div>
      
      <!-- TYPE 1: BRCWGS (Procurement Reports) -->
      <div v-if="docType === 'BRCWGS'" class="grid grid-cols-2 gap-4">
        <div class="flex flex-col col-span-2">
          <label class="text-xs text-white mb-1">Project Name</label>
          <span class="text-sm text-slate-200 font-medium">{{ data.details?.project_name || 'N/A' }}</span>
        </div>
        
        <div class="flex flex-col col-span-2">
          <label class="text-xs text-white mb-1">Winning Bidder</label>
          <span class="text-sm text-slate-200 font-medium">{{ data.details?.winning_bidder || 'N/A' }}</span>
        </div>

        <div class="flex flex-col">
          <label class="text-xs text-white mb-1">Approved Budget (ABC)</label>
          <span 
            class="text-sm font-medium"
            :class="data.details?.abc === null ? 'text-red-500 italic' : 'text-slate-200'"
          >
            {{ formatCurrency(data.details?.abc) }}
          </span>
        </div>

        <div class="flex flex-col">
          <label class="text-xs text-white mb-1">Bid Amount</label>
          <span 
            class="text-sm font-medium"
            :class="data.details?.bid_amount === null ? 'text-red-500 italic' : 'text-slate-200'"
          >
            {{ formatCurrency(data.details?.bid_amount) }}
          </span>
        </div>
      </div>

      <!-- TYPE 2: QSCF (Quarterly Statement of Cash Flow) -->
      <div v-else-if="docType === 'QSCF'" class="grid grid-cols-2 gap-4">
        <!-- QSCF BUD-001 -->
        <template v-if="data.details?.total_cash_inflow !== undefined">
          <div class="flex flex-col col-span-2">
            <label class="text-xs text-white mb-1">Fund Classification</label>
            <span class="text-sm text-slate-200 font-semibold">{{ data.details?.fund_type || data.row_ref }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Total Cash Inflow</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.total_cash_inflow) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Total Cash Outflow</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.total_cash_outflow) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Stated Net Operating</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.stated_net_operating) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Computed Net Operating</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.computed_net_operating) }}</span>
          </div>
        </template>

        <!-- QSCF BUD-002 -->
        <template v-else-if="data.details?.net_cash_investing !== undefined">
          <div class="flex flex-col col-span-2">
            <label class="text-xs text-white mb-1">Fund Classification</label>
            <span class="text-sm text-slate-200 font-semibold">{{ data.details?.fund_type || data.row_ref }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Net Cash Operating</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.net_cash_operating) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Net Cash Investing</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.net_cash_investing) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Stated Net Increase</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.stated_net_increase) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Computed Net Increase</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.computed_net_increase) }}</span>
          </div>
        </template>

        <!-- QSCF BUD-003 -->
        <template v-else-if="data.details?.beginning_balance !== undefined">
          <div class="flex flex-col col-span-2">
            <label class="text-xs text-white mb-1">Fund Classification</label>
            <span class="text-sm text-slate-200 font-semibold">{{ data.details?.fund_type || data.row_ref }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Beginning Cash Balance</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.beginning_balance) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Net Increase / (Decrease)</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.net_increase_cash) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Stated Ending Balance</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.stated_ending_balance) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Computed Ending Balance</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.computed_ending_balance) }}</span>
          </div>
        </template>

        <!-- QSCF BUD-004 -->
        <template v-else-if="data.details?.sum_of_funds !== undefined">
          <div class="flex flex-col col-span-2">
            <label class="text-xs text-white mb-1">Reconciliation Field</label>
            <span class="text-sm text-slate-200 font-semibold">{{ formatFieldName(data.details?.field) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Combined Stated Total</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.combined_stated) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Sum of Individual Funds</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.sum_of_funds) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">General Fund (GF)</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.gen_fund) }}</span>
          </div>
          <div class="flex flex-col">
            <label class="text-xs text-white mb-1">Special Education Fund (SEF)</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.sef) }}</span>
          </div>
          <div class="flex flex-col col-span-2">
            <label class="text-xs text-white mb-1">Trust Fund (TF)</label>
            <span class="text-sm text-slate-200 font-medium">{{ formatCurrency(data.details?.trust_fund) }}</span>
          </div>
        </template>
      </div>

      <!-- TYPE 3: UCA (Unliquidated Cash Advances) -->
      <div v-else-if="docType === 'UCA'" class="grid grid-cols-2 gap-4">
        <div class="flex flex-col col-span-2">
          <label class="text-xs text-white mb-1">Accountable Officer / Debtor</label>
          <span class="text-sm text-slate-200 font-medium">{{ data.details?.name_of_debtor || data.row_ref || 'N/A' }}</span>
        </div>

        <div class="flex flex-col col-span-2">
          <label class="text-xs text-white mb-1">Purpose</label>
          <span class="text-sm text-slate-200 font-medium">{{ data.details?.purpose || 'Beg Bal (Legacy Advance)' }}</span>
        </div>

        <div class="flex flex-col col-span-2">
          <label class="text-xs text-white mb-1">Cash Advance Classification</label>
          <span class="text-sm text-slate-200 font-medium">{{ data.details?.cash_advance_type || 'N/A' }}</span>
        </div>

        <div class="flex flex-col">
          <label class="text-xs text-white mb-1">Fund Source</label>
          <span class="text-sm text-slate-200 font-medium">{{ data.details?.fund_source || 'N/A' }}</span>
        </div>

        <div class="flex flex-col">
          <label class="text-xs text-white mb-1">Date Granted</label>
          <span class="text-sm text-slate-200 font-medium">{{ data.details?.date_granted || 'Legacy / Beg Bal' }}</span>
        </div>

        <div class="flex flex-col">
          <label class="text-xs text-white mb-1">Outstanding Balance</label>
          <span 
            class="text-sm font-medium"
            :class="data.details?.amount_balance < 0 ? 'text-amber-300' : 'text-slate-200'"
          >
            {{ formatCurrency(data.details?.amount_balance) }}
          </span>
        </div>

        <div class="flex flex-col">
          <label class="text-xs text-white mb-1">Balance Status</label>
          <span class="text-sm text-slate-200 font-medium">
            {{ formatBalanceDirection(data.details?.balance_direction) }}
          </span>
        </div>
      </div>
    </div>

    <!-- MODAL PORTAL -->
    <Teleport to="body">
      <ReportOverviewModal 
        v-if="isModalOpen" 
        :data="data" 
        @close="isModalOpen = false" 
      />
    </Teleport>

  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import ReportOverviewModal from './ReportOverviewModal.vue';

const props = defineProps<{
  data: any
}>(); 

const isModalOpen = ref(false);

const docType = computed(() => {
  if (props.data?.doc_type) return props.data.doc_type.toUpperCase();
  const ruleId = props.data?.rule_id || '';
  if (ruleId.startsWith('PROC')) return 'BRCWGS';
  if (ruleId.startsWith('BUD')) return 'QSCF';
  if (ruleId.startsWith('UCA')) return 'UCA';
  
  if (props.data?.details?.winning_bidder !== undefined || props.data?.details?.abc !== undefined) return 'BRCWGS';
  if (props.data?.details?.fund_type !== undefined || props.data?.details?.sum_of_funds !== undefined) return 'QSCF';
  if (props.data?.details?.name_of_debtor !== undefined || props.data?.details?.cash_advance_type !== undefined) return 'UCA';
  
  return 'BRCWGS';
});

const getSectionTitle = () => {
  switch (docType.value) {
    case 'QSCF':
      return 'Cash Flow Statement Details';
    case 'UCA':
      return 'Cash Advance Details';
    default:
      return 'Project Details';
  }
};

const getReportBadge = () => {
  const d = props.data;
  if (!d) return 'N/A';

  if (docType.value === 'QSCF') {
    if (d.details?.fund_type) return `Fund: ${d.details.fund_type}`;
    if (d.row_ref) return `Fund: ${d.row_ref}`;
    if (d.details?.field) return `Reconciliation: ${formatFieldName(d.details.field)}`;
    return 'QSCF • Cross-Fund';
  }

  if (docType.value === 'UCA') {
    const fund = d.details?.fund_source ? d.details.fund_source.replace(' FUND', '') : 'GF';
    const date = d.details?.date_granted || 'Beg Bal';
    return `${fund} • ${date}`;
  }

  return `Row #${d.row_ref ?? 'N/A'}`;
};

const getStatusClass = (status: string) => {
  const s = (status || '').toLowerCase();
  if (s === 'pass') return 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 hover:bg-emerald-500/30';
  if (s === 'flagged') return 'bg-rose-500/20 text-rose-300 border border-rose-500/40 hover:bg-rose-500/30';
  if (s === 'missing_data') return 'bg-amber-500/20 text-amber-300 border border-amber-500/40 hover:bg-amber-500/30';
  return 'bg-slate-500/20 text-slate-300 border border-slate-500/40 hover:bg-slate-500/30';
};

const formatCurrency = (value: any) => {
  if (value === null || value === undefined) return 'Missing / Not Provided';
  return new Intl.NumberFormat('en-PH', {
    style: 'currency',
    currency: 'PHP'
  }).format(value);
};

const formatFieldName = (name: string) => {
  if (!name) return 'Total Reconciliation';
  return name
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase());
};

const formatBalanceDirection = (direction: string) => {
  switch (direction) {
    case 'debt':
      return 'Debt (Unliquidated)';
    case 'credit':
      return 'Credit (Overpayment / Review)';
    case 'none':
      return 'Cleared (No Past-Due)';
    default:
      return direction ? direction.toUpperCase() : 'N/A';
  }
};
</script>