<!-- filepath: /Users/cristian/Documents/nativity-crm/frontend/src/modules/settings/pages/TripTemplateManager.vue -->
<template>
  <div class="trip-template-manager">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4>Trip Templates</h4>
        <p class="text-muted">Manage templates for creating marketing trips from quotes</p>
      </div>
      <button class="btn btn-primary" @click="openCreateForm">
        <i class="fas fa-plus me-2"></i>Create New Template
      </button>
    </div>

    <!-- Statistics Cards -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <h5>{{ templates.length }}</h5>
            <small>Total Templates</small>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-success text-white">
          <div class="card-body">
            <h5>{{ activeTemplates }}</h5>
            <small>Active Templates</small>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-warning text-white">
          <div class="card-body">
            <h5>{{ inactiveTemplates }}</h5>
            <small>Inactive Templates</small>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-info text-white">
          <div class="card-body">
            <h5>{{ uniqueDestinations }}</h5>
            <small>Destinations</small>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters mb-3">
      <div class="row g-3">
        <div class="col-md-4">
          <input 
            v-model="searchTerm" 
            type="text" 
            class="form-control" 
            placeholder="Search templates..."
          />
        </div>
        <div class="col-md-3">
          <select v-model="filterDestination" class="form-select">
            <option value="">All Destinations</option>
            <option v-for="dest in destinations" :key="dest" :value="dest">
              {{ dest }}
            </option>
          </select>
        </div>
        <div class="col-md-3">
          <select v-model="filterStatus" class="form-select">
            <option value="">All Status</option>
            <option value="active">Active Only</option>
            <option value="inactive">Inactive Only</option>
          </select>
        </div>
        <div class="col-md-2">
          <button class="btn btn-outline-secondary w-100" @click="clearFilters">
            <i class="fas fa-times me-1"></i>Clear
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="modal show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ editingTemplate ? 'Edit Template' : 'Create New Template' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          
          <form @submit.prevent="saveTemplate">
            <div class="modal-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Template Name *</label>
                  <input 
                    v-model="form.name" 
                    type="text" 
                    class="form-control" 
                    required
                    placeholder="e.g., Holy Land Pilgrimage"
                  />
                </div>
                
                <div class="col-md-6">
                  <label class="form-label">Destination *</label>
                  <input 
                    v-model="form.destination" 
                    type="text" 
                    class="form-control" 
                    required
                    placeholder="e.g., Jerusalem, Israel"
                  />
                </div>
                
                <div class="col-md-6">
                  <label class="form-label">Duration (Days) *</label>
                  <input 
                    v-model="form.duration_days" 
                    type="number" 
                    class="form-control" 
                    required
                    min="1"
                    max="365"
                  />
                </div>
                
                <div class="col-md-6">
                  <label class="form-label">Trip Title *</label>
                  <input 
                    v-model="form.trip_title" 
                    type="text" 
                    class="form-control" 
                    required
                    placeholder="e.g., Journey to the Holy Land"
                  />
                </div>
                
                <div class="col-12">
                  <label class="form-label">Trip Description</label>
                  <textarea 
                    v-model="form.trip_description" 
                    class="form-control" 
                    rows="4"
                    placeholder="Detailed description of the trip itinerary, highlights, and what's included..."
                  ></textarea>
                </div>

                <div class="col-md-6">
                  <label class="form-label">Base Price</label>
                  <div class="input-group">
                    <span class="input-group-text">$</span>
                    <input 
                      v-model="form.base_price" 
                      type="number" 
                      class="form-control" 
                      step="0.01"
                      placeholder="0.00"
                    />
                  </div>
                </div>

                <div class="col-md-6">
                  <label class="form-label">Category</label>
                  <select v-model="form.category" class="form-select">
                    <option value="">Select Category</option>
                    <option value="pilgrimage">Pilgrimage</option>
                    <option value="cultural">Cultural</option>
                    <option value="educational">Educational</option>
                    <option value="spiritual">Spiritual Retreat</option>
                    <option value="adventure">Adventure</option>
                    <option value="leisure">Leisure</option>
                  </select>
                </div>

                <div class="col-12">
                  <label class="form-label">Included Services</label>
                  <textarea 
                    v-model="form.included_services" 
                    class="form-control" 
                    rows="3"
                    placeholder="e.g., Round-trip airfare, First-class hotels, All meals, Professional guide..."
                  ></textarea>
                </div>

                <div class="col-12">
                  <label class="form-label">Not Included</label>
                  <textarea 
                    v-model="form.not_included" 
                    class="form-control" 
                    rows="3"
                    placeholder="e.g., Travel insurance, Personal expenses, Optional excursions..."
                  ></textarea>
                </div>
                
                <div class="col-md-6">
                  <div class="form-check">
                    <input 
                      v-model="form.is_active" 
                      class="form-check-input" 
                      type="checkbox" 
                      id="isActive"
                    />
                    <label class="form-check-label" for="isActive">
                      Active Template
                    </label>
                    <small class="form-text text-muted d-block">
                      Only active templates will be available for creating trips
                    </small>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="saving">
                <i class="fas fa-save me-2"></i>
                {{ saving ? 'Saving...' : (editingTemplate ? 'Update Template' : 'Create Template') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Templates List -->
    <div class="templates-list">
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading templates...</span>
        </div>
        <p class="mt-2">Loading templates...</p>
      </div>
      
      <div v-else-if="filteredTemplates.length === 0" class="text-center py-5">
        <div class="alert alert-info">
          <i class="fas fa-info-circle me-2"></i>
          {{ templates.length === 0 ? 'No templates found. Create your first template to get started!' : 'No templates match your current filters.' }}
        </div>
      </div>
      
      <div v-else class="row">
        <div 
          v-for="template in filteredTemplates" 
          :key="template.id"
          class="col-md-6 col-lg-4 mb-4"
        >
          <div class="card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h6 class="mb-0">{{ template.name }}</h6>
              <span :class="`badge ${template.is_active ? 'bg-success' : 'bg-warning'}`">
                {{ template.is_active ? 'Active' : 'Inactive' }}
              </span>
            </div>
            
            <div class="card-body">
              <p class="card-text">
                <strong>Destination:</strong> {{ template.destination }}<br>
                <strong>Duration:</strong> {{ template.duration_days }} days<br>
                <strong>Category:</strong> {{ template.category || 'Not specified' }}<br>
                <strong>Base Price:</strong> {{ template.base_price ? `$${template.base_price}` : 'Not set' }}
              </p>
              
              <p class="card-text">
                <strong>Title:</strong> {{ template.trip_title }}
              </p>
              
              <p class="card-text text-muted">
                {{ template.trip_description ? template.trip_description.substring(0, 100) + '...' : 'No description' }}
              </p>
            </div>
            
            <div class="card-footer">
              <div class="btn-group w-100">
                <button 
                  class="btn btn-sm btn-outline-primary"
                  @click="editTemplate(template)"
                >
                  <i class="fas fa-edit"></i> Edit
                </button>
                <button 
                  class="btn btn-sm btn-outline-info"
                  @click="duplicateTemplate(template)"
                >
                  <i class="fas fa-copy"></i> Copy
                </button>
                <button 
                  class="btn btn-sm btn-outline-danger"
                  @click="deleteTemplate(template)"
                >
                  <i class="fas fa-trash"></i> Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import http from '@/shared/services/http'

// Reactive data
const templates = ref([])
const loading = ref(false)
const saving = ref(false)
const showModal = ref(false)
const editingTemplate = ref(null)
const searchTerm = ref('')
const filterDestination = ref('')
const filterStatus = ref('')

const form = ref({
  name: '',
  destination: '',
  duration_days: '',
  trip_title: '',
  trip_description: '',
  base_price: '',
  category: '',
  included_services: '',
  not_included: '',
  is_active: true
})

// Computed properties
const activeTemplates = computed(() => 
  templates.value.filter(t => t.is_active).length
)

const inactiveTemplates = computed(() => 
  templates.value.filter(t => !t.is_active).length
)

const destinations = computed(() => 
  [...new Set(templates.value.map(t => t.destination).filter(Boolean))]
)

const uniqueDestinations = computed(() => destinations.value.length)

const filteredTemplates = computed(() => {
  let filtered = templates.value

  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    filtered = filtered.filter(t => 
      t.name.toLowerCase().includes(term) ||
      t.destination.toLowerCase().includes(term) ||
      t.trip_title.toLowerCase().includes(term) ||
      (t.trip_description && t.trip_description.toLowerCase().includes(term))
    )
  }

  if (filterDestination.value) {
    filtered = filtered.filter(t => t.destination === filterDestination.value)
  }

  if (filterStatus.value === 'active') {
    filtered = filtered.filter(t => t.is_active)
  } else if (filterStatus.value === 'inactive') {
    filtered = filtered.filter(t => !t.is_active)
  }

  return filtered
})

// Methods
const loadTemplates = async () => {
  try {
    loading.value = true
    const response = await http.get('/api/marketing/templates/')
    templates.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to load templates:', error)
    alert('Failed to load templates. Please check your connection and try again.')
  } finally {
    loading.value = false
  }
}

const openCreateForm = () => {
  editingTemplate.value = null
  resetForm()
  showModal.value = true
}

const editTemplate = (template) => {
  editingTemplate.value = template
  form.value = { ...template }
  showModal.value = true
}

const duplicateTemplate = (template) => {
  editingTemplate.value = null
  form.value = { 
    ...template, 
    name: `${template.name} (Copy)`,
    id: undefined
  }
  showModal.value = true
}

const saveTemplate = async () => {
  try {
    saving.value = true
    
    if (editingTemplate.value) {
      await http.put(`/api/marketing/templates/${editingTemplate.value.id}/`, form.value)
    } else {
      await http.post('/api/marketing/templates/', form.value)
    }
    
    await loadTemplates()
    closeModal()
    
    const action = editingTemplate.value ? 'updated' : 'created'
    alert(`Template ${action} successfully!`)
  } catch (error) {
    console.error('Failed to save template:', error)
    const errorMsg = error.response?.data?.error || 'Failed to save template'
    alert(errorMsg)
  } finally {
    saving.value = false
  }
}

const deleteTemplate = async (template) => {
  if (!confirm(`Are you sure you want to delete "${template.name}"?\n\nThis action cannot be undone.`)) {
    return
  }
  
  try {
    await http.delete(`/api/marketing/templates/${template.id}/`)
    await loadTemplates()
    alert('Template deleted successfully!')
  } catch (error) {
    console.error('Failed to delete template:', error)
    alert('Failed to delete template. It may be in use by existing trips.')
  }
}

const closeModal = () => {
  showModal.value = false
  editingTemplate.value = null
  resetForm()
}

const resetForm = () => {
  form.value = {
    name: '',
    destination: '',
    duration_days: '',
    trip_title: '',
    trip_description: '',
    base_price: '',
    category: '',
    included_services: '',
    not_included: '',
    is_active: true
  }
}

const clearFilters = () => {
  searchTerm.value = ''
  filterDestination.value = ''
  filterStatus.value = ''
}

onMounted(() => {
  loadTemplates()
})
</script>

<style scoped>
.trip-template-manager {
  padding: 20px;
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}

.modal.show {
  display: block;
}

.btn-group .btn {
  flex: 1;
}

.filters {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.badge {
  font-size: 0.75em;
}
</style>