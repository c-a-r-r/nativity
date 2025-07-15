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

const isEditing = ref(false)
const editContactData = ref({})
const isCreating = ref(false)
const contactsContainer = ref(null)
// Multi-field client-side filter for fallback
const filteredContacts = computed(() => {
  if (!search.value.trim()) return contacts.value
  const q = search.value.toLowerCase()
  return contacts.value.filter(c =>
    [
      c.first_name,
      c.last_name,
      c.email,
      c.email2,
      c.email3,
      c.phone,
      c.phone2,
      c.phone3,
      c.mobile,
      c.company,
      c.address,
      c.city,
      c.state,
      c.zip,
      c.tags,
      c.mail_lists,
      c.name_tag,
      c.from_web,
      c.hearabout,
      c.unique_ident,
      c.email_maillist
    ]
      .map(v => (v || '').toLowerCase())
      .some(v => v.includes(q))
  )
})

dayjs.extend(utc)
dayjs.extend(timezone)

function formatPST(dateStr) {
  if (!dateStr) return ''
  return dayjs.utc(dateStr).tz('America/Los_Angeles').format('MMM D, YYYY h:mm A [PST]')
}

// Debounced server-side search with replace
let searchTimeout = null
watch(search, (val) => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
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

// Always replace contacts on search, only append on infinite scroll
async function fetchContacts(url = '/api/contacts/', replace = true) {
  loadingMore.value = true
  try {
    const res = await axios.get(url)
    const data = res.data
    if (Array.isArray(data)) {
      contacts.value = data
      nextPage.value = null
    } else {
      if (replace) {
        contacts.value = data.results
      } else {
        // Only append for infinite scroll, not for search
        // Prevent duplicates when appending
        const existingIds = new Set(contacts.value.map(c => c.id))
        const newResults = data.results.filter(c => !existingIds.has(c.id))
        contacts.value = [...contacts.value, ...newResults]
      }
      nextPage.value = data.next
    }
    if (contacts.value.length && !selectedContact.value) selectedContact.value = contacts.value[0]
  } catch (e) {
    // fallback: do nothing, keep current contacts
  }
  loadingMore.value = false
}

// Infinite scroll handler
function onScroll(e) {
  const el = e.target
  if (
    el.scrollTop + el.clientHeight >= el.scrollHeight - 10 &&
    nextPage.value &&
    !loadingMore.value
  ) {
    fetchContacts(nextPage.value, false)
  }
}

onMounted(() => {
  fetchContacts()
})
</script>

<style scoped>
.edit-form-bg {
  background: #0d6efd;
  color: #fff;
  transition: background 0.2s;
}
.edit-form-bg:hover {
  background: #627aae;
}
</style>

<template>
  <div ref="contactsContainer" class="d-flex" style="height: 100vh;">
    <!-- Left: Contact List -->
    <div
      class="border-end bg-white"
      style="width: 350px; display: flex; flex-direction: column;">
      <!-- Create Contact button -->
      <div class="px-3 pt-3">
        <button class="btn btn-primary w-100" @click="startCreateContact">
          + Create Contact
        </button>
      </div>
      <!-- Search bar -->
      <div class="pt-2 pb-2 px-3">  
        <input
          v-model="search"
          class="form-control rounded-pill"
          type="text"
          placeholder="Search contacts..."
        />
      </div>
      <!-- Contact list -->
      <div class="flex-grow-1 overflow-auto" @scroll="onScroll">
        <ul class="list-unstyled mb-0">
          <li
            v-for="contact in filteredContacts"
            :key="contact.id"
            :class="['d-flex align-items-center px-3 py-2 contact-item', {active: selectedContact && selectedContact.id === contact.id}]"
            style="cursor: pointer;"
            @click="selectContact(contact)"
          >
            <div class="me-3">
              <div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center" style="width:48px; height:48px; color:white; font-size:1.3rem;">
                {{ getInitials(contact) }}
              </div>
            </div>
            <div>
              <div class="fw-bold">{{ contact.first_name }} {{ contact.last_name }}</div>
              <div class="text-muted small">{{ contact.client_type_display }}</div>
            </div>
          </li>
        </ul>
        <div v-if="loadingMore" class="text-center py-2">Loading...</div>
      </div>
    </div>
    <!-- Right: Details/Edit/Create -->
    <div class="flex-grow-1 p-4 overflow-auto">
      <ContactCreate
        v-if="isCreating"
        @created="handleCreated"
        @cancel="handleCreateCancel"
      />
      <div v-else-if="selectedContact && !isEditing">
<div class="d-flex align-items-center mb-3">
          <div class="rounded-circle d-flex align-items-center justify-content-center me-3" style="width:72px; height:72px; color:white; font-size:2rem; background-color: #9dafc7;">
            {{ getInitials(selectedContact) }}
          </div>
          <div>
            <div class="h4 mb-0">{{ selectedContact.first_name }} {{ selectedContact.last_name }}</div>
            <div class="text-muted">{{ selectedContact.client_type_display }}</div>
          </div>
        </div>
        <div class="mb-2" v-if="selectedContact.phone"><strong>Mobile:</strong> {{ selectedContact.phone }}</div>
        <div class="mb-2" v-if="selectedContact.email || selectedContact.email2 || selectedContact.email3">
          <span v-if="selectedContact.email"><strong>Email:</strong> {{ selectedContact.email }}</span>
          <span v-if="selectedContact.email2" class="ms-3"><strong>Email 2:</strong> {{ selectedContact.email2 }}</span>
          <span v-if="selectedContact.email3" class="ms-3"><strong>Email 3:</strong> {{ selectedContact.email3 }}</span>
        </div>
        <div class="mb-2" v-if="selectedContact.website">
          <strong>Website:</strong>
          <a :href="selectedContact.website" target="_blank">{{ selectedContact.website }}</a>
        </div>
        <div class="mb-2" v-if="selectedContact.address || selectedContact.city || selectedContact.state || selectedContact.zip">
          <span v-if="selectedContact.address"><strong>Address:</strong> {{ selectedContact.address }}</span>
          <span v-if="selectedContact.city" class="ms-3"><strong>City:</strong> {{ selectedContact.city }}</span>
          <span v-if="selectedContact.state" class="ms-3"><strong>State:</strong> {{ selectedContact.state }}</span>
          <span v-if="selectedContact.zip" class="ms-3"><strong>Zip:</strong> {{ selectedContact.zip }}</span>
        </div>
        <div class="mb-2" v-if="selectedContact.company"><strong>Company:</strong> {{ selectedContact.company }}</div>
        <div class="mb-2" v-if="selectedContact.phone || selectedContact.phone2 || selectedContact.phone3">
          <span v-if="selectedContact.phone"><strong>Phone:</strong> {{ selectedContact.phone }}</span>
          <span v-if="selectedContact.phone2" class="ms-3"><strong>Phone 2:</strong> {{ selectedContact.phone2 }}</span>
          <span v-if="selectedContact.phone3" class="ms-3"><strong>Phone 3:</strong> {{ selectedContact.phone3 }}</span>
        </div>
        <div class="mb-2" v-if="selectedContact.notes"><strong>Notes:</strong> {{ selectedContact.notes }}</div>
        <div class="mb-2" v-if="selectedContact.gender"><strong>Gender:</strong> {{ selectedContact.gender }}</div>
        <div class="mb-2" v-if="selectedContact.date_birth"><strong>Date of Birth:</strong> {{ selectedContact.date_birth }}</div>
        <div class="mb-2" v-if="selectedContact.ems_name"><strong>Emergency Name:</strong> {{ selectedContact.ems_name }}</div>
        <div class="mb-2" v-if="selectedContact.ems_phone"><strong>Emergency Phone:</strong> {{ selectedContact.ems_phone }}</div>
        <div class="mb-2" v-if="selectedContact.pp_number"><strong>Passport Number:</strong> {{ selectedContact.pp_number }}</div>
        <div class="mb-2" v-if="selectedContact.pp_date_issue"><strong>Passport Date Issue:</strong> {{ selectedContact.pp_date_issue }}</div>
        <div class="mb-2" v-if="selectedContact.pp_date_expire"><strong>Passport Date Expire:</strong> {{ selectedContact.pp_date_expire }}</div>
        <div class="mb-2" v-if="selectedContact.pp_place_issue"><strong>Passport Place Issue:</strong> {{ selectedContact.pp_place_issue }}</div>
        <div class="mb-2" v-if="selectedContact.pp_nationality"><strong>Passport Nationality:</strong> {{ selectedContact.pp_nationality }}</div>
        <div class="mb-2" v-if="selectedContact.pp_visa"><strong>Passport Visa:</strong> {{ selectedContact.pp_visa }}</div>
        <div class="mb-2" v-if="selectedContact.pp_visa_note"><strong>Passport Visa Note:</strong> {{ selectedContact.pp_visa_note }}</div>
        <div class="mb-2" v-if="selectedContact.pp_visa_received"><strong>Passport Visa Received:</strong> {{ selectedContact.pp_visa_received }}</div>
        <div class="mb-2" v-if="selectedContact.want_single_room"><strong>Want Single Room:</strong> {{ selectedContact.want_single_room }}</div>
        <div class="mb-2" v-if="selectedContact.want_roomate"><strong>Want Roommate:</strong> {{ selectedContact.want_roomate }}</div>
        <div class="mb-2" v-if="selectedContact.have_roomate"><strong>Have Roommate:</strong> {{ selectedContact.have_roomate }}</div>
        <div class="mb-2" v-if="selectedContact.have_roomate_name"><strong>Have Roommate Name:</strong> {{ selectedContact.have_roomate_name }}</div>
        <div class="mb-2" v-if="selectedContact.have_roomate_id"><strong>Have Roommate ID:</strong> {{ selectedContact.have_roomate_id }}</div>
        <div class="mb-2" v-if="selectedContact.registered_at_event"><strong>Registered at Event:</strong> {{ selectedContact.registered_at_event }}</div>
        <div class="mb-2" v-if="selectedContact.tags"><strong>Tags:</strong> {{ selectedContact.tags }}</div>
        <div class="mb-2" v-if="selectedContact.mail_lists"><strong>Mail Lists:</strong> {{ selectedContact.mail_lists }}</div>
        <div class="mb-2" v-if="selectedContact.name_tag"><strong>Name Tag:</strong> {{ selectedContact.name_tag }}</div>
        <div class="mb-2" v-if="selectedContact.from_web"><strong>From Web:</strong> {{ selectedContact.from_web }}</div>
        <div class="mb-2" v-if="selectedContact.hearabout"><strong>Hear About:</strong> {{ selectedContact.hearabout }}</div>
        <div class="mb-2" v-if="selectedContact.date_created">
          <strong>Date Created:</strong> {{ formatPST(selectedContact.date_created) }}
        </div>
        <div class="mb-2" v-if="selectedContact.date_updated">
          <strong>Last Updated:</strong> {{ formatPST(selectedContact.date_updated) }}
        </div>
        <button class="px-8 py-2 rounded shadow-sm text-white" @click="editContact(selectedContact)" style="background: gray; color: white;">Edit</button>
      </div>
      
      
      <form v-else-if="selectedContact && isEditing" @submit.prevent="saveContact" class="p-4 rounded shadow-sm" style="background: #e2e9e8; color: black;">
      <!-- ────────── Contact edit form fields ────────── -->
        <div class="row g-3 mb-3">
        <div class="col-md-4">
            <label class="form-label mb-1">First Name</label>
            <input v-model="editContactData.first_name" class="form-control shadow-sm" />
        </div>

        <div class="col-md-4">
            <label class="form-label mb-1">Middle Name</label>
            <input v-model="editContactData.middle_name" class="form-control shadow-sm" />
        </div>

        <div class="col-md-4">
            <label class="form-label mb-1">Last Name</label>
            <input v-model="editContactData.last_name" class="form-control shadow-sm" />
        </div>
        </div>
        <!-- 1 rigid row: Company · DOB · Website · Gender -->
        <div class="row row-cols-4 g-3 flex-nowrap mb-3">
        <div class="col">
            <label class="form-label mb-1">Company</label>
            <input v-model="editContactData.company" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Date&nbsp;of&nbsp;Birth</label>
            <input v-model="editContactData.date_birth" type="date" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Website</label>
            <input v-model="editContactData.website" type="url" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Gender</label>
            <input v-model="editContactData.gender" class="form-control shadow-sm">
        </div>
        </div>
        <!-- Address -->
        <div class="col mb-3">
        <label class="form-label mb-1">Address</label>
        <input v-model="editContactData.address" class="form-control shadow-sm" />
        </div>

        <!-- City / State / Zip on one line -->
        <div class="row g-3 mb-3">
        <div class="col-md-4">
            <label class="form-label mb-1">City</label>
            <input v-model="editContactData.city" class="form-control shadow-sm" />
        </div>

        <div class="col-md-4">
            <label class="form-label mb-1">State</label>
            <input v-model="editContactData.state" class="form-control shadow-sm" />
        </div>

        <div class="col-md-4">
            <label class="form-label mb-1">Zip</label>
            <input v-model="editContactData.zip" class="form-control shadow-sm" />
        </div>
        </div>
        <!-- Phone / Phone 2 / Phone 3 / Mobile on one line -->
        <div class="row g-3 mb-3">
        <div class="col-md-3">
            <label class="form-label mb-1">Phone</label>
            <input v-model="editContactData.phone"  type="tel" class="form-control shadow-sm" />
        </div>
        <div class="col-md-3">
            <label class="form-label mb-1">Phone 2</label>
            <input v-model="editContactData.phone2" type="tel" class="form-control shadow-sm" />
        </div>
        <div class="col-md-3">
            <label class="form-label mb-1">Phone 3</label>
            <input v-model="editContactData.phone3" type="tel" class="form-control shadow-sm" />
        </div>
        <div class="col-md-3">
            <label class="form-label mb-1">Mobile</label>
            <input v-model="editContactData.mobile" type="tel" class="form-control shadow-sm" />
        </div>
        </div>
        <!-- Email / Email 2 / Email 3 on one line -->
        <div class="row g-3 mb-3">
        <div class="col-md-4">
            <label class="form-label mb-1">Email</label>
            <input v-model="editContactData.email"  type="email" class="form-control shadow-sm">
        </div>

        <div class="col-md-4">
            <label class="form-label mb-1">Email 2</label>
            <input v-model="editContactData.email2" type="email" class="form-control shadow-sm">
        </div>

        <div class="col-md-4">
            <label class="form-label mb-1">Email 3</label>
            <input v-model="editContactData.email3" type="email" class="form-control shadow-sm">
        </div>
        </div>
        <!-- EMS Name · EMS Phone (one rigid row, 50 % / 50 %) -->
        <div class="row row-cols-2 g-3 flex-nowrap mb-3">
        <div class="col">
            <label class="form-label mb-1">EMS Name</label>
            <input v-model="editContactData.ems_name" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">EMS Phone</label>
            <input v-model="editContactData.ems_phone" type="tel" class="form-control shadow-sm">
        </div>
        </div>
        <!--──────────── Passport details : 4 inputs, one line on ≥ md ────────────-->
        <div class="row row-cols-1 row-cols-md-4 g-3 mb-3">
        <div class="col">
            <label class="form-label mb-1">Passport&nbsp;Number</label>
            <input v-model="editContactData.pp_number" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Issue&nbsp;Date</label>
            <input v-model="editContactData.pp_date_issue" type="date" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Expire&nbsp;Date</label>
            <input v-model="editContactData.pp_date_expire" type="date" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Place&nbsp;Issue</label>
            <input v-model="editContactData.pp_place_issue" class="form-control shadow-sm">
        </div>
        </div>
        <!--──────── Passport visa details : 4 inputs, one line on ≥ md ────────-->
        <div class="row row-cols-1 row-cols-md-4 g-3 mb-3">
        <div class="col">
            <label class="form-label mb-1">Passport&nbsp;Nationality</label>
            <input v-model="editContactData.pp_nationality" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Passport&nbsp;Visa</label>
            <input v-model="editContactData.pp_visa" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Visa&nbsp;Note</label>
            <input v-model="editContactData.pp_visa_note" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Visa&nbsp;Received</label>
            <input v-model="editContactData.pp_visa_received" class="form-control shadow-sm">
        </div>
        </div>
        <!--──── Room-preferences : 3 equal–width inputs, one line on ≥ md ────-->
        <div class="row row-cols-1 row-cols-md-3 g-3 mb-3">
        <div class="col">
            <label class="form-label mb-1">Want&nbsp;Single&nbsp;Room</label>
            <input v-model="editContactData.want_single_room" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Want&nbsp;Roommate</label>
            <input v-model="editContactData.want_roomate" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Have&nbsp;Roommate</label>
            <input v-model="editContactData.have_roomate" class="form-control shadow-sm">
        </div>
        </div>
        <!--──── Room-mate details : 2 equal fields, one line on ≥ md ────-->
        <div class="row row-cols-1 row-cols-md-2 g-3 mb-3">
        <div class="col">
            <label class="form-label mb-1">Roommate&nbsp;Name</label>
            <input v-model="editContactData.have_roomate_name" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Roommate&nbsp;ID</label>
            <input v-model="editContactData.have_roomate_id" type="number" class="form-control shadow-sm">
        </div>
        </div>
        <!--──── Registered / Tags / Mail-lists / Name-tag : 4-up on ≥ md ────-->
        <div class="row row-cols-1 row-cols-md-4 g-3 mb-3">
        <div class="col">
            <label class="form-label mb-1">Registered&nbsp;at&nbsp;Event</label>
            <input v-model="editContactData.registered_at_event" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Tags</label>
            <input v-model="editContactData.tags" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Mail&nbsp;Lists</label>
            <input v-model="editContactData.mail_lists" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Name&nbsp;Tag</label>
            <input v-model="editContactData.name_tag" class="form-control shadow-sm">
        </div>
        </div>
        <!--──── From-web / Hear-about / Unique-ID / Email-mail-list : 4-up ────-->
        <div class="row row-cols-1 row-cols-md-4 g-3 mb-3">
        <div class="col">
            <label class="form-label mb-1">From&nbsp;Web</label>
            <input v-model="editContactData.from_web" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Hear&nbsp;About</label>
            <input v-model="editContactData.hearabout" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Unique&nbsp;Ident</label>
            <input v-model="editContactData.unique_ident" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Email&nbsp;Mail-list</label>
            <input v-model="editContactData.email_maillist" class="form-control shadow-sm">
        </div>
        </div>
        <!--      Notes.      -->
        <div class="col-12 mb-3">
        <label class="form-label"><strong>Notes</strong></label>
        <textarea v-model="editContactData.notes" rows="3" class="form-control shadow-sm"></textarea>
        </div>
        <button type="submit" class="btn btn-primary me-2">Save</button>
        <button type="button" class="btn btn-secondary" @click="handleEditCancel">Cancel</button>
      </form>
      <div v-else class="text-muted d-flex align-items-center justify-content-center h-100">
        Select a contact to view details
      </div>
    </div>
  </div>
</template>