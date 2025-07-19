<template>
  <h3 class="mb-3">CREATE A QUOTE</h3>

  <!-- Workflow Status Component -->
  <QuoteWorkflowStatus 
    :current-status="form.workflow_status_rel || 10" 
    size="small"
  />

  <form @submit.prevent="save" class="p-4 rounded shadow-sm" style="background: #e2e9e8; color: black;">

    <!-- contact picker -->
    <ContactSelect v-model="form.client" />

    <!-- Editable fields -->
          <div class="row g-3 mb-3">
            <div class="col-md-6">
              <label class="form-label">Church Name</label>
              <input v-model="form.church_name" class="form-control" required />
            </div>
            <div class="col-md-6">
              <label class="form-label">Spiritual Director Name</label>
              <input v-model="form.leader_name" class="form-control" />
            </div>
          </div>


    <ItineraryForm v-model="form" />

    <!-- departure city + checkboxes -->
    <div class="row g-3 mb-3">
      <div class="col-md-4">
        <label class="form-label">Departure City</label>
        <DepartureCitySelect
          v-model="form.departure_city_id"
          @update:cost="form.departure_city_cost=$event" />
        
        <!-- Checkboxes vertically under the input -->
        <div class="mt-3">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="form.charge_city_fee" id="chargeCityFee" true-value="YES" false-value="NO">
            <label class="form-check-label" for="chargeCityFee">Add city cost to total price</label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="form.multi_city" id="multiCity">
            <label class="form-check-label" for="multiCity">Allow departure from multiple cities</label>
          </div>
        </div>
      </div>
    </div>

    <MultiCityBlock v-if="form.multi_city" v-model="form.multiCities" />

    <PriceForm v-model="form" />
   
    <!-- Cancellation / Max-Pax / Assigned-User -->
    <div class="row g-3 mb-3">
      <!-- Cancellation terms -->
      <div class="col-12 col-md-4">
        <label class="form-label">Cancellation Terms</label>
        <select
          v-model="form.cancelation_terms"
          class="form-select"
        >
          <option value="">-- Select --</option>
          <option value="YES">YES</option>
          <option value="NO">NO</option>
        </select>
      </div>

      <!-- Maximum passengers -->
      <div class="col-12 col-md-4">
        <label class="form-label">Maximum Passengers</label>
        <input
          type="number"
          min="0"
          v-model="form.max_pax"
          class="form-control"
        />
      </div>

      <!-- Assigned user (read-only) -->
      <div class="col-12 col-md-4">
        <label class="form-label">Assigned User</label>
        <input
          class="form-control"
          :value="currentUser.username"
          readonly
        />
      </div>
    </div>


    <!-- upload + notes + save --------------------------------------- -->
    <div class="row g-3 mb-3">
      <div class="col-md-4">
        <label class="form-label">Upload Agreement Document</label>
        <div class="d-flex gap-1 py-2 px-2" style="background: white; border: 1px solid #ccc; border-radius: 10px;">
          <button 
            type="button" 
            class="btn btn-outline-info btn-xs px-2 py-1"
            @click="triggerFileInput('agreement_file')"
            style="font-size: 18px; line-height: 1.2;"
          >
            <i class="fa fa-cloud-upload fa-1x" aria-hidden="true"></i>
          </button>
          <input 
            type="text" 
            class="form-control form-control-sm" 
            :value="getFileName('agreement_file')"
            readonly
            placeholder="No file selected"
            style="font-size: 12px;"
          />
        </div>
        <input 
          type="file" 
          class="d-none" 
          :ref="el => fileInputs['agreement_file'] = el"
          @change="handleFileUpload('agreement_file', $event)"
          accept=".pdf,.doc,.docx"
        />
      </div>
      <div class="col-md-4">
        <label class="form-label">Upload Official Document</label>
        <div class="d-flex gap-1 py-2 px-2" style="background: white; border: 1px solid #ccc; border-radius: 10px;">
          <button 
            type="button" 
            class="btn btn-outline-info btn-xs px-2 py-1"
            @click="triggerFileInput('official_file')"
            style="font-size: 18px; line-height: 1.2;"
          >
            <i class="fa fa-cloud-upload fa-1x" aria-hidden="true"></i>
          </button>
          <input 
            type="text" 
            class="form-control form-control-sm" 
            :value="getFileName('official_file')"
            readonly
            placeholder="No file selected"
            style="font-size: 12px;"
          />
        </div>
        <input 
          type="file" 
          class="d-none" 
          :ref="el => fileInputs['official_file'] = el"
          @change="handleFileUpload('official_file', $event)"
          accept=".pdf,.doc,.docx"
        />
      </div>
    </div>

    <div class="row g-3 mb-3">
      <div class="col-md-8">
        <textarea 
          v-model="form.notes" 
          class="form-control" 
          rows="3"
          placeholder="Notes"
        ></textarea>
      </div>
    </div>

    <!-- Marketing Block - Only shows for workflow statuses 60, 70, 80, 90 -->
    <MarketingBlock v-model="form" />

    <button class="btn btn-primary" :disabled="loading">
      {{ loading ? 'Saving…' : 'Create Quote' }}
    </button>
    <router-link :to="{ name: 'QuoteList' }" class="btn btn-secondary ms-2">
      Cancel
    </router-link>
    <div v-if="error" class="alert alert-danger mt-2">{{ error }}</div>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ContactSelect        from '../components/ContactSelect.vue'
import DepartureCitySelect  from '../components/DepartureCitySelect.vue'
import MultiCityBlock       from '../components/MultiCityBlock.vue'
import ItineraryForm        from '../components/ItineraryForm.vue'
import PriceForm            from '../components/PriceForm.vue'
import MarketingBlock       from '../components/MarketingBlock.vue'
import QuoteWorkflowStatus  from '../components/QuoteWorkflowStatus.vue'
import quoteApi             from '../api/quotes.api'
import useQuoteForm from '../composables/useQuoteForm'

const router  = useRouter()
const loading = ref(false)
const error   = ref('')
const quoteNumber = 'NP-NEW'

// Add fileInputs ref for file handling
const fileInputs = ref({})

const { form, currentUser, loadCurrentUser } = useQuoteForm()

// Load current user on component mount
onMounted(async () => {
  await loadCurrentUser()
})

// File handling functions
function getFileName(fieldName) {
  const file = form[fieldName]
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
    form[fieldName] = file
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
  form[fieldName] = null
  const input = fileInputs.value[fieldName]
  if (input) {
    input.value = ''
  }
}

function showFile(fieldName) {
  if (form[fieldName]) {
    if (form[fieldName] instanceof File) {
      const url = URL.createObjectURL(form[fieldName])
      window.open(url, '_blank')
    } else if (typeof form[fieldName] === 'string') {
      window.open(form[fieldName], '_blank')
    }
  }
}

async function save() {
  // Check if contact is selected
  if (!form.client) { 
    error.value = 'Contact is required'
    return 
  }
  
  if (!form.client.id) {
    error.value = 'Please select a valid contact'
    return
  }

  try {
    loading.value = true
    error.value = ''
    
    // Create clean data object - no FormData
    const data = {}
    
    // Add form data as clean object
    Object.entries(form).forEach(([k, v]) => {
      if (v == null || v === '') return
      
      if (k === 'client' && typeof v === 'object') {
        data.client = v.id
      } else if (k === 'multiCities' && Array.isArray(v)) {
        const validCities = v.filter(city => city.cityId && city.cost)
        if (validCities.length > 0) {
          data.multiCities = validCities
        }
      } else if (k === 'multi_city') {
        data.multi_city = v ? '1' : '0'
      } else if (k === 'is_dmc') {
        // Server expects integer: 1 for true, 0 for false
        data[k] = v ? 1 : 0
      } else if (k === 'mkt_shiped') {
        // Server expects max 3 chars: "YES" or "NO"
        data[k] = v ? 'YES' : 'NO'
      } else if (typeof v === 'boolean') {
        data[k] = v ? 'true' : 'false'
      } else if (typeof v !== 'object' && typeof v !== 'function') {
        data[k] = v
      }
    })

    console.log('Sending clean data:', data)

    await quoteApi.create(data)
    router.push({ name: 'QuoteList' })
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || 'An error occurred'
    console.error('Save error:', e)
    console.error('Error response:', e.response?.data)
  } finally { 
    loading.value = false 
  }
}

</script>