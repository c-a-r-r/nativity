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
<!-- MyComponent.vue (or .jsx/.svelte – anywhere that supports <style scoped>) -->
<style scoped>
/* ---------------------------------------------------------------------------
   1.  Load the font once
--------------------------------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

/* ---------------------------------------------------------------------------
   2.  Base-typography variables
--------------------------------------------------------------------------- */
:root {
  --base-font-family: 'Roboto', 'Montserrat', sans-serif;
  --base-font-size  : 14px;
  --base-font-weight: 400;
}

/* Put this class on the outer-most element of the component
   <div class="typography-root"> … </div>                                   */
.typography-root {
  font: var(--base-font-weight) var(--base-font-size)/1.5 var(--base-font-family);
}

/* Every child now *inherits* from .typography-root, so we don’t have to
   use the heavy universal selector (*) any more.                           */

/* ---------------------------------------------------------------------------
   3.  Preserve Font Awesome icons
--------------------------------------------------------------------------- */
.fa, .fas, .far, .fal, .fad, .fab,
[class^="fa-"], [class*=" fa-"] {
  font-family:
    "Font Awesome 6 Free",
    "Font Awesome 6 Pro",
    "Font Awesome 6 Brands",
    "Font Awesome 5 Free",
    "Font Awesome 5 Pro",
    "FontAwesome" !important;
  font-weight: 900;          /* solid style icons need this */
}

/* ---------------------------------------------------------------------------
   4.  Make form controls & buttons inherit the typography
--------------------------------------------------------------------------- */
button, input, textarea, select {
  font: inherit;
}

/* ---------------------------------------------------------------------------
   5.  Component-specific helpers
--------------------------------------------------------------------------- */
.trip-card         { background-color: #f8f9fa; }

.existing-trips {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1rem;
  background-color: #fff;
}

.marketing-section {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.25rem;
  background-color: #f8f9fa;
  margin-bottom: 1.25rem;
}
</style>