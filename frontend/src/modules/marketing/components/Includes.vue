<script setup>
/**
 * Props
 *  inc   : string[]  – “Trip includes”
 *  ninc  : string[]  – “Trip does NOT include”
 */
defineProps({ inc: Array, ninc: Array })
</script>

<template>
  <section class="my-5">
    <div class="container">
      <div class="row g-4">
        <!-- INCLUDES -->
        <div class="col-md-6">
          <div class="border rounded h-100 p-4">
            <h4 class="mb-3 text-success fw-bold">
              <i class="fa fa-check-circle me-2"></i> Your Trip Includes
            </h4>

            <ul class="list-unstyled lh-lg mb-0">
              <li v-for="(item, idx) in inc" :key="idx">
                <i class="fa fa-check text-success me-2"></i>{{ item }}
              </li>
            </ul>
          </div>
        </div>

        <!-- NOT INCLUDES -->
        <div class="col-md-6">
          <div class="border rounded h-100 p-4">
            <h4 class="mb-3 text-danger fw-bold">
              <i class="fa fa-times-circle me-2"></i> Not Included
            </h4>

            <ul class="list-unstyled lh-lg mb-0">
              <li v-for="(item, idx) in ninc" :key="idx">
                <i class="fa fa-times text-danger me-2"></i>{{ item }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>