import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { getModels, pullModel, checkModel } from '@/api/model'

const STORAGE_KEY = 'qwen-chat-selected-model'
const DEFAULT_MODEL = 'qwen3:1.7b'

export const useModelStore = defineStore('model', () => {
  // State
  const availableModels = ref([])
  const selectedModel = ref(null)
  const loading = ref(false)
  const pulling = ref({}) // modelName -> boolean
  const pullProgress = ref({}) // modelName -> { progress, status }

  // Initialize from localStorage
  function initSelectedModel() {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      selectedModel.value = stored
    } else {
      selectedModel.value = DEFAULT_MODEL
      localStorage.setItem(STORAGE_KEY, DEFAULT_MODEL)
    }
  }

  // Watch for changes and persist
  watch(selectedModel, (newModel) => {
    if (newModel) {
      localStorage.setItem(STORAGE_KEY, newModel)
    }
  })

  // Getters
  const isModelSelected = computed(() => !!selectedModel.value)

  const currentModel = computed(() => {
    if (!selectedModel.value) return null
    return availableModels.value.find(m => m.name === selectedModel.value) || { name: selectedModel.value }
  })

  const availableModelNames = computed(() => availableModels.value.map(m => m.name))

  const isPulling = computed(() => (modelName) => pulling.value[modelName] === true)

  const getPullProgress = computed(() => (modelName) => pullProgress.value[modelName] || { progress: 0, status: '' })

  // Actions
  async function fetchModels() {
    loading.value = true
    try {
      const response = await getModels()
      availableModels.value = response.data.models || response.data || []
      return availableModels.value
    } catch (error) {
      console.error('Failed to fetch models:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  function selectModel(modelName) {
    if (availableModelNames.value.includes(modelName) || !availableModels.value.length) {
      selectedModel.value = modelName
    } else {
      console.warn(`Model ${modelName} not in available models list`)
      selectedModel.value = modelName // Allow anyway
    }
  }

  async function pullModelByName(modelName) {
    pulling.value[modelName] = true
    pullProgress.value[modelName] = { progress: 0, status: 'starting' }

    try {
      // The pull endpoint might stream progress
      const response = await pullModel(modelName)

      // If streaming, we'd handle progress events here
      // For now, assume it returns when done
      pullProgress.value[modelName] = { progress: 100, status: 'complete' }

      // Refresh models list
      await fetchModels()

      return response.data
    } catch (error) {
      pullProgress.value[modelName] = { progress: 0, status: 'error', error: error.message }
      throw error
    } finally {
      pulling.value[modelName] = false
    }
  }

  async function checkModelAvailability(modelName) {
    try {
      const response = await checkModel(modelName)
      return response.data.available === true
    } catch {
      return false
    }
  }

  function setPullProgress(modelName, progress, status) {
    pullProgress.value[modelName] = { progress, status }
  }

  function reset() {
    availableModels.value = []
    selectedModel.value = DEFAULT_MODEL
    loading.value = false
    pulling.value = {}
    pullProgress.value = {}
    localStorage.setItem(STORAGE_KEY, DEFAULT_MODEL)
  }

  // Initialize on store creation
  initSelectedModel()

  return {
    // State
    availableModels,
    selectedModel,
    loading,
    pulling,
    pullProgress,

    // Getters
    isModelSelected,
    currentModel,
    availableModelNames,
    isPulling,
    getPullProgress,

    // Actions
    fetchModels,
    selectModel,
    pullModelByName,
    checkModelAvailability,
    setPullProgress,
    reset,
    initSelectedModel,
  }
})