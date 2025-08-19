<template>
  <div class="trip-hotels">
    <div class="section-header">
      <h3>
        <i class="fas fa-bed"></i>
        Hotel Management
      </h3>
      <div class="header-actions">
        <button @click="addHotel" class="btn btn-success">
          <i class="fas fa-plus"></i>
          Add Hotel
        </button>
      </div>
    </div>

    <!-- Hotel Content will be loaded here -->
    <div class="hotels-content">
      <p>Hotel management component - to be implemented with hotels.php functionality</p>
    </div>

    <!-- Comments Section -->
    <div class="comments-section">
      <div class="section-header">
        <h4>
          <i class="fas fa-comments"></i>
          Hotel Comments
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
        </div>
        
        <div v-if="comments.length === 0" class="no-comments">
          <i class="fas fa-comment-slash"></i>
          <p>No comments yet for hotel arrangements.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  tripId: [String, Number],
  comments: { type: Array, default: () => [] }
})

const emit = defineEmits(['add-comment'])

const showAddComment = ref(false)
const newComment = ref('')

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const addHotel = () => {
  console.log('Add hotel functionality')
}

const submitComment = () => {
  if (newComment.value.trim()) {
    emit('add-comment', 2, newComment.value.trim()) // Stage 2 = Hotels
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
/* Use same styles as TripProposal for consistency */
.trip-hotels { padding: 30px; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 2px solid #f8f9fa; }
.section-header h3, .section-header h4 { margin: 0; color: #2c3e50; display: flex; align-items: center; gap: 10px; }
.section-header i { color: #667eea; }
.header-actions { display: flex; gap: 12px; }
.hotels-content { padding: 40px; text-align: center; background: #f8f9fa; border-radius: 12px; margin-bottom: 30px; }
.comments-section { background: #f8f9fa; padding: 24px; border-radius: 12px; }
.add-comment-form { background: white; padding: 20px; border-radius: 8px; margin-bottom: 24px; border: 2px solid #e9ecef; }
.comment-textarea { width: 100%; border: 2px solid #e9ecef; border-radius: 8px; padding: 12px; font-size: 14px; resize: vertical; margin-bottom: 12px; }
.comment-textarea:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
.comment-actions { display: flex; gap: 12px; }
.comments-list { display: flex; flex-direction: column; gap: 16px; }
.comment-item { background: white; padding: 16px; border-radius: 8px; border-left: 4px solid #667eea; }
.comment-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.comment-author { font-weight: 600; color: #2c3e50; }
.comment-date { color: #7f8c8d; font-size: 14px; }
.comment-content { color: #2c3e50; line-height: 1.6; }
.no-comments { text-align: center; padding: 40px 20px; color: #7f8c8d; }
.no-comments i { font-size: 48px; margin-bottom: 16px; opacity: 0.5; }
.btn { padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 600; transition: all 0.3s ease; display: inline-flex; align-items: center; gap: 6px; }
.btn-success { background: #28a745; color: white; }
.btn-success:hover { background: #218838; transform: translateY(-1px); }
.btn-primary { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3); }
.btn-secondary { background: #6c757d; color: white; }
.btn-secondary:hover { background: #5a6268; transform: translateY(-1px); }
</style>
