<template>
  <!-- Readonly fields -->
  <div class="row g-3 mb-3">
    <div class="col-md-4">
      <label class="form-label">Quote #</label>
      <input type="text" class="form-control" :value="displayQuoteNumber" readonly>
    </div>
    <!-- Contact field -->
    <div class="col-md-4">
      <label class="form-label">Contact</label>
      <v-select
        v-model="selectedClient"
        :options="clientOptions"
        label="display"
        track-by="id"
        @search="onClientSearch"
        @option:selected="resetSearch"
        placeholder=""
        :filterable="false"
        :clearable="false"
        class="contact-vselect"
        @focus="contactSelectFocused = true"
        @blur="contactSelectFocused = false"
        style="background-color: white;"
      >
        <!-- helper line exactly as before -->
        <template #no-options>
          <div class="helper-line">
            {{ searchTerm.length < 3
                ? 'Please enter 3 or more characters'
                : 'No contacts match that search.' }}
          </div>
        </template>
      </v-select>
      <div
        class="contact-helper-text"
        v-if="contactSelectFocused && !selectedClient"
      >
        Please start typing the contact name
      </div>
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
</template>

<script setup>
import { ref, computed } from 'vue'
import vSelect from 'vue3-select'
import 'vue3-select/dist/vue3-select.css'
import quoteApi from '@/modules/quotes/api/quotes.api'

/* props for quote number ---------------------------------------------- */
const props = defineProps({
  quoteNumber: {
    type: String,
    default: 'NP-NEW'
  }
})

/* v-model passthrough ------------------------------------------------- */
const selectedClient = defineModel()

/* state ----------------------------------------------------------------*/
const clientOptions = ref([])
const searchTerm = ref('')
const contactSelectFocused = ref(false)

/* computed quote number ----------------------------------------------- */
const displayQuoteNumber = computed(() => props.quoteNumber || 'NP-NEW')

/* computed contact details from selected client ----------------------*/
const contactPhone = computed(() => selectedClient.value?.phone || '')
const contactEmail = computed(() => selectedClient.value?.email || '')
const contactEmail2 = computed(() => selectedClient.value?.email2 || '')
const contactEmail3 = computed(() => selectedClient.value?.email3 || '')

/* debounced remote search ---------------------------------------------*/
let timer = null
function onClientSearch(q) {
  searchTerm.value = q
  if (q.length < 3) { 
    clientOptions.value = []
    return 
  }

  clearTimeout(timer)
  timer = setTimeout(async () => {
    try {
      const res = await quoteApi.searchContacts(q)
      clientOptions.value = res.map(c => ({
        ...c,
        display: `${c.first_name} ${c.last_name}`.trim(),
      }))
      // keep current selection on top
      if (selectedClient.value && !clientOptions.value.find(o => o.id === selectedClient.value.id)) {
        clientOptions.value.unshift(selectedClient.value)
      }
    } catch (error) {
      console.error('Failed to search contacts:', error)
      clientOptions.value = []
    }
  }, 300)
}

function resetSearch() { 
  searchTerm.value = '' 
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

/* Use :deep() to penetrate component boundaries */
.contact-vselect :deep(.vs__dropdown-toggle) {
  min-height: 30px; /* Reduced from 44px to match Bootstrap form-control */
  border-radius: 0.375rem; /* Match Bootstrap's border-radius */
  font-size: 14px !important; /* Match our global font size */
  border: 1px solid #ced4da; /* Match Bootstrap border color */
}

.contact-vselect :deep(.vs__selected) {
  max-width: 100%; 
  overflow: hidden; 
  text-overflow: ellipsis; 
  white-space: nowrap;
  font-size: 14px !important; /* Match our global font size */
  line-height: 1.5 !important;
  margin: 0; /* Remove any default margin */
  padding: 0; /* Remove any default padding */
}

.contact-vselect :deep(.vs__search) {
  font-size: 14px !important; /* Match our global font size */
  line-height: 1.5 !important;
  margin: 0;
  padding: 0;
}

.contact-vselect :deep(.vs__dropdown-option) {
  font-size: 14px !important; /* Match our global font size */
  line-height: 1.5 !important;
}

/* Force the entire component font size */
.contact-vselect {
  font-size: 14px !important; /* Match our global font size */
}

.contact-vselect :deep(*) {
  font-size: inherit !important;
  font-family: 'Roboto', "Montserrat", sans-serif !important;
}

.helper-line { 
  padding: 4px 8px; 
  color: #6c757d; 
  font-size: 14px; /* Match our global font size */
}

.contact-helper-text {
  font-size: 14px; /* Match our global font size */
  color: #6c757d;
  margin-top: 0.25rem;
}
</style>

