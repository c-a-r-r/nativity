<!-- src/components/AppSidebar.vue -->
<template>
  <aside :class="['nativity-app-sidebar', { open: isOpen }]">
    <ul class="nativity-sidebar-nav">
      <li><router-link to="/"><i class="fa fa-home"></i> <span>Dashboard</span></router-link></li>
      <li><router-link to="/quotes"><i class="fa-solid fa-file-invoice-dollar"></i> <span>Quotes</span></router-link></li>
      <li><router-link to="/marketing"><i class="fas fa-bullhorn"></i> <span>Marketing</span></router-link></li>
      <li><router-link to="/trips"><i class="fa-solid fa-plane"></i> <span>Trips</span></router-link></li>
      <li><router-link to="/contacts"><i class="fas fa-users"></i> <span>Contacts</span></router-link></li>
      <li><router-link to="/task"><i class="fas fa-tasks"></i> <span>Task</span></router-link></li>
      <li><router-link to="/Trackingsheet"><i class="fas fa-clipboard-list"></i> <span>Tracking Sheet</span></router-link></li>
      <li><router-link to="/email"><i class="fas fa-comment-dots"></i> <span>Email</span></router-link></li>
      <li><router-link to="/calendar"><i class="fas fa-calendar-alt"></i> <span>Calendar</span></router-link></li>

        <li class="has-submenu" :class="{ 'submenu-open': financialsOpen }">
        <div @click="toggleFinancials" class="submenu-toggle">
            <i class="fas fa-file-invoice-dollar menu-icon"></i>
            <span>Financials</span>
            <i class="fas fa-chevron-down submenu-arrow" :class="{ rotated: financialsOpen }"></i>
        </div>
        <ul :class="['submenu', { visible: financialsOpen }]" >
            <li v-for="(item, idx) in submenuItems" :key="item.text" :class="{ show: financialsOpen }">
            <router-link :to="item.to"><i :class="item.icon"></i> <span>{{ item.text }}</span></router-link>
            </li>
        </ul>
        </li>

      <li><router-link to="/settings"><i class="fas fa-cogs"></i> <span>Settings</span></router-link></li>
      <li><router-link to="/about"><i class="fas fa-info-circle"></i> <span>About</span></router-link></li>
    </ul>
  </aside>
</template>

<script>
export default {
  props: {
    isOpen: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      financialsOpen: false,
      submenuItems: [
        { to: '/financials/payments', icon: 'fas fa-credit-card', text: 'Payments' },
        { to: '/financials/expenses', icon: 'fas fa-money-check-dollar', text: 'Expenses' },
        { to: '/financials/reports', icon: 'fas fa-chart-column', text: 'Reports' }
      ]
    }
  },
  watch: {
    isOpen(newVal, oldVal) {
      if (!newVal && this.financialsOpen) {
        // Sidebar is closing and submenu is open
        this.financialsOpen = false;
        // Wait for submenu animation to finish (match your CSS transition, e.g. 400ms)
        setTimeout(() => {
          this.$emit('close-sidebar'); // Or call your parent method to actually close sidebar
        }, 400);
      }
    }
  },
  methods: {
    toggleFinancials() {
      this.financialsOpen = !this.financialsOpen;
    }
  }
}
</script>

<style scoped>
.default-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.layout-body {
  display: flex;
  flex: 1;
}

.app-content {
  flex: 1;
  padding: 20px;
  background-color: #f9f9f9; /* gives it a light base */
}
.submenu-toggle:hover {
  cursor: pointer;
}
.submenu-toggle {
  position: relative;
  z-index: 1;
}
.submenu.visible {
   
  z-index: 1 !important;
}

</style>

