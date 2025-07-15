<!-- filepath: /Users/cristian/Documents/nativity-crm/frontend/src/modules/marketing/pages/TripPrivate.vue -->
<template>
  <div class="trip-private-view">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading trip...</span>
      </div>
    </div>
    
    <div v-else-if="trip" class="trip-content">
      <div class="alert alert-info mb-4">
        <i class="fas fa-lock me-2"></i>
        This is a private view of your trip details.
      </div>
      
      <div class="hero-section mb-5">
        <h1>{{ trip.trip_title }}</h1>
        <h2 class="text-muted">{{ trip.destination }}</h2>
        <p class="lead">{{ trip.duration_days }} Days with {{ trip.church_name }}</p>
        <span class="badge bg-warning">Private Access</span>
      </div>
      
      <div class="row">
        <div class="col-md-8">
          <div class="trip-description mb-4">
            <h3>Trip Description</h3>
            <p>{{ trip.trip_description }}</p>
          </div>
          
          <div class="trip-details mb-4">
            <h3>Trip Details</h3>
            <ul class="list-unstyled">
              <li><strong>Spiritual Director:</strong> {{ trip.spiritual_director }}</li>
              <li><strong>Departure Date:</strong> {{ formatDate(trip.departure_date) }}</li>
              <li><strong>Duration:</strong> {{ trip.duration_days }} days</li>
              <li><strong>Status:</strong> 
                <span :class="trip.is_published ? 'text-success' : 'text-warning'">
                  {{ trip.is_published ? 'Published' : 'Draft' }}
                </span>
              </li>
            </ul>
          </div>
          
          <!-- Private information -->
          <div class="private-info mb-4">
            <h3>Internal Information</h3>
            <div class="alert alert-secondary">
              <p><strong>Quote ID:</strong> {{ trip.quote_id }}</p>
              <p><strong>Created:</strong> {{ formatDate(trip.created_date) }}</p>
              <p class="mb-0"><strong>Last Updated:</strong> {{ formatDate(trip.updated_date) }}</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="price-card">
            <h3>Pricing Details</h3>
            <div class="price">${{ trip.price }}</div>
            <p class="text-muted">per person</p>
            
            <div class="actions mt-4">
              <a :href="`/trips/${trip.slug}`" target="_blank" class="btn btn-outline-primary btn-sm me-2">
                <i class="fas fa-eye me-1"></i>Public View
              </a>
              <button class="btn btn-outline-secondary btn-sm">
                <i class="fas fa-edit me-1"></i>Edit
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="alert alert-danger">
      Invalid access token or trip not found.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import http from '@/shared/services/http'

const route = useRoute()
const trip = ref(null)
const loading = ref(false)

const loadTrip = async () => {
  try {
    loading.value = true
    // Use the API endpoint for fetching trip data with private token
    const response = await http.get(`/api/marketing/trips/private/${route.params.token}/`)
    trip.value = response.data
  } catch (error) {
    console.error('Failed to load trip:', error)
    trip.value = null
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  if (!date) return 'TBD'
  return new Date(date).toLocaleDateString()
}

onMounted(() => {
  loadTrip()
})
</script>

<style scoped>
.trip-private-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.hero-section {
  text-align: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 2rem;
}

.price-card {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  position: sticky;
  top: 20px;
}

.price {
  font-size: 2.5rem;
  font-weight: bold;
  color: #28a745;
}

.private-info {
  background-color: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 1rem;
}
</style>