<template>
  <div class="flex gap-3">
    <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-tr from-neural-indigo to-neural-purple flex items-center justify-center">
      <span class="material-symbols-outlined text-sm">smart_toy</span>
    </div>
    <div class="flex-1 min-w-0">
      <div class="flex items-center gap-2 mb-1">
        <span class="text-xs font-medium text-accent-emerald">Assistant</span>
        <span class="material-symbols-outlined text-xs animate-pulse text-accent-emerald">circle</span>
      </div>
      <div class="markdown-content prose prose-invert prose-zinc max-w-none" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useMarkdown } from '@/composables/useMarkdown'

const props = defineProps({
  content: String
})

const { renderMarkdown } = useMarkdown()

const renderedContent = computed(() => {
  if (!props.content) return ''
  // Add cursor animation
  return renderMarkdown(props.content) + '<span class="inline-block w-1 h-4 bg-accent-emerald animate-pulse ml-0.5 align-bottom"></span>'
})
</script>

<style scoped>
/* Scoped styles */
</style>