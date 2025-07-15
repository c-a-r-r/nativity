<!-- filepath: /Users/cristian/Documents/nativity-crm/frontend/src/modules/settings/components/SettingsNavigation.vue -->
<template>
  <div class="settings-nav">
    <ul class="nav nav-pills flex-column">
      <!-- ... existing nav items -->
      
      <li class="nav-item">
        <router-link 
          to="/settings/trip-templates" 
          class="nav-link"
          active-class="active"
        >
          <i class="fas fa-map me-2"></i>
          Trip Templates
        </router-link>
      </li>
      
      <!-- ... other nav items -->
    </ul>
  </div>
</template>