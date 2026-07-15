<template>
  <div class="relative overflow-hidden py-4">
    <div 
      class="flex animate-marquee whitespace-nowrap gap-24 items-center w-max" 
      :style="{ animationDuration: duration + 's' }"
    >
      <div class="flex shrink-0 items-center gap-24 transition-all duration-500">
        <div 
          v-for="item in items" 
          :key="item.name" 
          class="flex-shrink-0"
        >
          <img 
            :src="item.src" 
            :alt="item.name" 
            class="h-8 w-auto object-contain" 
          />
        </div>
      </div>
      <div class="flex shrink-0 items-center gap-24 transition-all duration-500">
        <div 
          v-for="item in items" 
          :key="item.name + '-copy'" 
          class="flex-shrink-0"
        >
          <img 
            :src="item.src" 
            :alt="item.name" 
            class="h-8 w-auto object-contain" 
          />
        </div>
      </div>
    </div>
    <div v-if="showFadeLeft" class="absolute inset-y-0 left-0 w-32 bg-gradient-to-r from-black to-transparent z-10 pointer-events-none" />
    <div v-if="showFadeRight" class="absolute inset-y-0 right-0 w-32 bg-gradient-to-l from-black to-transparent z-10 pointer-events-none" />
  </div>
</template>

<script setup>
defineProps({
  className: { type: String, default: '' },
  showFadeLeft: { type: Boolean, default: true },
  showFadeRight: { type: Boolean, default: true },
  duration: { type: Number, default: 40 },
  gap: { type: Number, default: 24 },
  items: { type: Array, required: true },
  itemHeight: { type: Number, default: 32 },
  paused: { type: Boolean, default: false },
})
</script>

<style scoped>
@keyframes marquee-scroll {
  0% { transform: translateX(-50%); }
  100% { transform: translateX(0%); }
}

.animate-marquee {
  animation: marquee-scroll linear infinite;
  will-change: transform;
}
</style>