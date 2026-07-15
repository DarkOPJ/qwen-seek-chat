<template>
  <div class="relative aspect-square md:aspect-video lg:aspect-square bg-black/40 rounded-2xl border border-white/10 overflow-hidden shadow-2xl">
    <div class="absolute inset-0 flex items-center justify-center p-12">
      <div class="w-full h-full border border-white/5 rounded-full relative animate-[spin_60s_linear_infinite]">
        <div class="absolute top-0 left-1/2 -translate-x-1/2 w-4 h-4 bg-neural-indigo rounded-full shadow-[0_0_20px_#6366F1]"></div>
        <div class="absolute bottom-1/4 left-0 w-3 h-3 bg-accent-emerald rounded-full shadow-[0_0_15px_#10B981]"></div>
        <div class="absolute top-1/2 right-0 w-3 h-3 bg-neural-purple rounded-full shadow-[0_0_15px_#A855F7]"></div>
      </div>
      <div class="absolute w-3/4 h-3/4 border border-white/5 rounded-full animate-[spin_40s_linear_infinite_reverse]"></div>
      <div class="absolute w-1/2 h-1/2 border border-white/10 rounded-full flex items-center justify-center bg-black/60 backdrop-blur-md">
        <span class="material-symbols-outlined text-primary text-6xl">language</span>
      </div>
    </div>
    <div class="absolute bottom-6 left-6 right-6 flex justify-between">
      <div class="bg-white/10 backdrop-blur-md border border-white/20 p-3 rounded-lg flex items-center gap-3">
        <div class="w-2 h-2 rounded-full bg-accent-emerald"></div>
        <span class="text-[10px] font-mono-metrics text-primary uppercase">Nodes Active: 142</span>
      </div>
      <div class="bg-white/10 backdrop-blur-md border border-white/20 p-3 rounded-lg flex items-center gap-3">
        <div class="w-2 h-2 rounded-full bg-neural-indigo"></div>
        <span class="text-[10px] font-mono-metrics text-primary uppercase">Latency: 24ms</span>
      </div>
    </div>
  </div>
</template>

<script setup>
// Static visualization component
</script>

<style scoped>
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-\[spin_60s_linear_infinite\] {
  animation: spin 60s linear infinite;
}

.animate-\[spin_40s_linear_infinite_reverse\] {
  animation: spin 40s linear infinite reverse;
}
</style>