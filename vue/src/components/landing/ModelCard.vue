<template>
  <div class="glass-panel p-8 rounded-3xl group cursor-pointer hover:border-neural-indigo/50 transition-all">
    <div class="flex justify-between items-start mb-12">
      <div class="w-16 h-16 rounded-2xl overflow-hidden bg-black/40 p-2 flex items-center justify-center">
        <img :alt="model.name" :src="model.logo" class="w-full h-full object-contain" />
      </div>
      <span class="px-4 py-1 rounded-full bg-accent-emerald/10 text-accent-emerald font-mono-metrics text-xs">ACTIVE</span>
    </div>
    <h3 class="font-h3 text-h3 mb-2">{{ model.name }}</h3>
    <p class="font-body-md text-body-md text-on-tertiary-container mb-6">{{ model.description }}</p>
    <div class="flex items-center gap-2 text-neural-indigo font-label-caps text-label-caps">
      Explore capabilities <span class="material-symbols-outlined text-sm">arrow_forward</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  model: { type: Object, required: true },
})
</script>

<style scoped>
/* Styles handled by Tailwind */
</style>