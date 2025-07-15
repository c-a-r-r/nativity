<template>
  <div class="container-fluid p-0">

    <!-- header row -->
    <div class="d-flex align-items-center justify-content-between mt-1">
      <h3 class="mb-0">QUOTES</h3>
      <router-link :to="{ name: 'QuoteCreate' }" class="btn btn-primary">
        Create a Quote
      </router-link>
    </div>

    <!-- status tabs -->
    <ul class="nav nav-tabs mt-2">
      <li class="nav-item" v-for="label in statusLabels" :key="label">
        <router-link
          class="nav-link"
          :class="{ active: currentStatus === label.toLowerCase() }"
          :to="makeQuery({ status: label.toLowerCase(), page: 1 })">
          {{ label }}
        </router-link>
      </li>
    </ul>

    <!-- filter + top pagination -->
    <div class="d-flex align-items-center justify-content-between mb-2">
      <form class="d-flex align-items-center flex-nowrap my-3" @submit.prevent="onSearch">
        <span class="me-2">Displaying</span>
        <select v-model.number="per"
                class="form-select form-select-sm me-2"
                style="width: auto;"
                @change="onPerChange">
          <option v-for="opt in perOptions" :key="opt" :value="opt">{{ opt }}</option>
        </select>
        <span class="me-4">records</span>
        <input v-model="search"
               type="text"
               placeholder="search…"
               class="form-control form-control-sm me-2"
               style="width: 190px;">
        <button class="btn btn-sm btn-primary">Go</button>
      </form>
      <Pagination
        v-if="pageInfo.totalPages > 1"
        :page="pageInfo.page"
        :total="pageInfo.totalPages"
        :make-query="makeQuery" />
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
const statusLabels = ['All', 'Draft', 'Sent', 'Approved', 'Archived']
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

// --------------- API ---------------
async function fetchQuotes() {
  loading.value = true
  try {
    const res = await axios.get('/api/quotes/', {
      params: {
        status: currentStatus.value,
        per:    per.value,
        page:   pageInfo.page,
        q:      search.value,
      }
    })
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
.table thead tr th {
  color: #222;
  font-size: 14px;
  font-weight: bold;                /* Optional: text color */
}
.table td, .table th {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px; /* Adjust as needed for each column */
  border-right: 1px solid #eeeeee;
  vertical-align: middle;
}
/* Remove the border from the last cell in each row */
.table tr td:last-child,
.table tr th:last-child {
  border-right: none;
}
</style>
