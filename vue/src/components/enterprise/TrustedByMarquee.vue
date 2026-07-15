<template>
  <section class="py-12 border-y border-white/5 bg-black/20">
    <div class="max-w-[1280px] mx-auto px-[32px]">
      <p class="text-center font-label-caps text-label-caps text-secondary mb-10 opacity-60">POWERING THE NEXT GENERATION OF INTELLIGENT ENTERPRISE</p>
      <Marquee 
        :items="logos" 
        :duration="40" 
        :gap="24"
        :showFadeLeft="true"
        :showFadeRight="true"
      />
    </div>
  </section>
</template>

<script setup>
import Marquee from '@/components/ui/Marquee.vue'

const logos = [
  { name: 'DeepSeek', src: '/assets/deepseek.png' },
  { name: 'Gemma', src: '/assets/gemma.png' },
  { name: 'GLM', src: '/assets/glm.png' },
  { name: 'GPT-OSS', src: '/assets/gpt-oss.png' },
  { name: 'Kimi', src: '/assets/kimi.png' },
  { name: 'MiniMax', src: '/assets/minimax.png' },
  { name: 'Mistral', src: '/assets/mistral.png' },
  { name: 'Qwen', src: '/assets/qwen.png' },
]
</script>

<style scoped>
/* Styles handled by Tailwind */
</style>