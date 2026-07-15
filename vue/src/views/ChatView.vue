<template>
  <div class="min-h-screen bg-background text-on-surface">
    <!-- Background Animation -->
    <div class="bg-animation" aria-hidden="true"></div>
    <div class="neural-orb orb-indigo" aria-hidden="true"></div>
    <div class="neural-orb orb-violet" aria-hidden="true"></div>

    <!-- Navigation -->
    <nav class="docked full-width glass-panel border-b border-white/10">
      <div class="max-w-[1280px] mx-auto px-[32px] h-20 flex justify-between items-center">
        <div class="flex items-center gap-2">
          <svg class="w-8 h-8" viewBox="0 0 32 32" fill="none" aria-hidden="true">
            <rect width="32" height="32" rx="8" fill="#000"/>
            <path d="M8 16C8 11.5817 11.5817 8 16 8C20.4183 8 24 11.5817 24 16C24 20.4183 20.4183 24 16 24C11.5817 24 8 20.4183 8 16Z" stroke="#A855F7" stroke-width="2"/>
            <path d="M16 8V16L21 19" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
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

    <!-- Mobile Menu Button -->
    <button 
      v-if="uiStore.sidebarOpen"
      class="md:hidden fixed top-24 left-4 z-50 p-2 glass-panel rounded-lg shadow-lg"
      @click="uiStore.toggleSidebar"
      aria-label="Close sidebar"
    >
      <span class="material-symbols-outlined">close</span>
    </button>
    <button 
      v-else
      class="md:hidden fixed top-24 left-4 z-50 p-2 glass-panel rounded-lg shadow-lg"
      @click="uiStore.toggleSidebar"
      aria-label="Open sidebar"
    >
      <span class="material-symbols-outlined">menu</span>
    </button>

    <!-- Sidebar Overlay (Mobile) -->
    <div 
      v-if="uiStore.sidebarOpen" 
      class="md:hidden fixed inset-0 z-40 bg-black/50 backdrop-blur-sm"
      @click="uiStore.setSidebarOpen(false)"
      aria-hidden="true"
    ></div>

    <main class="relative z-10 pt-24 md:pt-24">
      <div class="flex h-[calc(100vh-6rem)]">
        <!-- Sidebar -->
        <aside 
          :class="[
            'w-[300px] h-full pt-24 pb-8 px-6 flex flex-col glass z-40 shrink-0 transition-transform duration-300 ease-out',
            uiStore.sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
          ]"
        >
          <ChatSidebar />
        </aside>

        <!-- Main Chat Area -->
        <section class="flex-1 h-full flex flex-col relative z-10 overflow-hidden">
          <!-- Top Toolbar / Model Selector -->
          <div class="h-16 px-8 flex items-center justify-between bg-black/20 backdrop-blur-sm border-b border-white/5">
            <div class="flex items-center gap-4">
              <ModelSelector />
              <div class="h-4 w-[1px] bg-white/10 mx-2"></div>
              <div class="flex items-center gap-2 text-on-tertiary-container">
                <span class="material-symbols-outlined !text-[16px] text-neural-purple">bolt</span>
                <span class="text-xs font-medium">Turbo Mode Active</span>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button class="p-2 rounded-lg hover:bg-white/5 text-on-secondary-container hover:text-white transition-colors" title="Share">
                <span class="material-symbols-outlined">share</span>
              </button>
            </div>
          </div>

          <!-- Chat Window -->
          <div class="flex-1 overflow-hidden">
            <ChatWindow />
          </div>
        </section>
      </div>
    </main>

    <!-- Footer -->
    <footer class="w-full py-[32px] md:py-[32px] bg-black border-t border-white/10 text-white relative overflow-hidden">
      <div class="max-w-[1280px] mx-auto px-[32px] flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="flex items-center gap-2 font-h3 text-h3 font-bold text-white">
          <svg class="w-8 h-8" viewBox="0 0 32 32" fill="none" aria-hidden="true">
            <rect width="32" height="32" rx="8" fill="#000"/>
            <path d="M8 16C8 11.5817 11.5817 8 16 8C20.4183 8 24 11.5817 24 16C24 20.4183 20.4183 24 16 24C11.5817 24 8 20.4183 8 16Z" stroke="#A855F7" stroke-width="2"/>
            <path d="M16 8V16L21 19" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Qwen Chat</span>
        </div>
        <p class="font-label-caps text-label-caps tracking-wider text-white/50">© 2025 QWEN CHAT. ALL RIGHTS RESERVED</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useChatStore } from '@/stores/chat'
import { useUIStore } from '@/stores/ui'
import ChatSidebar from '@/components/chat/ChatSidebar.vue'
import ChatWindow from '@/components/chat/ChatWindow.vue'
import ModelSelector from '@/components/chat/ModelSelector.vue'

const router = useRouter()
const chatStore = useChatStore()
const uiStore = useUIStore()

const navigateTo = (path) => {
  router.push(path)
}

// Initialize chat store on mount
import { onMounted } from 'vue'
onMounted(async () => {
  await chatStore.fetchSessions()
})
</script>

<style scoped>
/* Component-specific styles if needed */
</style>