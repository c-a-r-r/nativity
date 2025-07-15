<template>
  <select class="form-select" v-model="cityId" @change="emitBoth">
    <option value="">-- Select City --</option>
    <option v-for="c in cities" :key="c.id" :value="c.id">
      {{ c.short_display }}
    </option>
  </select>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import quoteApi from '@/modules/quotes/api/quotes.api'

const cityId = defineModel()            // v-model binding
const emit   = defineEmits(['update:cost'])

const cities = ref([])
onMounted(async () => {
  cities.value = await quoteApi.getCities()
  emitBoth()
})

function emitBoth () {
  const city = cities.value.find(c => c.id == cityId.value)
  emit('update:cost', city ? city.cost : 0)
}

onMounted(async () => {
  try {
    cities.value = await quoteApi.getCities()
  } catch (err) {
    if (err.response?.status === 401) {
      // optional: global event bus / pinia store -> redirect to login
      return
    }
    console.error(err)
  }
})
</script>