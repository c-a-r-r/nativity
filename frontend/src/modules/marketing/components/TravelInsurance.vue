<script setup>
/**
 * Props
 *  copy : string  – arbitrary HTML / Markdown string
 */
defineProps({ copy: String })
</script>

<template>
  <section class="my-5 py-5 bg-light border-top">
    <div class="container text-center">
      <h2 class="fw-bold mb-4">Travel Insurance</h2>

      <!-- Content may come with line-breaks or basic markup -->
      <div class="mx-auto text-start" style="max-width: 680px">
        <p style="white-space: pre-line" v-html="copy"></p>
      </div>

      <a
        class="btn btn-primary mt-4"
        href="https://nativitypilgrimage.com/insurance"
        target="_blank"
        rel="noopener"
      >
        Travel Insurance Link
      </a>
    </div>
  </section>
</template>