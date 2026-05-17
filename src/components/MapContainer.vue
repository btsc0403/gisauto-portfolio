<template>
  <div class="map-container">
    <div :id="withKeyId" class="mars2d-container"></div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, watch, onMounted, onBeforeUnmount } from "vue"
import * as L from "leaflet"
import * as mars2d from "mars2d"
import { useBuildingStore, isGXCategory, type CustomMarker } from "../stores/buildingStore"
import { getIconUrlByLabel, getGXBuildingMarkerColor, createColoredMarkerIcon } from "../composables/useBuildingStyles"
import { getBuildingImages, getGXBuildingImages } from "../composables/useBuildingImages"

const props = withDefaults(
  defineProps<{ url: string; mapKey?: string; options?: any }>(),
  { url: "", mapKey: "default", options: () => ({}) }
)
const emit = defineEmits(["onload"])

const store = useBuildingStore()
let map: mars2d.Map | null = null

const withKeyId = computed(() => `mars2d-container-${props.mapKey}`)

const floatingWindowStyle = reactive({
  top: "-9999px",
  left: "-9999px",
  visibility: "hidden" as "hidden" | "visible"
})

function updateFloatingWindowPosition(latLng: L.LatLng) {
  if (!map) return
  const point = map.latLngToContainerPoint(latLng)
  const mapEl = document.getElementById(withKeyId.value)
  if (!mapEl) return
  const rect = mapEl.getBoundingClientRect()
  const viewX = rect.left + point.x
  const viewY = rect.top + point.y
  floatingWindowStyle.top = `${viewY - 220}px`
  floatingWindowStyle.left = `${viewX + 20}px`
  floatingWindowStyle.visibility = "visible"
}

function hideFloatingWindow() {
  floatingWindowStyle.top = "-9999px"
  floatingWindowStyle.left = "-9999px"
  floatingWindowStyle.visibility = "hidden"
}

async function flyTo(coord: { label: string; lat: number; lng: number }) {
  await store.selectBuilding(coord)

  const cat = store.findBuildingCategory(coord)
  if (isGXCategory(cat)) {
    try {
      store.selectedBuildingImage = await getGXBuildingImages(coord.label)
    } catch {
      store.selectedBuildingImage = [`/GXbuildingsData/image/${coord.label}/1.jpg`]
    }
  } else {
    const categoryPath = cat.toLowerCase().replace(" ", "_")
    const labelPath = coord.label.replace(" ", "_")
    try {
      store.selectedBuildingImage = await getBuildingImages(labelPath, categoryPath)
    } catch {
      store.selectedBuildingImage = [`/buildingPic/${categoryPath}/${labelPath}/${labelPath}_1.jpg`]
    }
  }
}

function jumpToBuilding(coordinate: { lat: number; lng: number }) {
  const target = store.markers.find((m) => {
    const ll = m.getLatLng()
    return Math.abs(ll.lat - coordinate.lat) < 0.001 && Math.abs(ll.lng - coordinate.lng) < 0.001
  })
  if (target) target.fire("click")
}

watch(() => store.showGuangzhou, (show) => {
  store.markers.forEach((marker) => {
    if (!isGXCategory(marker.category)) {
      if (show) {
        if (map && !map.hasLayer(marker)) marker.addTo(map)
      } else {
        if (map && map.hasLayer(marker)) marker.removeFrom(map)
      }
    }
  })
})

defineExpose({ jumpToBuilding, floatingWindowStyle })

function initMap(option: any) {
  const finalOptions = { zoom: 7, ...option }
  if (finalOptions.center?.lat && finalOptions.center?.lng) {
    finalOptions.center = new L.LatLng(finalOptions.center.lat, finalOptions.center.lng)
  }
  map = new mars2d.Map(withKeyId.value, finalOptions)
  emit("onload", map)
}

onBeforeUnmount(() => {
  if (map) { map.destroy(); map = null }
})

onMounted(async () => {
  await store.loadCoordinates()

  const data: any = await mars2d.Util.fetchJson({ url: props.url })
  initMap({ ...data.mars2d, ...props.options })

  store.coordinates.forEach((category) => {
    category.items.forEach(async (coord, subIndex) => {
      let iconUrl = getIconUrlByLabel(category.label)
      if (isGXCategory(category.label)) {
        iconUrl = createColoredMarkerIcon(await getGXBuildingMarkerColor(coord.label))
      }
      const marker = L.marker([coord.lat, coord.lng], {
        icon: L.icon({ iconUrl, iconSize: [29, 29], iconAnchor: [14.5, 29] })
      }) as CustomMarker

      marker.category = category.label
      if (isGXCategory(category.label) || store.showGuangzhou) {
        marker.addTo(map!)
      }
      marker.buildingName = coord.label

      if (isGXCategory(category.label)) {
        const desc = await store.loadBuildingDescription(coord.label)
        if (desc) {
          marker.buildingYear = desc.build_year || ""
          marker.buildingCity = desc.city || ""
        }
      }

      marker.on("click", () => {
        flyTo(coord)
      })

      marker.on("mouseover", async () => {
        await store.hoverBuilding(coord, category.label)
        if (map) updateFloatingWindowPosition(new L.LatLng(coord.lat, coord.lng))
      })

      marker.on("mouseout", () => {
        store.unhoverBuilding()
        hideFloatingWindow()
      })

      store.markers.push(marker)
    })
  })
})
</script>

<style scoped>
.map-container { position: absolute; inset: 0; z-index: 0; }
.mars2d-container { width: 100%; height: 100%; }
</style>

<style>
.leaflet-marker-icon {
  transition: transform 0.2s ease, filter 0.2s ease;
}
.leaflet-marker-icon:hover {
  transform: scale(1.35);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  z-index: 9999 !important;
}
</style>
