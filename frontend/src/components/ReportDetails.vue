<template>
  <div class="absolute size-full bg-white border border-slate-200 rounded-lg shadow-md font-sans overflow-hidden">
    
    <!-- Header: Rule ID and Status -->
    <div class="flex justify-between items-center px-5 py-4 bg-slate-50 border-b border-slate-200">
      <h3 class="m-0 text-lg text-slate-900 font-semibold">{{ data.rule_id }}</h3>
      <span 
        class="px-2.5 py-1 rounded-full text-xs font-semibold tracking-wide uppercase"
      >
        {{ formatStatus(data.status) }}
      </span>
    </div>

    <!-- Alert Message -->
    <div class="px-5 py-4 bg-amber-50 text-amber-800 border-b border-slate-200 font-medium">
      <p class="m-0">{{ data.message }}</p>
    </div>

    <!-- Legal Basis Section -->
    <div class="px-5 py-4 border-b border-slate-200 last:border-b-0">
      <h4 class="mb-3 text-sm text-slate-500 uppercase tracking-wide font-semibold">Legal Basis</h4>
      <div class="text-sm text-slate-800">
        <span class="bg-sky-100 text-sky-700 px-1.5 py-0.5 rounded text-xs font-bold mr-2">
          {{ data.legal_basis.law }}
        </span>
        <strong>{{ data.legal_basis.section }}:</strong> 
        {{ data.legal_basis.title }}
      </div>
    </div>

    <!-- Details Section -->
    <div class="px-5 py-4 border-b border-slate-200 last:border-b-0">
      <div class="flex justify-between items-center mb-3">
        <h4 class="m-0 text-sm text-slate-500 uppercase tracking-wide font-semibold">Project Details</h4>
        <span class="text-xs text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
          Row #{{ data.row_ref }}
        </span>
      </div>
      
      <div class="grid grid-cols-2 gap-4">
        <!-- Full Width Items -->
        <div class="flex flex-col col-span-2">
          <label class="text-xs text-slate-500 mb-1">Project Name</label>
          <span class="text-sm text-slate-900 font-medium">{{ data.details.project_name || 'N/A' }}</span>
        </div>
        
        <div class="flex flex-col col-span-2">
          <label class="text-xs text-slate-500 mb-1">Winning Bidder</label>
          <span class="text-sm text-slate-900 font-medium">{{ data.details.winning_bidder || 'N/A' }}</span>
        </div>

        <!-- Half Width Items -->
        <div class="flex flex-col">
          <label class="text-xs text-slate-500 mb-1">Approved Budget (ABC)</label>
          <span 
            class="text-sm font-medium"
            :class="data.details.abc === null ? 'text-red-500 italic' : 'text-slate-900'"
          >
            {{ formatCurrency(data.details.abc) }}
          </span>
        </div>

        <div class="flex flex-col">
          <label class="text-xs text-slate-500 mb-1">Bid Amount</label>
          <span 
            class="text-sm font-medium"
            :class="data.details.bid_amount === null ? 'text-red-500 italic' : 'text-slate-900'"
          >
            {{ formatCurrency(data.details.bid_amount) }}
          </span>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup lang="ts">

const props = defineProps<{
    data: any
}>(); 

// Utility to format "missing_data" into "MISSING DATA"
const formatStatus = (status: any) => {
  if (!status) return 'UNKNOWN';
  return status.replace(/_/g, ' ').toUpperCase();
};

// Utility to format numbers into currency (defaults to PHP based on RA 9184)
const formatCurrency = (value: any) => {
  if (value === null || value === undefined) return 'Missing / Not Provided';
  
  return new Intl.NumberFormat('en-PH', {
    style: 'currency',
    currency: 'PHP'
  }).format(value);
};
</script>