<template>
    <main class="p-8 text-slate-100 flex flex-col gap-10">
        <Filter />
        <div v-for="(rL, index) in reportsList" :key="index">
            <!-- Styled the title -->
            <h1 class="text-2xl font-bold mb-2 text-white uppercase">{{ rL.title }}</h1>
            
            <div class="overflow-hidden border border-slate-700 shadow-md bg-slate-800/50">
                <table class="w-full table-fixed text-left border-collapse">
                    <thead class="bg-slate-700 text-slate-200">
                        <tr>
                            <th class="w-35/100 px-4 py-2 font-semibold">Name</th>
                            <th class="w-35/100 px-4 py-2 font-semibold">LGU</th>
                            <th class="w-13/100 px-4 py-2 font-semibold">Year</th>
                            <th class="w-12/100 px-4 py-2 font-semibold">Quarter</th>
                            <th class="w-5/100 px-4 py-2 font-semibold"></th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-slate-700">
                        <tr v-for="(r, i) in rL.reports" :key="i" class="hover:bg-slate-700/40 transition-colors">
                            <td class="px-4 py-2 wrap-break-word font-light">{{ r.name }}</td>
                            <td class="px-4 py-2 wrap-break-word font-light">{{ r.LGU }}</td>
                            <td class="px-4 py-2 wrap-break-word font-light">{{ r.posting_year }}</td>
                            <td class="px-4 py-2 wrap-break-word font-light">{{ r.posting_quarter }}</td>
                            
                            <td v-if="r.download_link" class="px-4 py-2">
                                <a :href="r.download_link" 
                                    class="inline-flex items-center justify-center w-8 h-8 bg-white rounded-lg text-slate-700 hover:bg-slate-200 transition-colors shadow-sm">
                                    <Download class="size-4.5" />
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">
import { Download } from '@lucide/vue';
import { ref } from 'vue';
import Filter from '../components/Filter.vue';

interface reportDetails {
    name: string;
    LGU: string;
    posting_year: string;
    posting_quarter: number;
    download_link?: string;
}

interface reportGroup {
    title: string;
    reports: reportDetails[];
};

const reportsList = ref<reportGroup[]>([{
    title: 'Budget Reports',
    reports: [{
        name: 'Quarterly Statement of Cash Flow (QSCF)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CEBU, ALCANTARA',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=241671'
    }
    ]
},
{
    title: 'Procurement Reports',
    reports: [{
        name: 'Bid Results on Civil Works, Goods and Services, and Consulting Services (BRCWGS)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CEBU, ALCANTARA',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=247698'
    }
    ]
},
{
    title: 'Special Purpose Fund Reports',
    reports: [{
        name: 'Unliquidated Cash Advances (UCA)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CEBU, ALCANTARA',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=241816'
    }
    ]
},
])
</script>