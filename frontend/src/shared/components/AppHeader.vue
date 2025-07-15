<!-- src/components/AppHeader.vue -->
<template>
  <header class="app-header">
    <button class="sidebar-toggle" @click="$emit('toggleSidebar')" aria-label="Toggle sidebar">☰</button>
    <div class="app-title">VIZITOR</div>

   <div
    class="user-profile">
    <button class="user-avatar" @click="toggleDropdown" aria-label="User profile menu">
        <i class="fas fa-user"></i>
    </button>
       <ul v-show="dropdownVisible" :class="['user-dropdown', { visible: dropdownVisible }]">
        <li><a href="#">Profile</a></li>
        <li><a href="#">Change Password</a></li>
        <li><a href="#" @click.prevent="logout">Logout</a></li>
        </ul>
    </div>
  </header>
</template>

<script>
export default {
  data() {
    return {
      dropdownVisible: false
    }
  },
  methods: {
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible
      if (this.dropdownVisible) {
        document.addEventListener('click', this.handleClickOutside)
      } else {
        document.removeEventListener('click', this.handleClickOutside)
      }
    },
    handleClickOutside(event) {
      // Check if the click was outside the user-profile div
      if (!this.$el.querySelector('.user-profile').contains(event.target)) {
        this.dropdownVisible = false
        document.removeEventListener('click', this.handleClickOutside)
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  }
}
</script>

<style scoped>
/* You can fine-tune this or import from dashboard.css */
</style>
