import { ref, computed } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useMessageStore } from '@/stores/message'
import { useModelStore } from '@/stores/model'
import { useUIStore } from '@/stores/ui'

export function useChat() {
  const chatStore = useChatStore()
  const messageStore = useMessageStore()
  const modelStore = useModelStore()
  const uiStore = useUIStore()

  // Create a new chat session
  async function createNewSession(title = 'New Chat', model = modelStore.selectedModel || 'qwen3:1.7b') {
    try {
      const session = await chatStore.createNewSession(title, model)
      return session
    } catch (error) {
      uiStore.addToast(`Failed to create session: ${error.message}`, 'error')
      throw error
    }
  }

  // Select/switch to a session
  function selectSession(sessionId) {
    chatStore.setActiveSession(sessionId)
    messageStore.fetchMessages(sessionId)
  }

  // Send a message in the current session
  async function sendMessage(content, model = modelStore.selectedModel) {
    const sessionId = chatStore.activeSessionId
    if (!sessionId) {
      // Create new session if none active
      const session = await createNewSession()
      return sendMessage(content, model)
    }

    try {
      await messageStore.sendUserMessage(sessionId, content, model)
    } catch (error) {
      uiStore.addToast(`Failed to send message: ${error.message}`, 'error')
      throw error
    }
  }

  // Regenerate the last assistant message
  async function regenerateMessage(messageId, model = modelStore.selectedModel) {
    const sessionId = chatStore.activeSessionId
    if (!sessionId) return

    try {
      await messageStore.regenerate(sessionId, messageId, model)
    } catch (error) {
      uiStore.addToast(`Failed to regenerate: ${error.message}`, 'error')
      throw error
    }
  }

  // Delete a session
  async function deleteSession(sessionId) {
    try {
      await chatStore.deleteSessionById(sessionId)
      uiStore.addToast('Session deleted', 'success')
    } catch (error) {
      uiStore.addToast(`Failed to delete session: ${error.message}`, 'error')
      throw error
    }
  }

  // Pin/unpin a session
  async function pinSession(sessionId) {
    try {
      await chatStore.pinSession(sessionId)
    } catch (error) {
      uiStore.addToast(`Failed to pin session: ${error.message}`, 'error')
    }
  }

  async function unpinSession(sessionId) {
    try {
      await chatStore.unpinSession(sessionId)
    } catch (error) {
      uiStore.addToast(`Failed to unpin session: ${error.message}`, 'error')
    }
  }

  // Update session title
  async function updateSessionTitle(sessionId, title) {
    try {
      await chatStore.updateSessionById(sessionId, { title })
    } catch (error) {
      uiStore.addToast(`Failed to update title: ${error.message}`, 'error')
    }
  }

  // Load more sessions (pagination)
  async function loadMoreSessions() {
    if (chatStore.currentPage < chatStore.totalPages) {
      await chatStore.fetchSessions(chatStore.currentPage + 1)
    }
  }

  // Getters from stores
  const activeSession = computed(() => chatStore.activeSession)
  const sessions = computed(() => chatStore.sessionsList)
  const messages = computed(() => messageStore.messagesBySession(chatStore.activeSessionId))
  const isStreaming = computed(() => messageStore.isStreaming)
  const streamingContent = computed(() => messageStore.currentStreamingContent)
  const selectedModel = computed(() => modelStore.selectedModel)
  const availableModels = computed(() => modelStore.modelOptions)

  return {
    // Actions
    createNewSession,
    selectSession,
    sendMessage,
    regenerateMessage,
    deleteSession,
    pinSession,
    unpinSession,
    updateSessionTitle,
    loadMoreSessions,

    // Getters
    activeSession,
    sessions,
    messages,
    isStreaming,
    streamingContent,
    selectedModel,
    availableModels,

    // Direct store access for advanced use
    chatStore,
    messageStore,
    modelStore,
    uiStore,
  }
}