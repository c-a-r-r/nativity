<template>
  <div class="customer-account">
    <div class="account-header">
      <h1>My Account</h1>
      <button @click="handleLogout" class="logout-btn">
        <i class="fa-solid fa-sign-out-alt"></i>
        Sign Out
      </button>
    </div>

    <div class="account-content">
      <!-- Profile Information -->
      <div class="account-section">
        <div class="section-header">
          <h2>Profile Information</h2>
          <button 
            @click="toggleEditProfile" 
            class="edit-btn"
            :class="{ active: editingProfile }"
          >
            <i :class="editingProfile ? 'fa-solid fa-times' : 'fa-solid fa-edit'"></i>
            {{ editingProfile ? 'Cancel' : 'Edit' }}
          </button>
        </div>

        <form v-if="editingProfile" @submit.prevent="saveProfile" class="profile-form">
          <div class="form-row">
            <div class="form-group">
              <label for="firstName">First Name</label>
              <input
                id="firstName"
                v-model="profileForm.first_name"
                type="text"
                required
                :disabled="loading"
              />
            </div>
            <div class="form-group">
              <label for="lastName">Last Name</label>
              <input
                id="lastName"
                v-model="profileForm.last_name"
                type="text"
                required
                :disabled="loading"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="email">Email Address</label>
            <input
              id="email"
              v-model="profileForm.email"
              type="email"
              required
              :disabled="loading"
            />
            <small v-if="!currentCustomer?.is_email_verified" class="email-warning">
              <i class="fa-solid fa-exclamation-triangle"></i>
              Email not verified. <button type="button" class="btn-link" @click="resendVerification">Resend verification</button>
            </small>
          </div>

          <div class="form-group">
            <label for="phone">Phone Number</label>
            <input
              id="phone"
              v-model="profileForm.phone_number"
              type="tel"
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="address">Address</label>
            <textarea
              id="address"
              v-model="profileForm.address"
              rows="3"
              :disabled="loading"
              placeholder="Street address, city, state, zip code"
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="emergencyName">Emergency Contact Name</label>
              <input
                id="emergencyName"
                v-model="profileForm.emergency_contact_name"
                type="text"
                :disabled="loading"
              />
            </div>
            <div class="form-group">
              <label for="emergencyPhone">Emergency Contact Phone</label>
              <input
                id="emergencyPhone"
                v-model="profileForm.emergency_contact_phone"
                type="tel"
                :disabled="loading"
              />
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="cancelEditProfile" class="btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn-primary" :disabled="loading">
              <i v-if="loading" class="fa-solid fa-spinner fa-spin"></i>
              {{ loading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>

        <div v-else class="profile-display">
          <div class="profile-item">
            <strong>Name:</strong> {{ currentCustomer?.first_name }} {{ currentCustomer?.last_name }}
          </div>
          <div class="profile-item">
            <strong>Email:</strong> 
            {{ currentCustomer?.email }}
            <span v-if="currentCustomer?.is_email_verified" class="verified-badge">
              <i class="fa-solid fa-check-circle"></i> Verified
            </span>
            <span v-else class="unverified-badge">
              <i class="fa-solid fa-exclamation-circle"></i> Not Verified
            </span>
          </div>
          <div class="profile-item" v-if="currentCustomer?.phone_number">
            <strong>Phone:</strong> {{ currentCustomer.phone_number }}
          </div>
          <div class="profile-item" v-if="userProfile?.address">
            <strong>Address:</strong> {{ userProfile.address }}
          </div>
          <div class="profile-item" v-if="userProfile?.emergency_contact_name">
            <strong>Emergency Contact:</strong> 
            {{ userProfile.emergency_contact_name }}
            <span v-if="userProfile.emergency_contact_phone">
              - {{ userProfile.emergency_contact_phone }}
            </span>
          </div>
        </div>
      </div>

      <!-- Password Change -->
      <div class="account-section">
        <div class="section-header">
          <h2>Security</h2>
          <button 
            @click="toggleEditPassword" 
            class="edit-btn"
            :class="{ active: editingPassword }"
          >
            <i :class="editingPassword ? 'fa-solid fa-times' : 'fa-solid fa-key'"></i>
            {{ editingPassword ? 'Cancel' : 'Change Password' }}
          </button>
        </div>

        <form v-if="editingPassword" @submit.prevent="changeUserPassword" class="password-form">
          <div class="form-group">
            <label for="currentPassword">Current Password</label>
            <input
              id="currentPassword"
              v-model="passwordForm.currentPassword"
              type="password"
              required
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="newPassword">New Password</label>
            <input
              id="newPassword"
              v-model="passwordForm.newPassword"
              type="password"
              required
              minlength="8"
              :disabled="loading"
            />
            <small class="password-help">
              Password must be at least 8 characters long
            </small>
          </div>

          <div class="form-group">
            <label for="confirmNewPassword">Confirm New Password</label>
            <input
              id="confirmNewPassword"
              v-model="passwordForm.confirmPassword"
              type="password"
              required
              :disabled="loading"
            />
          </div>

          <div class="form-actions">
            <button type="button" @click="cancelEditPassword" class="btn-secondary">
              Cancel
            </button>
            <button 
              type="submit" 
              class="btn-primary" 
              :disabled="loading || !isValidPasswordForm"
            >
              <i v-if="loading" class="fa-solid fa-spinner fa-spin"></i>
              {{ loading ? 'Changing...' : 'Change Password' }}
            </button>
          </div>
        </form>

        <div v-else class="security-display">
          <div class="profile-item">
            <strong>Password:</strong> •••••••••••
            <small class="text-muted">Last changed: {{ formatDate(currentCustomer?.date_joined) }}</small>
          </div>
        </div>
      </div>

      <!-- Trip History (Future) -->
      <div class="account-section">
        <div class="section-header">
          <h2>Trip History</h2>
        </div>
        <div class="empty-state">
          <i class="fa-solid fa-plane"></i>
          <p>No trips booked yet</p>
          <button @click="$router.push('/trips')" class="btn-primary">
            Browse Trips
          </button>
        </div>
      </div>
    </div>

    <!-- Messages -->
    <div v-if="message" class="message" :class="messageType">
      <i :class="messageType === 'error' ? 'fa-solid fa-exclamation-circle' : 'fa-solid fa-check-circle'"></i>
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCustomerAuth } from '../composables/useCustomerAuth'

const router = useRouter()
const { 
  currentCustomer, 
  loading, 
  logout, 
  getProfile, 
  updateProfile, 
  updateAccount, 
  changePassword,
  verifyEmail 
} = useCustomerAuth()

// Component state
const editingProfile = ref(false)
const editingPassword = ref(false)
const userProfile = ref(null)
const message = ref('')
const messageType = ref('error')

// Form data
const profileForm = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone_number: '',
  address: '',
  emergency_contact_name: '',
  emergency_contact_phone: ''
})

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// Computed properties
const isValidPasswordForm = computed(() => {
  return passwordForm.value.currentPassword &&
         passwordForm.value.newPassword &&
         passwordForm.value.newPassword === passwordForm.value.confirmPassword &&
         passwordForm.value.newPassword.length >= 8
})

// Methods
const showMessage = (msg, type = 'error') => {
  message.value = msg
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 5000)
}

const formatDate = (dateString) => {
  if (!dateString) return 'Unknown'
  return new Date(dateString).toLocaleDateString()
}

const loadProfile = async () => {
  const result = await getProfile()
  if (result.success) {
    userProfile.value = result.profile
    
    // Initialize form with current data
    profileForm.value = {
      first_name: currentCustomer.value?.first_name || '',
      last_name: currentCustomer.value?.last_name || '',
      email: currentCustomer.value?.email || '',
      phone_number: currentCustomer.value?.phone_number || '',
      address: result.profile.address || '',
      emergency_contact_name: result.profile.emergency_contact_name || '',
      emergency_contact_phone: result.profile.emergency_contact_phone || ''
    }
  } else {
    showMessage(result.message || 'Failed to load profile')
  }
}

const toggleEditProfile = () => {
  if (!editingProfile.value) {
    // Reset form when starting to edit
    profileForm.value = {
      first_name: currentCustomer.value?.first_name || '',
      last_name: currentCustomer.value?.last_name || '',
      email: currentCustomer.value?.email || '',
      phone_number: currentCustomer.value?.phone_number || '',
      address: userProfile.value?.address || '',
      emergency_contact_name: userProfile.value?.emergency_contact_name || '',
      emergency_contact_phone: userProfile.value?.emergency_contact_phone || ''
    }
  }
  editingProfile.value = !editingProfile.value
}

const cancelEditProfile = () => {
  editingProfile.value = false
  message.value = ''
}

const saveProfile = async () => {
  try {
    // Update account info (name, email, phone)
    const accountData = {
      first_name: profileForm.value.first_name,
      last_name: profileForm.value.last_name,
      email: profileForm.value.email,
      phone_number: profileForm.value.phone_number
    }
    
    const accountResult = await updateAccount(accountData)
    
    if (!accountResult.success) {
      showMessage(accountResult.message || 'Failed to update account information')
      return
    }

    // Update profile info (address, emergency contact)
    const profileData = {
      address: profileForm.value.address,
      emergency_contact_name: profileForm.value.emergency_contact_name,
      emergency_contact_phone: profileForm.value.emergency_contact_phone
    }
    
    const profileResult = await updateProfile(profileData)
    
    if (profileResult.success) {
      userProfile.value = profileResult.profile
      editingProfile.value = false
      showMessage('Profile updated successfully!', 'success')
    } else {
      showMessage(profileResult.message || 'Failed to update profile')
    }
  } catch (err) {
    showMessage('An error occurred while updating your profile')
  }
}

const toggleEditPassword = () => {
  if (!editingPassword.value) {
    // Reset form when starting to edit
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  }
  editingPassword.value = !editingPassword.value
}

const cancelEditPassword = () => {
  editingPassword.value = false
  passwordForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  message.value = ''
}

const changeUserPassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    showMessage('New passwords do not match')
    return
  }

  try {
    const result = await changePassword(
      passwordForm.value.currentPassword,
      passwordForm.value.newPassword
    )
    
    if (result.success) {
      showMessage(result.message, 'success')
      editingPassword.value = false
      passwordForm.value = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
      
      // Redirect to login after password change
      setTimeout(() => {
        router.push('/')
      }, 2000)
    } else {
      showMessage(result.message || 'Failed to change password')
    }
  } catch (err) {
    showMessage('An error occurred while changing your password')
  }
}

const resendVerification = async () => {
  // TODO: Implement resend verification
  showMessage('Verification email sent!', 'success')
}

const handleLogout = async () => {
  await logout()
  router.push('/')
}

// Lifecycle
onMounted(() => {
  if (!currentCustomer.value) {
    router.push('/')
    return
  }
  loadProfile()
})
</script>

<style scoped>
.customer-account {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #eee;
}

.account-header h1 {
  margin: 0;
  color: #333;
  font-size: 28px;
  font-weight: 600;
}

.logout-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.logout-btn:hover {
  background: #c82333;
}

.account-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.account-section {
  background: white;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #e1e5e9;
}

.section-header h2 {
  margin: 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.edit-btn {
  background: #4a90e2;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  transition: background-color 0.2s;
}

.edit-btn:hover {
  background: #357abd;
}

.edit-btn.active {
  background: #dc3545;
}

.edit-btn.active:hover {
  background: #c82333;
}

.profile-form,
.password-form {
  padding: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #e1e5e9;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4a90e2;
}

.form-group input:disabled,
.form-group textarea:disabled {
  background: #f5f5f5;
  color: #666;
}

.email-warning {
  color: #f56565;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
}

.password-help {
  color: #666;
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn-primary {
  background: #4a90e2;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #357abd;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-link {
  background: none;
  border: none;
  color: #4a90e2;
  cursor: pointer;
  text-decoration: underline;
  font-size: inherit;
}

.btn-link:hover {
  color: #357abd;
}

.profile-display,
.security-display {
  padding: 20px;
}

.profile-item {
  margin-bottom: 16px;
  line-height: 1.5;
}

.profile-item strong {
  display: inline-block;
  min-width: 120px;
  color: #333;
}

.verified-badge {
  color: #28a745;
  font-size: 12px;
  font-weight: 500;
  margin-left: 8px;
}

.unverified-badge {
  color: #ffc107;
  font-size: 12px;
  font-weight: 500;
  margin-left: 8px;
}

.text-muted {
  color: #666;
  font-size: 12px;
  margin-left: 8px;
}

.empty-state {
  padding: 40px 20px;
  text-align: center;
  color: #666;
}

.empty-state i {
  font-size: 48px;
  color: #ddd;
  margin-bottom: 16px;
}

.empty-state p {
  margin-bottom: 20px;
  font-size: 16px;
}

.message {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 12px 20px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  max-width: 400px;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.message.error {
  background: #fee;
  color: #d32f2f;
  border: 1px solid #ffcdd2;
}

.message.success {
  background: #e8f5e8;
  color: #388e3c;
  border: 1px solid #c8e6c9;
}

@media (max-width: 768px) {
  .customer-account {
    padding: 10px;
  }
  
  .account-header {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>
