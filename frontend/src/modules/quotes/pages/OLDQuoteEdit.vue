<template>
  <div class="container-fluid p-0">
    <!-- header row -->
    <div class="d-flex align-items-center justify-content-between mt-1">
      <h3 class="mb-0">EDIT QUOTE</h3>
      <router-link :to="{ name: 'QuoteList' }" class="btn btn-primary">
        Back to Quotes
      </router-link>
    </div>

    <div class="card bg-light mb-4 mt-3 w-100" style="max-width: 100%;">
      <div class="card-body">
        <form @submit.prevent="submitQuote"class="p-4 rounded shadow-sm" style="background: #e2e9e8; color: black;">
          <!-- Readonly fields -->
          <div class="row g-3 mb-3">
            <div class="col-md-4">
              <label class="form-label">Quote #</label>
              <input type="text" class="form-control" :value="quoteId" readonly>
            </div>
            <div class="col-md-4">
              <label class="form-label">Contact</label>
            <v-select
              v-model="selectedClient"
              :options="clientOptions"
              label="display"
              @search="onClientSearch"
              placeholder="Type to search clients..."
              style="background-color: white;"
            />
            </div>
            <div class="col-md-4">
              <label class="form-label">Contact Phone</label>
              <input type="text" class="form-control" :value="contactPhone" readonly>
            </div>
          </div>
          <div class="row g-3 mb-3">
            <div class="col-md-4">
              <label class="form-label">Contact Email</label>
              <input type="email" class="form-control" :value="contactEmail" readonly>
            </div>
            <div class="col-md-4">
              <label class="form-label">Contact Email 2</label>
              <input type="email" class="form-control" :value="contactEmail2" readonly>
            </div>
            <div class="col-md-4">
              <label class="form-label">Contact Email 3</label>
              <input type="email" class="form-control" :value="contactEmail3" readonly>
            </div>
          </div>

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

          <hr class="mt-4">
          <h4 class="mb-3">Itinerary Information</h4>

          <div class="row g-3 mb-3">
            <div class="col-md-4">
              <label class="form-label">Departure Date</label>
              <input
                v-model="form.departure_date"
                type="date"
                class="form-control"/>
            </div>
            <div class="col-md-4">
            <label class="form-label">Destination Group</label>
            <select v-model="form.destination_group" class="form-select">
              <option v-for="g in destinationGroups" :key="g.id" :value="g.id">
                {{ g.nombre }}
              </option>
            </select>             
            </div>
           <div class="col-md-4">
            <label class="form-label">Destination</label>
            <select v-model="form.itinerary_id" class="form-select">
              <option v-for="d in destinations" :key="d.id" :value="d.id">
                {{ d.nombre }}
              </option>
            </select>
            </div>
          </div>
          <div class="col-md-4">
            <label class="form-label">Departure City</label>
            <select
              v-model="form.departure_city_id"
              class="form-select"
              required
            >
              <option value="">-- Select City --</option>
              <option
                v-for="city in cities"
                :key="city.id"
                :value="city.id"
              >
                {{ city.short_display }}
              </option>
            </select>
          </div>
          <!-- Checkboxes -->
          <div class="col-md-6">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" v-model="form.charge_city_fee" id="chargeCityFee" true-value="YES" false-value="NO">
              <label class="form-check-label" for="chargeCityFee">Add city cost to total price</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" v-model="form.multi_city" id="multiCity">
              <label class="form-check-label" for="multiCity">Allow departure from multiple cities</label>
            </div>
          </div>

          <!-- Multi-city (example for 2 extra cities, expand as needed) -->
          <div v-if="form.multi_city" class="col-12 mt-3">
            <div class="border p-3 rounded bg-light">
              <div class="row mb-2">
                <div class="col-md-6"><strong>Additional City</strong></div>
                <div class="col-md-6"><strong>Additional Cost</strong></div>
              </div>
              <div class="row mb-2" v-for="i in 9" :key="i">
                <div class="col-md-6">
                  <select v-model="form[`dep_city_id${i}`]" class="form-select">
                    <option value="">-- Select City --</option>
                    <option v-for="city in cities" :key="city.id" :value="city.id">
                      {{ city.short_display }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6">
                  <input type="text" v-model="form[`dep_city_cost${i}`]" class="form-control">
                </div>
              </div>
            </div>
          </div>

          <hr class="mt-4">
          <h4 class="mb-3">Price Information</h4>
        <div class="row g-3 mb-3">
          <div class="col-md-4">
            <label class="form-label">Trip Price</label>
            <input v-model="form.itinerary_cost" class="form-control" />
          </div>
          <div class="col-md-4">
            <label class="form-label">Commission Sales</label>
            <input v-model="form.comision_usuario" class="form-control" />
          </div>
          <div class="col-md-4">
            <label class="form-label">Fundraiser</label>
            <input v-model="form.comision_leader" class="form-control" />
          </div>
        </div>
        <div class="row g-3 mb-3">
          <div class="col-md-4">
            <label class="form-label" >Total Price</label>
            <input v-model="form.total_cost" class="form-control" readonly/>
          </div>
          <div class="col-md-4">
            <label class="form-label">Land Only Price</label>
            <input v-model="form.total_cost_land_only" class="form-control" />
          </div>
        <div class="col-md-4">
          <label class="form-label">Display Commission Sales and Fundraiser</label>
          <select v-model="form.display_commission_fundraiser" class="form-select">
            <option value="NO">NO</option>
            <option value="YES">YES</option>
          </select>
        </div>
        </div>               
        <div class="row g-3 mb-3">
          <div class="col-md-4">
            <label class="form-label">Coordinator Name</label>
            <input v-model="form.coordinator_name" class="form-control" />
          </div>
          <div class="col-md-4">
            <label class="form-label">Coordinator Phone</label>
            <input v-model="form.coordinator_phone" class="form-control" />
          </div>
          <div class="col-md-4">
            <label class="form-label">Coordinator Email</label>
            <input v-model="form.coordinator_email" class="form-control" />
          </div>
        </div>        
        <div class="row g-3 mb-3">
         <div class="col-md-4">
            <label class="form-label">Language of Quote</label>
            <select v-model="form.language" class="form-select">
              <option value="">-- Select Language --</option>
              <option value="ENGLISH">ENGLISH</option>
              <option value="SPANISH">SPANISH</option>
              <option value="BILINGUAL">BILINGUAL</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Single Room Supplement</label>
            <input v-model="form.single_room_price" class="form-control" />
          </div>
          <div class="col-md-4">
            <label class="form-label">Minimum Deposit</label>
            <input v-model="form.minimum_deposit" class="form-control" />
          </div>
        </div>

          <div class="row g-3 mb-4">
            <div class="col-md-4">
              <label class="form-label">One Travels Free for each</label>
              <select v-model="form.free_each" class="form-select">
                <option value="0">NO FREE Travel</option>
                <option value="20">20</option>
                <option value="15">15</option>
                <option value="10">10</option>
                <option value="9">9</option>
                <option value="8">8</option>
                <option value="7">7</option>
                <option value="6">6</option>
                <option value="5">5</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">Price change</label>
              <div class="input-group">
                <span class="input-group-text" id="basic-addon1">$</span>
                <input
                  v-model="form.free_each_cost"
                  type="text"
                  class="form-control"
                  placeholder="0.00"
                  :readonly="form.free_each == 0 || form.free_each == 10"
                  aria-describedby="basic-addon1"
                />
              </div>
            </div>
          </div>

          <div class="row g-3 mb-4">
            <div class="col-md-5">
              <label class="form-label">Lunch and Tip Conditions</label>
              <select v-model="form.lunch_and_tip_includes" class="form-select">
                <option value="0">Does NOT Include Lunch and Tips</option>
                <option value="1">Includes Lunch</option>
                <option value="2">Includes Tips</option>
                <option value="3">Includes Lunch and Tips</option>
              </select>
            </div>
          </div>
          <div class="row g-3 mb-3">
            <div class="col-12 col-md-4">
              <label class="form-label">Lunch Included</label>
              <select v-model="form.lunch_included" class="form-select" :disabled="form.lunch_and_tip_includes == 0 || form.lunch_and_tip_includes == 2">
                <option value="NO">NO</option>
                <option value="YES">YES</option>
              </select>
            </div>
            <div class="col-12 col-md-3">
              <label class="form-label">Lunch cost $</label>
              <input v-model="form.lunch_cost" class="form-control" :readonly="form.lunch_and_tip_includes == 0 || form.lunch_and_tip_includes == 2" />
            </div>          
          </div>
          <div class="row g-3 mb-3">
            <div class="col-12 col-md-4">
              <label class="form-label">Tip Included</label>
              <select v-model="form.tip_included" class="form-select" :disabled="form.lunch_and_tip_includes == 0 || form.lunch_and_tip_includes == 1">
                <option value="NO">NO</option>
                <option value="YES">YES</option>
              </select>
            </div>
            <div class="col-12 col-md-3">
              <label class="form-label">Tips Cost $</label>
              <input v-model="form.tips_cost" class="form-control" :readonly="form.lunch_and_tip_includes == 0 || form.lunch_and_tip_includes == 1" />
            </div>
          </div>


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
            <input v-model="form.max_pax" class="form-control" />
          </div>
          <div class="col-12 col-md-4">
            <label class="form-label">Assigned User</label>
            <input class="form-control" :value="usuario" readonly>
          </div>
          </div>          
        <div class="row g-3 mb-3">
          <div class="col-12 col-md-4">
            <label class="form-label">Upload Agreement Document</label>
            <input
              type="file"
              @change="onFileChange($event, 'agreement_file')"
              class="form-control"
            >
          </div>
          <div class="col-12 col-md-4">
            <label class="form-label">Upload Official Document</label>
            <input
              type="file"
              @change="onFileChange($event, 'official_file')"
              class="form-control"
            >
          </div>
        </div>         
        <div class="col-12">
          <label class="form-label">Notes</label>
          <textarea v-model="form.notes" class="form-control" rows="3"></textarea>
        </div>
          <!-- Marketing Block - Only shows for workflow statuses 60, 70, 80, 90 -->
        <MarketingBlock v-model="form" />
        <div class="col-12 mt-4">
            <button type="submit" class="btn btn-primary px-5" :disabled="loading">
              {{ loading ? 'Saving...' : 'Create Quote' }}
            </button>
            <router-link :to="{ name: 'QuoteList' }" class="btn btn-secondary ms-2">Cancel</router-link>
            <div v-if="error" class="alert alert-danger mt-2">{{ error }}</div>
        </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const quoteId = route.params.id

const loading = ref(false)
const error = ref('')

// --- Client/contact fields ---
const selectedClient = ref(null)
const clientOptions = ref([])
const contactPhone = ref('')
const contactEmail = ref('')
const contactEmail2 = ref('')
const contactEmail3 = ref('')

// --- Dropdown data ---
const destinationGroups = ref([])
const destinations = ref([])
const cities = ref([])

// --- User display (readonly) ---
const usuario = ref('')

// --- Main form ---
const form = ref({
  id: quoteId,
  church_name: '',
  leader_name: '',
  departure_date: '',
  trip_name: '',
  itinerary_id: '',
  departure_city_id: '',
  charge_city_fee: '',
  multi_city: false,
  dep_city_id1: '', dep_city_cost1: '',
  dep_city_id2: '', dep_city_cost2: '',
  dep_city_id3: '', dep_city_cost3: '',
  dep_city_id4: '', dep_city_cost4: '',
  dep_city_id5: '', dep_city_cost5: '',
  dep_city_id6: '', dep_city_cost6: '',
  dep_city_id7: '', dep_city_cost7: '',
  dep_city_id8: '', dep_city_cost8: '',
  dep_city_id9: '', dep_city_cost9: '',
  itinerary_cost: '',
  comision_usuario: '',
  comision_leader: '',
  total_cost: '',
  total_cost_land_only: '',
  display_commission_fundraiser: '',
  coordinator_name: '',
  coordinator_phone: '',
  coordinator_email: '',
  language: '',
  single_room_price: '',
  minimum_deposit: '',
  lunch_and_tip_includes: '',
  free_each: '',
  free_each_cost: '',
  lunch_included: '',
  lunch_cost: '',
  tip_included: '',
  tips_cost: '',
  cancelation_terms: '',
  max_pax: '',
  user: '',
  agreement_file: null,
  official_file: null,
  date_created: '',
  notes: '',
  is_dmc: '',
  mkt_shiped: '',
  workflow_status_rel: '',
  quote_status: '',
})

// --- Fetch dropdowns and quote data ---
onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      fetchClients(),
      fetchDestinationGroups(),
      fetchDestinations(),
      fetchCities()
    ])
    // Fetch quote data
    const res = await axios.get(`/api/quotes/${quoteId}/`)
    Object.assign(form.value, res.data)
    // Set selected client if present
    if (res.data.client) {
      selectedClient.value = clientOptions.value.find(c => c.id === res.data.client) || null
      updateContactFields()
    }
    // Set usuario display if present
    if (res.data.user_display) {
      usuario.value = res.data.user_display
    }
  } catch (err) {
    error.value = 'Failed to load quote.'
  } finally {
    loading.value = false
  }
})

// --- Fetch functions ---
async function fetchClients() {
  const res = await axios.get('/api/contacts/')
  clientOptions.value = Array.isArray(res.data.results)
    ? res.data.results.map(c => ({
        ...c,
        display: `${c.first_name || ''} ${c.last_name || ''}`.trim()
      }))
    : []
}

async function fetchDestinationGroups() {
  const res = await axios.get('/api/destination-groups/')
  destinationGroups.value = res.data
}

async function fetchDestinations() {
  const res = await axios.get('/api/destinations/')
  destinations.value = res.data
}

async function fetchCities() {
  const res = await axios.get('/api/itinerary-cities/')
  cities.value = res.data
}

// --- Client search ---
function onClientSearch(search) {
  axios.get('/api/contacts/', { params: { search } }).then(res => {
    clientOptions.value = Array.isArray(res.data.results)
      ? res.data.results.map(c => ({
          ...c,
          display: `${c.first_name || ''} ${c.last_name || ''}`.trim()
        }))
      : []
  })
}

// --- Update contact fields when client changes ---
function updateContactFields() {
  if (selectedClient.value) {
    contactPhone.value = selectedClient.value.phone || ''
    contactEmail.value = selectedClient.value.email || ''
    contactEmail2.value = selectedClient.value.email2 || ''
    contactEmail3.value = selectedClient.value.email3 || ''
  } else {
    contactPhone.value = ''
    contactEmail.value = ''
    contactEmail2.value = ''
    contactEmail3.value = ''
  }
}

watch(selectedClient, (val) => {
  updateContactFields()
  // Set client foreign key in form
  form.value.client = val ? val.id : null
})

// --- File upload handlers ---
function onFileChange(event, field) {
  const file = event.target.files[0]
  form.value[field] = file || null
}

// --- Submit handler ---
async function submitQuote() {
  // Clean up optional fields before submit
  const cleanedForm = { ...form.value }

  // Clean number fields
  const numberFields = [
    'single_room_price',
    'minimum_deposit',
    'lunch_cost',
    'tips_cost',
    'max_pax'
  ]
  numberFields.forEach(field => {
    if (
      cleanedForm[field] === '' ||
      cleanedForm[field] === null ||
      cleanedForm[field] === undefined ||
      isNaN(cleanedForm[field])
    ) {
      cleanedForm[field] = null
    } else if (field === 'max_pax') {
      cleanedForm[field] = parseInt(cleanedForm[field])
    } else {
      cleanedForm[field] = parseFloat(cleanedForm[field])
    }
  })

  // Foreign keys
  cleanedForm.client = selectedClient.value ? selectedClient.value.id : null

  // Booleans/flags
  if (typeof cleanedForm.multi_city !== 'undefined') {
    cleanedForm.multi_city = cleanedForm.multi_city ? '1' : '0'
  }

  loading.value = true
  error.value = ''
  try {
    const formData = new FormData()
    for (const key in cleanedForm) {
      if (cleanedForm[key] !== null && cleanedForm[key] !== undefined) {
        formData.append(key, cleanedForm[key])
      }
    }
    await axios.patch(`/api/quotes/${quoteId}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    router.push({ name: 'QuoteList' })
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to update quote'
  } finally {
    loading.value = false
  }
}
</script>