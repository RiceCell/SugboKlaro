<template>
    <section class="sticky w-full h-20 bg-linear-to-b from-slate-800 to-slate-900 flex items-center px-5 shadow-md gap-12">
        <RouterLink to="/home" class="h-full flex items-center">
            <img :src="logo" class="h-[75%]">
        </RouterLink>

        <RouterLink to="/home" 
            class="text-xl transition-colors hover:text-cyan-500" 
            active-class="bg-linear-to-br from-cyan-gr-start to-cyan-gr-end bg-clip-text text-transparent underline underline-offset-5">
            Home
        </RouterLink>
        
        <RouterLink to="/reports" 
            class="text-xl transition-colors hover:text-cyan-500" 
            active-class="bg-linear-to-br from-cyan-gr-start to-cyan-gr-end bg-clip-text text-transparent underline underline-offset-5">
            Reports
        </RouterLink>

        <RouterLink to="/about" 
            class="text-xl transition-colors hover:text-cyan-500" 
            active-class="bg-linear-to-br from-cyan-gr-start to-cyan-gr-end bg-clip-text text-transparent underline underline-offset-5">
            About the Project
        </RouterLink>
    </section>    
</template>

<script setup lang="ts">
import logo from '../assets/SugboKlaroLogo_dark.png'
</script>
