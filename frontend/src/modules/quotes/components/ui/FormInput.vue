<template>
  <div class="col-md-4">
    <label class="form-label">{{ label }}</label>
    <input
      :value="modelValue"
      class="form-control"
      :readonly="readonly"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<script setup>
defineProps({
  label:      String,
  modelValue: [String, Number],
  readonly:   Boolean
})
defineEmits(['update:modelValue'])
</script>