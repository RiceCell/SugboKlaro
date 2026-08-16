<script setup lang="ts">
import { useRoute, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue';

const route = useRoute();
</script>

<template>
  <main class="flex flex-col items-center w-full min-h-screen bg-linear-to-br from-dark-blue-gr-start to-dark-blue-gr-end">
    <Navbar v-if="!route.meta.hideNavbar" />
    <RouterView />
  </main>
</template>