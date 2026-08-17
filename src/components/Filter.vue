<template>
    <div class="fixed top-6 right-6 z-50" >
        <Transition name="filter">
            <div class="absolute top-14 right-0 w-[370px] rounded-xl border border-gray-200 bg-white shadow-lg"
                v-if="showFilter">
                <!-- Header -->
                <div class="flex items-center justify-between rounded-t-xl border-b border-gray-100 bg-white px-4 py-3">
                    <div>
                        <h2 class="text-sm font-semibold text-gray-800">
                            Filters
                        </h2>
                    </div>

                    <button @click="showFilter = false" class="flex h-7 w-7 items-center justify-center rounded-md text-lg text-gray-400 transition hover:bg-gray-100 hover:text-gray-700">
                        <X />
                    </button>
                </div>

                <!-- Filters -->
                <div class="custom-scrollbar space-y-3 p-4 max-h-[60vh] overflow-y-auto">
                    <div v-for="filter in filters"
                        :key="filter"
                    >
                        <label class="mb-1.5 block text-xs font-medium text-gray-600">
                            {{ filter }}
                        </label>

                        <div class="relative">
                            <button
                                @click="toggleDropdown(filter)"
                                type="button"
                                class="flex w-full items-center justify-between rounded-lg border border-gray-200 bg-gray-50 px-3 py-2.5 text-xs text-gray-700 focus:border-blue-500 focus:outline-none"
                            >
                                {{ selectedFilters[filter] || `Select ${filter}` }}

                                <span
                                    class="transition-transform duration-200"
                                    :class="{
                                        'rotate-180': openDropdown === filter
                                    }"
                                >
                                    <ChevronDown />
                                </span>
                            </button>

                            <!-- Options -->
                            <div v-if="openDropdown === filter"
                                class="filter-options absolute max-h-50 left-0 top-full z-20 mt-1 w-full overflow-y-auto overflow-x-hidden rounded-lg border border-gray-200 bg-white shadow-lg"
                            >
                                <button
                                    v-for="option in getOptions(filter)"
                                    :key="option"
                                    @click="selectFilter(filter, option)"
                                    type="button"
                                    class="block w-full px-3 py-2.5 text-left text-xs text-gray-700 hover:bg-gray-100"
                                    :class="{
                                        'bg-blue-50 font-medium text-blue-600':
                                            selectedFilters[filter] === option
                                    }"
                                >
                                    {{ option }}
                                </button>
                            </div>
                        </div>
                    </div>

                </div>

                <!-- Footer -->
                <div class="flex justify-end gap-2 rounded-b-xl border-t border-gray-100 bg-white px-4 py-3">
                    <button
                        @click="clearFilters"
                        type="button"
                        class="rounded-lg px-3 py-2 text-xs font-medium text-gray-500 hover:bg-gray-100"
                    >
                        Clear
                    </button>

                    <button
                        @click="applyFilters"
                        type="button"
                        class="rounded-lg bg-blue-600 px-4 py-2 text-xs font-medium text-white hover:bg-blue-700"
                    >
                        Apply Filters
                    </button>
                </div>

            </div>
        </Transition>

       
        <button
            @click="showFilter = !showFilter"
            class="flex h-10 items-center gap-2 rounded-full bg-blue-600 px-4 text-sm font-medium text-white shadow-md transition-colors hover:bg-blue-700"
        >
            <span>
                <FunnelPlus />
            </span>
            Filter
        </button>

    </div>
</template>


<script setup lang="ts">
import { ref, reactive } from 'vue'
import { X , ChevronDown, FunnelPlus} from '@lucide/vue'

const showFilter = ref(false)

const openDropdown = ref<string | null>(null)


const emit = defineEmits(['apply'])

const applyFilters = () => {
    // Emit a copy of the selected filters
    emit('apply', { ...selectedFilters }) 
    // Close the dropdown
    showFilter.value = false 
}
const filters = [
    'Report',
    'Document',
    'Region',
    'Province',
    'Municipality/City',
    'Year'
]

const selectedFilters = reactive<Record<string, string>>({})

const filterOptions: Record<string, string[]> = {
    Report: [
        'Budget Reports',
        'Procurement Reports',
        'Special Purpose Fund Reports'
    ],

    Document: [
        'Annual Budget Report (ABR)',
        'Statement of Debt Service (SIPB)',
        'Statement of Receipts and Expenditures (SRE)',
        'Quarterly Statement of Cash Flow (QSCF)',
        'Manpower Complement (MANCOM)',
        'Annual Procurement Plan or Procurement List (APP)',
        'Bid Results on Civil Works, Goods and Services, and Consulting Services (BRCWGS)',
        'Supplemental Procurement Plan (SPP)',
        'Unliquidated Cash Advances (UCA)',
        'Report of SEF Utilization (SEF)',
        'Annual GAD Accomplishment Report (AGDAR)',
        'Trust Fund (PDAF) Utilization (TFU)',
        '20% of the National Tax Allotment Utilization (NTAU)',
        'Report of Local Disaster Risk Reduction and Management Fund (LDRRMF) Utilization (LDRRMF)'

    ],

    Region: [
        'Region VII - Central Visayas'
    ],

    Province: [
        'Cebu',
        'Bohol',
        'Negros Oriental'
    ],

    'Municipality/City': [
        'Cebu City',
        'Mandaue City',
        'Lapu-Lapu City'
    ],

    Year: [
        '2024',
        '2025',
        '2026'
    ]
}

const getOptions = (filter: string) => {
    return filterOptions[filter] || []
}

const toggleDropdown = (filter: string) => {
    if (openDropdown.value === filter) {
        openDropdown.value = null
    } else {
        openDropdown.value = filter
    }
}

const selectFilter = (filter: string, option: string) => {
    selectedFilters[filter] = option
    openDropdown.value = null
}

const clearFilters = () => {
    Object.keys(selectedFilters).forEach((key) => {
        delete selectedFilters[key]
    })

    openDropdown.value = null
}
</script>


<style>
.filter-enter-active,
.filter-leave-active {
    transition: all 0.2s ease;
}

.filter-enter-from,
.filter-leave-to {
    opacity: 0;
    transform: translateY(10px) scale(0.98);
    
}

.filter-options::-webkit-scrollbar {
    width: 5px;
}

.filter-options::-webkit-scrollbar-track {
    background: transparent;
}

.filter-options::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 10px;
}
</style>