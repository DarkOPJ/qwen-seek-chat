<template>
  <div class="flex gap-3" :class="message.role === 'user' ? 'flex-row-reverse' : 'flex-row'">
    <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm"
      :class="message.role === 'user' ? 'bg-purple-500/30' : 'bg-indigo-500/30'">
      <span class="material-symbols-outlined text-sm">{{ message.role === 'user' ? 'person' : 'smart_toy' }}</span>
    </div>
    <div class="flex-1 min-w-0 max-w-[85%]">
      <div class="flex items-center gap-2 mb-1">
        <span class="text-xs font-medium" :class="message.role === 'user' ? 'text-purple-400' : 'text-emerald-400'">
          {{ message.role === 'user' ? 'You' : 'Assistant' }}
        </span>
        <span v-if="message.model_name" class="text-[10px] text-zinc-500 px-1.5 py-0.5 rounded bg-white/5">
          {{ formatModelName(message.model_name) }}
        </span>
        <span class="text-[10px] text-zinc-500">{{ formatTime(message.created_at) }}</span>
      </div>
      <StreamingMessage
        :content="message.content"
        :thinking="message.thinking"
        :is-streaming="isStreaming"
      />
      <div v-if="message.role === 'assistant' && !isStreaming" class="flex items-center gap-2 mt-2 pt-2 border-t border-white/5">
        <button class="flex items-center gap-1 px-2 py-1 text-xs text-zinc-500 hover:text-white" @click="$emit('regenerate', message.id)">
          <span class="material-symbols-outlined text-sm">refresh</span> Regenerate
        </button>
        <button class="flex items-center gap-1 px-2 py-1 text-xs text-zinc-500 hover:text-white" @click="copyMessage">
          <span class="material-symbols-outlined text-sm">content_copy</span> Copy
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import StreamingMessage from './StreamingMessage.vue'

const props = defineProps({
  message: { type: Object, required: true },
  isStreaming: { type: Boolean, default: false }
})

const emit = defineEmits(['regenerate'])

const formatModelName = (model) => {
  if (model?.includes('qwen3:1.7b')) return 'Qwen 3'
  if (model?.includes('deepseek-r1:1.5b')) return 'DeepSeek'
  return model?.split(':')[0] || model
}

const formatTime = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const copyMessage = () => {
  navigator.clipboard.writeText(props.message.content || '')
}
</script>
