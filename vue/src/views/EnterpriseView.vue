<template>
  <div class="min-h-screen bg-background text-on-background font-body-md dark">
    <!-- Global Background Animation Wrapper -->
    <div class="fixed inset-0 -z-50 overflow-hidden bg-black">
      <NeuralOrb class="top-1/4 left-1/4 w-[500px] h-[500px] bg-neural-indigo" />
      <NeuralOrb class="bottom-1/4 right-1/4 w-[600px] h-[600px] bg-neural-purple" />
    </div>

    <!-- Navigation Shell -->
    <nav class="fixed top-0 w-full z-50 bg-white/5 backdrop-blur-3xl border-b border-white/10 inner-glow-px">
      <div class="max-w-[1280px] mx-auto flex justify-between items-center h-[64px] px-[32px]">
        <div class="flex items-center gap-3">
          <svg class="w-8 h-8 object-contain" viewBox="0 0 32 32" fill="none" aria-hidden="true">
            <rect width="32" height="32" rx="8" fill="#000"/>
            <path d="M8 16C8 11.5817 11.5817 8 16 8C20.4183 8 24 11.5817 24 16C24 20.4183 20.4183 24 16 24C11.5817 24 8 20.4183 8 16Z" stroke="#A855F7" stroke-width="2"/>
            <path d="M16 8V16L21 19" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="font-h3 text-h3 font-semibold tracking-tighter text-primary">Qwen Chat</span>
        </div>
        <div class="hidden md:flex items-center gap-8 absolute left-1/2 -translate-x-1/2">
          <a class="text-secondary hover:text-primary transition-colors duration-200 font-body-md text-body-md" href="#" @click.prevent="navigateTo('/')">Models</a>
          <a class="text-secondary hover:text-primary transition-colors duration-200 font-body-md text-body-md" href="#" @click.prevent="navigateTo('/chat')">Workspace</a>
          <a class="text-secondary hover:text-primary transition-colors duration-200 font-body-md text-body-md" href="#" @click.prevent="navigateTo('/pricing')">Pricing</a>
          <a class="text-primary font-semibold border-b-2 border-primary pb-1 font-body-md text-body-md" href="#">Enterprise</a>
        </div>
        <div class="flex items-center gap-4">
          <button class="bg-primary text-tertiary px-6 py-2 rounded-full font-semibold hover:opacity-90 active:scale-95 transition-all text-body-md" @click="navigateTo('/chat')">Get Started</button>
        </div>
      </div>
    </nav>

    <main class="relative">
      <!-- Hero Section -->
      <section class="pt-[160px] pb-[180px] max-w-[1280px] mx-auto px-[32px] text-center">
        <div class="inline-flex items-center gap-2 px-4 py-1 rounded-full border border-white/10 bg-white/5 mb-8">
          <span class="w-2 h-2 rounded-full bg-accent-emerald animate-pulse"></span>
          <span class="font-label-caps text-label-caps uppercase tracking-widest text-secondary">Qwen Chat for Enterprise</span>
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

      <!-- Trusted By Section -->
      <section class="py-12 border-y border-white/5 bg-black/20">
        <div class="max-w-[1280px] mx-auto px-[32px]">
          <p class="text-center font-label-caps text-label-caps text-secondary mb-10 opacity-60">POWERING THE NEXT GENERATION OF INTELLIGENT ENTERPRISE</p>
          <TrustedByMarquee :logos="trustedLogos" />
        </div>
      </section>

      <!-- Key Value Props -->
      <section class="py-[180px] max-w-[1280px] mx-auto px-[32px]">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <FeatureCard
            icon="admin_panel_settings"
            iconColor="neural-indigo"
            iconBg="neural-indigo"
            title="Security & Compliance"
            description="SOC2 Type II certified. Data residency options in 20+ regions with zero-retention policies as the default standard."
            :features="[
              { icon: 'check_circle', color: 'accent-emerald', text: 'ENCRYPTION AT REST & TRANSIT' },
              { icon: 'check_circle', color: 'accent-emerald', text: 'BYOK (BRING YOUR OWN KEY)' }
            ]"
          />
          <FeatureCard
            icon="hub"
            iconColor="accent-emerald"
            iconBg="accent-emerald"
            title="Custom Model Orchestration"
            description="Deploy private, optimized instances of DeepSeek, Qwen, and Llama within your own virtual private cloud perimeter."
            :tags="['DeepSeek-V3', 'Qwen-2.5', 'Llama-3.1']"
            isHighlighted
          />
          <FeatureCard
            icon="analytics"
            iconColor="neural-purple"
            iconBg="neural-purple"
            title="Administrative Control"
            description="Full SSO/SCIM integration with granular RBAC and real-time usage analytics across your entire global workforce."
            :features="[
              { icon: 'check_circle', color: 'accent-emerald', text: 'OKTA & AZURE AD SUPPORT' },
              { icon: 'check_circle', color: 'accent-emerald', text: 'COST ATTRIBUTION API' }
            ]"
          />
        </div>
      </section>

      <!-- Visualization Section -->
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
            <InfraVisualization />
          </div>
        </div>
      </section>

      <!-- Final Sign-off -->
      <section class="py-[180px] text-center max-w-[1280px] mx-auto px-[32px]">
        <h2 class="font-h2 text-h2-mobile md:text-h2 text-primary mb-8">Ready to scale?</h2>
        <p class="text-secondary font-body-lg text-body-lg max-w-[600px] mx-auto mb-12">
          Join 500+ enterprises building the future of autonomous intelligence on Qwen Chat.
        </p>
        <button class="bg-primary text-tertiary px-12 py-5 rounded-full font-bold text-body-lg hover:scale-105 active:scale-95 transition-all shadow-xl" @click="navigateTo('/chat')">Talk to Sales</button>
        <p class="mt-8 text-secondary font-label-caps text-label-caps opacity-50">OR EXPLORE OUR <a class="underline hover:text-primary" href="#">DEVELOPER DOCUMENTATION</a></p>
      </section>
    </main>

    <!-- Transparent Footer -->
    <footer class="w-full py-[80px] border-t border-white/5 relative overflow-hidden bg-black">
      <div class="max-w-[1280px] mx-auto px-[32px] flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="flex items-center gap-3">
          <svg class="w-8 h-8 object-contain" viewBox="0 0 32 32" fill="none" aria-hidden="true">
            <rect width="32" height="32" rx="8" fill="#000"/>
            <path d="M8 16C8 11.5817 11.5817 8 16 8C20.4183 8 24 11.5817 24 16C24 20.4183 20.4183 24 16 24C11.5817 24 8 20.4183 8 16Z" stroke="#A855F7" stroke-width="2"/>
            <path d="M16 8V16L21 19" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="font-h3 text-h3 font-bold text-primary">Qwen Chat</span>
        </div>
        <p class="text-secondary text-label-caps tracking-widest opacity-60">© 2025 QWEN CHAT. ALL RIGHTS RESERVED.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import TrustedByMarquee from '@/components/enterprise/TrustedByMarquee.vue'
import FeatureCard from '@/components/enterprise/FeatureCard.vue'
import InfraVisualization from '@/components/enterprise/InfraVisualization.vue'
import NeuralOrb from '@/components/ui/NeuralOrb.vue'

const router = useRouter()
const navigateTo = (path) => router.push(path)

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
/* All styles moved to CSS classes in main.css and components */
</style>