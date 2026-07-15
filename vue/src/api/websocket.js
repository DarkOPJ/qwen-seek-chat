/**
 * WebSocket connection manager for streaming chat responses
 */

let globalReconnectTimer = null

export function createWebSocketConnection({ sessionId, messageId, model, onMessage, onError, onClose, onOpen }) {
  const wsUrl = getWebSocketUrl(sessionId, messageId, model)
  const ws = new WebSocket(wsUrl)

  let reconnectAttempts = 0
  const maxReconnectAttempts = 5
  const baseReconnectDelay = 1000 // 1 second

  ws.onopen = (event) => {
    console.log('WebSocket connected:', wsUrl)
    reconnectAttempts = 0
    if (onOpen) onOpen(event)
  }

  ws.onmessage = (event) => {
    try {
      const data = parseMessage(event.data)
      if (onMessage) onMessage(data)
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error, event.data)
      if (onError) onError(new Error('Failed to parse message'))
    }
  }

  ws.onerror = (event) => {
    console.error('WebSocket error:', event)
    if (onError) onError(new Error('WebSocket connection error'))
  }

  ws.onclose = (event) => {
    console.log('WebSocket closed:', event.code, event.reason)

    // Attempt reconnection if not closed cleanly
    if (event.code !== 1000 && reconnectAttempts < maxReconnectAttempts) {
      const delay = baseReconnectDelay * Math.pow(2, reconnectAttempts) + Math.random() * 1000
      console.log(`Reconnecting in ${delay}ms (attempt ${reconnectAttempts + 1}/${maxReconnectAttempts})`)

      globalReconnectTimer = setTimeout(() => {
        reconnectAttempts++
        // Create new connection
        const newWs = createWebSocketConnection({ sessionId, messageId, model, onMessage, onError, onClose, onOpen })
        // Replace the reference (caller would need to handle this)
      }, delay)
    } else if (onClose) {
      onClose(event)
    }
  }

  function send(data) {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(data))
      return true
    }
    return false
  }

  function disconnect() {
    if (globalReconnectTimer) {
      clearTimeout(globalReconnectTimer)
      globalReconnectTimer = null
    }
    ws.close(1000, 'Client disconnect')
  }

  return {
    ws,
    send,
    disconnect,
    get readyState() {
      return ws.readyState
    },
  }
}

export function getWebSocketUrl(sessionId, messageId, model) {
  const baseUrl = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000'
  const params = new URLSearchParams({ message_id: messageId, model })
  return `${baseUrl}/chat/api/v1/sessions/${sessionId}/stream?${params.toString()}`
}

export function parseMessage(data) {
  // Handle different message formats from backend
  // Expected formats:
  // { type: 'token', content: '...', tokens: 1 }
  // { type: 'content', content: '...' }
  // { type: 'done', tokens: 150 }
  // { type: 'error', error: '...' }

  if (typeof data === 'string') {
    try {
      return JSON.parse(data)
    } catch {
      // Plain text message
      return { type: 'content', content: data }
    }
  }

  return data
}

export function createStreamingConnection(sessionId, messageId, model) {
  return createWebSocketConnection({ sessionId, messageId, model })
}