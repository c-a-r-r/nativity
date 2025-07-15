<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['created', 'cancel'])



const newContact = ref({
    first_name: '',
    middle_name: '',
    last_name: '',
    company: '',
    date_birth: '',
    website: '',
    gender: '',
    address: '',
    city: '',
    state: '',
    zip: '',
    phone: '',
    phone2: '',
    phone3: '',
    mobile: '',
    email: '',
    email2: '',
    email3: '',
    ems_name: '',
    ems_phone: '',
    pp_number: '',
    pp_date_issue: '',
    pp_date_expire: '',
    pp_place_issue: '',
    pp_nationality: '',
    pp_visa: 'N',
    pp_visa_note: '',
    pp_visa_received: 'N',
    want_single_room: '',
    want_roomate: '',
    have_roomate: '',
    have_roomate_name: '',
    have_roomate_id: '',
    registered_at_event: '',
    tags: '',
    mail_lists: '',
    name_tag: '',
    from_web: 'N',
    hearabout: '',
    unique_ident: '',
    email_maillist: '',
    notes: ''
})



function stripBlanks(obj) {
  const cleaned = {}
  for (const [k, v] of Object.entries(obj)) {
    cleaned[k] = v === null ? '' : v
  }
  return cleaned
}

async function createContact () {
  try {
    let payload = stripBlanks({ ...newContact.value })
    const { data } = await axios.post('/api/contacts/', payload)
    emit('created', data)      // tell parent a contact was added
  } catch (err) {
    alert('Failed to create contact')
  }
}
</script>

<template>
  <form @submit.prevent="createContact" class="p-4 rounded shadow-sm" style="background: #e2e9e8; color: black;">
<!-- ────────── Contact edit form fields ────────── -->
        <div class="row g-3 mb-3">
        <div class="col-md-4">
            <label class="form-label mb-1">First Name</label>
            <input v-model="newContact.first_name" class="form-control shadow-sm" />
        </div>

        <div class="col-md-4">
            <label class="form-label mb-1">Middle Name</label>
            <input v-model="newContact.middle_name" class="form-control shadow-sm" />
        </div>

        <div class="col-md-4">
            <label class="form-label mb-1">Last Name</label>
            <input v-model="newContact.last_name" class="form-control shadow-sm" />
        </div>
        </div>
        <!-- 1 rigid row: Company · DOB · Website · Gender -->
        <div class="row row-cols-4 g-3 flex-nowrap mb-3">
        <div class="col">
            <label class="form-label mb-1">Company</label>
            <input v-model="newContact.company" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Date&nbsp;of&nbsp;Birth</label>
            <input v-model="newContact.date_birth" type="date" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Website</label>
            <input v-model="newContact.website" type="url" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Gender</label>
            <input v-model="newContact.gender" class="form-control shadow-sm">
        </div>
        </div>
        <!-- Address -->
        <div class="col mb-3">
        <label class="form-label mb-1">Address</label>
        <input v-model="newContact.address" class="form-control shadow-sm" />
        </div>

        <!-- City / State / Zip on one line -->
        <div class="row g-3 mb-3">
        <div class="col-md-4">
            <label class="form-label mb-1">City</label>
            <input v-model="newContact.city" class="form-control shadow-sm" />
        </div>

        <div class="col-md-4">
            <label class="form-label mb-1">State</label>
            <input v-model="newContact.state" class="form-control shadow-sm" />
        </div>

        <div class="col-md-4">
            <label class="form-label mb-1">Zip</label>
            <input v-model="newContact.zip" class="form-control shadow-sm" />
        </div>
        </div>
        <!-- Phone / Phone 2 / Phone 3 / Mobile on one line -->
        <div class="row g-3 mb-3">
        <div class="col-md-3">
            <label class="form-label mb-1">Phone</label>
            <input v-model="newContact.phone"  type="tel" class="form-control shadow-sm" />
        </div>
        <div class="col-md-3">
            <label class="form-label mb-1">Phone 2</label>
            <input v-model="newContact.phone2" type="tel" class="form-control shadow-sm" />
        </div>
        <div class="col-md-3">
            <label class="form-label mb-1">Phone 3</label>
            <input v-model="newContact.phone3" type="tel" class="form-control shadow-sm" />
        </div>
        <div class="col-md-3">
            <label class="form-label mb-1">Mobile</label>
            <input v-model="newContact.mobile" type="tel" class="form-control shadow-sm" />
        </div>
        </div>
        <!-- Email / Email 2 / Email 3 on one line -->
        <div class="row g-3 mb-3">
        <div class="col-md-4">
            <label class="form-label mb-1">Email</label>
            <input v-model="newContact.email"  type="email" class="form-control shadow-sm">
        </div>

        <div class="col-md-4">
            <label class="form-label mb-1">Email 2</label>
            <input v-model="newContact.email2" type="email" class="form-control shadow-sm">
        </div>

        <div class="col-md-4">
            <label class="form-label mb-1">Email 3</label>
            <input v-model="newContact.email3" type="email" class="form-control shadow-sm">
        </div>
        </div>
        <!-- EMS Name · EMS Phone (one rigid row, 50 % / 50 %) -->
        <div class="row row-cols-2 g-3 flex-nowrap mb-3">
        <div class="col">
            <label class="form-label mb-1">EMS Name</label>
            <input v-model="newContact.ems_name" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">EMS Phone</label>
            <input v-model="newContact.ems_phone" type="tel" class="form-control shadow-sm">
        </div>
        </div>
        <!--──────────── Passport details : 4 inputs, one line on ≥ md ────────────-->
        <div class="row row-cols-1 row-cols-md-4 g-3 mb-3">
        <div class="col">
            <label class="form-label mb-1">Passport&nbsp;Number</label>
            <input v-model="newContact.pp_number" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Issue&nbsp;Date</label>
            <input v-model="newContact.pp_date_issue" type="date" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Expire&nbsp;Date</label>
            <input v-model="newContact.pp_date_expire" type="date" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Place&nbsp;Issue</label>
            <input v-model="newContact.pp_place_issue" class="form-control shadow-sm">
        </div>
        </div>
        <!--──────── Passport visa details : 4 inputs, one line on ≥ md ────────-->
        <div class="row row-cols-1 row-cols-md-4 g-3 mb-3">
        <!-- Passport visa? -->
        <div class="col">
        <label class="form-label mb-1">Passport Visa</label>
        <select v-model="newContact.pp_visa" class="form-select shadow-sm">
            <option value="N">No</option>
            <option value="Y">Yes</option>
        </select>
        </div>

        <div class="col">
            <label class="form-label mb-1">Passport&nbsp;Visa</label>
            <input v-model="newContact.pp_visa" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Visa&nbsp;Note</label>
            <input v-model="newContact.pp_visa_note" class="form-control shadow-sm">
        </div>

        <!-- Visa received? -->
        <div class="col">
        <label class="form-label mb-1">Visa Received</label>
        <select v-model="newContact.pp_visa_received" class="form-select shadow-sm">
            <option value="N">No</option>
            <option value="Y">Yes</option>
        </select>
        </div>
        </div>
        <!--──── Room-preferences : 3 equal–width inputs, one line on ≥ md ────-->
        <div class="row row-cols-1 row-cols-md-3 g-3 mb-3">
        <div class="col">
            <label class="form-label mb-1">Want&nbsp;Single&nbsp;Room</label>
            <input v-model="newContact.want_single_room" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Want&nbsp;Roommate</label>
            <input v-model="newContact.want_roomate" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Have&nbsp;Roommate</label>
            <input v-model="newContact.have_roomate" class="form-control shadow-sm">
        </div>
        </div>
        <!--──── Room-mate details : 2 equal fields, one line on ≥ md ────-->
        <div class="row row-cols-1 row-cols-md-2 g-3 mb-3">
        <div class="col">
            <label class="form-label mb-1">Roommate&nbsp;Name</label>
            <input v-model="newContact.have_roomate_name" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Roommate&nbsp;ID</label>
            <input v-model="newContact.have_roomate_id" type="number" class="form-control shadow-sm">
        </div>
        </div>
        <!--──── Registered / Tags / Mail-lists / Name-tag : 4-up on ≥ md ────-->
        <div class="row row-cols-1 row-cols-md-4 g-3 mb-3">
        <div class="col">
            <label class="form-label mb-1">Registered&nbsp;at&nbsp;Event</label>
            <input v-model="newContact.registered_at_event" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Tags</label>
            <input v-model="newContact.tags" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Mail&nbsp;Lists</label>
            <input v-model="newContact.mail_lists" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Name&nbsp;Tag</label>
            <input v-model="newContact.name_tag" class="form-control shadow-sm">
        </div>
        </div>
        <!--──── From-web / Hear-about / Unique-ID / Email-mail-list : 4-up ────-->
        <div class="row row-cols-1 row-cols-md-4 g-3 mb-3">
        <!-- Came from web? -->
        <div class="col">
        <label class="form-label mb-1">From Web</label>
        <select v-model="newContact.from_web" class="form-select shadow-sm">
            <option value="N">No</option>
            <option value="Y">Yes</option>
        </select>
        </div>

        <div class="col">
            <label class="form-label mb-1">Hear&nbsp;About</label>
            <input v-model="newContact.hearabout" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Unique&nbsp;Ident</label>
            <input v-model="newContact.unique_ident" class="form-control shadow-sm">
        </div>

        <div class="col">
            <label class="form-label mb-1">Email&nbsp;Mail-list</label>
            <input v-model="newContact.email_maillist" class="form-control shadow-sm">
        </div>
        </div>
        <!--      Notes.      -->
        <div class="col-12 mb-3">
        <label class="form-label"><strong>Notes</strong></label>
        <textarea v-model="newContact.notes" rows="3" class="form-control shadow-sm"></textarea>
        </div>
    <button type="submit" class="btn btn-success me-2">Create</button>
    <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Cancel</button>
  </form>
</template>