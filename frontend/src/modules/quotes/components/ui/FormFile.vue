<template>
  <div class="col-md-4">
    <label class="form-label">{{ label }}</label>
    <input
      type="file"
      class="form-control"
      @change="$emit('update:modelValue', $event.target.files[0])"
    />
  </div>
</template>

<script setup>
defineProps({ label:String })
defineEmits(['update:modelValue'])
</script>