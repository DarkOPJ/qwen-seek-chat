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
          <ModelSelector v-model="selectedModel" :disabled="disabled" />
          <button
            class="w-12 h-12 flex items-center justify-center bg-neural-purple text-white rounded-full hover:shadow-[0_0_15px_rgba(168,85,247,0.5)] hover:scale-105 active:scale-95 transition-all duration-200"
            @click="send"
            :disabled="disabled || !inputValue.trim() || isStreaming"
          >
            <span class="material-symbols-outlined">arrow_upward</span>
          </button>
        </div>
      </div>
      <!-- Bottom Metadata Bar -->
      <div class="flex items-center justify-between px-6 pb-2 pt-1 border-t border-white/5 mt-1">
        <div class="flex gap-4">
          <div class="flex items-center gap-1.5">
            <div class="w-1.5 h-1.5 rounded-full bg-accent-emerald animate-pulse"></div>
            <span class="text-[10px] font-bold text-on-tertiary-container uppercase tracking-tight">System Ready</span>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <span class="text-[10px] font-bold text-on-tertiary-container uppercase tracking-widest">Context: 128k Tokens</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import ModelSelector from './ModelSelector.vue'

const props = defineProps({
  model: String,
  disabled: Boolean,
  isStreaming: Boolean
})

const emit = defineEmits(['send', 'regenerate', 'model-change'])

const textareaRef = ref(null)
const inputValue = ref('')
const selectedModel = ref(props.model)

watch(() => props.model, (val) => {
  selectedModel.value = val
})

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

const send = () => {
  if (inputValue.value.trim() && !props.disabled && !props.isStreaming) {
    emit('send', inputValue.value.trim(), selectedModel.value)
    inputValue.value = ''
    nextTick(() => {
      if (textareaRef.value) {
        textareaRef.value.style.height = 'auto'
      }
    })
  }
}
</script>

<style scoped>
/* Scoped styles if needed */
</style>