import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getMessages, sendMessage, regenerateMessage, deleteMessage } from '@/api/chat'
import { createWebSocketConnection, getWebSocketUrl, parseMessage } from '@/api/websocket'

export const useMessageStore = defineStore('message', () => {
  // State
  const messages = ref({}) // Keyed by sessionId: { [sessionId]: Message[] }
  const streamingMessageId = ref(null)
  const streamingContent = ref('')
  const isStreaming = ref(false)
  const streamingTokens = ref(0)
  const streamingError = ref(null)
  const wsConnection = ref(null)

  // Getters
  const messagesBySession = computed(() => (sessionId) => messages.value[sessionId] || [])

  const currentStreamingContent = computed(() => streamingContent.value)

  const currentStreamingTokens = computed(() => streamingTokens.value)

  const currentStreamingError = computed(() => streamingError.value)

  // Actions
  async function fetchMessages(sessionId, page = 1, size = 50) {
    try {
      const response = await getMessages(sessionId, { page, size })
      const data = response.data

      if (page === 1) {
        messages.value[sessionId] = data.items || []
      } else {
        const existing = messages.value[sessionId] || []
        messages.value[sessionId] = [...existing, ...(data.items || [])]
      }

      return data
    } catch (error) {
      console.error('Failed to fetch messages:', error)
      throw error
    }
  }

  async function sendUserMessage(sessionId, content, model) {
    // Create optimistic user message
    const optimisticMessage = {
      id: `temp-${Date.now()}`,
      session_id: sessionId,
      role: 'user',
      content,
      model,
      created_at: new Date().toISOString(),
      is_optimistic: true,
    }

    if (!messages.value[sessionId]) messages.value[sessionId] = []
    messages.value[sessionId].push(optimisticMessage)

    try {
      const response = await sendMessage(sessionId, { content, model })
      const serverMessage = response.data

      // Replace optimistic with server response
      const index = messages.value[sessionId].findIndex(m => m.id === optimisticMessage.id)
      if (index !== -1) {
        messages.value[sessionId][index] = serverMessage
      }

      // Start streaming for the assistant response
      startStreaming(sessionId, serverMessage.id, model)

      return serverMessage
    } catch (error) {
      // Remove optimistic message on error
      const index = messages.value[sessionId].findIndex(m => m.id === optimisticMessage.id)
      if (index !== -1) {
        messages.value[sessionId].splice(index, 1)
      }
      throw error
    }
  }

  function startStreaming(sessionId, messageId, model) {
    streamingMessageId.value = messageId
    streamingContent.value = ''
    isStreaming.value = true
    streamingTokens.value = 0
    streamingError.value = null

    // Create assistant message placeholder
    const assistantMessage = {
      id: messageId,
      session_id: sessionId,
      role: 'assistant',
      content: '',
      model,
      created_at: new Date().toISOString(),
      is_streaming: true,
    }

    if (!messages.value[sessionId]) messages.value[sessionId] = []
    messages.value[sessionId].push(assistantMessage)

    // Connect WebSocket
    wsConnection.value = createWebSocketConnection({
      sessionId,
      messageId,
      model,
      onMessage: handleStreamMessage,
      onError: handleStreamError,
      onClose: handleStreamClose,
      onOpen: handleStreamOpen,
    })
  }

  function handleStreamMessage(data) {
    const parsed = parseMessage(data)

    switch (parsed.type) {
      case 'token':
      case 'content':
      case 'delta':
        streamingContent.value += parsed.content || ''
        streamingTokens.value = parsed.tokens || streamingTokens.value + 1
        // Update the streaming message content
        updateStreamingMessage()
        break
      case 'done':
        finishStreaming(parsed.tokens)
        break
      case 'error':
        streamingError.value = parsed.error
        finishStreaming()
        break
    }
  }

  function updateStreamingMessage() {
    if (!streamingMessageId.value) return
    const sessionMessages = Object.values(messages.value).flat()
    const msg = sessionMessages.find(m => m.id === streamingMessageId.value)
    if (msg) {
      msg.content = streamingContent.value
      msg.is_streaming = true
      msg.tokens = streamingTokens.value
    }
  }

  function finishStreaming(finalTokens = streamingTokens.value) {
    isStreaming.value = false

    if (streamingMessageId.value) {
      const sessionMessages = Object.values(messages.value).flat()
      const msg = sessionMessages.find(m => m.id === streamingMessageId.value)
      if (msg) {
        msg.content = streamingContent.value
        msg.is_streaming = false
        msg.tokens = finalTokens
      }
    }

    streamingMessageId.value = null
    streamingContent.value = ''
    streamingTokens.value = 0
    wsConnection.value = null
  }

  function handleStreamError(error) {
    streamingError.value = error.message
    finishStreaming()
  }

  function handleStreamClose(event) {
    if (isStreaming.value) {
      // Connection closed unexpectedly
      streamingError.value = 'Connection closed unexpectedly'
      finishStreaming()
    }
  }

  function handleStreamOpen(event) {
    console.log('WebSocket streaming connection opened')
  }

  async function regenerate(sessionId, messageId, model) {
    try {
      const response = await regenerateMessage(sessionId, messageId, model)
      const newMessage = response.data

      // Find and replace the old message
      const sessionMsgs = messages.value[sessionId] || []
      const index = sessionMsgs.findIndex(m => m.id === messageId)
      if (index !== -1) {
        sessionMsgs[index] = newMessage
      }

      return newMessage
    } catch (error) {
      console.error('Failed to regenerate message:', error)
      throw error
    }
  }

  async function removeMessage(sessionId, messageId) {
    try {
      await deleteMessage(sessionId, messageId)
      const sessionMsgs = messages.value[sessionId] || []
      messages.value[sessionId] = sessionMsgs.filter(m => m.id !== messageId)
    } catch (error) {
      console.error('Failed to delete message:', error)
      throw error
    }
  }

  function clearMessages(sessionId) {
    if (sessionId) {
      messages.value[sessionId] = []
    } else {
      messages.value = {}
    }
  }

  function addMessage(sessionId, message) {
    if (!messages.value[sessionId]) messages.value[sessionId] = []
    messages.value[sessionId].push(message)
  }

  function updateMessage(sessionId, messageId, updates) {
    const sessionMsgs = messages.value[sessionId] || []
    const index = sessionMsgs.findIndex(m => m.id === messageId)
    if (index !== -1) {
      messages.value[sessionId][index] = { ...sessionMsgs[index], ...updates }
    }
  }

  return {
    // State
    messages,
    streamingMessageId,
    streamingContent,
    isStreaming,
    streamingTokens,
    streamingError,
    wsConnection,

    // Getters
    messagesBySession,
    currentStreamingContent,
    currentStreamingTokens,
    currentStreamingError,

    // Actions
    fetchMessages,
    sendUserMessage,
    startStreaming,
    finishStreaming,
    regenerate,
    removeMessage,
    clearMessages,
    addMessage,
    updateMessage,
  }
})