import { defineStore } from "pinia"
import { ref, watch } from "vue"

export interface ThemeOption {
  id: string
  name: string
  icon: string
}

export const THEMES: ThemeOption[] = [
  { id: "default", name: "银灰", icon: "🌫️" },
  { id: "dark", name: "暗夜", icon: "🌙" }
]

export const useThemeStore = defineStore("theme", () => {
  const currentTheme = ref(localStorage.getItem("app-theme") || "default")

  function setTheme(themeId: string) {
    currentTheme.value = themeId
    document.documentElement.setAttribute("data-theme", themeId)
    localStorage.setItem("app-theme", themeId)
  }

  function initTheme() {
    document.documentElement.setAttribute("data-theme", currentTheme.value)
  }

  watch(currentTheme, (val) => {
    document.documentElement.setAttribute("data-theme", val)
  })

  return { currentTheme, setTheme, initTheme }
})
