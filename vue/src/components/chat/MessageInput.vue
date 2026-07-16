<template>
  <div class="absolute bottom-0 left-0 right-0 p-8 pt-0 pointer-events-none">
    <div class="max-w-4xl mx-auto glass p-2 rounded-[28px] shadow-2xl inner-glow pointer-events-auto border border-white/10 relative overflow-hidden">
      <div class="flex items-end gap-2 p-2">
        <div class="flex-1 flex flex-col min-h-[48px] justify-center px-2">
          <textarea
            ref="textareaRef"
            v-model="inputValue"
            class="w-full bg-transparent border-none focus:ring-0 resize-none text-sm leading-6 py-2 text-white placeholder-on-tertiary-container scrollbar-hide"
            placeholder="Type your instruction..."
            rows="1"
            @input="handleInput"
            @keydown="handleKeydown"
            :disabled="disabled"
          ></textarea>
        </div>
        <div class="flex items-center gap-1">
          <button
            v-if="isStreaming"
            class="w-12 h-12 flex items-center justify-center bg-red-600 text-white rounded-full hover:bg-red-500 active:scale-95 transition-all duration-200 shadow-lg"
            @click="handleStop"
            title="Stop generating"
          >
            <span class="material-symbols-outlined text-lg">stop</span>
          </button>
          <button
            v-else
            class="w-12 h-12 flex items-center justify-center bg-neural-purple text-white rounded-full hover:shadow-[0_0_15px_rgba(168,85,247,0.5)] hover:scale-105 active:scale-95 transition-all duration-200"
            @click="send"
            :disabled="!inputValue.trim()"
          >
            <span class="material-symbols-outlined">arrow_upward</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const props = defineProps({
  model: String,
  disabled: Boolean,
  isStreaming: Boolean
})

const emit = defineEmits(['send', 'stop'])

const textareaRef = ref(null)
const inputValue = ref('')

const handleInput = (e) => {
  inputValue.value = e.target.value
  nextTick(() => {
    e.target.style.height = 'auto'
    e.target.style.height = e.target.scrollHeight + 'px'
  })
}

const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}

const handleStop = () => {
  emit('stop')
}

const send = () => {
  if (inputValue.value.trim() && !props.disabled) {
    emit('send', inputValue.value.trim(), props.model)
    inputValue.value = ''
    nextTick(() => {
      if (textareaRef.value) {
        textareaRef.value.style.height = 'auto'
      }
    })
  }
}
</script>
