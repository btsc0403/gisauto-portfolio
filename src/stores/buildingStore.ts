import { defineStore } from "pinia"
import { ref, computed } from "vue"
import type * as L from "leaflet"

export type CoordinateItem = { label: string; lat: number; lng: number }
export type CoordinateCategory = { label: string; visible: boolean; items: CoordinateItem[] }

export function isGXCategory(category: string): boolean {
  return category === "GX Buildings" || category === "GX_BOOK_Buildings"
}
export type CustomMarker = L.Marker & {
  category: string
  buildingName: string
  buildingYear?: string
  buildingCity?: string
}

export const useBuildingStore = defineStore("building", () => {
  const coordinates = ref<CoordinateCategory[]>([])
  const markers = ref<CustomMarker[]>([])

  const selectedBuilding = ref<CoordinateItem | null>(null)
  const selectedBuildingDescription = ref<string | null>(null)
  const selectedBuildingYear = ref("")
  const selectedBuildingStructure = ref("")
  const selectedBuildingCity = ref("")
  const selectedBuildingImage = ref<string[]>([])
  const showDetailModal = ref(false)

  const hoveredBuilding = ref<CoordinateItem | null>(null)
  const hoveredBuildingDescription = ref("")
  const hoveredBuildingYear = ref("")
  const hoveredBuildingStructure = ref("")
  const hoveredBuildingCity = ref("")

  const selectedCategories = ref<string[]>([])
  const selectedCategoriesChart = ref<string[]>([])
  const selectedCategoriesList = ref<string[]>([])
  const selectedYearPeriods = ref<string[]>([])
  const selectedCities = ref<string[]>([])
  const selectedDistricts = ref<string[]>([])
  const selectedFeatures = ref<string[]>([])

  const selectedBuildingForKG = ref<string | null>(null)
  const showKnowledgeGraphDialog = ref(false)

  const processedData = ref<any[]>([])
  const processingStatus = ref("")

  const showKeywords3 = ref(true)
  const showGuangzhou = ref(false)

  async function loadCoordinates() {
    try {
      const resp = await fetch("/data/coordinates.json")
      const data: CoordinateCategory[] = await resp.json()
      coordinates.value = data
      selectedCategories.value = data.map((c) => c.label)
    } catch (e) {
      console.error("Failed to load coordinates:", e)
    }
  }

  function findBuildingCategory(building: CoordinateItem): string {
    for (const category of coordinates.value) {
      if (category.items.find((item) => item.label === building.label)) {
        return category.label
      }
    }
    return "Unknown Category"
  }

  async function loadBuildingDescription(label: string) {
    const path = `/buildingDescriptions/${encodeURIComponent(label + ".json")}`
    try {
      const resp = await fetch(path)
      if (!resp.ok) throw new Error("not found")
      return await resp.json()
    } catch {
      return null
    }
  }

  async function selectBuilding(coord: CoordinateItem) {
    selectedBuilding.value = coord
    showDetailModal.value = true
    selectedBuildingDescription.value = "loading"
    selectedBuildingForKG.value = coord.label

    const data = await loadBuildingDescription(coord.label)
    if (data) {
      selectedBuildingDescription.value = data.A2_content || "描述不可用"
      selectedBuildingYear.value = data.build_year || ""
      selectedBuildingStructure.value = data.structureType || ""
      const cat = findBuildingCategory(coord)
      selectedBuildingCity.value = isGXCategory(cat) ? (data.city || "") : ""
    } else {
      selectedBuildingDescription.value = "暂无"
      selectedBuildingCity.value = ""
    }
  }

  async function hoverBuilding(coord: CoordinateItem, category: string) {
    hoveredBuilding.value = coord
    const data = await loadBuildingDescription(coord.label)
    if (data) {
      hoveredBuildingDescription.value = data.A2_content || "暂无描述"
      hoveredBuildingYear.value = data.build_year || ""
      hoveredBuildingStructure.value = data.structureType || ""
      hoveredBuildingCity.value = isGXCategory(category) ? (data.city || "") : ""
    }
  }

  function unhoverBuilding() {
    hoveredBuilding.value = null
    hoveredBuildingDescription.value = ""
    hoveredBuildingYear.value = ""
    hoveredBuildingStructure.value = ""
    hoveredBuildingCity.value = ""
  }

  return {
    coordinates,
    markers,
    selectedBuilding,
    selectedBuildingDescription,
    selectedBuildingYear,
    selectedBuildingStructure,
    selectedBuildingCity,
    selectedBuildingImage,
    showDetailModal,
    hoveredBuilding,
    hoveredBuildingDescription,
    hoveredBuildingYear,
    hoveredBuildingStructure,
    hoveredBuildingCity,
    selectedCategories,
    selectedCategoriesChart,
    selectedCategoriesList,
    selectedYearPeriods,
    selectedCities,
    selectedDistricts,
    selectedFeatures,
    selectedBuildingForKG,
    showKnowledgeGraphDialog,
    processedData,
    processingStatus,
    showKeywords3,
    showGuangzhou,
    loadCoordinates,
    findBuildingCategory,
    loadBuildingDescription,
    selectBuilding,
    hoverBuilding,
    unhoverBuilding,
  }
})
