<template>
  <section class="min-h-screen flex flex-col justify-center px-[32px] max-w-[1280px] mx-auto pt-20">
    <div class="grid lg:grid-cols-2 gap-16 items-center" :class="{ 'opacity-100 translate-y-0': isLoaded, 'opacity-0 translate-y-10': !isLoaded }" style="transition: all 1s ease;">
      <div class="space-y-8">
        <h1 class="font-h1 text-h1 text-white leading-tight">
          Intelligence, <br>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-neural-indigo to-neural-purple">evolved.</span>
        </h1>
        <p class="font-body-lg text-body-lg text-on-tertiary-container max-w-lg">
          Access the world's most advanced reasoning engines in a single, unified workspace designed for precision and performance.
        </p>
        <div class="flex flex-wrap gap-4 pt-4">
          <button class="bg-white text-black px-8 py-4 rounded-full font-label-caps text-label-caps font-bold shadow-xl shadow-white/5 hover:bg-neutral-200 transition-all" @click="navigateTo('/chat')">
            Start Building
          </button>
        </div>
      </div>
      <div class="relative group">
        <div class="absolute -inset-4 bg-gradient-to-r from-neural-indigo/20 to-neural-purple/20 rounded-3xl blur-2xl group-hover:blur-3xl transition-all"></div>
        <div class="glass-panel rounded-3xl overflow-hidden animate-float">
          <img class="w-full h-auto" alt="Qwen Chat workspace interface showing dark-themed chat with code editor and AI responses" :src="heroImage" />
        </div>
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoaded = ref(false)

onMounted(() => {
  requestAnimationFrame(() => {
    isLoaded.value = true
  })
})

const navigateTo = (path) => router.push(path)

const heroImage = '/assets/hero-chat.png'
</script>

<style scoped>
/* Styles handled by Tailwind */
</style>