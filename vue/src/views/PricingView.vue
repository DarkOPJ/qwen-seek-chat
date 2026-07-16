<template>
  <div class="min-h-screen bg-black text-white">
    <Navbar />

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
            answer="The Pro tier is billed at $20/month and includes unlimited messages, priority access to high-performance models (DeepSeek-V4, Qwen3.7-Max), and a 128k context window. You can cancel anytime — access continues until the end of the current billing cycle with no hidden fees or termination penalties."
          />
          <FAQItem
            question="Can I switch between different models?"
            answer="Yes. Pro and Enterprise users can switch between models seamlessly within the workspace — no reconfiguration needed. The platform supports instant switching across DeepSeek, Qwen, and upcoming models like Mistral, Gemma, and GLM as they launch."
          />
          <FAQItem
            question="Is there a free tier available?"
            answer="Yes. The Starter plan is free and includes 100 messages per month with access to standard models and community support. It's a great way to evaluate the platform before upgrading to Pro or Enterprise for production workloads."
          />
          <FAQItem
            question="What security standards do Enterprise plans meet?"
            answer="Enterprise plans feature dedicated, isolated infrastructure with SOC 2 Type II compliance, encryption at rest and in transit, BYOK (Bring Your Own Key) support, SAML SSO, RBAC, and data residency options across 20+ regions. Zero-retention policies are enforced by default."
          />
          <FAQItem
            question="Can I use the API programmatically?"
            answer="Yes. All plans include API access. The Starter plan has rate-limited API access, while Pro and Enterprise tiers unlock higher rate limits, dedicated endpoints, and priority routing. We provide native SDKs for TypeScript, Python, and Rust."
          />
          <FAQItem
            question="What happens if I exceed my message limit?"
            answer="On the Starter plan, you'll be notified when approaching the 100 message limit and can upgrade to Pro at any time for unlimited messages. Pro and Enterprise plans have no message caps."
          />
        </div>
      </section>
    </main>

    <footer class="flex flex-col md:flex-row justify-between items-center py-[32px] px-[32px] max-w-[1280px] mx-auto w-full border-t border-white/10 bg-black text-white/50">
      <div class="flex items-center gap-2 font-h3 text-h3 font-bold text-white">
        <img :src="orbitalLogo" alt="Orbital AI" class="w-8 h-8 object-contain" />
        <span>Orbital AI</span>
      </div>
      <div class="font-label-caps text-label-caps tracking-wider text-white/50">© {{ currentYear }} Orbital AI. ALL RIGHTS RESERVED</div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import Navbar from '@/components/layout/Navbar.vue'
import PricingCard from '@/components/pricing/PricingCard.vue'
import FAQItem from '@/components/pricing/FAQItem.vue'

const router = useRouter()
const navigateTo = (path) => router.push(path)

const currentYear = new Date().getFullYear()
const orbitalLogo = '/assets/orbital-logo.png'
</script>

<style scoped>
/* Styles handled by Tailwind */
</style>