import api from './http'

export function getModels() {
  return api.get('/chat/api/v1/models')
}

export function getModel(name) {
  return api.get(`/chat/api/v1/models/${encodeURIComponent(name)}`)
}

export function pullModel(name, onProgress) {
  // Use streaming response for progress updates
  return api.post(
    `/chat/api/v1/models/${encodeURIComponent(name)}/pull`,
    {},
    {
      onDownloadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      },
      responseType: 'stream',
    }
  )
}

export function checkModel(name) {
  return api.get(`/chat/api/v1/models/${encodeURIComponent(name)}/check`)
}

export function deleteModel(name) {
  return api.delete(`/chat/api/v1/models/${encodeURIComponent(name)}`)
}