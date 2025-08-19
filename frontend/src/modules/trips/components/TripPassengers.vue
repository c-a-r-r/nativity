<template>
  <div class="trip-passengers">
    
    <!-- Section Header -->
    <div class="section-header">
      <h3>
        <i class="fas fa-users"></i>
        Passenger Management
      </h3>
      <div class="header-actions">
        <button @click="addPassenger" class="btn btn-success">
          <i class="fas fa-user-plus"></i>
          Add Passenger
        </button>
        <button @click="exportPassengers" class="btn btn-primary">
          <i class="fas fa-download"></i>
          Export List
        </button>
      </div>
    </div>

    <!-- Stats Summary -->
    <div class="stats-summary">
      <div class="stat-item">
        <span class="stat-label">Total Registered:</span>
        <span class="stat-value">{{ passengerStats.registered }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Total Paid:</span>
        <span class="stat-value">${{ formatCurrency(passengerStats.totalPaid) }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Total Due:</span>
        <span class="stat-value">${{ formatCurrency(passengerStats.totalDue) }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Outstanding:</span>
        <span class="stat-value outstanding">${{ formatCurrency(passengerStats.totalDue - passengerStats.totalPaid) }}</span>
      </div>
    </div>

    <!-- Search and Filters -->
    <div class="controls-section">
      <div class="search-box">
        <i class="fas fa-search"></i>
        <input 
          v-model="searchTerm"
          type="text"
          placeholder="Search passengers..."
          @input="filterPassengers"
        >
      </div>
      <div class="filter-controls">
        <select v-model="paymentFilter" @change="filterPassengers" class="form-select">
          <option value="">All Payment Status</option>
          <option value="paid-in-full">Paid in Full</option>
          <option value="partial-payment">Partial Payment</option>
          <option value="no-payment">No Payment</option>
        </select>
        <select v-model="roomingFilter" @change="filterPassengers" class="form-select">
          <option value="">All Rooming</option>
          <option value="assigned">Room Assigned</option>
          <option value="unassigned">No Room Assignment</option>
        </select>
      </div>
    </div>

    <!-- Passengers Table -->
    <div class="passengers-table-container">
      <div v-if="loading" class="loading-state">
        <i class="fas fa-spinner fa-spin"></i>
        Loading passengers...
      </div>
      
      <div v-else-if="filteredPassengers.length === 0" class="empty-state">
        <i class="fas fa-users-slash"></i>
        <h4>No Passengers Found</h4>
        <p>{{ searchTerm ? 'No passengers match your search criteria.' : 'No passengers registered for this trip yet.' }}</p>
        <button @click="addPassenger" class="btn btn-primary">
          <i class="fas fa-user-plus"></i>
          Add First Passenger
        </button>
      </div>

      <div v-else class="table-responsive">
        <table class="passengers-table">
          <thead>
            <tr>
              <th>Passenger Name</th>
              <th>Contact Info</th>
              <th>Payment Status</th>
              <th>Amount Due</th>
              <th>Amount Paid</th>
              <th>Outstanding</th>
              <th>Rooming</th>
              <th>Special Needs</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="passenger in paginatedPassengers" 
              :key="passenger.id"
              class="passenger-row"
              :class="{ 'payment-overdue': isPaymentOverdue(passenger) }"
            >
              <td class="passenger-name">
                <div class="name-info">
                  <strong>{{ passenger.passenger_name }}</strong>
                  <small>{{ passenger.passenger_details }}</small>
                </div>
              </td>
              
              <td class="contact-info">
                <div class="contact-details">
                  <div class="email">{{ passenger.email }}</div>
                  <div class="phone">{{ passenger.phone }}</div>
                </div>
              </td>
              
              <td class="payment-status">
                <span class="status-badge" :class="getPaymentStatusClass(passenger.payment_status)">
                  {{ passenger.payment_status }}
                </span>
              </td>
              
              <td class="amount-due">
                <span class="amount">${{ formatCurrency(passenger.amount_due) }}</span>
              </td>
              
              <td class="amount-paid">
                <span class="amount paid">${{ formatCurrency(passenger.amount_received) }}</span>
              </td>
              
              <td class="outstanding">
                <span class="amount" :class="{ 'overdue': passenger.amount_due - passenger.amount_received > 0 }">
                  ${{ formatCurrency(passenger.amount_due - passenger.amount_received) }}
                </span>
              </td>
              
              <td class="rooming">
                <span v-if="passenger.rooming_with" class="rooming-info">
                  <i class="fas fa-bed"></i>
                  {{ passenger.rooming_with }}
                </span>
                <span v-else class="no-rooming">
                  <i class="fas fa-bed text-muted"></i>
                  Not assigned
                </span>
              </td>
              
              <td class="special-needs">
                <div v-if="hasSpecialNeeds(passenger)" class="needs-list">
                  <span v-if="passenger.dietary_restrictions" class="need-item dietary">
                    <i class="fas fa-utensils"></i>
                    {{ passenger.dietary_restrictions }}
                  </span>
                  <span v-if="passenger.medical_conditions" class="need-item medical">
                    <i class="fas fa-heartbeat"></i>
                    {{ passenger.medical_conditions }}
                  </span>
                  <span v-if="passenger.special_requests" class="need-item special">
                    <i class="fas fa-star"></i>
                    {{ passenger.special_requests }}
                  </span>
                </div>
                <span v-else class="no-needs">
                  <i class="fas fa-check-circle text-success"></i>
                  None
                </span>
              </td>
              
              <td class="actions">
                <div class="action-buttons">
                  <button @click="editPassenger(passenger)" class="btn-action edit" title="Edit Passenger">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button @click="recordPayment(passenger)" class="btn-action payment" title="Record Payment">
                    <i class="fas fa-dollar-sign"></i>
                  </button>
                  <button @click="assignRoom(passenger)" class="btn-action room" title="Assign Room">
                    <i class="fas fa-bed"></i>
                  </button>
                  <button @click="viewDetails(passenger)" class="btn-action view" title="View Details">
                    <i class="fas fa-eye"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination-wrapper">
        <div class="pagination-info">
          Showing {{ (currentPage - 1) * pageSize + 1 }} to {{ Math.min(currentPage * pageSize, filteredPassengers.length) }} 
          of {{ filteredPassengers.length }} passengers
        </div>
        <div class="pagination-controls">
          <button 
            @click="currentPage--" 
            :disabled="currentPage === 1"
            class="btn btn-pagination"
          >
            <i class="fas fa-chevron-left"></i>
          </button>
          <span class="page-numbers">
            <button 
              v-for="page in visiblePages" 
              :key="page"
              @click="currentPage = page"
              :class="['btn', 'btn-page', { active: currentPage === page }]"
            >
              {{ page }}
            </button>
          </span>
          <button 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
            class="btn btn-pagination"
          >
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// Props
const props = defineProps({
  tripId: {
    type: [String, Number],
    required: true
  },
  passengerStats: {
    type: Object,
    default: () => ({
      registered: 0,
      totalPaid: 0,
      totalDue: 0
    })
  }
})

// Emits
const emit = defineEmits(['update-stats'])

// State
const loading = ref(true)
const passengers = ref([])
const filteredPassengers = ref([])
const searchTerm = ref('')
const paymentFilter = ref('')
const roomingFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// Computed
const totalPages = computed(() => Math.ceil(filteredPassengers.value.length / pageSize.value))

const paginatedPassengers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredPassengers.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages.value, start + maxVisible - 1)
  
  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

// Methods
const fetchPassengers = async () => {
  try {
    loading.value = true
    const response = await axios.get(`/api/trips/${props.tripId}/passengers/`)
    passengers.value = response.data.results || response.data || []
    filterPassengers()
    
    // Update stats
    updateStats()
    
  } catch (error) {
    console.error('Error fetching passengers:', error)
    passengers.value = []
  } finally {
    loading.value = false
  }
}

const filterPassengers = () => {
  let filtered = [...passengers.value]
  
  // Search filter
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    filtered = filtered.filter(passenger => 
      passenger.passenger_name.toLowerCase().includes(term) ||
      passenger.email.toLowerCase().includes(term) ||
      passenger.phone.includes(term)
    )
  }
  
  // Payment status filter
  if (paymentFilter.value) {
    filtered = filtered.filter(passenger => {
      const status = passenger.payment_status.toLowerCase().replace(' ', '-')
      return status === paymentFilter.value
    })
  }
  
  // Rooming filter
  if (roomingFilter.value) {
    filtered = filtered.filter(passenger => {
      if (roomingFilter.value === 'assigned') {
        return passenger.rooming_with && passenger.rooming_with.trim() !== ''
      } else {
        return !passenger.rooming_with || passenger.rooming_with.trim() === ''
      }
    })
  }
  
  filteredPassengers.value = filtered
  currentPage.value = 1
}

const updateStats = () => {
  const stats = {
    registered: passengers.value.length,
    totalPaid: passengers.value.reduce((sum, p) => sum + (parseFloat(p.amount_received) || 0), 0),
    totalDue: passengers.value.reduce((sum, p) => sum + (parseFloat(p.amount_due) || 0), 0)
  }
  
  emit('update-stats', stats)
}

const formatCurrency = (amount) => {
  return parseFloat(amount || 0).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const getPaymentStatusClass = (status) => {
  if (!status) return ''
  const statusLower = status.toLowerCase().replace(' ', '-')
  return `payment-${statusLower}`
}

const isPaymentOverdue = (passenger) => {
  // Logic to determine if payment is overdue
  const outstanding = (passenger.amount_due || 0) - (passenger.amount_received || 0)
  return outstanding > 0 && passenger.payment_status !== 'Paid in Full'
}

const hasSpecialNeeds = (passenger) => {
  return passenger.dietary_restrictions || passenger.medical_conditions || passenger.special_requests
}

// Action methods
const addPassenger = () => {
  console.log('Add new passenger')
  // Navigate to passenger form or open modal
}

const editPassenger = (passenger) => {
  console.log('Edit passenger:', passenger.id)
  // Navigate to edit form or open modal
}

const recordPayment = (passenger) => {
  console.log('Record payment for:', passenger.id)
  // Open payment recording modal
}

const assignRoom = (passenger) => {
  console.log('Assign room for:', passenger.id)
  // Open room assignment modal
}

const viewDetails = (passenger) => {
  console.log('View details for:', passenger.id)
  // Open passenger details modal
}

const exportPassengers = () => {
  console.log('Export passenger list')
  // Generate Excel or PDF export
}

// Lifecycle
onMounted(() => {
  fetchPassengers()
})
</script>

<style scoped>
.trip-passengers {
  padding: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f8f9fa;
}

.section-header h3 {
  margin: 0;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-header i {
  color: #667eea;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
  font-weight: 500;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
}

.stat-value.outstanding {
  color: #dc3545;
}

.controls-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 20px;
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 400px;
}

.search-box i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #7f8c8d;
}

.search-box input {
  width: 100%;
  padding: 10px 12px 10px 40px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 14px;
}

.search-box input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-controls {
  display: flex;
  gap: 12px;
}

.form-select {
  padding: 8px 12px;
  border: 2px solid #e9ecef;
  border-radius: 6px;
  background: white;
  font-size: 14px;
}

.form-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.passengers-table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.loading-state i {
  font-size: 32px;
  margin-bottom: 16px;
}

.empty-state i {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-state h4 {
  margin: 0 0 12px 0;
  color: #2c3e50;
}

.empty-state p {
  margin: 0 0 24px 0;
  font-size: 16px;
}

.passengers-table {
  width: 100%;
  border-collapse: collapse;
}

.passengers-table th {
  background: #f8f9fa;
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e9ecef;
  font-size: 14px;
}

.passengers-table td {
  padding: 16px 12px;
  border-bottom: 1px solid #f1f3f4;
  vertical-align: middle;
}

.passenger-row {
  transition: background-color 0.2s ease;
}

.passenger-row:hover {
  background-color: #f8f9fa;
}

.passenger-row.payment-overdue {
  background: linear-gradient(90deg, #fff5f5 0%, #ffffff 100%);
}

.name-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.name-info strong {
  color: #2c3e50;
  font-size: 15px;
}

.name-info small {
  color: #7f8c8d;
  font-size: 12px;
}

.contact-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.contact-details .email {
  color: #2c3e50;
  font-size: 14px;
}

.contact-details .phone {
  color: #7f8c8d;
  font-size: 13px;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.payment-paid-in-full {
  background: #d4edda;
  color: #155724;
}

.payment-partial-payment {
  background: #fff3cd;
  color: #856404;
}

.payment-no-payment {
  background: #f8d7da;
  color: #721c24;
}

.amount {
  font-weight: 600;
  color: #2c3e50;
}

.amount.paid {
  color: #28a745;
}

.amount.overdue {
  color: #dc3545;
}

.rooming-info {
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 6px;
}

.no-rooming {
  color: #7f8c8d;
  display: flex;
  align-items: center;
  gap: 6px;
}

.needs-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.need-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 12px;
}

.need-item.dietary {
  background: #fff3cd;
  color: #856404;
}

.need-item.medical {
  background: #f8d7da;
  color: #721c24;
}

.need-item.special {
  background: #d1ecf1;
  color: #0c5460;
}

.no-needs {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #28a745;
}

.action-buttons {
  display: flex;
  gap: 6px;
}

.btn-action {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  font-size: 12px;
}

.btn-action.edit {
  background: #ffc107;
  color: #212529;
}

.btn-action.payment {
  background: #28a745;
  color: white;
}

.btn-action.room {
  background: #17a2b8;
  color: white;
}

.btn-action.view {
  background: #007bff;
  color: white;
}

.btn-action:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.pagination-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.pagination-info {
  color: #7f8c8d;
  font-size: 14px;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-pagination,
.btn-page {
  padding: 8px 12px;
  border: 1px solid #e9ecef;
  background: white;
  color: #2c3e50;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.btn-pagination:hover,
.btn-page:hover {
  background: #f8f9fa;
  border-color: #667eea;
}

.btn-page.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.btn-pagination:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

/* Button Styles */
.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #218838;
  transform: translateY(-1px);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .passengers-table {
    font-size: 13px;
  }
  
  .passengers-table th,
  .passengers-table td {
    padding: 12px 8px;
  }
}

@media (max-width: 768px) {
  .trip-passengers {
    padding: 20px;
  }
  
  .section-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .controls-section {
    flex-direction: column;
    gap: 16px;
  }
  
  .filter-controls {
    flex-direction: column;
    gap: 8px;
  }
  
  .stats-summary {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .passengers-table-container {
    overflow-x: auto;
  }
  
  .passengers-table {
    min-width: 1000px;
  }
  
  .pagination-wrapper {
    flex-direction: column;
    gap: 16px;
  }
}

@media (max-width: 576px) {
  .stats-summary {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 4px;
  }
  
  .btn-action {
    width: 28px;
    height: 28px;
    font-size: 10px;
  }
}
</style>
