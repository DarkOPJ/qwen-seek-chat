import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getMessages, sendMessage, regenerateMessage, deleteMessage } from '@/api/chat'
import { createWebSocketConnection, parseMessage } from '@/api/websocket'

export const useMessageStore = defineStore('message', () => {
  // State
  const messages = ref({}) // Keyed by sessionId: { [sessionId]: Message[] }
  const streamingMessageId = ref(null)
  const streamingContent = ref('')
  const streamingThinking = ref('')
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
      const data = await getMessages(sessionId, { page, size })

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
    const msgId = `user-${Date.now()}`
    const assistantId = `assistant-${Date.now()}`

    // Create optimistic user message
    const userMessage = {
      id: msgId,
      session_id: sessionId,
      role: 'user',
      content,
      model,
      created_at: new Date().toISOString(),
    }

    // Create empty assistant message for streaming
    const assistantMessage = {
      id: assistantId,
      session_id: sessionId,
      role: 'assistant',
      content: '',
      model,
      created_at: new Date().toISOString(),
      is_streaming: true,
    }

    if (!messages.value[sessionId]) messages.value[sessionId] = []
    messages.value[sessionId].push(userMessage)
    messages.value[sessionId].push(assistantMessage)

    streamingMessageId.value = assistantId
    streamingContent.value = ''
    streamingThinking.value = ''
    isStreaming.value = true
    streamingTokens.value = 0
    streamingError.value = null

    // Open WebSocket to stream the response
    wsConnection.value = createWebSocketConnection({
      sessionId,
      content,
      model,
      onMessage: handleStreamMessage,
      onError: handleStreamError,
      onClose: handleStreamClose,
      onOpen: handleStreamOpen,
    })

    return { userMessage, assistantMessage }
  }

  function startStreaming(sessionId, messageId, model) {
    streamingMessageId.value = messageId
    streamingContent.value = ''
    streamingThinking.value = ''
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
        streamingContent.value = parsed.content || ''
        streamingThinking.value = parsed.thinking || ''
        streamingTokens.value = parsed.tokens || streamingTokens.value + 1
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
      msg.thinking = streamingThinking.value
      msg.is_streaming = true
      msg.tokens = streamingTokens.value
    }
  }

  function finishStreaming(finalTokens = streamingTokens.value) {
    isStreaming.value = false

    const mid = streamingMessageId.value
    const finalContent = streamingContent.value
    const finalThinking = streamingThinking.value

    if (mid) {
      for (const sid of Object.keys(messages.value)) {
        const idx = messages.value[sid].findIndex(m => m.id === mid)
        if (idx !== -1) {
          messages.value[sid][idx] = {
            ...messages.value[sid][idx],
            content: finalContent,
            is_streaming: false,
            tokens: finalTokens,
          }
          break
        }
      }
    }

    streamingMessageId.value = null
    streamingContent.value = ''
    streamingThinking.value = ''
    streamingTokens.value = 0
    wsConnection.value = null
  }

  function handleStreamError(error) {
    streamingError.value = error.message
    finishStreaming()
  }

  function handleStreamClose(event) {
    if (isStreaming.value) {
      finishStreaming()
    }
  }

  function handleStreamOpen(event) {
    console.log('WebSocket streaming connection opened')
  }

  async function regenerate(sessionId, messageId, model) {
    try {
      const newMessage = await regenerateMessage(sessionId, messageId, model)

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

  function stopStreaming() {
    if (wsConnection.value) {
      wsConnection.value.disconnect()
    }
    finishStreaming(streamingTokens.value)
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
    streamingThinking,
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
    stopStreaming,
    regenerate,
    removeMessage,
    clearMessages,
    addMessage,
    updateMessage,
  }
})