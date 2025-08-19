<template>
  <div class="trip-waiting-list">
    <div class="section-header">
      <h3>
        <i class="fas fa-clock"></i>
        Waiting List Management
      </h3>
    </div>

    <div class="waiting-list-content">
      <p>Waiting list component - integrates with passengers_waitinglist.php functionality</p>
      <p>Trip ID: {{ tripId }}</p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  tripId: [String, Number]
})

const emit = defineEmits(['update-stats'])
</script>

<style scoped>
.trip-waiting-list { padding: 30px; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 2px solid #f8f9fa; }
.section-header h3 { margin: 0; color: #2c3e50; display: flex; align-items: center; gap: 10px; }
.section-header i { color: #667eea; }
.waiting-list-content { padding: 40px; text-align: center; background: #f8f9fa; border-radius: 12px; }
</style>
