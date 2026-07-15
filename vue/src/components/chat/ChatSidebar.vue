<template>
  <aside 
    class="fixed lg:relative inset-y-0 left-0 z-40 w-[300px] transform transition-transform duration-300 ease-in-out bg-background/90 backdrop-blur-xl border-r border-white/10 flex flex-col"
    :class="{ '-translate-x-full': !sidebarOpen && !isDesktop }"
    aria-label="Chat sessions"
  >
    <!-- Mobile Overlay -->
    <div 
      v-if="sidebarOpen && !isDesktop" 
      class="fixed inset-0 bg-black/50 z-30 lg:hidden"
      @click="closeSidebar"
      aria-hidden="true"
    ></div>

    <!-- Sidebar Content -->
    <div class="flex-1 flex flex-col pt-24 lg:pt-24 pb-8 px-6 overflow-hidden">
      <!-- New Chat Button -->
      <button
        class="w-full flex items-center justify-between p-4 mb-8 bg-neural-purple text-white rounded-xl font-bold shadow-[0_0_20px_rgba(168,85,247,0.3)] hover:opacity-90 transition-all active:scale-95"
        @click="createNewSession"
        :disabled="chatStore.loading"
      >
        <span class="flex items-center gap-2">
          <span class="material-symbols-outlined">add_circle</span>
          <span>New Chat</span>
        </span>
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
        <!-- Pinned Section -->
        <template v-if="pinnedSessions.length > 0">
          <div>
            <h4 class="text-label-caps font-label-caps text-on-tertiary-container mb-3 uppercase tracking-widest text-[10px]">Pinned</h4>
            <div class="space-y-1">
              <SessionItem
                v-for="session in pinnedSessions"
                :key="session.id"
                :session="session"
                :is-active="chatStore.activeSessionId === session.id"
                :is-pinned="true"
              />
            </div>
          </div>
        </template>

        <!-- Recent Section -->
        <template v-if="filteredRecentSessions.length > 0">
          <div v-if="pinnedSessions.length > 0" class="pt-4 border-t border-white/10 mt-4">
            <h4 class="text-label-caps font-label-caps text-on-tertiary-container mb-3 uppercase tracking-widest text-[10px]">Recent</h4>
          </div>
          <template v-else>
            <h4 class="text-label-caps font-label-caps text-on-tertiary-container mb-3 uppercase tracking-widest text-[10px]">Recent</h4>
          </template>
          <div class="space-y-1">
            <SessionItem
              v-for="session in filteredRecentSessions"
              :key="session.id"
              :session="session"
              :is-active="chatStore.activeSessionId === session.id"
              :is-pinned="false"
            />
          </div>
        </template>

        <!-- Empty State -->
        <div v-if="pinnedSessions.length === 0 && filteredRecentSessions.length === 0 && !chatStore.loading" class="text-center py-12 text-on-tertiary-container">
          <span class="material-symbols-outlined text-4xl mb-3 block">chat_bubble_outline</span>
          <p class="text-sm">No conversations yet</p>
          <p class="text-xs mt-1">Start a new chat to begin</p>
        </div>

        <!-- Loading State -->
        <div v-if="chatStore.loading" class="space-y-3">
          <div v-for="i in 3" :key="i" class="skeleton h-12 rounded-lg"></div>
        </div>
      </div>

      <!-- Bottom User Section -->
      <div class="mt-auto pt-6 border-t border-white/10 space-y-4">
        <div class="flex items-center gap-3 p-2">
          <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-neural-purple to-neural-rose p-[1.5px]">
            <div class="w-full h-full rounded-full bg-black flex items-center justify-center overflow-hidden">
              <span class="material-symbols-outlined text-white text-lg">person</span>
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-bold text-white truncate">Guest User</p>
            <p class="text-xs text-on-tertiary-container">Free tier</p>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useChatStore } from '@/stores/chat'
import { useUIStore } from '@/stores/ui'
import SessionItem from './SessionItem.vue'

const router = useRouter()
const chatStore = useChatStore()
const uiStore = useUIStore()

const searchQuery = ref('')
const isDesktop = ref(window.innerWidth >= 1024)

const sidebarOpen = computed(() => uiStore.sidebarOpen)

const pinnedSessions = computed(() => 
  chatStore.sessions.filter(s => s.is_pinned)
)

const recentSessions = computed(() => 
  chatStore.sessions.filter(s => !s.is_pinned)
)

const filteredRecentSessions = computed(() => {
  if (!searchQuery.value) return recentSessions.value
  const query = searchQuery.value.toLowerCase()
  return recentSessions.value.filter(s => 
    s.title?.toLowerCase().includes(query)
  )
})

const createNewSession = async () => {
  const session = await chatStore.createSession('New Chat', modelStore.selectedModel)
  if (session) {
    await chatStore.setActiveSession(session.id)
    if (!isDesktop.value) {
      uiStore.setSidebarOpen(false)
    }
  }
}

const closeSidebar = () => {
  uiStore.setSidebarOpen(false)
}

watch(() => window.innerWidth, (width) => {
  isDesktop.value = width >= 1024
  if (isDesktop.value) {
    uiStore.setSidebarOpen(true)
  }
})

onMounted(() => {
  isDesktop.value = window.innerWidth >= 1024
  if (!isDesktop.value) {
    uiStore.setSidebarOpen(false)
  }
  window.addEventListener('resize', handleResize)
})

const handleResize = () => {
  const wasDesktop = isDesktop.value
  isDesktop.value = window.innerWidth >= 1024
  if (isDesktop.value && !wasDesktop) {
    uiStore.setSidebarOpen(true)
  }
}
</script>

<script>
import { useModelStore } from '@/stores/model'
const modelStore = useModelStore()
export default {
  name: 'ChatSidebar'
}
</script>

<style scoped>
/* Scoped styles if needed */
</style>