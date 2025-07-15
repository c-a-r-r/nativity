<script setup>
import { ref } from "vue"

/**
 * Props
 *  days      : string[]            – Headlines (“DAY 1 – Arrive …”)
 *  copy      : string[]            – Paragraph(s) for each day (same index)
 *  galleries : string[][] (array of arrays) – URLs for each day
 */
const props = defineProps({
  days: Array,
  copy: Array,
  galleries: Array,
})

const active = ref(0)
</script>

<template>
  <section class="my-5">
    <div class="container">

      <h2 class="mb-4 fw-bold text-center">Daily Itinerary</h2>

      <!-- day tabs -->
      <ul class="nav nav-tabs overflow-auto flex-nowrap mb-3">
        <li class="nav-item" v-for="(d, i) in props.days" :key="i">
          <button
            class="nav-link"
            :class="{ active: active === i }"
            @click="active = i"
          >
            {{ d || `Day ${i + 1}` }}
          </button>
        </li>
      </ul>

      <!-- active day content -->
      <div class="p-4 border rounded">
        <h4 class="fw-bold mb-3">{{ props.days[active] }}</h4>
        <p class="mb-4" style="white-space: pre-line">
          {{ props.copy[active] }}
        </p>

        <!-- gallery -->
        <div
          class="row g-3"
          v-if="props.galleries && props.galleries[active]?.length"
        >
          <div
            v-for="(url, k) in props.galleries[active]"
            :key="k"
            class="col-6 col-md-4 col-lg-3"
          >
            <img
              :src="url"
              class="img-fluid rounded"
              :alt="`Day ${active + 1} image ${k + 1}`"
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Optional: keep tabs on a single line on mobile */
.nav-tabs::-webkit-scrollbar {
  display: none;
}
</style>