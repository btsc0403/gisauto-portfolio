<template>
  <div v-if="store.showKnowledgeGraphDialog" class="knowledge-graph-dialog">
    <div class="dialog-header">
      <span>建筑知识图谱</span>
      <div class="header-actions">
        <button v-if="viewStack.length > 0" @click="goBack" class="back-button">← 返回</button>
        <button @click="resetToOverview" class="reset-button">概览</button>
        <button @click="store.showKnowledgeGraphDialog = false" class="close-button">×</button>
      </div>
    </div>
    <div class="dialog-content">
      <div v-if="loading" class="loading-overlay">加载中...</div>
      <div ref="graphNetworkContainer" class="knowledge-graph-network"></div>
      <div class="graph-legend">
        <div class="legend-item"><div class="legend-color" style="background-color: #96CEB4;"></div><div class="legend-text">城市</div></div>
        <div class="legend-item"><div class="legend-color" style="background-color: #4ECDC4;"></div><div class="legend-text">县区</div></div>
        <div class="legend-item"><div class="legend-color" style="background-color: #FECA57;"></div><div class="legend-text">建筑</div></div>
        <div class="legend-item"><div class="legend-color" style="background-color: #FF6B6B;"></div><div class="legend-text">结构类型</div></div>
        <div class="legend-item"><div class="legend-color" style="background-color: #45B7D1;"></div><div class="legend-text">年代</div></div>
        <div class="legend-item"><div class="legend-color" style="background-color: #DDA0DD;"></div><div class="legend-text">功能</div></div>
        <div class="graph-tip">点击节点查看详情 | 双击展开关联</div>
      </div>
    </div>
  </div>

  <!-- KG Thumbnail -->
  <div :class="['rag-box', { 'kg-flash': kgFlashing }]" @click="store.showKnowledgeGraphDialog = true">
    <div class="component-header">
      <div class="arrow"></div>
      <span>知识图谱</span>
    </div>
    <div class="kg-logo-container">
      <img class="kg-logo-image" src="/src/KGlogo2.png" alt="KG" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from "vue"
import { useBuildingStore } from "../stores/buildingStore"
// @ts-ignore
import { DataSet, Network } from "vis-network/standalone"

const API_BASE = "http://localhost:8000"

const store = useBuildingStore()
const graphNetworkContainer = ref<HTMLElement | null>(null)
const loading = ref(false)
const viewStack = ref<string[]>([])
const kgFlashing = ref(false)

let networkInstance: any = null
let nodesDataSet: any = null
let edgesDataSet: any = null

async function fetchGraph(url: string): Promise<{ nodes: any[]; edges: any[] }> {
  const resp = await fetch(url)
  return resp.json()
}

function renderGraph(data: { nodes: any[]; edges: any[] }, append = false) {
  if (!graphNetworkContainer.value) return

  if (!append || !nodesDataSet) {
    // 全新渲染
    if (networkInstance) { networkInstance.destroy(); networkInstance = null }
    // @ts-ignore
    nodesDataSet = new DataSet()
    // @ts-ignore
    edgesDataSet = new DataSet()
  }

  // 添加节点（跳过已存在的）
  const existingIds = new Set(nodesDataSet.getIds())
  for (const node of data.nodes) {
    if (!existingIds.has(node.id)) {
      nodesDataSet.add({
        ...node,
        font: node.font || { color: "black", size: 12, face: "DengXian, 等线, sans-serif" },
        shape: "dot",
        shadow: { enabled: true, color: "rgba(0,0,0,0.3)", size: 5, x: 3, y: 3 },
      })
    }
  }

  // 添加边（跳过已存在的）
  const existingEdges = new Set(edgesDataSet.getIds())
  for (const edge of data.edges) {
    const edgeId = `${edge.from}_${edge.to}`
    if (!existingEdges.has(edgeId)) {
      edgesDataSet.add({
        ...edge,
        id: edgeId,
        font: edge.label ? { size: 9, color: "#666", face: "DengXian, 等线, sans-serif" } : undefined,
        arrows: { to: { enabled: true, scaleFactor: 0.5 } },
        smooth: { enabled: true, type: "continuous", roundness: 0.5 },
      })
    }
  }

  if (!append || !networkInstance) {
    networkInstance = new Network(graphNetworkContainer.value, { nodes: nodesDataSet, edges: edgesDataSet }, {
      nodes: {
        font: { size: 12, face: "DengXian, 等线, sans-serif" },
        shadow: { enabled: true, color: "rgba(0,0,0,0.3)", size: 5, x: 3, y: 3 },
      },
      edges: {
        font: { size: 9, face: "DengXian, 等线, sans-serif" },
        arrows: { to: { enabled: true, scaleFactor: 0.5 } },
        smooth: { enabled: true, type: "continuous", roundness: 0.5 },
      },
      physics: {
        stabilization: { iterations: 150 },
        barnesHut: {
          gravitationalConstant: -50000,
          centralGravity: 0.3,
          springLength: 200,
          springConstant: 0.001,
          damping: 0.09,
          avoidOverlap: 0.1,
        },
      },
      interaction: {
        navigationButtons: false,
        keyboard: true,
        hover: true,
        dragView: true,
        zoomView: true,
        tooltipDelay: 200,
      },
    })

    // 双击节点：展开关联
    networkInstance.on("doubleClick", async (params: any) => {
      if (params.nodes.length === 0) return
      const nodeId = params.nodes[0] as string
      const node = nodesDataSet.get(nodeId)
      if (!node) return

      if (node.group === "Building") {
        // 双击建筑：展示该建筑的关系网
        viewStack.value.push("expand")
        await loadBuildingGraph(node.label)
      } else if (["City", "County", "StructureType", "Era", "Function"].includes(node.group)) {
        // 双击分类节点：展开其下的建筑
        viewStack.value.push("expand")
        await expandNode(node.group, node.label.split("\n")[0])
      }
    })
  }
}

async function loadOverview() {
  loading.value = true
  try {
    const data = await fetchGraph(`${API_BASE}/kg/overview`)
    renderGraph(data)
    viewStack.value = []
  } catch (e) {
    console.error("加载知识图谱概览失败:", e)
  } finally {
    loading.value = false
  }
}

async function loadBuildingGraph(name: string) {
  loading.value = true
  try {
    const data = await fetchGraph(`${API_BASE}/kg/building?name=${encodeURIComponent(name)}`)
    renderGraph(data)
  } catch (e) {
    console.error("加载建筑图谱失败:", e)
  } finally {
    loading.value = false
  }
}

async function expandNode(nodeType: string, name: string) {
  loading.value = true
  try {
    const data = await fetchGraph(`${API_BASE}/kg/expand?node_type=${nodeType}&name=${encodeURIComponent(name)}&limit=20`)
    renderGraph(data, true)
  } catch (e) {
    console.error("展开节点失败:", e)
  } finally {
    loading.value = false
  }
}

function goBack() {
  viewStack.value.pop()
  loadOverview()
}

function resetToOverview() {
  loadOverview()
}

// Flash the thumbnail border when a building is selected
watch(() => store.selectedBuildingForKG, (val) => {
  if (!val) return
  kgFlashing.value = false
  // Force reflow so re-adding the class restarts the animation
  void document.body.offsetHeight
  kgFlashing.value = true
  setTimeout(() => { kgFlashing.value = false }, 1200)
})

// 打开弹窗时加载
watch(() => store.showKnowledgeGraphDialog, (val) => {
  if (val) {
    nextTick(() => {
      // 如果有选中的建筑，直接展示该建筑的关系网
      if (store.selectedBuildingForKG) {
        loadBuildingGraph(store.selectedBuildingForKG)
        viewStack.value = ["building"]
      } else {
        loadOverview()
      }
    })
  }
})
</script>

<style scoped>
.rag-box { flex: 1; min-width: 0; height: 20vh; display: flex; flex-direction: column; border: 1px solid var(--glass-border); background: var(--glass-highlight), var(--glass-bg); backdrop-filter: blur(var(--glass-blur)) saturate(1.4); -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.4); box-shadow: var(--glass-shadow); border-radius: var(--glass-radius); cursor: pointer; transition: all 0.4s ease; }
.rag-box:hover { box-shadow: var(--glass-hover-shadow); border-color: var(--glass-hover-border); }

/* Flash animation when a building point is clicked */
.rag-box.kg-flash {
  animation: kgBorderFlash 1.2s ease-out;
}
@keyframes kgBorderFlash {
  0%   { border-color: rgba(156, 0, 0, 0.85); box-shadow: 0 0 12px rgba(156, 0, 0, 0.45), var(--glass-shadow); }
  25%  { border-color: rgba(156, 0, 0, 0.35); box-shadow: 0 0 4px rgba(156, 0, 0, 0.15), var(--glass-shadow); }
  50%  { border-color: rgba(156, 0, 0, 0.85); box-shadow: 0 0 14px rgba(156, 0, 0, 0.5), var(--glass-shadow); }
  75%  { border-color: rgba(156, 0, 0, 0.25); box-shadow: var(--glass-shadow); }
  100% { border-color: var(--glass-border); box-shadow: var(--glass-shadow); }
}

.component-header { display: flex; align-items: center; margin-bottom: 10px; padding: 15px; opacity: 0.75; }
.arrow { width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 8px solid var(--text-primary); margin-right: 5px; transition: border-color 0.4s; }
.component-header span { font-weight: bold; font-size: 16px; font-family: "DengXian", "等线", sans-serif; color: var(--text-primary); transition: color 0.4s; }

.kg-logo-container { width: 70%; height: 70%; display: flex; justify-content: flex-end; align-items: flex-end; position: relative; left: 40px; }
.kg-logo-image { width: 100%; height: 100%; object-fit: contain; }

.knowledge-graph-dialog { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 80vw; height: 80vh; background: var(--glass-highlight), var(--float-bg); backdrop-filter: blur(var(--float-blur)) saturate(1.4); -webkit-backdrop-filter: blur(var(--float-blur)) saturate(1.4); border-radius: var(--glass-radius); box-shadow: 0 1px 1px rgba(255,255,255,0.3) inset, 0 8px 32px rgba(0,0,0,0.15); border: 1px solid var(--glass-border); z-index: 1000; display: flex; flex-direction: column; overflow: hidden; }
.dialog-header { padding: 12px 16px; background-color: var(--dialog-header-bg); border-bottom: 1px solid var(--header-border); display: flex; justify-content: space-between; align-items: center; font-size: 16px; font-weight: bold; color: var(--dialog-header-text); transition: background-color 0.4s, color 0.4s; }
.header-actions { display: flex; gap: 8px; align-items: center; }
.back-button, .reset-button { background: var(--badge-bg); border: 1px solid var(--glass-border); border-radius: 6px; padding: 4px 12px; font-size: 13px; cursor: pointer; color: var(--text-primary); transition: all 0.3s; }
.back-button:hover, .reset-button:hover { opacity: 0.8; }
.dialog-content { flex: 1; padding: 16px; overflow: hidden; position: relative; }
.close-button { background: none; border: none; font-size: 24px; cursor: pointer; color: var(--text-secondary); padding: 0; line-height: 1; transition: color 0.3s; }
.close-button:hover { color: var(--text-primary); }
.knowledge-graph-network { width: 100%; height: 100%; background-color: var(--desc-bg); border: 1px solid var(--glass-border); transition: background-color 0.4s, border-color 0.4s; }

.loading-overlay { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: var(--badge-bg); padding: 12px 24px; border-radius: 8px; font-size: 14px; color: var(--text-primary); z-index: 10; border: 1px solid var(--glass-border); }

.graph-legend { display: flex; flex-wrap: wrap; align-items: center; padding: 10px; background-color: var(--legend-bg); border-top: 1px solid var(--legend-border); height: 60px; transition: background-color 0.4s, border-color 0.4s; }
.legend-item { display: flex; align-items: center; margin-right: 16px; }
.legend-color { width: 14px; height: 14px; margin-right: 4px; border: 1px solid var(--legend-border); border-radius: 50%; }
.legend-text { font-size: 12px; color: var(--text-primary); }
.graph-tip { margin-left: auto; font-style: italic; color: var(--text-secondary); font-size: 12px; transition: color 0.4s; }
</style>
