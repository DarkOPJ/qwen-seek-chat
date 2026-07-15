<template>
  <div class="glass-panel p-8 rounded-3xl hover:bg-white/5 transition-all">
    <div class="w-12 h-12 rounded-full flex items-center justify-center mb-8" :class="iconBg">
      <span class="material-symbols-outlined" :class="iconColor">{{ icon }}</span>
    </div>
    <h4 class="font-h3 text-xl mb-4 text-white">{{ title }}</h4>
    <p class="font-body-md text-body-md text-white/60">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  description: { type: String, required: true },
  icon: { type: String, required: true },
  iconBg: { type: String, required: true },
  iconColor: { type: String, required: true },
})
</script>