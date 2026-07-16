<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '@/components/layout/Navbar.vue'

const router = useRouter()
const isLoaded = ref(false)
const year = new Date().getFullYear()

onMounted(() => {
  requestAnimationFrame(() => {
    isLoaded.value = true
  })
})

const navigateTo = (path) => {
  router.push(path)
}

const comingSoonModels = ref([
  { name: 'MISTRAL', logo: '/assets/mistral.png' },
  { name: 'GEMMA', logo: '/assets/gemma.png' },
  { name: 'GPT-OSS', logo: '/assets/gpt-oss.png' },
  { name: 'GLM', logo: '/assets/glm.png' },
  { name: 'KIMI', logo: '/assets/kimi.png' },
  { name: 'MINIMAX', logo: '/assets/minimax.png' },
])

const features = ref([
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
])

const orbitalLogo = '/assets/orbital-logo.png'
const heroImage = '/assets/hero-chat.png'
const deepseekLogo = '/assets/deepseek.png'
const qwenLogo = '/assets/qwen.png'
</script>

<template>
  <div class="min-h-screen bg-background text-on-surface relative">
    <!-- Background Animation -->
    <div class="bg-animation" aria-hidden="true"></div>
    <div class="neural-orb orb-indigo" aria-hidden="true"></div>
    <div class="neural-orb orb-violet" aria-hidden="true"></div>

    <!-- Navigation -->
    <Navbar />

    <main class="relative z-10">
      <!-- Hero Section -->
      <section class="min-h-screen flex flex-col justify-center px-[32px] max-w-[1280px] mx-auto pt-[120px]">
        <div class="grid lg:grid-cols-2 gap-16 items-center" :class="{ 'opacity-100 translate-y-0': isLoaded, 'opacity-0 translate-y-10': !isLoaded }" style="transition: all 1s ease;">
          <!-- Left Content -->
          <div class="space-y-8">
            <h1 class="font-h1 text-h1-mobile md:text-h1 text-white leading-tight">
              Intelligence, <br>
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-neural-indigo to-neural-purple">evolved.</span>
            </h1>
            <p class="font-body-lg text-body-lg text-on-tertiary-container max-w-lg">
              Access the world's most advanced reasoning engines in a single, unified workspace designed for precision and performance.
            </p>
            <div class="flex flex-wrap gap-4 pt-4">
              <button class="bg-white text-black px-8 py-4 rounded-full font-label-caps text-label-caps font-bold shadow-xl shadow-white/5 hover:bg-zinc-200 transition-all" @click="navigateTo('/chat')">
                Start Building
              </button>
            </div>
          </div>

          <!-- Right Visual -->
          <div class="relative group">
            <div class="absolute -inset-4 bg-gradient-to-r from-neural-indigo/20 to-neural-purple/20 rounded-3xl blur-2xl group-hover:blur-3xl transition-all"></div>
            <div class="glass-panel rounded-3xl overflow-hidden animate-float">
              <img 
                class="w-full h-auto" 
                alt="Orbital AI workspace interface showing dark-themed chat with code editor and AI responses" 
                :src="heroImage"
              />
            </div>
            
            <!-- Floating UI Widget -->
            <div class="absolute -bottom-6 -left-6 glass-panel p-6 rounded-2xl hidden md:block" style="--mouse-x: 2.5px; --mouse-y: 63.75px;">
              <div class="flex items-center gap-3 mb-2">
                <span class="material-symbols-outlined text-accent-emerald">verified</span>
                <span class="font-mono-metrics">MODEL_SYNC_COMPLETE</span>
              </div>
              <div class="h-1 w-32 bg-white/10 rounded-full overflow-hidden">
                <div class="h-full w-3/4 bg-accent-emerald"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Model Section -->
      <section class="py-[180px] md:py-[180px] px-[32px] max-w-[1280px] mx-auto" :class="{ 'opacity-100 translate-y-0': isLoaded, 'opacity-0 translate-y-10': !isLoaded }" style="transition: all 1s ease 0.2s;">
        <div class="text-center mb-24">
          <h2 class="font-h2 text-h2 mb-6">Engineered for Choice</h2>
          <p class="font-body-lg text-body-lg text-on-tertiary-container max-w-2xl mx-auto">
            Switch between top-tier foundation models instantly. No setup, no latency, just pure intelligence.
          </p>
        </div>

        <!-- Active Models -->
        <div class="grid md:grid-cols-2 gap-8 mb-16">
          <!-- DeepSeek -->
          <div class="glass-panel p-8 rounded-3xl group cursor-pointer hover:border-neural-indigo/50 transition-all">
            <div class="flex justify-between items-start mb-12">
              <div class="w-16 h-16 rounded-2xl overflow-hidden bg-black/40 p-2 flex items-center justify-center">
                <img :alt="activeModels[0].name" :src="deepseekLogo" class="w-full h-full object-contain" />
              </div>
              <span class="px-4 py-1 rounded-full bg-accent-emerald/10 text-accent-emerald font-mono-metrics text-xs">ACTIVE</span>
            </div>
            <h3 class="font-h3 text-h3 mb-2">DeepSeek-V4</h3>
            <p class="font-body-md text-body-md text-on-tertiary-container mb-6">Unrivaled efficiency in code generation and complex mathematical reasoning.</p>
            <div class="flex items-center gap-2 text-neural-indigo font-label-caps text-label-caps">
              Explore capabilities <span class="material-symbols-outlined text-sm">arrow_forward</span>
            </div>
          </div>

          <!-- Qwen -->
          <div class="glass-panel p-8 rounded-3xl group cursor-pointer hover:border-neural-purple/50 transition-all">
            <div class="flex justify-between items-start mb-12">
              <div class="w-16 h-16 rounded-2xl overflow-hidden bg-black/40 p-2 flex items-center justify-center">
                <img :alt="activeModels[1].name" :src="qwenLogo" class="w-full h-full object-contain" />
              </div>
              <span class="px-4 py-1 rounded-full bg-accent-emerald/10 text-accent-emerald font-mono-metrics text-xs">ACTIVE</span>
            </div>
            <h3 class="font-h3 text-h3 mb-2">Qwen3.7-Max</h3>
            <p class="font-body-md text-body-md text-on-tertiary-container mb-6">State-of-the-art linguistic versatility with extreme context window support.</p>
            <div class="flex items-center gap-2 text-neural-purple font-label-caps text-label-caps">
              Explore capabilities <span class="material-symbols-outlined text-sm">arrow_forward</span>
            </div>
          </div>
        </div>

        <!-- Coming Soon Grid -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
          <div v-for="model in comingSoonModels" :key="model.name" class="glass-panel p-6 rounded-2xl text-center flex flex-col items-center group cursor-not-allowed">
            <img :alt="model.name" :src="model.logo" class="w-12 h-12 mb-4 object-contain opacity-70" />
            <span class="font-mono-metrics text-[10px] text-white/40 mb-1">{{ model.name }}</span>
            <span class="font-label-caps text-[10px] text-on-tertiary-container">COMING SOON</span>
          </div>
        </div>
      </section>

      <!-- Feature Grid Section -->
      <section class="py-[180px] md:py-[180px] bg-black relative overflow-hidden" :class="{ 'opacity-100 translate-y-0': isLoaded, 'opacity-0 translate-y-10': !isLoaded }" style="transition: all 1s ease 0.4s;">
        <div class="px-[32px] max-w-[1280px] mx-auto">
          <div class="mb-20">
            <h2 class="font-h3 text-h3 mb-4 text-white">Uncompromising Precision</h2>
            <p class="text-white/70 font-body-md max-w-lg">Advanced tooling for the most demanding technical workloads.</p>
          </div>
          <div class="grid md:grid-cols-3 gap-6">
            <div v-for="feature in features" :key="feature.title" class="glass-panel p-8 rounded-3xl hover:bg-white/5 transition-all">
              <div class="w-12 h-12 rounded-full flex items-center justify-center mb-8" :class="feature.iconBg">
                <span class="material-symbols-outlined" :class="feature.iconColor">{{ feature.icon }}</span>
              </div>
              <h4 class="font-h3 text-xl mb-4 text-white">{{ feature.title }}</h4>
              <p class="font-body-md text-body-md text-white/60">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="py-[180px] md:py-[180px] bg-black relative overflow-hidden text-center" :class="{ 'opacity-100 translate-y-0': isLoaded, 'opacity-0 translate-y-10': !isLoaded }" style="transition: all 1s ease 0.6s;">
        <div class="px-[32px] max-w-[1280px] mx-auto">
          <h2 class="font-h2 text-h2-mobile md:text-h2 text-white mb-8">Ready to build with Qwen?</h2>
          <p class="text-white/70 font-body-lg text-body-lg max-w-2xl mx-auto mb-12">
            Join thousands of developers building the future with Qwen 2.5. Start free, scale infinitely.
          </p>
          <div class="flex flex-col md:flex-row items-center justify-center gap-4">
            <button class="w-full md:w-auto bg-white text-black px-10 py-4 rounded-full font-bold text-body-lg hover:bg-zinc-200 transition-all shadow-2xl" @click="navigateTo('/chat')">
              Start Building Free
            </button>
            <button class="w-full md:w-auto border border-white/20 text-white px-10 py-4 rounded-full font-bold text-body-lg hover:bg-white/5 transition-all" @click="navigateTo('/pricing')">
              View Pricing
            </button>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="w-full py-[32px] bg-black border-t border-white/10 text-white">
      <div class="flex flex-col md:flex-row justify-between items-center px-[32px] max-w-[1280px] mx-auto gap-8">
        <div class="flex items-center gap-2">
          <img :src="orbitalLogo" alt="Orbital AI Logo" class="w-8 h-8 object-contain" />
          <span class="font-h3 text-h3 text-white font-bold">Orbital AI</span>
        </div>
        <p class="font-label-caps text-label-caps text-on-tertiary-container uppercase tracking-widest">© {{ year }} Orbital AI. ALL RIGHTS RESERVED.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      activeModels: [
        { name: 'DeepSeek', logo: '/assets/deepseek.png' },
        { name: 'Qwen', logo: '/assets/qwen.png' },
      ],
    }
  },
}
</script>

<style scoped>
/* Component-specific styles if needed */
</style>