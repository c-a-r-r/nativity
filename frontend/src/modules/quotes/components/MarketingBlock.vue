<template>
  <div v-if="shouldShowMarketing">
    <hr class="mt-4">
    <h4 class="mb-3">MARKETING</h4>
    
    <!-- Photo Upload Section -->
    <div class="row g-3 mb-3">
      <div class="col-md-4">
        <label class="form-label">Main Photo</label>
        <div class="d-flex gap-1 py-2 px-2" style="background: white; border: 1px solid #ccc; border-radius: 10px;">
          <button 
            type="button" 
            class="btn btn-outline-primary btn-xs px-2 py-1"
            @click="showFile('main_photo')"
            :disabled="!form.main_photo"
            style="font-size: 12px; line-height: 1.2; white-space: nowrap; min-width: 90px;"
          >
            <i class="fa-regular fa-image fa-lg"></i> Show File
          </button>
          <button 
            type="button" 
            class="btn btn-outline-secondary btn-xs px-2 py-1"
            @click="clearFile('main_photo')"
            :disabled="!form.main_photo"
            style="font-size: 11px; line-height: 1.2; color: red;"
          >
            ✕ Clear
          </button>
          <button 
            type="button" 
            class="btn btn-outline-info btn-xs px-2 py-1"
            @click="triggerFileInput('main_photo')"
            style="font-size: 18px; line-height: 1.2;"
          >
            <i class="fa fa-cloud-upload fa-1x" aria-hidden="true"></i>
          </button>
          <input 
            type="text" 
            class="form-control form-control-sm" 
            :value="getFileName('main_photo')"
            readonly
            placeholder="No file selected"
            style="font-size: 12px;"
          />
        </div>
        <input 
          type="file" 
          class="d-none" 
          :ref="el => fileInputs['main_photo'] = el"
          @change="handleFileUpload('main_photo', $event)"
          accept="image/*"
        />
      </div>
      
      <div class="col-md-4">
        <label class="form-label">Spiritual Coordinator Photo</label>
        <div class="d-flex gap-1 py-2 px-2" style="background: white; border: 1px solid #ccc; border-radius: 10px;">
          <button 
            type="button" 
            class="btn btn-outline-primary btn-xs px-2 py-1"
            @click="showFile('spiritual_coordinator_photo')"
            :disabled="!form.spiritual_coordinator_photo"
            style="font-size: 12px; line-height: 1.2; white-space: nowrap; min-width: 90px;"
          >
            <i class="fa-regular fa-image fa-lg"></i> Show File
          </button>
          <button 
            type="button" 
            class="btn btn-outline-secondary btn-xs px-2 py-1"
            @click="clearFile('spiritual_coordinator_photo')"
            :disabled="!form.spiritual_coordinator_photo"
            style="font-size: 11px; line-height: 1.2; color: red;"
          >
            ✕ Clear
          </button>
          <button 
            type="button" 
            class="btn btn-outline-info btn-xs px-2 py-1"
            @click="triggerFileInput('spiritual_coordinator_photo')"
            style="font-size: 18px; line-height: 1.2;"
          >
            <i class="fa fa-cloud-upload fa-1x" aria-hidden="true"></i>
          </button>
          <input 
            type="text" 
            class="form-control form-control-sm" 
            :value="getFileName('spiritual_coordinator_photo')"
            readonly
            placeholder="No file selected"
            style="font-size: 12px;"
          />
        </div>
        <input 
          type="file" 
          class="d-none" 
          :ref="el => fileInputs['spiritual_coordinator_photo'] = el"
          @change="handleFileUpload('spiritual_coordinator_photo', $event)"
          accept="image/*"
        />
      </div>
    </div>

    <!-- Brochure Files Section -->
    <div class="row g-3 mb-3">
      <div class="col-md-4">
        <label class="form-label">Brochure File (Private Page)</label>
        <div class="d-flex gap-1 py-2 px-2" style="background: white; border: 1px solid #ccc; border-radius: 10px;">
          <button 
            type="button" 
            class="btn btn-outline-primary btn-xs px-2 py-1"
            @click="showFile('brochure_private')"
            :disabled="!form.brochure_private"
            style="font-size: 12px; line-height: 1.2; white-space: nowrap; min-width: 90px;"
          >
            <i class="fa-regular fa-image fa-lg"></i> Show File
          </button>
          <button 
            type="button" 
            class="btn btn-outline-secondary btn-xs px-2 py-1"
            @click="clearFile('brochure_private')"
            :disabled="!form.brochure_private"
            style="font-size: 11px; line-height: 1.2; color: red;"
          >
            ✕ Clear
          </button>
          <button 
            type="button" 
            class="btn btn-outline-info btn-xs px-2 py-1"
            @click="triggerFileInput('brochure_private')"
            style="font-size: 18px; line-height: 1.2;"
          >
            <i class="fa fa-cloud-upload fa-1x" aria-hidden="true"></i>
          </button>
          <input 
            type="text" 
            class="form-control form-control-sm" 
            :value="getFileName('brochure_private')"
            readonly
            placeholder="No file selected"
            style="font-size: 12px;"
          />
        </div>
        <input 
          type="file" 
          class="d-none" 
          :ref="el => fileInputs['brochure_private'] = el"
          @change="handleFileUpload('brochure_private', $event)"
          accept=".pdf,.doc,.docx"
        />
      </div>
      
      <div class="col-md-4">
        <label class="form-label">Brochure File (Public Page)</label>
        <div class="d-flex gap-1 py-2 px-2" style="background: white; border: 1px solid #ccc; border-radius: 10px;">
          <button 
            type="button" 
            class="btn btn-outline-primary btn-xs px-2 py-1"
            @click="showFile('brochure_public')"
            :disabled="!form.brochure_public"
            style="font-size: 12px; line-height: 1.2; white-space: nowrap; min-width: 90px;"
          >
            <i class="fa-regular fa-image fa-lg"></i> Show File
          </button>
          <button 
            type="button" 
            class="btn btn-outline-secondary btn-xs px-2 py-1"
            @click="clearFile('brochure_public')"
            :disabled="!form.brochure_public"
            style="font-size: 11px; line-height: 1.2; color: red;"
          >
            ✕ Clear
          </button>
          <button 
            type="button" 
            class="btn btn-outline-info btn-xs px-2 py-1"
            @click="triggerFileInput('brochure_public')"
            style="font-size: 18px; line-height: 1.2;"
          >
            <i class="fa fa-cloud-upload fa-1x" aria-hidden="true"></i>
          </button>
          <input 
            type="text" 
            class="form-control form-control-sm" 
            :value="getFileName('brochure_public')"
            readonly
            placeholder="No file selected"
            style="font-size: 12px;"
          />
        </div>
        <input 
          type="file" 
          class="d-none" 
          :ref="el => fileInputs['brochure_public'] = el"
          @change="handleFileUpload('brochure_public', $event)"
          accept=".pdf,.doc,.docx"
        />
      </div>
      
      <div class="col-md-4">
        <label class="form-label">Registration Form</label>
        <div class="d-flex gap-1 py-2 px-2" style="background: white; border: 1px solid #ccc; border-radius: 10px;">
          <button 
            type="button" 
            class="btn btn-outline-primary btn-xs px-2 py-1"
            @click="showFile('registration_form')"
            :disabled="!form.registration_form"
            style="font-size: 12px; line-height: 1.2; white-space: nowrap; min-width: 90px;"
          >
            <i class="fa-regular fa-image fa-lg"></i> Show File
          </button>
          <button 
            type="button" 
            class="btn btn-outline-secondary btn-xs px-2 py-1"
            @click="clearFile('registration_form')"
            :disabled="!form.registration_form"
            style="font-size: 11px; line-height: 1.2; color: red;"
          >
            ✕ Clear
          </button>
          <button 
            type="button" 
            class="btn btn-outline-info btn-xs px-2 py-1"
            @click="triggerFileInput('registration_form')"
            style="font-size: 18px; line-height: 1.2;"
          >
            <i class="fa fa-cloud-upload fa-1x" aria-hidden="true"></i>
          </button>
          <input 
            type="text" 
            class="form-control form-control-sm" 
            :value="getFileName('registration_form')"
            readonly
            placeholder="No file selected"
            style="font-size: 12px;"
          />
        </div>
        <input 
          type="file" 
          class="d-none" 
          :ref="el => fileInputs['registration_form'] = el"
          @change="handleFileUpload('registration_form', $event)"
          accept=".pdf,.doc,.docx"
        />
      </div>
    </div>

    <!-- Video Link -->
    <div class="row g-3 mb-3">
      <div class="col-md-12">
        <label class="form-label">Video Link</label>
        <input 
          v-model="form.video_link" 
          type="url" 
          class="form-control" 
          placeholder="https://youtu.be/s8DMIDE9VWE"
        />
      </div>
    </div>

    <!-- Terms and Conditions Template -->
    <div class="row g-3 mb-3">
      <div class="col-md-12">
        <label class="form-label">Terms And Conditions Template</label>
        <select v-model="form.terms_conditions_template" class="form-select">
          <option value="">-- Select Template --</option>
          <option value="includes_tips">Includes Tips</option>
          <option value="standard">Standard</option>
          <option value="custom">Custom</option>
        </select>
      </div>
    </div>

    <!-- Trip Includes and Does Not Include -->
    <div class="row g-3 mb-3">
      <div class="col-md-6">
        <label class="form-label">Trip Includes</label>
        <textarea 
          v-model="form.trip_includes" 
          class="form-control" 
          rows="6"
          placeholder="Round-Trip Airfare&#10;Airport taxes & fuel surcharges&#10;First-Class Hotels&#10;Land Transportation"
        ></textarea>
      </div>
      <div class="col-md-6">
        <label class="form-label">Trip Does Not Include</label>
        <textarea 
          v-model="form.trip_not_includes" 
          class="form-control" 
          rows="6"
          placeholder="Trip Cancellation Insurance&#10;Lunch&#10;Personal Items"
        ></textarea>
      </div>
    </div>

    <!-- Marketing Template Section -->
    <div class="marketing-section mb-4" v-if="quote">
      <h5>Marketing Trip</h5>
      
      <!-- Show existing trips -->
      <div v-if="quote.trips?.length" class="existing-trips mb-3">
        <h6>Existing Marketing Trips:</h6>
        <div 
          v-for="trip in quote.trips" 
          :key="trip.id"
          class="trip-card mb-2 p-3 border rounded"
        >
          <h6>{{ trip.trip_name }}</h6>
          <p class="mb-2">
            <strong>Slug:</strong> {{ trip.slug }}<br>
            <strong>Status:</strong> 
            <span :class="trip.is_published ? 'text-success' : 'text-warning'">
              {{ trip.is_published ? 'Published' : 'Draft' }}
            </span>
          </p>
          <div class="trip-links">
            <a 
              :href="`/marketing/trips/${trip.slug}`" 
              target="_blank" 
              class="btn btn-sm btn-outline-primary me-2"
            >
              <i class="fas fa-external-link-alt me-1"></i>Public Page
            </a>
            <a 
              v-if="trip.private_token" 
              :href="`/marketing/trips/private/${trip.private_token}`" 
              target="_blank" 
              class="btn btn-sm btn-outline-secondary"
            >
              <i class="fas fa-lock me-1"></i>Private Page
            </a>
          </div>
        </div>
      </div>
      
      <!-- Create new trip -->
      <TripCreator 
        :quote="quote" 
        @trip-created="handleTripCreated"
      />
    </div>

    <!-- Marketing Kit Progress and Status -->
    <div class="row g-3 mb-3">
      <div class="col-md-3">
        <label class="form-label">Marketing kit file location</label>
        <input 
          v-model="form.marketing_kit_location" 
          class="form-control bg-warning" 
          readonly
        />
      </div>
      <div class="col-md-3">
        <label class="form-label">Marketing kit progress</label>
        <select v-model="form.marketing_kit_progress" class="form-select">
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="delivered">Delivered</option>
          <option value="completed">Completed</option>
        </select>
      </div>
      <div class="col-md-3">
        <label class="form-label">Marketing Kit Shipped</label>
        <select v-model="form.marketing_kit_shipped" class="form-select">
          <option value="NO">NO</option>
          <option value="YES">YES</option>
        </select>
      </div>
      <div class="col-md-3">
        <label class="form-label">Tracking Number</label>
        <input 
          v-model="form.tracking_number" 
          class="form-control"
        />
      </div>
    </div>

    <!-- Publish on Website -->
    <div class="row g-3 mb-3">
      <div class="col-md-12">
        <label class="form-label">Publish on Website</label>
        <select v-model="form.publish_on_website" class="form-select">
          <option value="NO">NO</option>
          <option value="YES">YES</option>
        </select>
      </div>
    </div>

    <!-- Private and Public Links -->
    <div class="row g-3 mb-3">
      <div class="col-md-12">
        <label class="form-label">Private Link</label>
        <input 
          v-model="form.private_link" 
          type="text" 
          class="form-control" 
          placeholder="Private link will be generated after creating a trip"
          readonly
        />
        <small class="form-text text-muted">
          This private link allows internal access to view and manage the trip.
        </small>
      </div>
    </div>

    <div class="row g-3 mb-3">
      <div class="col-md-12">
        <label class="form-label">Public Link</label>
        <input 
          v-model="form.public_link" 
          type="text" 
          class="form-control" 
          placeholder="Public link will be generated after creating a trip"
          readonly
        />
        <small class="form-text text-muted">
          This public link is what you share with potential travelers.
        </small>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import TripCreator from './TripCreator.vue'

// Define props - THIS WAS MISSING
const props = defineProps({
  quote: {
    type: Object,
    default: null
  }
})

// Define emits
const emit = defineEmits(['trip-created'])

const form = defineModel()
const fileInputs = ref({})

const handleTripCreated = (tripData) => {
  console.log('New trip created in MarketingBlock:', tripData)
  
  // Update the form with correct URLs
  if (tripData.slug || tripData.trip_slug) {
    const slug = tripData.trip_slug || tripData.slug
    form.value.public_link = `/trips/${slug}`
  }
  
  if (tripData.private_token) {
    form.value.private_link = `/trips/private/${tripData.private_token}`
  }
  
  // Emit event to parent
  emit('trip-created', tripData)
}

// Show marketing block only for specific workflow statuses
const shouldShowMarketing = computed(() => {
  const marketingStatuses = [60, 70, 80, 90]
  return marketingStatuses.includes(form.value?.workflow_status_rel)
})

// File handling functions
function getFileName(fieldName) {
  const file = form.value?.[fieldName]
  if (!file) return ''
  
  if (file instanceof File) {
    return file.name
  } else if (typeof file === 'string') {
    return file.split('/').pop() || file
  }
  
  return ''
}

function handleFileUpload(fieldName, event) {
  const file = event.target.files[0]
  if (file) {
    form.value[fieldName] = file
    console.log(`Uploaded ${fieldName}:`, file.name)
  }
}

function triggerFileInput(fieldName) {
  const input = fileInputs.value[fieldName]
  if (input) {
    input.click()
  }
}

function clearFile(fieldName) {
  form.value[fieldName] = null
  const input = fileInputs.value[fieldName]
  if (input) {
    input.value = ''
  }
}

function showFile(fieldName) {
  if (form.value[fieldName]) {
    if (form.value[fieldName] instanceof File) {
      const url = URL.createObjectURL(form.value[fieldName])
      window.open(url, '_blank')
    } else if (typeof form.value[fieldName] === 'string') {
      window.open(form.value[fieldName], '_blank')
    }
  }
}
</script>

<style scoped>
.trip-card {
  background-color: #f8f9fa;
}

.existing-trips {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
  background-color: #fff;
}

.marketing-section {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background-color: #f8f9fa;
  margin-bottom: 20px;
}
</style>