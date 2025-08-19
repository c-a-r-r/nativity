<template>
  <div class="trip-registration-form">
    <div class="registration-header">
      <h2>Trip Registration</h2>
      <p v-if="pilgrimage">{{ pilgrimage.name }}</p>
      <p class="cost-info" v-if="pilgrimage">Cost: ${{ pilgrimage.cost }}</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
      <p>Processing registration...</p>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
      <button @click="error = null" class="btn-close">×</button>
    </div>

    <!-- Success Message -->
    <div v-if="success" class="success-message">
      <h3>Registration Successful!</h3>
      <p>{{ successMessage }}</p>
      <div v-if="confirmationNumber" class="confirmation-details">
        <p><strong>Confirmation Number:</strong> {{ confirmationNumber }}</p>
        <p><strong>Amount Charged:</strong> ${{ amountCharged }}</p>
      </div>
    </div>

    <!-- Registration Form -->
    <form v-if="!success && !loading" @submit.prevent="submitRegistration" class="registration-form">
      
      <!-- Trip Information -->
      <div class="form-section">
        <h3>Trip Information</h3>
        <div class="form-group">
          <label for="paymentOption">Payment Option *</label>
          <select v-model="formData.paymentoption" id="paymentOption" required>
            <option value="">Select Payment Option</option>
            <option value="pay_in_email">Pay by Mail</option>
            <option value="deposit">Registration Deposit</option>
            <option value="total">Total Amount</option>
            <option value="three_month">3-Month Installment</option>
            <option value="six_month">6-Month Installment</option>
            <option value="custom">Custom Amount</option>
          </select>
        </div>

        <div v-if="formData.paymentoption === 'custom'" class="form-group">
          <label for="customAmount">Custom Payment Amount *</label>
          <input
            type="number"
            v-model="formData.customAmount"
            id="customAmount"
            step="0.01"
            min="0"
            required
          />
        </div>

        <div class="form-group">
          <label for="landOnly">
            <input type="checkbox" v-model="formData.landonly" id="landOnly" />
            Land Only (no flight)
          </label>
        </div>

        <div class="form-group">
          <label for="couponCode">Coupon Code</label>
          <input
            type="text"
            v-model="formData.coupon"
            id="couponCode"
            placeholder="Enter coupon code if applicable"
          />
        </div>

        <div class="form-group">
          <label for="heardAbout">How did you hear about us?</label>
          <textarea
            v-model="formData.know_us"
            id="heardAbout"
            rows="3"
            placeholder="Please tell us how you heard about this trip"
          ></textarea>
        </div>
      </div>

      <!-- Passengers Section -->
      <div class="form-section">
        <h3>Passenger Information</h3>
        <p class="section-description">
          Please provide information for each passenger. The first passenger will be the primary contact.
        </p>

        <div v-for="(passenger, index) in formData.passengers" :key="index" class="passenger-card">
          <div class="passenger-header">
            <h4>Passenger {{ index + 1 }} {{ index === 0 ? '(Primary Contact)' : '' }}</h4>
            <button
              v-if="formData.passengers.length > 1"
              @click="removePassenger(index)"
              type="button"
              class="btn-remove-passenger"
            >
              Remove
            </button>
          </div>

          <!-- Basic Information -->
          <div class="passenger-section">
            <h5>Basic Information</h5>
            <div class="form-row">
              <div class="form-group">
                <label :for="'title-' + index">Title</label>
                <select v-model="passenger.title" :id="'title-' + index">
                  <option value="">Select</option>
                  <option value="Mr">Mr.</option>
                  <option value="Mrs">Mrs.</option>
                  <option value="Ms">Ms.</option>
                  <option value="Dr">Dr.</option>
                  <option value="Rev">Rev.</option>
                </select>
              </div>
              <div class="form-group">
                <label :for="'firstName-' + index">First Name *</label>
                <input
                  type="text"
                  v-model="passenger.firstname"
                  :id="'firstName-' + index"
                  required
                />
              </div>
              <div class="form-group">
                <label :for="'middleName-' + index">Middle Name</label>
                <input
                  type="text"
                  v-model="passenger.middle_name"
                  :id="'middleName-' + index"
                />
              </div>
              <div class="form-group">
                <label :for="'lastName-' + index">Last Name *</label>
                <input
                  type="text"
                  v-model="passenger.lastname"
                  :id="'lastName-' + index"
                  required
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label :for="'preferredName-' + index">Preferred Name</label>
                <input
                  type="text"
                  v-model="passenger.preferred_name"
                  :id="'preferredName-' + index"
                  placeholder="Name for name tag"
                />
              </div>
              <div class="form-group">
                <label :for="'suffix-' + index">Suffix</label>
                <input
                  type="text"
                  v-model="passenger.suffix"
                  :id="'suffix-' + index"
                  placeholder="Jr., Sr., III, etc."
                />
              </div>
              <div class="form-group">
                <label :for="'gender-' + index">Gender *</label>
                <select v-model="passenger.gender" :id="'gender-' + index" required>
                  <option value="">Select</option>
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                </select>
              </div>
              <div class="form-group">
                <label :for="'birthday-' + index">Date of Birth *</label>
                <input
                  type="date"
                  v-model="passenger.birthday"
                  :id="'birthday-' + index"
                  required
                />
              </div>
            </div>
          </div>

          <!-- Contact Information -->
          <div class="passenger-section">
            <h5>Contact Information</h5>
            <div class="form-row">
              <div class="form-group">
                <label :for="'email-' + index">Email *</label>
                <input
                  type="email"
                  v-model="passenger.email"
                  :id="'email-' + index"
                  required
                />
              </div>
              <div class="form-group">
                <label :for="'personalEmail-' + index">Personal Email</label>
                <input
                  type="email"
                  v-model="passenger.personal_email"
                  :id="'personalEmail-' + index"
                />
              </div>
              <div class="form-group">
                <label :for="'businessEmail-' + index">Business Email</label>
                <input
                  type="email"
                  v-model="passenger.business_email"
                  :id="'businessEmail-' + index"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label :for="'phone-' + index">Phone *</label>
                <input
                  type="tel"
                  v-model="passenger.phone"
                  :id="'phone-' + index"
                  required
                />
              </div>
              <div class="form-group">
                <label :for="'mobilePhone-' + index">Mobile Phone</label>
                <input
                  type="tel"
                  v-model="passenger.mobile_phone"
                  :id="'mobilePhone-' + index"
                />
              </div>
              <div class="form-group">
                <label :for="'workPhone-' + index">Work Phone</label>
                <input
                  type="tel"
                  v-model="passenger.work_phone"
                  :id="'workPhone-' + index"
                />
              </div>
              <div class="form-group">
                <label :for="'fax-' + index">Fax</label>
                <input
                  type="tel"
                  v-model="passenger.fax"
                  :id="'fax-' + index"
                />
              </div>
            </div>
          </div>

          <!-- Address Information -->
          <div class="passenger-section">
            <h5>Address Information</h5>
            <div class="form-row">
              <div class="form-group">
                <label :for="'address-' + index">Address</label>
                <input
                  type="text"
                  v-model="passenger.address"
                  :id="'address-' + index"
                />
              </div>
              <div class="form-group">
                <label :for="'address2-' + index">Address 2</label>
                <input
                  type="text"
                  v-model="passenger.address2"
                  :id="'address2-' + index"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label :for="'city-' + index">City</label>
                <input
                  type="text"
                  v-model="passenger.city"
                  :id="'city-' + index"
                />
              </div>
              <div class="form-group">
                <label :for="'state-' + index">State/Province</label>
                <input
                  type="text"
                  v-model="passenger.state"
                  :id="'state-' + index"
                />
              </div>
              <div class="form-group">
                <label :for="'zipcode-' + index">ZIP/Postal Code</label>
                <input
                  type="text"
                  v-model="passenger.zipcode"
                  :id="'zipcode-' + index"
                />
              </div>
              <div class="form-group">
                <label :for="'country-' + index">Country</label>
                <select v-model="passenger.country" :id="'country-' + index">
                  <option value="">Select Country</option>
                  <option v-for="country in countries" :key="country.id" :value="country.nombre">
                    {{ country.nombre }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Travel Documents -->
          <div class="passenger-section">
            <h5>Travel Documents</h5>
            <div class="form-row">
              <div class="form-group">
                <label :for="'passport-' + index">Passport Number</label>
                <input
                  type="text"
                  v-model="passenger.passport"
                  :id="'passport-' + index"
                />
              </div>
              <div class="form-group">
                <label :for="'passportCountry-' + index">Passport Country</label>
                <select v-model="passenger.passport_country" :id="'passportCountry-' + index">
                  <option value="">Select Country</option>
                  <option v-for="country in countries" :key="country.id" :value="country.nombre">
                    {{ country.nombre }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label :for="'passportExp-' + index">Passport Expiry Date</label>
                <input
                  type="date"
                  v-model="passenger.passport_exp"
                  :id="'passportExp-' + index"
                />
              </div>
              <div class="form-group">
                <label :for="'nationality-' + index">Nationality</label>
                <input
                  type="text"
                  v-model="passenger.nationality"
                  :id="'nationality-' + index"
                />
              </div>
            </div>
          </div>

          <!-- Emergency Contact (only for first passenger) -->
          <div v-if="index === 0" class="passenger-section">
            <h5>Emergency Contact</h5>
            <div class="form-row">
              <div class="form-group">
                <label :for="'emergencyContact-' + index">Emergency Contact Name</label>
                <input
                  type="text"
                  v-model="passenger.emergency_contact"
                  :id="'emergencyContact-' + index"
                />
              </div>
              <div class="form-group">
                <label :for="'emergencyPhone-' + index">Emergency Contact Phone</label>
                <input
                  type="tel"
                  v-model="passenger.emergency_contact_phone"
                  :id="'emergencyPhone-' + index"
                />
              </div>
            </div>
          </div>

          <!-- Room & Travel Preferences -->
          <div class="passenger-section">
            <h5>Room & Travel Preferences</h5>
            <div class="form-row">
              <div class="form-group">
                <label :for="'roomPreference-' + index">Room Preference</label>
                <select v-model="passenger.room_preference" :id="'roomPreference-' + index">
                  <option value="">No Preference</option>
                  <option value="SGL">Single Room</option>
                  <option value="DBL">Double Room</option>
                  <option value="TWN">Twin Room</option>
                  <option value="TRPL">Triple Room</option>
                </select>
              </div>
              <div class="form-group">
                <label :for="'roommatePreference-' + index">Roommate Preference</label>
                <input
                  type="text"
                  v-model="passenger.roommate_preference"
                  :id="'roommatePreference-' + index"
                  placeholder="Name of preferred roommate"
                />
              </div>
              <div class="form-group">
                <label :for="'shirtSize-' + index">Shirt Size</label>
                <select v-model="passenger.shirt_size" :id="'shirtSize-' + index">
                  <option value="">Select Size</option>
                  <option value="XS">XS</option>
                  <option value="S">S</option>
                  <option value="M">M</option>
                  <option value="L">L</option>
                  <option value="XL">XL</option>
                  <option value="2XL">2XL</option>
                  <option value="3XL">3XL</option>
                </select>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label :for="'dietaryRestrictions-' + index">Dietary Restrictions</label>
                <textarea
                  v-model="passenger.dietary_restrictions"
                  :id="'dietaryRestrictions-' + index"
                  rows="3"
                  placeholder="Please list any dietary restrictions or food allergies"
                ></textarea>
              </div>
              <div class="form-group">
                <label :for="'medicalConditions-' + index">Medical Conditions</label>
                <textarea
                  v-model="passenger.medical_conditions"
                  :id="'medicalConditions-' + index"
                  rows="3"
                  placeholder="Please list any medical conditions we should be aware of"
                ></textarea>
              </div>
            </div>

            <div class="form-group">
              <label :for="'specialAssistance-' + index">Special Assistance Requirements</label>
              <textarea
                v-model="passenger.special_assistance"
                :id="'specialAssistance-' + index"
                rows="3"
                placeholder="Please describe any special assistance needs (mobility, accessibility, etc.)"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Add Passenger Button -->
        <button @click="addPassenger" type="button" class="btn-add-passenger">
          + Add Another Passenger
        </button>
      </div>

      <!-- Payment Information (if not pay by mail) -->
      <div v-if="formData.paymentoption && formData.paymentoption !== 'pay_in_email'" class="form-section">
        <h3>Payment Information</h3>
        <p class="payment-info">
          Total Amount: ${{ calculateTotalAmount() }}
          <span v-if="formData.paymentoption !== 'pay_in_email'" class="processing-fee">
            (includes 3% processing fee)
          </span>
        </p>

        <!-- Credit Card Information -->
        <div class="payment-section">
          <h4>Credit Card Information</h4>
          <div class="form-row">
            <div class="form-group">
              <label for="cardNumber">Card Number *</label>
              <input
                type="text"
                v-model="formData.card_number"
                id="cardNumber"
                placeholder="1234 5678 9012 3456"
                required
                maxlength="19"
              />
            </div>
            <div class="form-group">
              <label for="cardExpiry">Expiry Month *</label>
              <select v-model="formData.card_expiry_month" id="cardExpiry" required>
                <option value="">Month</option>
                <option v-for="month in 12" :key="month" :value="month.toString().padStart(2, '0')">
                  {{ month.toString().padStart(2, '0') }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="cardExpiryYear">Expiry Year *</label>
              <select v-model="formData.card_expiry_year" id="cardExpiryYear" required>
                <option value="">Year</option>
                <option v-for="year in getYearOptions()" :key="year" :value="year">
                  {{ year }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="cardCvv">CVV *</label>
              <input
                type="text"
                v-model="formData.card_cvv"
                id="cardCvv"
                placeholder="123"
                required
                maxlength="4"
              />
            </div>
          </div>

          <!-- Billing Address -->
          <h4>Billing Address</h4>
          <div class="form-row">
            <div class="form-group">
              <label for="billingFirstName">First Name *</label>
              <input
                type="text"
                v-model="formData.billing_firstname"
                id="billingFirstName"
                required
              />
            </div>
            <div class="form-group">
              <label for="billingLastName">Last Name *</label>
              <input
                type="text"
                v-model="formData.billing_lastname"
                id="billingLastName"
                required
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="billingAddress">Address *</label>
              <input
                type="text"
                v-model="formData.billing_address"
                id="billingAddress"
                required
              />
            </div>
            <div class="form-group">
              <label for="billingCity">City *</label>
              <input
                type="text"
                v-model="formData.billing_city"
                id="billingCity"
                required
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="billingState">State *</label>
              <input
                type="text"
                v-model="formData.billing_state"
                id="billingState"
                required
              />
            </div>
            <div class="form-group">
              <label for="billingZip">ZIP Code *</label>
              <input
                type="text"
                v-model="formData.billing_zip"
                id="billingZip"
                required
              />
            </div>
            <div class="form-group">
              <label for="billingCountry">Country *</label>
              <select v-model="formData.billing_country" id="billingCountry" required>
                <option value="">Select Country</option>
                <option v-for="country in countries" :key="country.id" :value="country.nombre">
                  {{ country.nombre }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Submit Button -->
      <div class="form-actions">
        <button type="submit" class="btn-submit" :disabled="loading">
          <span v-if="loading">Processing...</span>
          <span v-else>
            {{ formData.paymentoption === 'pay_in_email' ? 'Submit Registration' : 'Submit Payment' }}
          </span>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'TripRegistrationForm',
  setup() {
    const router = useRouter()
    const route = useRoute()
    
    // Reactive state
    const loading = ref(false)
    const error = ref(null)
    const success = ref(false)
    const successMessage = ref('')
    const confirmationNumber = ref('')
    const amountCharged = ref(0)
    
    const pilgrimage = ref(null)
    const countries = ref([])
    
    // Form data
    const formData = reactive({
      pilgrimage_id: null,
      ap: '',
      gsv: '142',
      paymentoption: '',
      customAmount: null,
      landonly: false,
      coupon: '',
      know_us: '',
      passengers: [createNewPassenger()],
      // Credit card fields
      card_number: '',
      card_expiry_month: '',
      card_expiry_year: '',
      card_cvv: '',
      billing_firstname: '',
      billing_lastname: '',
      billing_address: '',
      billing_city: '',
      billing_state: '',
      billing_zip: '',
      billing_country: ''
    })

    // Create new passenger object
    function createNewPassenger() {
      return {
        title: '',
        firstname: '',
        middle_name: '',
        lastname: '',
        preferred_name: '',
        suffix: '',
        email: '',
        personal_email: '',
        business_email: '',
        phone: '',
        mobile_phone: '',
        work_phone: '',
        fax: '',
        address: '',
        address2: '',
        city: '',
        state: '',
        zipcode: '',
        country: '',
        birthday: '',
        gender: '',
        passport: '',
        passport_country: '',
        passport_exp: '',
        nationality: '',
        emergency_contact: '',
        emergency_contact_phone: '',
        room_preference: '',
        roommate_preference: '',
        shirt_size: '',
        dietary_restrictions: '',
        medical_conditions: '',
        special_assistance: '',
        occupation: '',
        previous_traveler: ''
      }
    }

    // Add passenger
    function addPassenger() {
      formData.passengers.push(createNewPassenger())
    }

    // Remove passenger
    function removePassenger(index) {
      if (formData.passengers.length > 1) {
        formData.passengers.splice(index, 1)
      }
    }

    // Calculate total amount
    function calculateTotalAmount() {
      if (!pilgrimage.value) return 0
      
      let baseAmount = parseFloat(pilgrimage.value.cost)
      
      if (formData.paymentoption === 'custom' && formData.customAmount) {
        baseAmount = parseFloat(formData.customAmount)
      } else if (formData.paymentoption === 'deposit') {
        baseAmount = baseAmount * 0.25 // 25% deposit
      } else if (formData.paymentoption === 'three_month') {
        baseAmount = baseAmount / 3
      } else if (formData.paymentoption === 'six_month') {
        baseAmount = baseAmount / 6
      }
      
      // Add 3% processing fee for credit card payments
      if (formData.paymentoption !== 'pay_in_email') {
        baseAmount = baseAmount * 1.03
      }
      
      return baseAmount.toFixed(2)
    }

    // Get year options for credit card expiry
    function getYearOptions() {
      const currentYear = new Date().getFullYear()
      const years = []
      for (let i = 0; i < 10; i++) {
        years.push(currentYear + i)
      }
      return years
    }

    // Load initial data
    async function loadInitialData() {
      try {
        loading.value = true
        
        // Get pilgrimage ID from route
        const pilgrimageId = route.params.id
        if (!pilgrimageId) {
          throw new Error('No pilgrimage ID provided')
        }
        
        formData.pilgrimage_id = parseInt(pilgrimageId)
        
        // Load pilgrimage details and countries in parallel
        const [pilgrimageResponse, countriesResponse] = await Promise.all([
          fetch(`/api/registration/pilgrimage/${pilgrimageId}/`),
          fetch('/api/registration/countries/')
        ])
        
        if (!pilgrimageResponse.ok) {
          throw new Error('Failed to load pilgrimage details')
        }
        
        if (!countriesResponse.ok) {
          throw new Error('Failed to load countries')
        }
        
        pilgrimage.value = await pilgrimageResponse.json()
        countries.value = await countriesResponse.json()
        
        // Set the trip code (ap field)
        formData.ap = pilgrimage.value.slug || `TRIP-${pilgrimageId}`
        
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    // Submit registration
    async function submitRegistration() {
      try {
        loading.value = true
        error.value = null
        
        // Validate form
        if (!validateForm()) {
          return
        }
        
        // Prepare submission data
        const submissionData = {
          pilgrimage_id: formData.pilgrimage_id,
          ap: formData.ap,
          gsv: formData.gsv,
          paymentoption: formData.paymentoption,
          totalcost: parseFloat(calculateTotalAmount()),
          landonly: formData.landonly ? 'yes' : 'no',
          coupon: formData.coupon,
          know_us: formData.know_us,
          passengers: formData.passengers,
          lead_firstname: formData.passengers[0]?.firstname || '',
          lead_lastname: formData.passengers[0]?.lastname || '',
          lead_email: formData.passengers[0]?.email || '',
          lead_phone: formData.passengers[0]?.phone || '',
          emergency_contact: formData.passengers[0]?.emergency_contact || '',
          emergency_contact_phone: formData.passengers[0]?.emergency_contact_phone || ''
        }
        
        // Add credit card data if not paying by mail
        if (formData.paymentoption !== 'pay_in_email') {
          Object.assign(submissionData, {
            card_number: formData.card_number,
            card_expiry_month: formData.card_expiry_month,
            card_expiry_year: formData.card_expiry_year,
            card_cvv: formData.card_cvv,
            billing_firstname: formData.billing_firstname,
            billing_lastname: formData.billing_lastname,
            billing_address: formData.billing_address,
            billing_city: formData.billing_city,
            billing_state: formData.billing_state,
            billing_zip: formData.billing_zip,
            billing_country: formData.billing_country
          })
        }
        
        // Submit registration
        const response = await fetch('/api/registration/submit/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(submissionData)
        })
        
        const result = await response.json()
        
        if (!response.ok) {
          throw new Error(result.error || 'Registration failed')
        }
        
        if (result.payment_required) {
          // Process payment
          await processPayment(result.registration_id, result.session_id, submissionData)
        } else {
          // Pay by mail - show success
          success.value = true
          successMessage.value = result.message
        }
        
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    // Process payment
    async function processPayment(registrationId, sessionId, formData) {
      try {
        const paymentData = {
          registration_id: registrationId,
          session_id: sessionId,
          card_data: {
            card_number: formData.card_number,
            card_expiry_month: formData.card_expiry_month,
            card_expiry_year: formData.card_expiry_year,
            card_cvv: formData.card_cvv
          },
          billing_data: {
            firstname: formData.billing_firstname,
            lastname: formData.billing_lastname,
            address: formData.billing_address,
            city: formData.billing_city,
            state: formData.billing_state,
            zip: formData.billing_zip,
            country: formData.billing_country
          }
        }
        
        const response = await fetch('/api/registration/payment/process/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(paymentData)
        })
        
        const result = await response.json()
        
        if (!response.ok) {
          throw new Error(result.error || 'Payment failed')
        }
        
        if (result.success) {
          success.value = true
          successMessage.value = result.message
          confirmationNumber.value = result.confirmation_number
          amountCharged.value = result.amount_charged
        } else {
          throw new Error(result.decline_reason || 'Payment was declined')
        }
        
      } catch (err) {
        throw err
      }
    }

    // Validate form
    function validateForm() {
      // Basic validation
      if (!formData.paymentoption) {
        error.value = 'Please select a payment option'
        return false
      }
      
      if (formData.passengers.length === 0) {
        error.value = 'At least one passenger is required'
        return false
      }
      
      // Validate first passenger (required fields)
      const leadPassenger = formData.passengers[0]
      if (!leadPassenger.firstname || !leadPassenger.lastname || !leadPassenger.email) {
        error.value = 'Please fill in required fields for the primary passenger'
        return false
      }
      
      // Validate credit card fields if not paying by mail
      if (formData.paymentoption !== 'pay_in_email') {
        const requiredCardFields = [
          'card_number', 'card_expiry_month', 'card_expiry_year', 'card_cvv',
          'billing_firstname', 'billing_lastname', 'billing_address', 
          'billing_city', 'billing_state', 'billing_zip', 'billing_country'
        ]
        
        for (const field of requiredCardFields) {
          if (!formData[field]) {
            error.value = 'Please fill in all required payment information'
            return false
          }
        }
      }
      
      return true
    }

    // Load data on component mount
    onMounted(() => {
      loadInitialData()
    })

    return {
      loading,
      error,
      success,
      successMessage,
      confirmationNumber,
      amountCharged,
      pilgrimage,
      countries,
      formData,
      addPassenger,
      removePassenger,
      calculateTotalAmount,
      getYearOptions,
      submitRegistration
    }
  }
}
</script>

<style scoped>
@import url('./trip-registration.css');
</style>
