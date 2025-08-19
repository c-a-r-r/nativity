<template>
  <div class="trip-note-container">
    
    <!-- Notes Section -->
    <div class="notes-section">
      <div class="section-header">
        <h3>
          <i class="fas fa-sticky-note"></i>
          Trip Notes
        </h3>
        <button @click="addNewNote" class="btn btn-primary">
          <i class="fas fa-plus"></i>
          Add Note
        </button>
      </div>

      <!-- Add Note Form -->
      <div v-if="showAddForm" class="add-note-form">
        <div class="form-group">
          <label>Note Content</label>
          <textarea 
            v-model="newNote.content"
            class="form-control"
            rows="4"
            placeholder="Enter your note here..."
          ></textarea>
        </div>
        <div class="form-group">
          <label>Note Type</label>
          <select v-model="newNote.type" class="form-control">
            <option value="general">General Note</option>
            <option value="important">Important</option>
            <option value="reminder">Reminder</option>
            <option value="issue">Issue</option>
            <option value="follow-up">Follow-up Required</option>
          </select>
        </div>
        <div class="form-actions">
          <button @click="saveNote" class="btn btn-success" :disabled="!newNote.content.trim()">
            <i class="fas fa-save"></i>
            Save Note
          </button>
          <button @click="cancelAdd" class="btn btn-secondary">
            <i class="fas fa-times"></i>
            Cancel
          </button>
        </div>
      </div>

      <!-- Notes List -->
      <div class="notes-list">
        <div 
          v-for="note in sortedNotes" 
          :key="note.id"
          class="note-item"
          :class="getNoteClass(note.type)"
        >
          <div class="note-header">
            <div class="note-meta">
              <span class="note-type" :class="getTypeClass(note.type)">
                <i :class="getTypeIcon(note.type)"></i>
                {{ getTypeLabel(note.type) }}
              </span>
              <span class="note-date">{{ formatDate(note.created_at) }}</span>
              <span class="note-author">by {{ note.author || 'System' }}</span>
            </div>
            <div class="note-actions">
              <button @click="editNote(note)" class="btn-icon edit" title="Edit Note">
                <i class="fas fa-edit"></i>
              </button>
              <button @click="deleteNote(note.id)" class="btn-icon delete" title="Delete Note">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
          <div class="note-content">
            <div v-if="editingNote?.id === note.id" class="edit-form">
              <textarea 
                v-model="editingNote.content"
                class="form-control"
                rows="3"
              ></textarea>
              <div class="edit-actions">
                <button @click="updateNote" class="btn btn-sm btn-success">Save</button>
                <button @click="cancelEdit" class="btn btn-sm btn-secondary">Cancel</button>
              </div>
            </div>
            <div v-else class="note-text">
              {{ note.content }}
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="notes.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="fas fa-sticky-note"></i>
          </div>
          <h4>No Notes Yet</h4>
          <p>Add notes to keep track of important information about this trip.</p>
          <button @click="addNewNote" class="btn btn-primary">
            <i class="fas fa-plus"></i>
            Add First Note
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import axios from 'axios'

// Props
const props = defineProps({
  tripId: {
    type: [String, Number],
    required: true
  },
  comments: {
    type: Array,
    default: () => []
  }
})

// Emits
const emit = defineEmits(['add-comment'])

// State
const notes = ref([...props.comments])
const showAddForm = ref(false)
const editingNote = ref(null)
const loading = ref(false)

const newNote = reactive({
  content: '',
  type: 'general'
})

// Computed
const sortedNotes = computed(() => {
  return [...notes.value].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
})

// Methods
const addNewNote = () => {
  showAddForm.value = true
  newNote.content = ''
  newNote.type = 'general'
}

const cancelAdd = () => {
  showAddForm.value = false
  newNote.content = ''
  newNote.type = 'general'
}

const saveNote = async () => {
  if (!newNote.content.trim()) return
  
  try {
    loading.value = true
    
    const noteData = {
      trip_id: props.tripId,
      content: newNote.content.trim(),
      type: newNote.type,
      created_at: new Date().toISOString(),
      author: 'Current User' // TODO: Get from auth
    }
    
    // TODO: Replace with actual API call
    const response = await axios.post(`/api/trips/${props.tripId}/notes/`, noteData)
    
    notes.value.unshift(response.data)
    emit('add-comment', { section: 'notes', comment: response.data })
    
    cancelAdd()
    
  } catch (error) {
    console.error('Error saving note:', error)
  } finally {
    loading.value = false
  }
}

const editNote = (note) => {
  editingNote.value = { ...note }
}

const cancelEdit = () => {
  editingNote.value = null
}

const updateNote = async () => {
  if (!editingNote.value?.content.trim()) return
  
  try {
    loading.value = true
    
    // TODO: Replace with actual API call
    const response = await axios.patch(`/api/trips/${props.tripId}/notes/${editingNote.value.id}/`, {
      content: editingNote.value.content.trim()
    })
    
    const index = notes.value.findIndex(n => n.id === editingNote.value.id)
    if (index !== -1) {
      notes.value[index] = response.data
    }
    
    cancelEdit()
    
  } catch (error) {
    console.error('Error updating note:', error)
  } finally {
    loading.value = false
  }
}

const deleteNote = async (noteId) => {
  if (!confirm('Are you sure you want to delete this note?')) return
  
  try {
    loading.value = true
    
    // TODO: Replace with actual API call
    await axios.delete(`/api/trips/${props.tripId}/notes/${noteId}/`)
    
    notes.value = notes.value.filter(n => n.id !== noteId)
    
  } catch (error) {
    console.error('Error deleting note:', error)
  } finally {
    loading.value = false
  }
}

const getNoteClass = (type) => {
  const classes = {
    general: 'note-general',
    important: 'note-important',
    reminder: 'note-reminder',
    issue: 'note-issue',
    'follow-up': 'note-follow-up'
  }
  return classes[type] || 'note-general'
}

const getTypeClass = (type) => {
  const classes = {
    general: 'type-general',
    important: 'type-important',
    reminder: 'type-reminder',
    issue: 'type-issue',
    'follow-up': 'type-follow-up'
  }
  return classes[type] || 'type-general'
}

const getTypeIcon = (type) => {
  const icons = {
    general: 'fas fa-sticky-note',
    important: 'fas fa-exclamation-triangle',
    reminder: 'fas fa-clock',
    issue: 'fas fa-bug',
    'follow-up': 'fas fa-arrow-right'
  }
  return icons[type] || 'fas fa-sticky-note'
}

const getTypeLabel = (type) => {
  const labels = {
    general: 'General',
    important: 'Important',
    reminder: 'Reminder',
    issue: 'Issue',
    'follow-up': 'Follow-up'
  }
  return labels[type] || 'General'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString()
}
</script>

<style scoped>
.trip-note-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.notes-section {
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.section-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 20px;
  font-weight: 600;
}

.section-header h3 i {
  margin-right: 8px;
  color: #f59e0b;
}

.add-note-form {
  background: #f9fafb;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
}

label {
  display: block;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
  margin-bottom: 6px;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

textarea.form-control {
  resize: vertical;
  font-family: inherit;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.notes-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.note-item {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  background: white;
  transition: border-color 0.2s;
}

.note-item:hover {
  border-color: #d1d5db;
}

.note-important {
  border-left: 4px solid #dc2626;
  background: #fef2f2;
}

.note-reminder {
  border-left: 4px solid #f59e0b;
  background: #fffbeb;
}

.note-issue {
  border-left: 4px solid #ef4444;
  background: #fef2f2;
}

.note-follow-up {
  border-left: 4px solid #3b82f6;
  background: #eff6ff;
}

.note-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.note-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.note-type {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.type-general {
  background: #f3f4f6;
  color: #4b5563;
}

.type-important {
  background: #fef2f2;
  color: #dc2626;
}

.type-reminder {
  background: #fffbeb;
  color: #d97706;
}

.type-issue {
  background: #fef2f2;
  color: #ef4444;
}

.type-follow-up {
  background: #eff6ff;
  color: #2563eb;
}

.note-date {
  font-size: 12px;
  color: #6b7280;
}

.note-author {
  font-size: 12px;
  color: #6b7280;
  font-style: italic;
}

.note-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.btn-icon.edit {
  background: #eff6ff;
  color: #2563eb;
}

.btn-icon.edit:hover {
  background: #dbeafe;
}

.btn-icon.delete {
  background: #fef2f2;
  color: #dc2626;
}

.btn-icon.delete:hover {
  background: #fee2e2;
}

.note-content {
  color: #374151;
  line-height: 1.5;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.edit-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: #6b7280;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  color: #d1d5db;
}

.empty-state h4 {
  margin: 0 0 8px 0;
  color: #374151;
  font-size: 18px;
}

.empty-state p {
  margin: 0 0 24px 0;
  font-size: 14px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 12px;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-success {
  background-color: #10b981;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background-color: #059669;
}

.btn-secondary {
  background-color: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background-color: #4b5563;
}
</style>
