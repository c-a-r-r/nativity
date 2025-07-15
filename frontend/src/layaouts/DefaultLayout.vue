<!-- src/layouts/DefaultLayout.vue -->
<template>
  <div class="default-layout">
    <AppHeader @toggleSidebar="sidebarOpen = !sidebarOpen" />
    <div class="layout-body">
      <AppSidebar :isOpen="sidebarOpen" />
      <main class="app-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import AppHeader from '@/shared/components/AppHeader.vue'
import AppSidebar from '@/shared/components/AppSidebar.vue'

export default {
  components: {
    AppHeader,
    AppSidebar
  },
  data() {
    return {
      sidebarOpen: true
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

/* Add this: */
.app-content {
  flex: 1 1 0;
  min-width: 0;
  /* Optional: remove padding if you want edge-to-edge */
  /* padding: 0; */
}
</style>
