<template>
  <div class="trip-proposal">
    
    <!-- Section Header -->
    <div class="section-header">
      <h3>
        <i class="fas fa-file-contract"></i>
        Proposal & Confirmation
      </h3>
      <div class="header-actions">
        <button @click="editTrip" class="btn btn-edit">
          <i class="fas fa-edit"></i>
          Edit Trip Details
        </button>
      </div>
    </div>

    <!-- Trip Details Grid -->
    <div class="trip-details-grid">
      
      <!-- Basic Information -->
      <div class="detail-section">
        <h4>Basic Information</h4>
        <div class="detail-grid">
          <div class="detail-item">
            <label>Group Name:</label>
            <span>{{ tripData?.group_name || 'N/A' }}</span>
          </div>
          <div class="detail-item">
            <label>Church Name:</label>
            <span>{{ tripData?.church_name || 'N/A' }}</span>
          </div>
          <div class="detail-item">
            <label>Leader Name:</label>
            <span>{{ tripData?.leader_name || 'N/A' }}</span>
          </div>
          <div class="detail-item">
            <label>Contact:</label>
            <span>{{ tripData?.client_name }}</span>
          </div>
          <div class="detail-item">
            <label>Destination:</label>
            <span>{{ tripData?.trip_name }}</span>
          </div>
          <div class="detail-item">
            <label>Departure Date:</label>
            <span>{{ formatDate(tripData?.departure_date) }}</span>
          </div>
        </div>
      </div>

      <!-- Financial Information -->
      <div class="detail-section">
        <h4>Financial Details</h4>
        <div class="detail-grid">
          <div class="detail-item">
            <label>Total Cost:</label>
            <span class="amount">${{ formatCurrency(tripData?.total_cost) }}</span>
          </div>
          <div class="detail-item">
            <label>Commission User:</label>
            <span class="amount">{{ tripData?.commission_user || 0 }}%</span>
          </div>
          <div class="detail-item">
            <label>Commission Leader:</label>
            <span class="amount">{{ tripData?.commission_leader || 0 }}%</span>
          </div>
          <div class="detail-item">
            <label>Status:</label>
            <span class="status-badge" :class="getStatusClass(tripData?.workflow_status_nombre)">
              {{ tripData?.workflow_status_nombre }}
            </span>
          </div>
        </div>
      </div>

    </div>

    <!-- Email Management Section -->
    <div class="email-section">
      <div class="section-header">
        <h4>
          <i class="fas fa-envelope"></i>
          Email Campaign Management
        </h4>
        <button @click="editEmailTemplates" class="btn btn-secondary">
          <i class="fas fa-edit"></i>
          Edit Templates
        </button>
      </div>

      <div class="email-grid">
        <div 
          v-for="email in emailTemplates" 
          :key="email.id"
          class="email-card"
          :class="{ sent: isEmailSent(email.id) }"
        >
          <div class="email-header">
            <h5>{{ email.title }}</h5>
            <span class="email-status" :class="{ sent: isEmailSent(email.id) }">
              {{ isEmailSent(email.id) ? 'Sent' : 'Pending' }}
            </span>
          </div>
          <p class="email-description">{{ email.description }}</p>
          <div class="email-actions">
            <button 
              @click="previewEmail(email.id)" 
              class="btn btn-sm btn-outline-info"
            >
              <i class="fas fa-eye"></i>
              Preview
            </button>
            <button 
              @click="sendEmail(email.id)" 
              class="btn btn-sm btn-primary"
              :disabled="isEmailSent(email.id)"
            >
              <i class="fas fa-paper-plane"></i>
              {{ isEmailSent(email.id) ? 'Sent' : 'Send' }}
            </button>
          </div>
          <div v-if="isEmailSent(email.id)" class="sent-info">
            <small>
              <i class="fas fa-check"></i>
              Sent: {{ formatDate(getSentDate(email.id)) }}
            </small>
          </div>
        </div>
      </div>
    </div>

    <!-- Comments Section -->
    <div class="comments-section">
      <div class="section-header">
        <h4>
          <i class="fas fa-comments"></i>
          Stage Comments
        </h4>
        <button @click="showAddComment = !showAddComment" class="btn btn-success">
          <i class="fas fa-plus"></i>
          Add Comment
        </button>
      </div>

      <!-- Add Comment Form -->
      <div v-if="showAddComment" class="add-comment-form">
        <textarea 
          v-model="newComment"
          placeholder="Add your comment here..."
          class="comment-textarea"
          rows="3"
        ></textarea>
        <div class="comment-actions">
          <button @click="submitComment" class="btn btn-primary">
            <i class="fas fa-save"></i>
            Save Comment
          </button>
          <button @click="cancelComment" class="btn btn-secondary">
            Cancel
          </button>
        </div>
      </div>

      <!-- Comments List -->
      <div class="comments-list">
        <div 
          v-for="comment in comments" 
          :key="comment.id"
          class="comment-item"
        >
          <div class="comment-header">
            <span class="comment-author">{{ comment.user_name }}</span>
            <span class="comment-date">{{ formatDate(comment.date_created) }}</span>
          </div>
          <div class="comment-content">{{ comment.notes }}</div>
          <div v-if="comment.is_edit" class="comment-edit-info">
            <small>
              <i class="fas fa-edit"></i>
              Edited: {{ formatDate(comment.edit_created) }}
            </small>
          </div>
        </div>
        
        <div v-if="comments.length === 0" class="no-comments">
          <i class="fas fa-comment-slash"></i>
          <p>No comments yet. Add the first comment to start tracking this stage.</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Props
const props = defineProps({
  tripData: {
    type: Object,
    default: () => ({})
  },
  comments: {
    type: Array,
    default: () => []
  }
})

// Emits
const emit = defineEmits(['update-trip', 'add-comment', 'send-email'])

// State
const showAddComment = ref(false)
const newComment = ref('')

// Email templates configuration (based on pilgrimage.php)
const emailTemplates = ref([
  {
    id: 1,
    title: 'Welcome Email',
    description: 'Initial welcome message to group leader'
  },
  {
    id: 2,
    title: 'Confirmation Email', 
    description: 'Trip confirmation and details'
  },
  {
    id: 3,
    title: 'Payment Reminder',
    description: 'Balance due notice and payment instructions'
  },
  {
    id: 4,
    title: 'Final Details',
    description: 'Pre-trip information and final instructions'
  },
  {
    id: 5,
    title: 'Travel Documents',
    description: 'Important travel documents and requirements'
  },
  {
    id: 6,
    title: 'Post-Trip Thank You',
    description: 'Thank you message and feedback request'
  }
])

// Methods
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatCurrency = (amount) => {
  return parseFloat(amount || 0).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const getStatusClass = (status) => {
  if (!status) return ''
  const statusLower = status.toLowerCase()
  if (statusLower.includes('accepted')) return 'status-accepted'
  if (statusLower.includes('completed')) return 'status-completed'
  if (statusLower.includes('draft')) return 'status-draft'
  return 'status-default'
}

const isEmailSent = (emailId) => {
  return props.tripData?.[`mail_sent${emailId}`] !== null
}

const getSentDate = (emailId) => {
  return props.tripData?.[`mail_sent${emailId}`]
}

const editTrip = () => {
  // Navigate to trip edit form or open modal
  console.log('Edit trip details')
}

const editEmailTemplates = () => {
  // Open email template editor
  console.log('Edit email templates')
}

const previewEmail = (emailId) => {
  // Open email preview
  console.log('Preview email:', emailId)
}

const sendEmail = (emailId) => {
  emit('send-email', emailId)
}

const submitComment = () => {
  if (newComment.value.trim()) {
    emit('add-comment', 1, newComment.value.trim()) // Stage 1 = Proposal
    newComment.value = ''
    showAddComment.value = false
  }
}

const cancelComment = () => {
  newComment.value = ''
  showAddComment.value = false
}
</script>

<style scoped>
.trip-proposal {
  padding: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f8f9fa;
}

.section-header h3,
.section-header h4 {
  margin: 0;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-header i {
  color: #667eea;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.trip-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.detail-section {
  background: #f8f9fa;
  padding: 24px;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.detail-section h4 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 18px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-item label {
  font-weight: 600;
  color: #7f8c8d;
  font-size: 14px;
}

.detail-item span {
  color: #2c3e50;
  font-size: 16px;
}

.detail-item span.amount {
  font-weight: 600;
  color: #28a745;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  display: inline-block;
  width: fit-content;
}

.status-accepted {
  background: #d4edda;
  color: #155724;
}

.status-completed {
  background: #cce5ff;
  color: #004085;
}

.status-draft {
  background: #fff3cd;
  color: #856404;
}

.status-default {
  background: #f8f9fa;
  color: #6c757d;
}

.email-section {
  margin-bottom: 40px;
}

.email-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.email-card {
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
}

.email-card:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
}

.email-card.sent {
  border-color: #28a745;
  background: linear-gradient(135deg, #f8fff9 0%, #e8f5e8 100%);
}

.email-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.email-header h5 {
  margin: 0;
  color: #2c3e50;
  font-size: 16px;
}

.email-status {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  background: #ffc107;
  color: #856404;
}

.email-status.sent {
  background: #28a745;
  color: white;
}

.email-description {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 16px;
  line-height: 1.5;
}

.email-actions {
  display: flex;
  gap: 8px;
}

.sent-info {
  margin-top: 12px;
  color: #28a745;
  font-weight: 500;
}

.sent-info i {
  margin-right: 6px;
}

.comments-section {
  background: #f8f9fa;
  padding: 24px;
  border-radius: 12px;
}

.add-comment-form {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 24px;
  border: 2px solid #e9ecef;
}

.comment-textarea {
  width: 100%;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 12px;
  font-size: 14px;
  resize: vertical;
  margin-bottom: 12px;
}

.comment-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.comment-actions {
  display: flex;
  gap: 12px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  background: white;
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  color: #2c3e50;
}

.comment-date {
  color: #7f8c8d;
  font-size: 14px;
}

.comment-content {
  color: #2c3e50;
  line-height: 1.6;
  margin-bottom: 8px;
}

.comment-edit-info {
  color: #7f8c8d;
  font-style: italic;
}

.no-comments {
  text-align: center;
  padding: 40px 20px;
  color: #7f8c8d;
}

.no-comments i {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.no-comments p {
  margin: 0;
  font-style: italic;
}

/* Button Styles */
.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
}

.btn-edit {
  background: #ffc107;
  color: #212529;
}

.btn-edit:hover {
  background: #e0a800;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #218838;
  transform: translateY(-1px);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-outline-info {
  border: 2px solid #17a2b8;
  color: #17a2b8;
  background: transparent;
}

.btn-outline-info:hover {
  background: #17a2b8;
  color: white;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Responsive Design */
@media (max-width: 768px) {
  .trip-proposal {
    padding: 20px;
  }
  
  .section-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .trip-details-grid {
    grid-template-columns: 1fr;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .email-grid {
    grid-template-columns: 1fr;
  }
  
  .email-header {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }
  
  .email-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .comment-actions {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
