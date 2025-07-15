<!-- filepath: /Users/cristian/Documents/nativity-crm/frontend/src/modules/marketing/pages/TripPublic.vue -->
<template>
  <div class="trip-public-view">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading trip...</span>
      </div>
    </div>
    
    <div v-else-if="trip" class="trip-content">
      <div class="hero-section mb-5">
        <h1>{{ trip.trip_title }}</h1>
        <h2 class="text-muted">{{ trip.destination }}</h2>
        <p class="lead">{{ trip.duration_days }} Days with {{ trip.church_name }}</p>
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
            </ul>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="price-card">
            <h3>Starting Price</h3>
            <div class="price">${{ trip.price }}</div>
            <p class="text-muted">per person</p>
            
            <div class="contact-info mt-4">
              <h5>Contact Us</h5>
              <p>For more information about this trip, please contact us.</p>
              <button class="btn btn-primary">Request Information</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="alert alert-warning">
      Trip not found or no longer available.
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
    // Use the API endpoint for fetching trip data
    const response = await http.get(`/api/marketing/trips/public/${route.params.slug}/`)
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
.trip-public-view {
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

.contact-info {
  border-top: 1px solid #ddd;
  padding-top: 1rem;
}
</style>