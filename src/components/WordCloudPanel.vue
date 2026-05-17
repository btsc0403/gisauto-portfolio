<template>
  <div class="keyword-graph">
    <div class="component-header">
      <div class="arrow"></div>
      <span>词云图</span>
    </div>
    <div class="word-cloud-container" ref="containerRef">
      <canvas
        ref="canvasRef"
        v-show="hasWords"
        :class="{ 'cloud-visible': cloudReady }"
      ></canvas>
      <div v-if="!hasWords" class="empty-state">
        <svg class="empty-icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M8 32a8 8 0 0 0 8 8h18a10 10 0 0 0 1-19.94A14 14 0 0 0 8.2 14.1 11 11 0 0 0 8 25v7z"
                stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.5"/>
          <path d="M18 28l4-4 4 4M22 24v10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.35"/>
        </svg>
        <span>点击建筑查看关键词</span>
      </div>

      <div
        v-if="tooltipData"
        class="cloud-tooltip"
        :style="{ left: tooltipData.x + 'px', top: tooltipData.y + 'px' }"
      >
        <span class="tooltip-word">{{ tooltipData.word }}</span>
        <span class="tooltip-divider">·</span>
        <span class="tooltip-count">{{ tooltipData.count }}次</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from "vue"
import { useBuildingStore } from "../stores/buildingStore"
import { getWordFrequencies, getGradientColorFn } from "../composables/useWordCloud"

const store = useBuildingStore()

let WordCloudFn: any = null

const canvasRef = ref<HTMLCanvasElement | null>(null)
const containerRef = ref<HTMLElement | null>(null)
const wordList = ref<[string, number][]>([])
const cloudReady = ref(false)
const tooltipData = ref<{ word: string; count: number; x: number; y: number } | null>(null)

const hasWords = computed(() => wordList.value.length > 0)

let renderTimer: ReturnType<typeof setTimeout> | null = null

async function ensureWordCloud() {
  if (!WordCloudFn) {
    try {
      const mod = await import("wordcloud")
      WordCloudFn = mod.default || mod
    } catch (e) {
      console.error("Failed to load wordcloud:", e)
    }
  }
  return WordCloudFn
}

async function renderCloud() {
  const canvas = canvasRef.value
  const container = containerRef.value
  if (!canvas || !container || wordList.value.length === 0) return

  const WC = await ensureWordCloud()
  if (!WC) return

  cloudReady.value = false

  const rect = container.getBoundingClientRect()
  const pad = 24
  const w = rect.width - pad * 2
  const h = rect.height - pad * 2
  if (w < 10 || h < 10) return

  canvas.width = w
  canvas.height = h
  canvas.style.width = w + "px"
  canvas.style.height = h + "px"

  const maxCount = wordList.value[0]?.[1] || 1
  const colorFn = getGradientColorFn(maxCount)
  const minFont = Math.max(9, w / 36)
  const maxFont = Math.min(w / 8, h / 2.8)

  try {
    WC(canvas, {
      list: wordList.value,
      gridSize: 2,
      weightFactor: (size: number) => {
        const t = size / maxCount
        return minFont + (maxFont - minFont) * Math.pow(t, 0.45)
      },
      fontFamily: '"Microsoft YaHei", "PingFang SC", "Noto Sans SC", system-ui, sans-serif',
      fontWeight: ((_word: string, weight: number) => {
        const ratio = weight / maxCount
        if (ratio > 0.65) return 700
        if (ratio > 0.35) return 600
        if (ratio > 0.15) return 500
        return 400
      }) as any,
      color: colorFn as any,
      backgroundColor: "transparent",
      rotateRatio: 0,
      shuffle: false,
      shape: "circle",
      ellipticity: 0.65,
      drawOutOfBound: false,
      shrinkToFit: true,
      clearCanvas: true,
      wait: 16,
      hover: (item: any, _dim: any, event: MouseEvent) => {
        if (item && event) {
          const cr = container.getBoundingClientRect()
          tooltipData.value = {
            word: item[0],
            count: item[1],
            x: event.clientX - cr.left + 14,
            y: event.clientY - cr.top - 30,
          }
        } else {
          tooltipData.value = null
        }
      },
    })
  } catch (e) {
    console.error("WordCloud render error:", e)
  }

  requestAnimationFrame(() => {
    cloudReady.value = true
  })
}

function scheduleRender() {
  if (renderTimer) clearTimeout(renderTimer)
  renderTimer = setTimeout(() => {
    renderCloud()
  }, 180)
}

watch(
  () => store.selectedBuildingDescription,
  async (desc) => {
    tooltipData.value = null
    if (!desc || desc === "loading" || desc === "暂无") {
      wordList.value = []
      cloudReady.value = false
      return
    }
    wordList.value = getWordFrequencies(desc, 25)
    await nextTick()
    scheduleRender()
  }
)

let resizeObserver: ResizeObserver | null = null
let themeObserver: MutationObserver | null = null

onMounted(() => {
  if (containerRef.value) {
    resizeObserver = new ResizeObserver(() => {
      if (hasWords.value) scheduleRender()
    })
    resizeObserver.observe(containerRef.value)
  }

  themeObserver = new MutationObserver((mutations) => {
    for (const m of mutations) {
      if (m.attributeName === "data-theme" && hasWords.value) {
        scheduleRender()
        break
      }
    }
  })
  themeObserver.observe(document.documentElement, { attributes: true })
})

onUnmounted(() => {
  resizeObserver?.disconnect()
  themeObserver?.disconnect()
  if (renderTimer) clearTimeout(renderTimer)
})
</script>

<style scoped>
.keyword-graph {
  flex: 1;
  min-width: 0;
  height: 20vh;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--glass-border);
  background: var(--glass-highlight), var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur)) saturate(1.4);
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.4);
  box-shadow: var(--glass-shadow);
  border-radius: var(--glass-radius);
  transition: all 0.4s ease;
  overflow: hidden;
}
.keyword-graph:hover {
  box-shadow: var(--glass-hover-shadow);
  border-color: var(--glass-hover-border);
}

.component-header {
  display: flex;
  align-items: center;
  padding: 8px 14px;
  flex-shrink: 0;
  opacity: 0.75;
}
.arrow {
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 8px solid var(--text-primary);
  margin-right: 5px;
  transition: border-color 0.4s;
}
.component-header span {
  font-weight: bold;
  font-size: 16px;
  font-family: "DengXian", "等线", sans-serif;
  color: var(--text-primary);
  transition: color 0.4s;
}

.word-cloud-container {
  position: relative;
  flex: 1;
  min-height: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 16px;
}

.word-cloud-container canvas {
  display: block;
  opacity: 0;
  transition: opacity 0.5s ease;
}
.word-cloud-container canvas.cloud-visible {
  opacity: 1;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 6px;
  user-select: none;
}
.empty-icon {
  width: 36px;
  height: 36px;
  color: var(--text-secondary);
  opacity: 0.3;
}
.empty-state span {
  font-size: 11px;
  color: var(--text-secondary);
  opacity: 0.35;
  font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
  letter-spacing: 1px;
}

.cloud-tooltip {
  position: absolute;
  pointer-events: none;
  padding: 5px 12px;
  background: var(--tooltip-bg, rgba(255, 255, 255, 0.95));
  border: 1px solid var(--tooltip-border, rgba(0,0,0,0.08));
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0,0,0,0.04);
  display: flex;
  gap: 4px;
  align-items: baseline;
  z-index: 10;
  white-space: nowrap;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}
.tooltip-word {
  font-size: 13px;
  font-weight: 700;
  color: var(--tooltip-text, #333);
  letter-spacing: 0.3px;
}
.tooltip-divider {
  font-size: 11px;
  color: var(--text-secondary, #aaa);
  opacity: 0.5;
}
.tooltip-count {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-secondary, #888);
}
</style>
