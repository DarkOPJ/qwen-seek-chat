<template>
  <div class="min-h-screen bg-background text-on-surface">
    <div class="bg-animation" aria-hidden="true"></div>
    <div class="neural-orb orb-indigo" aria-hidden="true"></div>
    <div class="neural-orb orb-violet" aria-hidden="true"></div>

    <nav class="docked full-width glass-panel border-b border-white/10">
      <div class="max-w-[1280px] mx-auto px-[32px] h-20 flex justify-between items-center">
        <div class="flex items-center gap-2">
          <img :src="orbitalLogo" alt="Qwen Chat" class="w-8 h-8 object-contain" />
          <span class="font-h3 text-h3 font-bold text-white">Qwen Chat</span>
        </div>
        <div class="hidden md:flex items-center gap-8 absolute left-1/2 -translate-x-1/2">
          <a href="#" class="text-white/70 hover:text-white transition-colors font-body-md text-body-md" @click.prevent="navigateTo('/')">Models</a>
          <a href="#" class="text-white font-semibold border-b-2 border-white pb-1 font-body-md text-body-md">Workspace</a>
          <a href="#" class="text-white/70 hover:text-white transition-colors font-body-md text-body-md" @click.prevent="navigateTo('/pricing')">Pricing</a>
          <a href="#" class="text-white/70 hover:text-white transition-colors font-body-md text-body-md" @click.prevent="navigateTo('/enterprise')">Enterprise</a>
        </div>
        <button class="bg-white text-black px-6 py-2 rounded-full font-label-caps text-label-caps font-bold hover:opacity-80 transition-opacity active:scale-95 duration-200" @click="navigateTo('/chat')">
          Get Started
        </button>
      </div>
    </nav>

    <main class="relative z-10 pt-24">
      <div class="max-w-4xl mx-auto px-[32px] py-16">
        <div class="text-center mb-16">
          <h1 class="font-h1 text-h1-mobile md:text-h1 mb-6 text-white tracking-tight">
            Available Models
          </h1>
          <p class="font-body-lg text-body-lg text-white/70 max-w-2xl mx-auto">
            Compare and select from our curated collection of state-of-the-art foundation models.
          </p>
        </div>

        <div class="grid md:grid-cols-2 gap-8 mb-16">
          <ModelCard 
            v-for="model in activeModels" 
            :key="model.id" 
            :model="model" 
            @select="selectModel"
          />
        </div>

        <h2 class="font-h3 text-h3 mb-8 text-center text-white">Coming Soon</h2>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
          <div v-for="model in comingSoonModels" :key="model.name" class="glass-panel p-6 rounded-2xl text-center flex flex-col items-center">
            <img :src="model.logo" :alt="model.name" class="w-12 h-12 mb-4 object-contain opacity-70" />
            <span class="font-mono-metrics text-[10px] text-white/40 mb-1">{{ model.name }}</span>
            <span class="font-label-caps text-[10px] text-on-tertiary-container">COMING SOON</span>
          </div>
        </div>
      </div>
    </main>

    <footer class="w-full py-[32px] md:py-[180px] bg-black border-t border-white/10 text-white relative overflow-hidden">
      <div class="max-w-[1280px] mx-auto px-[32px] flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="flex items-center gap-2">
          <img :src="orbitalLogo" alt="Qwen Chat" class="w-8 h-8 object-contain" />
          <span class="font-h3 text-h3 text-white font-bold">Qwen Chat</span>
        </div>
        <p class="font-label-caps text-label-caps text-on-tertiary-container uppercase tracking-widest">© 2025 QWEN CHAT. ALL RIGHTS RESERVED.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import ModelCard from '@/components/ModelCard.vue'

const router = useRouter()

const navigateTo = (path) => router.push(path)

const activeModels = [
  {
    id: 'qwen3:1.7b',
    name: 'Qwen3.7-Max',
    badge: 'ACTIVE',
    badgeColor: 'accent-emerald',
    logo: '/assets/qwen.png',
    description: 'State-of-the-art linguistic versatility with extreme context window support.',
    accentColor: 'neural-purple',
  },
  {
    id: 'deepseek-r1:1.5b',
    name: 'DeepSeek-V4',
    badge: 'ACTIVE',
    badgeColor: 'accent-emerald',
    logo: '/assets/deepseek.png',
    description: 'Unrivaled efficiency in code generation and complex mathematical reasoning.',
    accentColor: 'neural-indigo',
  },
]

const comingSoonModels = [
  { name: 'MISTRAL', logo: '/assets/mistral.png' },
  { name: 'GEMMA', logo: '/assets/gemma.png' },
  { name: 'GPT-OSS', logo: '/assets/gpt-oss.png' },
  { name: 'GLM', logo: '/assets/glm.png' },
  { name: 'KIMI', logo: '/assets/kimi.png' },
  { name: 'MINIMAX', logo: '/assets/minimax.png' },
]

const orbitalLogo = '/assets/orbital-logo.png'

const selectModel = (modelId) => {
  router.push({ path: '/chat', query: { model: modelId } })
}
</script>

<style scoped>
/* Styles handled by Tailwind */
</style>