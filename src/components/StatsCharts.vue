<template>
  <div class="charts-wrapper">
    <div class="charts-container">
      <div class="chart-box">
        <div class="chart-container">
          <div class="chart-label">
            <div class="label-arrow"></div>
            <span>地区筛选</span>
          </div>
          <div ref="barChartContainer" class="chart-inner"></div>
        </div>
      </div>
      <div class="chart-box">
        <div class="chart-container">
          <div class="chart-label">
            <div class="label-arrow"></div>
            <span>年代筛选</span>
          </div>
          <div ref="pieChartContainer" class="chart-inner"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import * as echarts from "echarts"
import { useBuildingStore, isGXCategory } from "../stores/buildingStore"
import { CITY_COLORS, YEAR_COLORS, CITY_LIST, getSimplifiedYear } from "../composables/useBuildingStyles"
import { getGXBuildingMarkerColor, createColoredMarkerIcon, getIconUrlByLabel } from "../composables/useBuildingStyles"
import * as L from "leaflet"

const store = useBuildingStore()
const barChartContainer = ref<HTMLDivElement | null>(null)
const pieChartContainer = ref<HTMLDivElement | null>(null)

const toggleCity = async (cityName: string) => {
  const barChart = echarts.getInstanceByDom(barChartContainer.value!)
  if (barChart) {
    barChart.showLoading({ text: "筛选中...", color: "#81c784", textColor: "#333", maskColor: "rgba(255,255,255,0.8)", fontSize: 12, showSpinner: true, spinnerRadius: 10, lineWidth: 3 } as any)
    const idx = CITY_LIST.indexOf(cityName)
    setTimeout(() => { barChart.hideLoading(); if (idx !== -1) barChart.dispatchAction({ type: "highlight", seriesIndex: 0, dataIndex: idx }) }, 100)
  }
  const arr = store.selectedCities
  const i = arr.indexOf(cityName)
  if (i !== -1) arr.splice(i, 1); else arr.push(cityName)

  setTimeout(async () => {
    await updateMarkersVisibilityByYearAndCity()
    updateChartColors()
    if (barChart) barChart.dispatchAction({ type: "downplay", seriesIndex: 0 })
  }, 300)
}

const toggleYearPeriod = async (yearPeriod: string) => {
  const pieChart = echarts.getInstanceByDom(pieChartContainer.value!)
  if (pieChart) {
    pieChart.showLoading({ text: "筛选中...", color: "#4fc3f7", textColor: "#333", maskColor: "rgba(255,255,255,0.8)", fontSize: 10, showSpinner: true, spinnerRadius: 10, lineWidth: 3 } as any)
    const idx = ["明代及以前", "清代", "民国", "建国后", "改革开放后", "现代"].indexOf(yearPeriod)
    setTimeout(() => { pieChart.hideLoading(); if (idx !== -1) pieChart.dispatchAction({ type: "highlight", seriesIndex: 0, dataIndex: idx }) }, 100)
  }
  const arr = store.selectedYearPeriods
  const i = arr.indexOf(yearPeriod)
  if (i !== -1) arr.splice(i, 1); else arr.push(yearPeriod)

  setTimeout(async () => {
    await updateMarkersVisibilityByYearAndCity()
    updateChartColors()
    if (pieChart) pieChart.dispatchAction({ type: "downplay", seriesIndex: 0 })
  }, 300)
}

async function updateMarkersVisibilityByYearAndCity() {
  const updates = store.markers.map(async (marker) => {
    let isVisible = true
    if (isGXCategory(marker.category)) {
      if (store.selectedYearPeriods.length > 0 && marker.buildingYear) {
        if (!store.selectedYearPeriods.includes(getSimplifiedYear(marker.buildingYear))) isVisible = false
      }
      if (store.selectedCities.length > 0 && marker.buildingCity) {
        if (!store.selectedCities.includes(marker.buildingCity)) isVisible = false
      }
    }
    let iconUrl: string
    if (isGXCategory(marker.category)) {
      if (isVisible) {
        try { iconUrl = createColoredMarkerIcon(await getGXBuildingMarkerColor(marker.buildingName || "")) } catch { iconUrl = getIconUrlByLabel(marker.category) }
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

function updateChartColors() {
  const barChart = echarts.getInstanceByDom(barChartContainer.value!)
  if (barChart) {
    barChart.setOption({
      animation: true, animationDuration: 750, animationEasing: "cubicInOut" as const,
      series: [{ itemStyle: { color: (p: any) => { const sel = store.selectedCities.length === 0 || store.selectedCities.includes(p.name); return sel ? (CITY_COLORS[p.name] || "#D3D3D3") : "#D3D3D3" } } }]
    }, false)
  }
  const pieChart = echarts.getInstanceByDom(pieChartContainer.value!)
  if (pieChart) {
    pieChart.setOption({
      animation: true, animationDuration: 900, animationEasing: "cubicInOut" as const,
      series: [{ itemStyle: { color: (p: any) => { const sel = store.selectedYearPeriods.length === 0 || store.selectedYearPeriods.includes(p.name); return sel ? (YEAR_COLORS[p.name] || "#D3D3D3") : "#D3D3D3" } } }]
    }, false)
  }
}

onMounted(() => {
  if (!barChartContainer.value || !pieChartContainer.value) return
  const barChart = echarts.init(barChartContainer.value)
  const pieChart = echarts.init(pieChartContainer.value)

  const barData = [25, 18, 15, 30, 22, 20, 28, 35, 12, 18, 16, 25, 10, 8]
  const categories = CITY_LIST

  const pieData = [15, 25, 35, 45, 30, 50]
  const pieCategories = ["明代及以前", "清代", "民国", "建国后", "改革开放后", "现代"]

  barChart.setOption({
    animation: true, animationDuration: 800, animationEasing: "cubicOut" as const,
    grid: { top: "5%", bottom: "15%", left: "10%", right: "10%" },
    tooltip: { show: true, trigger: "axis", axisPointer: { type: "shadow" }, formatter: "{b}: {c} 个建筑" },
    xAxis: { type: "category", data: categories, axisLabel: { show: true, rotate: 45, fontSize: 9, color: "#333", margin: 8, interval: 0 }, axisLine: { show: true } },
    yAxis: { type: "value", axisLabel: { show: true, fontSize: 12, color: "#333" }, axisLine: { show: true } },
    series: [{
      name: "城市建筑分布", type: "bar", data: barData,
      label: { show: true, position: "top", fontSize: 10, color: "#333", fontFamily: "DengXian, 等线, sans-serif" },
      itemStyle: { color: (p: any) => CITY_COLORS[categories[p.dataIndex]] || "#D3D3D3", shadowBlur: 4, shadowColor: "rgba(0,0,0,0.2)", borderRadius: [4, 4, 0, 0], borderWidth: 1, borderColor: "#fff" },
      animationDelay: (idx: number) => idx * 50, animationEasing: "elasticOut",
      emphasis: { itemStyle: { shadowBlur: 15, shadowColor: "rgba(0,0,0,0.4)", borderWidth: 2, borderColor: "#fff" } }
    }]
  })

  pieChart.setOption({
    animation: true, animationDuration: 1000, animationEasing: "cubicInOut" as const,
    tooltip: { trigger: "item", backgroundColor: "rgba(255,255,255,0.95)", borderColor: "#ccc", borderWidth: 1, borderRadius: 6, padding: [8, 12], textStyle: { color: "#333", fontSize: 12 }, formatter: "年代分布<br/>{b}: {c}个 ({d}%)" },
    legend: { show: true, orient: "vertical", right: "5%", top: "center", itemWidth: 14, itemHeight: 14, textStyle: { fontSize: 12, color: "#333" } },
    series: [{
      name: "年代分布", type: "pie", radius: ["55%", "15%"], center: ["32%", "50%"],
      avoidLabelOverlap: true, label: { show: false }, labelLine: { show: false },
      data: pieCategories.map((c, i) => ({ name: c, value: pieData[i] })),
      itemStyle: { color: (p: any) => YEAR_COLORS[p.name] || "#D3D3D3", shadowBlur: 8, shadowColor: "rgba(0,0,0,0.2)", borderWidth: 2, borderColor: "rgba(255,255,255,0.5)" },
      animationType: "scale", animationEasing: "elasticOut",
      animationDelay: (idx: number) => idx * 100,
      emphasis: { itemStyle: { shadowBlur: 20, shadowColor: "rgba(0,0,0,0.4)", borderWidth: 3, borderColor: "rgba(255,255,255,0.5)" }, label: { show: false }, labelLine: { show: false } }
    }]
  })

  barChart.on("click", (p: any) => { toggleCity(p.name) })
  pieChart.on("click", (p: any) => { toggleYearPeriod(p.name) })
})
</script>

<style scoped>
.charts-wrapper { flex-shrink: 0; width: 100%; box-sizing: border-box; }

.charts-container { display: flex; width: 100%; gap: 10px; }
.chart-box { flex: 1; min-width: 0; }
.chart-container {
  width: 100%; height: 260px; position: relative; z-index: 1;
  border: 1px solid var(--glass-border);
  background: var(--glass-highlight), var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur)) saturate(1.4);
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.4);
  box-shadow: var(--glass-shadow); border-radius: var(--glass-radius);
  transition: all 0.4s ease; padding: 10px; box-sizing: border-box;
  display: flex; flex-direction: column;
}
.chart-container:hover {
  box-shadow: var(--glass-hover-shadow);
  border-color: var(--glass-hover-border);
}

.chart-label {
  display: flex; align-items: center;
  padding: 2px 4px 4px; flex-shrink: 0;
  opacity: 0.75;
}
.label-arrow {
  width: 0; height: 0;
  border-left: 6px solid transparent; border-right: 6px solid transparent;
  border-top: 8px solid var(--text-primary);
  margin-right: 5px; transition: border-color 0.4s;
}
.chart-label span {
  font-weight: bold; font-size: 16px;
  font-family: "DengXian", "等线", sans-serif;
  color: var(--text-primary);
  transition: color 0.4s;
}

.chart-inner { flex: 1; min-height: 0; width: 100%; }
</style>
