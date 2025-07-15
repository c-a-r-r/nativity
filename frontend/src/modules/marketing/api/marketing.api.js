import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor to add auth token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      // ADD DEBUG LOG
      console.log('Marketing API - Adding auth token:', token.substring(0, 10) + '...')
      console.log('Marketing API - Request URL:', config.url)
    } else {
      console.log('Marketing API - No auth token found')
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle common errors
api.interceptors.response.use(
  (response) => {
    console.log('Marketing API - Success response:', response.config.url, response.status)
    return response
  },
  (error) => {
    console.error('Marketing API - Error response:', error.config?.url, error.response?.status)
    console.error('Marketing API - Error details:', error.response?.data)
    
    if (error.response?.status === 401) {
      console.error('Authentication failed:', error.response.data)
      // Handle unauthorized access
      localStorage.removeItem('authToken')
      // Optionally redirect to login
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export { api }
export default api