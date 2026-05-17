<template>
  <div class="coordinate-list">
    <h3>Coordinates</h3>
    <ul>
      <li v-for="(category, index) in localCoordinates" :key="index">
        <strong @click="toggleCategory(index)">{{ category.label }}</strong>
        <ul v-if="category.visible">
          <li
            v-for="(coord, subIndex) in category.items"
            :key="subIndex"
            @click="flyTo(coord, subIndex)"
            @mouseover="highlightMarker(subIndex)"
            @mouseleave="removeHighlightMarker(subIndex)"
            :class="{ highlighted: highlightedItem === subIndex }"
          >
            {{ coord.label }} [{{ coord.lat }}, {{ coord.lng }}]
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"

// 使用 props
const props = defineProps<{ coordinates: any[] }>()

// 创建本地状态的副本
const localCoordinates = ref(props.coordinates.map(category => ({ ...category, visible: false })))

// 定义 highlightedItem 用来追踪当前高亮的项
const highlightedItem = ref<number | null>(null)

const toggleCategory = (index: number) => {
  // 切换当前点击的类别的可见性
  localCoordinates.value[index].visible = !localCoordinates.value[index].visible
  
  // 确保其他类别被折叠
  localCoordinates.value.forEach((category, idx) => {
    if (idx !== index) {
      category.visible = false
    }
  })
}

const flyTo = (coord: { label: string; lat: number; lng: number }, subIndex: number) => {
  highlightedItem.value = subIndex
  // 这里添加地图飞行到指定坐标的逻辑
  console.log(`飞行到: ${coord.label} [${coord.lat}, ${coord.lng}]`)
}

const highlightMarker = (subIndex: number) => {
  highlightedItem.value = subIndex
  // 这里添加高亮标记的逻辑
  console.log(`高亮显示项索引: ${subIndex}`)
}

const removeHighlightMarker = (subIndex: number) => {
  if (highlightedItem.value === subIndex) {
    highlightedItem.value = null
  }
  // 这里添加移除高亮标记的逻辑
  console.log(`移除高亮显示项索引: ${subIndex}`)
}
</script>

<style scoped>
.coordinate-list ul {
  list-style-type: none;
  padding-left: 10px;
}

.coordinate-list ul li {
  cursor: pointer;
  padding: 5px;
  border-radius: 8px;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.coordinate-list ul li.highlighted {
  border: 2px solid blue;
}

.coordinate-list ul li:hover {
  background-color: #f0f8ff;
  border: 2px solid blue;
}
</style>
