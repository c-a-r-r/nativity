<!-- filepath: /Users/cristian/Documents/nativity-crm/frontend/src/modules/marketing/components/RegistrationModal.vue -->
<template>
  <div class="modal fade show d-block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Register for {{ trip.final_title }}</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitRegistration">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">First Name *</label>
                <input v-model="form.first_name" type="text" class="form-control" required>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Last Name *</label>
                <input v-model="form.last_name" type="text" class="form-control" required>
              </div>
            </div>
            
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Email *</label>
                <input v-model="form.email" type="email" class="form-control" required>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Phone</label>
                <input v-model="form.phone" type="tel" class="form-control">
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Date of Birth</label>
                <input v-model="form.date_of_birth" type="date" class="form-control">
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Passport Number</label>
                <input v-model="form.passport_number" type="text" class="form-control">
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Emergency Contact Name</label>
                <input v-model="form.emergency_contact_name" type="text" class="form-control">
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Emergency Contact Phone</label>
                <input v-model="form.emergency_contact_phone" type="tel" class="form-control">
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label">Dietary Restrictions</label>
              <textarea v-model="form.dietary_restrictions" class="form-control" rows="2"></textarea>
            </div>

            <div class="mb-3">
              <label class="form-label">Medical Conditions</label>
              <textarea v-model="form.medical_conditions" class="form-control" rows="2"></textarea>
            </div>

            <div class="mb-3">
              <label class="form-label">Special Requests</label>
              <textarea v-model="form.special_requests" class="form-control" rows="2"></textarea>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="submitRegistration"
            :disabled="submitting"
          >
            {{ submitting ? 'Submitting...' : 'Submit Registration' }}
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show"></div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '../api/marketing.api.js'

const props = defineProps(['trip'])
const emit = defineEmits(['close', 'registered'])

const submitting = ref(false)
const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  date_of_birth: '',
  passport_number: '',
  emergency_contact_name: '',
  emergency_contact_phone: '',
  dietary_restrictions: '',
  medical_conditions: '',
  special_requests: ''
})

const submitRegistration = async () => {
  try {
    submitting.value = true
    
    const payload = {
      ...form.value,
      trip: props.trip.id
    }
    
    const response = await api.post('/marketing/registrations/', payload)
    emit('registered', response.data)
    
  } catch (error) {
    console.error('Registration failed:', error)
    alert('Registration failed. Please try again.')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.modal {
  z-index: 1050;
}
.modal-backdrop {
  z-index: 1040;
}
</style>