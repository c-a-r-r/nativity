import http from '@/shared/services/http'

export default {
  // Main CRUD operations
  async list(params = {}) {
    const response = await http.get('/api/quotes/', { params })
    return response.data
  },

  async get(id) {
    const response = await http.get(`/api/quotes/${id}/`)
    return response.data
  },

  async create(data) {
    const response = await http.post('/api/quotes/', data, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return response.data
  },

  async update(id, data) {
    const response = await http.put(`/api/quotes/${id}/`, data, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return response.data
  },

  async delete(id) {
    const response = await http.delete(`/api/quotes/${id}/`)
    return response.data
  },

  // Support lookups used by components
  async searchContacts(search) {
    const response = await http.get('/api/contacts/', { 
      params: { search } 
    })
    return response.data.results || []
  },

  async getCities() {
    const response = await http.get('/api/itinerary-cities/')
    return response.data
  },

  async getDestGroups() {
    const response = await http.get('/api/destination-groups/')
    return response.data
  },

  async getDestinations() {
    const response = await http.get('/api/destinations/')
    return response.data
  }
}