<template>
  <div class="trip-management-wrapper">
    
    <!-- Notification System -->
    <div class="notification-container">
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        :class="['notification', `notification-${notification.type}`]"
      >
        <div class="notification-content">
          <span class="notification-message">{{ notification.message }}</span>
          <button 
            @click="removeNotification(notification.id)"
            class="notification-close"
          >
            ×
          </button>
        </div>
      </div>
    </div>
    
    <!-- Header Section -->
    <div class="management-header">
      <div class="header-left">
        <button @click="goBack" class="back-btn">
          <i class="fas fa-arrow-left"></i>
          Back to Trips
        </button>
        <div class="trip-info">
          <h2 class="trip-title">
            <i class="fas fa-plane-departure"></i>
            {{ tripData?.trip_name || 'Loading...' }}
          </h2>
          <div class="trip-meta" v-if="tripData">
            <span class="meta-item">
              <i class="fas fa-user"></i>
              {{ tripData.client_name }}
            </span>
            <span class="meta-item">
              <i class="fas fa-church"></i>
              {{ tripData.church_name || 'N/A' }}
            </span>
            <span class="meta-item">
              <i class="fas fa-calendar"></i>
              {{ formatDate(tripData.departure_date) }}
            </span>
          </div>
        </div>
      </div>
      <div class="header-right">
        <span class="trip-status" :class="getStatusClass(tripData?.quote_status?.nombre || tripData?.workflow_status_nombre)">
          {{ tripData?.quote_status?.nombre || tripData?.workflow_status_nombre }}
        </span>
        <div class="trip-id">{{ formatTripId(tripData?.id) }}</div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="quick-stats-grid" v-if="tripData">
      <div class="stat-card passengers">
        <div class="stat-icon">
          <i class="fas fa-users"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ passengerStats.registered }}</div>
          <div class="stat-label">Passenger Count</div>
        </div>
      </div>
      
      <div class="stat-card commission">
        <div class="stat-icon">
          <i class="fas fa-percentage"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">${{ formatCurrency(calculateCommission()) }}</div>
          <div class="stat-label">Commission</div>
        </div>
      </div>
      
      <div class="stat-card amount-due">
        <div class="stat-icon">
          <i class="fas fa-dollar-sign"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">${{ formatCurrency(calculateAmountDue()) }}</div>
          <div class="stat-label">Amount Due</div>
        </div>
      </div>
      
      <div class="stat-card amount-received">
        <div class="stat-icon">
          <i class="fas fa-money-bill-wave"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">${{ formatCurrency(passengerStats.totalPaid) }}</div>
          <div class="stat-label">Amount Received</div>
        </div>
      </div>
      
      <div class="stat-card total-due">
        <div class="stat-icon">
          <i class="fas fa-balance-scale"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">${{ formatCurrency(calculateTotalDue()) }}</div>
          <div class="stat-label">Total Due</div>
        </div>
      </div>

      <div class="stat-card final-payment">
        <div class="stat-icon">
          <i class="fas fa-calendar-check"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ formatDate(tripData.full_payment_date) }}</div>
          <div class="stat-label">Final Payment Due</div>
        </div>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="tab-navigation">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
      >
        <i :class="tab.icon"></i>
        {{ tab.label }}
        <span v-if="tab.count !== undefined" class="tab-count">{{ tab.count }}</span>
      </button>
    </div>

    <!-- Tab Content -->
    <div class="tab-content-wrapper">
      
      <!-- Tab 1: Quote -->
      <div v-if="activeTab === 'quote'" class="tab-content quote-tab">
        <TripQuote 
          :trip-data="tripData"
          @update-trip="updateTripData"
        />
      </div>

      <!-- Tab 2: Note -->
      <div v-if="activeTab === 'note'" class="tab-content note-tab">
        <TripNote 
          :trip-id="tripId"
          :comments="comments.notes"
          @add-comment="addComment"
        />
      </div>

      <!-- Tab 3: Customer Registration -->
      <div v-if="activeTab === 'customer-registration'" class="tab-content customer-registration-tab">
        <TripCustomerRegistration 
          :trip-id="tripId"
          :trip-data="tripData"
          :passenger-stats="passengerStats"
          @update-stats="updatePassengerStats"
          @send-email="sendEmail"
        />
      </div>

      <!-- Tab 4: Customer Waiting List -->
      <div v-if="activeTab === 'customer-waiting-list'" class="tab-content customer-waiting-list-tab">
        <TripCustomerWaitingList 
          :trip-id="tripId"
          :passenger-stats="passengerStats"
          @update-stats="updatePassengerStats"
        />
      </div>

      <!-- Tab 5: Air -->
      <div v-if="activeTab === 'air'" class="tab-content air-tab">
        <TripAir 
          :trip-id="tripId"
          :trip-data="tripData"
          @update-trip="updateTripData"
        />
      </div>

      <!-- Tab 6: Land -->
      <div v-if="activeTab === 'land'" class="tab-content land-tab">
        <TripLand 
          :trip-id="tripId"
          :trip-data="tripData"
          @update-trip="updateTripData"
        />
      </div>

    </div>

    <!-- Loading Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Loading trip data...</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

// Import tab components
import TripQuote from '../components/TripQuote.vue'
import TripNote from '../components/TripNote.vue'
import TripCustomerRegistration from '../components/TripCustomerRegistration.vue'
import TripCustomerWaitingList from '../components/TripCustomerWaitingList.vue'
import TripAir from '../components/TripAir.vue'
import TripLand from '../components/TripLand.vue'

const route = useRoute()
const router = useRouter()

// State
const loading = ref(true)
const activeTab = ref('quote')
const tripId = ref(route.params.id)
const tripData = ref(null)

const passengerStats = reactive({
  registered: 0,
  waiting: 0,
  totalPaid: 0,
  totalDue: 0
})

// Comments system
const comments = reactive({
  notes: [],
  air: [],
  land: []
})

// Tab configuration (matching pilgrimage.php interface from screenshots)
const tabs = computed(() => [
  {
    id: 'quote',
    label: 'Quote',
    icon: 'fas fa-file-invoice-dollar'
  },
  {
    id: 'note',
    label: 'Note',
    icon: 'fas fa-sticky-note'
  },
  {
    id: 'customer-registration',
    label: 'Customer Registration',
    icon: 'fas fa-user-plus',
    count: passengerStats.registered
  },
  {
    id: 'customer-waiting-list',
    label: 'Customer Waiting List',
    icon: 'fas fa-users',
    count: passengerStats.waiting
  },
  {
    id: 'air',
    label: 'Air',
    icon: 'fas fa-plane'
  },
  {
    id: 'land',
    label: 'Land',
    icon: 'fas fa-bus'
  }
])

// Methods
const fetchTripData = async () => {
  try {
    loading.value = true
    
    // Fetch main trip data
    const tripResponse = await axios.get(`/api/quotes/${tripId.value}/`)
    tripData.value = tripResponse.data
    
    // Fetch comments for all stages
    await fetchComments()
    
    // Fetch passenger statistics
    await fetchPassengerStats()
    
  } catch (error) {
    console.error('Error fetching trip data:', error)
    // Handle error - maybe redirect or show error message
  } finally {
    loading.value = false
  }
}

const fetchComments = async () => {
  try {
    // Fetch comments for pilgrimage stages (based on pilgrimage.php stage_id system)
    // Stage 1: Proposal/Quote Stage
    // Stage 2: Customer Registration/Hotels Stage  
    // Stage 3: Passenger Management Stage
    // Stage 4: Completion/Air Stage
    const [stageOneComments, stageTwoComments, stageThreeComments, stageFourComments] = await Promise.all([
      axios.get(`/api/trips/${tripId.value}/comments/?stage=1`), // Quote/Proposal stage
      axios.get(`/api/trips/${tripId.value}/comments/?stage=2`), // Customer Registration stage
      axios.get(`/api/trips/${tripId.value}/comments/?stage=3`), // Passenger Management stage
      axios.get(`/api/trips/${tripId.value}/comments/?stage=4`)  // Air/Completion stage
    ])
    
    comments.notes = stageOneComments.data.results || []
    comments.air = stageFourComments.data.results || []
    comments.land = stageTwoComments.data.results || []
    
  } catch (error) {
    console.error('Error fetching comments:', error)
  }
}

const fetchPassengerStats = async () => {
  try {
    const response = await axios.get(`/api/trips/${tripId.value}/passenger-stats/`)
    Object.assign(passengerStats, response.data)
  } catch (error) {
    console.error('Error fetching passenger stats:', error)
  }
}

const updateTripData = (updatedData) => {
  tripData.value = { ...tripData.value, ...updatedData }
}

const updatePassengerStats = (updatedStats) => {
  Object.assign(passengerStats, updatedStats)
}

const addComment = async (stage, comment) => {
  try {
    // Add comment with pilgrimage stage_id (based on pilgrimage.php comment system)
    const stageMapping = {
      'quote': 1,     // Quote/Proposal stage
      'notes': 1,     // Notes also map to proposal stage
      'customer-registration': 2, // Customer Registration stage
      'customer-waiting-list': 2, // Waiting list comments map to registration stage
      'air': 4,       // Air/Flight stage
      'land': 2       // Land/Hotels stage
    }
    
    const response = await axios.post(`/api/trips/${tripId.value}/comments/`, {
      content: comment,
      stage_id: stageMapping[stage] || 1,
      user_id: 1, // Current user ID
      created_at: new Date().toISOString()
    })
    
    // Update local comments array
    if (stage === 'notes' || stage === 'quote') {
      comments.notes.push(response.data)
    } else if (stage === 'air') {
      comments.air.push(response.data)
    } else if (stage === 'land' || stage === 'customer-registration' || stage === 'customer-waiting-list') {
      comments.land.push(response.data)
    }
    
    await fetchComments() // Refresh comments
    
  } catch (error) {
    console.error('Error adding comment:', error)
  }
}

const sendEmail = async (emailType) => {
  try {
    // Send pilgrimage email based on 7-stage email campaign system
    // Email campaign stages: mail_sent1 through mail_sent6 + confirmation
    const emailMapping = {
      'confirmation': 'confirmation',     // Initial confirmation email
      'first_followup': 'mail1',         // First follow-up (mail_sent1)
      'second_followup': 'mail2',        // Second follow-up (mail_sent2) 
      'third_followup': 'mail3',         // Third follow-up (mail_sent3)
      'fourth_followup': 'mail4',        // Fourth follow-up (mail_sent4)
      'fifth_followup': 'mail5',         // Fifth follow-up (mail_sent5)
      'final_notice': 'mail6'           // Final notice (mail_sent6)
    }
    
    const response = await axios.post(`/api/trips/${tripId.value}/send-email/`, {
      email_type: emailMapping[emailType] || 'confirmation',
      trip_id: tripId.value,
      timestamp: new Date().toISOString()
    })
    
    // Update trip data to reflect email sent
    if (response.data.success) {
      const emailField = `mail_sent${emailMapping[emailType].replace('mail', '')}`
      if (emailField !== 'mail_sentconfirmation') {
        tripData.value[emailField] = new Date().toISOString()
      }
      
      showNotification('Email sent successfully', 'success')
      await fetchTripData() // Refresh trip data
    }
    
  } catch (error) {
    console.error('Error sending email:', error)
    showNotification('Failed to send email', 'error')
  }
}

const calculateCommission = () => {
  // Commission calculation per passenger (from pilgrimage.php logic)
  // $amount_commision = $row["comision_usuario"] * $total_pasajeros;
  if (!tripData.value) return 0
  const commissionPerPassenger = tripData.value.comision_usuario || 0
  const totalPassengers = passengerStats.registered || 0
  return commissionPerPassenger * totalPassengers
}

const calculateAmountDue = () => {
  // Amount Due = Total trip cost for all passengers (from pilgrimage.php)
  // $amount_due = $row["total_cost"] * $total_pasajeros;
  if (!tripData.value) return 0
  const costPerPerson = tripData.value.total_cost || 0
  const totalPassengers = passengerStats.registered || 0
  return costPerPerson * totalPassengers
}

const calculateTotalDue = () => {
  // Total Due = Outstanding balance (Amount Due - Amount Received)
  // $amount_total = $amount_due - $amount_received;
  return calculateAmountDue() - (passengerStats.totalPaid || 0)
}

const calculateBalance = () => {
  // Legacy method - keeping for backward compatibility
  return calculateTotalDue()
}

const formatTripId = (id) => {
  // Format trip ID to match pilgrimage system
  if (!id) return ''
  return `PILGRIMAGE-${id}`
}

const getStatusClass = (status) => {
  if (!status) return ''
  const statusLower = status.toLowerCase()
  if (statusLower.includes('accepted')) return 'status-accepted'
  if (statusLower.includes('completed')) return 'status-completed'
  if (statusLower.includes('draft')) return 'status-draft'
  return 'status-default'
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatCurrency = (amount) => {
  return parseFloat(amount || 0).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const goBack = () => {
  router.push('/trips')
}

// Notification system matching pilgrimage.php feedback system
const notifications = ref([])

const showNotification = (message, type = 'info') => {
  const notification = {
    id: Date.now(),
    message,
    type, // success, error, warning, info
    timestamp: new Date().toISOString(),
    duration: type === 'error' ? 5000 : 3000 // Errors stay longer
  }
  
  notifications.value.push(notification)
  
  // Auto-remove notification after duration
  setTimeout(() => {
    const index = notifications.value.findIndex(n => n.id === notification.id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }, notification.duration)
}

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

// Lifecycle
onMounted(() => {
  fetchTripData()
})
</script>

<style scoped>
/* Notification System */
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  max-width: 400px;
}

.notification {
  margin-bottom: 10px;
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: slideInRight 0.3s ease-out;
  transition: all 0.3s ease;
}

.notification-success {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
}

.notification-error {
  background: linear-gradient(135deg, #dc3545, #e74c3c);
  color: white;
}

.notification-warning {
  background: linear-gradient(135deg, #ffc107, #fd7e14);
  color: #212529;
}

.notification-info {
  background: linear-gradient(135deg, #17a2b8, #007bff);
  color: white;
}

.notification-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notification-message {
  font-weight: 500;
  font-size: 14px;
}

.notification-close {
  background: none;
  border: none;
  color: inherit;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  padding: 0;
  margin-left: 15px;
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.notification-close:hover {
  opacity: 1;
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Main styles */
.trip-management-wrapper {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.management-header {
  background: white;
  padding: 20px 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-btn {
  padding: 10px 16px;
  border: 2px solid #6c757d;
  background: white;
  color: #6c757d;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.back-btn:hover {
  background: #6c757d;
  color: white;
  transform: translateY(-2px);
}

.trip-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.trip-title {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.trip-title i {
  color: #667eea;
}

.trip-meta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #7f8c8d;
  font-size: 14px;
}

.meta-item i {
  color: #667eea;
}

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.trip-status {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-accepted {
  background: #d4edda;
  color: #155724;
}

.status-completed {
  background: #cce5ff;
  color: #004085;
}

.status-draft {
  background: #fff3cd;
  color: #856404;
}

.status-default {
  background: #f8f9fa;
  color: #6c757d;
}

.trip-id {
  font-size: 18px;
  font-weight: bold;
  color: #667eea;
}

.quick-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  padding: 14px 18px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 14px;
  transition: transform 0.3s ease;
  min-height: 70px;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
  flex-shrink: 0;
}

.stat-card.passengers .stat-icon {
  background: linear-gradient(135deg, #28a745, #20c997);
}

.stat-card.commission .stat-icon {
  background: linear-gradient(135deg, #6f42c1, #6610f2);
}

.stat-card.amount-due .stat-icon {
  background: linear-gradient(135deg, #fd7e14, #e83e8c);
}

.stat-card.amount-received .stat-icon {
  background: linear-gradient(135deg, #007bff, #6610f2);
}

.stat-card.total-due .stat-icon {
  background: linear-gradient(135deg, #dc3545, #e83e8c);
}

.stat-card.final-payment .stat-icon {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 3px;
}

.stat-label {
  color: #7f8c8d;
  font-size: 13px;
  font-weight: 500;
}

.tab-navigation {
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
  padding: 8px;
  display: flex;
  gap: 4px;
  overflow-x: auto;
}

.tab-btn {
  padding: 12px 20px;
  border: none;
  background: transparent;
  color: #7f8c8d;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
  min-width: fit-content;
}

.tab-btn:hover {
  background: #f8f9fa;
  color: #2c3e50;
}

.tab-btn.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
}

.tab-count {
  background: rgba(255, 255, 255, 0.3);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  min-width: 20px;
  text-align: center;
}

.tab-btn.active .tab-count {
  background: rgba(255, 255, 255, 0.3);
}

.tab-btn:not(.active) .tab-count {
  background: #667eea;
  color: white;
}

.tab-content-wrapper {
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.tab-content {
  min-height: 500px;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-spinner {
  background: white;
  padding: 40px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.loading-spinner i {
  font-size: 32px;
  color: #667eea;
  margin-bottom: 16px;
}

.loading-spinner p {
  margin: 0;
  color: #7f8c8d;
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 768px) {
  .trip-management-wrapper {
    padding: 10px;
  }
  
  .management-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .header-left {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .trip-meta {
    flex-direction: column;
    gap: 8px;
  }
  
  .quick-stats-grid {
    grid-template-columns: 1fr;
  }
  
  .tab-navigation {
    overflow-x: auto;
  }
  
  .trip-title {
    font-size: 20px;
  }
}

@media (max-width: 576px) {
  .stat-card {
    padding: 10px 12px;
  }
  
  .stat-icon {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }
  
  .stat-value {
    font-size: 16px;
  }
  
  .tab-btn {
    padding: 10px 16px;
    font-size: 13px;
  }
}
</style>
