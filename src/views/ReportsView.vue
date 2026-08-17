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
                            <th class="w-12/100 px-4 py-2 font-semibold">Year</th>
                            <th class="w-8/100 px-2 py-2 font-semibold">Quarter</th>
                            <th class="w-10/100 px-4 py-2 font-semibold"></th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-slate-700">
                        <tr v-for="(r, i) in rL.reports" :key="i" @click="handleRowClick(r, rL.title)" class="hover:bg-slate-700/40 transition-colors cursor-pointer">
                            <td class="px-4 py-2 wrap-break-word font-light">{{ r.name }}</td>
                            <td class="px-4 py-2 wrap-break-word font-light">{{ r.LGU }}</td>
                            <td class="px-4 py-2 wrap-break-word font-light">{{ r.posting_year }}</td>
                            <td class="px-4 py-2 wrap-break-word font-light">{{ r.posting_quarter }}</td>
                            
                            <td v-if="r.download_link" class="px-4 py-2">
                                <div class="flex items-center gap-2">
                                    <!-- Eye Button (View in Browser via Office Web Viewer) -->
                                    <a :href="`https://view.officeapps.live.com/op/view.aspx?src=${encodeURIComponent(r.download_link)}`" 
                                        target="_blank" 
                                        rel="noopener noreferrer" 
                                        @click.stop
                                        class="inline-flex items-center justify-center min-w-8 w-8 h-8 bg-white rounded-lg text-slate-700 hover:bg-slate-200 transition-colors shadow-sm"
                                        title="View in Browser">
                                        <Eye class="size-4.5" />
                                    </a>
                                    
                                    <!-- Download Button -->
                                    <a :href="r.download_link" @click.stop
                                        class="inline-flex items-center justify-center min-w-8 w-8 h-8 bg-white rounded-lg text-slate-700 hover:bg-slate-200 transition-colors shadow-sm"
                                        title="Download File">
                                        <Download class="size-4.5" />
                                    </a>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">
// NEW: Imported the 'Eye' icon from lucide
import { Download, Eye } from '@lucide/vue';
import { ref } from 'vue';
import Filter from '../components/Filter.vue';
import { useRouter } from 'vue-router';

interface reportDetails {
    id: string;
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

const reportsList = ref<reportGroup[]>([
{
    title: 'Budget Reports',
    reports: [{
        id: 'abr_2026_q1',
        name: 'Annual Budget Report (ABR)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'N/A'
    }, {
        id: 'sipb_2026_q1',
        name: 'Statement of Debt Service (SIPB)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=241805'
    }, {
        id: 'sre_2026_q1',
        name: 'Statement of Receipts and Expenditures (SRE)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=241810'
    }, {
        id: 'qscf_2026_q1',
        name: 'Quarterly Statement of Cash Flow (QSCF)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=241671'
    }, {
        id: 'mancom_2026_q1',
        name: 'Manpower Complement (MANCOM)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=241667'
    }
    ]
},
{
    title: 'Procurement Reports',
    reports: [{
        id: 'app_2026_q1',
        name: 'Annual Procurement Plan or Procurement List (APP)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'N/A'
    }, {
        id: 'brcwgs_2026_q1',
        name: 'Bid Results on Civil Works, Goods and Services, and Consulting Services (BRCWGS)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=247698'
    }, {
        id: 'spp_2026_q1',
        name: 'Supplemental Procurement Plan (SPP)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'N/A'
    }
    ]
},
{
    title: 'Special Purpose Fund Reports',
    reports: [{
        id: 'uca_2026_q1',
        name: 'Unliquidated Cash Advances (UCA)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=241805'
    }, {
        id: 'sef_2026_q1',
        name: 'Report of SEF Utilization (SEF)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=241672'
    }, {
        id: 'agdar_2026_q1',
        name: 'Annual GAD Accomplishment Report (AGDAR)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'N/A'
    }, {
        id: 'tfu_2026_q1',
        name: 'Trust Fund (PDAF) Utilization (TFU)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=241673'
    }, {
        id: 'ntau_2026_q1',
        name: '20% of the National Tax Allotment Utilization (NTAU)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=241823'
    }, {
        id: 'ldrrmf_2026_q1',
        name: 'Report of Local Disaster Risk Reduction and Management Fund (LDRRMF) Utilization (LDRRMF)',
        LGU: 'REGION VII - CENTRAL VISAYAS, CITY OF CEBU (CAPITAL), CITY OF CEBU (Capital)',
        posting_year: '2026',
        posting_quarter: 1,
        download_link: 'https://fdpp.dilg.gov.ph/fdpp/report/document-download?id=241670'
    }
    ]
},
])

const router = useRouter();

// Update: Pass the categoryTitle to pass into URL parameters
const handleRowClick = (item: reportDetails, categoryTitle: string) => {
    router.push({
        path: `${router.currentRoute.value.path}/${item.id}`,
        query: { category: categoryTitle, name: item.name }
    });
}   

</script>