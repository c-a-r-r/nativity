<template>
  <div class="template-form">
    <h2>Create/Edit Marketing Trip Template</h2>
    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label>Name</label>
        <input v-model="form.name" class="form-control" required />
      </div>
      <div class="mb-3">
        <label>Trip Title</label>
        <input v-model="form.trip_title" class="form-control" required />
      </div>
      <div class="mb-3">
        <label>Destination</label>
        <select v-model="form.destination" class="form-select" required>
          <option value="">Select Destination</option>
          <option v-for="dest in destinations" :key="dest.id" :value="dest.id">
            {{ dest.name }}
          </option>
        </select>
      </div>
      <div class="form-check form-switch mb-3">
        <input
          class="form-check-input"
          type="checkbox"
          id="isActiveSwitch"
          v-model="form.is_active"
        />
        <label class="form-check-label" for="isActiveSwitch">
          Active
        </label>
      </div>
      <div class="mb-3">
        <label>Hero Image</label>
        <input type="file" accept="image/*" @change="onHeroImageChange" class="form-control mb-2" />
        <div v-if="heroImageName || form.hero_image" class="mb-2 d-flex align-items-center gap-3">
          <img v-if="form.hero_image" :src="form.hero_image" alt="Hero Preview" style="max-width: 200px; max-height: 120px; border-radius: 6px; border: 1px solid #ccc;" />
          <span v-if="heroImageName" class="ms-2">{{ heroImageName }}</span>
          <button v-if="form.hero_image" type="button" class="btn btn-sm btn-outline-danger ms-2" @click="removeHeroImage">Remove</button>
        </div>
      </div>
      <h4>Itinerary (up to 20 days)</h4>
      <div v-for="(day, idx) in form.itinerary" :key="idx" class="itinerary-day mb-4 p-3 border rounded">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <h6 class="mb-0">Day {{ day.day }}</h6>
          <button type="button" class="btn btn-sm btn-outline-danger" @click="removeDay(idx)">Remove</button>
        </div>
        <div class="mb-2">
          <label class="form-label">Title</label>
          <input v-model="day.title" class="form-control" placeholder="Day title" />
        </div>
        <div class="mb-2">
          <label class="form-label">Description</label>
          <textarea v-model="day.description" class="form-control" rows="3" placeholder="Day description"></textarea>
        </div>
        <div class="mb-2">
          <label class="form-label">Images (URLs)</label>
          <div v-for="(img, imgIdx) in day.images" :key="imgIdx" class="mb-1">
            <input v-model="day.images[imgIdx]" class="form-control" placeholder="Image URL" />
          </div>
          <button type="button" class="btn btn-sm btn-outline-secondary mt-1" @click="day.images.push('')">Add Image</button>
        </div>
      </div>
      <button type="button" class="btn btn-outline-primary mb-3" @click="addDay" :disabled="form.itinerary.length >= 20">
        Add Day
      </button>
      <div>
        <button type="submit" class="btn btn-success">Save Template</button>
      </div>
    </form>
  </div>
</template>


<script setup>
import { ref, watch } from 'vue'
const emit = defineEmits(['saved'])
import axios from 'axios'
const props = defineProps({
  destinations: {
    type: Array,
    default: () => []
  },
  template: {
    type: Object,
    default: null
  }
})

const heroImageName = ref('')
const onHeroImageChange = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  heroImageName.value = file.name
  const formData = new FormData()
  formData.append('image', file)
  try {
    const res = await axios.post('/api/marketing/upload-image/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    form.value.hero_image = res.data.url
  } catch (err) {
    alert('Image upload failed')
    heroImageName.value = ''
  }
}

const removeHeroImage = () => {
  form.value.hero_image = ''
  heroImageName.value = ''
}

const form = ref({
  name: '',
  trip_title: '',
  destination: '',
  hero_image: '',
  itinerary: [],
  is_active: true
})

watch(() => props.template, (newTemplate) => {
  if (newTemplate) {
    form.value = {
      name: newTemplate.name || '',
      trip_title: newTemplate.trip_title || '',
      destination: newTemplate.destination || '',
      hero_image: newTemplate.hero_image || '',
      itinerary: newTemplate.itinerary || [],
      is_active: typeof newTemplate.is_active === 'boolean' ? newTemplate.is_active : true
    }
  } else {
    form.value = {
      name: '',
      trip_title: '',
      destination: '',
      hero_image: '',
      itinerary: [],
      is_active: true
    }
  }
}, { immediate: true })

function addDay() {
  if (form.value.itinerary.length < 20) {
    form.value.itinerary.push({
      day: form.value.itinerary.length + 1,
      title: '',
      description: '',
      images: ['', '']
    })
  }
}

function removeDay(idx) {
  form.value.itinerary.splice(idx, 1)
  // Re-number days
  form.value.itinerary.forEach((d, i) => (d.day = i + 1))
}

async function handleSubmit() {
  // Clean up images: remove empty strings
  const payload = {
    ...form.value,
    itinerary: form.value.itinerary.map(day => ({
      ...day,
      images: day.images.filter(Boolean)
    }))
  }
  delete payload.promo_text // Remove promo_text if present
  try {
    if (props.template && props.template.id) {
      await axios.put(`/api/marketing/templates/${props.template.id}/`, payload)
    } else {
      await axios.post('/api/marketing/templates/', payload)
    }
    emit('saved')
  } catch (e) {
    console.error('Full error object:', e)
    const errorMsg = e.response?.data?.detail || JSON.stringify(e.response?.data) || 'Error saving template'
    alert(errorMsg)
    console.error('Error saving template:', e.response?.data)
  }
}
</script>

<style scoped>
.template-form {
  max-width: 700px;
  margin: 0 auto;
}
</style>
