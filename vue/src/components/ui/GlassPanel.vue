<template>
  <div :class="['glass-panel', variant, className]">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  variant: { type: String, default: 'default' }, // default, dark, card, input
  className: { type: String, default: '' },
})
</script>

<style scoped>
.glass-panel {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.05);
}

.glass-panel.dark {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.glass-panel.card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.glass-panel.input {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
}

.glass-panel:hover {
  background: rgba(255, 255, 255, 0.05);
}
</style>