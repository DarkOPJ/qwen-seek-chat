<template>
  <div class="h-screen overflow-hidden bg-background text-on-surface">
    <!-- Background Animation -->
    <div class="bg-animation" aria-hidden="true"></div>
    <div class="neural-orb orb-indigo" aria-hidden="true"></div>
    <div class="neural-orb orb-violet" aria-hidden="true"></div>

    <!-- Navigation -->
    <Navbar />

    <main class="relative z-10">
      <div class="flex h-[calc(100vh-6rem)]">
        <!-- Sidebar -->
        <aside
          :class="[
            'w-[300px] h-full pt-24 pb-8 px-6 flex flex-col glass shrink-0 transition-transform duration-300 ease-out z-50',
            uiStore.sidebarOpen ? 'translate-x-0' : '-translate-x-full min-nav:translate-x-0'
          ]"
          aria-label="Chat sessions"
        >
          <!-- New Chat Button -->
          <button
            class="w-full flex items-center justify-center gap-2 p-4 mb-8 bg-neural-purple text-white rounded-xl font-bold shadow-[0_0_20px_rgba(168,85,247,0.3)] hover:opacity-90 transition-all active:scale-95"
          >
            <span class="material-symbols-outlined">add_circle</span>
            <span>New Chat</span>
          </button>

          <!-- Search -->
          <div class="relative mb-6">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 material-symbols-outlined text-on-tertiary-container">search</span>
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search conversations..."
              class="w-full pl-10 pr-4 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-white placeholder-on-tertiary-container focus:ring-1 focus:ring-neural-purple/50 outline-none"
            />
          </div>

          <!-- History -->
          <div class="flex-1 overflow-y-auto scrollbar-hide space-y-6 min-h-0">
            <!-- Pinned -->
            <div>
              <h4 class="text-label-caps font-label-caps text-on-tertiary-container mb-3 uppercase tracking-widest text-[10px]">Pinned</h4>
              <div class="space-y-1">
               <div
                  v-for="item in pinnedItems"
                  :key="item.title"
                  class="flex items-center gap-3 py-2.5 px-3 rounded-lg text-sm text-on-secondary-container hover:bg-white/5 hover:text-white transition-colors cursor-pointer"
                >
                  <span class="material-symbols-outlined text-[16px] text-on-tertiary-container shrink-0">{{ item.icon }}</span>
                  <span class="truncate">{{ item.title }}</span>
                </div>
              </div>
            </div>

            <!-- Recent -->
            <div class="pt-4 border-t border-white/10">
              <h4 class="text-label-caps font-label-caps text-on-tertiary-container mb-3 uppercase tracking-widest text-[10px]">Recent</h4>
              <div class="space-y-1">
                <div
                  v-for="item in recentItems"
                  :key="item.title"
                  class="flex items-center gap-3 py-2.5 px-3 rounded-lg text-sm text-on-secondary-container hover:bg-white/5 hover:text-white transition-colors cursor-pointer"
                >
                  <span class="material-symbols-outlined text-[16px] text-on-tertiary-container shrink-0">{{ item.icon }}</span>
                  <span class="truncate">{{ item.title }}</span>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="pinnedItems.length === 0 && recentItems.length === 0" class="text-center py-12 text-on-tertiary-container">
              <span class="material-symbols-outlined text-4xl mb-3 block">chat_bubble_outline</span>
              <p class="text-sm">No conversations yet</p>
            </div>
          </div>

          <!-- User Profile -->
          <div class="mt-4 pt-4 border-t border-white/10 flex items-center gap-3">
            <div class="w-9 h-9 rounded-full bg-neural-purple/30 flex items-center justify-center text-xs font-bold text-white shrink-0">
              AR
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-white truncate">Alex Rivera</p>
              <p class="text-xs text-on-tertiary-container truncate">alex@orbital.ai</p>
            </div>
            <button class="p-1.5 rounded-lg hover:bg-white/5 transition-colors text-on-tertiary-container hover:text-white" title="Settings">
              <span class="material-symbols-outlined !text-[18px]">more_vert</span>
            </button>
          </div>
        </aside>

        <!-- Main Chat Area -->
        <section class="flex-1 h-full flex flex-col relative z-10 overflow-hidden">
          <ChatWindow />
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useUIStore } from '@/stores/ui'
import ChatWindow from '@/components/chat/ChatWindow.vue'
import Navbar from '@/components/layout/Navbar.vue'

const chatStore = useChatStore()
const uiStore = useUIStore()

const searchQuery = ref('')

const pinnedItems = ref([
  { icon: 'architecture', title: 'System Architecture v2' },
  { icon: 'description', title: 'Orbital API Documentation' },
])

const recentItems = ref([
  { icon: 'code', title: 'Next.js 14 Server Actions' },
  { icon: 'speed', title: 'React Native performance' },
  { icon: 'storage', title: 'Data scrubbing strategies' },
])

onMounted(async () => {
  await chatStore.fetchSessions()
})
</script>
