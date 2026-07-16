<template>
  <div class="glass-panel rounded-xl p-8 flex flex-col">
    <div v-if="isRecommended" class="absolute -top-3 left-1/2 -translate-x-1/2 bg-neural-purple text-white px-3 py-1 rounded-full font-label-caps text-[10px] tracking-wider whitespace-nowrap">
      RECOMMENDED
    </div>
    <div class="mb-8">
      <h3 class="font-h3 text-h3 mb-2">{{ title }}</h3>
      <div class="flex items-baseline gap-1 mb-4">
        <span class="font-h2 text-h2">{{ price }}</span>
        <span v-if="period" class="font-body-md text-body-md text-white/50">{{ period }}</span>
      </div>
      <p class="font-body-md text-body-md text-white/70">{{ description }}</p>
    </div>
    <button :class="buttonClass" class="w-full py-3 px-4 rounded-full font-label-caps text-label-caps transition-colors mb-8">
      {{ ctaText }}
    </button>
    <div class="flex-grow">
      <ul class="space-y-4 font-body-md text-body-md text-white/80">
        <li v-for="feature in features" :key="feature.text" class="flex items-start gap-3">
          <span :class="feature.highlight ? 'material-symbols-outlined text-neural-purple text-[20px] mt-1' : 'material-symbols-outlined text-white/50 text-[20px]'">{{ feature.icon || 'check' }}</span>
          <div v-if="feature.models" class="">
            {{ feature.text }}
            <div class="flex gap-2 mt-2 items-center">
              <div class="bg-white/10 rounded-md p-1 border border-white/5">
                <img alt="Qwen Model" class="w-6 h-6 object-contain rounded-sm" :src="qwenLogo" />
              </div>
              <div class="bg-white/10 rounded-md p-1 border border-white/5">
                <img alt="DeepSeek Model" class="w-6 h-6 object-contain rounded-sm" :src="deepseekLogo" />
              </div>
            </div>
          </div>
          <span v-else>{{ feature.text }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: { type: String, required: true },
  price: { type: String, required: true },
  period: { type: String, default: '/mo' },
  description: { type: String, required: true },
  ctaText: { type: String, required: true },
  features: { type: Array, required: true },
  variant: { type: String, default: 'default' },
  isRecommended: { type: Boolean, default: false },
})

const qwenLogo = 'https://lh3.googleusercontent.com/aida-public/AB6AXuBOVC1IzU0D5OtePvol_dJfh21bzKSQEoOZEdsnBna3QsWL6zCFX8tY1DMMboIz2p9tQtR_ZzynB5JuraVdqwF6hN2husm3WYaZYL8Fr91F5Xe2AN9eGEQ1dnkpgUMcI0xK-GkrR64r96klfLy-iXXzVGzE1ErPezl6n8GyEqR7xgLTWA-8IHkO11ocbWVpDuECZIHuLQQNZtUwqBI8IYmxWfjHz6LndiTE5oL7qxnMt4YeHyvU3nykTw20LMlK5l-PuvQ'
const deepseekLogo = 'https://lh3.googleusercontent.com/aida-public/AB6AXuAo2IyPICTI53qWOaNTB2Hv0YOHjJw2ktEsHbxvbCmMtCXeCIm2xyFOyHX9G4gRaLOIwCVF1e1lmZ6UNj3oWV852e-xCDzxBxf5CQpGdx7R_S0lMTHvULnSJXysiZkVuv0dk3sdmhfYUov6C6H8-Z0z7DWd-ZE3Sq_byVPU_Wge8aC86cXwwkhErYQTxcY0oHBwRWCKZ-j1KFjpHHofyl_2PU0BFb3GnxYxjt8zZH1u6UhH1BErFs0DMMpwNnaG_GeNtiA'

const buttonClass = computed(() => {
  switch (props.variant) {
    case 'recommended':
      return 'bg-white text-black hover:bg-white/90'
    case 'enterprise':
      return 'border border-white/20 hover:bg-white/10'
    default:
      return 'border border-white/20 hover:bg-white/10'
  }
})
</script>

<style scoped>
/* Styles handled by Tailwind */
</style>