<template>
  <main class="relative flex flex-col items-center justify-center w-full min-h-screen bg-linear-to-b from-dark-blue-gr-start to-dark-blue-gr-end overflow-hidden font-sans">
    
    <!-- Header Content -->
    <div class="mt-16 text-center z-20 px-4">
      <h1 class="text-4xl font-extrabold text-white tracking-wide drop-shadow-lg">
        Transparency Reports Overview
      </h1>
      <p class="text-sky-200 mt-3 text-sm max-w-lg mx-auto leading-relaxed">
        Automated, rule-based compliance checks for Full Disclosure Policy reports such as
        procurements, cash flow, and special funds submitted by local governments. 
        Click "Check" for the full breakdown and legal citation behind each result.
      </p>
    </div>

    <!-- Carousel Container -->
    <div 
      class="relative w-full max-w-6xl h-[600px] -mt-15 flex items-center justify-center perspective-1000"
      @mouseenter="stopAutoPlay"
      @mouseleave="startAutoPlay"
    >
      
      <!-- Left Navigation Arrow -->
      <button 
        @click="prev" 
        class="absolute left-4 md:left-12 z-50 p-3 rounded-full bg-white/10 hover:bg-white/20 text-white backdrop-blur-sm transition-all duration-200 cursor-pointer shadow-lg hover:scale-110 active:scale-95"
        aria-label="Previous Report"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      <!-- Right Navigation Arrow -->
      <button 
        @click="next" 
        class="absolute right-4 md:right-12 z-50 p-3 rounded-full bg-white/10 hover:bg-white/20 text-white backdrop-blur-sm transition-all duration-200 cursor-pointer shadow-lg hover:scale-110 active:scale-95"
        aria-label="Next Report"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
        </svg>
      </button>

      <!-- Rotating Cards -->
      <div 
        v-for="(card, index) in sampleCards" 
        :key="index"
        class="absolute left-0 right-0 mx-auto top-1/2 -translate-y-1/2 w-[420px] h-[380px] transition-all duration-500 ease-out cursor-pointer"
        :class="getCardClass(index)"
        @click="goToCard(index)"
      >
        <!-- FIX: Added explicitly locked h-[460px] to the wrapper above -->
        <!-- FIX: Added !overflow-y-auto to allow taller UCA cards to scroll internally without breaking the carousel sizing -->
        <ReportDetails 
          :data="card" 
          class="!relative w-full h-full !overflow-y-auto overflow-x-hidden !border-slate-400/30 !shadow-none" 
        />
      </div>

    </div>

  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import ReportDetails from '../components/ReportDetails.vue';

// Import the datasets 
import brcwgsData from '../../data/compliance_results/brcwgs.json';
import qscfData from '../../data/compliance_results/qscf.json';
import ucaData from '../../data/compliance_results/uca.json';

// Extract 6 sample items (2 from each JSON) and inject the root doc_type[cite: 13]
const sampleCards = [
  ...brcwgsData.results.slice(0, 2).map((r: any) => ({ ...r, doc_type: brcwgsData.doc_type })),
  ...qscfData.results.slice(0, 2).map((r: any) => ({ ...r, doc_type: qscfData.doc_type })),
  ...ucaData.results.slice(0, 2).map((r: any) => ({ ...r, doc_type: ucaData.doc_type }))
];

// Carousel State
const currentIndex = ref(0);
let autoPlayInterval: ReturnType<typeof setInterval> | null = null;

// Navigation Methods
const next = () => {
  currentIndex.value = (currentIndex.value + 1) % sampleCards.length;
};

const prev = () => {
  currentIndex.value = (currentIndex.value - 1 + sampleCards.length) % sampleCards.length;
};

const goToCard = (index: number) => {
  currentIndex.value = index;
};

// Auto-play Handlers
const startAutoPlay = () => {
  if (autoPlayInterval) return;
  autoPlayInterval = setInterval(next, 3000);
};

const stopAutoPlay = () => {
  if (autoPlayInterval) {
    clearInterval(autoPlayInterval);
    autoPlayInterval = null;
  }
};

// Returns strict string classes for 3D transforms to prevent overlapping state bugs
const getCardClass = (index: number) => {
  const diff = (index - currentIndex.value + sampleCards.length) % sampleCards.length;
  
  switch (diff) {
    // Center Card (Active)
    case 0: 
      return 'shadow-[0_0_20px_rgba(6,182,212,0.8)] rounded-lg border-2 border-[#00D8FF] translate-x-0 scale-105 z-50 opacity-100 hover:scale-105 shadow-2xl';
    
    // Right Side 1
    case 1: 
      return 'translate-x-[70%] scale-90 z-40 opacity-80 hover:opacity-100 shadow-xl';
    
    // Right Side 2
    case 2: 
      return 'translate-x-[130%] scale-75 z-30 opacity-40 hover:opacity-80 shadow-lg';
    
    // Hidden (Back of the carousel)
    case 3: 
      return 'translate-x-0 scale-50 z-10 opacity-0 pointer-events-none';
    
    // Left Side 2
    case 4: 
      return '-translate-x-[130%] scale-75 z-30 opacity-40 hover:opacity-80 shadow-lg';
    
    // Left Side 1
    case 5: 
      return '-translate-x-[70%] scale-90 z-40 opacity-80 hover:opacity-100 shadow-xl';
    
    default: 
      return '';
  }
};

// Lifecycle hooks
onMounted(() => {
  startAutoPlay();
});

onUnmounted(() => {
  stopAutoPlay();
});
</script>

<style scoped>
/* Optional: Customizes the scrollbar slightly so it looks neat when UCA cards scroll */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
}
</style>