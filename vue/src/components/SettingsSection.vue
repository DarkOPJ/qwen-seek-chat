<template>
  <div class="mb-10">
    <div class="flex items-center gap-3 mb-6">
      <div class="w-10 h-10 rounded-lg flex items-center justify-center" :class="iconBg">
        <span class="material-symbols-outlined" :class="iconColor">{{ props.icon }}</span>
      </div>
      <h2 class="font-h3 text-h3 text-white">{{ props.title }}</h2>
    </div>
    <div class="glass-card rounded-2xl p-6" :class="variantClasses">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  icon: { type: String, required: true },
  variant: { type: String, default: 'default' }, // 'default' | 'danger'
})

const iconBg = computed(() => 
  props.variant === 'danger' ? 'bg-neural-rose/20' : 'bg-white/5'
)

const iconColor = computed(() => 
  props.variant === 'danger' ? 'text-neural-rose' : 'text-white'
)

const variantClasses = computed(() => 
  props.variant === 'danger' ? 'border-neural-rose/30' : 'border-white/10'
)
</script>

<style scoped>
</style>