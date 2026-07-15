import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Transform response if needed
    return response.data
  },
  (error) => {
    // Handle errors
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response

      switch (status) {
        case 401:
          // Unauthorized - clear token and redirect to login
          localStorage.removeItem('auth_token')
          if (window.location.pathname !== '/login') {
            window.location.href = '/login'
          }
          break
        case 403:
          // Forbidden
          console.error('Access denied:', data)
          break
        case 404:
          // Not found
          console.error('Resource not found:', data)
          break
        case 500:
          // Server error
          console.error('Server error:', data)
          break
        default:
          console.error('API error:', data)
      }

      // Return a standardized error object
      return Promise.reject({
        status,
        message: data?.detail || data?.message || 'An error occurred',
        data,
      })
    } else if (error.request) {
      // Network error
      return Promise.reject({
        status: 0,
        message: 'Network error. Please check your connection.',
        data: null,
      })
    } else {
      // Other error
      return Promise.reject({
        status: 0,
        message: error.message || 'An unexpected error occurred',
        data: null,
      })
    }
  }
)

export default api