<template>
  <div class="flex-1 h-full flex flex-col relative z-10 overflow-hidden">
    <!-- Top Toolbar / Model Selector -->
    <div class="h-16 px-8 flex items-center justify-between bg-black/20 backdrop-blur-sm border-b border-white/5 flex-shrink-0">
      <div class="flex items-center gap-4">
        <ModelSelector v-model="modelStore.selectedModel" />
        <div class="h-4 w-[1px] bg-white/10 mx-2"></div>
        <div class="flex items-center gap-2 text-on-tertiary-container">
          <span class="material-symbols-outlined !text-[16px] text-neural-purple">bolt</span>
          <span class="text-xs font-medium">Turbo Mode Active</span>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <button class="p-2 rounded-lg hover:bg-white/5 text-on-secondary-container hover:text-white transition-colors" title="Share">
          <span class="material-symbols-outlined">share</span>
        </button>
      </div>
    </div>

    <!-- Chat Canvas -->
    <div class="flex-1 overflow-y-auto scrollbar-hide px-8 pb-44 flex flex-col">
      <!-- Welcome Screen (no session, no local messages) -->
      <WelcomeScreen
        v-if="showWelcome"
        @use-prompt="handleUsePrompt"
      />

      <!-- Messages from store (active session) -->
      <div v-else-if="chatStore.activeSessionId" class="flex-1 w-full max-w-3xl mx-auto mt-8 flex flex-col">
        <div class="flex-1 overflow-y-auto scrollbar-hide space-y-6">
          <MessageBubble
            v-for="msg in activeMessages"
            :key="msg.id"
            :message="msg"
            :is-streaming="messageStore.streamingMessageId === msg.id"
            :streaming-content="messageStore.streamingContent"
            :streaming-thinking="messageStore.streamingThinking"
            @regenerate="handleRegenerate"
          />
        </div>
        <div ref="messagesEndRef"></div>
      </div>

      <!-- Local messages (offline fallback) -->
      <div v-else-if="localMessages.length > 0" class="flex-1 w-full max-w-3xl mx-auto mt-8 flex flex-col">
        <div class="flex-1 overflow-y-auto scrollbar-hide space-y-6">
          <MessageBubble
            v-for="msg in localMessages"
            :key="msg.id"
            :message="msg"
          />
        </div>
        <div ref="messagesEndRef"></div>
      </div>
    </div>

    <!-- Floating Input Area -->
    <MessageInput
      :model="modelStore.selectedModel"
      @send="handleSendMessage"
      @stop="handleStopStreaming"
      :disabled="messageStore.isStreaming"
      :is-streaming="messageStore.isStreaming"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useMessageStore } from '@/stores/message'
import { useModelStore } from '@/stores/model'
import WelcomeScreen from './WelcomeScreen.vue'
import MessageBubble from './MessageBubble.vue'
import MessageInput from './MessageInput.vue'
import ModelSelector from './ModelSelector.vue'

const chatStore = useChatStore()
const messageStore = useMessageStore()
const modelStore = useModelStore()

const messagesEndRef = ref(null)

const localMessages = ref([])
let localIdCounter = 0

const showWelcome = computed(() => {
  return !chatStore.activeSessionId && localMessages.value.length === 0
})

const activeMessages = computed(() => {
  const sid = chatStore.activeSessionId
  if (!sid) return []
  return messageStore.messages[sid] || []
})

const scrollToBottom = async () => {
  await nextTick()
  if (messagesEndRef.value) {
    messagesEndRef.value.scrollIntoView({ behavior: 'smooth' })
  }
}

watch(() => activeMessages.value.length, () => {
  scrollToBottom()
})

watch(() => messageStore.isStreaming, (streaming) => {
  if (!streaming) {
    scrollToBottom()
  }
})

const addLocalMessage = (content, role) => {
  localIdCounter++
  return {
    id: `local-${localIdCounter}`,
    role,
    content,
    model_name: role === 'assistant' ? modelStore.selectedModel : null,
    created_at: new Date().toISOString()
  }
}

const simulateAiResponse = () => {
  const fakeResponses = [
    "Great question! Here's what I can tell you about that topic.\n\n```python\ndef example():\n    return \"Hello from Qwen!\"\n```\n\nLet me know if you need more details!",
    "I've analyzed your request. Based on the information provided, here are my thoughts:\n\n> **Key Insight**: The solution involves a multi-step approach.\n\n1. First, we need to understand the requirements\n2. Then design the architecture\n3. Finally implement and test",
    "That's an interesting problem to solve. Here's my approach:\n\n| Aspect | Consideration |\n|--------|--------------|\n| Performance | Optimize for speed |\n| Scalability | Design for growth |\n| Maintainability | Keep it simple |",
    "I'd be happy to help with that.\n\nThe core concept revolves around **efficient data processing** and **clean architecture**.\n\n```javascript\nconst solution = (input) => {\n  return input.filter(Boolean).map(item => item.trim())\n}\n```"
  ]
  const response = fakeResponses[Math.floor(Math.random() * fakeResponses.length)]
  localMessages.value.push(addLocalMessage(response, 'assistant'))
  scrollToBottom()
}

const handleUsePrompt = async (prompt) => {
  if (chatStore.activeSessionId) {
    await messageStore.sendUserMessage(chatStore.activeSessionId, prompt, modelStore.selectedModel)
  } else {
    try {
      const session = await chatStore.createNewSession('New Chat', modelStore.selectedModel)
      await messageStore.sendUserMessage(session.id, prompt, modelStore.selectedModel)
    } catch {
      localMessages.value.push(addLocalMessage(prompt, 'user'))
      setTimeout(simulateAiResponse, 600)
    }
  }
  scrollToBottom()
}

const handleSendMessage = async (content) => {
  if (chatStore.activeSessionId) {
    await messageStore.sendUserMessage(chatStore.activeSessionId, content, modelStore.selectedModel)
  } else {
    try {
      const session = await chatStore.createNewSession('New Chat', modelStore.selectedModel)
      await messageStore.sendUserMessage(session.id, content, modelStore.selectedModel)
    } catch {
      localMessages.value.push(addLocalMessage(content, 'user'))
      setTimeout(simulateAiResponse, 600)
    }
  }
  scrollToBottom()
}

const handleStopStreaming = () => {
  messageStore.stopStreaming()
}

const handleRegenerate = async (messageId) => {
  if (chatStore.activeSessionId) {
    try {
      await messageStore.regenerate(chatStore.activeSessionId, messageId, modelStore.selectedModel)
    } catch {
      const lastAi = [...localMessages.value].reverse().find(m => m.role === 'assistant')
      if (lastAi) {
        localMessages.value = localMessages.value.filter(m => m.id !== lastAi.id)
      }
      setTimeout(simulateAiResponse, 600)
    }
  } else {
    const lastAi = [...localMessages.value].reverse().find(m => m.role === 'assistant')
    if (lastAi) {
      localMessages.value = localMessages.value.filter(m => m.id !== lastAi.id)
    }
    setTimeout(simulateAiResponse, 600)
  }
}
</script>

<style scoped>
</style>
