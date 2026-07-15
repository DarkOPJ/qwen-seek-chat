<template>
  <section class="py-[180px] md:py-[180px] bg-black relative overflow-hidden" :class="{ 'opacity-100 translate-y-0': isLoaded, 'opacity-0 translate-y-10': !isLoaded }" style="transition: all 1s ease 0.4s;">
    <div class="px-[32px] max-w-[1280px] mx-auto" :class="{ 'opacity-100 translate-y-0': isLoaded, 'opacity-0 translate-y-10': !isLoaded }" style="transition: all 1s ease 0.6s;">
      <div class="mb-20">
        <h2 class="font-h3 text-h3 mb-4 text-white">Uncompromising Precision</h2>
        <p class="text-white/70 font-body-md max-w-lg">Advanced tooling for the most demanding technical workloads.</p>
      </div>
      <div class="grid md:grid-cols-3 gap-6">
        <FeatureCard
          v-for="feature in features"
          :key="feature.title"
          :title="feature.title"
          :description="feature.description"
          :icon="feature.icon"
          :iconBg="feature.iconBg"
          :iconColor="feature.iconColor"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import FeatureCard from './FeatureCard.vue'

const isLoaded = ref(false)

onMounted(() => {
  requestAnimationFrame(() => {
    isLoaded.value = true
  })
})

const features = [
  {
    title: 'Advanced Reasoning',
    description: 'Multi-step cognitive chains that solve complex problems with unprecedented accuracy.',
    icon: 'psychology',
    iconBg: 'bg-neural-indigo/20',
    iconColor: 'text-neural-indigo',
  },
  {
    title: 'Real-time Synthesis',
    description: 'Instant integration of live data streams directly into your AI context window.',
    icon: 'dynamic_feed',
    iconBg: 'bg-neural-purple/20',
    iconColor: 'text-neural-purple',
  },
  {
    title: 'Enterprise Security',
    description: 'End-to-end encryption with zero-retention policies for your sensitive IP.',
    icon: 'security',
    iconBg: 'bg-accent-emerald/20',
    iconColor: 'text-accent-emerald',
  },
  {
    title: 'Neural Tuning',
    description: 'Fine-tune model personality and output constraints on the fly with orbital sliders.',
    icon: 'auto_awesome',
    iconBg: 'bg-neural-rose/20',
    iconColor: 'text-neural-rose',
  },
  {
    title: 'Native SDKs',
    description: 'Deeply typed integrations for TypeScript, Python, and Rust workflows.',
    icon: 'api',
    iconBg: 'bg-white/10',
    iconColor: 'text-white',
  },
  {
    title: 'Global Edge',
    description: 'Sub-100ms latency globally powered by our distributed orbital network nodes.',
    icon: 'speed',
    iconBg: 'bg-orange-400/20',
    iconColor: 'text-orange-400',
  },
]
</script>