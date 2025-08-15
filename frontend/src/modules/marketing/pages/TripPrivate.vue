<template>
  <div class="container">
    <h2>Private Trip View</h2>
    <p>This view is under development. Please use the public trip view for now.</p>
    <router-link :to="`/marketing/trips/${$route.params.slug}`" class="btn btn-primary">
      View Public Trip
    </router-link>
  </div>
</template>

<script setup>
// Placeholder component for private trip view
</script>