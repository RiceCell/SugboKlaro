<script setup>
import { ref } from 'vue'

const count = ref(0)
const toggleState = ref(false)
</script>

<template>
  <div class="relative flex min-h-screen flex-col items-center justify-center overflow-hidden p-6 text-white">
    <div class="pointer-events-none absolute inset-0 z-0 flex items-center justify-center opacity-10">
      <img
        src="/ph.svg"
        alt="PH Map"
        class="w-[80%] max-w-4xl"
      />
    </div>

    <!-- 3D Cube -->
    <div class="relative z-10 mb-20 size-24 perspective-midrange">
      <div class="relative size-24 transform-3d animate-[cube-rotate_8s_linear_infinite]">
        <!-- Front -->
        <div class="absolute inset-0 flex size-24 items-center justify-center bg-sky-300/75 text-2xl font-bold [transform:translateZ(48px)]">
          Front
        </div>
        <!-- Back -->
        <div class="absolute inset-0 flex size-24 items-center justify-center  bg-sky-300/75 text-2xl font-bold [transform:rotateY(180deg)_translateZ(48px)]">
          Back
        </div>
        <!-- Right -->
        <div class="absolute inset-0 flex size-24 items-center justify-center bg-sky-300/75 text-2xl font-bold [transform:rotateY(90deg)_translateZ(48px)]">
          Right
        </div>
        <!-- Left -->
        <div class="absolute inset-0 flex size-24 items-center justify-center  bg-sky-300/75 text-2xl font-bold [transform:rotateY(-90deg)_translateZ(48px)]">
          Left
        </div>
        <!-- Top -->
        <div class="absolute inset-0 flex size-24 items-center justify-center  bg-sky-300/75 text-2xl font-bold [transform:rotateX(90deg)_translateZ(48px)]">
          Top
        </div>
        <!-- Bottom -->
        <div class="absolute inset-0 flex size-24 items-center justify-center  bg-sky-300/75 text-2xl font-bold [transform:rotateX(-90deg)_translateZ(48px)]">
          Bottom
        </div>
      </div>
    </div>

    <!-- Card -->
    <div class="relative z-20 w-full max-w-sm rounded-2xl border border-slate-700 bg-slate-800 p-8 text-center shadow-xl">
      <h1 class="mb-2 text-3xl font-extrabold text-indigo-400">
        Vue + Tailwind
      </h1>
      <p class="mb-6 text-sm text-slate-400">
        Simple reactive setup running on Vite
      </p>

      <!-- Counter -->
      <button
        @click="count++"
        class="mb-4 w-full cursor-pointer rounded-xl bg-indigo-600 px-4 py-2.5 font-semibold text-white transition duration-200 hover:bg-indigo-500 active:scale-95"
      >
        Count is: {{ count }}
      </button>
      <!-- Toggle -->
      <div class="mt-6 flex items-center justify-between border-t border-slate-700 pt-4">
        <span class="text-sm font-medium text-slate-300">
          Status: {{ toggleState ? 'Active' : 'Inactive' }}
        </span>

        <button
          @click="toggleState = !toggleState"
          :class="toggleState ? 'bg-emerald-500' : 'bg-slate-600'"
          class="flex h-6 w-12 cursor-pointer items-center rounded-full p-1 duration-300"
        >
          <div :class="{ 'translate-x-6': toggleState }" class="h-4 w-4 rounded-full bg-white shadow-md duration-300">
            
          </div>
        </button>
      </div>

    </div>

  </div>
</template>

<style>
@keyframes cube-rotate {
  from {
    transform: rotateX(-20deg) rotateY(0deg);
  }

  to {
    transform: rotateX(-20deg) rotateY(360deg);
  }
}
</style>