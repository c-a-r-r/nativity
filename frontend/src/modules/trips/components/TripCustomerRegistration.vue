<template>
  <div class="customer-registration-container">
    
    <!-- Action Buttons Section -->
    <div class="action-buttons-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-user-plus"></i>
          Customer Registration Management
        </h3>
        <div class="passenger-info">
          <span class="passenger-count">
            Maximum Passengers: <strong>{{ tripData?.maximum_passengers || 'N/A' }}</strong>
          </span>
        </div>
      </div>

      <!-- Action Buttons Row -->
      <div class="action-buttons-grid">
        <button @click="openPassengerUrl" class="action-btn passenger-url">
          <i class="fas fa-external-link-alt"></i>
          Open Passenger URL
        </button>
        <button @click="processPayments" class="action-btn payments">
          <i class="fas fa-credit-card"></i>
          Payments
        </button>
        <button @click="managePassengerList" class="action-btn passenger-list">
          <i class="fas fa-list"></i>
          Passenger List
        </button>
        <button @click="generatePdf" class="action-btn pdf">
          <i class="fas fa-file-pdf"></i>
          PDF
        </button>
        <button @click="emailPtfAndEstimates" class="action-btn email-ptf">
          <i class="fas fa-envelope"></i>
          Email PTF and Estimates
        </button>
        <button @click="sendEmail" class="action-btn send-email">
          <i class="fas fa-paper-plane"></i>
          Send Email
        </button>
      </div>
    </div>

    <!-- Email Campaign Section -->
    <div class="email-campaign-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-envelope-open-text"></i>
          Email Campaign Management
        </h3>
        <div class="campaign-info">
          <span class="campaign-status">
            Active Campaigns: <strong>{{ activeCampaigns }}</strong>
          </span>
        </div>
      </div>

      <!-- Email Campaign Table -->
      <div class="campaign-table">
        <table class="table">
          <thead>
            <tr>
              <th>#</th>
              <th>Email</th>
              <th>Sent</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="email in emailCampaigns" :key="email.id" class="campaign-row">
              <td class="campaign-number">{{ email.id }}</td>
              <td class="email-title">{{ email.title }}</td>
              <td class="sent-status">
                <span v-if="email.sent" class="status-sent">
                  <i class="fas fa-check-circle"></i>
                  {{ formatDate(email.sent_date) }}
                </span>
                <span v-else class="status-pending">
                  <i class="fas fa-clock"></i>
                  No
                </span>
              </td>
              <td class="action-cell">
                <button 
                  v-if="!email.sent" 
                  @click="sendCampaignEmail(email)" 
                  class="btn-send-now"
                  :disabled="sendingEmail === email.id"
                >
                  <i class="fas fa-paper-plane"></i>
                  {{ sendingEmail === email.id ? 'Sending...' : 'Send Now' }}
                </button>
                <span v-else class="sent-indicator">
                  <i class="fas fa-check"></i>
                  Sent
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Weekly Email Section -->
      <div class="weekly-email-section">
        <h4>Weekly Emails</h4>
        <div class="weekly-email-item">
          <div class="weekly-email-info">
            <span class="email-number">7</span>
            <span class="email-title">Rooming List and Balance Sheet</span>
            <div class="recipient-list">
              <div class="recipient-item">
                <label>Recipient 1:</label>
                <input 
                  type="email" 
                  v-model="weeklyEmail.recipient1" 
                  class="form-control"
                  placeholder="recipient@example.com"
                >
              </div>
              <div class="recipient-item">
                <label>Recipient 2:</label>
                <input 
                  type="email" 
                  v-model="weeklyEmail.recipient2" 
                  class="form-control"
                  placeholder="recipient@example.com"
                >
              </div>
              <div class="recipient-item">
                <label>Recipient 3:</label>
                <input 
                  type="email" 
                  v-model="weeklyEmail.recipient3" 
                  class="form-control"
                  placeholder="recipient@example.com"
                >
              </div>
            </div>
          </div>
          <div class="weekly-email-controls">
            <label class="checkbox-container">
              <input 
                type="checkbox" 
                v-model="weeklyEmail.active"
                @change="updateWeeklyEmailStatus"
              >
              <span class="checkmark"></span>
              Send weekly
            </label>
            <span class="last-sent">
              <i class="fas fa-calendar"></i>
              {{ weeklyEmail.lastSent || 'Never sent' }}
            </span>
            <button @click="sendWeeklyEmail" class="btn-send-weekly">
              <i class="fas fa-paper-plane"></i>
              Send Now
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-bolt"></i>
          Quick Actions
        </h3>
      </div>

      <div class="quick-actions-grid">
        <div class="quick-action-item">
          <button @click="downloadExcel" class="btn btn-info btn-block">
            <i class="fas fa-download"></i>
            Download Excel
          </button>
        </div>
        <div class="quick-action-item">
          <button @click="emailTemplates" class="btn btn-primary btn-block">
            <i class="fas fa-envelope-open"></i>
            Email Templates
          </button>
        </div>
        <div class="quick-action-item">
          <button @click="financialReport" class="btn btn-success btn-block">
            <i class="fas fa-chart-line"></i>
            Financial Report
          </button>
        </div>
        <div class="quick-action-item">
          <button @click="saveProgress" class="btn btn-warning btn-block">
            <i class="fas fa-save"></i>
            Save Progress
          </button>
        </div>
      </div>
    </div>

    <!-- Email Template Modal -->
    <div v-if="showEmailModal" class="modal-overlay" @click="closeEmailModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4>Send Email Campaign</h4>
          <button @click="closeEmailModal" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Subject</label>
            <input 
              type="text" 
              v-model="emailModal.subject" 
              class="form-control"
              placeholder="Email subject"
            >
          </div>
          <div class="form-group">
            <label>Recipients</label>
            <select v-model="emailModal.recipients" class="form-control" multiple>
              <option value="all">All Passengers</option>
              <option value="paid">Paid Passengers Only</option>
              <option value="pending">Pending Passengers Only</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="confirmSendEmail" class="btn btn-primary">Send Email</button>
          <button @click="closeEmailModal" class="btn btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import axios from 'axios'

// Props
const props = defineProps({
  tripId: {
    type: [String, Number],
    required: true
  },
  tripData: {
    type: Object,
    default: () => ({})
  },
  passengerStats: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['update-stats', 'send-email'])

// State
const sendingEmail = ref(null)
const showEmailModal = ref(false)
const loading = ref(false)

// Email campaigns data (based on screenshot)
const emailCampaigns = ref([
  {
    id: 1,
    title: 'Great Email to Traveler',
    sent: true,
    sent_date: '2023-12-01T10:00:00Z'
  },
  {
    id: 2,
    title: 'Passports and Information',
    sent: false,
    sent_date: null
  },
  {
    id: 3,
    title: 'Trip Preparation Guide and Tips',
    sent: false,
    sent_date: null
  },
  {
    id: 4,
    title: 'Final Payment Reminder',
    sent: false,
    sent_date: null
  },
  {
    id: 5,
    title: 'What to Pack and Airport Information',
    sent: false,
    sent_date: null
  },
  {
    id: 6,
    title: 'Final Trip Information',
    sent: false,
    sent_date: null
  },
  {
    id: 7,
    title: 'Welcome Back',
    sent: false,
    sent_date: null
  }
])

const weeklyEmail = reactive({
  recipient1: 'firstbaptistspeccare@yahoo.com',
  recipient2: 'test@nativitypilgrimage.com',
  recipient3: 'test@nativitypilgrimage.com',
  active: true,
  lastSent: '03/28/2023'
})

const emailModal = reactive({
  subject: '',
  recipients: ['all']
})

// Computed
const activeCampaigns = computed(() => {
  return emailCampaigns.value.filter(email => !email.sent).length
})

// Methods
const openPassengerUrl = () => {
  const url = `${window.location.origin}/trip-registration/${props.tripId}`
  window.open(url, '_blank')
}

const processPayments = () => {
  // TODO: Navigate to payments management
  console.log('Opening payments management')
}

const managePassengerList = () => {
  // TODO: Navigate to passenger list management
  console.log('Opening passenger list management')
}

const generatePdf = () => {
  // TODO: Generate PDF report
  console.log('Generating PDF report')
}

const emailPtfAndEstimates = () => {
  // TODO: Send PTF and estimates email
  console.log('Sending PTF and estimates')
}

const sendEmail = () => {
  showEmailModal.value = true
}

const closeEmailModal = () => {
  showEmailModal.value = false
  emailModal.subject = ''
  emailModal.recipients = ['all']
}

const confirmSendEmail = () => {
  // TODO: Send email
  console.log('Sending email with:', emailModal)
  closeEmailModal()
}

const sendCampaignEmail = async (email) => {
  try {
    sendingEmail.value = email.id
    
    // TODO: Replace with actual API call
    await axios.post(`/api/trips/${props.tripId}/send-campaign-email/`, {
      campaign_id: email.id,
      email_type: email.title
    })
    
    // Update email status
    email.sent = true
    email.sent_date = new Date().toISOString()
    
    emit('send-email', {
      type: 'campaign',
      campaign_id: email.id,
      title: email.title
    })
    
  } catch (error) {
    console.error('Error sending campaign email:', error)
  } finally {
    sendingEmail.value = null
  }
}

const updateWeeklyEmailStatus = async () => {
  try {
    // TODO: Replace with actual API call
    await axios.patch(`/api/trips/${props.tripId}/weekly-email/`, {
      active: weeklyEmail.active,
      recipients: [
        weeklyEmail.recipient1,
        weeklyEmail.recipient2,
        weeklyEmail.recipient3
      ].filter(Boolean)
    })
    
  } catch (error) {
    console.error('Error updating weekly email status:', error)
  }
}

const sendWeeklyEmail = async () => {
  try {
    loading.value = true
    
    // TODO: Replace with actual API call
    await axios.post(`/api/trips/${props.tripId}/send-weekly-email/`, {
      recipients: [
        weeklyEmail.recipient1,
        weeklyEmail.recipient2,
        weeklyEmail.recipient3
      ].filter(Boolean)
    })
    
    weeklyEmail.lastSent = new Date().toLocaleDateString()
    
  } catch (error) {
    console.error('Error sending weekly email:', error)
  } finally {
    loading.value = false
  }
}

const downloadExcel = () => {
  // TODO: Generate and download Excel report
  console.log('Downloading Excel report')
}

const emailTemplates = () => {
  // TODO: Open email templates management
  console.log('Opening email templates')
}

const financialReport = () => {
  // TODO: Generate financial report
  console.log('Generating financial report')
}

const saveProgress = () => {
  // TODO: Save current progress
  console.log('Saving progress')
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString()
}
</script>

<style scoped>
.customer-registration-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.action-buttons-section,
.email-campaign-section,
.quick-actions-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.section-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 18px;
  font-weight: 600;
}

.section-header h3 i {
  margin-right: 8px;
  color: #3b82f6;
}

.passenger-info,
.campaign-info {
  font-size: 14px;
  color: #6b7280;
}

.action-buttons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.action-btn {
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  color: #374151;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.action-btn:hover {
  border-color: #3b82f6;
  background: #f8fafc;
  color: #3b82f6;
}

.action-btn.passenger-url {
  background: #dbeafe;
  border-color: #3b82f6;
  color: #1e40af;
}

.action-btn.payments {
  background: #dcfce7;
  border-color: #10b981;
  color: #065f46;
}

.action-btn.passenger-list {
  background: #fef3c7;
  border-color: #f59e0b;
  color: #92400e;
}

.action-btn.pdf {
  background: #fecaca;
  border-color: #ef4444;
  color: #991b1b;
}

.action-btn.email-ptf {
  background: #e0e7ff;
  border-color: #6366f1;
  color: #4338ca;
}

.action-btn.send-email {
  background: #f3e8ff;
  border-color: #8b5cf6;
  color: #6b21a8;
}

.campaign-table {
  margin-bottom: 24px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}

.table th {
  background: #f9fafb;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

.table td {
  padding: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.campaign-row:hover {
  background: #f9fafb;
}

.campaign-number {
  font-weight: 600;
  color: #374151;
  width: 60px;
}

.email-title {
  color: #1f2937;
  font-weight: 500;
}

.status-sent {
  color: #10b981;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.status-pending {
  color: #f59e0b;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.btn-send-now {
  padding: 6px 12px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: background-color 0.2s;
}

.btn-send-now:hover:not(:disabled) {
  background: #2563eb;
}

.btn-send-now:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.sent-indicator {
  color: #10b981;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.weekly-email-section {
  border-top: 1px solid #e5e7eb;
  padding-top: 20px;
}

.weekly-email-section h4 {
  margin: 0 0 16px 0;
  color: #374151;
  font-size: 16px;
  font-weight: 600;
}

.weekly-email-item {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 20px;
  align-items: start;
}

.weekly-email-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.email-number {
  display: inline-block;
  width: 24px;
  height: 24px;
  background: #3b82f6;
  color: white;
  border-radius: 50%;
  text-align: center;
  line-height: 24px;
  font-size: 12px;
  font-weight: 600;
  margin-right: 8px;
}

.recipient-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}

.recipient-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.recipient-item label {
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
}

.form-control {
  padding: 6px 8px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 12px;
}

.weekly-email-controls {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
}

.last-sent {
  font-size: 12px;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 4px;
}

.btn-send-weekly {
  padding: 6px 12px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn-block {
  width: 100%;
}

.btn-info {
  background: #06b6d4;
  color: white;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-success {
  background: #10b981;
  color: white;
}

.btn-warning {
  background: #f59e0b;
  color: white;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h4 {
  margin: 0;
  color: #1f2937;
}

.modal-close {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #6b7280;
}

.modal-body {
  padding: 24px;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #374151;
}

.form-group .form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 768px) {
  .action-buttons-grid {
    grid-template-columns: 1fr;
  }

  .weekly-email-item {
    grid-template-columns: 1fr;
  }

  .weekly-email-controls {
    align-items: flex-start;
  }

  .recipient-list {
    grid-template-columns: 1fr;
  }
}
</style>
