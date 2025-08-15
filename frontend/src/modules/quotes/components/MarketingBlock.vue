<template>
  <div v-if="shouldShowMarketing">
    <hr class="mt-4">
    <h4 class="mb-3">Marketing</h4>
    
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
          rows="8"
          placeholder="Round-Trip Airfare&#10;Airport taxes & fuel surcharges&#10;First-Class Hotels&#10;Land Transportation"
        ></textarea>
      </div>
      <div class="col-md-6">
        <label class="form-label">Trip Does Not Include</label>
        <textarea 
          v-model="form.trip_not_includes" 
          class="form-control" 
          rows="8"
          placeholder="Trip Cancellation Insurance&#10;Lunch&#10;Personal Items"
        ></textarea>
      </div>
    </div>

    <!-- Marketing Template Section -->
    <div class="marketing-section mb-4" v-if="quote">
      <h5>Marketing Trip</h5>

      <!-- Template selection and trip creation -->
      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <label class="form-label">Marketing Trip Template</label>
          <select v-model="selectedTemplate" class="form-select">
            <option value="">-- Select Template --</option>
            <option v-for="tpl in templates" :key="tpl.id" :value="tpl.id">
              {{ tpl.name }}
            </option>
          </select>
        </div>
        <div class="col-md-6 d-flex align-items-end">
          <button class="btn btn-success" :disabled="!selectedTemplate || creatingTrip" @click="createMarketingTrip">
            {{ creatingTrip ? 'Creating…' : 'Create Marketing Trip' }}
          </button>
        </div>
      </div>

      <!-- Show trip links if created -->
      <div v-if="tripLinks.public || tripLinks.private" class="alert alert-info mb-3">
        <div v-if="tripLinks.public">
          <strong>Public Link:</strong>
          <a :href="tripLinks.public" target="_blank">{{ tripLinks.public }}</a>
        </div>
        <div v-if="tripLinks.private">
          <strong>Private Link:</strong>
          <a :href="tripLinks.private" target="_blank">{{ tripLinks.private }}</a>
        </div>
      </div>

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
          :placeholder="form.private_link ? form.private_link : 'Private link will be generated after creating a trip'"
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
          :placeholder="form.public_link ? form.public_link : 'Public link will be generated after creating a trip'"
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
import { ref, computed, onMounted } from 'vue'
import http from '@/shared/services/http'
const form = defineModel()
const props = defineProps({
  quote: {
    type: Object,
    default: null
  }
})
const emit = defineEmits(['trip-created'])
const fileInputs = ref({})

const templates = ref([])
const selectedTemplate = ref('')
const tripLinks = ref({ public: '', private: '' })
const creatingTrip = ref(false)

const shouldShowMarketing = computed(() => {
  const marketingStatuses = [60, 70, 80, 90]
  return marketingStatuses.includes(form.value?.workflow_status_rel)
})

async function loadTemplates() {
  try {
    const response = await http.get('/api/marketing/templates/')
    templates.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to load templates:', error)
  }
}


async function createMarketingTrip() {
  if (!selectedTemplate.value || !props.quote?.id) return
  creatingTrip.value = true
  try {
    const response = await http.post('/api/marketing/create-trip/', {
      quote_id: props.quote.id,
      template_id: selectedTemplate.value
    })
    // Show links in alert
    tripLinks.value.public = response.data.public_link
    tripLinks.value.private = response.data.private_link
    // Persist links to backend quote record
    await http.patch(`/api/quotes/${props.quote.id}/`, {
      marketing_public_link: response.data.public_link,
      marketing_private_link: response.data.private_link
    })
    emit('trip-created', response.data)
  } catch (error) {
    console.error('Failed to create marketing trip:', error)
    alert('Failed to create marketing trip.')
  } finally {
    creatingTrip.value = false
  }
}

onMounted(() => {
  loadTemplates()
})


// Removed handleTripCreated: parent should reload quote and update form fields after trip creation

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

<!-- MyComponent.vue (or .jsx/.svelte – anywhere that supports <style scoped>) -->
<style scoped>
/* ---------------------------------------------------------------------------
   1.  Load the font once
--------------------------------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

/* ---------------------------------------------------------------------------
   2.  Base-typography variables
--------------------------------------------------------------------------- */
:root {
  --base-font-family: 'Roboto', 'Montserrat', sans-serif;
  --base-font-size  : 14px;
  --base-font-weight: 400;
}

/* Put this class on the outer-most element of the component
   <div class="typography-root"> … </div>                                   */
.typography-root {
  font: var(--base-font-weight) var(--base-font-size)/1.5 var(--base-font-family);
}

/* Every child now *inherits* from .typography-root, so we don’t have to
   use the heavy universal selector (*) any more.                           */

/* ---------------------------------------------------------------------------
   3.  Preserve Font Awesome icons
--------------------------------------------------------------------------- */
.fa, .fas, .far, .fal, .fad, .fab,
[class^="fa-"], [class*=" fa-"] {
  font-family:
    "Font Awesome 6 Free",
    "Font Awesome 6 Pro",
    "Font Awesome 6 Brands",
    "Font Awesome 5 Free",
    "Font Awesome 5 Pro",
    "FontAwesome" !important;
  font-weight: 900;          /* solid style icons need this */
}

/* ---------------------------------------------------------------------------
   4.  Make form controls & buttons inherit the typography
--------------------------------------------------------------------------- */
button, input, textarea, select {
  font: inherit;
}

/* ---------------------------------------------------------------------------
   5.  Component-specific helpers
--------------------------------------------------------------------------- */
.trip-card         { background-color: #f8f9fa; }

.existing-trips {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1rem;
  background-color: #fff;
}

.marketing-section {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.25rem;
  background-color: #f8f9fa;
  margin-bottom: 1.25rem;
}
</style>