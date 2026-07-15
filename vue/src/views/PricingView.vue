<template>
  <div class="min-h-screen bg-black text-white">
    <nav class="flex justify-between items-center h-16 px-[32px] max-w-[1280px] mx-auto w-full bg-black/25 backdrop-blur-3xl docked full-width top-0 sticky border-b border-white/10 z-50">
      <div class="flex items-center gap-2 font-h3 text-h3 font-semibold tracking-tight text-white">
        <svg class="w-8 h-8 object-contain" viewBox="0 0 32 32" fill="none" aria-hidden="true">
          <rect width="32" height="32" rx="8" fill="#000"/>
          <path d="M8 16C8 11.5817 11.5817 8 16 8C20.4183 8 24 11.5817 24 16C24 20.4183 20.4183 24 16 24C11.5817 24 8 20.4183 8 16Z" stroke="#A855F7" stroke-width="2"/>
          <path d="M16 8V16L21 19" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Qwen Chat</span>
      </div>
      <div class="hidden md:flex gap-8 items-center font-body-md text-body-md">
        <a class="text-white/70 hover:text-white transition-colors" href="#" @click.prevent="navigateTo('/')">Models</a>
        <a class="text-white/70 hover:text-white transition-colors" href="#" @click.prevent="navigateTo('/chat')">Workspace</a>
        <a class="text-white font-semibold border-b-2 border-white pb-1 active:scale-95 transition-transform duration-200" href="#">Pricing</a>
        <a class="text-white/70 hover:text-white transition-colors" href="#" @click.prevent="navigateTo('/enterprise')">Enterprise</a>
      </div>
      <button class="bg-white text-black px-6 py-2 rounded-full font-label-caps text-label-caps hover:opacity-80 transition-opacity active:scale-95 duration-200" @click="navigateTo('/chat')">
        Get Started
      </button>
    </nav>

    <main class="flex-grow flex flex-col items-center w-full max-w-[1280px] mx-auto px-[32px] pt-[120px] pb-[180px]">
      <section class="text-center w-full max-w-3xl mb-[80px] md:mb-[120px]">
        <h1 class="font-h1-mobile text-h1-mobile md:font-h1 md:text-h1 mb-6 text-white tracking-tight">
          Pricing built for scale.
        </h1>
        <p class="font-body-lg text-body-lg text-white/70 max-w-2xl mx-auto">
          Transparent, flexible plans designed to support independent researchers and scale seamlessly to enterprise production environments.
        </p>
      </section>

      <section class="w-full grid grid-cols-1 md:grid-cols-3 gap-6 mb-[180px] relative z-10">
        <PricingCard
          title="Starter"
          price="$0"
          period="/mo"
          description="Perfect for prototyping and exploration."
          :features="[
            { icon: 'check', text: '100 messages/mo' },
            { icon: 'check', text: 'Standard models access' },
            { icon: 'check', text: 'Community support' }
          ]"
          ctaText="Start Free"
          variant="default"
        />
        <PricingCard
          title="Pro"
          price="$20"
          period="/mo"
          description="For professionals requiring high-performance models."
          :features="[
            { icon: 'check', text: 'Unlimited messages', highlight: true },
            { icon: 'check', text: 'Priority access to high-performance models', highlight: true, models: true },
            { icon: 'check', text: '128k context window', highlight: true },
            { icon: 'check', text: 'Email support', highlight: true }
          ]"
          ctaText="Upgrade to Pro"
          variant="recommended"
          isRecommended
        />
        <PricingCard
          title="Enterprise"
          price="Custom"
          description="Custom tailored solutions for large organizations."
          :features="[
            { icon: 'check', text: 'Dedicated infrastructure' },
            { icon: 'check', text: 'Custom model fine-tuning' },
            { icon: 'check', text: 'RBAC & SSO' },
            { icon: 'check', text: '24/7 dedicated support' }
          ]"
          ctaText="Contact Sales"
          variant="enterprise"
        />
      </section>

      <section class="w-full max-w-3xl">
        <h2 class="font-h2 text-h2 mb-12 text-center">Frequently Asked Questions</h2>
        <div class="space-y-4">
          <FAQItem
            question="How does billing work for the Pro tier?"
            answer="The Pro tier is billed monthly at $20/month. You can cancel at any time, and you'll retain access until the end of your current billing cycle. There are no hidden fees or usage limits for standard chat interactions."
          />
          <FAQItem
            question="Can I switch between different models?"
            answer="Yes, Pro users have seamless access to switch between our highest-performing models, including Qwen3.7-Max and DeepSeek-V4, directly within the workspace interface without any additional configuration."
          />
          <FAQItem
            question="What security standards do Enterprise plans meet?"
            answer="Enterprise plans feature dedicated, isolated infrastructure ensuring zero data crossover. We support SAML SSO, Role-Based Access Control (RBAC), and are compliant with SOC 2 Type II standards."
          />
        </div>
      </section>
    </main>

    <footer class="flex flex-col md:flex-row justify-between items-center py-[32px] px-[32px] max-w-[1280px] mx-auto w-full border-t border-white/10 bg-black text-white/50">
      <div class="flex items-center gap-2 font-h3 text-h3 font-bold text-white">
        <svg class="w-8 h-8 object-contain" viewBox="0 0 32 32" fill="none" aria-hidden="true">
          <rect width="32" height="32" rx="8" fill="#000"/>
          <path d="M8 16C8 11.5817 11.5817 8 16 8C20.4183 8 24 11.5817 24 16C24 20.4183 20.4183 24 16 24C11.5817 24 8 20.4183 8 16Z" stroke="#A855F7" stroke-width="2"/>
          <path d="M16 8V16L21 19" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>QWEN CHAT</span>
      </div>
      <div class="font-label-caps text-label-caps tracking-wider text-white/50">© 2025 QWEN CHAT. ALL RIGHTS RESERVED</div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import PricingCard from '@/components/pricing/PricingCard.vue'
import FAQItem from '@/components/pricing/FAQItem.vue'

const router = useRouter()
const navigateTo = (path) => router.push(path)
</script>

<style scoped>
/* Styles handled by Tailwind */
</style>