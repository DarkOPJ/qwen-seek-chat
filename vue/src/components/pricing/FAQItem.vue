<template>
  <div class="faq-item glass-panel rounded-lg px-6 py-4 cursor-pointer" @click="toggle">
    <div class="flex justify-between items-center">
      <h4 class="font-body-lg text-body-lg font-semibold">{{ question }}</h4>
      <span class="material-symbols-outlined faq-icon transition-transform duration-300" :class="{ 'rotate-180': isOpen }">expand_more</span>
    </div>
    <div class="faq-content" :class="{ active: isOpen }">
      <p class="font-body-md text-body-md text-white/70">{{ answer }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  question: String,
  answer: String,
})

const isOpen = ref(false)

const toggle = () => {
  isOpen.value = !isOpen.value
}
</script>

<style scoped>
.faq-content {
  transition: max-height 0.3s ease-in-out, opacity 0.3s ease-in-out;
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}

.faq-item.active .faq-content {
  max-height: 200px;
  opacity: 1;
  padding-top: 16px;
}

.faq-icon {
  transition: transform 0.3s ease;
}

.faq-icon.rotate-180 {
  transform: rotate(180deg);
}
</style>