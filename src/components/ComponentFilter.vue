<template>
  <div class="component-filter">
    <div class="component-header">
      <div class="arrow"></div>
      <span>构件筛选</span>
      <button
        v-if="store.selectedFeatures.length > 0"
        class="clear-btn"
        @click="clearAll"
        title="清除筛选"
      >清除</button>
    </div>

    <div class="tag-scroll" ref="scrollRef">
      <div v-if="loading" class="loading-state">
        <span class="spinner"></span>
        <span>加载构件数据…</span>
      </div>

      <div v-else-if="features.length === 0" class="empty-state">
        <svg class="empty-icon" viewBox="0 0 48 48" fill="none">
          <rect x="6" y="10" width="36" height="28" rx="4" stroke="currentColor" stroke-width="1.5" opacity="0.4"/>
          <path d="M14 22h8M14 28h12M30 18l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.35"/>
        </svg>
        <span>暂无构件数据</span>
      </div>

      <div v-else class="tag-wall">
        <div
          v-for="(f, idx) in features"
          :key="f.name"
          class="tag-item"
          :class="{ active: store.selectedFeatures.includes(f.name) }"
          :style="tagStyle(idx, store.selectedFeatures.includes(f.name))"
          @click="toggleFeature(f.name)"
        >
          <span class="tag-name" :style="{ color: store.selectedFeatures.includes(f.name) ? tagColor(idx) : undefined }">{{ f.name }}</span>
          <div class="tag-bar-track">
            <div
              class="tag-bar-fill"
              :style="barStyle(idx, f.count, store.selectedFeatures.includes(f.name))"
            ></div>
          </div>
          <span class="tag-count" :style="{ color: store.selectedFeatures.includes(f.name) ? tagColor(idx) : undefined }">{{ f.count }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useBuildingStore } from "../stores/buildingStore"

interface FeatureItem {
  name: string
  count: number
}

const TAG_PALETTE = [
  { h: 210, s: 70, l: 52 },  // 蓝
  { h: 160, s: 55, l: 42 },  // 青绿
  { h: 32,  s: 75, l: 50 },  // 琥珀
  { h: 280, s: 50, l: 55 },  // 紫
  { h: 350, s: 60, l: 55 },  // 玫红
  { h: 120, s: 45, l: 42 },  // 绿
  { h: 190, s: 65, l: 45 },  // 深青
  { h: 45,  s: 70, l: 48 },  // 金黄
  { h: 240, s: 50, l: 58 },  // 靛蓝
  { h: 5,   s: 65, l: 52 },  // 赤红
  { h: 80,  s: 50, l: 44 },  // 橄榄绿
  { h: 310, s: 45, l: 52 },  // 洋红
]

function tagHSL(index: number) {
  const p = TAG_PALETTE[index % TAG_PALETTE.length]
  const shift = Math.floor(index / TAG_PALETTE.length) * 25
  return { h: (p.h + shift) % 360, s: p.s, l: p.l }
}

function tagColor(index: number) {
  const { h, s, l } = tagHSL(index)
  return `hsl(${h}, ${s}%, ${l}%)`
}

function tagStyle(index: number, active: boolean) {
  const { h, s } = tagHSL(index)
  if (active) {
    return {
      borderColor: `hsla(${h}, ${s}%, 50%, 0.6)`,
      background: `hsla(${h}, ${s}%, 50%, 0.14)`,
      boxShadow: `0 1px 8px hsla(${h}, ${s}%, 50%, 0.15)`,
    }
  }
  return {
    borderColor: `hsla(${h}, ${s}%, 50%, 0.2)`,
    background: `hsla(${h}, ${s}%, 50%, 0.05)`,
  }
}

function barStyle(index: number, count: number, active: boolean) {
  const { h, s } = tagHSL(index)
  const MIN_W = 10
  const MAX_W = 100
  const ratio = count / maxCount.value
  const w = MIN_W + (MAX_W - MIN_W) * Math.pow(ratio, 0.55)
  const alpha = active ? 0.85 : 0.5
  return {
    width: w + '%',
    background: `linear-gradient(90deg, hsla(${h}, ${s}%, 55%, ${alpha * 0.6}), hsla(${h}, ${s}%, 45%, ${alpha}))`,
  }
}

const store = useBuildingStore()
const features = ref<FeatureItem[]>([])
const loading = ref(true)
const maxCount = ref(1)

const featureBuildingsCache = ref<Record<string, string[]>>({})

async function fetchFeatures() {
  loading.value = true
  try {
    const res = await fetch("http://localhost:8000/kg/features")
    if (!res.ok) throw new Error("fetch failed")
    const data: FeatureItem[] = await res.json()
    features.value = data
    maxCount.value = data.length > 0 ? data[0].count : 1
  } catch (e) {
    console.error("Failed to load features:", e)
    features.value = []
  } finally {
    loading.value = false
  }
}

async function fetchBuildingsForFeature(featureName: string): Promise<string[]> {
  if (featureBuildingsCache.value[featureName]) {
    return featureBuildingsCache.value[featureName]
  }
  try {
    const res = await fetch(`http://localhost:8000/kg/feature-buildings?feature=${encodeURIComponent(featureName)}&limit=200`)
    if (!res.ok) throw new Error("fetch failed")
    const data = await res.json()
    const names = data.map((b: any) => b.name as string)
    featureBuildingsCache.value[featureName] = names
    return names
  } catch (e) {
    console.error("Failed to fetch buildings for feature:", featureName, e)
    return []
  }
}

const emit = defineEmits<{
  (e: "filterChanged", buildingNames: string[], isFiltering: boolean): void
}>()

async function toggleFeature(name: string) {
  const arr = store.selectedFeatures
  const idx = arr.indexOf(name)
  if (idx !== -1) {
    arr.splice(idx, 1)
  } else {
    arr.push(name)
    await fetchBuildingsForFeature(name)
  }
  await emitFilter()
}

function clearAll() {
  store.selectedFeatures.splice(0)
  emit("filterChanged", [], false)
}

async function emitFilter() {
  if (store.selectedFeatures.length === 0) {
    emit("filterChanged", [], false)
    return
  }
  const sets: Set<string>[] = []
  for (const f of store.selectedFeatures) {
    const buildings = await fetchBuildingsForFeature(f)
    sets.push(new Set(buildings))
  }
  let intersection = sets[0]
  for (let i = 1; i < sets.length; i++) {
    intersection = new Set([...intersection].filter(n => sets[i].has(n)))
  }
  emit("filterChanged", Array.from(intersection), true)
}

onMounted(() => {
  fetchFeatures()
})
</script>

<style scoped>
.component-filter {
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
.component-filter:hover {
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
  width: 0; height: 0;
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

.clear-btn {
  margin-left: auto;
  padding: 1px 10px;
  font-size: 11px;
  font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
  border: 1px solid rgba(140, 180, 220, 0.4);
  border-radius: 10px;
  background: rgba(100, 160, 220, 0.12);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  line-height: 1.6;
}
.clear-btn:hover {
  background: rgba(100, 160, 220, 0.25);
  color: var(--text-primary);
}

.tag-scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0 16px 10px 12px;
}
.tag-scroll::-webkit-scrollbar { width: 3px; }
.tag-scroll::-webkit-scrollbar-thumb {
  background: rgba(120, 160, 200, 0.25);
  border-radius: 3px;
}

.tag-wall {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 14px;
  border: 1px solid rgba(140, 180, 220, 0.25);
  background: rgba(140, 180, 220, 0.06);
  cursor: pointer;
  transition: all 0.22s ease;
  user-select: none;
  flex-shrink: 0;
}
.tag-item:hover {
  filter: brightness(1.08);
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.08);
}
.tag-item.active .tag-name {
  font-weight: 600;
}

.tag-name {
  font-size: 12px;
  font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
  color: var(--text-primary);
  white-space: nowrap;
  line-height: 1.3;
  transition: color 0.2s;
}

.tag-bar-track {
  width: 64px;
  height: 4px;
  background: rgba(140, 180, 220, 0.12);
  border-radius: 2px;
  overflow: hidden;
  flex-shrink: 0;
}
.tag-bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.4s ease, background 0.3s ease;
}

.tag-count {
  font-size: 10px;
  color: var(--text-secondary);
  opacity: 0.6;
  min-width: 14px;
  text-align: right;
  font-family: "Consolas", monospace;
  transition: color 0.2s;
}
.tag-item.active .tag-count {
  opacity: 1;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 8px;
}
.spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(100, 180, 240, 0.2);
  border-top-color: rgba(100, 180, 240, 0.7);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-state span {
  font-size: 11px;
  color: var(--text-secondary);
  opacity: 0.5;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 6px;
}
.empty-icon {
  width: 36px; height: 36px;
  color: var(--text-secondary);
  opacity: 0.3;
}
.empty-state span {
  font-size: 11px;
  color: var(--text-secondary);
  opacity: 0.35;
  font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
}
</style>
