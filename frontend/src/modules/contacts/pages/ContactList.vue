<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import ContactCreate from './ContactCreate.vue'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

const contacts = ref([])
const search = ref('')
const selectedContact = ref(null)
const nextPage = ref(null)
const loadingMore = ref(false)
const loading = ref(false)
const totalCount = ref(0)

const isEditing = ref(false)
const editContactData = ref({})
const isCreating = ref(false)
const contactsContainer = ref(null)
const per = ref(25)
const searchTimeout = ref(null)

// Computed property for displayed contacts - no client-side filtering for pagination
const displayedContacts = computed(() => {
  // Server-side search will handle filtering
  return contacts.value
})

dayjs.extend(utc)
dayjs.extend(timezone)

function formatPST(dateStr) {
  if (!dateStr) return ''
  return dayjs.utc(dateStr).tz('America/Los_Angeles').format('MMM D, YYYY h:mm A [PST]')
}

// Debounced server-side search with replace
watch(search, (val) => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  searchTimeout.value = setTimeout(() => {
    if (val && val.trim().length > 1) {
      fetchContacts(`/api/contacts/?search=${encodeURIComponent(val.trim())}`, true)
    } else {
      fetchContacts('/api/contacts/', true)
    }
  }, 350)
})

function selectContact(contact) {
  selectedContact.value = contact
  isEditing.value = false
  isCreating.value = false
}

function getInitials(contact) {
  return (contact.first_name?.[0] || '') + (contact.last_name?.[0] || '')
}

function editContact(contact) {
  editContactData.value = { ...contact }
  isEditing.value = true
  isCreating.value = false
}

function handleEditCancel() {
  isEditing.value = false
  // Select the first contact if available (optional, or keep current)
  if (contacts.value.length > 0) {
    selectedContact.value = contacts.value[0]
  } else {
    selectedContact.value = null
  }
  // Scroll all overflow-auto panels and the outer container to top
  setTimeout(() => {
    document.querySelectorAll('.overflow-auto').forEach(panel => {
      panel.scrollTop = 0
    })
    if (contactsContainer.value) {
      contactsContainer.value.scrollTop = 0
    }
    window.scrollTo({ top: 0 })
  }, 0)
}

function startCreateContact() {
  isCreating.value = true
  isEditing.value = false
  selectedContact.value = null
}

function handleCreated(newContact) {
  // Add the new contact to the top of the list
  contacts.value.unshift(newContact)
  isCreating.value = false
  selectedContact.value = newContact

  // Scroll all overflow-auto panels and the outer container to top
  setTimeout(() => {
    document.querySelectorAll('.overflow-auto').forEach(panel => {
      panel.scrollTop = 0
    })
    // Scroll the outer container if scrollable
    if (contactsContainer.value) {
      contactsContainer.value.scrollTop = 0
    }
    // Also scroll the window, just in case
    window.scrollTo({ top: 0 })
  }, 0)
}

// Call this when the user cancels creating a contact
function handleCreateCancel() {
  isCreating.value = false
  // Select the first contact if available
  if (contacts.value.length > 0) {
    selectedContact.value = contacts.value[0]
  } else {
    selectedContact.value = null
  }
  // Scroll all overflow-auto panels and the outer container to top
  setTimeout(() => {
    document.querySelectorAll('.overflow-auto').forEach(panel => {
      panel.scrollTop = 0
    })
    // Scroll the outer container if scrollable
    if (contactsContainer.value) {
      contactsContainer.value.scrollTop = 0
    }
    // Also scroll the window, just in case
    window.scrollTo({ top: 0 })
  }, 0)
}

async function saveContact() {
  try {
    let payload = { ...editContactData.value }
    delete payload.client_type_display
    delete payload.id
    delete payload.date_updated
    delete payload.date_created
    delete payload.user_updated
    payload = stripBlanks(payload)

    const res = await axios.patch(`/api/contacts/${editContactData.value.id}/`, payload)
    Object.assign(selectedContact.value, res.data)
    const idx = contacts.value.findIndex(c => c.id === res.data.id)
    if (idx !== -1) contacts.value[idx] = res.data
    isEditing.value = false
  } catch (e) {
    alert('Failed to save contact')
  }
}

function stripBlanks(obj) {
  const result = {}
  for (const [key, value] of Object.entries(obj)) {
    if (value !== '' && value !== null && value !== undefined) {
      result[key] = value
    }
  }
  return result
}

// Always replace contacts on search, only append on infinite scroll
async function fetchContacts(url = null, append = false) {
  if (!append) {
    loading.value = true
  }
  loadingMore.value = append
  
  try {
    const apiUrl = url || '/api/contacts/'
    const params = url ? {} : {
      per: per.value,
      search: search.value.trim() || undefined
    }
    
    const { data } = await axios.get(apiUrl, { params })
    
    if (data) {
      if (append) {
        // Prevent duplicates when appending
        const existingIds = new Set(contacts.value.map(c => c.id))
        const newResults = (data.results || data).filter(c => !existingIds.has(c.id))
        contacts.value = [...contacts.value, ...newResults]
      } else {
        // Replace contacts for new search or initial load
        contacts.value = data.results || data
        totalCount.value = data.count || contacts.value.length
      }
      nextPage.value = data.next
    }
    
    if (contacts.value.length && !selectedContact.value) {
      selectedContact.value = contacts.value[0]
    }
  } catch (e) {
    console.error('Failed to fetch contacts:', e)
    if (!append) {
      contacts.value = []
      totalCount.value = 0
    }
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

// Infinite scroll handler
function onScroll(e) {
  const el = e.target
  if (
    el.scrollTop + el.clientHeight >= el.scrollHeight - 10 &&
    nextPage.value &&
    !loadingMore.value
  ) {
    fetchContacts(nextPage.value, true)
  }
}

// Search functionality
function onSearch() {
  // Reset pagination and fetch new results
  nextPage.value = null
  selectedContact.value = null
  fetchContacts()
}

// Handle per-page change
function onPerChange() {
  // Reset pagination and fetch new results
  nextPage.value = null
  selectedContact.value = null
  fetchContacts()
}

onMounted(() => {
  fetchContacts()
})
</script>

<style scoped>
/* Modern Contact Page Styles - Better Contrast */
.contacts-page {
  padding: 20px;
  background: #fff; 
  min-height: 100vh;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  padding: 0.8rem 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

.page-title {
  font-size: 1.8rem;
  font-weight: 500;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
  text-decoration: none;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  color: white;
  text-decoration: none;
}

/* Controls Section */
.controls-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.95);
  padding: 0.5rem 1.5rem;
  border-radius: 15px;
  margin-bottom: 5px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  gap: 2rem;
  backdrop-filter: blur(10px);
}

.search-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  z-index: 2;
}

.search-input {
  width: 100%;
  padding: 0.3rem 1rem 0.3rem 3rem;
  border: 2px solid #e9ecef;
  border-radius: 50px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-controls {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.per-page-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.total-count {
  display: flex;
  align-items: center;
  padding: 0.3rem 0.8rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 20px;
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.total-count .control-label {
  color: #667eea;
  font-weight: 600;
  font-size: 0.85rem;
}

.control-label {
  color: #6c757d;
  font-weight: 500;
}

.form-select {
  border: 2px solid #dddedf;
  border-radius: 10px;
  padding: 0.2rem 0.4rem 0.2rem 0.8rem;
  background: #e9e9e9;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  background: white;
}

.contacts-content {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  min-height: calc(100vh - 180px);
  backdrop-filter: blur(10px);
}

.contacts-sidebar {
  background: rgba(248, 249, 250, 0.8);
  border-right: 1px solid rgba(233, 236, 239, 0.5);
  height: calc(100vh - 180px);
  overflow-y: auto;
}

.contacts-main {
  background: white;
  height: calc(100vh - 180px);
  overflow-y: auto;
}

.contact-list-container {
  padding: 1rem;
}

.contact-item {
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.contact-item:hover {
  background: #f8f9fa;
  border-color: #667eea;
  transform: translateX(2px);
}

.contact-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
}

.contact-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1rem;
  font-weight: 600;
}

.contact-item.active .contact-avatar {
  background: rgba(255, 255, 255, 0.2);
}

.contact-info h6 {
  font-weight: 600;
  margin: 0;
  font-size: 0.95rem;
  color: #2c3e50;
}

.contact-type,
.contact-email {
  font-size: 0.8rem;
  margin: 0;
  color: #6c757d;
  font-weight: 400;
}

.contact-item.active .contact-info h6,
.contact-item.active .contact-type,
.contact-item.active .contact-email {
  color: white;
}

.details-header {
  padding: 2rem;
  background: white;
  border-bottom: 1px solid #e9ecef;
  margin: 0;
}

.details-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
}

.details-name {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.details-type {
  color: #6c757d;
  font-size: 1rem;
  font-weight: 400;
}

.info-section {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem;
}

.section-title {
  color: #2c3e50;
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e9ecef;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 500;
  color: #6c757d;
  min-width: 120px;
  font-size: 0.9rem;
}

.info-value {
  color: #2c3e50;
  flex: 1;
  font-size: 0.9rem;
}

.edit-btn {
  background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
  border: none;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.empty-state i {
  font-size: 3rem;
  color: #dee2e6;
  margin-bottom: 1rem;
}

.loading-indicator {
  text-align: center;
  padding: 1rem;
  color: #667eea;
  font-weight: 500;
}

.filter-tabs-container {
  background: white;
  border-bottom: 1px solid #e9ecef;
  padding: 1rem 0;
}

.filter-tabs {
  display: flex;
  gap: 1rem;
}

.filter-tab {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  color: #6c757d;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
}

.filter-tab .badge {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 10px;
}

.search-container-header {
  position: relative;
  width: 300px;
}

.search-input-header {
  width: 100%;
  padding: 0.5rem 0.75rem 0.5rem 2.5rem;
  border: 1px solid #dee2e6;
  border-radius: 20px;
  font-size: 0.9rem;
  background: #f8f9fa;
}

.search-input-header:focus {
  outline: none;
  border-color: #667eea;
  background: white;
}

.contacts-content {
  background: white;
  min-height: calc(100vh - 140px);
}

.contacts-sidebar {
  background: #f8f9fa;
  border-right: 1px solid #e9ecef;
  height: calc(100vh - 140px);
  overflow-y: auto;
}

.contacts-main {
  background: white;
  height: calc(100vh - 140px);
  overflow-y: auto;
}

.contact-list-container {
  padding: 1rem;
}

.contact-item {
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.contact-item:hover {
  background: #f8f9fa;
  border-color: #667eea;
  transform: translateX(2px);
}

.contact-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
}

.contact-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1rem;
  font-weight: 600;
}

.contact-item.active .contact-avatar {
  background: rgba(255, 255, 255, 0.2);
}

.contact-info h6 {
  font-weight: 600;
  margin: 0;
  font-size: 0.95rem;
  color: #2c3e50;
}

.contact-type {
  font-size: 0.8rem;
  margin: 0;
  color: #6c757d;
  font-weight: 400;
}

.contact-email {
  font-size: 0.8rem;
  margin: 0;
  color: #6c757d;
  font-weight: 400;
}

.contact-item.active .contact-info h6,
.contact-item.active .contact-type,
.contact-item.active .contact-email {
  color: white;
}

.create-btn {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  border: none;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.create-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.details-header {
  padding: 2rem;
  background: white;
  border-bottom: 1px solid #e9ecef;
  margin: 0;
}

.details-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
}

.details-name {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.details-type {
  color: #6c757d;
  font-size: 1rem;
  font-weight: 400;
}

.info-section {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem;
}

.section-title {
  color: #2c3e50;
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e9ecef;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 500;
  color: #6c757d;
  min-width: 120px;
  font-size: 0.9rem;
}

.info-value {
  color: #2c3e50;
  flex: 1;
  font-size: 0.9rem;
}

.edit-btn {
  background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
  border: none;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.empty-state i {
  font-size: 3rem;
  color: #dee2e6;
  margin-bottom: 1rem;
}

.loading-indicator {
  text-align: center;
  padding: 1rem;
  color: #667eea;
  font-weight: 500;
}

/* Remove old redundant styles */

.edit-form {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

.form-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.section-title {
  color: #495057;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e9ecef;
}

.form-control {
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  background: white;
}

.form-label {
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 25px;
  padding: 0.75rem 2rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
  border: none;
  border-radius: 25px;
  padding: 0.75rem 2rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(108, 117, 125, 0.3);
}

.btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(108, 117, 125, 0.4);
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.empty-state i {
  font-size: 4rem;
  color: #e9ecef;
  margin-bottom: 1rem;
}

.loading-indicator {
  text-align: center;
  padding: 1rem;
  color: #667eea;
  font-weight: 500;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .contacts-sidebar {
    width: 100% !important;
    border-radius: 15px 15px 0 0;
  }
  
  .contacts-main {
    border-radius: 0 0 15px 15px;
  }
  
  .page-header {
    border-radius: 15px 15px 0 0;
  }
  
  .details-name {
    font-size: 1.5rem;
  }
  
  .details-avatar {
    width: 60px;
    height: 60px;
    font-size: 1.8rem;
  }
}
</style>

<template>
  <div class="contacts-page">
    <!-- header row -->
    <div class="page-header">
      <h3 class="page-title">CONTACTS</h3>
      <button class="btn btn-primary" @click="startCreateContact">
        <i class="fas fa-plus me-2"></i>
        Create Contact
      </button>
    </div>

    <!-- search and controls -->
    <div class="controls-section">
      <div class="search-controls">
        <div class="search-box">
          <i class="fas fa-search search-icon"></i>
          <input 
            v-model="search"
            type="text"
            placeholder="Search contacts by name, email, company…"
            class="search-input">
        </div>
      </div>
      
      <div class="filter-controls">
        <div class="per-page-selector">
          <label class="control-label">Show:</label>
          <select v-model.number="per" @change="onPerChange" class="form-select">
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
          <span class="control-label">entries</span>
        </div>
        <div v-if="totalCount" class="total-count">
          <span class="control-label">{{ totalCount }} total contacts</span>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="contacts-content">
      <div class="container-fluid">
        <div class="row g-0">
          <!-- Left Sidebar: Contact List -->
          <div class="col-md-4">
            <div class="contacts-sidebar" @scroll="onScroll">
              <!-- Contact List -->
              <div class="contact-list-container">
                <div v-if="loading && !contacts.length" class="loading-indicator">
                  <i class="fas fa-spinner fa-spin me-2"></i>
                  Loading contacts...
                </div>
                <div v-else-if="displayedContacts.length">
                  <div
                    v-for="contact in displayedContacts"
                    :key="contact.id"
                    :class="['contact-item', { active: selectedContact && selectedContact.id === contact.id }]"
                    @click="selectContact(contact)"
                  >
                    <div class="d-flex align-items-center">
                      <div class="contact-avatar me-3">
                        {{ getInitials(contact) }}
                      </div>
                      <div class="contact-info flex-grow-1">
                        <h6>{{ contact.first_name }} {{ contact.last_name }}</h6>
                        <p class="contact-type">{{ contact.client_type_display }}</p>
                        <p class="contact-email">{{ contact.email }}</p>
                      </div>
                    </div>
                  </div>
                  <div v-if="loadingMore" class="loading-indicator">
                    <i class="fas fa-spinner fa-spin me-2"></i>
                    Loading more contacts...
                  </div>
                </div>
                <div v-else class="empty-state">
                  <i class="fas fa-user-slash"></i>
                  <p>{{ search ? 'No contacts found matching your search' : 'No contacts found' }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Right Main Content -->
          <div class="col-md-8">
            <div class="contacts-main">
        <!-- Create Contact Form -->
        <ContactCreate
          v-if="isCreating"
          @created="handleCreated"
          @cancel="handleCreateCancel"
        />
        
        <!-- Contact Details View -->
        <div v-else-if="selectedContact && !isEditing" class="p-4">
          <!-- Contact Header -->
          <div class="details-header">
            <div class="d-flex align-items-center">
              <div class="details-avatar me-4">
                {{ getInitials(selectedContact) }}
              </div>
              <div class="flex-grow-1">
                <h1 class="details-name">{{ selectedContact.first_name }} {{ selectedContact.last_name }}</h1>
                <p class="details-type">{{ selectedContact.client_type_display }}</p>
              </div>
              <button class="edit-btn" @click="editContact(selectedContact)">
                <i class="fas fa-edit me-2"></i>
                Edit Contact
              </button>
            </div>
          </div>

          <!-- Contact Information Sections -->
          <div class="row">
            <!-- Basic Information -->
            <div class="col-md-6">
              <div class="info-section">
                <h5 class="section-title">
                  <i class="fas fa-user me-2"></i>
                  Basic Information
                </h5>
                <div v-if="selectedContact.company" class="info-item">
                  <span class="info-label">Company:</span>
                  <span class="info-value">{{ selectedContact.company }}</span>
                </div>
                <div v-if="selectedContact.website" class="info-item">
                  <span class="info-label">Website:</span>
                  <span class="info-value">
                    <a :href="selectedContact.website" target="_blank" class="text-decoration-none">
                      {{ selectedContact.website }}
                    </a>
                  </span>
                </div>
                <div v-if="selectedContact.gender" class="info-item">
                  <span class="info-label">Gender:</span>
                  <span class="info-value">{{ selectedContact.gender }}</span>
                </div>
                <div v-if="selectedContact.date_birth" class="info-item">
                  <span class="info-label">Date of Birth:</span>
                  <span class="info-value">{{ selectedContact.date_birth }}</span>
                </div>
              </div>
            </div>

            <!-- Contact Details -->
            <div class="col-md-6">
              <div class="info-section">
                <h5 class="section-title">
                  <i class="fas fa-phone me-2"></i>
                  Contact Information
                </h5>
                <div v-if="selectedContact.email" class="info-item">
                  <span class="info-label">Primary Email:</span>
                  <span class="info-value">{{ selectedContact.email }}</span>
                </div>
                <div v-if="selectedContact.email2" class="info-item">
                  <span class="info-label">Email 2:</span>
                  <span class="info-value">{{ selectedContact.email2 }}</span>
                </div>
                <div v-if="selectedContact.email3" class="info-item">
                  <span class="info-label">Email 3:</span>
                  <span class="info-value">{{ selectedContact.email3 }}</span>
                </div>
                <div v-if="selectedContact.phone" class="info-item">
                  <span class="info-label">Phone:</span>
                  <span class="info-value">{{ selectedContact.phone }}</span>
                </div>
                <div v-if="selectedContact.mobile" class="info-item">
                  <span class="info-label">Mobile:</span>
                  <span class="info-value">{{ selectedContact.mobile }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Address Information -->
          <div v-if="selectedContact.address || selectedContact.city || selectedContact.state || selectedContact.zip">
            <div class="info-section">
              <h5 class="section-title">
                <i class="fas fa-map-marker-alt me-2"></i>
                Address Information
              </h5>
              <div v-if="selectedContact.address" class="info-item">
                <span class="info-label">Address:</span>
                <span class="info-value">{{ selectedContact.address }}</span>
              </div>
              <div class="d-flex gap-4">
                <div v-if="selectedContact.city" class="info-item flex-fill">
                  <span class="info-label">City:</span>
                  <span class="info-value">{{ selectedContact.city }}</span>
                </div>
                <div v-if="selectedContact.state" class="info-item flex-fill">
                  <span class="info-label">State:</span>
                  <span class="info-value">{{ selectedContact.state }}</span>
                </div>
                <div v-if="selectedContact.zip" class="info-item flex-fill">
                  <span class="info-label">Zip:</span>
                  <span class="info-value">{{ selectedContact.zip }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Emergency Contact -->
          <div v-if="selectedContact.ems_name || selectedContact.ems_phone">
            <div class="info-section">
              <h5 class="section-title">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Emergency Contact
              </h5>
              <div v-if="selectedContact.ems_name" class="info-item">
                <span class="info-label">Emergency Contact:</span>
                <span class="info-value">{{ selectedContact.ems_name }}</span>
              </div>
              <div v-if="selectedContact.ems_phone" class="info-item">
                <span class="info-label">Emergency Phone:</span>
                <span class="info-value">{{ selectedContact.ems_phone }}</span>
              </div>
            </div>
          </div>

          <!-- Additional Information -->
          <div v-if="selectedContact.notes || selectedContact.tags">
            <div class="info-section">
              <h5 class="section-title">
                <i class="fas fa-sticky-note me-2"></i>
                Additional Information
              </h5>
              <div v-if="selectedContact.notes" class="info-item">
                <span class="info-label">Notes:</span>
                <span class="info-value">{{ selectedContact.notes }}</span>
              </div>
              <div v-if="selectedContact.tags" class="info-item">
                <span class="info-label">Tags:</span>
                <span class="info-value">{{ selectedContact.tags }}</span>
              </div>
              <div v-if="selectedContact.date_created" class="info-item">
                <span class="info-label">Created:</span>
                <span class="info-value">{{ formatPST(selectedContact.date_created) }}</span>
              </div>
              <div v-if="selectedContact.date_updated" class="info-item">
                <span class="info-label">Last Updated:</span>
                <span class="info-value">{{ formatPST(selectedContact.date_updated) }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Edit Contact Form -->
        <div v-else-if="selectedContact && isEditing" class="p-4">
          <form @submit.prevent="saveContact" class="edit-form">
            <div class="d-flex align-items-center mb-4">
              <h2 class="mb-0">
                <i class="fas fa-edit me-2"></i>
                Edit Contact
              </h2>
            </div>

            <!-- Basic Information Section -->
            <div class="form-section">
              <h5 class="section-title">Basic Information</h5>
              <div class="row g-3">
                <div class="col-md-4">
                  <label class="form-label">First Name</label>
                  <input v-model="editContactData.first_name" class="form-control" />
                </div>
                <div class="col-md-4">
                  <label class="form-label">Middle Name</label>
                  <input v-model="editContactData.middle_name" class="form-control" />
                </div>
                <div class="col-md-4">
                  <label class="form-label">Last Name</label>
                  <input v-model="editContactData.last_name" class="form-control" />
                </div>
              </div>
              <div class="row g-3 mt-2">
                <div class="col-md-3">
                  <label class="form-label">Company</label>
                  <input v-model="editContactData.company" class="form-control">
                </div>
                <div class="col-md-3">
                  <label class="form-label">Date of Birth</label>
                  <input v-model="editContactData.date_birth" type="date" class="form-control">
                </div>
                <div class="col-md-3">
                  <label class="form-label">Website</label>
                  <input v-model="editContactData.website" type="url" class="form-control">
                </div>
                <div class="col-md-3">
                  <label class="form-label">Gender</label>
                  <input v-model="editContactData.gender" class="form-control">
                </div>
              </div>
            </div>

            <!-- Contact Information Section -->
            <div class="form-section">
              <h5 class="section-title">Contact Information</h5>
              <div class="row g-3">
                <div class="col-md-4">
                  <label class="form-label">Primary Email</label>
                  <input v-model="editContactData.email" type="email" class="form-control">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Email 2</label>
                  <input v-model="editContactData.email2" type="email" class="form-control">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Email 3</label>
                  <input v-model="editContactData.email3" type="email" class="form-control">
                </div>
              </div>
              <div class="row g-3 mt-2">
                <div class="col-md-3">
                  <label class="form-label">Phone</label>
                  <input v-model="editContactData.phone" type="tel" class="form-control" />
                </div>
                <div class="col-md-3">
                  <label class="form-label">Phone 2</label>
                  <input v-model="editContactData.phone2" type="tel" class="form-control" />
                </div>
                <div class="col-md-3">
                  <label class="form-label">Phone 3</label>
                  <input v-model="editContactData.phone3" type="tel" class="form-control" />
                </div>
                <div class="col-md-3">
                  <label class="form-label">Mobile</label>
                  <input v-model="editContactData.mobile" type="tel" class="form-control" />
                </div>
              </div>
            </div>

            <!-- Address Section -->
            <div class="form-section">
              <h5 class="section-title">Address Information</h5>
              <div class="mb-3">
                <label class="form-label">Address</label>
                <input v-model="editContactData.address" class="form-control" />
              </div>
              <div class="row g-3">
                <div class="col-md-4">
                  <label class="form-label">City</label>
                  <input v-model="editContactData.city" class="form-control" />
                </div>
                <div class="col-md-4">
                  <label class="form-label">State</label>
                  <input v-model="editContactData.state" class="form-control" />
                </div>
                <div class="col-md-4">
                  <label class="form-label">Zip</label>
                  <input v-model="editContactData.zip" class="form-control" />
                </div>
              </div>
            </div>

            <!-- Emergency Contact Section -->
            <div class="form-section">
              <h5 class="section-title">Emergency Contact</h5>
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Emergency Contact Name</label>
                  <input v-model="editContactData.ems_name" class="form-control">
                </div>
                <div class="col-md-6">
                  <label class="form-label">Emergency Contact Phone</label>
                  <input v-model="editContactData.ems_phone" type="tel" class="form-control">
                </div>
              </div>
            </div>

            <!-- Additional Information Section -->
            <div class="form-section">
              <h5 class="section-title">Additional Information</h5>
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Tags</label>
                  <input v-model="editContactData.tags" class="form-control">
                </div>
                <div class="col-md-6">
                  <label class="form-label">Mail Lists</label>
                  <input v-model="editContactData.mail_lists" class="form-control">
                </div>
              </div>
              <div class="mt-3">
                <label class="form-label">Notes</label>
                <textarea v-model="editContactData.notes" rows="4" class="form-control"></textarea>
              </div>
            </div>

            <!-- Form Actions -->
            <div class="d-flex gap-3 mt-4">
              <button type="submit" class="btn btn-primary">
                <i class="fas fa-save me-2"></i>
                Save Changes
              </button>
              <button type="button" class="btn btn-secondary" @click="handleEditCancel">
                <i class="fas fa-times me-2"></i>
                Cancel
              </button>
            </div>
          </form>
        </div>
        
        <!-- Empty State -->
        <div v-else class="empty-state">
          <i class="fas fa-user-circle"></i>
          <h5>Select a contact to view details</h5>
          <p>Choose a contact from the list to see their information</p>
        </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>