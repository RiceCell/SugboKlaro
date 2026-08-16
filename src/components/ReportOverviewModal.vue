<template>
  <div 
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs font-sans"
    @click.self="$emit('close')"
  >
    <div class="relative w-full max-w-2xl bg-linear-to-b from-dark-blue-gr-start to-dark-blue-gr-end border border-slate-200/30 rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
      
      <!-- Modal Header -->
      <div class="flex justify-between items-center px-6 py-4 border-b border-slate-200/20">
        <div class="flex items-center gap-3">
          <h3 class="m-0 text-lg text-white font-bold tracking-tight">
            {{ data.rule_id }}
          </h3>
          <span 
            class="px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide uppercase"
            :class="getStatusClass(data.status)"
          >
            {{ formatStatus(data.status) }}
          </span>
        </div>
        
        <button 
          type="button"
          @click="$emit('close')"
          class="text-slate-400 hover:text-white transition-colors p-1 rounded-lg hover:bg-white/10 cursor-pointer"
          aria-label="Close modal"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 overflow-y-auto space-y-6">
        
        <!-- SECTION 1: LEGAL BASIS (Renders immediately) -->
        <div class="bg-white/5 border border-white/10 rounded-lg p-4">
          <div class="flex items-center gap-2 mb-2">
            <svg class="w-4 h-4 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
            </svg>
            <h4 class="m-0 text-xs font-bold text-white uppercase tracking-wider">
              Legal Basis & Regulatory Standard
            </h4>
          </div>

          <div class="text-sm text-slate-200 leading-relaxed">
            <span class="bg-sky-100 text-sky-800 px-2 py-0.5 rounded text-xs font-bold mr-2">
              {{ data.legal_basis?.law || 'N/A' }}
            </span>
            <strong>{{ data.legal_basis?.section }}:</strong> 
            {{ data.legal_basis?.title }}
          </div>

          <div v-if="data.message" class="mt-3 text-xs text-slate-300 italic bg-black/20 p-3 rounded border border-white/5">
            {{ data.message }}
          </div>
        </div>

        <!-- SECTION 2: AI OVERVIEW (Loads below legal basis) -->
        <div class="bg-white/5 border border-sky-400/20 rounded-lg p-4">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 text-amber-300" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2L14.4 7.6L20 10L14.4 12.4L12 18L9.6 12.4L4 10L9.6 7.6L12 2Z" />
              </svg>
              <h4 class="m-0 text-xs font-bold text-white uppercase tracking-wider">
                AI Overview
              </h4>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="isLoading" class="py-4 flex flex-col items-center justify-center gap-3">
            <div class="w-6 h-6 border-2 border-sky-400 border-t-transparent rounded-full animate-spin"></div>
            <p class="text-xs text-slate-300 animate-pulse m-0">Generating AI compliance summary...</p>
          </div>

          <!-- Error State -->
          <div v-else-if="errorMessage" class="text-xs text-rose-300 bg-rose-500/10 p-3 rounded border border-rose-500/20 flex justify-between items-center">
            <span>{{ errorMessage }}</span>
            <button 
              @click="fetchOverview" 
              class="text-xs text-white underline hover:text-sky-300 cursor-pointer"
            >
              Retry
            </button>
          </div>

          <!-- Content Output -->
          <div v-else class="text-sm text-slate-100 leading-relaxed font-normal">
            {{ aiOverviewText }}
          </div>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="flex justify-end px-6 py-3 border-t border-slate-200/20 bg-black/10">
        <button 
          type="button" 
          @click="$emit('close')"
          class="px-4 py-1.5 text-xs font-semibold text-slate-200 bg-white/10 hover:bg-white/20 rounded-md transition-colors cursor-pointer"
        >
          Close
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { generateProjectOverview } from '../services/aiOverview';

const props = defineProps<{
  data: any
}>();

const emit = defineEmits<{
  (e: 'close'): void
}>();

const isLoading = ref<boolean>(true);
const aiOverviewText = ref<string>('');
const errorMessage = ref<string | null>(null);

const fetchOverview = async () => {
  isLoading.value = true;
  errorMessage.value = null;

  try {
    aiOverviewText.value = await generateProjectOverview(props.data);
  } catch (error) {
    errorMessage.value = 'Failed to load AI overview. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

const formatStatus = (status: string) => {
  if (!status) return 'UNKNOWN';
  return status.replace(/_/g, ' ').toUpperCase();
};

const getStatusClass = (status: string) => {
  const s = (status || '').toLowerCase();
  if (s === 'pass') return 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
  if (s === 'flagged') return 'bg-rose-500/20 text-rose-300 border border-rose-500/30';
  if (s === 'missing_data') return 'bg-amber-500/20 text-amber-300 border border-amber-500/30';
  return 'bg-slate-500/20 text-slate-300 border border-slate-500/30';
};

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    emit('close');
  }
};

onMounted(() => {
  fetchOverview();
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});
</script>