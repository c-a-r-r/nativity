import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000',
  // withCredentials: true,
})

// Add auth token to requests
http.interceptors.request.use(config => {
  const token = localStorage.getItem('access') || sessionStorage.getItem('access')  // ✅ Look for 'access'
  console.log(`🔑 HTTP Request: ${config.method?.toUpperCase()} ${config.url}`, {
    hasToken: !!token,
    token: token ? `${token.substring(0, 10)}...` : 'none'
  })
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle auth errors
http.interceptors.response.use(
  response => {
    console.log(`✅ HTTP Response: ${response.status} ${response.config.url}`)
    return response
  },
  error => {
    console.log(`❌ HTTP Error: ${error.response?.status} ${error.config?.url}`, error.response?.data)
    if (error.response?.status === 401) {
      localStorage.removeItem('access')     // ✅ Clear 'access'
      localStorage.removeItem('refresh')    // ✅ Clear 'refresh'
      sessionStorage.removeItem('access')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default http