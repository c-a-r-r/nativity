<!-- filepath: /Users/cristian/Documents/nativity-crm/frontend/src/modules/settings/pages/SettingsMenuTiles.vue -->
<template>
  <div class="settings-menu-tiles">
    <div class="settings-header mb-4">
      <h2><i class="fas fa-cogs me-3"></i>Settings</h2>
      <p class="text-muted">Manage your application settings and configurations</p>
    </div>

    <div class="row g-4">
      <!-- Trip Templates Tile -->
      <div class="col-md-6 col-lg-4">
        <div class="settings-tile" @click="navigateTo('/settings/trip-templates')">
          <div class="tile-icon">
            <i class="fas fa-map"></i>
          </div>
          <div class="tile-content">
            <h5>Trip Templates</h5>
            <p>Create and manage templates for marketing trips</p>
            <div class="tile-stats">
              <span class="badge bg-primary">{{ templateCount }} Templates</span>
            </div>
          </div>
          <div class="tile-arrow">
            <i class="fas fa-chevron-right"></i>
          </div>
        </div>
      </div>

      <!-- User Management Tile -->
      <div class="col-md-6 col-lg-4">
        <div class="settings-tile" @click="navigateTo('/settings/users')">
          <div class="tile-icon">
            <i class="fas fa-users"></i>
          </div>
          <div class="tile-content">
            <h5>User Management</h5>
            <p>Manage user accounts, roles, and permissions</p>
            <div class="tile-stats">
              <span class="badge bg-success">{{ userCount }} Users</span>
            </div>
          </div>
          <div class="tile-arrow">
            <i class="fas fa-chevron-right"></i>
          </div>
        </div>
      </div>

      <!-- Email Settings Tile -->
      <div class="col-md-6 col-lg-4">
        <div class="settings-tile" @click="navigateTo('/settings/email')">
          <div class="tile-icon">
            <i class="fas fa-envelope"></i>
          </div>
          <div class="tile-content">
            <h5>Email Settings</h5>
            <p>Configure email templates and SMTP settings</p>
            <div class="tile-stats">
              <span class="badge bg-info">SMTP Configured</span>
            </div>
          </div>
          <div class="tile-arrow">
            <i class="fas fa-chevron-right"></i>
          </div>
        </div>
      </div>

      <!-- System Configuration Tile -->
      <div class="col-md-6 col-lg-4">
        <div class="settings-tile" @click="navigateTo('/settings/system')">
          <div class="tile-icon">
            <i class="fas fa-server"></i>
          </div>
          <div class="tile-content">
            <h5>System Configuration</h5>
            <p>General system settings and preferences</p>
            <div class="tile-stats">
              <span class="badge bg-warning">Admin Only</span>
            </div>
          </div>
          <div class="tile-arrow">
            <i class="fas fa-chevron-right"></i>
          </div>
        </div>
      </div>

      <!-- Quote Settings Tile -->
      <div class="col-md-6 col-lg-4">
        <div class="settings-tile" @click="navigateTo('/settings/quotes')">
          <div class="tile-icon">
            <i class="fas fa-file-invoice-dollar"></i>
          </div>
          <div class="tile-content">
            <h5>Quote Settings</h5>
            <p>Configure quote templates and pricing rules</p>
            <div class="tile-stats">
              <span class="badge bg-secondary">Templates</span>
            </div>
          </div>
          <div class="tile-arrow">
            <i class="fas fa-chevron-right"></i>
          </div>
        </div>
      </div>

      <!-- Destinations Management Tile -->
      <div class="col-md-6 col-lg-4">
        <div class="settings-tile" @click="navigateTo('/settings/destinations')">
          <div class="tile-icon">
            <i class="fas fa-globe"></i>
          </div>
          <div class="tile-content">
            <h5>Destinations</h5>
            <p>Manage travel destinations and locations</p>
            <div class="tile-stats">
              <span class="badge bg-primary">{{ destinationCount }} Destinations</span>
            </div>
          </div>
          <div class="tile-arrow">
            <i class="fas fa-chevron-right"></i>
          </div>
        </div>
      </div>

      <!-- Integrations Tile -->
      <div class="col-md-6 col-lg-4">
        <div class="settings-tile" @click="navigateTo('/settings/integrations')">
          <div class="tile-icon">
            <i class="fas fa-plug"></i>
          </div>
          <div class="tile-content">
            <h5>Integrations</h5>
            <p>Connect with third-party services and APIs</p>
            <div class="tile-stats">
              <span class="badge bg-success">3 Connected</span>
            </div>
          </div>
          <div class="tile-arrow">
            <i class="fas fa-chevron-right"></i>
          </div>
        </div>
      </div>

      <!-- Backup & Security Tile -->
      <div class="col-md-6 col-lg-4">
        <div class="settings-tile" @click="navigateTo('/settings/security')">
          <div class="tile-icon">
            <i class="fas fa-shield-alt"></i>
          </div>
          <div class="tile-content">
            <h5>Backup & Security</h5>
            <p>Data backup settings and security configurations</p>
            <div class="tile-stats">
              <span class="badge bg-success">Protected</span>
            </div>
          </div>
          <div class="tile-arrow">
            <i class="fas fa-chevron-right"></i>
          </div>
        </div>
      </div>

      <!-- Reports & Analytics Tile -->
      <div class="col-md-6 col-lg-4">
        <div class="settings-tile" @click="navigateTo('/settings/reports')">
          <div class="tile-icon">
            <i class="fas fa-chart-bar"></i>
          </div>
          <div class="tile-content">
            <h5>Reports & Analytics</h5>
            <p>Configure reporting settings and dashboard metrics</p>
            <div class="tile-stats">
              <span class="badge bg-info">Analytics On</span>
            </div>
          </div>
          <div class="tile-arrow">
            <i class="fas fa-chevron-right"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions Section -->
    <div class="quick-actions mt-5">
      <h4 class="mb-3">Quick Actions</h4>
      <div class="row g-3">
        <div class="col-md-3">
          <button class="btn btn-outline-primary w-100" @click="navigateTo('/settings/trip-templates')">
            <i class="fas fa-plus me-2"></i>
            Create Template
          </button>
        </div>
        <div class="col-md-3">
          <button class="btn btn-outline-success w-100" @click="navigateTo('/settings/users')">
            <i class="fas fa-user-plus me-2"></i>
            Add User
          </button>
        </div>
        <div class="col-md-3">
          <button class="btn btn-outline-info w-100" @click="navigateTo('/settings/destinations')">
            <i class="fas fa-map-marker-alt me-2"></i>
            Add Destination
          </button>
        </div>
        <div class="col-md-3">
          <button class="btn btn-outline-warning w-100" @click="exportSettings">
            <i class="fas fa-download me-2"></i>
            Export Settings
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import http from '@/shared/services/http'

const router = useRouter()

// Reactive data for statistics
const templateCount = ref(0)
const userCount = ref(0)
const destinationCount = ref(0)

// Methods
const navigateTo = (path) => {
  router.push(path)
}

const exportSettings = () => {
  // Implement settings export functionality
  alert('Export settings functionality coming soon!')
}

// Load statistics on mount
const loadStatistics = async () => {
  try {
    // Load template count
    const templatesResponse = await http.get('/api/marketing/templates/')
    templateCount.value = (templatesResponse.data.results || templatesResponse.data).length

    // Load destinations count (if you have this endpoint)
    try {
      const destinationsResponse = await http.get('/api/destinations/')
      destinationCount.value = (destinationsResponse.data.results || destinationsResponse.data).length
    } catch (error) {
      console.log('Destinations endpoint not available')
    }

    // You can add more statistics as needed
    userCount.value = 5 // Placeholder - replace with actual API call

  } catch (error) {
    console.error('Failed to load statistics:', error)
  }
}

onMounted(() => {
  loadStatistics()
})
</script>

<style scoped>
.settings-menu-tiles {
  padding: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.settings-header {
  text-align: center;
  margin-bottom: 2rem;
}

.settings-header h2 {
  color: #2c3e50;
  font-weight: 600;
}

.settings-tile {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid #e9ecef;
  height: 100%;
  display: flex;
  align-items: center;
  gap: 16px;
}

.settings-tile:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

.tile-icon {
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #007bff, #0056b3);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.tile-content {
  flex: 1;
}

.tile-content h5 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-weight: 600;
}

.tile-content p {
  margin: 0 0 12px 0;
  color: #6c757d;
  font-size: 14px;
  line-height: 1.4;
}

.tile-stats {
  margin-top: 8px;
}

.tile-arrow {
  flex-shrink: 0;
  color: #adb5bd;
  font-size: 18px;
  transition: all 0.3s ease;
}

.settings-tile:hover .tile-arrow {
  color: #007bff;
  transform: translateX(4px);
}

.quick-actions {
  border-top: 1px solid #e9ecef;
  padding-top: 2rem;
}

.quick-actions h4 {
  color: #2c3e50;
  font-weight: 600;
}

.btn {
  padding: 12px 20px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-2px);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .settings-menu-tiles {
    padding: 20px 15px;
  }
  
  .settings-tile {
    padding: 20px;
  }
  
  .tile-icon {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .tile-content h5 {
    font-size: 16px;
  }
  
  .tile-content p {
    font-size: 13px;
  }
}

/* Different icon colors for variety */
.settings-tile:nth-child(1) .tile-icon { background: linear-gradient(135deg, #28a745, #1e7e34); }
.settings-tile:nth-child(2) .tile-icon { background: linear-gradient(135deg, #17a2b8, #117a8b); }
.settings-tile:nth-child(3) .tile-icon { background: linear-gradient(135deg, #ffc107, #e0a800); }
.settings-tile:nth-child(4) .tile-icon { background: linear-gradient(135deg, #dc3545, #c82333); }
.settings-tile:nth-child(5) .tile-icon { background: linear-gradient(135deg, #6f42c1, #59359a); }
.settings-tile:nth-child(6) .tile-icon { background: linear-gradient(135deg, #20c997, #1aa179); }
.settings-tile:nth-child(7) .tile-icon { background: linear-gradient(135deg, #fd7e14, #e55a00); }
.settings-tile:nth-child(8) .tile-icon { background: linear-gradient(135deg, #6c757d, #5a6268); }
.settings-tile:nth-child(9) .tile-icon { background: linear-gradient(135deg, #007bff, #0056b3); }
</style>