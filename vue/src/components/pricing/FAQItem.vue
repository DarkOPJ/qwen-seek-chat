<template>
  <div class="faq-item glass-panel rounded-lg px-6 py-4 cursor-pointer select-none" @click="toggle">
    <div class="flex justify-between items-center">
      <h4 class="font-body-lg text-body-lg font-semibold">{{ question }}</h4>
      <span class="material-symbols-outlined text-white/50 transition-transform duration-300" :class="{ 'rotate-180': isOpen }">expand_more</span>
    </div>
    <div class="overflow-hidden transition-all duration-300" :style="answerStyle">
      <p class="font-body-md text-body-md text-white/70 pt-4">{{ answer }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  question: String,
  answer: String,
})

const isOpen = ref(false)

const answerStyle = computed(() => ({
  maxHeight: isOpen.value ? '500px' : '0',
  opacity: isOpen.value ? '1' : '0',
}))

const toggle = () => {
  isOpen.value = !isOpen.value
}
</script>

<style scoped>
.rotate-180 {
  transform: rotate(180deg);
}
</style>