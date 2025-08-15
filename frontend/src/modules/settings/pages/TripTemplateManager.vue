<!-- filepath: /Users/cristian/Documents/nativity-crm/frontend/src/modules/settings/pages/TripTemplateManager.vue -->
<template>
  <div class="trip-template-manager">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4>Trip Templates</h4>
        <p class="text-muted">Manage templates for creating marketing trips from quotes</p>
      </div>
      <div class="d-flex">
        <button class="btn btn-primary me-2" @click="openCreateForm">
          <i class="fas fa-plus me-2"></i>Create New Template
        </button>
        <button class="btn btn-secondary" @click="openManageDestinationsModal">
          <i class="fas fa-map-marker-alt me-2"></i>Manage Destinations
        </button>
      </div>
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
            <h5>{{ destinations.length }}</h5>
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
            <option v-for="dest in destinations" :key="dest.id" :value="dest.id">
              {{ dest.name }}
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

    <!-- Manage Destinations Modal -->
    <div v-if="showManageDestinationsModal" class="modal show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Manage Destinations</h5>
            <button type="button" class="btn-close" @click="closeManageDestinationsModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveDestination">
              <div class="mb-3">
                <label class="form-label">Destination Name</label>
                <input 
                  v-model="newDestination" 
                  type="text" 
                  class="form-control" 
                  placeholder="e.g., Jerusalem, Israel"
                />
                <div v-if="destinationError" class="text-danger mt-1">{{ destinationError }}</div>
              </div>
              <button type="submit" class="btn btn-primary" :disabled="!newDestination.trim()">Add Destination</button>
            </form>
            <ul class="list-group mt-3">
              <li v-for="dest in destinations" :key="dest.id" class="list-group-item d-flex justify-content-between align-items-center">
                {{ dest.name }}
                <button class="btn btn-danger btn-sm" @click="removeDestination(dest.id)">
                  <i class="fas fa-trash"></i>
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Delete Template</h5>
            <button type="button" class="btn-close" @click="cancelDeleteTemplate"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete "{{ templateToDelete?.name }}"?</p>
            <p class="text-danger">This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="cancelDeleteTemplate">Cancel</button>
            <button class="btn btn-danger" @click="confirmDeleteTemplate">Delete</button>
          </div>
        </div>
      </div>
    </div>
    <!-- End Delete Confirmation Modal -->

    <!-- Success Modal -->
    <div v-if="showSuccessModal" class="modal show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Success</h5>
            <button type="button" class="btn-close" @click="closeSuccessModal"></button>
          </div>
          <div class="modal-body">
            <p>{{ successMessage }}</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-primary" @click="closeSuccessModal">OK</button>
          </div>
        </div>
      </div>
    </div>
    <!-- End Success Modal -->

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
              <p class="card-text mb-1">
                <strong>Destination:</strong> {{ getDestinationName(template.destination) }}
              </p>
              <p class="card-text mb-1">
                <strong>Name:</strong> {{ template.name }}
              </p>
              <p class="card-text mb-1">
                <strong>Title:</strong> {{ template.trip_title }}
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
import { useRouter } from 'vue-router'
import http from '@/shared/services/http'

const router = useRouter()

const templates = ref([])
const destinations = ref([])

const showManageDestinationsModal = ref(false)
const showDeleteModal = ref(false)
const templateToDelete = ref(null)
const showSuccessModal = ref(false)
const successMessage = ref('')
const newDestination = ref('')
const loading = ref(false)
const searchTerm = ref('')
const filterDestination = ref('')
const filterStatus = ref('')
const destinationError = ref('')

function getDestinationName(destId) {
  const dest = destinations.value.find(d => d.id === destId)
  return dest ? dest.name : ''
}

const activeTemplates = computed(() =>
  templates.value.filter(t => t.is_active).length
)
const inactiveTemplates = computed(() =>
  templates.value.filter(t => !t.is_active).length
)
const uniqueDestinations = computed(() =>
  [...new Set(templates.value.map(t => t.destination).filter(Boolean))].length
)
const filteredTemplates = computed(() => {
  let filtered = templates.value
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    filtered = filtered.filter(t => {
      const destName = getDestinationName(t.destination)?.toLowerCase() || ''
      return (
        t.name?.toLowerCase().includes(term) ||
        destName.includes(term) ||
        t.trip_title?.toLowerCase().includes(term) ||
        (t.trip_description && t.trip_description.toLowerCase().includes(term))
      )
    })
  }
  if (filterDestination.value) {
    filtered = filtered.filter(t => String(t.destination) === String(filterDestination.value))
  }
  if (filterStatus.value === 'active') {
    filtered = filtered.filter(t => t.is_active)
  } else if (filterStatus.value === 'inactive') {
    filtered = filtered.filter(t => !t.is_active)
  }
  return filtered
})

const loadTemplates = async () => {
  try {
    loading.value = true
    const response = await http.get('/api/marketing/templates/')
    templates.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to load templates:', error)
  } finally {
    loading.value = false
  }
}

const loadDestinations = async () => {
  try {
    const response = await http.get('/api/marketing/template-destinations/')
    destinations.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to load destinations:', error)
  }
}

const openCreateForm = () => {
  router.push('/settings/trip-templates/create')
}

const openManageDestinationsModal = () => {
  showManageDestinationsModal.value = true
}

const closeManageDestinationsModal = () => {
  showManageDestinationsModal.value = false
}

const saveDestination = async () => {
  if (!newDestination.value.trim()) {
    destinationError.value = 'Destination name is required.'
    return
  }
  try {
    await http.post('/api/marketing/template-destinations/', { name: newDestination.value })
    newDestination.value = ''
    destinationError.value = ''
    await loadDestinations()
  } catch (error) {
    console.error('Failed to save destination:', error)
    destinationError.value = 'Failed to save destination.'
  }
}

const removeDestination = async (destId) => {
  try {
    await http.delete(`/api/marketing/template-destinations/${destId}/`)
    await loadDestinations()
  } catch (error) {
    console.error('Failed to remove destination:', error)
  }
}

const clearFilters = () => {
  searchTerm.value = ''
  filterDestination.value = ''
  filterStatus.value = ''
}

const editTemplate = (template) => {
  router.push(`/settings/trip-templates/edit/${template.id}`)
}

const duplicateTemplate = (template) => {
  router.push(`/settings/trip-templates/create?duplicate=${template.id}`)
}

const deleteTemplate = (template) => {
  templateToDelete.value = template
  showDeleteModal.value = true
}

const confirmDeleteTemplate = async () => {
  if (!templateToDelete.value) return
  try {
    await http.delete(`/api/marketing/templates/${templateToDelete.value.id}/`)
    await loadTemplates()
    successMessage.value = 'Template deleted successfully!'
    showSuccessModal.value = true
  } catch (error) {
    console.error('Failed to delete template:', error)
    successMessage.value = 'Failed to delete template. It may be in use by existing trips.'
    showSuccessModal.value = true
  } finally {
    showDeleteModal.value = false
    templateToDelete.value = null
  }
}

const closeSuccessModal = () => {
  showSuccessModal.value = false
  successMessage.value = ''
}

const cancelDeleteTemplate = () => {
  showDeleteModal.value = false
  templateToDelete.value = null
}

onMounted(() => {
  loadTemplates()
  loadDestinations()
})
</script>

<style scoped>
.trip-template-manager {
  padding: 20px;
}

.modal.show {
  display: block;
}

.list-group-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>