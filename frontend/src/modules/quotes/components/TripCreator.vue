<!-- filepath: /Users/cristian/Documents/nativity-crm/frontend/src/modules/quotes/components/TripCreator.vue -->
<script setup>
import { ref, computed, onMounted } from 'vue'
// Use the same HTTP client as your quotes app
import http from '@/shared/services/http'

const props = defineProps({
  quote: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['trip-created'])

// Reactive data
const templates = ref([])
const selectedTemplate = ref('')
const loading = ref(false)
const creating = ref(false)
const message = ref('')
const messageType = ref('success')
const createdTrip = ref(null)

const customization = ref({
  title: '',
  description: '',
  trip_name: ''
})

// Computed
const selectedTemplateData = computed(() => {
  if (!selectedTemplate.value) return null
  return templates.value.find(t => t.id === selectedTemplate.value)
})

// Methods
const loadTemplates = async () => {
  try {
    loading.value = true
    console.log('Loading templates using main HTTP client...')
    
    // FIXED: Add the /api/ prefix to match your Django URL patterns
    const response = await http.get('/api/marketing/templates/')
    templates.value = response.data.results || response.data
    console.log('Loaded templates:', templates.value)
  } catch (error) {
    console.error('Failed to load templates:', error)
    console.error('Error response:', error.response?.data)
    showMessage('Failed to load templates. Please try again.', 'danger')
  } finally {
    loading.value = false
  }
}

const onTemplateChange = () => {
  // Reset customization when template changes
  customization.value = {
    title: '',
    description: '',
    trip_name: ''
  }
  message.value = ''
}

const createTrip = async () => {
  if (!selectedTemplate.value) {
    showMessage('Please select a template', 'warning')
    return
  }

  try {
    creating.value = true
    
    const payload = {
      template_id: selectedTemplate.value,
      customizations: {
        custom_title: customization.value.title,
        custom_description: customization.value.description,
        trip_name: customization.value.trip_name
      }
    }

    const response = await http.post(`/api/marketing/quotes/${props.quote.id}/create-trip/`, payload)
    
    console.log('Create trip response:', response.data)
    
    createdTrip.value = response.data
    showMessage('Trip created successfully!', 'success')
    
    // Generate complete URLs with domain
    const baseUrl = window.location.origin // http://localhost:3000
    const publicUrl = `${baseUrl}/trips/${response.data.trip_slug || response.data.slug}`
    const privateUrl = response.data.private_token 
      ? `${baseUrl}/trips/private/${response.data.private_token}` 
      : null
    
    // Emit event to parent with complete URLs
    emit('trip-created', {
      ...response.data,
      trip_name: response.data.trip_name,
      slug: response.data.trip_slug || response.data.slug,
      private_token: response.data.private_token,
      public_url: publicUrl,
      private_url: privateUrl
    })
    
    // Reset form
    selectedTemplate.value = ''
    customization.value = {
      title: '',
      description: '',
      trip_name: ''
    }
    
  } catch (error) {
    console.error('Failed to create trip:', error)
    const errorMsg = error.response?.data?.error || error.response?.data?.detail || 'Failed to create trip. Please try again.'
    showMessage(errorMsg, 'danger')
  } finally {
    creating.value = false
  }
}

const showMessage = (msg, type = 'success') => {
  message.value = msg
  messageType.value = type
  
  // Auto-hide success messages after 5 seconds
  if (type === 'success') {
    setTimeout(() => {
      message.value = ''
    }, 5000)
  }
}

onMounted(() => {
  loadTemplates()
})

// Add copy to clipboard function
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    showMessage('Link copied to clipboard!', 'success')
  } catch (err) {
    console.error('Failed to copy: ', err)
    showMessage('Failed to copy link', 'danger')
  }
}
</script>

<template>
  <div class="trip-creator">
    <h5>Create Marketing Trip</h5>
    
    <!-- Loading State -->
    <div v-if="loading" class="text-center mb-3">
      <div class="spinner-border spinner-border-sm" role="status">
        <span class="visually-hidden">Loading templates...</span>
      </div>
      <span class="ms-2">Loading templates...</span>
    </div>
    
    <!-- Template Selection -->
    <div class="mb-3" v-else>
      <label class="form-label">Select Trip Template</label>
      <select v-model="selectedTemplate" class="form-select" @change="onTemplateChange">
        <option value="">-- Select a Template --</option>
        <option 
          v-for="template in templates" 
          :key="template.id" 
          :value="template.id"
        >
          {{ template.name }} ({{ template.duration_days }} days) - {{ template.destination }}
        </option>
      </select>
      
      <!-- Show message if no templates available -->
      <div v-if="templates.length === 0 && !loading" class="alert alert-info mt-2">
        <i class="fas fa-info-circle me-2"></i>
        No trip templates available. Please create templates in the marketing module first.
      </div>
    </div>

    <!-- Template Preview -->
    <div v-if="selectedTemplateData" class="template-preview mb-3 p-3 border rounded">
      <h6><i class="fas fa-eye me-2"></i>Template Preview:</h6>
      <div class="row">
        <div class="col-md-6">
          <p><strong>Title:</strong> {{ selectedTemplateData.trip_title }}</p>
          <p><strong>Destination:</strong> {{ selectedTemplateData.destination }}</p>
        </div>
        <div class="col-md-6">
          <p><strong>Duration:</strong> {{ selectedTemplateData.duration_days }} days</p>
          <p><strong>Status:</strong> 
            <span :class="selectedTemplateData.is_active ? 'text-success' : 'text-warning'">
              {{ selectedTemplateData.is_active ? 'Active' : 'Inactive' }}
            </span>
          </p>
        </div>
      </div>
      <p><strong>Description:</strong></p>
      <p class="text-muted">{{ selectedTemplateData.trip_description }}</p>
    </div>

    <!-- Auto-populated Info -->
    <div v-if="selectedTemplate" class="auto-populated-info mb-3 p-3 bg-light rounded">
      <h6><i class="fas fa-magic me-2"></i>Auto-populated Information:</h6>
      <div class="row">
        <div class="col-md-6">
          <p><strong>Trip Name:</strong> {{ selectedTemplateData?.name }} - {{ props.quote?.church_name || 'Church Name' }}</p>
          <p><strong>Church:</strong> {{ props.quote?.church_name || 'N/A' }}</p>
        </div>
        <div class="col-md-6">
          <p><strong>Spiritual Director:</strong> {{ props.quote?.leader_name || 'N/A' }}</p>
          <p><strong>Departure:</strong> {{ props.quote?.departure_date || 'N/A' }}</p>
        </div>
      </div>
      <p><strong>Price:</strong> ${{ props.quote?.total_cost || 'N/A' }}</p>
    </div>

    <!-- Trip Customization -->
    <div v-if="selectedTemplate" class="customization-section mb-3">
      <h6><i class="fas fa-edit me-2"></i>Customize Trip (Optional)</h6>
      
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label">Custom Trip Title</label>
          <input 
            v-model="customization.title" 
            type="text" 
            class="form-control"
            :placeholder="selectedTemplateData?.trip_title"
          />
        </div>
        <div class="col-md-6">
          <label class="form-label">Trip Name Override</label>
          <input 
            v-model="customization.trip_name" 
            type="text" 
            class="form-control"
            :placeholder="`${selectedTemplateData?.name} - ${props.quote?.church_name || 'Church Name'}`"
          />
        </div>
      </div>

      <div class="mt-3">
        <label class="form-label">Custom Description</label>
        <textarea 
          v-model="customization.description" 
          class="form-control" 
          rows="3"
          :placeholder="selectedTemplateData?.trip_description"
        ></textarea>
      </div>
    </div>

    <!-- Create Trip Actions -->
    <div class="form-actions d-flex gap-2">
      <button 
        type="button"
        class="btn btn-primary"
        @click="createTrip"
        :disabled="!selectedTemplate || creating"
      >
        <i class="fas fa-plus me-2"></i>
        {{ creating ? 'Creating...' : 'Create Marketing Trip' }}
      </button>
      
      <button 
        type="button"
        class="btn btn-outline-secondary"
        @click="loadTemplates"
        :disabled="loading || creating"
      >
        <i class="fas fa-refresh me-2"></i>
        Refresh Templates
      </button>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="message" class="mt-3">
      <div :class="`alert alert-${messageType}`" role="alert">
        <i class="fas" :class="{
          'fa-check-circle': messageType === 'success',
          'fa-exclamation-triangle': messageType === 'warning',
          'fa-times-circle': messageType === 'danger'
        }" ></i>
        {{ message }}
      </div>
    </div>

    <!-- Show created trip info with complete URLs -->
    <div v-if="createdTrip" class="created-trip mt-3 p-3 border border-success rounded">
      <h6 class="text-success"><i class="fas fa-check-circle me-2"></i>Trip Created Successfully!</h6>
      <p><strong>Trip Name:</strong> {{ createdTrip.trip_name }}</p>
      <p><strong>Slug:</strong> {{ createdTrip.trip_slug || createdTrip.slug }}</p>
      
      <!-- Show complete URLs -->
      <div class="link-section mb-3">
        <label class="form-label"><strong>Public Link:</strong></label>
        <div class="input-group mb-2">
          <input 
            type="text" 
            class="form-control" 
            :value="`${window.location.origin}/trips/${createdTrip.trip_slug || createdTrip.slug}`" 
            readonly 
          />
          <button class="btn btn-outline-secondary" @click="copyToClipboard(`${window.location.origin}/trips/${createdTrip.trip_slug || createdTrip.slug}`)">
            <i class="fas fa-copy"></i>
          </button>
        </div>
        
        <label class="form-label"><strong>Private Link:</strong></label>
        <div class="input-group mb-3">
          <input 
            type="text" 
            class="form-control" 
            :value="createdTrip.private_token ? `${window.location.origin}/trips/private/${createdTrip.private_token}` : 'No private token available'" 
            readonly 
          />
          <button 
            v-if="createdTrip.private_token"
            class="btn btn-outline-secondary" 
            @click="copyToClipboard(`${window.location.origin}/trips/private/${createdTrip.private_token}`)"
          >
            <i class="fas fa-copy"></i>
          </button>
        </div>
      </div>
      
      <div class="d-flex gap-2">
        <a 
          :href="`${window.location.origin}/trips/${createdTrip.trip_slug || createdTrip.slug}`" 
          target="_blank" 
          class="btn btn-sm btn-outline-primary"
        >
          <i class="fas fa-external-link-alt me-1"></i>View Public Page
        </a>
        <a 
          v-if="createdTrip.private_token" 
          :href="`${window.location.origin}/trips/private/${createdTrip.private_token}`" 
          target="_blank" 
          class="btn btn-sm btn-outline-secondary"
        >
          <i class="fas fa-lock me-1"></i>View Private Page
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trip-creator {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background-color: #f8f9fa;
}

.template-preview {
  background-color: #fff;
  border-color: #dee2e6;
}

.auto-populated-info {
  border: 1px solid #d1ecf1;
}

.customization-section {
  background-color: #fff;
  padding: 15px;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.created-trip {
  background-color: #f8fff8;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>