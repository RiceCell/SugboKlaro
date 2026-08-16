<template>
  <div class="fixed bottom-6 right-6 z-50">

    <!-- chat window-->
    <Transition name="chat">
      <div v-if="isOpen" class=" absolute bottom-0 right-0 w-[370px] h-[500px] max-w-[calc(100vw-2rem)] bg-white rounded-3xl shadow-[0_20px_60px_rgba(0,0,0,0.18)] border-2 border-[#37b5e7] overflow-hidden flex flex-col">

        <!-- HEADER -->
        <div class="bg-[#1F3B5C] px-5 py-3 text-white">
          <div class="flex items-center justify-between">
          <!-- Left side -->
          <div class="flex items-center">
            <div class = "w-9 h-9 rounded-full flex items-center justify-center">
              <img src="/MagnifyingGlass_white.png" class="w-5 h-5 object-contain"/>
             </div>

              <!-- Sugbo Klaro Logo -->
              <div class="flex items-center">
                <img  src="/SugboKlaroLogo_dark.png" class="h-6 w-auto max-w-[150px] object-contain" />
              </div>
          </div>


          <!-- Close button -->
          <button @click ="isOpen = false" class = "w-8 h-8 rounded-full flex items-center  justify-center text-white hover:text-[#0DD1D4]  transition">
            <X  class = "h-5 w-5 "/>
          </button>

          </div>

        </div>


        <!-- ================= CHAT AREA ================= -->
        <div ref="chatBox" class = "flex-1 overflow-y-auto bg-[#f8fafc] px-4 py-5 space-y-5">
          <!-- Date -->
          <div class="flex items-center gap-2">
            <div class="h-px bg-slate-200 flex-1"></div>
            <span class="text-[10px] tracking-wider text-slate-400 font-medium ">
              TODAY
            </span>
            <div class="h-px bg-slate-200 flex-1"></div>
          </div>

          <!-- Messages -->
          <div v-for="(msg, index) in messages"
              :key="index"
              :class="[ 'flex gap-2.5', msg.role === 'user' ? 'justify-end' : 'justify-start']">

            <!-- Bot Avatar -->
            <div v-if="msg.role === 'bot'" class=" w-7 h-7 shrink-0 rounded-full bg-[#2B5582] flex items-center justify-center">
              <img src="/MagnifyingGlass_white.png" class="w-5 h-5 object-contain"/>
            </div>
            <!-- Message Content -->
            <div :class="[ 'max-w-[78%]',msg.role === 'user'
                  ? 'items-end'
                  : 'items-start'
              ]"
            >

              <!-- Message Bubble -->
              <div :class="[ 'px-4 py-2 text-sm leading-relaxed shadow-sm',msg.role === 'user' ? `bg-[#237899] text-white rounded-2xl rounded-br-md` : `bg-white text-slate-700 border border-slate-200 rounded-2xl rounded-bl-md`]">
                {{ msg.content }}
              </div>

              <!-- Sender
              <p :class="['text-[9px] text-slate-400 mt-1', msg.role === 'user'? 'text-right': 'text-left']">
                {{ msg.role === 'user' ? 'You' : 'omai' }}
              </p>
            -->
            </div>
          </div>


          <!-- Typing Indicator -->
          <div v-if="isTyping" class="flex items-start gap-2.5">
            <div class="w-7 h-7 rounded-full bg-emerald-500flex items-center justify-center text-white text-[10px] font-bold">
              <img src="/MagnifyingGlass_white.png" class="w-5 h-5 object-contain"/>
            </div>

            <div class=" bg-white border border-slate-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
              <div class="flex gap-1">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </div>
            </div>
          </div>
        </div>

        <!-- inpur -->
        <div class="bg-white border-t border-slate-200 px-4 py-3">
          <form @submit.prevent="sendMessage" class=" flex items-center gap-2 bg-slate-100 rounded-2xl p-1.5 focus-within:ring-2 focus-within:ring-[#37b5e7] transition">
            <input  v-model="newMessage" type="text" placeholder="Type a message..." :disabled="isTyping" class="flex-1 bg-transaprent border-none outline-none text-sm text-slate-700 placeholder:text-slate-400 px-3 py-2" />
            <!-- Send -->
            <button type="submit"
              :disabled="!newMessage.trim() || isTyping"
              class=" w-9 h-9 shrink rounded-xl bg-[#37b5e7] text-white flex items-center justify-center hover:bg-[#237899] hover:scale-105 active:scale-95 disabled:opacity-40 disabled:hover:scale-100 transition-all">
              <Send />

            </button>

          </form>
          <!--
          <p class="text-[9px] text-center text-slate-400 mt-2">
            Powered by SugboKlaro
          </p>
-->
        </div>

      </div>
    </Transition>


  
    <Transition name="button">
      <button v-if="!isOpen"@click="isOpen = true"
        class=" fixed bottom-6 right-6 w-12 h-12 rounded-full bg-[#37b5e7] text-white shadow-[0_8px_30px_rgba(16,185,129,0.35)] flex items-center justify-center hover:bg-[#237899] hover:scale-105 active:scale-95 transition-all">
        <MessageCircleMore />
      </button>

    </Transition>

  </div>
</template>


<script setup>
import { ref, nextTick } from 'vue'
import { X, Send, MessageCircleMore} from '@lucide/vue';

const isOpen = ref(false)
const newMessage = ref('')
const isTyping = ref(false)
const chatBox = ref(null)

const messages = ref([
  {
    role: 'bot', content: "Hi! 👋 I'm omai. How can I help you today?"
  }
])


const scrollToBottom = async () => {
  await nextTick()

  if (chatBox.value) {
    chatBox.value.scrollTop = chatBox.value.scrollHeight
  }
}


const sendMessage = async () => {
  const text = newMessage.value.trim()

  if (!text) return

  messages.value.push({ role: 'user',content: text})
  newMessage.value = ''

  isTyping.value = true

  await scrollToBottom()



  setTimeout(() => {
    isTyping.value = false
  })
}


const sendQuickMessage = (message) => {
  newMessage.value = message
  sendMessage()
}
</script>


<style scoped>

.chat-enter-active,
.chat-leave-active {
  transition:
    opacity 0.25s ease,
    transform 0.25s ease;

  transform-origin: bottom right;
}

.chat-enter-from,
.chat-leave-to {
  opacity: 0;
  transform: translateY(15px) scale(0.95);
}

.button-enter-active,
.button-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.button-enter-from,
.button-leave-to {
  opacity: 0;
  transform: scale(0.5);
}


.dot {
  width: 6px;
  height: 6px;
  background: #94a3b8;
  border-radius: 50%;

  animation:
    typing 1.4s infinite ease-in-out;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}


@keyframes typing {

  0%,
  60%,
  100% {
    transform: translateY(0);
    opacity: 0.5;
  }

  30% {
    transform: translateY(-4px);
    opacity: 1;
  }

}


::-webkit-scrollbar {
  width: 5px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}


/*mobile

@media (max-width: 500px) {

  .fixed.bottom-6.right-6 {
    right: 1rem;
    bottom: 1rem;
  }

}

*/

</style>