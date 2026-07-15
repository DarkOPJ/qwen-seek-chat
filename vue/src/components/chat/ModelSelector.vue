<template>
  <div class="flex items-center gap-1 p-1 bg-white/5 rounded-full border border-white/10">
    <button
      v-for="model in models"
      :key="model.id"
      :class="[
        'px-4 py-1.5 rounded-full text-xs font-medium transition-all',
        selectedModel === model.id
          ? 'bg-white/10 shadow-sm font-bold text-white'
          : 'text-on-secondary-container font-medium hover:text-white'
      ]"
      @click="selectModel(model.id)"
      :disabled="disabled"
    >
      {{ model.name }}
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: String,
  disabled: Boolean
})

const emit = defineEmits(['update:modelValue'])

const selectedModel = computed({
  get() { return props.modelValue },
  set(val) { emit('update:modelValue', val) }
})

const models = [
  { id: 'qwen3:1.7b', name: 'Qwen3.7-Max' },
  { id: 'deepseek-r1:1.5b', name: 'DeepSeek-V4' }
]

const selectModel = (modelId) => {
  if (!props.disabled) {
    selectedModel.value = modelId
  }
}
</script>

<style scoped>
/* Scoped styles if needed */
</style>