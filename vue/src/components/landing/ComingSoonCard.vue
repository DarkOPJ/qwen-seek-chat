<template>
  <div class="glass-panel p-6 rounded-2xl text-center flex flex-col items-center group cursor-not-allowed">
    <img :alt="model.name" :src="model.logo" class="w-12 h-12 mb-4 object-contain opacity-70" />
    <span class="font-mono-metrics text-[10px] text-white/40 mb-1">{{ model.name }}</span>
    <span class="font-label-caps text-[10px] text-on-tertiary-container">COMING SOON</span>
  </div>
</template>

<script setup>
defineProps({
  model: { type: Object, required: true },
})
</script>