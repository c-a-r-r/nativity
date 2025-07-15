<!-- filepath: /Users/cristian/Documents/nativity-crm/frontend/src/modules/marketing/pages/TripList.vue -->
<template>
  <div class="trip-list-page">
    <div class="container py-5">
      <div class="text-center mb-5">
        <h1 class="display-4">Available Pilgrimage Trips</h1>
        <p class="lead">Discover our upcoming spiritual journeys</p>
      </div>

      <div v-if="loading" class="text-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="trips.length === 0" class="text-center">
        <div class="alert alert-info">
          <h4>No trips available at this time</h4>
          <p>Please check back later for upcoming pilgrimage opportunities.</p>
        </div>
      </div>

      <div v-else class="row">
        <div 
          v-for="trip in trips" 
          :key="trip.id"
          class="col-lg-4 col-md-6 mb-4"
        >
          <div class="card trip-card h-100">
            <img 
              :src="trip.template?.hero_image || '/images/default-trip.jpg'" 
              :alt="trip.final_title"
              class="card-img-top"
              style="height: 200px; object-fit: cover;"
            >
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">{{ trip.final_title }}</h5>
              <p class="card-text text-muted small">{{ trip.church_name }}</p>
              <p class="card-text">{{ truncateText(trip.final_description, 100) }}</p>
              
              <div class="trip-details mb-3">
                <div class="row">
                  <div class="col-6">
                    <small class="text-muted">Departure:</small><br>
                    <small>{{ formatDate(trip.departure_date) }}</small>
                  </div>
                  <div class="col-6">
                    <small class="text-muted">Duration:</small><br>
                    <small>{{ trip.template?.duration_days }} days</small>
                  </div>
                </div>
              </div>

              <div class="mt-auto">
                <div class="d-flex justify-content-between align-items-center">
                  <span class="h5 text-primary mb-0">${{ trip.price }}</span>
                  <router-link 
                    :to="{ name: 'TripPublic', params: { slug: trip.slug } }"
                    class="btn btn-primary"
                  >
                    View Details
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api/marketing.api.js'

const trips = ref([])
const loading = ref(true)

const loadTrips = async () => {
  try {
    const response = await api.get('/marketing/trips/')
    trips.value = response.data.results || response.data
  } catch (error) {
    console.error('Error loading trips:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

onMounted(() => {
  loadTrips()
})
</script>

<style scoped>
.trip-card {
  transition: transform 0.2s ease-in-out;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.trip-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.trip-details {
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
  padding: 0.75rem 0;
}
</style>