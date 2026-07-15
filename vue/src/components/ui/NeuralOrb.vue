<template>
  <div
    class="neural-orb fixed rounded-full blur-[120px] -z-10 opacity-15 pointer-events-none"
    :class="[
      position,
      size,
      `bg-${color}`,
      customClass
    ]"
    :style="style"
  />
</template>

<script setup>
defineProps({
  position: { type: String, default: 'orb-indigo' }, // orb-indigo, orb-violet, custom
  size: { type: String, default: 'w-[60vw] h-[60vw]' },
  color: { type: String, default: 'neural-indigo' },
  customClass: { type: String, default: '' },
  style: { type: Object, default: () => ({}) },
})
</script>

<style scoped>
.neural-orb {
  filter: blur(120px);
  border-radius: 50%;
  opacity: 0.15;
  pointer-events: none;
}

.orb-indigo {
  top: -20%;
  left: -10%;
  width: 60vw;
  height: 60vw;
  background: #6366F1;
}

.orb-violet {
  bottom: -20%;
  right: -10%;
  width: 60vw;
  height: 60vw;
  background: #A855F7;
}

.orb-enterprise-indigo {
  top: 25%;
  left: 25%;
  width: 500px;
  height: 500px;
  background: #6366F1;
  filter: blur(80px);
  opacity: 0.15;
}

.orb-enterprise-purple {
  bottom: 25%;
  right: 25%;
  width: 600px;
  height: 600px;
  background: #A855F7;
  filter: blur(80px);
  opacity: 0.15;
}
</style>