<template>
  <div class="flex-1 h-full flex flex-col relative z-10 overflow-hidden">
    <!-- Top Toolbar / Model Selector -->
    <div class="h-16 px-8 flex items-center justify-between bg-black/20 backdrop-blur-sm border-b border-white/5 flex-shrink-0">
      <div class="flex items-center gap-4">
        <ModelSelector />
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
    <div class="flex-1 overflow-y-auto scrollbar-hide px-8 pb-32 flex flex-col">
      <!-- Welcome Screen (when no active session) -->
      <WelcomeScreen 
        v-if="!chatStore.activeSession" 
        @use-prompt="handleUsePrompt"
      />

      <!-- Messages List (when active session) -->
      <div v-else class="flex-1 w-full max-w-3xl mx-auto mt-8 flex flex-col">
        <div 
          ref="messagesEndRef" 
          class="flex-1 overflow-y-auto scrollbar-hide space-y-6"
        >
          <MessageBubble
            v-for="message in chatStore.messagesBySession"
            :key="message.id"
            :message="message"
            :is-streaming="messageStore.streamingMessageId === message.id"
            :streaming-content="messageStore.streamingContent"
          />
          
          <!-- Streaming Indicator -->
          <div v-if="messageStore.isStreaming && messageStore.streamingMessageId === null" class="flex justify-start">
            <StreamingMessage :content="messageStore.streamingContent" />
          </div>
        </div>
        
        <!-- Auto-scroll anchor -->
        <div ref="messagesEndRef"></div>
      </div>
    </div>

    <!-- Floating Input Area -->
    <MessageInput
      v-if="chatStore.activeSession"
      :model="modelStore.selectedModel"
      @send="handleSendMessage"
      @regenerate="handleRegenerate"
      :disabled="messageStore.isStreaming"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useMessageStore } from '@/stores/message'
import { useModelStore } from '@/stores/model'
import WelcomeScreen from './WelcomeScreen.vue'
import MessageBubble from './MessageBubble.vue'
import MessageInput from './MessageInput.vue'
import StreamingMessage from './StreamingMessage.vue'
import ModelSelector from './ModelSelector.vue'

const chatStore = useChatStore()
const messageStore = useMessageStore()
const modelStore = useModelStore()

const messagesEndRef = ref(null)

const scrollToBottom = async () => {
  await nextTick()
  if (messagesEndRef.value) {
    messagesEndRef.value.scrollIntoView({ behavior: 'smooth' })
  }
}

watch(() => chatStore.activeSessionId, async () => {
  if (chatStore.activeSessionId) {
    await messageStore.fetchMessages(chatStore.activeSessionId)
    await nextTick()
    scrollToBottom()
  }
})

watch(() => messageStore.messagesBySession.length, () => {
  scrollToBottom()
})

watch(() => messageStore.isStreaming, (streaming) => {
  if (!streaming) {
    scrollToBottom()
  }
})

const handleUsePrompt = (prompt) => {
  messageStore.sendMessage(chatStore.activeSessionId, prompt, modelStore.selectedModel)
}

const handleSendMessage = async (content) => {
  if (!chatStore.activeSessionId) return
  await messageStore.sendMessage(chatStore.activeSessionId, content, modelStore.selectedModel)
}

const handleRegenerate = async (messageId) => {
  if (!chatStore.activeSessionId) return
  await messageStore.regenerateMessage(chatStore.activeSessionId, messageId, modelStore.selectedModel)
}
</script>

<style scoped>
/* Scoped styles if needed */
</style>