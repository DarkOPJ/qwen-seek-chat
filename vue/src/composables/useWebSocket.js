import { ref, onUnmounted } from 'vue'
import { useMessageStore } from '@/stores/message'

export function useWebSocket(sessionId, messageId, model) {
  const messageStore = useMessageStore()
  const ws = ref(null)
  const isConnected = ref(false)
  const error = ref(null)
  const reconnectAttempts = ref(0)
  const maxReconnectAttempts = 5
  const reconnectDelay = ref(1000)

  const connect = () => {
    if (ws.value && (ws.value.readyState === WebSocket.OPEN || ws.value.readyState === WebSocket.CONNECTING)) {
      return
    }

    const wsUrl = `${import.meta.env.VITE_API_BASE_URL || ''}/ws/chat/api/v1/sessions/${sessionId}/stream?message_id=${messageId}&model=${model}`
      .replace('http://', 'ws://')
      .replace('https://', 'wss://')

    ws.value = new WebSocket(wsUrl)

    ws.value.onopen = () => {
      console.log('WebSocket connected')
      isConnected.value = true
      error.value = null
      reconnectAttempts.value = 0
      reconnectDelay.value = 1000
    }

    ws.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        
        if (data.error) {
          error.value = data.error
          messageStore.finishStreaming(data.message_id, data.tokens || 0)
          return
        }

        if (data.content) {
          messageStore.appendStreamingContent(data.content)
        }

        if (data.done) {
          messageStore.finishStreaming(data.message_id, data.tokens || 0)
          disconnect()
        }
      } catch (err) {
        console.error('WebSocket message parse error:', err)
      }
    }

    ws.value.onclose = () => {
      console.log('WebSocket disconnected')
      isConnected.value = false
      
      if (reconnectAttempts.value < maxReconnectAttempts) {
        setTimeout(() => {
          reconnectAttempts.value++
          reconnectDelay.value *= 2
          connect()
        }, reconnectDelay.value)
      } else {
        error.value = 'Connection lost. Please try again.'
        messageStore.finishStreaming(messageId, 0)
      }
    }

    ws.value.onerror = (err) => {
      console.error('WebSocket error:', err)
      error.value = 'Connection error'
    }
  }

  const disconnect = () => {
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
    isConnected.value = false
  }

  const send = (data) => {
    if (ws.value && ws.value.readyState === WebSocket.OPEN) {
      ws.value.send(JSON.stringify(data))
    }
  }

  onUnmounted(() => {
    disconnect()
  })

  return {
    ws,
    isConnected,
    error,
    connect,
    disconnect,
    send
  }
}