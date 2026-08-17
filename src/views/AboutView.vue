<template>
    <main class="w-full overflow-y-auto px-8">
        <!-- About the Project -->
        <section class="mt-8 flex flex-col justify-start">
          <h1 class="text-4xl font-extrabold text-white tracking-wide drop-shadow-lg">
            <span class="flex items-center gap-4">
                About
                <img :src="Logo" class="w-40" />
            </span>
          </h1>
          <p class="text-sky-200 mt-3 text-sm max-w-lg leading-relaxed">
            SugboKlaro is a citizen-centered transparency and compliance checker that analyzes publicly disclosed LGU spending against applicable laws and regulations. This makes government data easier for ordinary citizens to understand and question.
          </p>
        </section>

        <!-- FDPP -->
        <section class="mt-20 flex justify-between items-center">
            <img :src="FDPP" class="w-2/5" />
            <div>
                <h1 class="text-4xl font-extrabold text-white tracking-wide drop-shadow-lg">
                    Where is the data from?
                </h1>
                <p class="text-sky-200 mt-3 text-sm max-w-lg text-right leading-relaxed">
                    All data is consolidated from the Full Disclure Property Portal 
                    <a href ="https://fdpp.dilg.gov.ph" target ="_blank" class="text-cyan-gr-start underline font-bold">(FDPP)</a> 
                    established by the Department of the Interior and Local Government 
                    <a href ="https://www.dilg.gov.ph" target ="_blank" class="text-cyan-gr-start underline font-bold">(DILG)</a>.
                </p>  
            </div>
          
        </section>

        <!-- About Us -->
        <section class="mt-20 flex justify-between">
            <div>
                <h1 class="text-4xl font-extrabold text-white tracking-wide drop-shadow-lg">
                  M & 'Ems
                </h1>
                <p class="text-sky-200 mt-3 text-sm max-w-lg leading-relaxed">
                  Hailing from the University of the Philippines Cebu, we are the developers of M & 'Ems.
                    <br><br>
                    <strong>Developers: </strong><br>
                    ➣ BUNO, RUSSEL NIÑO B.<br>
                    ➣ CASTAÑOS, LORIZ MARIE I.<br>
                    ➣ MANLANGIT, ANGELO MARI H.<br>
                    ➣ SANTILLAN, CARL BENEDICT T.<br>
                    ➣ RETUTAL, RYAN ANTHONY B.<br>

                    <br>
                    <strong>Mentored by:</strong> SANTIAGO, MARION KRISTOFFER
                </p>
            </div>
            <img :src="Us" class="w-2/5" />
        </section>
    </main>
</template>

<script setup lang="ts">
import Logo from '../assets/SugboKlaroLogo_dark.png'
import Us from '/us.jpg'
import FDPP from '/FDPP.png'
</script>