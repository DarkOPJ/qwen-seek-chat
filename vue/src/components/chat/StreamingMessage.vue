<template>
  <div>
    <button
      v-if="thinking"
      class="flex items-center gap-1.5 text-xs text-on-tertiary-container/60 hover:text-white transition-colors mb-2"
      @click="thinkingOpen = !thinkingOpen"
    >
      <span class="material-symbols-outlined !text-[14px] transition-transform duration-200" :class="thinkingOpen ? 'rotate-90' : ''">chevron_right</span>
      <span>Thinking</span>
      <span v-if="!content" class="material-symbols-outlined !text-[10px] animate-pulse text-accent-emerald">circle</span>
    </button>
    <div v-if="thinkingOpen && thinking" class="mb-3 text-xs leading-relaxed text-on-tertiary-container/60 whitespace-pre-wrap border-l-2 border-white/10 pl-3">
      {{ thinking }}
    </div>

    <div v-if="content" class="markdown-content prose prose-invert prose-zinc max-w-none" v-html="renderedContent"></div>
    <span v-else-if="isStreaming" class="inline-block w-1 h-4 bg-accent-emerald animate-pulse align-bottom"></span>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useMarkdown } from '@/composables/useMarkdown'

const props = defineProps({
  content: String,
  thinking: String,
  isStreaming: Boolean,
})

const { renderMarkdown } = useMarkdown()
const thinkingOpen = ref(false)

const renderedContent = computed(() => {
  if (!props.content) return ''
  const rendered = renderMarkdown(props.content)
  if (props.isStreaming) {
    return rendered + '<span class="inline-block w-1 h-4 bg-accent-emerald animate-pulse ml-0.5 align-bottom"></span>'
  }
  return rendered
})
</script>
