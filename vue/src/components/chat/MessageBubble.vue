<template>
  <div 
    class="flex gap-3" 
    :class="[message.role === 'user' ? 'flex-row-reverse' : 'flex-row']"
  >
    <!-- Avatar -->
    <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center" :class="avatarClass">
      <span class="material-symbols-outlined text-sm" v-if="message.role === 'user'">person</span>
      <span class="material-symbols-outlined text-sm" v-else>smart_toy</span>
    </div>

    <!-- Message Content -->
    <div class="flex-1 min-w-0 max-w-[85%]">
      <!-- Message Header -->
      <div class="flex items-center gap-2 mb-1">
        <span class="text-xs font-medium" :class="roleColor">{{ message.role === 'user' ? 'You' : 'Assistant' }}</span>
        <span v-if="message.model_name" class="text-[10px] font-mono-metrics text-on-tertiary-container px-1.5 py-0.5 rounded bg-white/5">
          {{ formatModelName(message.model_name) }}
        </span>
        <span class="text-[10px] text-on-tertiary-container">{{ formatTime(message.created_at) }}</span>
      </div>

      <!-- Message Body -->
      <div class="relative">
        <!-- Streaming Message -->
        <StreamingMessage 
          v-if="isStreaming && streamingContent" 
          :content="streamingContent" 
        />

        <!-- Regular Message with Markdown -->
        <div v-else class="markdown-content prose prose-invert prose-zinc max-w-none" v-html="renderedContent"></div>

        <!-- Regenerate Button (for assistant messages) -->
        <div v-if="message.role === 'assistant' && !isStreaming" class="flex items-center gap-2 mt-3 pt-3 border-t border-white/5">
          <button
            class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-on-tertiary-container hover:text-white transition-colors rounded-lg hover:bg-white/5"
            @click="handleRegenerate"
            :disabled="isStreaming"
          >
            <span class="material-symbols-outlined text-sm">refresh</span>
            Regenerate
          </button>
          <button
            class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-on-tertiary-container hover:text-white transition-colors rounded-lg hover:bg-white/5"
            @click="copyMessage"
          >
            <span class="material-symbols-outlined text-sm">content_copy</span>
            Copy
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useMarkdown } from '@/composables/useMarkdown'
import StreamingMessage from './StreamingMessage.vue'

const props = defineProps({
  message: Object,
  isStreaming: Boolean,
  streamingContent: String
})

const emit = defineEmits(['regenerate', 'copy'])

const { renderMarkdown } = useMarkdown()

const avatarClass = computed(() => 
  props.message.role === 'user' 
    ? 'bg-gradient-to-tr from-neural-purple to-neural-rose' 
    : 'bg-gradient-to-tr from-neural-indigo to-neural-purple'
)

const roleColor = computed(() => 
  props.message.role === 'user' ? 'text-neural-purple' : 'text-accent-emerald'
)

const formatModelName = (model) => {
  if (model.includes('qwen3:1.7b')) return 'Qwen 3'
  if (model.includes('deepseek-r1:1.5b')) return 'DeepSeek'
  return model.split(':')[0]
}

const formatTime = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const renderedContent = computed(() => {
  if (!props.message.content) return ''
  return renderMarkdown(props.message.content)
})

const handleRegenerate = () => {
  emit('regenerate', props.message.id)
}

const copyMessage = () => {
  navigator.clipboard.writeText(props.message.content)
  emit('copy')
}
</script>

<style scoped>
/* Scoped styles */
</style>