<template>
  <div class="row g-2 mb-2">
    <div class="col-md-6">
      <select v-model="cityId" class="form-select">
        <option value="">-- Select City --</option>
        <option v-for="c in cities" :key="c.id" :value="c.id">
          {{ c.short_display }}
        </option>
      </select>
    </div>
    <div class="col-md-6">
      <input 
        type="number" 
        v-model="cost" 
        class="form-control" 
        placeholder="Additional Cost"
        step="0.01"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import quoteApi from '@/modules/quotes/api/quotes.api'

const cityId = defineModel('cityId')
const cost   = defineModel('cost')

const cities = ref([])
onMounted(async () => {
  cities.value = await quoteApi.getCities()
})
</script>