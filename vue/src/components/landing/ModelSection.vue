<template>
  <section class="py-[180px] md:py-[180px] px-[32px] max-w-[1280px] mx-auto" :class="{ 'opacity-100 translate-y-0': isLoaded, 'opacity-0 translate-y-10': !isLoaded }" style="transition: all 1s ease 0.2s;">
    <div class="text-center mb-24">
      <h2 class="font-h2 text-h2 mb-6">Engineered for Choice</h2>
      <p class="font-body-lg text-body-lg text-on-tertiary-container max-w-2xl mx-auto">
        Switch between top-tier foundation models instantly. No setup, no latency, just pure intelligence.
      </p>
    </div>

    <!-- Active Models -->
    <div class="grid md:grid-cols-2 gap-8 mb-16">
      <ModelCard v-for="model in activeModels" :key="model.id" :model="model" />
    </div>

    <!-- Coming Soon Grid -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
      <ComingSoonCard v-for="model in comingSoonModels" :key="model.id" :model="model" />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ModelCard from './ModelCard.vue'
import ComingSoonCard from './ComingSoonCard.vue'

const isLoaded = ref(false)

onMounted(() => {
  requestAnimationFrame(() => {
    isLoaded.value = true
  })
})

const activeModels = [
  {
    id: 'deepseek',
    name: 'DeepSeek-V4',
    logo: '/assets/deepseek.png',
    description: 'Unrivaled efficiency in code generation and complex mathematical reasoning.',
    color: 'neural-indigo',
  },
  {
    id: 'qwen',
    name: 'Qwen3.7-Max',
    logo: '/assets/qwen.png',
    description: 'State-of-the-art linguistic versatility with extreme context window support.',
    color: 'neural-purple',
  },
]

const comingSoonModels = [
  { id: 'mistral', name: 'MISTRAL', logo: '/assets/mistral.png' },
  { id: 'gemma', name: 'GEMMA', logo: '/assets/gemma.png' },
  { id: 'gpt-oss', name: 'GPT-OSS', logo: '/assets/gpt-oss.png' },
  { id: 'glm', name: 'GLM', logo: '/assets/glm.png' },
  { id: 'kimi', name: 'KIMI', logo: '/assets/kimi.png' },
  { id: 'minimax', name: 'MINIMAX', logo: '/assets/minimax.png' },
]
</script>