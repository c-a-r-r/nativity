<template>
  <div class="border p-3 rounded bg-light">
    <div class="row mb-2">
      <div class="col-6"><strong>Additional City</strong></div>
      <div class="col-6"><strong>Additional Cost</strong></div>
    </div>

    <MultiCityRow
      v-for="(_, i) in rows"
      :key="i"
      v-model:cityId="rows[i].cityId"
      v-model:cost="rows[i].cost"
    />
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import MultiCityRow from './MultiCityRow.vue'

const model = defineModel()   // Expect array length 9

const rows = reactive(
  model.value?.length === 9
    ? model.value
    : Array.from({ length: 9 }, (_, i) => model.value?.[i] || { cityId:'', cost:'' })
)

watch(rows, () => { model.value = rows }, { deep:true })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

* {
  font-size: 14px;
  font-weight: 400;
  font-family: 'Roboto', "Montserrat", sans-serif;
}

h3 {
  font-size: 25px;
  font-weight: 500;
  font-family: 'Roboto', "Montserrat", sans-serif;
}

</style>