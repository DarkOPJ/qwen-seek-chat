<template>
  <button
    class="text-white/70 hover:text-white transition-colors font-body-md text-body-md py-2 cursor-pointer bg-transparent border-none"
    :class="{ 'text-white font-semibold border-b-2 border-white pb-1': active }"
    @click="navigate"
  >
    <slot />
  </button>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  to: {
    type: [String, Object],
    required: true
  },
  active: {
    type: Boolean,
    default: false
  }
})

const router = useRouter()

function navigate() {
  router.push(props.to)
}
</script>