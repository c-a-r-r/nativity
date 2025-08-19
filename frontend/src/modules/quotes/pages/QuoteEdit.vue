<template>
  <div class="container-fluid p-0">
    <!-- Header -->
    <div class="d-flex align-items-center justify-content-between mt-1">
      <h3 class="mb-0">EDIT QUOTE</h3>
      <router-link 
        :to="route.query.returnTo === 'marketing' ? { name: 'MarketingViews' } : { name: 'QuoteList' }" 
        class="btn btn-primary">
        {{ route.query.returnTo === 'marketing' ? 'Back to Marketing' : 'Back to Quotes' }}
      </router-link>
    </div>

    <!-- ...existing code... -->

    <!-- Workflow Status Component -->
    <QuoteWorkflowStatus 
      v-if="!loading && form.workflow_status_rel"
      :current-status="form.workflow_status_rel" 
    />

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading quote data...</p>
    </div>

    <!-- Error state -->
    <div v-if="error && !loading" class="alert alert-danger mt-3">
      {{ error }}
    </div>

    <form @submit.prevent="save" class="p-4 rounded shadow-sm mt-3" style="background: #e2e9e8; color: black;" v-if="!loading">
      
      <!-- Use existing ContactSelect component -->
      <ContactSelect v-model="form.client" :quote-number="quoteId" />

      <!-- Editable Church Info -->
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

      <!-- Rest of the form remains the same... -->
      <ItineraryForm v-model="form" />
      
    <div class="row g-3 mb-3">
      <div class="col-md-4">
        <label class="form-label">Departure City</label>
        <DepartureCitySelect
          v-model="form.departure_city_id"
          @update:cost="form.departure_city_cost=$event" />
        <div class="mt-3">
          <!-- ...existing code for checkboxes... -->
        </div>
      </div>
    </div>

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

    <!-- This should be hidden when form.multi_city is false -->
    <MultiCityBlock v-if="form.multi_city" v-model="form.multiCities" />
      <PriceForm v-model="form" />

      <div class="row g-3 mb-3">
        <div class="col-12 col-md-4">
          <label class="form-label">Cancellation Terms</label>
          <select v-model="form.cancelation_terms" class="form-select">
            <option value="">-- Select --</option>
            <option value="YES">YES</option>
            <option value="NO">NO</option>
          </select>
        </div>
        <div class="col-12 col-md-4">
          <label class="form-label">Maximum Passengers</label>
          <input type="number" min="0" v-model="form.max_pax" class="form-control" />
        </div>
        <div class="col-12 col-md-4">
          <label class="form-label">Assigned User</label>
          <input 
            class="form-control" 
            :value="form.assigned_user_name || 'No user assigned'" 
            readonly 
          />
          <small v-if="form.user_id" class="text-muted">
            User ID: {{ form.user_id }}
          </small>
        </div>
      </div>

      <!-- Account Manager and Sales Agent Row -->
      <div class="row g-3 mb-3">
        <div class="col-12 col-md-6">
          <label class="form-label">Account Manager</label>
          <input 
            class="form-control" 
            :value="form.account_manager_name || 'No account manager assigned'" 
            readonly 
          />
          <small v-if="form.manager_id" class="text-muted">
            Manager ID: {{ form.manager_id }}
          </small>
        </div>
        <div class="col-12 col-md-6">
          <label class="form-label">Sales Agent</label>
          <input 
            class="form-control" 
            :value="form.sales_agent_name || 'No sales agent assigned'" 
            readonly 
          />
          <small v-if="form.agent_id" class="text-muted">
            Agent ID: {{ form.agent_id }}
          </small>
        </div>
      </div>

        <div class="row g-3 mb-3">
          <div class="col-md-4">
            <label class="form-label">Status</label>
            <select v-model="form.quote_status" class="form-select">
              <option value="">-- Select Status --</option>
              <option value="1">Draft</option>
              <option value="2">Sent to Contact</option>
              <option value="4">Accepted</option>
              <option value="5">Rejected</option>
              <option value="6">Completed</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Workflow</label>
            <select v-model="form.workflow_status_rel" class="form-select">
              <option value="">-- Select Workflow --</option>
              <option value="10">Itinerary Created</option>
              <option value="20">Send to Priest</option>
              <option value="30">Sends interest back</option>
              <option value="40">Send a quote w/ prices</option>
              <option value="50">Priest approves & sends back</option>
              <option value="60">Create marketing</option>
              <option value="70">Upload marketing</option>
              <option value="80">Send back to Priest via DocuSign</option>
              <option value="90">Receive back approval</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Date Created</label>
            <input :value="formatDate(form.date_created)" class="form-control" readonly />
          </div>
        </div>  

        <div class="row g-3 mb-3">
        <div class="col-md-4">
            <label class="form-label">Upload Agreement Document</label>
            <div class="d-flex gap-1 py-2 px-2" style="background: white; border: 1px solid #ccc; border-radius: 10px;">
            <button 
                type="button" 
                class="btn btn-outline-primary btn-xs px-2 py-1"
                @click="showFile('agreement_file')"
                :disabled="!form.agreement_file"
                style="font-size: 12px; line-height: 1.2; white-space: nowrap; min-width: 90px;"
            >
                <i class="fa fa-file-o" aria-hidden="true"></i> Show File
            </button>
            <button 
                type="button" 
                class="btn btn-outline-secondary btn-xs px-2 py-1"
                @click="clearFile('agreement_file')"
                :disabled="!form.agreement_file"
                style="font-size: 11px; line-height: 1.2; color: red;"
            >
                ✕ Clear
            </button>
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
                class="btn btn-outline-primary btn-xs px-2 py-1"
                @click="showFile('official_file')"
                :disabled="!form.official_file"
                style="font-size: 12px; line-height: 1.2; white-space: nowrap; min-width: 90px;"
            >
                <i class="fa fa-file-o" aria-hidden="true"></i> Show File
            </button>
            <button 
                type="button" 
                class="btn btn-outline-secondary btn-xs px-2 py-1"
                @click="clearFile('official_file')"
                :disabled="!form.official_file"
                style="font-size: 11px; line-height: 1.2; color: red;"
            >
                ✕ Clear
            </button>
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

      <textarea v-model="form.notes" class="form-control mb-3" rows="3" placeholder="Notes"></textarea>

        <MarketingBlock 
        v-if="quote"
        v-model="form" 
        :quote="quote" 
        @trip-created="handleTripCreated"
        />

      <button class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Updating…' : 'Update Quote' }}
      </button>
      <router-link :to="{ name: 'QuoteList' }" class="btn btn-secondary ms-2">
        Cancel
      </router-link>
      <div v-if="error" class="alert alert-danger mt-2">{{ error }}</div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ContactSelect from '../components/ContactSelect.vue'
import DepartureCitySelect from '../components/DepartureCitySelect.vue'
import MultiCityBlock from '../components/MultiCityBlock.vue'
import ItineraryForm from '../components/ItineraryForm.vue'
import PriceForm from '../components/PriceForm.vue'
import MarketingBlock from '../components/MarketingBlock.vue'
import QuoteWorkflowStatus from '../components/QuoteWorkflowStatus.vue'
import FormFile from '@/modules/quotes/components/ui/FormFile.vue'
import quoteApi from '../api/quotes.api'
import useQuoteForm from '../composables/useQuoteForm'
import http from '@/shared/services/http'

const route = useRoute()
const router = useRouter()
const quoteId = route.params.id

const loading = ref(false)
const error = ref('')
const quote = ref(null)

const fileInputs = ref({})

const { form, currentUser, loadCurrentUser } = useQuoteForm()

const templates = ref([])
const selectedTemplate = ref('')
const tripLinks = ref({ public: '', private: '' })
const creatingTrip = ref(false)

const handleTripCreated = async (tripData) => {
  console.log('Trip created successfully:', tripData)
  // Only reload quote from backend to update form fields with permanent links
  await loadQuote()
}

function formatDate(dateString) {
  if (!dateString) return ''
  try {
    return new Date(dateString).toLocaleDateString()
  } catch (error) {
    return dateString
  }
}

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

function onMultiCityChange() {
  console.log('Multi-city changed to:', form.multi_city)
  
  // Clear multiCities array when multi_city is unchecked
  if (!form.multi_city) {
    form.multiCities = []
    console.log('Cleared multiCities array')
  }
}

async function loadTemplates() {
  try {
    const response = await http.get('/api/marketing/templates/')
    templates.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to load templates:', error)
  }
}

async function createMarketingTrip() {
  if (!selectedTemplate.value || !quoteId) return
  creatingTrip.value = true
  try {
    // Call backend to create trip, pass quoteId and selectedTemplate
    const response = await http.post('/api/marketing/create-trip/', {
      quote_id: quoteId,
      template_id: selectedTemplate.value
    })
    // Assume response contains public_link and private_link
    tripLinks.value.public = response.data.public_link
    tripLinks.value.private = response.data.private_link
    // Save links to backend
    await quoteApi.update(quoteId, {
      marketing_public_link: response.data.public_link,
      marketing_private_link: response.data.private_link
    })
    // Reload quote to update form fields with saved links
    await loadQuote()
  } catch (error) {
    console.error('Failed to create marketing trip:', error)
    alert('Failed to create marketing trip.')
  } finally {
    creatingTrip.value = false
  }
}

onMounted(async () => {
  loading.value = true
  error.value = ''
  try {
    await loadCurrentUser()
    await loadQuote()
    await loadTemplates()
  } catch (err) {
    error.value = err.message || 'Failed to load quote data.'
    console.error('Load error:', err)
  } finally {
    loading.value = false
  }
})

async function loadQuote() {
  try {
    const quoteData = await quoteApi.get(quoteId)
    console.log('Loaded quote data:', quoteData)
    
    // Store quote data in reactive property
    quote.value = quoteData
    
    // Populate form with quote data
    Object.assign(form, quoteData)
    
    // Map backend field names to frontend field names
    if (quoteData.trip_not_include) {
      form.trip_not_includes = quoteData.trip_not_include
    }
    
    // Ensure marketing links are loaded into form (always overwrite)
    form.public_link = quoteData.marketing_public_link || ''
    form.private_link = quoteData.marketing_private_link || ''

    // CONVERT SERVER VALUES TO PROPER BOOLEANS
    form.multi_city = quoteData.multi_city === '1' || quoteData.multi_city === 1 || quoteData.multi_city === true

    console.log('Converted multi_city from:', quoteData.multi_city, 'to:', form.multi_city)

    // If client is just an ID, fetch the full client data
    if (quoteData.client && typeof quoteData.client === 'number') {
      try {
        const response = await http.get(`/api/contacts/${quoteData.client}/`)
        form.client = {
          ...response.data,
          display: `${response.data.first_name || ''} ${response.data.last_name || ''}`.trim()
        }
        console.log('Loaded client data:', form.client)
      } catch (clientError) {
        console.error('Failed to load client details:', clientError)
        form.client = { id: quoteData.client, display: `Contact ID: ${quoteData.client}` }
      }
    } else if (quoteData.client && typeof quoteData.client === 'object') {
      form.client = {
        ...quoteData.client,
        display: `${quoteData.client.first_name || ''} ${quoteData.client.last_name || ''}`.trim()
      }
    }

    // Convert multi-city data if it exists
    if (quoteData.multiCities && Array.isArray(quoteData.multiCities)) {
      form.multiCities = quoteData.multiCities
    } else {
      form.multiCities = []
    }

    console.log('Final form.client:', form.client)
    console.log('Final multi_city value:', form.multi_city, typeof form.multi_city)
  } catch (err) {
    console.error('Failed to load quote:', err)
    throw new Error(`Failed to load quote data: ${err.message || err}`)
  }
}

// Rest of the component remains the same...
async function save() {
  if (!form.client?.id) {
    error.value = 'Contact is required'
    return
  }

  try {
    loading.value = true
    error.value = ''
    
    const data = {}
    

    Object.entries(form).forEach(([k, v]) => {
      if (k === 'client' && typeof v === 'object') {
        data.client = v.id
      } else if (k === 'multiCities' && Array.isArray(v)) {
        const validCities = v.filter(city => city.cityId && city.cost)
        if (validCities.length > 0) {
          data.multiCities = validCities
        }
      } else if (k === 'multi_city') {
        data.multi_city = v ? '1' : '0'
      } else if (k === 'workflow_status_rel' || k === 'quote_status') {
        data[k] = Number(v)
      } else if (k === 'is_dmc') {
        data[k] = v ? 1 : 0
      } else if (k === 'mkt_shiped') {
        data[k] = v ? 'YES' : 'NO'
      } else if (k === 'public_link' || k === 'private_link') {
        // handled below
      } else if (typeof v === 'boolean') {
        data[k] = v ? 'true' : 'false'
      } else if (typeof v !== 'object' && typeof v !== 'function' && v != null && v !== '') {
        data[k] = v
      }
    })

    // Map frontend field names to backend field names
    if (form.trip_not_includes) {
      data.trip_not_include = form.trip_not_includes
    }

    // Always send marketing_public_link and marketing_private_link, even if empty
    data.marketing_public_link = form.public_link || ''
    data.marketing_private_link = form.private_link || ''

    console.log('Updating quote with data:', data)

    await quoteApi.update(quoteId, data)
    
    // Check if we should return to marketing views
    const returnTo = route.query.returnTo
    if (returnTo === 'marketing') {
      router.push({ name: 'MarketingViews' })
    } else {
      router.push({ name: 'QuoteList' })
    }
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || 'An error occurred'
    console.error('Update error:', e)
  } finally {
    loading.value = false
  }
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

* {
  font-size: 14px;
  font-weight: 400;
  font-family: 'Roboto', "Montserrat", sans-serif;
}

/* Apply to all elements within this component */
div, span, p, h1, h2, h3, h4, h5, h6, 
a, li, td, th, label, button, input, 
textarea, select, .form-control, .form-select, 
.btn, .card, .alert {
  font-size: 14px;
  font-weight: 400;
  font-family: 'Roboto', "Montserrat", sans-serif;
}

/* Preserve FontAwesome icons */
.fa, .fas, .far, .fal, .fad, .fab, [class*="fa-"], 
i.fa, i.fas, i.far, i.fal, i.fad, i.fab, i[class*="fa-"] {
  font-family: "Font Awesome 6 Free", "Font Awesome 6 Pro", "Font Awesome 6 Brands", "Font Awesome 5 Free", "Font Awesome 5 Pro", "FontAwesome" !important;
}

/* Preserve upload button styling */
button[onclick*="triggerFileInput"],
button[onclick*="FileInput"],
button[onclick*="file"],
button[onclick*="upload"] {
  font-size: inherit;
  font-weight: inherit;
  font-family: inherit;
}
</style>