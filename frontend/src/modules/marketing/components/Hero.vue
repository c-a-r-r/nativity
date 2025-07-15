<script setup>
defineProps({ heading: String, sub: String })
</script>

<template>
  <header class="hero py-5 text-white text-center">
    <div class="container">
      <h1 class="display-4">{{ heading }}</h1>
      <p class="lead">{{ sub }}</p>
    </div>
  </header>
</template>

<style scoped>
.hero {
  background:url('/hero-default.jpg') center/cover no-repeat;
}
</style>