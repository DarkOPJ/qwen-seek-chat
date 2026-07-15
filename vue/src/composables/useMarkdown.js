import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-dark.css'

// Configure marked
marked.setOptions({
  breaks: true,
  gfm: true
})

// Custom renderer for code blocks with copy button
const renderer = new marked.Renderer()

// Store code blocks for copy functionality
const codeBlocks = new Map()

renderer.code = function({ text, lang }) {
  const language = lang || 'plaintext'
  const codeId = 'code-' + Math.random().toString(36).substr(2, 9)
  
  // Store code for copy functionality
  codeBlocks.set(codeId, text)
  
  let highlighted = text
  try {
    if (hljs.getLanguage(language)) {
      highlighted = hljs.highlight(text, { language }).value
    } else {
      highlighted = hljs.highlightAuto(text).value
    }
  } catch (e) {
    highlighted = escapeHtml(text)
  }
  
  return `<div class="code-block-wrapper relative group my-3" data-code-id="${codeId}">
    <div class="code-block-header flex items-center justify-between px-4 py-2 bg-white/5 border-b border-white/10">
      <span class="font-mono-metrics text-xs text-on-tertiary-container">${escapeHtml(language)}</span>
      <button class="copy-btn p-1.5 rounded hover:bg-white/10 text-on-tertiary-container hover:text-white transition-colors opacity-0 group-hover:opacity-100" data-code-id="${codeId}" title="Copy code">
        <span class="material-symbols-outlined text-sm">content_copy</span>
      </button>
    </div>
    <pre class="p-4 overflow-x-auto m-0"><code class="language-${escapeHtml(language)} hljs">${highlighted}</code></pre>
  </div>`
}

function escapeHtml(text) {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

// Override inline code
renderer.codespan = function({ text }) {
  return `<code class="font-mono-metrics text-sm bg-white/5 px-1.5 py-0.5 rounded">${escapeHtml(text)}</code>`
}

marked.use({ renderer })

// Handle copy button clicks
if (typeof window !== 'undefined') {
  document.addEventListener('click', async (e) => {
    const copyBtn = e.target.closest('.copy-btn')
    if (copyBtn) {
      const codeId = copyBtn.dataset.codeId
      const code = codeBlocks.get(codeId)
      if (code) {
        try {
          await navigator.clipboard.writeText(code)
          const icon = copyBtn.querySelector('.material-symbols-outlined')
          if (icon) {
            const original = icon.textContent
            icon.textContent = 'check'
            icon.classList.add('text-accent-emerald')
            setTimeout(() => {
              icon.textContent = original
              icon.classList.remove('text-accent-emerald')
            }, 2000)
          }
        } catch (err) {
          console.error('Copy failed:', err)
        }
      }
    }
  })
}

export function useMarkdown() {
  const renderMarkdown = (text) => {
    if (!text) return ''
    return marked.parse(text)
  }

  return {
    renderMarkdown
  }
}