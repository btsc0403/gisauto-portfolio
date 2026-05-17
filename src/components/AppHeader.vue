<template>
  <header class="app-header">
    <div class="header-left">
      <img class="brand-logo" src="/logo.png" alt="Heritage Explorer" />
    </div>
    <nav class="header-nav">
      <router-link
        v-for="item in navItems"
        :key="item.key"
        :to="item.to"
        :class="['nav-link']"
        active-class="active"
        exact-active-class="active"
      >
        {{ item.label }}
      </router-link>
    </nav>
    <div class="header-right">
      <div class="theme-switcher">
        <button class="icon-btn" title="切换主题" @click="showPicker = !showPicker">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="5"/>
            <line x1="12" y1="1" x2="12" y2="3"/>
            <line x1="12" y1="21" x2="12" y2="23"/>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
            <line x1="1" y1="12" x2="3" y2="12"/>
            <line x1="21" y1="12" x2="23" y2="12"/>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
          </svg>
        </button>
        <div v-if="showPicker" class="theme-picker">
          <button
            v-for="t in themes"
            :key="t.id"
            :class="['theme-option', { selected: themeStore.currentTheme === t.id }]"
            @click="selectTheme(t.id)"
          >
            <span class="theme-icon">{{ t.icon }}</span>
            <span class="theme-name">{{ t.name }}</span>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue"
import { useThemeStore, THEMES } from "../stores/themeStore"
const themeStore = useThemeStore()
const themes = THEMES
const showPicker = ref(false)

const navItems = [
  { key: "portfolio", label: "Portfolio", to: "/portfolio" },
  { key: "introduce", label: "Introduce", to: "/introduce" },
  { key: "map", label: "Map", to: "/" }
]

function selectTheme(id: string) {
  themeStore.setTheme(id)
  showPicker.value = false
}

function handleClickOutside(e: MouseEvent) {
  const el = (e.target as HTMLElement).closest(".theme-switcher")
  if (!el) showPicker.value = false
}

onMounted(() => {
  themeStore.initTheme()
  document.addEventListener("click", handleClickOutside)
})
onUnmounted(() => document.removeEventListener("click", handleClickOutside))
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 50px;
  padding: 0 24px;
  background: var(--glass-highlight), var(--header-bg);
  backdrop-filter: blur(var(--header-blur)) saturate(1.4);
  -webkit-backdrop-filter: blur(var(--header-blur)) saturate(1.4);
  border-bottom: 1px solid var(--header-border);
  flex-shrink: 0;
  z-index: 100;
  transition: background-color 0.4s, border-color 0.4s;
}

.header-left { display: flex; align-items: center; }

.brand-logo {
  height: 36px;
  width: auto;
  object-fit: contain;
}

.header-nav { display: flex; align-items: center; gap: 48px; }

.nav-link {
  font-family: "DengXian", "等线", sans-serif;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.8px;
  color: var(--header-text);
  text-decoration: none;
  padding: 14px 0;
  border-bottom: 2px solid transparent;
  transition: color 0.3s, border-color 0.3s;
}
.nav-link:hover { color: var(--header-active); }
.nav-link.active { color: var(--header-active); border-bottom-color: var(--header-active); }

.header-right { display: flex; align-items: center; gap: 16px; }

.theme-switcher { position: relative; }

.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background: none;
  color: var(--header-text);
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.2s, color 0.2s;
  padding: 0;
  margin: 0;
}
.icon-btn:hover { background-color: var(--glass-bg); color: var(--header-active); }

.theme-picker {
  position: absolute;
  top: 44px;
  right: 0;
  background: var(--glass-highlight), var(--float-bg);
  backdrop-filter: blur(var(--float-blur)) saturate(1.4);
  -webkit-backdrop-filter: blur(var(--float-blur)) saturate(1.4);
  border: 1px solid var(--glass-border);
  border-radius: var(--glass-radius);
  box-shadow:
    0 1px 1px rgba(255, 255, 255, 0.3) inset,
    0 8px 32px rgba(0, 0, 0, 0.12);
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 140px;
  z-index: 200;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}

.theme-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text-primary);
  transition: background-color 0.2s;
}
.theme-option:hover { background-color: var(--glass-bg); }
.theme-option.selected {
  background-color: var(--header-active);
  color: #fff;
}
.theme-icon { font-size: 16px; }
.theme-name { font-family: "DengXian", "等线", sans-serif; }


</style>
