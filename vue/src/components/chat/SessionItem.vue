<template>
  <button
    class="w-full flex items-center gap-3 p-3 rounded-lg transition-colors text-left group"
    :class="[
      isActive ? 'bg-white/10 border border-white/10' : 'hover:bg-white/5',
      isPinned ? '' : ''
    ]"
    @click="selectSession"
    @contextmenu.prevent="showContextMenu = true"
  >
    <span 
      class="material-symbols-outlined flex-shrink-0"
      :class="isPinned ? 'text-neural-purple' : 'text-on-secondary-container'"
    >
      {{ isPinned ? 'push_pin' : 'chat_bubble' }}
    </span>
    <span class="text-sm font-medium text-white/90 truncate flex-1 min-w-0">
      {{ session.title || 'Untitled' }}
    </span>
    <span v-if="session.model_name" class="flex-shrink-0 text-[10px] font-mono-metrics text-on-tertiary-container px-1.5 py-0.5 rounded bg-white/5">
      {{ formatModelName(session.model_name) }}
    </span>
  </button>

  <!-- Context Menu -->
  <Teleport to="body">
    <div 
      v-if="showContextMenu" 
      class="fixed z-50 glass-panel rounded-lg p-2 min-w-[160px] shadow-xl border border-white/10"
      :style="{ top: menuPosition.y + 'px', left: menuPosition.x + 'px' }"
    >
      <button 
        class="w-full flex items-center gap-2 px-3 py-2 rounded text-sm text-white hover:bg-white/5 transition-colors"
        @click="pinSession"
      >
        <span class="material-symbols-outlined text-sm">{{ isPinned ? 'push_pin' : 'push_pin' }}</span>
        {{ isPinned ? 'Unpin' : 'Pin' }}
      </button>
      <button 
        class="w-full flex items-center gap-2 px-3 py-2 rounded text-sm text-white hover:bg-white/5 transition-colors"
        @click="renameSession"
      >
        <span class="material-symbols-outlined text-sm">edit</span>
        Rename
      </button>
      <button 
        class="w-full flex items-center gap-2 px-3 py-2 rounded text-sm text-neural-rose hover:bg-white/5 transition-colors"
        @click="deleteSession"
      >
        <span class="material-symbols-outlined text-sm">delete</span>
        Delete
      </button>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useUIStore } from '@/stores/ui'

const props = defineProps({
  session: Object,
  isActive: Boolean,
  isPinned: Boolean
})

const emit = defineEmits(['select', 'pin', 'rename', 'delete'])
const chatStore = useChatStore()
const uiStore = useUIStore()

const showContextMenu = ref(false)
const menuPosition = ref({ x: 0, y: 0 })

const formatModelName = (model) => {
  if (model.includes('qwen3:1.7b')) return 'Qwen 3'
  if (model.includes('deepseek-r1:1.5b')) return 'DeepSeek'
  return model.split(':')[0]
}

const selectSession = () => {
  chatStore.setActiveSession(props.session.id)
  if (!uiStore.isDesktop) {
    uiStore.setSidebarOpen(false)
  }
}

const pinSession = async () => {
  await chatStore.togglePin(props.session.id)
  showContextMenu.value = false
}

const renameSession = () => {
  const newTitle = prompt('Enter new title:', props.session.title)
  if (newTitle && newTitle.trim()) {
    chatStore.updateSession(props.session.id, { title: newTitle.trim() })
  }
  showContextMenu.value = false
}

const deleteSession = async () => {
  if (confirm('Delete this conversation?')) {
    await chatStore.deleteSession(props.session.id)
  }
  showContextMenu.value = false
}

const handleContextMenu = (e) => {
  e.preventDefault()
  menuPosition.value = { x: e.clientX, y: e.clientY }
  showContextMenu.value = true
}

document.addEventListener('click', () => {
  showContextMenu.value = false
})
</script>

<style scoped>
/* Scoped styles */
</style>