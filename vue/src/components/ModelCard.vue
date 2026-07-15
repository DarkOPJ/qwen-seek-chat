<template>
  <div class="glass-panel p-8 rounded-3xl group cursor-pointer transition-all" :class="hoverClass">
    <div class="flex justify-between items-start mb-12">
      <div class="w-16 h-16 rounded-2xl overflow-hidden bg-black/40 p-2 flex items-center justify-center">
        <img :alt="model.name" :src="model.logo" class="w-full h-full object-contain" />
      </div>
      <span class="px-4 py-1 rounded-full" :class="`bg-${model.badgeColor}/10 text-${model.badgeColor} font-mono-metrics text-xs`">{{ model.badge }}</span>
    </div>
    <h3 class="font-h3 text-h3 mb-2">{{ model.name }}</h3>
    <p class="font-body-md text-body-md text-on-tertiary-container mb-6">{{ model.description }}</p>
    <div class="flex items-center gap-2" :class="`text-${model.accentColor} font-label-caps text-label-caps`">
      Explore capabilities <span class="material-symbols-outlined text-sm">arrow_forward</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  model: {
    type: Object,
    required: true,
  },
})

defineEmits(['select'])

const hoverClass = 'hover:border-neural-indigo/50'
</script>

<style scoped>
</style>