<template>
  <div class="min-h-screen bg-background text-on-background font-body-md dark">
    <div class="fixed inset-0 -z-50 overflow-hidden bg-black">
      <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-neural-indigo neural-orb rounded-full"></div>
      <div class="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] bg-neural-purple neural-orb rounded-full"></div>
    </div>

    <Navbar />

    <main class="relative">
      <section class="pt-[160px] pb-[180px] max-w-[1280px] mx-auto px-[32px] text-center">
        <div class="inline-flex items-center gap-2 px-4 py-1 rounded-full border border-white/10 bg-white/5 mb-8">
          <span class="w-2 h-2 rounded-full bg-accent-emerald animate-pulse"></span>
          <span class="font-label-caps text-label-caps uppercase tracking-widest text-secondary">Orbital AI for Enterprise</span>
        </div>
        <h1 class="font-h1 text-h1-mobile md:text-h1 text-gradient mb-8 max-w-[900px] mx-auto">
          Intelligence, secured and scaled.
        </h1>
        <p class="text-secondary font-body-lg text-body-lg max-w-[600px] mx-auto mb-12">
          Deploy state-of-the-art AI infrastructure with absolute control, enterprise-grade security, and precision orchestration.
        </p>
        <div class="flex flex-col md:flex-row items-center justify-center gap-4">
          <button class="w-full md:w-auto bg-primary text-tertiary px-10 py-4 rounded-full font-bold text-body-lg hover:bg-neutral-200 transition-all shadow-2xl" @click="navigateTo('/chat')">Contact Sales</button>
          <button class="w-full md:w-auto border border-white/20 text-primary px-10 py-4 rounded-full font-bold text-body-lg hover:bg-white/5 transition-all" @click="navigateTo('/chat')">Request Demo</button>
        </div>
      </section>

      <section class="py-12 border-y border-white/5 bg-black/20">
        <div class="max-w-[1280px] mx-auto px-[32px]">
          <p class="text-center font-label-caps text-label-caps text-secondary mb-10 opacity-60">POWERING THE NEXT GENERATION OF INTELLIGENT ENTERPRISE</p>
          <div class="relative overflow-hidden py-4">
            <div class="flex animate-marquee whitespace-nowrap gap-24 items-center w-max">
              <div class="flex shrink-0 items-center gap-24">
                <img v-for="logo in trustedLogos" :key="logo.name" :src="logo.src" :alt="logo.name" class="h-8 w-auto object-contain" />
              </div>
              <div class="flex shrink-0 items-center gap-24">
                <img v-for="logo in trustedLogos" :key="'dup-' + logo.name" :src="logo.src" :alt="logo.name" class="h-8 w-auto object-contain" />
              </div>
            </div>
            <div class="absolute inset-y-0 left-0 w-32 bg-gradient-to-r from-black to-transparent z-10"></div>
            <div class="absolute inset-y-0 right-0 w-32 bg-gradient-to-l from-black to-transparent z-10"></div>
          </div>
        </div>
      </section>

      <section class="py-[180px] max-w-[1280px] mx-auto px-[32px]">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="glass-card p-10 rounded-xl group hover:border-white/20 transition-all">
            <div class="w-14 h-14 rounded-lg bg-neural-indigo/10 flex items-center justify-center mb-8 border border-neural-indigo/20">
              <span class="material-symbols-outlined text-neural-indigo" style="font-variation-settings: 'FILL' 1;">admin_panel_settings</span>
            </div>
            <h3 class="font-h3 text-h3 mb-4 text-primary">Security & Compliance</h3>
            <p class="text-secondary font-body-md text-body-md leading-relaxed">
              SOC2 Type II certified. Data residency options in 20+ regions with zero-retention policies as the default standard.
            </p>
            <ul class="mt-8 space-y-3">
              <li class="flex items-center gap-3 text-secondary text-label-caps">
                <span class="material-symbols-outlined text-accent-emerald text-sm">check_circle</span>
                ENCRYPTION AT REST & TRANSIT
              </li>
              <li class="flex items-center gap-3 text-secondary text-label-caps">
                <span class="material-symbols-outlined text-accent-emerald text-sm">check_circle</span>
                BYOK (BRING YOUR OWN KEY)
              </li>
            </ul>
          </div>

          <div class="glass-card p-10 rounded-xl border-white/20 relative overflow-hidden group">
            <div class="absolute -top-24 -right-24 w-48 h-48 bg-accent-emerald/10 blur-[60px]"></div>
            <div class="w-14 h-14 rounded-lg bg-accent-emerald/10 flex items-center justify-center mb-8 border border-accent-emerald/20">
              <span class="material-symbols-outlined text-accent-emerald" style="font-variation-settings: 'FILL' 1;">hub</span>
            </div>
            <h3 class="font-h3 text-h3 mb-4 text-primary">Custom Model Orchestration</h3>
            <p class="text-secondary font-body-md text-body-md leading-relaxed">
              Deploy private, optimized instances of DeepSeek, Qwen, and Llama within your own virtual private cloud perimeter.
            </p>
            <div class="mt-8 flex flex-wrap gap-2">
              <span class="px-3 py-1 rounded bg-white/5 text-[10px] font-mono-metrics text-secondary uppercase border border-white/10 tracking-widest">DeepSeek-V3</span>
              <span class="px-3 py-1 rounded bg-white/5 text-[10px] font-mono-metrics text-secondary uppercase border border-white/10 tracking-widest">Qwen-2.5</span>
              <span class="px-3 py-1 rounded bg-white/5 text-[10px] font-mono-metrics text-secondary uppercase border border-white/10 tracking-widest">Llama-3.1</span>
            </div>
          </div>

          <div class="glass-card p-10 rounded-xl group hover:border-white/20 transition-all">
            <div class="w-14 h-14 rounded-lg bg-neural-purple/10 flex items-center justify-center mb-8 border border-neural-purple/20">
              <span class="material-symbols-outlined text-neural-purple" style="font-variation-settings: 'FILL' 1;">analytics</span>
            </div>
            <h3 class="font-h3 text-h3 mb-4 text-primary">Administrative Control</h3>
            <p class="text-secondary font-body-md text-body-md leading-relaxed">
              Full SSO/SCIM integration with granular RBAC and real-time usage analytics across your entire global workforce.
            </p>
            <ul class="mt-8 space-y-3">
              <li class="flex items-center gap-3 text-secondary text-label-caps">
                <span class="material-symbols-outlined text-accent-emerald text-sm">check_circle</span>
                OKTA & AZURE AD SUPPORT
              </li>
              <li class="flex items-center gap-3 text-secondary text-label-caps">
                <span class="material-symbols-outlined text-accent-emerald text-sm">check_circle</span>
                COST ATTRIBUTION API
              </li>
            </ul>
          </div>
        </div>
      </section>

      <section class="py-[180px] relative overflow-hidden bg-black">
        <div class="max-w-[1280px] mx-auto px-[32px] relative z-10">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-[32px] items-center">
            <div>
              <h2 class="font-h2 text-h2 mb-6 text-primary leading-tight">Enterprise-Grade Infrastructure</h2>
              <p class="text-secondary font-body-lg text-body-lg mb-8 leading-relaxed">
                Our proprietary edge network ensures sub-50ms latency globally, with built-in redundancy and failover mechanisms that guarantee 99.99% uptime for critical AI workloads.
              </p>
              <div class="space-y-6">
                <div class="flex gap-4">
                  <div class="shrink-0 w-8 h-8 rounded-full bg-white/10 border border-white/10 flex items-center justify-center">
                    <span class="material-symbols-outlined text-primary text-sm">public</span>
                  </div>
                  <div>
                    <h4 class="text-primary font-bold mb-1">Global Edge Sync</h4>
                    <p class="text-secondary text-sm">Instant synchronization of model weights and context across 140+ PoPs.</p>
                  </div>
                </div>
                <div class="flex gap-4">
                  <div class="shrink-0 w-8 h-8 rounded-full bg-white/10 border border-white/10 flex items-center justify-center">
                    <span class="material-symbols-outlined text-primary text-sm">bolt</span>
                  </div>
                  <div>
                    <h4 class="text-primary font-bold mb-1">Auto-Scaling Compute</h4>
                    <p class="text-secondary text-sm">Dynamically allocate H100/A100 clusters based on real-time traffic spikes.</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="relative aspect-square md:aspect-video lg:aspect-square bg-black/40 rounded-2xl border border-white/10 overflow-hidden shadow-2xl">
              <div class="absolute inset-0 flex items-center justify-center p-12">
                <div class="w-full h-full border border-white/5 rounded-full relative animate-spin-slow">
                  <div class="absolute top-0 left-1/2 -translate-x-1/2 w-4 h-4 bg-neural-indigo rounded-full shadow-[0_0_20px_#6366F1]"></div>
                  <div class="absolute bottom-1/4 left-0 w-3 h-3 bg-accent-emerald rounded-full shadow-[0_0_15px_#10B981]"></div>
                  <div class="absolute top-1/2 right-0 w-3 h-3 bg-neural-purple rounded-full shadow-[0_0_15px_#A855F7]"></div>
                </div>
                <div class="absolute w-3/4 h-3/4 border border-white/5 rounded-full animate-spin-reverse"></div>
                <div class="absolute w-1/2 h-1/2 border border-white/10 rounded-full flex items-center justify-center bg-black/60 backdrop-blur-md">
                  <span class="material-symbols-outlined text-primary text-6xl">language</span>
                </div>
              </div>
              <div class="absolute bottom-6 left-6 right-6 flex justify-between">
                <div class="bg-white/10 backdrop-blur-md border border-white/20 p-3 rounded-lg flex items-center gap-3">
                  <div class="w-2 h-2 rounded-full bg-accent-emerald"></div>
                  <span class="text-[10px] font-mono-metrics text-primary uppercase">Nodes Active: 142</span>
                </div>
                <div class="bg-white/10 backdrop-blur-md border border-white/20 p-3 rounded-lg flex items-center gap-3">
                  <div class="w-2 h-2 rounded-full bg-neural-indigo"></div>
                  <span class="text-[10px] font-mono-metrics text-primary uppercase">Latency: 24ms</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="py-[180px] text-center max-w-[1280px] mx-auto px-[32px]">
        <h2 class="font-h2 text-h2-mobile md:text-h2 text-primary mb-8">Ready to scale?</h2>
        <p class="text-secondary font-body-lg text-body-lg max-w-[600px] mx-auto mb-12">
          Join 500+ enterprises building the future of autonomous intelligence on Orbital AI.
        </p>
        <button class="bg-primary text-tertiary px-12 py-5 rounded-full font-bold text-body-lg hover:scale-105 active:scale-95 transition-all shadow-xl" @click="navigateTo('/chat')">Talk to Sales</button>
        
      </section>
    </main>

    <footer class="w-full py-[32px] border-t border-white/5 relative overflow-hidden bg-black">
      <div class="max-w-[1280px] mx-auto px-[32px] flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="flex items-center gap-3">
          <img :src="orbitalLogo" alt="Orbital AI" class="w-8 h-8 object-contain" />
          <span class="font-h3 text-h3 font-bold text-primary">Orbital AI</span>
        </div>
        <p class="text-secondary text-label-caps tracking-widest opacity-60">© {{ currentYear }} Orbital AI. ALL RIGHTS RESERVED.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import Navbar from '@/components/layout/Navbar.vue'

const router = useRouter()
const navigateTo = (path) => router.push(path)

const currentYear = new Date().getFullYear()
const orbitalLogo = '/assets/orbital-logo.png'

const trustedLogos = [
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
</style>