import api from './http'

// Session API
export function createSession(data) {
  return api.post('/chat/api/v1/sessions', data)
}

export function getSessions(params = {}) {
  return api.get('/chat/api/v1/sessions', { params })
}

export function getSession(id) {
  return api.get(`/chat/api/v1/sessions/${id}`)
}

export function updateSession(id, data) {
  return api.patch(`/chat/api/v1/sessions/${id}`, data)
}

export function deleteSession(id) {
  return api.delete(`/chat/api/v1/sessions/${id}`)
}

// Message API
export function sendMessage(sessionId, data) {
  return api.post(`/chat/api/v1/sessions/${sessionId}/messages`, data)
}

export function getMessages(sessionId, params = {}) {
  return api.get(`/chat/api/v1/sessions/${sessionId}/messages`, { params })
}

export function regenerateMessage(sessionId, messageId, model) {
  return api.post(`/chat/api/v1/sessions/${sessionId}/messages/${messageId}/regenerate`, { model })
}

export function deleteMessage(sessionId, messageId) {
  return api.delete(`/chat/api/v1/sessions/${sessionId}/messages/${messageId}`)
}

// WebSocket endpoint for streaming (matches backend: /chat/api/v1/sessions/{session_id}/stream?message_id={id}&model={model})
export function getWebSocketUrl(sessionId, messageId, model) {
  const baseUrl = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000'
  const params = new URLSearchParams({ message_id: messageId, model })
  return `${baseUrl}/chat/api/v1/sessions/${sessionId}/stream?${params.toString()}`
}