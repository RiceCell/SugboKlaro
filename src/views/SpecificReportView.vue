<template>
  <div class="w-full overflow-hidden p-6">
    <div
        v-if="selectedReport" 
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs font-sans"
        @click.self="closeReport"
    >
        <ReportDetails 
            :data="selectedReport"
        />
    </div>

    <!-- Breadcrumbs Navigation -->
    <nav class="mb-6 flex items-center gap-2 text-sm text-slate-300 font-medium">
        <span 
            @click="router.push('/reports')" 
            class="cursor-pointer hover:text-white transition-colors uppercase"
        >
            {{ reportCategory }}
        </span>
        <span>&gt;</span>
        <span class="text-white">
            {{ reportName }} - {{ id }}
        </span>
    </nav>

    <div v-if="loading">Loading report data...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else-if="reportData" class="w-full p-5">
        
        <section class="grid grid-cols-4 gap-8 px-5">
            <button @click="openReport(r)" 
                v-for="(r, index) in reportData.results" :key="index"
                class="p-2 pt-6 flex flex-col items-center gap-3 rounded-2xl transition-colors group hover:bg-slate-800 cursor-pointer">
                <img :src="folderColor(r.status)" class="w-1/2 transition-all group-hover:scale-110 group-hover:-rotate-2" />

                <h1 v-if="idType && idType[0] === 'brcwgs'" class="text-center">
                    {{ r.rule_id }} | {{ r.details.project_name || 'N/A' }}
                </h1>
                <h1 v-if="idType && idType[0] === 'qscf'" class="text-center">
                    {{ r.rule_id }} | {{ r.details.fund_type || 'N/A' }}
                </h1>
                <h1 v-if="idType && idType[0] === 'uca'" class="text-center">
                    {{ r.rule_id }} | {{ r.details.date_granted || 'N/A' }} {{ r.row_ref }}
                </h1>
            </button>
        </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import ReportDetails from '../components/ReportDetails.vue'

const route = useRoute()
const router = useRouter()

import FolderGray from '../assets/Folder_gray.png'
import FolderCyan from '../assets/Folder_cyan.png'
import FolderRed from '../assets/Folder_red.png'

const folderColor = (status: string) => {
    if (status === 'pass') { return FolderCyan }
    else if (status === 'flagged') { return FolderRed }
    else { return FolderGray }
}

const props = defineProps<{
  id: string
}>()

// Computed properties mapping to query parameters
const reportCategory = computed(() => route.query.category ? String(route.query.category) : 'Reports');
const reportName = computed(() => route.query.name ? String(route.query.name) : 'Report Details');

const reportData = ref<any>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const loadReport = async (reportId: string) => {
  loading.value = true
  error.value = null
  
  try {
    // Dynamically import the JSON file based on the ID.
    // Vite will automatically bundle files in this directory.
    const data = await import(`../../data/compliance_results/${reportId}.json`)
    
    // JSON imports in Vite expose the data on the .default property
    reportData.value = data.default
  } catch (err: any) {
    error.value = `Failed to load report ${reportId}. Make sure the file exists in data/compliance_results/.`
  } finally {
    loading.value = false
  }
}

const idType = props.id.match(/^[^_]+/);

onMounted(() => {
  loadReport(props.id)
})

watch(() => props.id, (newId) => {
  loadReport(newId)
})

const openReport = (r: any) => {
  router.push({ query: { ...route.query, item: JSON.stringify(r) } })
}

const closeReport = () => {
  const query = { ...route.query }
  delete query.item
  router.push({ query })
}

const selectedReport = computed(() => {
  const itemQuery = route.query.item
  if (!itemQuery) return null

  try {
    // Vue Router can sometimes return an array if a query param appears multiple times.
    // This ensures we always pass a string to JSON.parse()
    const jsonString = Array.isArray(itemQuery) ? itemQuery[0] : itemQuery
    
    // Return the parsed JSON directly to the modal
    return JSON.parse(jsonString as string)
  } catch (e) {
    console.error("Failed to parse report from query string:", e)
    return null
  }
})
</script>