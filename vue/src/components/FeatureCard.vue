<template>
  <div class="glass-panel p-8 rounded-3xl hover:bg-white/5 transition-all">
    <div class="w-12 h-12 rounded-full :bg-color/20 flex items-center justify-center mb-8" :class="bgColorClass">
      <span class="material-symbols-outlined :text-color" :class="textColorClass">{{ feature.icon }}</span>
    </div>
    <h4 class="font-h3 text-xl mb-4 text-white">{{ feature.title }}</h4>
    <p class="font-body-md text-body-md text-white/60">{{ feature.desc }}</p>
  </div>
</template>

<script setup>
defineProps({
  feature: {
    type: Object,
    required: true,
  },
})

const bgColorClass = `bg-${props.feature.color}/20`
const textColorClass = `text-${props.feature.color}`
</script>

<style scoped>
/* Scoped styles if needed */
</style>