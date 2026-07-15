import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getSessions, createSession, getSession, updateSession, deleteSession } from '@/api/chat'

export const useChatStore = defineStore('chat', () => {
  // State
  const sessions = ref([])
  const activeSessionId = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pinnedSessions = ref([])
  const recentSessions = ref([])
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalSessions = ref(0)

  // Getters
  const activeSession = computed(() => {
    if (!activeSessionId.value) return null
    return sessions.value.find(s => s.id === activeSessionId.value) || null
  })

  const sessionsList = computed(() => {
    // Combine pinned and recent, removing duplicates
    const all = [...pinnedSessions.value, ...recentSessions.value]
    const seen = new Set()
    return all.filter(s => {
      if (seen.has(s.id)) return false
      seen.add(s.id)
      return true
    })
  })

  const isLoading = computed(() => loading.value)

  // Actions
  async function fetchSessions(page = 1, size = 20) {
    loading.value = true
    error.value = null
    try {
      const response = await getSessions({ page, size })
      const data = response.data

      if (page === 1) {
        sessions.value = data.items || []
      } else {
        sessions.value = [...sessions.value, ...(data.items || [])]
      }

      // Update pinned and recent
      pinnedSessions.value = sessions.value.filter(s => s.pinned)
      recentSessions.value = sessions.value.filter(s => !s.pinned).slice(0, 10)

      currentPage.value = data.page || page
      totalPages.value = data.total_pages || 1
      totalSessions.value = data.total || 0

      return data
    } catch (err) {
      error.value = err.message || 'Failed to fetch sessions'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createNewSession(title = 'New Chat', model = 'qwen3:1.7b') {
    loading.value = true
    error.value = null
    try {
      const response = await createSession({ title, model })
      const session = response.data
      sessions.value.unshift(session)
      if (!session.pinned) {
        recentSessions.value.unshift(session)
      }
      setActiveSession(session.id)
      return session
    } catch (err) {
      error.value = err.message || 'Failed to create session'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchSessionById(sessionId) {
    loading.value = true
    error.value = null
    try {
      const response = await getSession(sessionId)
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to fetch session'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateSessionById(sessionId, data) {
    loading.value = true
    error.value = null
    try {
      const response = await updateSession(sessionId, data)
      const updated = response.data
      updateSessionInList(updated)
      return updated
    } catch (err) {
      error.value = err.message || 'Failed to update session'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteSessionById(sessionId) {
    loading.value = true
    error.value = null
    try {
      await deleteSession(sessionId)
      removeSession(sessionId)
    } catch (err) {
      error.value = err.message || 'Failed to delete session'
      throw err
    } finally {
      loading.value = false
    }
  }

  function setActiveSession(sessionId) {
    activeSessionId.value = sessionId
  }

  function addSession(session) {
    sessions.value.unshift(session)
    if (!session.pinned) {
      recentSessions.value.unshift(session)
      if (recentSessions.value.length > 10) {
        recentSessions.value = recentSessions.value.slice(0, 10)
      }
    }
  }

  function removeSession(sessionId) {
    sessions.value = sessions.value.filter(s => s.id !== sessionId)
    pinnedSessions.value = pinnedSessions.value.filter(s => s.id !== sessionId)
    recentSessions.value = recentSessions.value.filter(s => s.id !== sessionId)

    if (activeSessionId.value === sessionId) {
      activeSessionId.value = sessions.value[0]?.id || null
    }
  }

  function updateSessionInList(session) {
    const index = sessions.value.findIndex(s => s.id === session.id)
    if (index !== -1) {
      sessions.value[index] = session
    }

    const pinnedIndex = pinnedSessions.value.findIndex(s => s.id === session.id)
    if (pinnedIndex !== -1) {
      pinnedSessions.value[pinnedIndex] = session
    }

    const recentIndex = recentSessions.value.findIndex(s => s.id === session.id)
    if (recentIndex !== -1) {
      recentSessions.value[recentIndex] = session
    }
  }

  async function pinSession(sessionId) {
    const session = sessions.value.find(s => s.id === sessionId)
    if (session) {
      await updateSessionById(sessionId, { ...session, pinned: true })
    }
  }

  async function unpinSession(sessionId) {
    const session = sessions.value.find(s => s.id === sessionId)
    if (session) {
      await updateSessionById(sessionId, { ...session, pinned: false })
    }
  }

  function clearError() {
    error.value = null
  }

  function reset() {
    sessions.value = []
    activeSessionId.value = null
    pinnedSessions.value = []
    recentSessions.value = []
    currentPage.value = 1
    totalPages.value = 1
    totalSessions.value = 0
    error.value = null
  }

  return {
    // State
    sessions,
    activeSessionId,
    loading,
    error,
    pinnedSessions,
    recentSessions,
    currentPage,
    totalPages,
    totalSessions,

    // Getters
    activeSession,
    sessionsList,
    isLoading,

    // Actions
    fetchSessions,
    createNewSession,
    fetchSessionById,
    updateSessionById,
    deleteSessionById,
    setActiveSession,
    addSession,
    removeSession,
    updateSessionInList,
    pinSession,
    unpinSession,
    clearError,
    reset,
  }
})