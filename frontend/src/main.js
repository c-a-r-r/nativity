// frontend/src/main.js

import { createApp } from 'vue'
import App          from './App.vue'
import router       from './router'          // your router/index.js

// --- Vuetify setup (if you’re using it) ---
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components  from 'vuetify/components'
import * as directives  from 'vuetify/directives'
const vuetify = createVuetify({ components, directives })

// --- Axios defaults (optional) ---
import axios from 'axios'
import './shared/styles/dashboard.css'
import '@/shared/styles/trip-template.css'
import '@fortawesome/fontawesome-free/css/all.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

axios.defaults.baseURL = 'http://localhost:8000'

axios.interceptors.request.use(config => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})



//refresh tokenaxios.interceptors.response.use(
let isRefreshing = false
let failedQueue = []

function processQueue(error, token = null) {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

axios.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // If token expired and we haven't already tried to refresh
    if (
      error.response &&
      error.response.status === 401 &&
      error.response.data &&
      error.response.data.detail &&
      error.response.data.detail.includes('Token is expired') &&
      !originalRequest._retry
    ) {
      if (isRefreshing) {
        // Queue the request until refresh is done
        return new Promise(function(resolve, reject) {
          failedQueue.push({ resolve, reject })
        })
          .then(token => {
            originalRequest.headers['Authorization'] = 'Bearer ' + token
            return axios(originalRequest)
          })
          .catch(err => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true
      const refresh = localStorage.getItem('refresh')
      try {
        const res = await axios.post('/api/auth/refresh/', { refresh })
        localStorage.setItem('access', res.data.access)
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + res.data.access
        processQueue(null, res.data.access)
        return axios(originalRequest)
      } catch (err) {
        processQueue(err, null)
        // Optionally, redirect to login
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        window.location.href = '/login'
        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

// --- mount the app ---
createApp(App)
  .use(router)
  .use(vuetify)          // comment out if you’re _not_ using Vuetify
  .mount('#app')