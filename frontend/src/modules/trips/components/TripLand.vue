<template>
  <div class="trip-land-container">
    
    <!-- Land Information Section -->
    <div class="land-info-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-bus"></i>
          Land Arrangements Management
        </h3>
        <div class="section-actions">
          <button @click="addArrangement" class="btn btn-primary">
            <i class="fas fa-plus"></i>
            Add Arrangement
          </button>
          <button @click="importArrangements" class="btn btn-info">
            <i class="fas fa-upload"></i>
            Import Data
          </button>
        </div>
      </div>

      <!-- Land Details Form -->
      <div class="land-details-form">
        <div class="form-row">
          <div class="form-group">
            <label>Ground Transportation</label>
            <select v-model="landData.ground_transportation" @change="updateField('ground_transportation')" class="form-control">
              <option value="">Select Transportation</option>
              <option value="Luxury Coach">Luxury Coach</option>
              <option value="Standard Bus">Standard Bus</option>
              <option value="Mini Bus">Mini Bus</option>
              <option value="Private Cars">Private Cars</option>
              <option value="Mixed Transportation">Mixed Transportation</option>
            </select>
          </div>
          <div class="form-group">
            <label>Transportation Provider</label>
            <input 
              type="text" 
              v-model="landData.transportation_provider" 
              @blur="updateField('transportation_provider')"
              class="form-control"
              placeholder="Company name"
            >
          </div>
          <div class="form-group">
            <label>Driver Contact</label>
            <input 
              type="text" 
              v-model="landData.driver_contact" 
              @blur="updateField('driver_contact')"
              class="form-control"
              placeholder="Driver phone/contact"
            >
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Local Guide</label>
            <input 
              type="text" 
              v-model="landData.local_guide" 
              @blur="updateField('local_guide')"
              class="form-control"
              placeholder="Guide name"
            >
          </div>
          <div class="form-group">
            <label>Guide Contact</label>
            <input 
              type="text" 
              v-model="landData.guide_contact" 
              @blur="updateField('guide_contact')"
              class="form-control"
              placeholder="Guide phone/email"
            >
          </div>
          <div class="form-group">
            <label>Guide Language</label>
            <select v-model="landData.guide_language" @change="updateField('guide_language')" class="form-control">
              <option value="English">English</option>
              <option value="Spanish">Spanish</option>
              <option value="French">French</option>
              <option value="Italian">Italian</option>
              <option value="Portuguese">Portuguese</option>
              <option value="German">German</option>
              <option value="Arabic">Arabic</option>
              <option value="Hebrew">Hebrew</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Land Cost per Person</label>
            <input 
              type="number" 
              v-model="landData.cost_per_person" 
              @blur="updateField('cost_per_person')"
              class="form-control"
              step="0.01"
              placeholder="0.00"
            >
          </div>
          <div class="form-group">
            <label>Total Land Cost</label>
            <input 
              type="number" 
              v-model="landData.total_cost" 
              @blur="updateField('total_cost')"
              class="form-control"
              step="0.01"
              placeholder="0.00"
            >
          </div>
          <div class="form-group">
            <label>Booking Reference</label>
            <input 
              type="text" 
              v-model="landData.booking_reference" 
              @blur="updateField('booking_reference')"
              class="form-control"
              placeholder="Land operator booking ref"
            >
          </div>
        </div>

        <div class="form-group">
          <label>Special Arrangements</label>
          <textarea 
            v-model="landData.special_arrangements" 
            @blur="updateField('special_arrangements')"
            class="form-control"
            rows="3"
            placeholder="Any special land arrangements or requirements..."
          ></textarea>
        </div>
      </div>
    </div>

    <!-- Hotel Accommodations Section -->
    <div class="hotel-accommodations-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-bed"></i>
          Hotel Accommodations
        </h3>
        <button @click="addHotel" class="btn btn-secondary">
          <i class="fas fa-plus"></i>
          Add Hotel
        </button>
      </div>

      <div class="hotel-list">
        <div 
          v-for="(hotel, index) in hotels" 
          :key="hotel.id"
          class="hotel-item"
        >
          <div class="hotel-header">
            <h4>
              <i class="fas fa-building"></i>
              Hotel {{ index + 1 }}
              <span v-if="hotel.name" class="hotel-name">- {{ hotel.name }}</span>
            </h4>
            <button @click="removeHotel(hotel.id)" class="btn-icon remove">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <div class="hotel-details">
            <div class="form-row">
              <div class="form-group">
                <label>Hotel Name</label>
                <input 
                  type="text" 
                  v-model="hotel.name" 
                  class="form-control"
                  placeholder="Hotel name"
                >
              </div>
              <div class="form-group">
                <label>Location/City</label>
                <input 
                  type="text" 
                  v-model="hotel.location" 
                  class="form-control"
                  placeholder="City, Country"
                >
              </div>
              <div class="form-group">
                <label>Star Rating</label>
                <select v-model="hotel.star_rating" class="form-control">
                  <option value="">Select Rating</option>
                  <option value="3">3 Star</option>
                  <option value="4">4 Star</option>
                  <option value="5">5 Star</option>
                  <option value="Boutique">Boutique</option>
                  <option value="Local">Local Hotel</option>
                </select>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Check-in Date</label>
                <input 
                  type="date" 
                  v-model="hotel.checkin_date" 
                  class="form-control"
                >
              </div>
              <div class="form-group">
                <label>Check-out Date</label>
                <input 
                  type="date" 
                  v-model="hotel.checkout_date" 
                  class="form-control"
                >
              </div>
              <div class="form-group">
                <label>Nights</label>
                <input 
                  type="number" 
                  v-model="hotel.nights" 
                  class="form-control"
                  min="1"
                  placeholder="Number of nights"
                >
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Room Type</label>
                <select v-model="hotel.room_type" class="form-control">
                  <option value="">Select Room Type</option>
                  <option value="Single">Single</option>
                  <option value="Double">Double</option>
                  <option value="Twin">Twin</option>
                  <option value="Triple">Triple</option>
                  <option value="Suite">Suite</option>
                  <option value="Family Room">Family Room</option>
                </select>
              </div>
              <div class="form-group">
                <label>Cost per Room</label>
                <input 
                  type="number" 
                  v-model="hotel.cost_per_room" 
                  class="form-control"
                  step="0.01"
                  placeholder="0.00"
                >
              </div>
              <div class="form-group">
                <label>Total Rooms</label>
                <input 
                  type="number" 
                  v-model="hotel.total_rooms" 
                  class="form-control"
                  min="1"
                  placeholder="Number of rooms"
                >
              </div>
            </div>

            <div class="form-group">
              <label>Hotel Contact</label>
              <input 
                type="text" 
                v-model="hotel.contact_info" 
                class="form-control"
                placeholder="Hotel phone/email"
              >
            </div>

            <div class="form-group">
              <label>Special Requests</label>
              <textarea 
                v-model="hotel.special_requests" 
                class="form-control"
                rows="2"
                placeholder="Special dietary requirements, room preferences, etc..."
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="hotels.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="fas fa-bed"></i>
          </div>
          <h4>No Hotels Added</h4>
          <p>Add hotel accommodations for your trip itinerary.</p>
          <button @click="addHotel" class="btn btn-primary">
            <i class="fas fa-plus"></i>
            Add First Hotel
          </button>
        </div>
      </div>
    </div>

    <!-- Itinerary Activities Section -->
    <div class="activities-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-map-marked-alt"></i>
          Itinerary Activities
        </h3>
        <button @click="addActivity" class="btn btn-secondary">
          <i class="fas fa-plus"></i>
          Add Activity
        </button>
      </div>

      <div class="activities-list">
        <div 
          v-for="(activity, index) in activities" 
          :key="activity.id"
          class="activity-item"
        >
          <div class="activity-header">
            <h4>
              <i class="fas fa-map-pin"></i>
              Day {{ activity.day }} - {{ activity.title || 'New Activity' }}
            </h4>
            <button @click="removeActivity(activity.id)" class="btn-icon remove">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <div class="activity-details">
            <div class="form-row">
              <div class="form-group">
                <label>Day</label>
                <input 
                  type="number" 
                  v-model="activity.day" 
                  class="form-control"
                  min="1"
                  placeholder="Day number"
                >
              </div>
              <div class="form-group">
                <label>Activity Title</label>
                <input 
                  type="text" 
                  v-model="activity.title" 
                  class="form-control"
                  placeholder="Activity name"
                >
              </div>
              <div class="form-group">
                <label>Time</label>
                <input 
                  type="time" 
                  v-model="activity.time" 
                  class="form-control"
                >
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Location</label>
                <input 
                  type="text" 
                  v-model="activity.location" 
                  class="form-control"
                  placeholder="Activity location"
                >
              </div>
              <div class="form-group">
                <label>Duration</label>
                <input 
                  type="text" 
                  v-model="activity.duration" 
                  class="form-control"
                  placeholder="e.g., 2 hours"
                >
              </div>
              <div class="form-group">
                <label>Cost</label>
                <input 
                  type="number" 
                  v-model="activity.cost" 
                  class="form-control"
                  step="0.01"
                  placeholder="0.00"
                >
              </div>
            </div>

            <div class="form-group">
              <label>Description</label>
              <textarea 
                v-model="activity.description" 
                class="form-control"
                rows="2"
                placeholder="Activity description and details..."
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="activities.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="fas fa-map-marked-alt"></i>
          </div>
          <h4>No Activities Planned</h4>
          <p>Add activities and excursions to your trip itinerary.</p>
          <button @click="addActivity" class="btn btn-primary">
            <i class="fas fa-plus"></i>
            Add First Activity
          </button>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="land-actions">
      <button @click="saveLandData" class="btn btn-success" :disabled="saving">
        <i class="fas fa-save"></i>
        {{ saving ? 'Saving...' : 'Save Land Information' }}
      </button>
      <button @click="generateItinerary" class="btn btn-info">
        <i class="fas fa-route"></i>
        Generate Itinerary
      </button>
      <button @click="emailLandDetails" class="btn btn-primary">
        <i class="fas fa-envelope"></i>
        Email Land Details
      </button>
      <button @click="exportLandData" class="btn btn-secondary">
        <i class="fas fa-download"></i>
        Export Data
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'

// Props
const props = defineProps({
  tripId: {
    type: [String, Number],
    required: true
  },
  tripData: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['update-trip'])

// State
const saving = ref(false)
const landData = reactive({
  ground_transportation: '',
  transportation_provider: '',
  driver_contact: '',
  local_guide: '',
  guide_contact: '',
  guide_language: 'English',
  cost_per_person: 0,
  total_cost: 0,
  booking_reference: '',
  special_arrangements: ''
})

const hotels = ref([])
const activities = ref([])

// Methods
const updateField = async (fieldName) => {
  try {
    saving.value = true
    
    const updateData = {
      land_details: {
        ...landData,
        [fieldName]: landData[fieldName]
      }
    }
    
    const response = await axios.patch(`/api/quotes/${props.tripId}/`, updateData)
    
    emit('update-trip', response.data)
    
  } catch (error) {
    console.error(`Error updating ${fieldName}:`, error)
  } finally {
    saving.value = false
  }
}

const addArrangement = () => {
  // TODO: Open add arrangement modal
  console.log('Adding new arrangement')
}

const importArrangements = () => {
  // TODO: Open import arrangements modal
  console.log('Importing arrangements')
}

const addHotel = () => {
  const newHotel = {
    id: Date.now(),
    name: '',
    location: '',
    star_rating: '',
    checkin_date: '',
    checkout_date: '',
    nights: 1,
    room_type: '',
    cost_per_room: 0,
    total_rooms: 1,
    contact_info: '',
    special_requests: ''
  }
  hotels.value.push(newHotel)
}

const removeHotel = (hotelId) => {
  hotels.value = hotels.value.filter(h => h.id !== hotelId)
}

const addActivity = () => {
  const newActivity = {
    id: Date.now(),
    day: activities.value.length + 1,
    title: '',
    time: '',
    location: '',
    duration: '',
    cost: 0,
    description: ''
  }
  activities.value.push(newActivity)
}

const removeActivity = (activityId) => {
  activities.value = activities.value.filter(a => a.id !== activityId)
}

const saveLandData = async () => {
  try {
    saving.value = true
    
    const updateData = {
      land_details: landData,
      hotels: hotels.value,
      activities: activities.value
    }
    
    const response = await axios.patch(`/api/quotes/${props.tripId}/`, updateData)
    
    emit('update-trip', response.data)
    
  } catch (error) {
    console.error('Error saving land data:', error)
  } finally {
    saving.value = false
  }
}

const generateItinerary = () => {
  // TODO: Generate complete itinerary
  console.log('Generating itinerary')
}

const emailLandDetails = () => {
  // TODO: Email land details to passengers
  console.log('Emailing land details')
}

const exportLandData = () => {
  // TODO: Export land data
  console.log('Exporting land data')
}
</script>

<style scoped>
.trip-land-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.land-info-section,
.hotel-accommodations-section,
.activities-section {
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

.section-actions {
  display: flex;
  gap: 8px;
}

.land-details-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
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

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}

.hotel-list,
.activities-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.hotel-item,
.activity-item {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  background: #f9fafb;
}

.hotel-header,
.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.hotel-header h4,
.activity-header h4 {
  margin: 0;
  color: #1f2937;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.hotel-name {
  color: #3b82f6;
  font-weight: 500;
}

.btn-icon {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.btn-icon.remove {
  background: #fef2f2;
  color: #dc2626;
}

.btn-icon.remove:hover {
  background: #fee2e2;
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: #6b7280;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  color: #d1d5db;
}

.empty-state h4 {
  margin: 0 0 8px 0;
  color: #374151;
  font-size: 18px;
}

.empty-state p {
  margin: 0 0 24px 0;
  font-size: 14px;
}

.land-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-start;
  padding: 20px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
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

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-secondary {
  background-color: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background-color: #4b5563;
}

.btn-success {
  background-color: #10b981;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background-color: #059669;
}

.btn-info {
  background-color: #06b6d4;
  color: white;
}

.btn-info:hover {
  background-color: #0891b2;
}

/* Responsive */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
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

  .land-actions {
    flex-wrap: wrap;
  }
}
</style>
