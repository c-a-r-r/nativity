<template>
  <div class="trip-quote-container">
    
    <!-- Trip Information Section -->
    <div class="trip-info-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-file-invoice-dollar"></i>
          Quote Information
        </h3>
        <div class="section-actions">
          <button @click="copyPriceListLink" class="btn btn-outline">
            <i class="fas fa-link"></i>
            Copy Price List Link
          </button>
          <button @click="copyPublicLink" class="btn btn-outline">
            <i class="fas fa-external-link-alt"></i>
            Copy Public Link
          </button>
        </div>
      </div>

      <div class="quote-form-grid">
        
        <!-- Left Column -->
        <div class="form-column">
          
          <!-- Basic Information -->
           <div class="form-row">
              <div class="form-group third">
            <label>Quote #</label>
            <input 
              type="text" 
              :value="tripData?.id || ''" 
              readonly 
              class="form-control readonly"
            >
          </div>
          
          <div class="form-group two-thirds">
            <label>Trip Name</label>
            <input 
              type="text" 
              v-model="localTripData.trip_name" 
              @blur="updateField('trip_name')"
              class="form-control"
            >
          </div>
          </div>

          <!-- Contact Information -->
          <div class="info-subsection">
            <h4>Contact Information</h4>
            
            <div class="form-row">
              <div class="form-group half">
                <label>Contact</label>
                <input 
                  type="text" 
                  v-model="localTripData.client_name" 
                  @blur="updateField('client_name')"
                  class="form-control"
                >
              </div>
              <div class="form-group half">
                <label>Contact Phone</label>
                <input 
                  type="tel" 
                  :value="contactPhone"
                  readonly
                  class="form-control readonly"
                >
              </div>
            </div>

            <div class="form-row">
              <div class="form-group half">
                <label>Contact Email</label>
                <input 
                  type="email" 
                  :value="contactEmail"
                  readonly
                  class="form-control readonly"
                >
              </div>
              <div class="form-group half">
                <label>Contact Email 2</label>
                <input 
                  type="email" 
                  :value="contactEmail2"
                  readonly
                  class="form-control readonly"
                >
              </div>
            </div>

            <!-- <div class="form-row">
              <div class="form-group half">
                <label>Contact Email 3</label>
                <input 
                  type="email" 
                  :value="contactEmail3"
                  readonly
                  class="form-control readonly"
                >
              </div>
            </div> -->

            <div class="form-row">
              <div class="form-group half">
                <label>Church Name</label>
                <input 
                  type="text" 
                  v-model="localTripData.church_name" 
                  @blur="updateField('church_name')"
                  class="form-control"
                >
              </div>
              <div class="form-group half">
                <label>Spiritual Director Name</label>
                <input 
                  type="text" 
                  v-model="localTripData.leader_name" 
                  @blur="updateField('leader_name')"
                  class="form-control"
                >
              </div>
            </div>

            <div class="form-row">
              <div class="form-group half">
                <label>Coordinator Name</label>
                <input 
                  type="text" 
                  v-model="localTripData.coordinator_name" 
                  @blur="updateField('coordinator_name')"
                  class="form-control"
                >
              </div>
              <div class="form-group half">
                <label>Coordinator Email</label>
                <input 
                  type="email" 
                  v-model="localTripData.coordinator_email" 
                  @blur="updateField('coordinator_email')"
                  class="form-control"
                >
              </div>
            </div>
          </div>

          <div class="cost-section">
            <h4>Cost Breakdown</h4>
            
            <div class="form-row">
              <div class="form-group third">
                <label>Bus Cost Total</label>
                <input 
                  type="number" 
                  v-model="localTripData.cost_bus" 
                  @blur="updateField('cost_bus')"
                  class="form-control"
                  step="0.01"
                >
              </div>
              <div class="form-group third">
                <label>Air Cost ea.</label>
                <input 
                  type="number" 
                  v-model="localTripData.cost_air" 
                  @blur="updateField('cost_air')"
                  class="form-control"
                  step="0.01"
                >
              </div>
              <div class="form-group third">
                <label>Land Cost ea.</label>
                <input 
                  type="number" 
                  v-model="localTripData.cost_land" 
                  @blur="updateField('cost_land')"
                  class="form-control"
                  step="0.01"
                >
              </div>
            </div>

            <div class="form-row">
              <div class="form-group half">
                <label>Marketing Cost</label>
                <input 
                  type="number" 
                  v-model="localTripData.cost_marketing" 
                  @blur="updateField('cost_marketing')"
                  class="form-control"
                  step="0.01"
                >
              </div>
              <div class="form-group half">
                <label>Misc. Cost</label>
                <input 
                  type="number" 
                  v-model="localTripData.cost_misc" 
                  @blur="updateField('cost_misc')"
                  class="form-control"
                  step="0.01"
                >
              </div>
            </div>
          </div>

          
        </div>

        <!-- Right Column -->
        <div class="form-column">

            <div class="info-subsection">
            <h4>Itinerary Information</h4>
            
            <div class="form-row">
              <div class="form-group half">
                <label>Departure Date</label>
                <input 
                  type="date" 
                  v-model="localTripData.departure_date" 
                  @blur="updateField('departure_date')"
                  class="form-control"
                >
              </div>
              <div class="form-group half">
                <label>Departure City</label>
                <input 
                  type="text" 
                  :value="departureCityDisplay"
                  readonly
                  class="form-control readonly"
                  placeholder="No departure city selected"
                >
              </div>
            </div>

            <div class="form-row">
              <div class="form-group half">
                <label>Cost</label>
                <input 
                  type="number" 
                  v-model="localTripData.itinerary_cost" 
                  @blur="updateField('itinerary_cost')"
                  class="form-control"
                  step="0.01"
                >
              </div>
              <div class="form-group half">
                <label>Commission Base</label>
                <input 
                  type="number" 
                  v-model="localTripData.comision_usuario" 
                  @blur="updateField('comision_usuario')"
                  class="form-control"
                  step="0.01"
                >
              </div>
            </div>

            <div class="form-row">
            <div class="form-group half">
              <label>Fundraiser</label>
              <input 
                type="number" 
                v-model="localTripData.comision_leader" 
                @blur="updateField('comision_leader')"
                class="form-control"
                step="0.01"
              >
            </div>
            <div class="form-group half">
              <label>Total Cost</label>
              <input 
                type="number" 
                v-model="localTripData.total_cost" 
                @blur="updateField('total_cost')"
                class="form-control total-cost"
                step="0.01"
              >
            </div>
          </div>

          <div class="form-row">
            <div class="form-group half">
              <label>Language</label>
              <select 
                v-model="localTripData.language" 
                @change="updateField('language')"
                class="form-control"
              >
                <option value="">Select Language</option>
                <option value="ENGLISH">ENGLISH</option>
                <option value="SPANISH">SPANISH</option>
                <option value="BILINGUAL">BILINGUAL</option>
              </select>
            </div>
            <div class="form-group half">
              <label>One Travels Free for each</label>
              <input 
                type="number" 
                v-model="localTripData.free_each" 
                @blur="updateField('free_each')"
                class="form-control"
                step="1"
              >
            </div>
          </div>

          <div class="form-row">
            <div class="form-group half">
              <label>Leader Travels Free</label>
              <select 
                v-model="localTripData.leader_free" 
                @change="updateField('leader_free')"
                class="form-control"
              >
                <option value="Y">Yes</option>
                <option value="N">No</option>
              </select>
            </div>
            <div class="form-group half">
              <label>Status</label>
              <select 
                v-model="localTripData.quote_status" 
                @change="updateField('quote_status')"
                class="form-control"
              >
                <option value="">Select Status</option>
                <option value="1">Draft</option>
                <option value="2">Sent to Contact</option>
                <option value="4">Accepted</option>
                <option value="5">Rejected</option>
                <option value="6">Completed</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Notes</label>
            <textarea 
              v-model="localTripData.notes" 
              @blur="updateField('notes')"
              class="form-control"
              rows="4"
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-group half">
              <label>Sales Person</label>
              <input 
                class="form-control readonly" 
                :value="assignedUserName || 'No user assigned'" 
                readonly 
              />
              <small v-if="localTripData.user_id" class="text-muted">
                User ID: {{ localTripData.user_id }}
              </small>
            </div>
            <div class="form-group half">
              <label>Date Created</label>
              <input 
                type="text" 
                :value="formatDate(tripData?.date_created)" 
                readonly 
                class="form-control readonly"
              >
            </div>
          </div>

          <!-- Account Manager and Agent -->
          <div class="form-row">
            <div class="form-group half">
              <label>Account Manager</label>
              <select 
                v-model="localTripData.manager_id" 
                @change="updateField('manager_id')"
                class="form-control"
                :disabled="loadingUsers"
              >
                <option value="">{{ loadingUsers ? 'Loading...' : 'Select Account Manager' }}</option>
                <option 
                  v-for="manager in accountManagers" 
                  :key="manager.id" 
                  :value="manager.id"
                >
                  {{ manager.nombre }}
                </option>
              </select>
            </div>
            <div class="form-group half">
              <label>Sales Agent</label>
              <select 
                v-model="localTripData.agent_id" 
                @change="updateField('agent_id')"
                class="form-control"
                :disabled="loadingUsers"
              >
                <option value="">{{ loadingUsers ? 'Loading...' : 'Select Sales Agent' }}</option>
                <option 
                  v-for="agent in salesAgents" 
                  :key="agent.id" 
                  :value="agent.id"
                >
                  {{ agent.nombre }}
                </option>
              </select>
            </div>
          </div>


          </div><!-- end of itinerary information -->

          

          <!-- Cost Information -->
          
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="form-actions">
        <button @click="saveChanges" class="btn btn-success" :disabled="saving">
          <i class="fas fa-save"></i>
          {{ saving ? 'Saving...' : 'Save' }}
        </button>
        <button @click="emailTemplate" class="btn btn-primary">
          <i class="fas fa-envelope"></i>
          Email Template
        </button>
        <button @click="downloadExcel" class="btn btn-info">
          <i class="fas fa-download"></i>
          Download Excel
        </button>
        <button @click="shareRecord" class="btn btn-secondary">
          <i class="fas fa-share"></i>
          Share Record
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import axios from 'axios'

// Props
const props = defineProps({
  tripData: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['update-trip'])

// State
const saving = ref(false)
const localTripData = reactive({})
const accountManagers = ref([])
const salesAgents = ref([])
const loadingUsers = ref(false)

// Copy trip data to local state
watch(() => props.tripData, (newData) => {
  if (newData) {
    Object.assign(localTripData, newData)
  }
}, { immediate: true, deep: true })

// Fetch users on component mount
const fetchUsers = async () => {
  try {
    loadingUsers.value = true
    
    // Fetch account managers and sales agents separately for better performance
    const [managersResponse, agentsResponse] = await Promise.all([
      axios.get('/api/users-by-role/?role=managers'),
      axios.get('/api/users-by-role/?role=agents')
    ])
    
    accountManagers.value = managersResponse.data
    salesAgents.value = agentsResponse.data
    
  } catch (error) {
    console.error('Error fetching users:', error)
    // Fallback to full user list if the role-based endpoint fails
    try {
      const response = await axios.get('/api/users/')
      accountManagers.value = response.data.filter(user => user.agent === 'NO' && user.activo === 'YES')
      salesAgents.value = response.data.filter(user => user.agent === 'YES' && user.activo === 'YES')
    } catch (fallbackError) {
      console.error('Error fetching users (fallback):', fallbackError)
    }
  } finally {
    loadingUsers.value = false
  }
}

// Load users when component mounts
fetchUsers()

// Computed properties for contact information
const contactPhone = computed(() => {
  return localTripData.contact_phone || ''
})

const contactEmail = computed(() => {
  return localTripData.contact_email || ''
})

const contactEmail2 = computed(() => {
  return localTripData.contact_email_2 || ''
})

const contactEmail3 = computed(() => {
  return localTripData.contact_email_3 || ''
})

// Computed property for departure city display
const departureCityDisplay = computed(() => {
  return localTripData.departure_city_display || ''
})

// Computed properties for displaying Account Manager and Sales Agent names
const accountManagerName = computed(() => {
  if (!localTripData.manager_id) return ''
  const manager = accountManagers.value.find(m => m.id === localTripData.manager_id)
  return manager ? manager.nombre : ''
})

const salesAgentName = computed(() => {
  if (!localTripData.agent_id) return ''
  const agent = salesAgents.value.find(a => a.id === localTripData.agent_id)
  return agent ? agent.nombre : ''
})

// Computed property for assigned user name (from user_id)
const assignedUserName = computed(() => {
  // First try to use the user_full_name if available from backend
  if (localTripData.user_full_name) {
    return localTripData.user_full_name
  }
  
  // If user_full_name is not available, try to find user from all users
  if (!localTripData.user_id) return ''
  
  // Search in both account managers and sales agents since user_id could be either
  const allUsers = [...accountManagers.value, ...salesAgents.value]
  const user = allUsers.find(u => u.id === localTripData.user_id)
  return user ? user.nombre : `User ID: ${localTripData.user_id}`
})

// Methods
const updateField = async (fieldName) => {
  try {
    saving.value = true
    
    const updateData = {
      [fieldName]: localTripData[fieldName]
    }
    
    const response = await axios.patch(`/api/quotes/${props.tripData.id}/`, updateData)
    
    emit('update-trip', response.data)
    
  } catch (error) {
    console.error(`Error updating ${fieldName}:`, error)
    // Revert local change on error
    localTripData[fieldName] = props.tripData[fieldName]
  } finally {
    saving.value = false
  }
}

const saveChanges = async () => {
  try {
    saving.value = true
    
    const response = await axios.patch(`/api/quotes/${props.tripData.id}/`, localTripData)
    
    emit('update-trip', response.data)
    
  } catch (error) {
    console.error('Error saving trip data:', error)
  } finally {
    saving.value = false
  }
}

const copyPriceListLink = () => {
  const link = `${window.location.origin}/trip-template/${props.tripData.id}`
  navigator.clipboard.writeText(link)
  // TODO: Show toast notification
}

const copyPublicLink = () => {
  const link = `${window.location.origin}/public/trip/${props.tripData.id}`
  navigator.clipboard.writeText(link)
  // TODO: Show toast notification
}

const emailTemplate = () => {
  // TODO: Open email template modal
}

const downloadExcel = () => {
  // TODO: Generate and download Excel report
}

const shareRecord = () => {
  // TODO: Open share dialog
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString()
}
</script>

<style scoped>
.trip-quote-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.trip-info-section {
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.section-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 20px;
  font-weight: 600;
}

.section-header h3 i {
  margin-right: 8px;
  color: #3b82f6;
}

.section-actions {
  display: flex;
  gap: 8px;
}

.quote-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  margin-bottom: 24px;
}

.form-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-subsection {
  background: #f9fafb;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.info-subsection h4 {
  margin: 0 0 16px 0;
  color: #374151;
  font-size: 16px;
  font-weight: 600;
  padding-bottom: 8px;
  border-bottom: 1px solid #d1d5db;
}

.cost-section {
  background: #fef3f2;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #fecaca;
}

.cost-section h4 {
  margin: 0 0 16px 0;
  color: #dc2626;
  font-size: 16px;
  font-weight: 600;
  padding-bottom: 8px;
  border-bottom: 1px solid #fecaca;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-row {
  display: grid;
  gap: 16px;
}

.form-row .half {
  grid-template-columns: 1fr 1fr;
}

.form-row .third {
  grid-template-columns: 1fr 1fr 1fr;
}

.form-group.half {
  flex: 1;
}

.form-group.third {
  flex: 1;
}

.form-group.two-thirds {
  flex: 2;
}

.form-row {
  display: flex;
  gap: 16px;
}

label {
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.form-control {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-control.readonly {
  background-color: #f9fafb;
  color: #6b7280;
}

.form-control.total-cost {
  font-weight: 600;
  font-size: 16px;
  background-color: #fef3f2;
  border-color: #dc2626;
}

.text-muted {
  color: #6b7280;
  font-size: 12px;
  margin-top: 2px;
  font-style: italic;
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-start;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-success {
  background-color: #10b981;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background-color: #059669;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background-color: #2563eb;
}

.btn-info {
  background-color: #06b6d4;
  color: white;
}

.btn-info:hover {
  background-color: #0891b2;
}

.btn-secondary {
  background-color: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background-color: #4b5563;
}

.btn-outline {
  background-color: white;
  border: 1px solid #d1d5db;
  color: #374151;
}

.btn-outline:hover {
  background-color: #f9fafb;
  border-color: #9ca3af;
}

/* Responsive */
@media (max-width: 768px) {
  .quote-form-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .section-actions {
    width: 100%;
    justify-content: flex-start;
  }

  .form-row {
    flex-direction: column;
  }

  .form-actions {
    flex-wrap: wrap;
  }
}
</style>
