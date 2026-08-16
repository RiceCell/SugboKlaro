<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue';
</script>

<template>
  <main class="flex flex-col items-center w-full min-h-screen bg-linear-to-b from-dark-blue-gr-start to-dark-blue-gr-end">
    <Navbar />
    <RouterView />
  </main>
</template>