<template>
  <div class="new-description-container">
    <div class="component-header">
      <div class="arrow"></div>
      <span>详细信息</span>
    </div>
    <div v-if="store.selectedBuilding">
      <h2 class="oldfont">{{ store.selectedBuilding.label }}</h2>
      <div class="building-category">
        <img :src="categoryIcon" alt="icon" class="label-icon" />
        <span>{{ categoryLabel }}</span>
      </div>
      <div v-if="store.selectedBuildingYear" class="year-tag-detail"
        :style="{ color: yearStyle.color, backgroundColor: yearStyle.background, borderColor: yearStyle.borderColor }">
        <span class="year-label">建造年代：</span>
        <span class="year-value">{{ simplifiedYear }}</span>
      </div>
      <div v-if="store.selectedBuildingStructure" class="structure-tag-detail"
        :style="{ color: structStyle.color, backgroundColor: structStyle.background, borderColor: structStyle.borderColor }">
        <span class="structure-label">建筑结构：</span>
        <span class="structure-value">{{ simplifiedStructure }}</span>
      </div>
      <p class="description-box"><strong>建筑描述</strong>: {{ store.selectedBuildingDescription }}</p>
    </div>
    <div v-if="store.selectedBuilding" class="image-display">
      <div
        class="carousel-scene"
        ref="carouselRef"
        @mousedown="onDragStart"
        @wheel.prevent="onWheel"
      >
        <div class="carousel-ring" :style="{ transform: `rotateY(${rotation}deg)` }">
          <div
            v-for="(img, index) in carouselImages"
            :key="index"
            class="carousel-card"
            :style="cardStyle(index)"
            @click.stop="openLightbox(img)"
          >
            <img :src="img" @error="() => onImageError(index)" alt="Building Image" draggable="false" />
          </div>
        </div>
      </div>
    </div>

    <Teleport to="body">
      <div v-if="lightboxSrc" class="lightbox-overlay" @click="lightboxSrc = ''">
        <img :src="lightboxSrc" class="lightbox-img" @click.stop />
        <button class="lightbox-close" @click="lightboxSrc = ''">&times;</button>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onBeforeUnmount } from "vue"
import { useBuildingStore, isGXCategory } from "../stores/buildingStore"
import {
  getIconUrlByLabel, createColoredDotIcon, getGXBuildingCityColor,
  getBuildingYearStyle, getSimplifiedYear,
  getBuildingStructureStyle, getSimplifiedStructure
} from "../composables/useBuildingStyles"

const store = useBuildingStore()

const category = computed(() => store.selectedBuilding ? store.findBuildingCategory(store.selectedBuilding) : "")
const isGX = computed(() => isGXCategory(category.value))
const categoryIcon = computed(() =>
  isGX.value && store.selectedBuildingCity
    ? createColoredDotIcon(getGXBuildingCityColor(store.selectedBuildingCity), 20)
    : getIconUrlByLabel(category.value)
)
const categoryLabel = computed(() =>
  isGX.value && store.selectedBuildingCity ? store.selectedBuildingCity : category.value
)
const yearStyle = computed(() => getBuildingYearStyle(store.selectedBuildingYear))
const simplifiedYear = computed(() => getSimplifiedYear(store.selectedBuildingYear))
const structStyle = computed(() => getBuildingStructureStyle(store.selectedBuildingStructure))
const simplifiedStructure = computed(() => getSimplifiedStructure(store.selectedBuildingStructure))

const lightboxSrc = ref("")
const rotation = ref(0)
const carouselRef = ref<HTMLElement | null>(null)

const RADIUS = 220

const carouselImages = computed(() => store.selectedBuildingImage.slice(0, 10))

function cardStyle(index: number) {
  const total = carouselImages.value.length
  if (total === 0) return {}
  const angle = (360 / total) * index
  return {
    transform: `rotateY(${angle}deg) translateZ(${RADIUS}px)`,
  }
}

function openLightbox(src: string) {
  if (isDragged) return
  lightboxSrc.value = src
}

let isDragging = false
let isDragged = false
let dragStartX = 0
let dragStartRotation = 0

function onDragStart(e: MouseEvent) {
  isDragging = true
  isDragged = false
  dragStartX = e.clientX
  dragStartRotation = rotation.value
  document.addEventListener("mousemove", onDragMove)
  document.addEventListener("mouseup", onDragEnd)
}

function onDragMove(e: MouseEvent) {
  if (!isDragging) return
  const dx = e.clientX - dragStartX
  if (Math.abs(dx) > 3) isDragged = true
  rotation.value = dragStartRotation + dx * 0.4
}

function onDragEnd() {
  isDragging = false
  document.removeEventListener("mousemove", onDragMove)
  document.removeEventListener("mouseup", onDragEnd)
}

function onWheel(e: WheelEvent) {
  rotation.value += e.deltaY > 0 ? -12 : 12
}

onBeforeUnmount(() => {
  document.removeEventListener("mousemove", onDragMove)
  document.removeEventListener("mouseup", onDragEnd)
})

const onImageError = (index: number) => {
  store.selectedBuildingImage.splice(index, 1, "https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png")
}
</script>

<style scoped>
.new-description-container { width: 100%; flex: 1; min-height: 0; border: 1px solid var(--glass-border); background: var(--glass-highlight), var(--glass-bg); backdrop-filter: blur(var(--glass-blur)) saturate(1.4); -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.4); box-shadow: var(--glass-shadow); border-radius: var(--glass-radius); transition: all 0.4s ease; padding: 15px; box-sizing: border-box; overflow-y: auto; overflow-x: hidden; }
.new-description-container:hover { box-shadow: var(--glass-hover-shadow); border-color: var(--glass-hover-border); }

.component-header { display: flex; align-items: center; margin-bottom: 10px; opacity: 0.75; }
.arrow { width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 8px solid black; margin-right: 5px; }
.component-header span { font-weight: bold; font-size: 16px; font-family: "DengXian", "等线", sans-serif; color: var(--text-primary); transition: color 0.4s; }
.arrow { border-top-color: var(--text-primary) !important; transition: border-color 0.4s; }

.oldfont { font-size: 28px; font-weight: bold; }
.label-icon { width: 20px; height: 20px; margin-right: 8px; vertical-align: middle; }
.building-category { display: flex; align-items: center; }

.description-box { font-size: 16px; padding: 10px; background-color: var(--desc-bg); border-radius: 8px; border: 1px solid var(--glass-border); margin: 12px 2px 0; max-width: 855px; color: var(--desc-text); line-height: 1.5; max-height: calc(1.5em * 4); overflow-y: auto; word-wrap: break-word; transition: background-color 0.4s, color 0.4s; }

.year-tag-detail, .structure-tag-detail { display: flex; align-items: center; padding: 8px 12px; border-radius: 6px; border: 1px solid; margin: 10px 0; font-size: 14px; }
.year-label, .structure-label { font-weight: 500; margin-right: 6px; }
.year-value, .structure-value { font-weight: 600; }

/* --- 3D Carousel --- */
.carousel-scene {
  margin-top: 15px;
  margin-bottom: 15px;
  width: 100%;
  height: 180px;
  perspective: 900px;
  overflow: visible;
  cursor: grab;
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
}
.carousel-scene:active { cursor: grabbing; }

.carousel-ring {
  width: 110px;
  height: 135px;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.3s ease-out;
}

.carousel-card {
  position: absolute;
  width: 110px;
  height: 135px;
  border-radius: 8px;
  overflow: hidden;
  backface-visibility: hidden;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
  border: 2px solid rgba(255,255,255,0.5);
  cursor: pointer;
  transition: box-shadow 0.3s;
}
.carousel-card:hover {
  box-shadow: 0 8px 28px rgba(0,0,0,0.35);
  border-color: var(--btn-bg);
}
.carousel-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  pointer-events: none;
}

/* --- Lightbox --- */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  z-index: 99999;
  background: rgba(0,0,0,0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: lbFadeIn 0.25s ease;
}
.lightbox-img {
  max-width: 85vw;
  max-height: 85vh;
  border-radius: 10px;
  box-shadow: 0 12px 48px rgba(0,0,0,0.5);
  animation: lbZoomIn 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
}
.lightbox-close {
  position: absolute;
  top: 24px;
  right: 32px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(255,255,255,0.15);
  color: #fff;
  font-size: 22px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}
.lightbox-close:hover { background: rgba(255,255,255,0.3); }
@keyframes lbFadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes lbZoomIn { from { opacity: 0; transform: scale(0.85); } to { opacity: 1; transform: scale(1); } }
</style>
