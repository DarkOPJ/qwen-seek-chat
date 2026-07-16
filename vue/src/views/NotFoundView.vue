<template>
  <div class="min-h-screen bg-background text-on-surface flex items-center justify-center">
    <div class="bg-animation" aria-hidden="true"></div>
    <div class="neural-orb orb-indigo" aria-hidden="true"></div>
    <div class="neural-orb orb-violet" aria-hidden="true"></div>

    <Navbar />

    <div class="relative z-10 text-center px-8">
      <div class="mb-8">
        <span class="font-mono-metrics text-6xl text-neural-purple/50">404</span>
      </div>
      <h1 class="font-h1 text-h1-mobile md:text-h1 mb-6 text-white">Page Not Found</h1>
      <p class="font-body-lg text-body-lg text-white/70 max-w-md mx-auto mb-10">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <button class="px-8 py-4 rounded-full bg-white text-black font-label-caps text-label-caps font-bold hover:bg-zinc-200 transition-all" @click="goHome">
          Go Home
        </button>
        <button class="px-8 py-4 rounded-full border border-white/20 text-white font-label-caps text-label-caps font-bold hover:bg-white/10 transition-colors" @click="goBack">
          Go Back
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import Navbar from '@/components/layout/Navbar.vue'

const router = useRouter()

const goHome = () => router.push('/')
const goBack = () => router.back()
</script>

<style scoped>
</style>