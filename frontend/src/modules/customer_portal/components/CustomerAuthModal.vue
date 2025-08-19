<template>
  <div class="auth-modal-overlay" @click="closeModal">
    <div class="auth-modal" @click.stop>
      <div class="auth-header">
        <h2>{{ isLogin ? 'Sign In' : 'Create Account' }}</h2>
        <button class="close-btn" @click="closeModal">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>

      <div class="auth-content">
        <!-- Login Form -->
        <form v-if="isLogin" @submit.prevent="handleLogin" class="auth-form">
          <div class="form-group">
            <label for="email">Email Address</label>
            <input
              id="email"
              v-model="loginForm.email"
              type="email"
              required
              :disabled="loading"
              placeholder="Enter your email"
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <div class="password-field">
              <input
                id="password"
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                required
                :disabled="loading"
                placeholder="Enter your password"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
              >
                <i :class="showPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
              </button>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="loading">
              <i v-if="loading" class="fa-solid fa-spinner fa-spin"></i>
              {{ loading ? 'Signing In...' : 'Sign In' }}
            </button>
            <button type="button" class="btn-link" @click="showForgotPassword = true">
              Forgot Password?
            </button>
          </div>
        </form>

        <!-- Registration Form -->
        <form v-else @submit.prevent="handleRegister" class="auth-form">
          <div class="form-row">
            <div class="form-group">
              <label for="firstName">First Name</label>
              <input
                id="firstName"
                v-model="registerForm.firstName"
                type="text"
                required
                :disabled="loading"
                placeholder="First name"
              />
            </div>
            <div class="form-group">
              <label for="lastName">Last Name</label>
              <input
                id="lastName"
                v-model="registerForm.lastName"
                type="text"
                required
                :disabled="loading"
                placeholder="Last name"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="regEmail">Email Address</label>
            <input
              id="regEmail"
              v-model="registerForm.email"
              type="email"
              required
              :disabled="loading"
              placeholder="Enter your email"
            />
          </div>

          <div class="form-group">
            <label for="phone">Phone Number</label>
            <input
              id="phone"
              v-model="registerForm.phone"
              type="tel"
              :disabled="loading"
              placeholder="(555) 123-4567"
            />
          </div>

          <div class="form-group">
            <label for="regPassword">Password</label>
            <div class="password-field">
              <input
                id="regPassword"
                v-model="registerForm.password"
                :type="showPassword ? 'text' : 'password'"
                required
                :disabled="loading"
                placeholder="Create a password"
                minlength="8"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
              >
                <i :class="showPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
              </button>
            </div>
          </div>

          <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <input
              id="confirmPassword"
              v-model="registerForm.confirmPassword"
              type="password"
              required
              :disabled="loading"
              placeholder="Confirm your password"
            />
          </div>

          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input
                v-model="registerForm.agreeTerms"
                type="checkbox"
                required
                :disabled="loading"
              />
              <span class="checkmark"></span>
              I agree to the <a href="#" @click="showTerms">Terms of Service</a> 
              and <a href="#" @click="showPrivacy">Privacy Policy</a>
            </label>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="loading || !isValidRegistration">
              <i v-if="loading" class="fa-solid fa-spinner fa-spin"></i>
              {{ loading ? 'Creating Account...' : 'Create Account' }}
            </button>
          </div>
        </form>

        <!-- Toggle between forms -->
        <div class="auth-toggle">
          <p v-if="isLogin">
            Don't have an account?
            <button type="button" class="btn-link" @click="toggleMode">
              Create one here
            </button>
          </p>
          <p v-else>
            Already have an account?
            <button type="button" class="btn-link" @click="toggleMode">
              Sign in here
            </button>
          </p>
        </div>

        <!-- Forgot Password Modal -->
        <div v-if="showForgotPassword" class="forgot-password-overlay" @click="showForgotPassword = false">
          <div class="forgot-password-modal" @click.stop>
            <h3>Reset Password</h3>
            <form @submit.prevent="handleForgotPassword">
              <div class="form-group">
                <label for="resetEmail">Enter your email address</label>
                <input
                  id="resetEmail"
                  v-model="forgotPasswordEmail"
                  type="email"
                  required
                  placeholder="Enter your email"
                />
              </div>
              <div class="form-actions">
                <button type="button" class="btn-secondary" @click="showForgotPassword = false">
                  Cancel
                </button>
                <button type="submit" class="btn-primary">
                  Send Reset Link
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Error/Success Messages -->
        <div v-if="message" class="message" :class="messageType">
          <i :class="messageType === 'error' ? 'fa-solid fa-exclamation-circle' : 'fa-solid fa-check-circle'"></i>
          {{ message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineEmits } from 'vue'
import { useCustomerAuth } from '../composables/useCustomerAuth'

const emit = defineEmits(['close', 'authenticated'])

const { login, register, requestPasswordReset, loading, error } = useCustomerAuth()

// Component state
const isLogin = ref(true)
const showPassword = ref(false)
const showForgotPassword = ref(false)
const message = ref('')
const messageType = ref('error')

// Form data
const loginForm = ref({
  email: '',
  password: ''
})

const registerForm = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

const forgotPasswordEmail = ref('')

// Computed properties
const isValidRegistration = computed(() => {
  return registerForm.value.firstName &&
         registerForm.value.lastName &&
         registerForm.value.email &&
         registerForm.value.password &&
         registerForm.value.password === registerForm.value.confirmPassword &&
         registerForm.value.agreeTerms
})

// Methods
const closeModal = () => {
  emit('close')
}

const toggleMode = () => {
  isLogin.value = !isLogin.value
  clearMessage()
  clearForms()
}

const clearMessage = () => {
  message.value = ''
  messageType.value = 'error'
}

const clearForms = () => {
  loginForm.value = { email: '', password: '' }
  registerForm.value = {
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    agreeTerms: false
  }
}

const showMessage = (msg, type = 'error') => {
  message.value = msg
  messageType.value = type
  setTimeout(() => clearMessage(), 5000)
}

const handleLogin = async () => {
  clearMessage()
  
  try {
    const result = await login(loginForm.value.email, loginForm.value.password)
    
    if (result.success) {
      showMessage('Login successful!', 'success')
      setTimeout(() => {
        emit('authenticated', result.user)
        closeModal()
      }, 1000)
    } else {
      showMessage(result.message || 'Login failed. Please try again.')
    }
  } catch (err) {
    showMessage('An error occurred during login. Please try again.')
  }
}

const handleRegister = async () => {
  clearMessage()
  
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    showMessage('Passwords do not match.')
    return
  }
  
  try {
    const userData = {
      email: registerForm.value.email,
      password: registerForm.value.password,
      password_confirm: registerForm.value.confirmPassword,
      first_name: registerForm.value.firstName,
      last_name: registerForm.value.lastName,
      phone: registerForm.value.phone || '',
      church_name: '',
      spiritual_director: '',
      marketing_emails: true,
      sms_notifications: false
    }
    
    const result = await register(userData)
    
    if (result.success) {
      showMessage('Account created successfully! Please check your email to verify your account.', 'success')
      setTimeout(() => {
        emit('authenticated', result.user)
        closeModal()
      }, 2000)
    } else {
      showMessage(result.message || 'Registration failed. Please try again.')
    }
  } catch (err) {
    showMessage('An error occurred during registration. Please try again.')
  }
}

const handleForgotPassword = async () => {
  try {
    const result = await requestPasswordReset(forgotPasswordEmail.value)
    
    if (result.success) {
      showMessage('Password reset email sent! Please check your inbox.', 'success')
      showForgotPassword.value = false
      forgotPasswordEmail.value = ''
    } else {
      showMessage(result.message || 'Failed to send reset email.')
    }
  } catch (err) {
    showMessage('An error occurred. Please try again.')
  }
}

const showTerms = () => {
  // TODO: Open terms modal
  console.log('Show terms of service')
}

const showPrivacy = () => {
  // TODO: Open privacy policy modal
  console.log('Show privacy policy')
}
</script>

<style scoped>
.auth-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.auth-modal {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.auth-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #eee;
}

.auth-header h2 {
  margin: 0;
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  color: #666;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background: #f5f5f5;
}

.auth-content {
  padding: 24px;
}

.auth-form {
  margin-bottom: 20px;
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

.form-group input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e5e9;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #4a90e2;
}

.form-group input:disabled {
  background: #f5f5f5;
  color: #666;
}

.password-field {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 4px;
}

.checkbox-group {
  margin: 24px 0;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  line-height: 1.5;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin-right: 8px;
  margin-top: 2px;
}

.form-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 24px;
}

.btn-primary {
  background: #4a90e2;
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
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
  padding: 12px 20px;
  border-radius: 6px;
  cursor: pointer;
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

.auth-toggle {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.forgot-password-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
}

.forgot-password-modal {
  background: white;
  padding: 24px;
  border-radius: 8px;
  max-width: 400px;
  width: 90%;
}

.forgot-password-modal h3 {
  margin-top: 0;
  margin-bottom: 20px;
}

.forgot-password-modal .form-actions {
  flex-direction: row;
  justify-content: flex-end;
}

.message {
  margin-top: 16px;
  padding: 12px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
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

@media (max-width: 600px) {
  .auth-modal {
    margin: 10px;
    max-height: calc(100vh - 20px);
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .auth-header,
  .auth-content {
    padding: 16px;
  }
}
</style>
