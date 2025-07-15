<template>
<!-- Itinerary details – two rows --------------------------------------- -->
<h3 class="mb-3">Itinerary Details</h3>

<!-- Row 1: Dates -->
<div class="row g-3 mb-3">
  <!-- departure date -->
  <div class="col-md-4">
    <label class="form-label">Departure Date</label>
    <div class="position-relative">
      <input
        type="date"
        class="form-control custom-date-input"
        v-model="form.departure_date"
      >
      <i class="fa-regular fa-calendar-days custom-calendar-icon" aria-hidden="true"></i>
    </div>
  </div>

  <!-- arrival date -->
  <div class="col-md-4">
    <label class="form-label">Arrival Date</label>
    <div class="position-relative">
      <input
        type="date"
        class="form-control custom-date-input"
        v-model="form.arrival_date"
      >
      <i class="fa-regular fa-calendar-days custom-calendar-icon" aria-hidden="true"></i>
    </div>
  </div>
</div>

<!-- Row 2: Destinations -->
<div class="row g-3 mb-3">
  <!-- destination group -->
  <div class="col-md-4">
    <label class="form-label">Destination Group</label>
    <select
      v-model="form.destination_group"
      class="form-select"
    >
      <option value="">Select Group</option>
      <option
        v-for="g in groups"
        :key="g.id"
        :value="g.id"
      >
        {{ g.nombre }}
      </option>
    </select>
  </div>

  <!-- destination -->
  <div class="col-md-4">
    <label class="form-label">Destination</label>
    <select
      v-model="form.itinerary_id"
      class="form-select"
    >
      <option value="">Select Destination</option>
      <option
        v-for="d in destinations"
        :key="d.id"
        :value="d.id"
      >
        {{ d.nombre }}
      </option>
    </select>
  </div>
</div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import quoteApi from '@/modules/quotes/api/quotes.api'

const form = defineModel()

const groups       = ref([])
const destinations = ref([])

onMounted(async () => {
  groups.value       = await quoteApi.getDestGroups()
  destinations.value = await quoteApi.getDestinations()
})

watch(() => form.value.destination_group, id => {
  const g = groups.value.find(g => g.id === id)
  if (g) form.value.trip_name = g.nombre
})
</script>
<style scoped>
/* Hide the default calendar icon */
.custom-date-input::-webkit-calendar-picker-indicator {
  opacity: 0;
  position: absolute;
  right: 0;
  width: 20px;
  height: 20px;
  cursor: pointer;
}

/* Style for custom calendar icon */
.custom-calendar-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #42406f;
  pointer-events: none;
  font-size: 18px;
}

/* Ensure the input container is positioned relative */
.position-relative {
  position: relative;
}
</style>