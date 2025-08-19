import { ref, reactive, readonly } from 'vue'

// Customer authentication store
const currentCustomer = ref(null)
const authToken = ref(localStorage.getItem('customer_token') || null)
const loading = ref(false)
const error = ref(null)

// Base API URL
const API_BASE = 'http://localhost:8000/api/customer'

export function useCustomerAuth() {
  
  // Helper function for API calls
  const apiCall = async (endpoint, options = {}) => {
    const url = `${API_BASE}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(authToken.value && { 'Authorization': `Token ${authToken.value}` })
      },
      ...options
    }

    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body)
    }

    try {
      const response = await fetch(url, config)
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.detail || data.message || 'API call failed')
      }
      
      return { success: true, data }
    } catch (err) {
      console.error('API Error:', err)
      return { success: false, error: err.message }
    }
  }

  // Login function
  const login = async (email, password) => {
    loading.value = true
    error.value = null

    try {
      const result = await apiCall('/login/', {
        method: 'POST',
        body: { email, password }
      })

      if (result.success) {
        const { user, token } = result.data
        
        // Store authentication data
        authToken.value = token
        currentCustomer.value = user
        localStorage.setItem('customer_token', token)
        localStorage.setItem('customer_user', JSON.stringify(user))

        return { success: true, user, message: 'Login successful' }
      } else {
        error.value = result.error
        return { success: false, message: result.error }
      }
    } catch (err) {
      error.value = err.message
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  // Register function
  const register = async (userData) => {
    loading.value = true
    error.value = null

    try {
      const result = await apiCall('/register/', {
        method: 'POST',
        body: userData
      })

      if (result.success) {
        const { user, token } = result.data
        
        // Store authentication data
        authToken.value = token
        currentCustomer.value = user
        localStorage.setItem('customer_token', token)
        localStorage.setItem('customer_user', JSON.stringify(user))

        return { success: true, user, message: 'Registration successful' }
      } else {
        error.value = result.error
        return { success: false, message: result.error }
      }
    } catch (err) {
      error.value = err.message
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  // Logout function
  const logout = async () => {
    loading.value = true

    try {
      if (authToken.value) {
        await apiCall('/logout/', { method: 'POST' })
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear local storage and state regardless of API success
      authToken.value = null
      currentCustomer.value = null
      localStorage.removeItem('customer_token')
      localStorage.removeItem('customer_user')
      loading.value = false
    }
  }

  // Get current user profile
  const getProfile = async () => {
    if (!authToken.value) {
      return { success: false, message: 'Not authenticated' }
    }

    loading.value = true

    try {
      const result = await apiCall('/profile/')
      
      if (result.success) {
        return { success: true, profile: result.data }
      } else {
        return { success: false, message: result.error }
      }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  // Update customer profile
  const updateProfile = async (profileData) => {
    if (!authToken.value) {
      return { success: false, message: 'Not authenticated' }
    }

    loading.value = true

    try {
      const result = await apiCall('/profile/', {
        method: 'PATCH',
        body: profileData
      })

      if (result.success) {
        return { success: true, profile: result.data }
      } else {
        return { success: false, message: result.error }
      }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  // Update account information
  const updateAccount = async (accountData) => {
    if (!authToken.value) {
      return { success: false, message: 'Not authenticated' }
    }

    loading.value = true

    try {
      const result = await apiCall('/account/', {
        method: 'PATCH',
        body: accountData
      })

      if (result.success) {
        // Update current user data
        currentCustomer.value = { ...currentCustomer.value, ...result.data }
        localStorage.setItem('customer_user', JSON.stringify(currentCustomer.value))
        
        return { success: true, user: result.data }
      } else {
        return { success: false, message: result.error }
      }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  // Change password
  const changePassword = async (currentPassword, newPassword) => {
    if (!authToken.value) {
      return { success: false, message: 'Not authenticated' }
    }

    loading.value = true

    try {
      const result = await apiCall('/change-password/', {
        method: 'POST',
        body: {
          current_password: currentPassword,
          new_password: newPassword
        }
      })

      if (result.success) {
        // Force logout to require re-login with new password
        await logout()
        return { success: true, message: 'Password changed successfully. Please log in again.' }
      } else {
        return { success: false, message: result.error }
      }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  // Request password reset
  const requestPasswordReset = async (email) => {
    loading.value = true

    try {
      const result = await apiCall('/request-password-reset/', {
        method: 'POST',
        body: { email }
      })

      if (result.success) {
        return { success: true, message: 'Password reset email sent' }
      } else {
        return { success: false, message: result.error }
      }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  // Confirm password reset
  const confirmPasswordReset = async (token, newPassword) => {
    loading.value = true

    try {
      const result = await apiCall('/confirm-password-reset/', {
        method: 'POST',
        body: {
          token,
          new_password: newPassword
        }
      })

      if (result.success) {
        return { success: true, message: 'Password reset successful' }
      } else {
        return { success: false, message: result.error }
      }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  // Verify email
  const verifyEmail = async (token) => {
    loading.value = true

    try {
      const result = await apiCall(`/verify-email/${token}/`, {
        method: 'POST'
      })

      if (result.success) {
        // Update current user if logged in
        if (currentCustomer.value) {
          currentCustomer.value.is_email_verified = true
          localStorage.setItem('customer_user', JSON.stringify(currentCustomer.value))
        }
        
        return { success: true, message: 'Email verified successfully' }
      } else {
        return { success: false, message: result.error }
      }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  // Check if user is authenticated
  const isAuthenticated = () => {
    return !!authToken.value && !!currentCustomer.value
  }

  // Initialize authentication state from localStorage
  const initAuth = () => {
    const storedUser = localStorage.getItem('customer_user')
    if (authToken.value && storedUser) {
      try {
        currentCustomer.value = JSON.parse(storedUser)
      } catch (err) {
        console.error('Error parsing stored user:', err)
        logout()
      }
    }
  }

  // Initialize on composable creation
  initAuth()

  return {
    // State
    currentCustomer: readonly(currentCustomer),
    authToken: readonly(authToken),
    loading: readonly(loading),
    error: readonly(error),
    
    // Methods
    login,
    register,
    logout,
    getProfile,
    updateProfile,
    updateAccount,
    changePassword,
    requestPasswordReset,
    confirmPasswordReset,
    verifyEmail,
    isAuthenticated,
    initAuth
  }
}
