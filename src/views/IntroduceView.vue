<template>
  <div class="introduce-page">
    <section class="hero-section">
      <img class="hero-logo" src="/logo.png" alt="Heritage Explorer" />
      <div class="hero-right">
        <span class="hero-badge">INSTITUTIONAL REPOSITORY</span>
        <h1 class="hero-title">Heritage Archive 2.0</h1>
        <p class="hero-desc">
          A comprehensive, searchable repository for all {{ totalCount }} architectural landmarks.<br />
          Preserving the structural soul of our shared history through digital curation.
        </p>
        <div class="hero-counter">
          <span class="counter-number">{{ totalCount }}</span>
          <span class="counter-label">ACTIVE RECORDS</span>
        </div>
      </div>
    </section>

    <section class="filter-bar">
      <div class="filter-item">
        <label>QUICK SEARCH</label>
        <input v-model="searchText" type="text" placeholder="Building name..." class="filter-input" />
      </div>
      <div class="filter-item">
        <label>LOCATION</label>
        <select v-model="selectedCity" class="filter-select">
          <option value="">All Cities</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>
      <div class="filter-item">
        <label>CATEGORY</label>
        <select v-model="selectedCategory" class="filter-select">
          <option value="">All Types</option>
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>
      <div class="filter-item">
        <label>ERA</label>
        <select v-model="selectedEra" class="filter-select">
          <option value="">Select Period</option>
          <option value="清代">清代</option>
          <option value="民国">民国</option>
          <option value="明代">明代</option>
          <option value="近现代">近现代</option>
        </select>
      </div>
      <button class="filter-btn" @click="resetFilters">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
        </svg>
      </button>
    </section>

    <section class="cards-grid">
      <div
        v-for="(building, idx) in paginatedBuildings"
        :key="idx"
        class="building-card"
      >
        <div class="card-image">
          <img :src="building.image" :alt="building.label" @error="onImgError($event)" />
          <div class="card-tags">
            <span v-if="building.era" class="tag tag-era">{{ building.era }}</span>
            <span v-if="building.category" class="tag tag-category">{{ building.category }}</span>
          </div>
        </div>
        <div class="card-body">
          <h3 class="card-title">{{ building.label }}</h3>
          <p v-if="building.city" class="card-location">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="#8b2500" stroke="none"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>
            {{ building.city }}
          </p>
          <p class="card-desc">{{ building.description }}</p>
          <div class="card-footer">
            <span v-if="building.structure" class="card-type">{{ building.structure }}</span>
            <router-link to="/" class="card-link" @click="selectAndJump(building)">VIEW DETAILS →</router-link>
          </div>
        </div>
      </div>
    </section>

    <section v-if="totalPages > 1" class="pagination">
      <button :disabled="currentPage === 1" @click="currentPage--">&lt;</button>
      <button
        v-for="p in visiblePages"
        :key="p"
        :class="{ active: p === currentPage }"
        @click="currentPage = p"
      >{{ p }}</button>
      <span v-if="totalPages > 5">... {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="currentPage++">&gt;</button>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { useBuildingStore, isGXCategory } from "../stores/buildingStore"
import { useRouter } from "vue-router"

const store = useBuildingStore()
const router = useRouter()

const searchText = ref("")
const selectedCity = ref("")
const selectedCategory = ref("")
const selectedEra = ref("")
const currentPage = ref(1)
const perPage = 9

interface CardBuilding {
  label: string
  lat: number
  lng: number
  city: string
  category: string
  era: string
  structure: string
  description: string
  image: string
}

const allBuildings = ref<CardBuilding[]>([])

const cities = computed(() => {
  const s = new Set(allBuildings.value.map((b) => b.city).filter(Boolean))
  return [...s].sort()
})

const categories = computed(() => {
  const s = new Set(allBuildings.value.map((b) => b.category).filter(Boolean))
  return [...s].sort()
})

const totalCount = computed(() => allBuildings.value.length)

const filteredBuildings = computed(() => {
  let list = allBuildings.value
  if (searchText.value) {
    const q = searchText.value.toLowerCase()
    list = list.filter((b) => b.label.toLowerCase().includes(q))
  }
  if (selectedCity.value) list = list.filter((b) => b.city === selectedCity.value)
  if (selectedCategory.value) list = list.filter((b) => b.category === selectedCategory.value)
  if (selectedEra.value) list = list.filter((b) => b.era.includes(selectedEra.value))
  return list
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredBuildings.value.length / perPage)))
const visiblePages = computed(() => {
  const pages: number[] = []
  for (let i = 1; i <= Math.min(5, totalPages.value); i++) pages.push(i)
  return pages
})

const paginatedBuildings = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredBuildings.value.slice(start, start + perPage)
})

function resetFilters() {
  searchText.value = ""
  selectedCity.value = ""
  selectedCategory.value = ""
  selectedEra.value = ""
  currentPage.value = 1
}

function onImgError(e: Event) {
  (e.target as HTMLImageElement).src = "https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png"
}

function selectAndJump(building: CardBuilding) {
  store.selectBuilding({ label: building.label, lat: building.lat, lng: building.lng })
  router.push("/")
}

onMounted(async () => {
  if (!store.coordinates.length) await store.loadCoordinates()

  const buildings: CardBuilding[] = []
  for (const cat of store.coordinates) {
    for (const item of cat.items) {
      let city = ""
      let era = ""
      let structure = ""
      let description = ""
      let image = ""

      if (isGXCategory(cat.label)) {
        const desc = await store.loadBuildingDescription(item.label)
        if (desc) {
          city = desc.city || ""
          era = desc.build_year || ""
          structure = desc.structureType || ""
          description = desc.description ? desc.description.substring(0, 120) + "..." : ""
        }
        image = `/GXbuildingsData/image/${item.label}/1.jpg`
      } else {
        const catPath = cat.label.toLowerCase().replace(" ", "_")
        const labelPath = item.label.replace(" ", "_")
        image = `/buildingPic/${catPath}/${labelPath}/${labelPath}_1.jpg`
      }

      buildings.push({
        label: item.label,
        lat: item.lat,
        lng: item.lng,
        city,
        category: isGXCategory(cat.label) ? "GX Heritage" : cat.label,
        era,
        structure,
        description,
        image
      })
    }
  }
  allBuildings.value = buildings
})
</script>

<style scoped>
.introduce-page {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0 48px 40px;
  box-sizing: border-box;
  background-color: var(--page-bg);
}

.hero-section {
  display: flex;
  align-items: center;
  gap: 48px;
  padding: 40px 0 28px;
}
.hero-logo {
  height: 80px;
  width: auto;
  object-fit: contain;
  flex-shrink: 0;
}
.hero-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  text-align: right;
}
.hero-badge {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 2px;
  color: var(--header-active);
  font-weight: 600;
  margin-bottom: 8px;
  text-transform: uppercase;
}
.hero-title {
  font-family: "Georgia", "Times New Roman", serif;
  font-size: 42px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 12px;
  line-height: 1.1;
}
.hero-desc {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0 0 16px;
  max-width: 560px;
}
.hero-counter {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background-color: var(--header-active);
  color: #fff;
  border-radius: 10px;
  padding: 10px 22px;
}
.counter-number {
  font-size: 26px;
  font-weight: 800;
  line-height: 1;
}
.counter-label {
  font-size: 10px;
  letter-spacing: 1.5px;
  opacity: 0.85;
}

.filter-bar {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  padding: 20px 24px;
  background: var(--glass-highlight), var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur)) saturate(1.4);
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.4);
  border: 1px solid var(--glass-border);
  border-radius: var(--glass-radius);
  box-shadow: var(--glass-shadow);
  margin-bottom: 32px;
  transition: background-color 0.4s, border-color 0.4s, box-shadow 0.4s;
}
.filter-item {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}
.filter-item label {
  font-size: 10px;
  letter-spacing: 1.5px;
  color: var(--text-secondary);
  font-weight: 600;
  margin-bottom: 6px;
  text-transform: uppercase;
}
.filter-input, .filter-select {
  padding: 8px 12px;
  border: 1.5px solid var(--glass-border);
  border-radius: 8px;
  font-size: 13px;
  background: var(--legend-bg);
  color: var(--text-primary);
  outline: none;
  transition: border-color 0.2s, background-color 0.4s, color 0.4s;
}
.filter-input:focus, .filter-select:focus {
  border-color: var(--header-active);
}
.filter-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 38px;
  flex-shrink: 0;
  border: none;
  background-color: var(--header-active);
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.filter-btn:hover { opacity: 0.85; }

.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
  margin-bottom: 40px;
}

.building-card {
  background: var(--glass-highlight), var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur)) saturate(1.4);
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.4);
  border: 1px solid var(--glass-border);
  border-radius: var(--glass-radius);
  overflow: hidden;
  box-shadow: var(--glass-shadow);
  transition: transform 0.25s, box-shadow 0.25s, background-color 0.4s, border-color 0.4s;
}
.building-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--glass-hover-shadow);
  border-color: var(--glass-hover-border);
}

.card-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}
.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}
.building-card:hover .card-image img {
  transform: scale(1.05);
}
.card-tags {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.tag {
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
.tag-era {
  background-color: var(--header-active);
  color: #fff;
  transition: background-color 0.4s;
}
.tag-category {
  background-color: var(--btn-bg);
  color: #fff;
  transition: background-color 0.4s;
}

.card-body {
  padding: 18px 20px 16px;
}
.card-title {
  font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 6px;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.card-location {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-secondary);
  margin: 0 0 10px;
}
.card-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0 0 14px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 58px;
}
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--glass-border);
}
.card-type {
  font-size: 10px;
  letter-spacing: 1px;
  color: var(--text-secondary);
  text-transform: uppercase;
  font-weight: 600;
}
.card-link {
  font-size: 12px;
  font-weight: 600;
  color: var(--header-active);
  text-decoration: none;
  letter-spacing: 0.5px;
  transition: opacity 0.2s;
}
.card-link:hover { opacity: 0.7; }

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  padding-bottom: 20px;
}
.pagination button {
  min-width: 36px;
  height: 36px;
  border: 1px solid var(--glass-border);
  background: var(--legend-bg);
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  color: var(--text-primary);
  transition: all 0.2s;
}
.pagination button:hover:not(:disabled) {
  border-color: var(--header-active);
  color: var(--header-active);
}
.pagination button.active {
  background-color: var(--header-active);
  color: #fff;
  border-color: var(--header-active);
}
.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.pagination span {
  font-size: 14px;
  color: var(--text-secondary);
}
</style>
