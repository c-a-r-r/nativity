<template>
  <div class="quote-list-wrapper">

    <!-- header row -->
    <div class="page-header">
      <h3 class="page-title">QUOTE MANAGEMENT</h3>
      <router-link :to="{ name: 'QuoteCreate' }" class="btn btn-primary">
        <i class="fas fa-plus"></i> Create Quote
      </router-link>
    </div>

    <!-- status tabs -->
    <div class="status-nav-container">
      <div class="status-nav">
        <button
          v-for="statusObj in statusLabels" 
          :key="statusObj.id"
          :class="['status-pill', { active: currentStatus === statusObj.id }]"
          @click="navigateToStatus(statusObj.id)">
          <span class="pill-text">{{ statusObj.label }}</span>
          <span v-if="statusObj.id === 'all'" class="pill-badge">{{ quotes.length }}</span>
        </button>
      </div>
    </div>

    <!-- search and controls -->
    <div class="controls-section">
      <div class="search-controls">
        <div class="search-box">
          <i class="fas fa-search search-icon"></i>
          <input 
            v-model="search"
            type="text"
            placeholder="Search quotes by id,contact, church, destination..."
            class="search-input"
            @keyup.enter="onSearch">
        </div>
        <button class="btn btn-search" @click="onSearch">
          <i class="fas fa-search"></i>
        </button>
      </div>
      
      <div class="filter-controls">
        <div class="per-page-selector">
          <label class="control-label">Show:</label>
          <select v-model.number="per" class="form-select" @change="onPerChange">
            <option v-for="opt in perOptions" :key="opt" :value="opt">{{ opt }}</option>
          </select>
          <span class="control-label">entries</span>
        </div>
        
        <Pagination
          v-if="pageInfo.totalPages > 1"
          :page="pageInfo.page"
          :total="pageInfo.totalPages"
          :make-query="makeQuery" 
          class="top-pagination" />
      </div>
    </div>

    <!-- quote table -->
    <div class="card bg-light mb-4 w-100" style="max-width: 100%;">
      <div class="card-body">
        <div v-if="loading" class="text-center py-5">
          Loading…
        </div>
        <template v-else>
          <div v-if="quotes.length" class="table-responsive">
            <table class="table table-sm table-hover" >
              <thead>
                <tr>
                  <th>Quote&nbsp;ID</th><th>Date Created</th><th>Contact</th><th>Destination</th>
                  <th>Dep.&nbsp;Date</th><th>Dep.&nbsp;City</th><th>Church Name</th>
                  <th>Workflow</th><th>User</th><th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="quote in quotes" :key="quote.id">
                  <td>NP-{{ quote.id }}</td>
                  <td>{{ formatDate(quote.date_created) }}</td>
                  <td>{{ quote.client_name }}</td>
                  <td>{{ quote.trip_name }}</td>
                  <td>{{ formatDate(quote.departure_date) }}</td>
                  <td>{{ quote.departure_city_display }}</td>
                  <td>{{ quote.church_name }}</td>
                  <td>{{ quote.workflow_status_nombre }}</td>
                  <td>{{ quote.user_full_name }}</td>
                  <td>
                    <router-link :to="{ name: 'QuoteEdit', params: { id: quote.id } }"
                                 class="btn btn-sm btn-outline-info me-1">
                      <i class="fa fa-pen" />
                    </router-link>
                    <button class="btn btn-sm btn-outline-danger"
                            @click="deleteQuote(quote.id)">
                      <i class="fa fa-trash" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <h5 v-else class="alert alert-primary">No Quote Records</h5>
        </template>
      </div>
    </div>

    <!-- bottom pagination -->
    <div v-if="pageInfo.totalPages > 1" class="mb-4">
      <Pagination
        :page="pageInfo.page"
        :total="pageInfo.totalPages"
        :make-query="makeQuery" />
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import Pagination from '@/shared/components/Pagination.vue'

// --------------- route helpers ---------------
const route  = useRoute()
const router = useRouter()

// --------------- constants ---------------
const statusLabels = [
  { id: 'draft', label: 'Draft' },
  { id: 'sent-to-contact', label: 'Sent to Contact' },
  { id: 'accepted', label: 'Accepted' },
  { id: 'rejected', label: 'Rejected' },
  { id: 'completed', label: 'Completed' },
  { id: 'all', label: 'All' }
]
const perOptions   = [10, 25, 50, 100]

// --------------- state ---------------
const quotes  = ref([])
const loading = ref(false)

const pageInfo = reactive({
  page: 1,
  totalPages: 1,
})

const currentStatus = ref(route.query.status ?? 'all')
const per    = ref(Number(route.query.per ?? 25))
const search = ref(route.query.q ?? '')

// --------------- helpers ---------------
function formatDate(dt) {
  return dt ? new Date(dt).toLocaleDateString() : ''
}

function makeQuery(extra = {}) {
  return {
    path: route.path,
    query: {
      status: currentStatus.value,
      per:    per.value,
      page:   pageInfo.page,
      q:      search.value,
      ...extra
    }
  }
}

function navigateToStatus(statusId) {
  currentStatus.value = statusId
  pageInfo.page = 1
  router.push(makeQuery({ status: statusId, page: 1 }))
}

// --------------- API ---------------
async function fetchQuotes() {
  loading.value = true
  try {
    const params = {
      per: per.value,
      page: pageInfo.page,
      q: search.value,
    }
    
    // Add status filter - backend handles 'all' by default
    if (currentStatus.value !== 'all') {
      params.status = currentStatus.value
    }
    
    const res = await axios.get('/api/quotes/', { params })
    quotes.value        = res.data.results || res.data || []
    pageInfo.totalPages = Math.ceil((res.data.count || quotes.value.length) / per.value)
  } catch (err) {
    quotes.value = []
    pageInfo.totalPages = 1
    // Optionally show an error message
    console.error('Failed to fetch quotes:', err)
  } finally {
    loading.value = false
  }
}

// --------------- UI callbacks ---------------
function onPerChange() {
  pageInfo.page = 1
  router.push(makeQuery({ page: 1 }))
}

function onSearch() {
  pageInfo.page = 1
  router.push(makeQuery({ page: 1, q: search.value.trim() }))
}

async function deleteQuote(id) {
  if (!confirm('Delete this quote?')) return
  await axios.delete(`/api/quotes/${id}`)
  fetchQuotes()
}

// --------------- react to query‑param changes ---------------
watch(
  () => route.query,
  q => {
    currentStatus.value = q.status ?? 'all'
    per.value           = Number(q.per ?? 25)
    search.value        = q.q ?? ''
    pageInfo.page       = Number(q.page ?? 1)
    fetchQuotes()
  },
  { immediate: true }
)

onMounted(fetchQuotes)
</script>
<style scoped>
.quote-list-wrapper {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 5px;
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

/* Status Navigation */
.status-nav-container {
  margin-bottom: 5px;
}

.status-nav {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding: 1rem 1.5rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

.status-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.2rem 1.25rem;
  border: 2px solid #d8dbdf;
  border-radius: 25px;
  background: rgb(237, 235, 251);
  color: #5e656c;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.status-pill:hover {
  border-color: #667eea;
  color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
}

.status-pill.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.pill-badge {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 15px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-pill:not(.active) .pill-badge {
  background: #667eea;
  color: white;
}

/* Controls Section */
.controls-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 0.5rem 1.5rem;
  border-radius: 15px;
  margin-bottom: 5px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  gap: 2rem;
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

.btn-search {
  padding: 0.3rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 50px;
  color: white;
  transition: all 0.3s ease;
}

.btn-search:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
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

.status-tabs {
  margin-bottom: 20px;
}

.table thead tr th {
  color: #222;
  font-size: 14px;
  font-weight: bold;
}
.table td, .table th {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
  border-right: 1px solid #eeeeee;
  vertical-align: middle;
}
/* Remove the border from the last cell in each row */
.table tr td:last-child,
.table tr th:last-child {
  border-right: none;
}

/* Fix for navigation tabs to prevent text cutoff */
.nav-tabs .nav-link {
  white-space: nowrap;
  padding: 0.5rem 0.75rem;
  font-size: 0.9rem;
}

.nav-tabs {
  flex-wrap: wrap;
}
</style>
