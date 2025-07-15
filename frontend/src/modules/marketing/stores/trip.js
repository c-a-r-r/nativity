import { defineStore } from "pinia"
import axios from "axios"

export const useTripStore = defineStore("trip", {
  state: () => ({ 
    data: null, 
    loading: false, 
    error: null,
    templates: []
  }),
  
  actions: {
    async fetchPublic(slug) {
      this.loading = true
      this.error = null
      
      try {
        const { data } = await axios.get(`/api/trips/public/${slug}/`)
        this.data = data
      } catch (e) {
        this.error = e.response?.data?.message || 'Failed to load trip'
      } finally {
        this.loading = false
      }
    },
    
    async fetchPrivate(token) {
      this.loading = true
      this.error = null
      
      try {
        const { data } = await axios.get(`/api/trips/private/${token}/`)
        this.data = data
      } catch (e) {
        this.error = e.response?.data?.message || 'Failed to load trip'
      } finally {
        this.loading = false
      }
    },
    
    async loadTemplates(filters = {}) {
      try {
        const { data } = await axios.get('/api/trip-templates/', { params: filters })
        this.templates = data
        return data
      } catch (error) {
        console.error('Failed to load templates:', error)
        return []
      }
    }
  }
})