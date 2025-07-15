<script setup>
defineProps({
  page:  Number,
  total: Number,
  makeQuery: Function   // callback from the parent
})
</script>

<template>
  <nav>
    <ul class="pagination pagination-sm mb-0">
      <!-- previous -->
      <li class="page-item" :class="{ disabled: page === 1 }">
        <router-link
          class="page-link"
          :to="makeQuery({ page: page - 1 })"
          tabindex="-1">
          Previous
        </router-link>
      </li>

      <!-- page x / y -->
      <li class="page-item disabled">
        <span class="page-link">Page {{ page }} / {{ total }}</span>
      </li>

      <!-- next -->
      <li class="page-item" :class="{ disabled: page === total }">
        <router-link
          class="page-link"
          :to="makeQuery({ page: page + 1 })">
          Next
        </router-link>
      </li>
    </ul>
  </nav>
</template>