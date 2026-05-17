<template>
  <div v-if="store.hoveredBuilding" class="floating-window" :style="styleObj">
    <h2>{{ store.hoveredBuilding.label }}</h2>
    <div class="building-info-row">
      <img :src="categoryIcon" alt="icon" class="label-icon" />
      <span>{{ categoryLabel }}</span>
    </div>
    <div class="tag-container">
      <div v-if="store.hoveredBuildingYear" class="year-tag"
        :style="{ color: yearStyle.color, backgroundColor: yearStyle.background, borderColor: yearStyle.borderColor }">
        {{ simplifiedYear }}
      </div>
      <div v-if="store.hoveredBuildingStructure" class="structure-tag"
        :style="{ color: structStyle.color, backgroundColor: structStyle.background, borderColor: structStyle.borderColor }">
        {{ simplifiedStructure }}
      </div>
    </div>
    <p>{{ store.hoveredBuildingDescription }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed, type CSSProperties } from "vue"
import { useBuildingStore, isGXCategory } from "../stores/buildingStore"
import {
  getIconUrlByLabel, createColoredDotIcon, getGXBuildingCityColor,
  getBuildingYearStyle, getSimplifiedYear,
  getBuildingStructureStyle, getSimplifiedStructure
} from "../composables/useBuildingStyles"

const props = defineProps<{ floatingStyle: Record<string, any> }>()
const store = useBuildingStore()

const styleObj = computed<CSSProperties>(() => props.floatingStyle as CSSProperties)

const category = computed(() => store.hoveredBuilding ? store.findBuildingCategory(store.hoveredBuilding) : "")
const isGX = computed(() => isGXCategory(category.value))
const categoryIcon = computed(() =>
  isGX.value && store.hoveredBuildingCity
    ? createColoredDotIcon(getGXBuildingCityColor(store.hoveredBuildingCity), 20)
    : getIconUrlByLabel(category.value)
)
const categoryLabel = computed(() =>
  isGX.value && store.hoveredBuildingCity ? store.hoveredBuildingCity : category.value
)
const yearStyle = computed(() => getBuildingYearStyle(store.hoveredBuildingYear))
const simplifiedYear = computed(() => getSimplifiedYear(store.hoveredBuildingYear))
const structStyle = computed(() => getBuildingStructureStyle(store.hoveredBuildingStructure))
const simplifiedStructure = computed(() => getSimplifiedStructure(store.hoveredBuildingStructure))
</script>

<style scoped>
.floating-window { position: fixed; background-color: var(--float-bg); backdrop-filter: blur(var(--float-blur)); -webkit-backdrop-filter: blur(var(--float-blur)); padding: 15px; border-radius: var(--glass-radius); box-shadow: 0 8px 32px rgba(0,0,0,0.18); border: 1px solid var(--glass-border); z-index: 99999; max-height: 250px; max-width: 320px; pointer-events: none; overflow-y: auto; overflow-x: hidden; word-break: break-word; }
.floating-window h2 { font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", "Helvetica Neue", sans-serif; font-size: 18px; font-weight: 700; margin: 0 0 8px 0; line-height: 1.3; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: var(--text-primary); }
.floating-window p { font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", sans-serif; font-size: 13px; line-height: 1.5; margin: 0; display: -webkit-box; -webkit-line-clamp: 5; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis; color: var(--text-secondary); }
.building-info-row { display: flex; align-items: center; margin-bottom: 8px; }
.label-icon { width: 20px; height: 20px; margin-right: 8px; vertical-align: middle; }
.tag-container { display: flex; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; }
.year-tag, .structure-tag { display: inline-block; padding: 4px 8px; border-radius: 4px; border: 1px solid; font-size: 12px; font-weight: 500; margin-bottom: 8px; text-align: center; }
</style>
