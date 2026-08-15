<template>
  <!-- Main -->
  <div class="mx-auto flex flex-col w-full max-w-md h-[600px] bg-yellow border border-slate-200 rounded-xl shadow-lg overflow-hidden font-sans-seriff">
    
    <!-- Header -->
    <div class="bg-[#0e101d] px-4 py-3 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <h2 class="text-white text-sm font-semibold tracking-wide">omai</h2>
      </div>
    </div>

    <div ref="chatBox" class="flex-1 p-4 overflow-y-auto bg-slate-50 space-y-4">
      <div 
        v-for="(msg, index) in messages" 
        :key="index"
        :class="['flex w-full', msg.role === 'user' ? 'justify-end' : 'justify-start']"
      >
        <div 
          :class="[
            'max-w-[80%] px-4 py-2 text-sm rounded-2xl',
            msg.role === 'user' 
              ? 'bg-emerald-600 text-white rounded-br-none' 
              : 'bg-white border border-slate-200 text-slate-700 shadow-sm rounded-bl-none'
          ]"
        >
          {{ msg.content }}
        </div>
      </div>
    </div>

    <div class="p-3 bg-white border-t border-slate-200">
      <form @submit.prevent="sendMessage" class="flex items-center gap-2">
        <input 
          v-model="newMessage"
          type="text" 
          placeholder="Tanongin mo aq, baby" 
          class="flex-1 bg-slate-100 text-slate-700 text-sm rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all"
          :disabled="isTyping"
        />
        <button 
          type="submit" 
          :disabled="!newMessage.trim() || isTyping"
          class="bg-emerald-600 text-white p-2 rounded-full hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transform rotate-45 mb-0.5 ml-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </form>
    </div>

  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const newMessage = ref('')
const isTyping = ref(false)
const chatBox = ref(null)

const messages = ref([
  { role: 'bot', content: 'blabla' }
])



const sendMessage = () => {
  const text = newMessage.value.trim()
  if (!text) return

  messages.value.push({ role: 'user', content: text })
  newMessage.value = ''



  setTimeout(() => {
    isTyping.value = false
  })
}
</script>