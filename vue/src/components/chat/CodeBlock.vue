<template>
  <div class="code-block relative group">
    <!-- Header with language and copy button -->
    <div class="code-block-header flex items-center justify-between px-4 py-2 bg-white/5 border-b border-white/10">
      <span class="font-mono-metrics text-xs text-on-tertiary-container">{{ language || 'text' }}</span>
      <button
        class="copy-btn p-1.5 rounded hover:bg-white/10 text-on-tertiary-container hover:text-white transition-colors opacity-0 group-hover:opacity-100"
        @click="copyCode"
        :title="copied ? 'Copied!' : 'Copy code'"
      >
        <span class="material-symbols-outlined text-sm" :class="{ 'text-accent-emerald': copied }">
          {{ copied ? 'check' : 'content_copy' }}
        </span>
      </button>
    </div>

    <!-- Code content -->
    <pre class="p-4 overflow-x-auto bg-transparent m-0"><code 
      class="font-mono-metrics text-sm leading-relaxed" 
      v-html="highlightedCode"
    ></code></pre>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-dark.css'

const props = defineProps({
  code: String,
  language: String
})

const highlightedCode = ref('')
const copied = ref(false)

const highlight = async () => {
  await nextTick()
  const code = props.code
  const lang = props.language || 'plaintext'
  
  try {
    if (hljs.getLanguage(lang)) {
      highlightedCode.value = hljs.highlight(code, { language: lang }).value
    } else {
      highlightedCode.value = hljs.highlightAuto(code).value
    }
  } catch (e) {
    highlightedCode.value = escapeHtml(code)
  }
}

const escapeHtml = (text) => {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

const copyCode = async () => {
  try {
    await navigator.clipboard.writeText(props.code)
    copied.value = true
    setTimeout(() => copied.value = false, 2000)
  } catch (e) {
    console.error('Failed to copy:', e)
  }
}

watch(() => props.code, highlight, { immediate: true })
watch(() => props.language, highlight)
</script>

<style scoped>
.code-block {
  @apply rounded-xl overflow-hidden bg-zinc-950/50 border border-white/10 my-3;
}

.code-block-header {
  @apply bg-white/5 border-b border-white/10;
}

.copy-btn {
  @apply transition-all duration-200;
}

.copy-btn:hover {
  @apply bg-white/10;
}

.copy-btn .text-accent-emerald {
  @apply animate-pulse;
}

pre {
  @apply m-0 p-0;
}

code {
  @apply font-mono-metrics text-sm;
}

/* Override highlight.js styles for dark theme */
.hljs {
  @apply bg-transparent text-white;
}

.hljs-keyword,
.hljs-selector-tag,
.hljs-built_in,
.hljs-name,
.hljs-tag {
  @apply text-neural-purple;
}

.hljs-string,
.hljs-attr,
.hljs-symbol,
.hljs-bullet,
.hljs-addition {
  @apply text-accent-emerald;
}

.hljs-comment,
.hljs-quote,
.hljs-deletion {
  @apply text-zinc-500 italic;
}

.hljs-number,
.hljs-literal,
.hljs-regexp {
  @apply text-neural-rose;
}

.hljs-function,
.hljs-title,
.hljs-section,
.hljs-type {
  @apply text-neural-indigo;
}

.hljs-params,
.hljs-variable {
  @apply text-white;
}
</style>