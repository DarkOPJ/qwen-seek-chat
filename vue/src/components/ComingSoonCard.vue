<template>
  <div class="glass-panel p-6 rounded-2xl text-center flex flex-col items-center group cursor-not-allowed">
    <div class="w-12 h-12 mb-4 flex items-center justify-center bg-gradient-to-br from-zinc-800 to-zinc-900 rounded-xl">
      <span class="font-bold text-white text-lg opacity-70">{{ model.initials }}</span>
    </div>
    <span class="font-mono-metrics text-[10px] text-white/40 mb-1">{{ model.name }}</span>
    <span class="font-label-caps text-[10px] text-on-tertiary-container">COMING SOON</span>
  </div>
</template>

<script setup>
defineProps({
  model: {
    type: Object,
    required: true,
  },
})
</script>

<style scoped>
</style>