<template>
  <nav class="docked full-width glass-panel border-b border-white/10">
    <div class="max-w-[1280px] mx-auto px-[32px] h-20 flex justify-between items-center">
      <!-- Logo -->
      <div class="flex items-center gap-2">
        <svg class="w-8 h-8" viewBox="0 0 32 32" fill="none" aria-hidden="true">
          <rect width="32" height="32" rx="8" fill="#000"/>
          <path d="M8 16C8 11.5817 11.5817 8 16 8C20.4183 8 24 11.5817 24 16C24 20.4183 20.4183 24 16 24C11.5817 24 8 20.4183 8 16Z" stroke="#A855F7" stroke-width="2"/>
          <path d="M16 8V16L21 19" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="font-h3 text-h3 font-bold text-white">Orbital AI</span>
      </div>

      <!-- Desktop Navigation -->
      <div class="hidden md:flex items-center gap-8 absolute left-1/2 -translate-x-1/2">
        <NavLink :to="{ name: 'home' }" :active="isActive('home')">Home</NavLink>
        <NavLink :to="{ name: 'chat' }" :active="isActive('chat')">Workspace</NavLink>
        <NavLink :to="{ name: 'pricing' }" :active="isActive('pricing')">Pricing</NavLink>
        <NavLink :to="{ name: 'enterprise' }" :active="isActive('enterprise')">Enterprise</NavLink>
      </div>

      <!-- Desktop CTA -->
      <button class="hidden md:block bg-white text-black px-6 py-2 rounded-full font-label-caps text-label-caps font-bold hover:opacity-80 transition-opacity active:scale-95 duration-200" @click="navigateToChat">
        Get Started
      </button>

      <!-- Mobile Menu Button -->
      <button 
        class="md:hidden p-2 rounded-lg hover:bg-white/5 text-on-secondary-container hover:text-white transition-colors"
        @click="toggleMobileMenu"
        aria-label="Toggle menu"
        aria-expanded="mobileMenuOpen"
      >
        <span class="material-symbols-outlined text-xl" :class="{ 'rotate-90': mobileMenuOpen }">menu</span>
      </button>
    </div>

    <!-- Mobile Menu Dropdown -->
    <div 
      v-if="mobileMenuOpen" 
      class="md:hidden absolute top-full left-0 right-0 bg-black/95 backdrop-blur-xl border-b border-white/10 py-6 px-[32px] z-50 animate-slide-down"
    >
      <div class="flex flex-col items-center gap-4">
        <NavLink :to="{ name: 'home' }" :active="isActive('home')" @click="closeMobileMenu">Home</NavLink>
        <NavLink :to="{ name: 'chat' }" :active="isActive('chat')" @click="closeMobileMenu">Workspace</NavLink>
        <NavLink :to="{ name: 'pricing' }" :active="isActive('pricing')" @click="closeMobileMenu">Pricing</NavLink>
        <NavLink :to="{ name: 'enterprise' }" :active="isActive('enterprise')" @click="closeMobileMenu">Enterprise</NavLink>
        <div class="w-full pt-4 border-t border-white/10"></div>
        <button class="w-full bg-white text-black px-6 py-3 rounded-full font-label-caps text-label-caps font-bold hover:opacity-80 transition-opacity active:scale-95 duration-200" @click="navigateToChat">
          Get Started
        </button>
      </div>
    </div>

    <!-- Mobile Overlay -->
    <div 
      v-if="mobileMenuOpen" 
      class="md:hidden fixed inset-0 z-40 bg-black/50 backdrop-blur-sm"
      @click="closeMobileMenu"
      aria-hidden="true"
    ></div>
  </nav>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()
const route = useRoute()

const mobileMenuOpen = ref(false)

const isActive = (name) => {
  return route.name === name
}

const navigateToChat = () => {
  router.push({ name: 'chat' })
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}
</script>

<style scoped>
/* NavLink styles are handled by the component below */
</style>