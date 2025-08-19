<template>
  <div class="customer-waiting-list-container">
    
    <!-- Action Buttons Section (Same as Customer Registration) -->
    <div class="action-buttons-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-users"></i>
          Customer Waiting List Management
        </h3>
        <div class="passenger-info">
          <span class="passenger-count">
            Maximum Passengers: <strong>{{ maxPassengers }}</strong>
          </span>
        </div>
      </div>

      <!-- Action Buttons Row -->
      <div class="action-buttons-grid">
        <button @click="openPassengerUrl" class="action-btn passenger-url">
          <i class="fas fa-external-link-alt"></i>
          Open Passenger URL
        </button>
        <button @click="processPayments" class="action-btn payments">
          <i class="fas fa-credit-card"></i>
          Payments
        </button>
        <button @click="managePassengerList" class="action-btn passenger-list">
          <i class="fas fa-list"></i>
          Passenger List
        </button>
        <button @click="generatePdf" class="action-btn pdf">
          <i class="fas fa-file-pdf"></i>
          PDF
        </button>
        <button @click="emailPtfAndEstimates" class="action-btn email-ptf">
          <i class="fas fa-envelope"></i>
          Email PTF and Estimates
        </button>
        <button @click="sendEmail" class="action-btn send-email">
          <i class="fas fa-paper-plane"></i>
          Send Email
        </button>
      </div>
    </div>

    <!-- Passenger List Section -->
    <div class="passenger-list-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-list"></i>
          Passenger List
        </h3>
        <div class="list-controls">
          <button @click="addNewPassenger" class="btn btn-primary">
            <i class="fas fa-plus"></i>
            New Passenger
          </button>
        </div>
      </div>

      <!-- List Controls -->
      <div class="list-controls-bar">
        <div class="display-control">
          <label>Displaying</label>
          <select v-model="displayCount" @change="updateDisplay" class="form-control">
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
          <span>records</span>
        </div>
        <div class="search-control">
          <label>Search:</label>
          <input 
            type="text" 
            v-model="searchQuery"
            @input="filterPassengers"
            class="form-control"
            placeholder="Search passengers..."
          >
        </div>
      </div>

      <!-- Passenger Table -->
      <div class="passenger-table-container">
        <table class="passenger-table">
          <thead>
            <tr>
              <th class="col-edit">Edit</th>
              <th class="col-select">
                <input 
                  type="checkbox" 
                  v-model="selectAll"
                  @change="toggleSelectAll"
                >
              </th>
              <th class="col-name">Name</th>
              <th class="col-phone">Phone</th>
              <th class="col-mobile">Mobile</th>
              <th class="col-email">Email</th>
              <th class="col-parent">Parent Name</th>
              <th class="col-book-id">Book ID</th>
              <th class="col-bunk">Bunk Type</th>
              <th class="col-passengers">Passengers Count</th>
              <th class="col-web">WEB</th>
              <th class="col-land">Land Only</th>
              <th class="col-visa">Visa</th>
              <th class="col-roommates">Roommates</th>
              <th class="col-insurance">Insurance</th>
              <th class="col-cancellation">Cancellation</th>
              <th class="col-remove">Remove?</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="passenger in paginatedPassengers" 
              :key="passenger.id"
              class="passenger-row"
              :class="getRowClass(passenger)"
            >
              <td class="col-edit">
                <button @click="editPassenger(passenger)" class="btn-icon edit">
                  <i class="fas fa-edit"></i>
                </button>
              </td>
              <td class="col-select">
                <input 
                  type="checkbox" 
                  v-model="selectedPassengers"
                  :value="passenger.id"
                >
              </td>
              <td class="col-name">
                <div class="passenger-name">
                  <span class="name-text">{{ passenger.name }}</span>
                  <div class="name-details">
                    <span v-if="passenger.book_type" class="book-type">{{ passenger.book_type }}</span>
                  </div>
                </div>
              </td>
              <td class="col-phone">{{ passenger.phone || '-' }}</td>
              <td class="col-mobile">{{ passenger.mobile || '-' }}</td>
              <td class="col-email">
                <a v-if="passenger.email" :href="`mailto:${passenger.email}`" class="email-link">
                  {{ passenger.email }}
                </a>
                <span v-else>-</span>
              </td>
              <td class="col-parent">{{ passenger.parent_name || '-' }}</td>
              <td class="col-book-id">{{ passenger.book_id || '-' }}</td>
              <td class="col-bunk">{{ passenger.bunk_type || '-' }}</td>
              <td class="col-passengers text-center">{{ passenger.passengers_count || 1 }}</td>
              <td class="col-web text-center">
                <span v-if="passenger.web_booking" class="status-indicator yes">Y</span>
                <span v-else class="status-indicator no">N</span>
              </td>
              <td class="col-land text-center">
                <span v-if="passenger.land_only" class="status-indicator yes">Y</span>
                <span v-else class="status-indicator no">N</span>
              </td>
              <td class="col-visa text-center">
                <span v-if="passenger.visa_required" class="status-indicator yes">Y</span>
                <span v-else class="status-indicator no">N</span>
              </td>
              <td class="col-roommates">{{ passenger.roommates || '-' }}</td>
              <td class="col-insurance">
                <span class="insurance-amount">{{ formatCurrency(passenger.insurance_amount) }}</span>
              </td>
              <td class="col-cancellation text-center">
                <span v-if="passenger.cancellation_protection" class="status-indicator yes">Y</span>
                <span v-else class="status-indicator no">N</span>
              </td>
              <td class="col-remove">
                <button @click="removePassenger(passenger)" class="btn-icon remove">
                  <i class="fas fa-times"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="pagination-section">
        <div class="pagination-info">
          <span>
            Displaying records {{ startRecord }} to {{ endRecord }} from a total of {{ totalRecords }} records
          </span>
        </div>
        <div class="pagination-controls">
          <span>Search:</span>
          <input 
            type="text" 
            v-model="paginationSearch"
            class="form-control pagination-search"
            placeholder="Quick search..."
          >
          <div class="pagination-buttons">
            <button 
              @click="goToPage(1)" 
              :disabled="currentPage === 1"
              class="pagination-btn"
            >
              Previous
            </button>
            <span class="page-numbers">
              <button 
                v-for="page in visiblePages" 
                :key="page"
                @click="goToPage(page)"
                :class="['page-btn', { active: page === currentPage }]"
              >
                {{ page }}
              </button>
            </span>
            <button 
              @click="goToPage(totalPages)" 
              :disabled="currentPage === totalPages"
              class="pagination-btn"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch } from 'vue'
import axios from 'axios'

// Props
const props = defineProps({
  tripId: {
    type: [String, Number],
    required: true
  },
  passengerStats: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['update-stats'])

// State
const passengers = ref([
  {
    id: 1,
    name: 'Lori Lynn Jastick',
    phone: '281-231-0686',
    mobile: '',
    email: 'lori@aptlytymages.com',
    parent_name: '',
    book_id: '',
    book_type: 'Admin-Manually',
    bunk_type: '',
    passengers_count: 1,
    web_booking: false,
    land_only: true,
    visa_required: false,
    roommates: 'SOLJ',
    insurance_amount: 0,
    cancellation_protection: false
  },
  {
    id: 2,
    name: 'Braxton James Necsoe',
    phone: '',
    mobile: '',
    email: 'braxtonecsoe@yahoo.com',
    parent_name: '',
    book_id: '',
    book_type: 'Admin-Manually',
    bunk_type: '',
    passengers_count: 1,
    web_booking: false,
    land_only: false,
    visa_required: false,
    roommates: 'SOLJ',
    insurance_amount: 0,
    cancellation_protection: false
  },
  {
    id: 3,
    name: 'Deborah Jutt Warren',
    phone: '2109771-4307',
    mobile: '',
    email: 'ed.debbie.warren@gmail.com',
    parent_name: '',
    book_id: '',
    book_type: 'online',
    bunk_type: '',
    passengers_count: 1,
    web_booking: true,
    land_only: true,
    visa_required: false,
    roommates: 'DBL/T',
    insurance_amount: 0,
    cancellation_protection: false
  },
  {
    id: 4,
    name: 'Daniel Edward Warren Jr',
    phone: '2109771-6076',
    mobile: '',
    email: 'ed.debbie.warren@gmail.com',
    parent_name: '',
    book_id: '',
    book_type: 'online',
    bunk_type: '',
    passengers_count: 1,
    web_booking: true,
    land_only: true,
    visa_required: false,
    roommates: 'DBL/T',
    insurance_amount: 0,
    cancellation_protection: false
  },
  {
    id: 5,
    name: 'Margarita Prins',
    phone: '979-236-1948',
    mobile: '',
    email: 'prinsum@yahoo.com',
    parent_name: '',
    book_id: '',
    book_type: 'Admin-Manually',
    bunk_type: '',
    passengers_count: 1,
    web_booking: false,
    land_only: false,
    visa_required: false,
    roommates: 'TWN/T',
    insurance_amount: 0,
    cancellation_protection: false
  },
  {
    id: 6,
    name: 'Jacqueline Ruth King',
    phone: '979-799-5758',
    mobile: '',
    email: 'jackiekrn615@gmail.com',
    parent_name: '',
    book_id: '',
    book_type: 'Admin-Manually',
    bunk_type: '',
    passengers_count: 1,
    web_booking: false,
    land_only: false,
    visa_required: false,
    roommates: 'TWN/T',
    insurance_amount: 0,
    cancellation_protection: false
  },
  {
    id: 7,
    name: 'Gene K Sheridan',
    phone: '228-233-7791',
    mobile: '',
    email: 'msgene@att.net',
    parent_name: '',
    book_id: '',
    book_type: 'Admin-Manually',
    bunk_type: '',
    passengers_count: 1,
    web_booking: false,
    land_only: false,
    visa_required: false,
    roommates: 'TWN/T',
    insurance_amount: 0,
    cancellation_protection: false
  },
  {
    id: 8,
    name: 'Donna Marie Gaulcher',
    phone: '228-396-8835',
    mobile: '',
    email: 'fosterpatchwork@att.net',
    parent_name: '',
    book_id: 'NVP-394',
    book_type: 'online-with-book-now',
    bunk_type: '',
    passengers_count: 1,
    web_booking: true,
    land_only: false,
    visa_required: false,
    roommates: 'TWN/T',
    insurance_amount: 0,
    cancellation_protection: false
  },
  {
    id: 9,
    name: 'Vicky Lee Wescovich',
    phone: '(228) 861-9122',
    mobile: '',
    email: 'vicky.wescovich@gmail.com',
    parent_name: '',
    book_id: '',
    book_type: 'Admin-Manually',
    bunk_type: '',
    passengers_count: 1,
    web_booking: false,
    land_only: false,
    visa_required: false,
    roommates: 'DBL/T',
    insurance_amount: 0,
    cancellation_protection: false
  },
  {
    id: 10,
    name: 'Robert Ripley Wescovich Jr',
    phone: '(228) 861-9122',
    mobile: '',
    email: 'rrwescovi@gmail.com',
    parent_name: '',
    book_id: '',
    book_type: 'Admin-Manually',
    bunk_type: '',
    passengers_count: 1,
    web_booking: false,
    land_only: false,
    visa_required: false,
    roommates: 'DBL/T',
    insurance_amount: 0,
    cancellation_protection: false
  }
])

const displayCount = ref(10)
const searchQuery = ref('')
const paginationSearch = ref('')
const currentPage = ref(1)
const selectAll = ref(false)
const selectedPassengers = ref([])
const maxPassengers = ref(16)

// Computed
const filteredPassengers = computed(() => {
  let filtered = passengers.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(passenger => 
      passenger.name.toLowerCase().includes(query) ||
      passenger.email?.toLowerCase().includes(query) ||
      passenger.phone?.includes(query)
    )
  }
  
  if (paginationSearch.value) {
    const query = paginationSearch.value.toLowerCase()
    filtered = filtered.filter(passenger => 
      passenger.name.toLowerCase().includes(query) ||
      passenger.email?.toLowerCase().includes(query)
    )
  }
  
  return filtered
})

const totalRecords = computed(() => filteredPassengers.value.length)
const totalPages = computed(() => Math.ceil(totalRecords.value / displayCount.value))

const paginatedPassengers = computed(() => {
  const start = (currentPage.value - 1) * displayCount.value
  const end = start + displayCount.value
  return filteredPassengers.value.slice(start, end)
})

const startRecord = computed(() => {
  if (totalRecords.value === 0) return 0
  return (currentPage.value - 1) * displayCount.value + 1
})

const endRecord = computed(() => {
  const end = currentPage.value * displayCount.value
  return Math.min(end, totalRecords.value)
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// Methods
const updateDisplay = () => {
  currentPage.value = 1
}

const filterPassengers = () => {
  currentPage.value = 1
}

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedPassengers.value = paginatedPassengers.value.map(p => p.id)
  } else {
    selectedPassengers.value = []
  }
}

const getRowClass = (passenger) => {
  return {
    'admin-booking': passenger.book_type?.includes('Admin'),
    'online-booking': passenger.book_type?.includes('online'),
    'land-only': passenger.land_only
  }
}

const addNewPassenger = () => {
  // TODO: Open add passenger modal
  console.log('Adding new passenger')
}

const editPassenger = (passenger) => {
  // TODO: Open edit passenger modal
  console.log('Editing passenger:', passenger)
}

const removePassenger = (passenger) => {
  if (confirm(`Are you sure you want to remove ${passenger.name}?`)) {
    passengers.value = passengers.value.filter(p => p.id !== passenger.id)
    emit('update-stats')
  }
}

const openPassengerUrl = () => {
  const url = `${window.location.origin}/trip-registration/${props.tripId}`
  window.open(url, '_blank')
}

const processPayments = () => {
  console.log('Opening payments management')
}

const managePassengerList = () => {
  console.log('Opening passenger list management')
}

const generatePdf = () => {
  console.log('Generating PDF report')
}

const emailPtfAndEstimates = () => {
  console.log('Sending PTF and estimates')
}

const sendEmail = () => {
  console.log('Opening email modal')
}

const formatCurrency = (amount) => {
  if (!amount) return '0.00'
  return Number(amount).toFixed(2)
}

// Watch for pagination search changes
watch(paginationSearch, () => {
  currentPage.value = 1
})
</script>

<style scoped>
.customer-waiting-list-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.action-buttons-section,
.passenger-list-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.section-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 18px;
  font-weight: 600;
}

.section-header h3 i {
  margin-right: 8px;
  color: #3b82f6;
}

.passenger-info {
  font-size: 14px;
  color: #6b7280;
}

.action-buttons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.action-btn {
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  color: #374151;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.action-btn:hover {
  border-color: #3b82f6;
  background: #f8fafc;
  color: #3b82f6;
}

.action-btn.passenger-url {
  background: #dbeafe;
  border-color: #3b82f6;
  color: #1e40af;
}

.action-btn.payments {
  background: #dcfce7;
  border-color: #10b981;
  color: #065f46;
}

.action-btn.passenger-list {
  background: #fef3c7;
  border-color: #f59e0b;
  color: #92400e;
}

.action-btn.pdf {
  background: #fecaca;
  border-color: #ef4444;
  color: #991b1b;
}

.action-btn.email-ptf {
  background: #e0e7ff;
  border-color: #6366f1;
  color: #4338ca;
}

.action-btn.send-email {
  background: #f3e8ff;
  border-color: #8b5cf6;
  color: #6b21a8;
}

.list-controls-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.display-control,
.search-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.display-control label,
.search-control label {
  font-weight: 500;
  color: #374151;
  font-size: 14px;
}

.form-control {
  padding: 6px 10px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.passenger-table-container {
  overflow-x: auto;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  margin-bottom: 20px;
}

.passenger-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  min-width: 1400px;
}

.passenger-table th {
  background: #f9fafb;
  padding: 10px 8px;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  white-space: nowrap;
}

.passenger-table td {
  padding: 8px;
  border-bottom: 1px solid #f3f4f6;
  vertical-align: middle;
}

.passenger-row:hover {
  background: #f9fafb;
}

.passenger-row.admin-booking {
  background: #fef3f2;
}

.passenger-row.online-booking {
  background: #f0f9ff;
}

.passenger-row.land-only td {
  color: #059669;
  font-weight: 500;
}

.col-edit,
.col-select,
.col-remove {
  width: 50px;
  text-align: center;
}

.col-name {
  min-width: 180px;
}

.col-phone,
.col-mobile {
  min-width: 120px;
}

.col-email {
  min-width: 200px;
}

.col-parent {
  min-width: 150px;
}

.col-book-id,
.col-bunk {
  min-width: 100px;
}

.col-passengers,
.col-web,
.col-land,
.col-visa,
.col-cancellation {
  width: 80px;
  text-align: center;
}

.col-roommates {
  min-width: 100px;
}

.col-insurance {
  min-width: 100px;
}

.passenger-name {
  display: flex;
  flex-direction: column;
}

.name-text {
  font-weight: 500;
  color: #1f2937;
}

.name-details {
  font-size: 11px;
  color: #6b7280;
  margin-top: 2px;
}

.book-type {
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 10px;
  font-weight: 500;
}

.email-link {
  color: #3b82f6;
  text-decoration: none;
}

.email-link:hover {
  text-decoration: underline;
}

.status-indicator {
  font-weight: 600;
  font-size: 11px;
}

.status-indicator.yes {
  color: #10b981;
}

.status-indicator.no {
  color: #ef4444;
}

.insurance-amount {
  font-weight: 500;
  color: #1f2937;
}

.btn-icon {
  padding: 4px 6px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 11px;
  transition: all 0.2s;
}

.btn-icon.edit {
  background: #eff6ff;
  color: #2563eb;
}

.btn-icon.edit:hover {
  background: #dbeafe;
}

.btn-icon.remove {
  background: #fef2f2;
  color: #dc2626;
}

.btn-icon.remove:hover {
  background: #fee2e2;
}

.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f9fafb;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.pagination-info {
  font-size: 14px;
  color: #6b7280;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pagination-search {
  width: 150px;
}

.pagination-buttons {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination-btn {
  padding: 6px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: white;
  color: #374151;
  cursor: pointer;
  font-size: 14px;
}

.pagination-btn:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 2px;
}

.page-btn {
  padding: 6px 10px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: white;
  color: #374151;
  cursor: pointer;
  font-size: 14px;
}

.page-btn:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}

.page-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.text-center {
  text-align: center;
}

/* Responsive */
@media (max-width: 768px) {
  .action-buttons-grid {
    grid-template-columns: 1fr;
  }

  .list-controls-bar {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .pagination-section {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .pagination-controls {
    flex-wrap: wrap;
  }
}
</style>
