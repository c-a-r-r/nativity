<template>
  <div class="marketing-views-wrapper">

    <!-- header row -->
    <div class="page-header">
      <h3 class="page-title">MARKETING</h3>
      <router-link :to="{ name: 'QuoteList' }" class="btn btn-primary">
        <i class="fas fa-arrow-left"></i> Back to All Quotes
      </router-link>
    </div>

    <!-- marketing stats -->
    <div class="stats-nav-container">
      <div class="stats-nav">
        <div class="stats-pill">
          <span class="pill-text">Total Marketing Quotes</span>
          <span class="pill-badge">{{ totalCount }}</span>
        </div>
        <div class="stats-pill">
          <span class="pill-text">Need Trip Creation</span>
          <span class="pill-badge">{{ totalQuotesWithoutTrips }}</span>
        </div>
        <div class="stats-pill">
          <span class="pill-text">With Marketing Trips</span>
          <span class="pill-badge">{{ totalWithTrips }}</span>
        </div>
        <div class="stats-pill">
          <span class="pill-text">Showing This Page</span>
          <span class="pill-badge">{{ quotes.length }}</span>
        </div>
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
            placeholder="Search church name, contact, destination…"
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
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-2">Loading marketing quotes...</p>
        </div>
        <template v-else>
          <div v-if="quotes.length" class="table-responsive">
            <table class="table table-sm table-hover">
              <thead>
                <tr>
                  <th>Quote&nbsp;ID</th>
                  <th>Date Created</th>
                  <th>Contact</th>
                  <th>Destination</th>
                  <th>Dep.&nbsp;Date</th>
                  <th>Dep.&nbsp;City</th>
                  <th>Church Name</th>
                  <th>Status</th>
                  <th>Trip Links</th>
                  <th>Actions</th>
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
                  <td>
                    <span v-if="hasMarketingTrip(quote)" class="badge bg-success">
                      <i class="fa fa-check me-1"></i>Trip Created
                    </span>
                    <span v-else class="badge bg-warning">
                      <i class="fa fa-clock me-1"></i>Needs Trip
                    </span>
                  </td>
                  <td>
                    <div class="d-flex gap-1" v-if="hasMarketingTrip(quote)">
                      <a v-if="quote.marketing_public_link" 
                         :href="getFullUrl(quote.marketing_public_link)" 
                         target="_blank" 
                         class="btn btn-xs btn-outline-primary">
                        <i class="fa fa-external-link-alt me-1"></i>Public
                      </a>
                      <a v-if="quote.marketing_private_link" 
                         :href="getFullUrl(quote.marketing_private_link)" 
                         target="_blank" 
                         class="btn btn-xs btn-outline-secondary">
                        <i class="fa fa-lock me-1"></i>Private
                      </a>
                    </div>
                    <span v-else class="text-muted small">No links yet</span>
                  </td>
                  <td>
                    <div class="d-flex gap-1">
                      <router-link :to="{ 
                          name: 'QuoteEdit', 
                          params: { id: quote.id },
                          query: { returnTo: 'marketing' }
                        }"
                                   class="btn btn-sm btn-outline-info"
                                   title="Edit Quote">
                        <i class="fa fa-pen" />
                      </router-link>
                      <button v-if="hasMarketingTrip(quote)"
                              class="btn btn-sm btn-outline-success"
                              @click="viewTrip(quote)"
                              title="View Marketing Trip">
                        <i class="fa fa-eye" />
                      </button>
                      <button v-else
                              class="btn btn-sm btn-outline-warning"
                              @click="createTrip(quote)"
                              title="Create Marketing Trip">
                        <i class="fa fa-plus" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="text-center py-5">
            <i class="fa fa-inbox fa-3x text-muted mb-3"></i>
            <h5 class="text-muted">No Marketing Quotes Found</h5>
            <p class="text-muted">There are no quotes with "Create marketing" workflow status at the moment.</p>
            <router-link :to="{ name: 'QuoteList' }" class="btn btn-primary">
              View All Quotes
            </router-link>
          </div>
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
import { ref, reactive, watch, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import Pagination from '@/shared/components/Pagination.vue'

// --------------- route helpers ---------------
const route  = useRoute()
const router = useRouter()

// --------------- constants ---------------
const perOptions = [10, 25, 50, 100]
const MARKETING_WORKFLOW_ID = 60 // "Create marketing" workflow status

// --------------- state ---------------
const quotes  = ref([])
const loading = ref(false)
const totalCount = ref(0) // Add total count for all quotes with workflow status 60
const totalWithTrips = ref(0) // Total quotes with marketing trips across all pages

const pageInfo = reactive({
  page: 1,
  totalPages: 1,
})

const per    = ref(Number(route.query.per ?? 25))
const search = ref(route.query.q ?? '')

// --------------- computed properties ---------------
const quotesWithTrips = computed(() => {
  return quotes.value.filter(quote => hasMarketingTrip(quote)).length
})

const quotesWithoutTrips = computed(() => {
  return quotes.value.filter(quote => !hasMarketingTrip(quote)).length
})

// Total counts across all pages
const totalQuotesWithoutTrips = computed(() => {
  return totalCount.value - totalWithTrips.value
})

// --------------- helpers ---------------
function formatDate(dt) {
  return dt ? new Date(dt).toLocaleDateString() : ''
}

function makeQuery(extra = {}) {
  return {
    path: route.path,
    query: {
      per:    per.value,
      page:   pageInfo.page,
      q:      search.value,
      ...extra
    }
  }
}

function hasMarketingTrip(quote) {
  return quote.marketing_public_link || quote.marketing_private_link
}

function getFullUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `${window.location.origin}${path}`
}

function viewTrip(quote) {
  if (quote.marketing_public_link) {
    window.open(getFullUrl(quote.marketing_public_link), '_blank')
  }
}

function createTrip(quote) {
  // Navigate to quote edit page where they can create the marketing trip
  // Add returnTo parameter so it comes back to marketing views
  router.push({ 
    name: 'QuoteEdit', 
    params: { id: quote.id },
    query: { returnTo: 'marketing' }
  })
}

// --------------- API ---------------
async function fetchQuotes() {
  loading.value = true
  try {
    const params = {
      per: per.value,
      page: pageInfo.page,
      q: search.value,
      workflow_status: MARKETING_WORKFLOW_ID // Filter by "Create marketing" status
    }
    
    const res = await axios.get('/api/quotes/', { params })
    quotes.value        = res.data.results || res.data || []
    totalCount.value    = res.data.count || quotes.value.length // Store total count
    pageInfo.totalPages = Math.ceil((res.data.count || quotes.value.length) / per.value)
    
    // Fetch all quotes to get accurate count of quotes with marketing trips
    await fetchTotalWithTrips()
  } catch (err) {
    quotes.value = []
    totalCount.value = 0
    totalWithTrips.value = 0
    pageInfo.totalPages = 1
    console.error('Failed to fetch marketing quotes:', err)
  } finally {
    loading.value = false
  }
}

async function fetchTotalWithTrips() {
  try {
    // Fetch all quotes with workflow status 60 to count those with marketing trips
    const params = {
      per: 1000, // Get enough to capture all 77 quotes
      workflow_status: MARKETING_WORKFLOW_ID
    }
    
    const res = await axios.get('/api/quotes/', { params })
    const allQuotes = res.data.results || res.data || []
    
    // Count quotes with marketing trips
    totalWithTrips.value = allQuotes.filter(quote => 
      quote.marketing_public_link || quote.marketing_private_link
    ).length
    
  } catch (err) {
    console.error('Failed to fetch total with trips:', err)
    totalWithTrips.value = 0
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

// --------------- react to query‑param changes ---------------
watch(
  () => route.query,
  q => {
    per.value     = Number(q.per ?? 25)
    search.value  = q.q ?? ''
    pageInfo.page = Number(q.page ?? 1)
    fetchQuotes()
  },
  { immediate: true }
)

onMounted(fetchQuotes)
</script>

<style scoped>
.marketing-views-wrapper {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
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

/* Stats Navigation */
.stats-nav-container {
  margin-bottom: 10px;
}

.stats-nav {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  padding: 0;
  background: transparent;
}

.stats-pill {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-left: 4px solid;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  min-width: 200px;
  flex: 1;
  min-height: 50px;
}

.stats-pill:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.pill-badge {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
  line-height: 1;
  margin: 0;
  margin-bottom: 0.25rem;
}

.pill-text {
  font-size: 0.875rem;
  color: #718096;
  font-weight: 500;
  line-height: 1.2;
  margin: 0;
}

/* Color variations for different stats - left border colors */
.stats-pill:nth-child(1) {
  border-left-color: #38b2ac; /* Teal */
}

.stats-pill:nth-child(2) {
  border-left-color: #ed8936; /* Orange */
}

.stats-pill:nth-child(3) {
  border-left-color: #38a169; /* Green */
}

.stats-pill:nth-child(4) {
  border-left-color: #805ad5; /* Purple */
}

/* Icon styling */
.stats-pill::after {
  content: '';
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  opacity: 0.6;
}

.stats-pill:nth-child(1)::after {
  background-color: #38b2ac;
}

.stats-pill:nth-child(2)::after {
  background-color: #ed8936;
}

.stats-pill:nth-child(3)::after {
  background-color: #38a169;
}

.stats-pill:nth-child(4)::after {
  background-color: #805ad5;
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

.table tr td:last-child,
.table tr th:last-child {
  border-right: none;
}

.btn-xs {
  padding: 0.15rem 0.4rem;
  font-size: 0.75rem;
  line-height: 1.2;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.badge {
  font-size: 0.75em;
}
</style>
