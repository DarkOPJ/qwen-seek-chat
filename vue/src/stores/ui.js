import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const STORAGE_KEY = 'qwen-chat-ui-preferences'

export const useUIStore = defineStore('ui', () => {
  // State
  const sidebarOpen = ref(false)
  const theme = ref('dark') // 'dark' | 'light' | 'system'
  const toasts = ref([])
  const sidebarCollapsed = ref(false)
  const rightPanelOpen = ref(false)
  const commandPaletteOpen = ref(false)

  // Load preferences from localStorage
  function loadPreferences() {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        const prefs = JSON.parse(stored)
        if (prefs.sidebarOpen !== undefined) sidebarOpen.value = prefs.sidebarOpen
        if (prefs.sidebarCollapsed !== undefined) sidebarCollapsed.value = prefs.sidebarCollapsed
        if (prefs.theme) theme.value = prefs.theme
      }
    } catch (error) {
      console.error('Failed to load UI preferences:', error)
    }
  }

  // Save preferences to localStorage
  function savePreferences() {
    try {
      const prefs = {
        sidebarOpen: sidebarOpen.value,
        sidebarCollapsed: sidebarCollapsed.value,
        theme: theme.value,
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs))
    } catch (error) {
      console.error('Failed to save UI preferences:', error)
    }
  }

  // Watch for changes and persist
  watch([sidebarOpen, sidebarCollapsed, theme], savePreferences, { deep: true })

  // Toast management
  let toastId = 0

  function addToast(message, type = 'info', duration = 5000) {
    const id = ++toastId
    const toast = { id, message, type, duration }
    toasts.value.push(toast)

    if (duration > 0) {
      setTimeout(() => removeToast(id), duration)
    }

    return id
  }

  function removeToast(id) {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index !== -1) {
      toasts.value.splice(index, 1)
    }
  }

  function clearToasts() {
    toasts.value = []
  }

  // Sidebar actions
  function toggleSidebar() {
    sidebarOpen.value = !sidebarOpen.value
  }

  function setSidebarOpen(open) {
    sidebarOpen.value = open
  }

  function toggleSidebarCollapsed() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  function setSidebarCollapsed(collapsed) {
    sidebarCollapsed.value = collapsed
  }

  // Right panel
  function toggleRightPanel() {
    rightPanelOpen.value = !rightPanelOpen.value
  }

  function setRightPanelOpen(open) {
    rightPanelOpen.value = open
  }

  // Command palette
  function openCommandPalette() {
    commandPaletteOpen.value = true
  }

  function closeCommandPalette() {
    commandPaletteOpen.value = false
  }

  function toggleCommandPalette() {
    commandPaletteOpen.value = !commandPaletteOpen.value
  }

  // Theme
  function setTheme(newTheme) {
    theme.value = newTheme
    applyTheme(newTheme)
  }

  function toggleTheme() {
    const themes = ['dark', 'light']
    const currentIndex = themes.indexOf(theme.value)
    const nextIndex = (currentIndex + 1) % themes.length
    setTheme(themes[nextIndex])
  }

  function applyTheme(newTheme) {
    const html = document.documentElement
    if (newTheme === 'system') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      html.classList.toggle('dark', prefersDark)
    } else {
      html.classList.toggle('dark', newTheme === 'dark')
    }
  }

  // Initialize theme on load
  function initTheme() {
    applyTheme(theme.value)

    if (theme.value === 'system') {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        applyTheme('system')
      })
    }
  }

  // Load preferences on store creation
  loadPreferences()
  initTheme()

  return {
    // State
    sidebarOpen,
    sidebarCollapsed,
    theme,
    toasts,
    rightPanelOpen,
    commandPaletteOpen,

    // Getters (computed would be here if needed)

    // Actions
    loadPreferences,
    savePreferences,
    addToast,
    removeToast,
    clearToasts,
    toggleSidebar,
    setSidebarOpen,
    toggleSidebarCollapsed,
    setSidebarCollapsed,
    toggleRightPanel,
    setRightPanelOpen,
    openCommandPalette,
    closeCommandPalette,
    toggleCommandPalette,
    setTheme,
    toggleTheme,
    applyTheme,
    initTheme,
  }
})