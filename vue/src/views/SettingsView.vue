<template>
  <div class="min-h-screen bg-background text-on-surface">
    <div class="bg-animation" aria-hidden="true"></div>
    <div class="neural-orb orb-indigo" aria-hidden="true"></div>
    <div class="neural-orb orb-violet" aria-hidden="true"></div>

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
          <a href="#" class="text-white/70 hover:text-white transition-colors font-body-md text-body-md" @click.prevent="navigateTo('/chat')">Workspace</a>
          <a href="#" class="text-white/70 hover:text-white transition-colors font-body-md text-body-md" @click.prevent="navigateTo('/pricing')">Pricing</a>
          <a href="#" class="text-white/70 hover:text-white transition-colors font-body-md text-body-md" @click.prevent="navigateTo('/enterprise')">Enterprise</a>
        </div>
        <button class="bg-white text-black px-6 py-2 rounded-full font-label-caps text-label-caps font-bold hover:opacity-80 transition-opacity active:scale-95 duration-200" @click="navigateTo('/chat')">
          Get Started
        </button>
      </div>
    </nav>

    <main class="relative z-10 pt-24">
      <div class="max-w-3xl mx-auto px-[32px] py-16">
        <div class="text-center mb-12">
          <h1 class="font-h1 text-h1-mobile md:text-h1 mb-4 text-white">Settings</h1>
          <p class="font-body-lg text-body-lg text-white/70">Manage your account, preferences, and integrations.</p>
        </div>

        <SettingsSection title="Profile" icon="person">
          <div class="flex items-center gap-4">
            <div class="w-16 h-16 rounded-full bg-gradient-to-tr from-neural-purple to-neural-rose p-[1.5px]">
              <div class="w-full h-full rounded-full bg-black flex items-center justify-center overflow-hidden">
                <span class="text-2xl font-bold text-white">JD</span>
              </div>
            </div>
            <div>
              <h3 class="font-h3 text-lg font-semibold text-white">John Developer</h3>
              <p class="text-on-secondary-container font-body-md">john@developer.com</p>
            </div>
          </div>
          <button class="mt-4 px-4 py-2 bg-white/10 border border-white/20 rounded-lg font-label-caps text-label-caps hover:bg-white/20 transition-colors">Edit Profile</button>
        </SettingsSection>

        <SettingsSection title="Models" icon="psychology">
          <div class="space-y-4">
            <div class="flex items-center justify-between p-4 bg-white/5 rounded-lg border border-white/10">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-neural-indigo/20 flex items-center justify-center">
                  <span class="material-symbols-outlined text-neural-indigo">smart_toy</span>
                </div>
                <div>
                  <h4 class="font-bold text-white">Qwen 2.5</h4>
                  <p class="text-xs text-on-tertiary-container">Primary model • 128k context</p>
                </div>
              </div>
              <span class="px-3 py-1 bg-accent-emerald/20 text-accent-emerald rounded-full font-mono-metrics text-xs">ACTIVE</span>
            </div>
            <div class="flex items-center justify-between p-4 bg-white/5 rounded-lg border border-white/10">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-neural-purple/20 flex items-center justify-center">
                  <span class="material-symbols-outlined text-neural-purple">bolt</span>
                </div>
                <div>
                  <h4 class="font-bold text-white">DeepSeek v3</h4>
                  <p class="text-xs text-on-tertiary-container">Reasoning model • 128k context</p>
                </div>
              </div>
              <span class="px-3 py-1 bg-white/10 text-white/50 rounded-full font-mono-metrics text-xs">Available</span>
            </div>
          </div>
        </SettingsSection>

        <SettingsSection title="API Keys" icon="vpn_key">
          <p class="text-white/70 font-body-md mb-4">Manage your API keys for programmatic access.</p>
          <div class="space-y-3">
            <div class="flex items-center justify-between p-4 bg-white/5 rounded-lg border border-white/10">
              <div>
                <h4 class="font-bold text-white">Production Key</h4>
                <p class="text-xs text-on-tertiary-container font-mono-metrics">sk_qw_••••••••••••••••••••••••</p>
              </div>
              <button class="px-3 py-1 bg-white/10 border border-white/20 rounded-lg font-label-caps text-label-caps text-sm hover:bg-white/20 transition-colors">Revoke</button>
            </div>
            <button class="w-full px-4 py-2 bg-neural-purple text-white rounded-lg font-label-caps text-label-caps hover:opacity-90 transition-opacity">Create New Key</button>
          </div>
        </SettingsSection>

        <SettingsSection title="Appearance" icon="palette">
          <div class="space-y-4">
            <label class="flex items-center justify-between cursor-pointer">
              <div>
                <h4 class="font-bold text-white">Dark Mode</h4>
                <p class="text-xs text-on-tertiary-container">Use dark theme (system default)</p>
              </div>
              <input type="checkbox" class="w-11 h-6 appearance-none bg-white/10 rounded-full relative checked:bg-neural-purple checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:w-5 after:h-5 after:bg-white after:rounded-full after:transition-all" checked />
            </label>
            <label class="flex items-center justify-between cursor-pointer">
              <div>
                <h4 class="font-bold text-white">Reduced Motion</h4>
                <p class="text-xs text-on-tertiary-container">Minimize animations and transitions</p>
              </div>
              <input type="checkbox" class="w-11 h-6 appearance-none bg-white/10 rounded-full relative after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:w-5 after:h-5 after:bg-white after:rounded-full after:transition-all" />
            </label>
          </div>
        </SettingsSection>

        <SettingsSection title="Danger Zone" icon="warning" variant="danger">
          <div class="space-y-4">
            <div class="p-4 bg-white/5 rounded-lg border border-white/10">
              <h4 class="font-bold text-white mb-2">Delete Account</h4>
              <p class="text-white/70 font-body-md text-sm mb-4">Permanently delete your account and all associated data. This action cannot be undone.</p>
              <button class="px-4 py-2 bg-neural-rose/20 text-neural-rose border border-neural-rose/30 rounded-lg font-label-caps text-label-caps hover:bg-neural-rose/30 transition-colors">Delete Account</button>
            </div>
          </div>
        </SettingsSection>
      </div>
    </main>

    <footer class="w-full py-[32px] md:py-[180px] bg-black border-t border-white/10 text-white relative overflow-hidden">
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

const router = useRouter()
const navigateTo = (path) => router.push(path)
</script>

<style scoped>
</style>