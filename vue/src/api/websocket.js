/**
 * WebSocket connection manager for streaming chat responses
 */

import { getWebSocketUrl } from '@/api/chat'

export function createWebSocketConnection({ sessionId, messageId, content, model, onMessage, onError, onClose, onOpen }) {
  const wsUrl = getWebSocketUrl(sessionId, { messageId, content, model })
  const ws = new WebSocket(wsUrl)

  ws.onopen = (event) => {
    console.log('WebSocket connected:', wsUrl)
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
    if (onClose) onClose(event)
  }

  function disconnect() {
    ws.close(1000, 'Client disconnect')
  }

  return {
    ws,
    disconnect,
    get readyState() {
      return ws.readyState
    },
  }
}

export function parseMessage(data) {
  if (typeof data === 'string') {
    try {
      const parsed = JSON.parse(data)
      return translateBackendChunk(parsed)
    } catch {
      return { type: 'content', content: data }
    }
  }
  return translateBackendChunk(data)
}

function translateBackendChunk(chunk) {
  if (chunk.error) {
    return { type: 'error', error: chunk.error }
  }
  if (chunk.done) {
    return { type: 'done', content: '', tokens: chunk.tokens || 0, message_id: chunk.message_id }
  }
  return {
    type: 'content',
    content: chunk.accumulated_content || chunk.content || '',
    thinking: chunk.accumulated_thinking || chunk.thinking || '',
    tokens: chunk.tokens || 0,
  }
}

export function createStreamingConnection(sessionId, messageId, model) {
  return createWebSocketConnection({ sessionId, messageId, model })
}