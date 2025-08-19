<template>
  <div class="trip-air-container">
    
    <!-- Air Information Section -->
    <div class="air-info-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-plane"></i>
          Flight Information Management
        </h3>
        <div class="section-actions">
          <button @click="addFlight" class="btn btn-primary">
            <i class="fas fa-plus"></i>
            Add Flight
          </button>
          <button @click="importFlights" class="btn btn-info">
            <i class="fas fa-upload"></i>
            Import Flights
          </button>
        </div>
      </div>

      <!-- Flight Details Form -->
      <div class="flight-details-form">
        <div class="form-row">
          <div class="form-group">
            <label>Airline</label>
            <select v-model="airData.airline" @change="updateField('airline')" class="form-control">
              <option value="">Select Airline</option>
              <option value="American Airlines">American Airlines</option>
              <option value="Delta Airlines">Delta Airlines</option>
              <option value="United Airlines">United Airlines</option>
              <option value="Southwest Airlines">Southwest Airlines</option>
              <option value="JetBlue Airways">JetBlue Airways</option>
              <option value="Alaska Airlines">Alaska Airlines</option>
              <option value="Lufthansa">Lufthansa</option>
              <option value="British Airways">British Airways</option>
              <option value="Air France">Air France</option>
              <option value="KLM">KLM</option>
              <option value="Other">Other</option>
            </select>
          </div>
          <div class="form-group">
            <label>Departure Airport</label>
            <input 
              type="text" 
              v-model="airData.departure_airport" 
              @blur="updateField('departure_airport')"
              class="form-control"
              placeholder="e.g., JFK, LAX, DFW"
            >
          </div>
          <div class="form-group">
            <label>Arrival Airport</label>
            <input 
              type="text" 
              v-model="airData.arrival_airport" 
              @blur="updateField('arrival_airport')"
              class="form-control"
              placeholder="e.g., TLV, CAI, ATH"
            >
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Departure Date</label>
            <input 
              type="datetime-local" 
              v-model="airData.departure_date" 
              @blur="updateField('departure_date')"
              class="form-control"
            >
          </div>
          <div class="form-group">
            <label>Arrival Date</label>
            <input 
              type="datetime-local" 
              v-model="airData.arrival_date" 
              @blur="updateField('arrival_date')"
              class="form-control"
            >
          </div>
          <div class="form-group">
            <label>Flight Duration</label>
            <input 
              type="text" 
              v-model="airData.flight_duration" 
              @blur="updateField('flight_duration')"
              class="form-control"
              placeholder="e.g., 12h 30m"
            >
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Flight Number</label>
            <input 
              type="text" 
              v-model="airData.flight_number" 
              @blur="updateField('flight_number')"
              class="form-control"
              placeholder="e.g., AA123, DL456"
            >
          </div>
          <div class="form-group">
            <label>Aircraft Type</label>
            <input 
              type="text" 
              v-model="airData.aircraft_type" 
              @blur="updateField('aircraft_type')"
              class="form-control"
              placeholder="e.g., Boeing 777, Airbus A330"
            >
          </div>
          <div class="form-group">
            <label>Seat Class</label>
            <select v-model="airData.seat_class" @change="updateField('seat_class')" class="form-control">
              <option value="Economy">Economy</option>
              <option value="Premium Economy">Premium Economy</option>
              <option value="Business">Business</option>
              <option value="First">First Class</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Cost per Person</label>
            <input 
              type="number" 
              v-model="airData.cost_per_person" 
              @blur="updateField('cost_per_person')"
              class="form-control"
              step="0.01"
              placeholder="0.00"
            >
          </div>
          <div class="form-group">
            <label>Total Cost</label>
            <input 
              type="number" 
              v-model="airData.total_cost" 
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
              v-model="airData.booking_reference" 
              @blur="updateField('booking_reference')"
              class="form-control"
              placeholder="Airline booking reference"
            >
          </div>
        </div>

        <div class="form-group">
          <label>Special Instructions</label>
          <textarea 
            v-model="airData.special_instructions" 
            @blur="updateField('special_instructions')"
            class="form-control"
            rows="3"
            placeholder="Any special instructions for passengers..."
          ></textarea>
        </div>
      </div>
    </div>

    <!-- Flight Itinerary Section -->
    <div class="flight-itinerary-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-route"></i>
          Flight Itinerary
        </h3>
        <button @click="addFlightSegment" class="btn btn-secondary">
          <i class="fas fa-plus"></i>
          Add Segment
        </button>
      </div>

      <div class="flight-segments">
        <div 
          v-for="(segment, index) in flightSegments" 
          :key="segment.id"
          class="flight-segment"
        >
          <div class="segment-header">
            <h4>
              <i class="fas fa-plane-departure"></i>
              Segment {{ index + 1 }}
              <span v-if="segment.type" class="segment-type">{{ segment.type }}</span>
            </h4>
            <button @click="removeSegment(segment.id)" class="btn-icon remove">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <div class="segment-details">
            <div class="form-row">
              <div class="form-group">
                <label>From</label>
                <input 
                  type="text" 
                  v-model="segment.from_airport" 
                  class="form-control"
                  placeholder="Airport code"
                >
              </div>
              <div class="form-group">
                <label>To</label>
                <input 
                  type="text" 
                  v-model="segment.to_airport" 
                  class="form-control"
                  placeholder="Airport code"
                >
              </div>
              <div class="form-group">
                <label>Flight</label>
                <input 
                  type="text" 
                  v-model="segment.flight_number" 
                  class="form-control"
                  placeholder="Flight number"
                >
              </div>
              <div class="form-group">
                <label>Departure</label>
                <input 
                  type="datetime-local" 
                  v-model="segment.departure_time" 
                  class="form-control"
                >
              </div>
              <div class="form-group">
                <label>Arrival</label>
                <input 
                  type="datetime-local" 
                  v-model="segment.arrival_time" 
                  class="form-control"
                >
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="flightSegments.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="fas fa-route"></i>
          </div>
          <h4>No Flight Segments</h4>
          <p>Add flight segments to build the complete itinerary.</p>
          <button @click="addFlightSegment" class="btn btn-primary">
            <i class="fas fa-plus"></i>
            Add First Segment
          </button>
        </div>
      </div>
    </div>

    <!-- Passenger Air Requirements -->
    <div class="passenger-air-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-users-cog"></i>
          Passenger Air Requirements
        </h3>
        <div class="requirements-stats">
          <span class="stat-item">
            <i class="fas fa-passport"></i>
            {{ passengerRequirements.passport_required }} need passports
          </span>
          <span class="stat-item">
            <i class="fas fa-wheelchair"></i>
            {{ passengerRequirements.special_assistance }} need assistance
          </span>
        </div>
      </div>

      <div class="requirements-grid">
        <div class="requirement-card">
          <h4>
            <i class="fas fa-passport"></i>
            Passport Requirements
          </h4>
          <div class="requirement-details">
            <p>Passengers must have valid passports with at least 6 months validity.</p>
            <div class="requirement-actions">
              <button @click="checkPassportStatus" class="btn btn-info btn-sm">
                <i class="fas fa-check"></i>
                Check Status
              </button>
              <button @click="sendPassportReminder" class="btn btn-warning btn-sm">
                <i class="fas fa-envelope"></i>
                Send Reminder
              </button>
            </div>
          </div>
        </div>

        <div class="requirement-card">
          <h4>
            <i class="fas fa-suitcase"></i>
            Baggage Information
          </h4>
          <div class="requirement-details">
            <div class="baggage-info">
              <div class="baggage-item">
                <span class="label">Carry-on:</span>
                <span class="value">{{ airData.carryon_allowance || '1 bag, 10kg max' }}</span>
              </div>
              <div class="baggage-item">
                <span class="label">Checked:</span>
                <span class="value">{{ airData.checked_allowance || '2 bags, 23kg each' }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="requirement-card">
          <h4>
            <i class="fas fa-wheelchair"></i>
            Special Assistance
          </h4>
          <div class="requirement-details">
            <p>Coordinate special assistance requirements with airline.</p>
            <div class="requirement-actions">
              <button @click="manageAssistance" class="btn btn-primary btn-sm">
                <i class="fas fa-cog"></i>
                Manage
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="air-actions">
      <button @click="saveAirData" class="btn btn-success" :disabled="saving">
        <i class="fas fa-save"></i>
        {{ saving ? 'Saving...' : 'Save Air Information' }}
      </button>
      <button @click="generateFlightManifest" class="btn btn-info">
        <i class="fas fa-file-alt"></i>
        Generate Flight Manifest
      </button>
      <button @click="emailFlightDetails" class="btn btn-primary">
        <i class="fas fa-envelope"></i>
        Email Flight Details
      </button>
      <button @click="exportAirData" class="btn btn-secondary">
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
const airData = reactive({
  airline: '',
  departure_airport: '',
  arrival_airport: '',
  departure_date: '',
  arrival_date: '',
  flight_duration: '',
  flight_number: '',
  aircraft_type: '',
  seat_class: 'Economy',
  cost_per_person: 0,
  total_cost: 0,
  booking_reference: '',
  special_instructions: '',
  carryon_allowance: '1 bag, 10kg max',
  checked_allowance: '2 bags, 23kg each'
})

const flightSegments = ref([])

const passengerRequirements = reactive({
  passport_required: 0,
  special_assistance: 0
})

// Methods
const updateField = async (fieldName) => {
  try {
    saving.value = true
    
    const updateData = {
      air_details: {
        ...airData,
        [fieldName]: airData[fieldName]
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

const addFlight = () => {
  // TODO: Open add flight modal
  console.log('Adding new flight')
}

const importFlights = () => {
  // TODO: Open import flights modal
  console.log('Importing flights')
}

const addFlightSegment = () => {
  const newSegment = {
    id: Date.now(),
    type: flightSegments.value.length === 0 ? 'Outbound' : 'Return',
    from_airport: '',
    to_airport: '',
    flight_number: '',
    departure_time: '',
    arrival_time: ''
  }
  flightSegments.value.push(newSegment)
}

const removeSegment = (segmentId) => {
  flightSegments.value = flightSegments.value.filter(s => s.id !== segmentId)
}

const checkPassportStatus = () => {
  // TODO: Check passport status for all passengers
  console.log('Checking passport status')
}

const sendPassportReminder = () => {
  // TODO: Send passport reminder emails
  console.log('Sending passport reminders')
}

const manageAssistance = () => {
  // TODO: Open special assistance management
  console.log('Managing special assistance')
}

const saveAirData = async () => {
  try {
    saving.value = true
    
    const updateData = {
      air_details: airData,
      flight_segments: flightSegments.value
    }
    
    const response = await axios.patch(`/api/quotes/${props.tripId}/`, updateData)
    
    emit('update-trip', response.data)
    
  } catch (error) {
    console.error('Error saving air data:', error)
  } finally {
    saving.value = false
  }
}

const generateFlightManifest = () => {
  // TODO: Generate flight manifest
  console.log('Generating flight manifest')
}

const emailFlightDetails = () => {
  // TODO: Email flight details to passengers
  console.log('Emailing flight details')
}

const exportAirData = () => {
  // TODO: Export air data
  console.log('Exporting air data')
}
</script>

<style scoped>
.trip-air-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.air-info-section,
.flight-itinerary-section,
.passenger-air-section {
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

.flight-details-form {
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

.flight-segments {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.flight-segment {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  background: #f9fafb;
}

.segment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.segment-header h4 {
  margin: 0;
  color: #1f2937;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.segment-type {
  background: #3b82f6;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
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

.requirements-stats {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #6b7280;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.requirements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.requirement-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  background: white;
}

.requirement-card h4 {
  margin: 0 0 12px 0;
  color: #1f2937;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.requirement-details p {
  margin: 0 0 12px 0;
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
}

.requirement-actions {
  display: flex;
  gap: 8px;
}

.baggage-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.baggage-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.baggage-item .label {
  font-weight: 600;
  color: #374151;
}

.baggage-item .value {
  color: #6b7280;
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

.air-actions {
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

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
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

.btn-warning {
  background-color: #f59e0b;
  color: white;
}

.btn-warning:hover {
  background-color: #d97706;
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

  .requirements-grid {
    grid-template-columns: 1fr;
  }

  .air-actions {
    flex-wrap: wrap;
  }

  .requirements-stats {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
