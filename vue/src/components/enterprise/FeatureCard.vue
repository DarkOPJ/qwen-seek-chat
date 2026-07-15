<template>
  <div :class="['feature-card', variantClass, glowClass, borderClass]">
    <div class="icon-wrapper" :class="iconWrapperClass">
      <span class="material-symbols-outlined" :class="iconColorClass" style="font-variation-settings: 'FILL' 1;">{{ icon }}</span>
    </div>
    <h3 class="font-h3 text-h3 mb-4 text-primary">{{ title }}</h3>
    <p class="text-secondary font-body-md text-body-md leading-relaxed">{{ description }}</p>
    <ul v-if="features && features.length" class="mt-8 space-y-3">
      <li v-for="feature in features" :key="feature.text" class="flex items-center gap-3 text-secondary text-label-caps">
        <span class="material-symbols-outlined text-sm" :class="feature.color">{{ feature.icon }}</span>
        {{ feature.text }}
      </li>
    </ul>
    <div v-if="badges && badges.length" class="mt-8 flex flex-wrap gap-2">
      <span v-for="badge in badges" :key="badge" class="px-3 py-1 rounded bg-white/5 text-[10px] font-mono-metrics text-secondary uppercase border border-white/10 tracking-widest">{{ badge }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

defineProps({
  icon: { type: String, required: true },
  iconColor: { type: String, default: 'neural-indigo' },
  iconBg: { type: String, default: 'neural-indigo/10' },
  borderColor: { type: String, default: 'white/20' },
  title: { type: String, required: true },
  description: { type: String, required: true },
  features: { type: Array, default: () => [] },
  badges: { type: Array, default: () => [] },
  variant: { type: String, default: 'default' }, // default, accent-glow
  isHighlighted: { type: Boolean, default: false },
})

const variantClass = computed(() => {
  if (isHighlighted) return 'border-white/20 relative overflow-hidden'
  return ''
})

const glowClass = computed(() => {
  if (isHighlighted) return 'absolute -top-24 -right-24 w-48 h-48 bg-accent-emerald/10 blur-[60px]'
  return ''
})

const borderClass = computed(() => `border-${borderColor}`)

const iconWrapperClass = computed(() => {
  const base = 'w-14 h-14 rounded-lg flex items-center justify-center mb-8 border'
  return `${base} bg-${iconBg} border-${iconColor}/20`
})

const iconColorClass = computed(() => `text-${iconColor}`)
</script>

<style scoped>
.feature-card {
  padding: 2.5rem;
  border-radius: 0.75rem;
  transition: all;
}

.icon-wrapper {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
  border-width: 1px;
}
</style>