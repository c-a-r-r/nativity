<template>
  <div class="website-template-creator">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4>Create New Website Template</h4>
        <p class="text-muted">Create a comprehensive template for marketing trips</p>
      </div>
      <div class="d-flex">
        <button class="btn btn-secondary me-2" @click="goBack">
          <i class="fas fa-arrow-left me-2"></i>Back to Templates
        </button>
        <button class="btn btn-success" @click="saveTemplate" :disabled="saving">
          <i class="fas fa-save me-2"></i>
          {{ saving ? 'Saving...' : 'Save Template' }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading template...</span>
      </div>
      <p class="mt-2">{{ duplicateId ? 'Loading template for duplication...' : 'Loading...' }}</p>
    </div>

    <form v-else @submit.prevent="saveTemplate">
      <!-- Basic Information -->
      <div class="card mb-4">
        <div class="card-header">
          <h5 class="mb-0">Basic Information</h5>
        </div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">Template Name *</label>
              <input 
                v-model="form.name" 
                type="text" 
                class="form-control" 
                placeholder="e.g., Holy Land Template"
                required
              />
            </div>
            <div class="col-md-6">
              <label class="form-label">Destination *</label>
              <select v-model="form.destination" class="form-select" required>
                <option value="">Select destination</option>
                <option v-for="dest in destinations" :key="dest.id" :value="dest.id">
                  {{ dest.name }}
                </option>
              </select>
            </div>
            <div class="col-12">
              <label class="form-label">Trip Title *</label>
              <input 
                v-model="form.trip_title" 
                type="text" 
                class="form-control" 
                placeholder="e.g., 10 DAYS HOLY LAND"
                required
              />
            </div>
            <div class="col-12">
              <label class="form-label">Promotional Text *</label>
              <textarea 
                v-model="form.promo_text" 
                class="form-control" 
                rows="4"
                placeholder="Enter compelling description that will attract pilgrims..."
                required
              ></textarea>
            </div>
            <div class="col-md-6">
              <label class="form-label">Hero Image *</label>
              <input 
                type="file" 
                accept="image/*" 
                @change="onHeroImageChange"
                class="form-control mb-2" 
                required
              />
              <div v-if="heroImageUploading" class="text-muted small mb-2">
                <i class="fas fa-spinner fa-spin me-1"></i>Uploading...
              </div>
              <div v-if="heroImageName || form.hero_image" class="mb-2 d-flex align-items-center gap-3">
                <img v-if="form.hero_image" :src="form.hero_image" alt="Hero Preview" style="max-width: 200px; max-height: 120px; border-radius: 6px; border: 1px solid #ccc;" />
                <span v-if="heroImageName" class="text-muted small">{{ heroImageName }}</span>
                <button v-if="form.hero_image" type="button" class="btn btn-sm btn-outline-danger" @click="removeHeroImage">Remove</button>
              </div>
            </div>
            <div class="col-md-6">
              <label class="form-label">Video Link</label>
              <input 
                v-model="form.video_link" 
                type="url" 
                class="form-control" 
                placeholder="https://www.youtube.com/embed/..."
              />
            </div>
            <div class="col-md-6">
              <label class="form-label">Brochure Link</label>
              <input 
                v-model="form.brochure_link" 
                type="url" 
                class="form-control" 
                placeholder="https://example.com/brochure.pdf"
              />
            </div>
            <div class="col-md-6">
              <div class="form-check form-switch mt-4">
                <input 
                  v-model="form.is_active" 
                  class="form-check-input" 
                  type="checkbox" 
                  id="activeSwitch"
                />
                <label class="form-check-label" for="activeSwitch">
                  Active Template
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Itinerary -->
      <div class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0">Itinerary</h5>
          <button type="button" class="btn btn-sm btn-primary" @click="addDay">
            <i class="fas fa-plus me-1"></i>Add Day
          </button>
        </div>
        <div class="card-body">
          <div v-if="form.itinerary.length === 0" class="text-center py-4">
            <p class="text-muted">No days added yet. Click "Add Day" to start building your itinerary.</p>
          </div>
          <div v-else>
            <div 
              v-for="(day, index) in form.itinerary" 
              :key="index"
              class="day-item mb-3 p-3 border rounded"
            >
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h6>Day {{ day.day }}</h6>
                <button 
                  type="button" 
                  class="btn btn-sm btn-outline-danger" 
                  @click="removeDay(index)"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
              <div class="row g-2">
                <div class="col-12">
                  <label class="form-label">Title *</label>
                  <input 
                    v-model="day.title" 
                    type="text" 
                    class="form-control" 
                    placeholder="e.g., Old City of Jerusalem"
                    required
                  />
                </div>
                <div class="col-12">
                  <label class="form-label">Description *</label>
                  <textarea 
                    v-model="day.description" 
                    class="form-control" 
                    rows="3"
                    placeholder="Describe the activities and sites for this day..."
                    required
                  ></textarea>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Gallery -->
      <div class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0">Gallery (Maximum 10 Images)</h5>
          <button 
            type="button" 
            class="btn btn-sm btn-primary" 
            @click="addGalleryImage"
            :disabled="form.gallery.length >= 10"
          >
            <i class="fas fa-plus me-1"></i>Add Image
          </button>
        </div>
        <div class="card-body">
          <div v-if="form.gallery.length === 0" class="text-center py-4">
            <p class="text-muted">No images added yet. Click "Add Image" to start building your gallery.</p>
          </div>
          <div v-else class="row g-3">
            <div 
              v-for="(image, index) in form.gallery" 
              :key="index"
              class="col-md-6 col-lg-4"
            >
              <div class="gallery-item p-3 border rounded">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <h6>Image {{ index + 1 }}</h6>
                  <button 
                    type="button" 
                    class="btn btn-sm btn-outline-danger" 
                    @click="removeGalleryImage(index)"
                  >
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
                
                <!-- Image Preview -->
                <div v-if="image.url" class="mb-2">
                  <img 
                    :src="image.url" 
                    :alt="image.title || 'Gallery image'"
                    class="img-fluid rounded"
                    style="height: 120px; width: 100%; object-fit: cover;"
                    @error="handleImageError"
                  />
                </div>
                
                <div class="mb-2">
                  <label class="form-label">Image Upload *</label>
                  <input 
                    type="file" 
                    accept="image/*" 
                    @change="(e) => onGalleryImageChange(e, index)"
                    class="form-control form-control-sm mb-2" 
                    required
                  />
                  <div v-if="image.uploading" class="text-muted small">
                    <i class="fas fa-spinner fa-spin me-1"></i>Uploading...
                  </div>
                  <div v-if="image.fileName" class="text-muted small">
                    <i class="fas fa-check me-1"></i>{{ image.fileName }}
                  </div>
                </div>
                <div class="mb-2">
                  <label class="form-label">Title *</label>
                  <input 
                    v-model="image.title" 
                    type="text" 
                    class="form-control form-control-sm" 
                    placeholder="e.g., Western Wall"
                    required
                  />
                </div>
                <div>
                  <label class="form-label">Description *</label>
                  <textarea 
                    v-model="image.description" 
                    class="form-control form-control-sm" 
                    rows="2"
                    placeholder="Describe this location or moment..."
                    required
                  ></textarea>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="d-flex justify-content-between">
        <button type="button" class="btn btn-secondary" @click="goBack">
          Cancel
        </button>
        <button type="submit" class="btn btn-success" :disabled="saving">
          <i class="fas fa-save me-2"></i>
          {{ saving ? 'Saving...' : 'Save Template' }}
        </button>
      </div>
    </form>

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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import http from '@/shared/services/http'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const destinations = ref([])
const saving = ref(false)
const loading = ref(false)
const showSuccessModal = ref(false)
const successMessage = ref('')
const duplicateId = route.query.duplicate
const heroImageName = ref('')
const heroImageUploading = ref(false)

const form = ref({
  name: '',
  trip_title: '',
  promo_text: '',
  hero_image: '',
  video_link: '',
  brochure_link: '',
  destination: '',
  is_active: true,
  itinerary: [],
  gallery: []
})

const loadDestinations = async () => {
  try {
    const response = await http.get('/api/marketing/template-destinations/')
    destinations.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to load destinations:', error)
  }
}

const loadTemplateForDuplication = async () => {
  if (!duplicateId) return
  
  try {
    loading.value = true
    const response = await http.get(`/api/marketing/templates/${duplicateId}/`)
    const template = response.data
    
    form.value = {
      name: `${template.name} (Copy)`,
      trip_title: template.trip_title || '',
      promo_text: template.promo_text || '',
      hero_image: template.hero_image || '',
      video_link: template.video_link || '',
      brochure_link: template.brochure_link || '',
      destination: template.destination || '',
      is_active: template.is_active !== undefined ? template.is_active : true,
      itinerary: typeof template.itinerary === 'string' ? JSON.parse(template.itinerary || '[]') : (template.itinerary || []),
      gallery: typeof template.gallery === 'string' ? 
        JSON.parse(template.gallery || '[]').map(item => ({
          url: item.url || '',
          title: item.title || '',
          description: item.description || '',
          fileName: item.fileName || '',
          uploading: false
        })) : 
        (template.gallery || []).map(item => ({
          url: item.url || '',
          title: item.title || '',
          description: item.description || '',
          fileName: item.fileName || '',
          uploading: false
        }))
    }
  } catch (error) {
    console.error('Failed to load template for duplication:', error)
  } finally {
    loading.value = false
  }
}

const addDay = () => {
  const newDay = {
    day: form.value.itinerary.length + 1,
    title: '',
    description: '',
    expanded: false
  }
  form.value.itinerary.push(newDay)
}

const removeDay = (index) => {
  form.value.itinerary.splice(index, 1)
  // Renumber the remaining days
  form.value.itinerary.forEach((day, idx) => {
    day.day = idx + 1
  })
}

const addGalleryImage = () => {
  if (form.value.gallery.length < 10) {
    form.value.gallery.push({
      url: '',
      title: '',
      description: '',
      fileName: '',
      uploading: false
    })
  }
}

const removeGalleryImage = (index) => {
  form.value.gallery.splice(index, 1)
}

const onGalleryImageChange = async (event, index) => {
  const file = event.target.files[0]
  if (!file) return
  
  // Set uploading state
  form.value.gallery[index].uploading = true
  form.value.gallery[index].fileName = file.name
  
  const formData = new FormData()
  formData.append('image', file)
  
  try {
    const response = await axios.post('/api/marketing/upload-image/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    // Update the gallery item with the uploaded URL
    form.value.gallery[index].url = response.data.url
    form.value.gallery[index].uploading = false
    
  } catch (error) {
    console.error('Failed to upload gallery image:', error)
    form.value.gallery[index].uploading = false
    form.value.gallery[index].fileName = ''
    alert('Failed to upload image. Please try again.')
  }
}

const onHeroImageChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  heroImageUploading.value = true
  heroImageName.value = file.name
  
  const formData = new FormData()
  formData.append('image', file)
  
  try {
    const response = await axios.post('/api/marketing/upload-image/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    form.value.hero_image = response.data.url
    heroImageUploading.value = false
    
  } catch (error) {
    console.error('Failed to upload hero image:', error)
    heroImageUploading.value = false
    heroImageName.value = ''
    alert('Failed to upload hero image. Please try again.')
  }
}

const removeHeroImage = () => {
  form.value.hero_image = ''
  heroImageName.value = ''
}

const handleImageError = (event) => {
  console.log('Image failed to load:', event.target.src)
}

const saveTemplate = async () => {
  try {
    saving.value = true
    
    // Prepare the data for API - clean up gallery data
    const cleanGallery = form.value.gallery.map(item => ({
      url: item.url,
      title: item.title,
      description: item.description
    }))
    
    const templateData = {
      ...form.value,
      itinerary: JSON.stringify(form.value.itinerary),
      gallery: JSON.stringify(cleanGallery)
    }
    
    await http.post('/api/marketing/templates/', templateData)
    
    successMessage.value = 'Template created successfully!'
    showSuccessModal.value = true
    
  } catch (error) {
    console.error('Failed to save template:', error)
    successMessage.value = 'Failed to save template. Please try again.'
    showSuccessModal.value = true
  } finally {
    saving.value = false
  }
}

const closeSuccessModal = () => {
  showSuccessModal.value = false
  if (successMessage.value.includes('successfully')) {
    goBack()
  }
}

const goBack = () => {
  router.push('/settings/trip-templates')
}

onMounted(() => {
  loadDestinations()
  loadTemplateForDuplication()
})
</script>

<style scoped>
.website-template-creator {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.day-item {
  background-color: #f8f9fa;
}

.gallery-item {
  background-color: #f8f9fa;
}

.modal.show {
  display: block;
}

.card-header h5 {
  color: #495057;
}

.btn-outline-danger:hover {
  color: white;
}
</style>
