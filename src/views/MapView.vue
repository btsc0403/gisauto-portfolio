<template>
  <div class="page_container">
    <MapContainer
      ref="mapContainerRef"
      :url="configUrl"
      map-key="test"
      @onload="onMapLoad"
    />

    <div class="overlay-panels">
      <ChatPanel @jumpToBuilding="handleJumpToBuilding" />

      <div class="spacer"></div>

      <div class="side-panel">
        <StatsCharts />

        <div class="knowledge-row-container">
          <KnowledgeGraphDialog />
          <ComponentFilter @filterChanged="handleFeatureFilter" />
        </div>

        <BuildingDetail />
      </div>
    </div>

    <FloatingWindow :floating-style="floatingStyle" />
  </div>
  <ChatInput />
</template>

<script setup lang="ts">
import { ref, computed } from "vue"
import ChatPanel from "../components/ChatPanel.vue"
import MapContainer from "../components/MapContainer.vue"
import StatsCharts from "../components/StatsCharts.vue"
import KnowledgeGraphDialog from "../components/KnowledgeGraphDialog.vue"
import ComponentFilter from "../components/ComponentFilter.vue"
import BuildingDetail from "../components/BuildingDetail.vue"
import ChatInput from "../components/ChatInput.vue"
import FloatingWindow from "../components/FloatingWindow.vue"
import { useBuildingStore, isGXCategory } from "../stores/buildingStore"
import { createColoredMarkerIcon, getGXBuildingMarkerColor, getIconUrlByLabel } from "../composables/useBuildingStyles"
import * as L from "leaflet"

const store = useBuildingStore()
const configUrl = "config/config.json"
const mapContainerRef = ref<InstanceType<typeof MapContainer> | null>(null)

const floatingStyle = computed(() => mapContainerRef.value?.floatingWindowStyle ?? {})

function onMapLoad(_map: any) {
  // map loaded
}

function handleJumpToBuilding(coordinate: { lat: number; lng: number }) {
  mapContainerRef.value?.jumpToBuilding(coordinate)
}

async function handleFeatureFilter(buildingNames: string[], isFiltering: boolean) {
  const nameSet = new Set(buildingNames)

  const updates = store.markers.map(async (marker) => {
    let isVisible = true
    if (isGXCategory(marker.category)) {
      if (isFiltering && marker.buildingName) {
        if (!nameSet.has(marker.buildingName)) isVisible = false
      }
    }

    let iconUrl: string
    if (isGXCategory(marker.category)) {
      if (isVisible) {
        try {
          iconUrl = createColoredMarkerIcon(await getGXBuildingMarkerColor(marker.buildingName || ""))
        } catch {
          iconUrl = getIconUrlByLabel(marker.category)
        }
      } else {
        iconUrl = createColoredMarkerIcon("#D3D3D3")
      }
    } else {
      iconUrl = getIconUrlByLabel(marker.category, !isVisible)
    }
    marker.setIcon(L.icon({ iconUrl, iconSize: [32, 32], iconAnchor: [16, 32] }))
    marker.setZIndexOffset(isVisible ? 1000 : 0)
  })
  await Promise.all(updates)
}
</script>

<style scoped>
.page_container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}
.overlay-panels {
  position: relative;
  z-index: 10;
  display: flex;
  width: 100%;
  height: 100%;
  padding: 10px;
  box-sizing: border-box;
  gap: 10px;
  pointer-events: none;
}
.overlay-panels > * {
  pointer-events: auto;
}
.spacer {
  flex: 1;
  pointer-events: none !important;
}
.side-panel {
  width: 28%;
  flex: 0 0 28%;
  overflow: hidden;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.knowledge-row-container {
  display: flex;
  width: 100%;
  flex-shrink: 0;
  gap: 10px;
}
</style>
