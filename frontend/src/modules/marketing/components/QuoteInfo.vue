<script setup>
defineProps({ start: String, end: String, price: [String,Number], city: String })
</script>

<template>
  <section class="quote-info py-4 border my-4">
    <div class="container text-center">
      <strong>Trip dates:</strong> {{ start }} – {{ end }} •
      <strong>Cost:</strong> ${{ price }} (dbl occ.) •
      <strong>Departure city:</strong> {{ city }}
    </div>
  </section>
</template>