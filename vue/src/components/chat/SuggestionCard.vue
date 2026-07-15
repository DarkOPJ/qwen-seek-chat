<template>
  <button 
    class="p-6 rounded-2xl glass-dark hover:bg-white/[0.08] transition-all text-left group"
    @click="$emit('click', prompt)"
  >
    <span class="material-symbols-outlined mb-3" :class="iconColor">{{ prompt.icon }}</span>
    <h4 class="font-bold text-sm mb-1 text-white group-hover:text-neural-indigo transition-colors">{{ prompt.title }}</h4>
    <p class="text-xs text-on-tertiary-container leading-relaxed">{{ prompt.desc }}</p>
  </button>
</template>

<script setup>
const props = defineProps({
  prompt: Object
})

const emit = defineEmits(['click'])

const iconColor = computed(() => {
  const colors = {
    code: 'text-neural-indigo',
    schema: 'text-accent-emerald',
    terminal: 'text-neural-purple',
    auto_awesome: 'text-neural-rose'
  }
  return colors[props.prompt.icon] || 'text-neural-indigo'
})
</script>

<style scoped>
/* Scoped styles if needed */
</style>