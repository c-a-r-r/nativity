<template>
  <div class="trip-template">
    <!-- Header -->
    <header>
      <div class="top-bar"></div>
      <nav class="nav">
        <a href="/" class="logo">VIZITOR</a>
        <div class="auth-buttons" v-if="!isCustomerAuthenticated">
          <a href="#" class="signin" @click="showAuthModalHandler('login')">SIGN&nbsp;IN</a>
          <a href="#" class="register" @click="showAuthModalHandler('register')">REGISTER</a>
        </div>
        <div class="customer-menu" v-else>
          <span class="customer-greeting">Hello, {{ currentCustomer?.first_name }}!</span>
          <button @click="showAccountModal = true" class="account-btn">
            <i class="fa-solid fa-user"></i>
            My Account
          </button>
        </div>
      </nav>
    </header>

    <!-- Hero Section with Tabs -->
    <section class="hero" :style="{ backgroundImage: `url(${trip.hero_image || defaultHeroImage})` }">
      <nav class="tab-bar" id="tabs">
        <a 
          v-for="tab in tabs" 
          :key="tab.key"
          href="#" 
          class="tab" 
          :class="{ active: activeTab === tab.key }"
          @click="setActiveTab(tab.key)"
        >
          <i :class="tab.icon" style="padding-bottom: 5px;"></i>
          {{ tab.label }}
        </a>
      </nav>
    </section>

    <!-- Mobile Navigation -->
    <section class="mobile-nav">
      <div class="mobile-nav-grid">
        <a 
          v-for="tab in tabs" 
          :key="`mobile-${tab.key}`"
          href="#" 
          class="mobile-nav-item" 
          :class="{ active: activeTab === tab.key }"
          @click="setActiveTab(tab.key)"
        >
          <i :class="tab.icon"></i>
          <span>{{ tab.label }}</span>
        </a>
      </div>
    </section>

    <!-- Main Content -->
    <main>
      <!-- Trip Details -->
      <div v-if="activeTab === 'details'" class="pane active">
        <div class="trip-header">
          <h1 class="trip-title">{{ trip.trip_title }}</h1>
          <span class="trip-price">${{ trip.total_cost }} <small>/ per person</small></span>
        </div>

        <p class="trip-desc">{{ trip.promo_text }}</p>

        <div class="features">
          <div class="feature-item" v-if="formatDuration()">
            <i class="fa-regular fa-calendar-days"></i>
            {{ formatDuration() }}
          </div>
          <div class="feature-item" v-if="trip.destination?.name">
            <i class="fa-solid fa-cross"></i>
            {{ trip.destination?.name }}
          </div>
          <div class="feature-item">
            <i class="fa-solid fa-walking"></i>
            Pilgrimage
          </div>
          <div class="feature-item">
            <i class="fa-solid fa-map-location-dot"></i>
            Sightseeing
          </div>
        </div>

        <table class="spec-table">
          <tbody>
            <tr v-if="trip.destination?.name"><th>Destination</th><td>{{ trip.destination?.name }}</td></tr>
            <tr v-if="trip.quote?.departure_city"><th>Departure City</th><td>{{ trip.quote?.departure_city }}</td></tr>
            <tr v-if="trip.departure_date"><th>Departure date</th><td>{{ formatDate(trip.departure_date) }}</td></tr>
            <tr v-if="trip.arrival_date"><th>Return Date</th><td>{{ formatDate(trip.arrival_date) }}</td></tr>
            <tr v-if="trip.leader_name"><th>Spiritual Director</th><td>{{ trip.leader_name }}</td></tr>
          </tbody>
        </table>
      </div>

      <!-- Itinerary -->
      <div v-if="activeTab === 'itinerary'" class="pane active">
        <h1 class="trip-title" style="display:flex;align-items:center;gap:2rem;color: #3d3d3d; font-weight: 100;">
          ITINERARY
          <label style="margin-left:auto;display:flex;align-items:center;font-size:1rem;gap:.5rem;cursor:pointer;font-weight: 400;color: #00b5c6;">
            <span>Expand all</span>
            <input 
              type="checkbox" 
              v-model="expandAllItinerary" 
              @change="toggleAllItinerary"
              style="accent-color:#ff5a1f;width:32px;height:18px;"
            >
          </label>
        </h1>
        
        <div v-if="itinerary.length === 0" class="text-center py-5">
          <p class="text-muted">No itinerary available for this trip.</p>
        </div>
        
        <ol v-else class="itinerary-timeline">
          <li 
            v-for="(day, index) in itinerary" 
            :key="index"
            class="itinerary-day"
            :class="{ active: day.expanded }"
            @click="toggleItineraryDay(index)"
          >
            <div class="itinerary-dot">
              <i v-if="index === 0 || index === itinerary.length - 1" class="fa-solid fa-location-dot"></i>
              <i v-else class="fa-regular fa-circle"></i>
            </div>
            <div class="itinerary-content">
              <div class="itinerary-title">
                <b style="font-size: 0.995rem;">Day {{ day.day }}: {{ day.title }}</b>
              </div>
              <div class="itinerary-details">
                {{ day.description }}
              </div>
            </div>
          </li>
        </ol>
      </div>

      <!-- Gallery -->
      <div v-if="activeTab === 'gallery'" class="pane active">
        <h1 class="trip-title" style="color: #3d3d3d; font-weight: 100;">GALLERY</h1>
        
        <div v-if="galleryImages.length > 0" class="gallery-grid">
          <div 
            v-for="(image, index) in galleryImages" 
            :key="index"
            class="gallery-item"
            :class="image.class"
          >
            <img :src="image.url" :alt="image.alt" loading="lazy">
            <div class="gallery-overlay">
              <h3>{{ image.title }}</h3>
              <p>{{ image.description }}</p>
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-5">
          <p class="text-muted">No gallery images available for this trip.</p>
        </div>
      </div>

      <!-- Includes/Not Includes -->
      <div v-if="activeTab === 'includes'" class="pane active">
        <h1 class="trip-title" style="color: #3d3d3d; font-weight: 100;">WHAT'S INCLUDED & WHAT'S NOT</h1>
        
        <div class="included-content" v-if="getIncludedItems().length > 0 || getNotIncludedItems().length > 0">
          <div class="included-column" v-if="getIncludedItems().length > 0">
            <h3><i class="fa-solid fa-check-circle"></i> What's Included</h3>
            <ul class="included-list">
              <li v-for="item in getIncludedItems()" :key="item">
                <i class="fa-solid fa-check"></i> {{ item }}
              </li>
            </ul>
          </div>
          <div class="not-included-column" v-if="getNotIncludedItems().length > 0">
            <h3><i class="fa-solid fa-times-circle"></i> What's Not Included</h3>
            <ul class="not-included-list">
              <li v-for="item in getNotIncludedItems()" :key="item">
                <i class="fa-solid fa-times"></i> {{ item }}
              </li>
            </ul>
          </div>
        </div>
        <div v-else class="text-center py-5">
          <p class="text-muted">No inclusion information available for this trip.</p>
        </div>
      </div>

      <!-- Brochure -->
      <div v-if="activeTab === 'brochure'" class="pane active">
        <h1 class="trip-title" style="color: #3d3d3d; font-weight: 100;">BROCHURE</h1>
        
        <div class="brochure-container">
          <div class="brochure-preview" @click="downloadBrochure">
            <img :src="brochurePreviewImage" alt="Trip Brochure" class="brochure-image">
            <div class="brochure-overlay">
              <i class="fa-solid fa-download"></i>
              <span>Click to Download</span>
            </div>
          </div>
          
          <div class="brochure-info">
            <h3 v-if="trip.destination?.name">Spiritual Guide to {{ trip.destination?.name }}</h3>
            <h3 v-else>Trip Brochure</h3>
            <p>Our detailed brochure includes:</p>
            <ul class="brochure-features">
              <li><i class="fa-solid fa-check"></i> Complete day-by-day itinerary</li>
              <li><i class="fa-solid fa-check"></i> Historical background of sacred sites</li>
              <li><i class="fa-solid fa-check"></i> Spiritual reflections and prayers</li>
              <li><i class="fa-solid fa-check"></i> Practical travel information</li>
              <li><i class="fa-solid fa-check"></i> High-quality photos of destinations</li>
              <li><i class="fa-solid fa-check"></i> Maps and location details</li>
            </ul>
            <a 
              :href="trip.brochure" 
              :download="`${trip.trip_title}-Brochure.pdf`" 
              class="download-button"
              v-if="trip.brochure"
            >
              <i class="fa-solid fa-download"></i>
              Download Brochure (PDF)
            </a>
          </div>
        </div>
      </div>

      <!-- Video -->
      <div v-if="activeTab === 'video'" class="pane active">
        <h1 class="trip-title" style="color: #3d3d3d; font-weight: 100; padding-bottom: 25px;">VIDEO</h1>
        <iframe 
          v-if="trip.video_link"
          :src="getVideoEmbedUrl()" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          referrerpolicy="strict-origin-when-cross-origin" 
          allowfullscreen
          style="width: 100%; max-width: 900px; height: 500px; margin-bottom: 30px; border-radius: 8px;"
        ></iframe>
        <div v-else>
          <p>No video available for this trip.</p>
        </div>
      </div>
    </main>

    <!-- Registration and Insurance Section -->
    <section class="registration-section">
      <div class="registration-container">
        <!-- How to Register -->
        <div class="reg-block">
          <div class="reg-header">
            <h2>HOW TO REGISTER</h2>
          </div>
          <div class="reg-content">
            <h3>Register Online</h3>
            <p>Fill the form online and upload a copy of your passport. We accept all major Credit/Debit cards (3% fee applies).</p>
            <a href="#" class="reg-button" @click="handleRegistration">
              {{ isCustomerAuthenticated ? 'Register for Trip' : 'Sign In to Register' }}
            </a>
          </div>
        </div>

        <!-- Travel Insurance -->
        <div class="reg-block">
          <div class="reg-header">
            <h2>TRAVEL INSURANCE</h2>
          </div>
          <div class="reg-content">
            <p>Although travel insurance is optional, it is highly recommended. Buy it now upon registration to get cancel for any reason. There are 2 options for travel insurance:</p>
            <ol class="insurance-options">
              <li>Buy directly online through our website after submitting the application</li>
              <li>Buy insurance from your own insurance company.</li>
            </ol>
            <a href="#" class="reg-button insurance-button" @click="handleInsurance">Travel Insurance Link</a>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>VIZITOR</h3>
          <p>Your trusted partner for unforgettable spiritual journeys and pilgrimage experiences.</p>
        </div>
        <div class="footer-section">
          <h4>Contact Info</h4>
          <div class="contact-item" v-if="getContactPhone()">
            <i class="fa-solid fa-phone"></i>
            <span>{{ getContactPhone() }}</span>
          </div>
          <div class="contact-item" v-if="getContactEmail()">
            <i class="fa-solid fa-envelope"></i>
            <span>{{ getContactEmail() }}</span>
          </div>
          <div class="contact-item" v-if="trip.quote?.departure_city">
            <i class="fa-solid fa-location-dot"></i>
            <span>{{ trip.quote?.departure_city }}</span>
          </div>
        </div>
        <div class="footer-section">
          <h4>Follow Us</h4>
          <div class="social-links">
            <a href="#"><i class="fa-brands fa-facebook"></i></a>
            <a href="#"><i class="fa-brands fa-instagram"></i></a>
            <a href="#"><i class="fa-brands fa-twitter"></i></a>
            <a href="#"><i class="fa-brands fa-youtube"></i></a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2025 VIZITOR. All rights reserved.</p>
      </div>
    </footer>

    <!-- Authentication Modal -->
    <CustomerAuthModal
      v-if="showAuthModal"
      :initial-mode="authModalMode"
      @close="closeAuthModal"
      @authenticated="handleAuthenticated"
    />

    <!-- Customer Account Modal -->
    <div v-if="showAccountModal" class="account-modal-overlay" @click="showAccountModal = false">
      <div class="account-modal" @click.stop>
        <CustomerAccount />
        <button class="close-account-modal" @click="showAccountModal = false">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCustomerAuth } from '../../customer_portal/composables/useCustomerAuth'
import CustomerAuthModal from '../../customer_portal/components/CustomerAuthModal.vue'
import CustomerAccount from '../../customer_portal/components/CustomerAccount.vue'

// Router
const router = useRouter()

// Props
const props = defineProps({
  trip: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

// Customer authentication
const { currentCustomer, isAuthenticated } = useCustomerAuth()
const isCustomerAuthenticated = computed(() => isAuthenticated())

// Modal state
const showAuthModal = ref(false)
const authModalMode = ref('login') // 'login' or 'register'
const showAccountModal = ref(false)

// Reactive data
const activeTab = ref('details')
const expandAllItinerary = ref(false)
const itinerary = ref([])

// Watch for changes in trip prop and update itinerary
const updateItinerary = () => {
  if (props.trip && props.trip.itinerary && Array.isArray(props.trip.itinerary)) {
    itinerary.value = props.trip.itinerary.map(day => ({
      ...day,
      expanded: day.expanded || false
    }))
  } else {
    itinerary.value = []
  }
}

// Update itinerary when component mounts or trip changes
onMounted(() => {
  updateItinerary()
})

// Watch for trip changes
watch(() => props.trip, (newTrip) => {
  updateItinerary()
}, { deep: true, immediate: true })

// Default values
const defaultHeroImage = "https://gotravel.qodeinteractive.com/wp-content/uploads/2016/10/single-title-image-1.jpg"
const brochurePreviewImage = "/images/brochure.webp"

// Tab configuration
const tabs = [
  { key: 'details', label: 'TRIP DETAILS', icon: 'fa-solid fa-info-circle' },
  { key: 'itinerary', label: 'ITINERARY', icon: 'fa-solid fa-route' },
  { key: 'gallery', label: 'GALLERY', icon: 'fa-solid fa-camera-retro' },
  { key: 'includes', label: 'INCLUDES', icon: 'fa-solid fa-clone' },
  { key: 'brochure', label: 'BROCHURE', icon: 'fa-solid fa-file-pdf' },
  { key: 'video', label: 'VIDEO', icon: 'fa-solid fa-video' }
]

// Gallery images from trip data only
const galleryImages = computed(() => {
  // If trip has gallery data, use it
  if (props.trip.gallery && Array.isArray(props.trip.gallery) && props.trip.gallery.length > 0) {
    return props.trip.gallery.map((item, index) => ({
      url: item.url,
      alt: item.title || `Gallery image ${index + 1}`,
      title: item.title || `Image ${index + 1}`,
      description: item.description || '',
      class: getGalleryItemClass(index)
    }))
  }
  
  // If trip.gallery is a string (JSON), parse it
  if (props.trip.gallery && typeof props.trip.gallery === 'string') {
    try {
      const parsed = JSON.parse(props.trip.gallery)
      if (Array.isArray(parsed) && parsed.length > 0) {
        return parsed.map((item, index) => ({
          url: item.url,
          alt: item.title || `Gallery image ${index + 1}`,
          title: item.title || `Image ${index + 1}`,
          description: item.description || '',
          class: getGalleryItemClass(index)
        }))
      }
    } catch (e) {
      console.error('Failed to parse gallery JSON:', e)
    }
  }
  
  // Return empty array if no gallery data
  return []
})

// Helper function to assign CSS classes for gallery layout
const getGalleryItemClass = (index) => {
  // Create a nice varied layout
  if (index === 0) return 'gallery-large'
  if (index === 3) return 'gallery-tall'
  if (index === 6) return 'gallery-wide'
  return ''
}

// Methods
const setActiveTab = (tabKey) => {
  activeTab.value = tabKey
}

const formatDate = (dateString) => {
  if (!dateString) return 'TBD'
  return new Date(dateString).toLocaleDateString('en-US', {
    month: '2-digit',
    day: '2-digit',
    year: 'numeric'
  })
}

const formatDuration = () => {
  if (props.trip.departure_date && props.trip.arrival_date) {
    const start = new Date(props.trip.departure_date)
    const end = new Date(props.trip.arrival_date)
    const diffTime = Math.abs(end - start)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return `${diffDays} Days`
  }
  return ''
}

const toggleItineraryDay = (index) => {
  if (itinerary.value && itinerary.value[index]) {
    itinerary.value[index].expanded = !itinerary.value[index].expanded
  }
}

const toggleAllItinerary = () => {
  if (itinerary.value) {
    itinerary.value.forEach(day => {
      day.expanded = expandAllItinerary.value
    })
  }
}

const getIncludedItems = () => {
  if (props.trip.trip_includes) {
    // Handle if trip_includes is a JSON string
    let includesText = props.trip.trip_includes
    if (typeof includesText === 'string' && includesText.startsWith('[')) {
      try {
        // If it's a JSON array, join the items
        const parsed = JSON.parse(includesText)
        if (Array.isArray(parsed)) {
          includesText = parsed.join('\n')
        }
      } catch (e) {
        // If JSON parsing fails, use as is
      }
    }
    const items = includesText.split('\n').filter(item => item.trim())
    return items
  }
  return []
}

const getNotIncludedItems = () => {
  if (props.trip.trip_not_includes) {
    // Handle if trip_not_includes is a JSON string
    let notIncludesText = props.trip.trip_not_includes
    if (typeof notIncludesText === 'string' && notIncludesText.startsWith('[')) {
      try {
        // If it's a JSON array, join the items
        const parsed = JSON.parse(notIncludesText)
        if (Array.isArray(parsed)) {
          notIncludesText = parsed.join('\n')
        }
      } catch (e) {
        // If JSON parsing fails, use as is
      }
    }
    const items = notIncludesText.split('\n').filter(item => item.trim())
    return items
  }
  return []
}

const getVideoEmbedUrl = () => {
  if (!props.trip.video_link) return ''
  
  // Handle YouTube URLs
  if (props.trip.video_link.includes('youtube.com') || props.trip.video_link.includes('youtu.be')) {
    const videoId = props.trip.video_link.split('v=')[1] || props.trip.video_link.split('/').pop()
    return `https://www.youtube.com/embed/${videoId}`
  }
  
  return props.trip.video_link
}

const downloadBrochure = () => {
  if (props.trip.brochure) {
    window.open(props.trip.brochure, '_blank')
  }
}

const handleRegistration = () => {
  console.log('Registration clicked!')
  console.log('Is authenticated:', isCustomerAuthenticated.value)
  console.log('Trip ID:', props.trip.id)
  console.log('Full trip object:', props.trip)
  
  if (isCustomerAuthenticated.value) {
    // Customer is logged in, proceed with trip registration
    // Navigate to registration form
    console.log('Navigating to:', `/trips/register/${props.trip.id}`)
    router.push(`/trips/register/${props.trip.id}`)
  } else {
    // Customer needs to log in first
    console.log('Not authenticated, showing auth modal')
    showAuthModalHandler('register')
  }
}

const handleInsurance = () => {
  // TODO: Implement insurance logic
  console.log('Insurance clicked')
}

// Modal handlers
const showAuthModalHandler = (mode = 'login') => {
  authModalMode.value = mode
  showAuthModal.value = true
}

const closeAuthModal = () => {
  showAuthModal.value = false
}

const handleAuthenticated = (user) => {
  console.log('User authenticated:', user)
  // Modal will close automatically
}

const getContactPhone = () => {
  // Extract phone from contact_info
  if (props.trip.contact_info) {
    const phoneMatch = props.trip.contact_info.match(/\+?1?\s*\(?[0-9]{3}\)?[-.\s]*[0-9]{3}[-.\s]*[0-9]{4}/)
    return phoneMatch ? phoneMatch[0] : ''
  }
  return ''
}

const getContactEmail = () => {
  // Extract email from contact_info
  if (props.trip.contact_info) {
    const emailMatch = props.trip.contact_info.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/)
    return emailMatch ? emailMatch[0] : ''
  }
  return ''
}

// Initialize itinerary expanded state
onMounted(() => {
  if (props.trip.itinerary) {
    props.trip.itinerary.forEach((day, index) => {
      if (day.expanded === undefined) {
        day.expanded = index === 0 // First day expanded by default
      }
    })
  }
})
</script>

<style scoped>
@import '@/shared/styles/trip-template.css';

/* Customer Authentication Styles */
.customer-menu {
  display: flex;
  align-items: center;
  gap: 16px;
}

.customer-greeting {
  color: #333;
  font-weight: 500;
  font-size: 14px;
}

.account-btn {
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
  font-weight: 500;
  transition: background-color 0.2s;
}

.account-btn:hover {
  background: #357abd;
}

.account-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
  padding: 20px;
}

.account-modal {
  background: white;
  border-radius: 12px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.close-account-modal {
  position: absolute;
  top: 20px;
  right: 20px;
  background: #f5f5f5;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  color: #666;
  transition: background-color 0.2s;
  z-index: 10;
}

.close-account-modal:hover {
  background: #e9ecef;
}

@media (max-width: 768px) {
  .customer-menu {
    flex-direction: column;
    gap: 8px;
    align-items: flex-end;
  }
  
  .customer-greeting {
    font-size: 12px;
  }
  
  .account-btn {
    padding: 6px 12px;
    font-size: 12px;
  }
  
  .account-modal {
    margin: 10px;
    max-height: calc(100vh - 20px);
  }
}
</style>
