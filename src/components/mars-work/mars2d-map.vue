<template>
  <div class="page_container">
    <!-- 聊天框部分 -->
    <div class="gpt4-chatbox">
      <div class="component-header">
        <div class="arrow"></div>
        <span>问答</span>
      </div>
      <div class="chat-content">
        <p v-for="(msg, index) in chatMessages" :key="index" :class="msg.startsWith('User:') ? 'user-message' : ''" v-html="msg"></p>
              <!-- 主题搜索结果显示区域 -->
        <div v-if="themeSearchResults && themeSearchResults.length > 0" class="theme-results">
          <div class="theme-results-header">
            <span>🏛️相关建筑结果</span>
          </div>
          <div class="theme-results-list">
            <div 
              v-for="(building, index) in themeSearchResults" 
              :key="index"
              class="result-item"
              @click="jumpToBuildingAndSwitchKeywords(building.coordinate)"
            >
              <span class="result-number">{{ index + 1 }}</span>
              <div class="result-content">
                <span class="result-name">{{ building.name }}</span>
                <div class="result-details">
                  <span v-if="building.city" class="result-city">📍{{ building.city }}</span>
                  <span v-if="building.structure" class="result-structure">🏗️{{ building.structure }}</span>
                  <span v-if="building.year" class="result-year">📅{{ building.year }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- 测试按钮 -->
        <!-- <button @click="testThemeSearch" style="margin: 10px; padding: 5px 10px; background: #4CAF50; color: white; border: none; border-radius: 4px;">
          测试主题搜索
        </button> -->
        <div class="input-container">
          <textarea v-model="userInput" placeholder="Type here"></textarea>
          <button @click="sendMessage">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="30"
              height="30"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="feather feather-send"
            >
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </div>
    </div>
    <div class="map-container">
      <!-- 地图部分 -->
      <div class="component-header">
        <div class="arrow"></div>
        <span>地图</span>
      </div>
      <div :id="withKeyId" class="mars2d-container"></div>
    </div>

    <!-- 侧边面板 -->
    <div class="side-panel">
      <!-- 统计部分 -->
      <div class="component-header">
        <div class="arrow"></div>
        <span>数据</span>
      </div>
      
      <!-- 图表容器 - 设置为并排显示 -->
      <div class="charts-container">
        <!-- 柱状图容器 -->      
        <div class="chart-box">        
          <div class="component-header">         
            <div class="arrow"></div>          
            <span>地区筛选</span>        
          </div>        
          <div ref="barChartContainer" class="chart-container"></div>    
        </div>      
        
        <!-- 饼图容器 -->     
        <div class="chart-box">        
          <div class="component-header">        
            <div class="arrow"></div>         
            <span>年代筛选</span>       
          </div>       
          <div ref="pieChartContainer" class="chart-container"></div>     
        </div>
      </div>

      <div class="knowledge-row-container" style="display: flex; width: 100%; margin: 10px 0; gap: 20px;">
        <!-- 左侧 rag-box - 修改为单个知识图谱缩略图 -->
        <div class="rag-box" style="width: 48% !important; flex: 0 0 48% !important; height: 20vh; display: inline-block !important; border: 2px solid rgba(177, 177, 177, 0.308); background-color: rgba(236, 232, 232, 0.2); box-shadow: 0 0 10px rgba(216, 214, 214, 0.8); border-radius: 8px; cursor: pointer;" @click="showKnowledgeGraphDialog = true">
          <div class="component-header">
            <div class="arrow"></div>
            <span>知识图谱</span>
          </div>
          <!-- 知识图谱缩略图 -->
          <div class="kg-logo-container">
            <img class="kg-logo-image" src="/src/KGlogo2.png" alt="KG" />
            <div class="kg-logo-overlay">
              <span class="kg-logo-text">点击查看</span>
            </div>
          </div>
        </div>
        
        <!-- 右侧词义图 -->
        <div class="keyword-graph" style="width: 43% !important; flex: 0 0 48% !important; height: 20vh; display: inline-block !important; vertical-align: top; border: 2px solid rgba(177, 177, 177, 0.308); background-color: rgba(236, 232, 232, 0.2); box-shadow: 0 0 10px rgba(216, 214, 214, 0.8); border-radius: 8px;">
          <div class="component-header">
          <div class="arrow"></div>
          <span>词云图</span>
        </div>
        
        <!-- 使用图片替代原有词云 -->
        <div class="word-cloud-container" ref="cloudContainer" style="display: flex; justify-content: center; align-items: center; padding: 0;">
          <img :src="currentKeywordsImage" style="width: 98%; height: 100%; object-fit: contain; transform: translateY(-25px); transform: translateX(-5px);" alt="关键词云" />
        </div>
        
        <!-- 原词云显示区域（已隐藏） -->
        <div style="display: none;">
          <div 
            v-for="(word, index) in keywordsList" 
            :key="index" 
            class="keyword-item"
            :style="{
              fontSize: calculateFontSize(word.count) + 'px',
              fontWeight: calculateFontWeight(word.count),
              opacity: calculateOpacity(word.count),
              color: getRandomColor(index),
              left: word.left || '50%',
              top: word.top || '50%',
              writingMode: word.vertical ? 'vertical-lr' : 'horizontal-tb',
              letterSpacing: word.vertical ? '0px' : 'normal'
            }"
          >
            {{ word.text }}
          </div>
        </div>
      </div>
    </div>


      <div class="new-description-container">
        <div class="component-header">
          <div class="arrow"></div>
          <span>详细信息</span>
        </div>

        <div v-if="selectedBuilding">
          <h2 class="oldfont">{{ selectedBuilding?.label }}</h2>

          <div class="building-category">
            <img :src="findBuildingCategory(selectedBuilding, coordinates) === 'GX Buildings' && selectedBuildingCity ? 
                       createColoredDotIcon(getGXBuildingCityColor(selectedBuildingCity), 20) : 
                       getIconUrlByLabel(findBuildingCategory(selectedBuilding, coordinates))" 
                 alt="icon" class="label-icon" />
            <span>{{ 
              findBuildingCategory(selectedBuilding, coordinates) === 'GX Buildings' && selectedBuildingCity ? 
              selectedBuildingCity : 
              findBuildingCategory(selectedBuilding, coordinates) 
            }}</span>
          </div>
          
          <div v-if="selectedBuildingYear" class="year-tag-detail" 
               :style="{ 
                 color: getBuildingYearStyle(selectedBuildingYear).color,
                 backgroundColor: getBuildingYearStyle(selectedBuildingYear).background,
                 borderColor: getBuildingYearStyle(selectedBuildingYear).borderColor
               }">
            <span class="year-label">建造年代：</span>
            <span class="year-value">{{ getSimplifiedYear(selectedBuildingYear) }}</span>
          </div>
          
          <div v-if="selectedBuildingStructure" class="structure-tag-detail" 
               :style="{ 
                 color: getBuildingStructureStyle(selectedBuildingStructure).color,
                 backgroundColor: getBuildingStructureStyle(selectedBuildingStructure).background,
                 borderColor: getBuildingStructureStyle(selectedBuildingStructure).borderColor
               }">
            <span class="structure-label">建筑结构：</span>
            <span class="structure-value">{{ getSimplifiedStructure(selectedBuildingStructure) }}</span>
          </div>
          
          <p class="description-box"><strong>建筑描述</strong>: {{ selectedBuildingDescription }}</p>
        </div>
        <div v-if="selectedBuilding" class="image-display">
        <div class="image-gallery">
          <img
            v-for="(img, index) in selectedBuildingImage.slice(0, 5)"
            :key="index"
            :src="img"
            @error="() => onImageError(index)"
            alt="Building Image"
            class="gallery-image"
          />  
        </div>
        </div>
      </div>
    </div>

    <!-- 浮动窗口部分 -->
<!-- 浮动窗口部分：仅在 hoveredBuilding 存在时显示 -->
  <div v-if="hoveredBuilding" class="floating-window" :style="floatingWindowStyle">
    <h2>{{ hoveredBuilding.label }}</h2>
    <div class="building-info-row">
      <img 
        :src="findBuildingCategory(hoveredBuilding, coordinates) === 'GX Buildings' && hoveredBuildingCity ? 
               createColoredDotIcon(getGXBuildingCityColor(hoveredBuildingCity), 20) : 
               getIconUrlByLabel(findBuildingCategory(hoveredBuilding, coordinates))" 
        alt="icon" 
        class="label-icon" 
      />
      <span>{{ 
        findBuildingCategory(hoveredBuilding, coordinates) === 'GX Buildings' && hoveredBuildingCity ? 
        hoveredBuildingCity : 
        findBuildingCategory(hoveredBuilding, coordinates) 
      }}</span>
    </div>
    <div class="tag-container">
      <div v-if="hoveredBuildingYear" class="year-tag" 
           :style="{ 
             color: getBuildingYearStyle(hoveredBuildingYear).color,
             backgroundColor: getBuildingYearStyle(hoveredBuildingYear).background,
             borderColor: getBuildingYearStyle(hoveredBuildingYear).borderColor
           }">
        {{ getSimplifiedYear(hoveredBuildingYear) }}
      </div>
      <div v-if="hoveredBuildingStructure" class="structure-tag" 
           :style="{ 
             color: getBuildingStructureStyle(hoveredBuildingStructure).color,
             backgroundColor: getBuildingStructureStyle(hoveredBuildingStructure).background,
             borderColor: getBuildingStructureStyle(hoveredBuildingStructure).borderColor
           }">
        {{ getSimplifiedStructure(hoveredBuildingStructure) }}
      </div>
    </div>
    <p>{{ hoveredBuildingDescription }}</p>
  </div>
</div>


  <!--
    <div class="description-container">
    <div class="component-header">
    <div class="arrow"></div>
    <span>Details</span>
  </div>
   详情部分 
  <div v-if="selectedBuilding">
    <h2 class="oldfont">{ selectedBuilding?.label }}</h2>
    
    <div class="building-category">
      <img 
        :src="getIconUrlByLabel(findBuildingCategory(selectedBuilding, coordinates))" 
        alt="icon" 
        class="label-icon" 
      />
      <span>{ findBuildingCategory(selectedBuilding, coordinates) }}</span>
    </div>
    
     展示批次信息的绿色框 
    <div v-if="historicalBuildingBatch" class="batch-greencontainer">
      { historicalBuildingBatch }}
    </div>
    
    <p class="description-box">Description: { selectedBuildingDescription }}</p>
  </div>
  
  <div v-else>
    <p>Please select a building for more details.</p>
  </div>
</div>
 -->

<!-- 知识图谱对话框 -->
<div v-if="showKnowledgeGraphDialog" class="knowledge-graph-dialog">
  <div class="dialog-header">
    <span>建筑知识图谱</span>
    <button @click="showKnowledgeGraphDialog = false" class="close-button">×</button>
  </div>
  <div class="dialog-content">
    <div ref="graphNetworkContainer" class="knowledge-graph-network" style="background-color: #f0f0f0;"></div>
    <!-- 图谱说明区域 -->
    <div class="graph-legend">
      <div class="legend-item">
        <div class="legend-color building-color"></div>
        <div class="legend-text">建筑</div>
      </div>
      <div class="legend-item">
        <div class="legend-color category-color"></div>
        <div class="legend-text">类别</div>
      </div>
      <div class="legend-item">
        <div class="legend-color address-color"></div>
        <div class="legend-text">地址</div>
      </div>
      <div class="legend-item">
        <div class="legend-color type-color"></div>
        <div class="legend-text">建筑类型</div>
      </div>
      <div class="legend-item">
        <div class="legend-color renovation-color"></div>
        <div class="legend-text">改造项目</div>
      </div>
      <div class="graph-tip">提示：可拖动、缩放、点击节点查看详情</div>
    </div>
  </div>
</div>
</template>

<script setup lang="ts">
/* =========================================
 * 1. 导入 & 类型声明
 * ========================================= */
import { ref, computed, onBeforeUnmount, onMounted, watch, nextTick } from "vue"
import * as L from "leaflet"
import * as mars2d from "mars2d"
import * as echarts from "echarts" // 引入 ECharts
import * as XLSX from "xlsx" // 引入xlsx处理库
// 知识图谱相关
// @ts-ignore
import { DataSet, Network } from "vis-network/standalone"

type CustomMarker = L.Marker & { 
  category: string
  buildingName: string
  buildingYear?: string 
  buildingCity?: string 
}

/* =========================================
 * 2. defineProps & defineEmits
 * ========================================= */
const props = withDefaults(
  defineProps<{
    url: string
    mapKey?: string
    options?: any
  }>(),
  {
    url: "",
    mapKey: "default",
    options: () => ({})
  }
)

const emit = defineEmits(["onload"])

/* =========================================
 * 3. 工具函数
 * ========================================= */



/* =========================================
 * 4. 所有的响应式 const / let
 * ========================================= */

/** 地图实例 */
let map: mars2d.Map
// 知识图谱对话框显示控制
const showKnowledgeGraphDialog = ref(false)
const graphNetworkContainer = ref(null) // 知识图谱网络容器
const knowledgeGraphNetwork = ref(null) // 知识图谱网络实例
// 存储从地图选中的建筑，用于在KG中高亮显示
const selectedBuildingForKG = ref<string | null>(null)
// 控制关键词图片显示
const showKeywords3 = ref(true)
// 建筑信息处理相关变量
const processedData = ref([]) // 存储处理后的数据
const processingStatus = ref("") // 处理状态信息
const coordinates = ref([
  {
    label: "Commercial Buildings",
    visible: false,
    items: [
      { label: "中国出口商品交易会流花路旧址", lat: 23.14296, lng: 113.257971 },
      { label: "太如茶楼旧址", lat: 23.11357, lng: 113.252397 },
      { label: "光复中路当楼旧址", lat: 23.117014, lng: 113.251563 },
      { label: "添男茶楼旧址", lat: 23.112217, lng: 113.25058 },
      { label: "生隆昌老号旧址", lat: 23.112398, lng: 113.252478 },
      { label: "大同酒家", lat: 23.108482, lng: 113.254793 },
      { label: "山庄旅舍", lat: 23.19637, lng: 113.308289 },
      { label: "白云宾馆", lat: 23.13774, lng: 113.286536 },
      { label: "花园酒店", lat: 23.135124, lng: 113.286216 },
      { label: "流花宾馆北楼", lat: 23.146517, lng: 113.25632 },
      { label: "流花宾馆南楼", lat: 23.146163, lng: 113.256218 },
      { label: "广东迎宾馆碧海楼", lat: 23.129634, lng: 113.261167 },
      { label: "广东迎宾馆净慧楼", lat: 23.128486, lng: 113.261321 },
      { label: "广东迎宾馆六榕楼", lat: 23.12842, lng: 113.259972 },
      { label: "羊城宾馆旧址", lat: 23.13932, lng: 113.258599 },
      { label: "东方宾馆西楼", lat: 23.13932, lng: 113.258599 },
      { label: "中国大酒店", lat: 23.139938, lng: 113.26044 },
      { label: "广州宾馆", lat: 23.115912, lng: 113.265621 },
      { label: "矿泉别墅旧址", lat: 23.163054, lng: 113.253873 },
      { label: "北平旅店旧址", lat: 23.109118, lng: 113.255599 },
      { label: "新爱群大厦", lat: 23.109473, lng: 113.257038 },
      { label: "大新路276号骑楼", lat: 23.115898, lng: 113.257911 },
      { label: "大新路278号骑楼", lat: 23.115848, lng: 113.25779 },
      { label: "大新路407、409号骑楼", lat: 23.114977, lng: 113.254457 },
      { label: "广九四马路21、23号骑楼", lat: 23.118319, lng: 113.281711 },
      { label: "惠福西路106号骑楼", lat: 23.120325, lng: 113.256645 },
      { label: "人民南路140号骑楼", lat: 23.113198, lng: 113.253512 },
      { label: "文德路53、55、57、59号骑楼", lat: 23.121945, lng: 113.272065 },
      { label: "沿江西路55、57号骑楼", lat: 23.108053, lng: 113.253627 },
      { label: "大新路341号骑楼", lat: 23.115297, lng: 113.255883 },
      { label: "大新路343号骑楼", lat: 23.115315, lng: 113.255891 },
      { label: "大新路349号骑楼", lat: 23.115298, lng: 113.255787 },
      { label: "海珠南路152、152-1、152-2、152-3号骑楼", lat: 23.114148, lng: 113.2568 },
      { label: "海珠中路113号骑楼", lat: 23.120148, lng: 113.256261 },
      { label: "南华西路77、79号骑楼", lat: 23.10532, lng: 113.254022 },
      { label: "中国福安保险公司广州分公司旧址", lat: 23.111653, lng: 113.251956 },
      { label: "位元堂旧址", lat: 23.112392, lng: 113.252413 }
      /*
      { label: "位元堂栈房旧址", lat: 23.112358, lng: 113.252223 },
      { label: "黄耀南老药行旧址", lat: 23.111987, lng: 113.251205 },
      { label: "下九路天喜堂旧址", lat: 23.113858, lng: 113.246794 },
      { label: "大新路107号骑楼", lat: 23.116384, lng: 113.26171 },
      { label: "大新路73、75号骑楼", lat: 23.1165, lng: 113.262444 },
      { label: "一德路173、175、177、179、181号骑楼", lat: 23.113791, lng: 113.261841 },
      { label: "安亚药行旧址", lat: 23.112365, lng: 113.255149 },
      { label: "香港中国康年人寿保险公司旧址", lat: 23.112338, lng: 113.255085 },
      { label: "东里大街商铺旧址", lat: 22.827282, lng: 113.507313 },
      { label: "北京路370号骑楼", lat: 23.127101, lng: 113.268972 },
      { label: "西湖路80号骑楼", lat: 23.123095, lng: 113.26529 },
      { label: "西湖路82号骑楼", lat: 23.123047, lng: 113.265188 },
      { label: "恩宁路46~54号（双号）骑楼", lat: 23.115284, lng: 113.236596 },
      { label: "恩宁路140号骑楼", lat: 23.114053, lng: 113.238542 },
      { label: "恩宁路255、257号骑楼", lat: 23.11351, lng: 113.241028 },
      { label: "陈永记旧址", lat: 23.116908, lng: 113.249031 },
      { label: "皇上皇腊味店", lat: 23.11385, lng: 113.246152 },
      { label: "蛇王福旧址", lat: 23.111788, lng: 113.252757 },
      { label: "黄河洋行旧址", lat: 23.111829, lng: 113.251524 },
      { label: "黄祥华如意油广州总店旧址", lat: 23.112281, lng: 113.251966 },
      { label: "天泉银号旧址", lat: 23.112771, lng: 113.251959 },
      { label: "西荣巷32号后货楼旧址", lat: 23.11382, lng: 113.252047 },
      { label: "道亨银号货楼旧址", lat: 23.112257, lng: 113.252526 },
      { label: "人民南路185号骑楼", lat: 23.114416, lng: 113.252703 },
      { label: "人民南路33号骑楼", lat: 23.109899, lng: 113.253661 },
      { label: "人民南路35号骑楼", lat: 23.109857, lng: 113.253786 },
      { label: "人民南路37号骑楼", lat: 23.109832, lng: 113.253821 },
      { label: "人民南路7号骑楼", lat: 23.108865, lng: 113.253795 },
      { label: "荣珍酒楼旧址", lat: 23.115268, lng: 113.249843 },
      { label: "上九路72号骑楼", lat: 23.115531, lng: 113.25101 },
      { label: "富国茶楼旧址", lat: 23.110626, lng: 113.246118 }
       */
    ]
  },
  {
    label: "Military Buildings",
    visible: false,
    items: [
      { label: "民国广东警备司令部旧址", lat: 23.13023, lng: 113.267167 },
      { label: "沙湾镇北村民兵营部旧址", lat: 22.903745, lng: 113.334401 },
      { label: "粤赣湘边纵队东江第三支队六团增城人民常备第二大队部旧址", lat: 23.286264, lng: 113.838653 },
      { label: "上塘村炮楼", lat: 23.149988, lng: 113.832437 },
      { label: "石迳村炮楼", lat: 23.236995, lng: 113.679568 },
      { label: "民乐村炮楼", lat: 23.546277, lng: 113.585226 },
      { label: "五丰村鲇鱼塘", lat: 23.546277, lng: 113.585226 },
      { label: "石岭村碉楼", lat: 23.703706, lng: 113.657611 },
      { label: "民国广东警备司令部旧址", lat: 23.130231, lng: 113.267167 }
    ]
  },
  {
    label: "Religious Buildings",
    visible: false,
    items: [
      /*
      { label: "小洲村玉虚宫", lat: 23.061028, lng: 113.355997 },
      { label: "同福中路伍氏宗祠旧址", lat: 23.103996, lng: 113.257574 },
      { label: "方石曹氏宗祠", lat: 23.319805, lng: 113.288335 },
      { label: "广伦钟公祠", lat: 23.244256, lng: 113.283213 },
      { label: "南野公祠", lat: 23.546277, lng: 113.585226 },
      { label: "必遂李公祠", lat: 23.546277, lng: 113.585226 },
      { label: "寅中祖楼", lat: 23.546277, lng: 113.585226 },
      { label: "仁卿李公祠", lat: 23.546277, lng: 113.585226 },
      { label: "东林梁公祠", lat: 23.052134, lng: 113.374942 },
      { label: "元始梁公祠", lat: 23.050954, lng: 113.373817 },
      { label: "南园崔公祠", lat: 23.047802, lng: 113.372137 },
      { label: "北亭村陈氏宗祠", lat: 23.047285, lng: 113.372265 },
      { label: "愚菴崔公祠", lat: 23.047285, lng: 113.372265 },
      { label: "福缘林公祠", lat: 22.964403, lng: 113.354433 },
      { label: "斐客白公祠", lat: 23.080506, lng: 113.333954 },
      { label: "洪积刘公祠", lat: 23.374185, lng: 113.266123 },
      { label: "贤德刘公祠", lat: 23.374185, lng: 113.266123 },
      { label: "文鳯陆公祠", lat: 23.103278, lng: 113.46463 },
      { label: "秀之刘公祠", lat: 23.20335, lng: 113.53686 },
      { label: "郑田庙岭村石王古庙", lat: 23.217179, lng: 113.827773 },
      { label: "长流村镇庆庙", lat: 23.736767, lng: 113.803976 },
      { label: "沙湾镇承芳里社稷坛", lat: 22.907173, lng: 113.335969 },
      { label: "沙湾镇何氏翰林祠", lat: 22.905033, lng: 113.337591 },
      { label: "沙湾镇何氏三代文魁祠", lat: 22.907578, lng: 113.340768 },
      { label: "伯季合祠", lat: 23.076809, lng: 113.513388 },
      { label: "济川江公祠", lat: 23.279395, lng: 113.235404 },
      { label: "羽吾大夫祠", lat: 23.273033, lng: 113.237548 },
      { label: "南清江公祠", lat: 23.311312, lng: 113.240493 },
      { label: "宥庄沈公祠", lat: 23.325988, lng: 113.285755 },
      { label: "永荫堂", lat: 23.34957, lng: 113.291662 },
      { label: "国政周公祠", lat: 23.165352, lng: 113.240501 },
      { label: "白土村和益南街方氏祠堂", lat: 23.357504, lng: 113.43059 },
      { label: "光明村宋氏祠堂", lat: 23.33818, lng: 113.415153 },
      { label: "光明村梅州司铎", lat: 23.33765, lng: 113.416094 },
      { label: "岭东村冯公四房祠", lat: 22.790564, lng: 113.396373 },
      { label: "仲贵祖祠", lat: 22.764949, lng: 113.579407 },
      { label: "塘坑村朱氏公祠", lat: 22.753098, lng: 113.573064 },
      { label: "林隐陈公祠", lat: 23.037954, lng: 113.451157 },
      { label: "沙涌村祠堂", lat: 22.956052, lng: 113.425467 },
      { label: "礼村高氏二房祠堂", lat: 23.040805, lng: 113.312638 },
      { label: "潭山村天后宫", lat: 22.992833, lng: 113.449823 },
      { label: "南昌祖祠", lat: 23.048176, lng: 113.445768 },
      { label: "江南村李氏宗祠", lat: 22.992414, lng: 113.368022 },
      { label: "楚庭陈公祠", lat: 22.983587, lng: 113.399634 },
      { label: "茂盛陈公祠", lat: 22.983914, lng: 113.399786 },
      { label: "紫坭村韩氏宗祠", lat: 22.896683, lng: 113.290696 },
      { label: "秉熙曾公祠", lat: 22.961393, lng: 113.434121 },
      { label: "李氏宗祠（敦本堂）", lat: 23.122054, lng: 113.233391 },
      { label: "礼祐关公祠", lat: 23.059294, lng: 113.234761 },
      { label: "善崙蔡公祠", lat: 23.128874, lng: 113.233617 },
      { label: "德华潘公祠", lat: 23.127346, lng: 113.340076 },
      { label: "上社村仁圣宫", lat: 23.13481, lng: 113.373299 },
      { label: "慕隐潘公祠", lat: 23.125427, lng: 113.386516 },
      { label: "镇龙村黄氏宗祠", lat: 23.27971, lng: 113.57342 },
      { label: "伦江张公祠", lat: 23.081318, lng: 113.501179 },
      { label: "横坑村观音古庙", lat: 23.130587, lng: 113.460339 },
      { label: "子安刘公祠", lat: 23.203473, lng: 113.535129 },
      { label: "颖远任公祠", lat: 23.436279, lng: 113.052397 },
      { label: "自求钟公祠", lat: 23.340283, lng: 113.096101 },
      { label: "直斋公祠", lat: 23.197042, lng: 113.769726 },
      { label: "仙塘村冯氏宗祠", lat: 23.152781, lng: 113.825011 },
      { label: "诒榖单公祠", lat: 23.165483, lng: 113.801021 },
      { label: "东洲村东洲大道钟氏大宗祠", lat: 23.098219, lng: 113.592361 },
      { label: "湾谷村罗氏祠堂", lat: 23.201741, lng: 113.665791 },
      { label: "郭村达宽郭公祠", lat: 22.935567, lng: 112.182537 },
      { label: "光耀村又昌路陈氏祠堂", lat: 23.3549, lng: 113.854952 },
      { label: "光耀村新屋路陈氏祠堂", lat: 23.3549, lng: 113.854952 },
      { label: "黄塘村梁氏宗祠", lat: 23.403936, lng: 113.852769 },
      { label: "西湖滩村郑氏祠堂", lat: 23.403327, lng: 113.890401 },
       */
      { label: "老屋村郭氏祠堂", lat: 23.371006, lng: 113.618712 },
      { label: "横塱村刘氏宗祠", lat: 23.257928, lng: 113.71489 },
      { label: "君松徐公祠", lat: 23.546277, lng: 113.585226 },
      { label: "龙聚村曾氏宗祠", lat: 23.546277, lng: 113.585226 },
      { label: "龙聚村胡氏宗祠", lat: 23.546277, lng: 113.585226 },
      { label: "龙聚村胡氏祠堂", lat: 23.546277, lng: 113.585226 },
      { label: "济尧梁公祠", lat: 23.57576, lng: 113.425751 },
      { label: "悦涯祖祠", lat: 23.546277, lng: 113.585226 },
      { label: "春盛公祠", lat: 23.546277, lng: 113.585226 },
      { label: "埔顶将军楼", lat: 23.546277, lng: 113.585226 },
      { label: "大凹村李氏宗祠", lat: 23.511276, lng: 113.558123 },
      { label: "约斋黄公祠", lat: 23.546277, lng: 113.585226 },
      { label: "南向村钟氏宗祠", lat: 23.546277, lng: 113.585226 },
      { label: "天颖廖公祠", lat: 23.546277, lng: 113.585226 },
      { label: "原英陈公祠", lat: 23.546277, lng: 113.585226 },
      { label: "民国广东警备司令部旧址", lat: 23.13023, lng: 113.267167 }
    ]
  },
  {
    label: "Public Buildings",
    visible: false,
    items: [
      /*
      { label: "华南土特产展览交流大会旧址水产馆", lat: 23.109669, lng: 113.251401 },
      { label: "华南土特产展览交流大会旧址省际馆", lat: 23.109669, lng: 113.251401 },
      { label: "华南土特产展览交流大会旧址手工业馆", lat: 23.109669, lng: 113.251401 },
      { label: "华南土特产展览交流大会旧址水果蔬菜馆", lat: 23.109669, lng: 113.251401 },
      { label: "华南土特产展览交流大会旧址门楼", lat: 23.109669, lng: 113.251401 },
      { label: "西汉南越王博物馆建筑群", lat: 23.138452, lng: 113.261319 },
      { label: "广东科学馆大楼", lat: 23.13284, lng: 113.262844 },
      { label: "广州中苏友好大厦旧址", lat: 23.14296, lng: 113.257971 },
      { label: "友谊剧院", lat: 23.145134, lng: 113.257519 },
      { label: "广东省农业展览馆旧址", lat: 23.138707, lng: 113.299932 },
      { label: "广州美术学院主楼", lat: 23.093278, lng: 113.279114 },
      { label: "救亡日报社南迁广州旧址", lat: 23.118259, lng: 113.250973 },
      { label: "明心书院建筑群旧址之一", lat: 23.101101, lng: 113.238494 },
      { label: "明心书院建筑群旧址之二", lat: 23.098814, lng: 113.238938 },
      { label: "明心书院建筑群旧址之三", lat: 23.099766, lng: 113.239608 },
      { label: "明心书院建筑群旧址之四", lat: 23.098711, lng: 113.238746 },
      { label: "明心书院建筑群旧址之五", lat: 23.098711, lng: 113.238746 },
      { label: "广州市第二中学教学楼旧址 （一中楼）", lat: 23.113169, lng: 113.23467 },
      { label: "华南工学院办公大楼旧址", lat: 23.150129, lng: 113.347859 },
      { label: "华南工学院化工实验室大楼旧址", lat: 23.150129, lng: 113.347859 },
      { label: "华南工学院化工系楼旧址", lat: 23.150129, lng: 113.347859 },
      { label: "华南工学院数学电讯楼旧址", lat: 23.150129, lng: 113.347859 },
      { label: "华南工学院图书馆旧址", lat: 23.152082, lng: 113.345982 },
      { label: "华南工学院物理楼旧址", lat: 23.150129, lng: 113.347859 },
      { label: "华南工学院综合教学楼旧址", lat: 23.150129, lng: 113.347859 },
      { label: "广州市总工会办公楼", lat: 23.131369, lng: 113.260653 },
      { label: "广州市总工会礼堂", lat: 23.131369, lng: 113.260653 },
      { label: "广东国民大学第二校舍旧址", lat: 23.12025, lng: 113.257865 },
      { label: "教育路何氏书院旧址", lat: 23.123822, lng: 113.265643 },
      { label: "考亭书院旧址", lat: 23.124469, lng: 113.266414 },
      { label: "法国天主教会东山安老院旧址", lat: 23.128282, lng: 113.305099 },
      { label: "广州大中中学旧址", lat: 23.136451, lng: 113.273706 },
      { label: "见大书院旧址", lat: 23.124901, lng: 113.266858 },
      { label: "广东妇女解放协会旧址", lat: 23.121496, lng: 113.277685 },
      { label: "中山医学院药理寄生虫楼旧址", lat: 23.129506, lng: 113.289218 },
      { label: "中西医院旧址", lat: 23.108252, lng: 113.26361 },
      { label: "伍家祠道教会医院旧址", lat: 23.1038, lng: 113.257098 },
      { label: "两广浸信会医院附属建筑旧址", lat: 23.121925, lng: 113.293612 },
      { label: "达保罗医院旧址", lat: 23.119646, lng: 113.253181 },
      { label: "奇和堂药局旧址", lat: 23.11211, lng: 113.247439 },
      { label: "明珠影画院旧址", lat: 23.111697, lng: 113.260891 },
      { label: "广东国际大厦", lat: 23.138617, lng: 113.282611 },
      { label: "趣园红楼旧址", lat: 23.092528, lng: 113.252207 },
      { label: "民国广州第十一区警署警察宿舍旧址", lat: 23.102172, lng: 113.269735 },
      { label: "华南工学院南一宿舍1~6号旧址", lat: 23.152082, lng: 113.345982 },
      { label: "先施公司附属建筑群旧址", lat: 23.111725, lng: 113.25826 },
      { label: "智兴街明园", lat: 23.128807, lng: 113.280749 },
      { label: "慎园", lat: 23.119168, lng: 113.296978 },
      { label: "平正纪念楼", lat: 23.123333, lng: 113.294546 },
      { label: "进园", lat: 23.122265, lng: 113.299434 },
      { label: "华南植物园水榭", lat: 23.186873, lng: 113.367191 },
      { label: "兰圃", lat: 23.142594, lng: 113.259982 },
      { label: "著义小学校旧址（门楼）", lat: 23.296653, lng: 113.26835 },
      { label: "五龙岗村学校旧址（门楼）", lat: 23.244256, lng: 113.283213 },
      { label: "枧村渤海里门楼", lat: 23.546277, lng: 113.585226 },
      { label: "枧村仁厚里门楼", lat: 23.546277, lng: 113.585226 },
      { label: "温泉镇乌石村大围队门楼", lat: 23.853954, lng: 113.809549 },
      { label: "北亭村路接青云街门", lat: 23.047938, lng: 113.374915 },
      { label: "大岭村龙津街街门", lat: 22.985158, lng: 113.477564 },
      { label: "大岭村龙荫坊坊门", lat: 22.985158, lng: 113.477564 },
      { label: "大岭村耀德里坊门", lat: 22.985158, lng: 113.477564 },
      { label: "大岭村颖源里坊门", lat: 22.985158, lng: 113.477564 },
      { label: "大岭村沙井气古井", lat: 22.985158, lng: 113.477564 },
      { label: "大岭村大巷巷门", lat: 22.985158, lng: 113.477564 },
      { label: "穗石村长林厚道村门", lat: 23.050558, lng: 113.414741 },
      { label: "穗石村双桂坊门楼", lat: 23.046805, lng: 113.410209 },
      { label: "广东省荣军医院旧址（观鱼亭和碧漪亭）", lat: 23.088857, lng: 113.396211 },
      { label: "茅岗村塘口门楼", lat: 23.110261, lng: 113.433913 },
      { label: "时敏桥", lat: 23.116897, lng: 113.235328 },
      { label: "芳村儿童托养院旧址", lat: 23.098121, lng: 113.243251 },
      { label: "明心书院建筑群旧址之六", lat: 23.098711, lng: 113.238746 },
      { label: "西华路彩虹桥", lat: 23.132227, lng: 113.246943 },
      { label: "佛塱上南客家围屋", lat: 23.369851, lng: 113.532146 },
      { label: "小虎岛人民公社礼堂旧址", lat: 22.843267, lng: 113.532923 },
      { label: "暨南大学办公楼旧址", lat: 23.130324, lng: 113.348478 },
      { label: "华南农业大学亚太地区蚕桑培训中心", lat: 23.159671, lng: 113.351813 },
      { label: "流花湖公园南门", lat: 23.137227, lng: 113.249368 },
      { label: "流花湖公园红桥及葵堤", lat: 23.137227, lng: 113.249368 },
      { label: "东湖公园九曲桥", lat: 23.115193, lng: 113.292052 },
      { label: "东湖公园船闸", lat: 23.115193, lng: 113.292052 },
      { label: "东湖公园西门", lat: 23.115193, lng: 113.292052 },
      { label: "粤汉铁路流溪河大桥", lat: 23.267578, lng: 113.230052 },
      { label: "城郊村逸亭书舍", lat: 23.546277, lng: 113.585226 },
      { label: "高田村平山围门楼", lat: 23.546277, lng: 113.585226 },
      { label: "沙湾镇正园", lat: 22.905865, lng: 113.335966 },
      { label: "沙湾镇沙坑会场", lat: 22.913202, lng: 113.344254 },
      { label: "沙湾镇公局巷孖井", lat: 22.903715, lng: 113.336322 },
      { label: "沙湾镇安宁西街大中堂", lat: 22.902987, lng: 113.335811 },
      { label: "沙湾镇三槐里社稷坛", lat: 22.907173, lng: 113.335969 },
      { label: "沙湾镇何氏福荫堂", lat: 22.902152, lng: 113.33609 },
      { label: "广州美术学院附属中等美术学校南楼", lat: 23.092635, lng: 113.278528 },
      { label: "朗头村近光里巷口书室", lat: 23.352072, lng: 113.075299 },
      { label: "敬思堂", lat: 23.07386, lng: 113.409209 },
      { label: "广州华侨学生补习学校石牌旧址", lat: 23.130324, lng: 113.348478 },
      { label: "中华人民共和国广州华侨学生接待站", lat: 23.151673, lng: 113.331995 },
      { label: "华南农学院7号楼", lat: 23.158908, lng: 113.356424 },
      { label: "华南农学院11号楼", lat: 23.158908, lng: 113.356424 },
      { label: "同安南约门楼", lat: 22.625484, lng: 110.144045 },
      { label: "流花西苑", lat: 23.137227, lng: 113.249368 },
      { label: "广九铁路俱乐部旧址", lat: 23.124396, lng: 113.29853 },
      { label: "梧岗书舍", lat: 23.279395, lng: 113.235404 },
      { label: "泰昌书舍", lat: 23.349783, lng: 113.174852 },
      { label: "德寿里门楼", lat: 23.198038, lng: 113.264467 },
      { label: "丁联社旧址", lat: 23.346792, lng: 113.28584 },
      { label: "沛泽源流门楼", lat: 23.350189, lng: 113.315911 },
      { label: "滘心南堤水闸与滘心乡堤基宪示碑", lat: 23.221884, lng: 113.257489 },
      { label: "月峯书舍", lat: 23.296115, lng: 113.304052 },
      { label: "丽翁书舍", lat: 23.296115, lng: 113.304052 },
      { label: "建阳书舍", lat: 23.296009, lng: 113.305591 },
      { label: "南沙牌坊", lat: 22.80136, lng: 113.533521 },
      { label: "小龙村长巷门楼", lat: 23.017199, lng: 113.395338 },
      { label: "小龙村乡约", lat: 22.961639, lng: 113.435803 },
      { label: "岳溪小学旧址", lat: 22.985285, lng: 113.470347 },
      { label: "先锋四巷门楼", lat: 22.942502, lng: 113.362892 },
      { label: "永汉电影院", lat: 23.12129, lng: 113.26928 },
      { label: "竺园", lat: 23.118486, lng: 113.296568 },
      { label: "培正小学善正楼", lat: 23.119371, lng: 113.287832 },
      { label: "华英医院旧址", lat: 23.131114, lng: 113.286258 },
      { label: "广东大埔同乡会旧址", lat: 23.120796, lng: 113.271993 },
      { label: "坑口村乡约", lat: 23.075889, lng: 113.237214 },
      { label: "《群声报》报馆旧址", lat: 23.116907, lng: 113.251795 },
      { label: "《宏道日报》报社旧址", lat: 23.117185, lng: 113.251776 },
      { label: "民声日报社旧址", lat: 23.117625, lng: 113.251728 },
      */
      { label: "乐干楼", lat: 23.106028, lng: 113.281487 },
      { label: "岭南画派纪念馆", lat: 23.092635, lng: 113.278528 },
      { label: "马应彪夫人护养院副楼", lat: 23.096091, lng: 113.296798 },
      { label: "广州市美术有限公司画棚旧址", lat: 23.147279, lng: 113.310079 },
      { label: "暨南大学化学楼", lat: 23.130535, lng: 113.348576 },
      { label: "东郊公园湖心亭", lat: 23.126824, lng: 113.365284 },
      { label: "东郊公园双层亭", lat: 23.126824, lng: 113.365284 },
      { label: "华南农学院8号楼", lat: 23.158908, lng: 113.356424 },
      { label: "华南植物园草坪办公楼", lat: 23.183036, lng: 113.366548 },
      { label: "蒲岗桥", lat: 23.183036, lng: 113.366548 },
      { label: "棕榈休息亭", lat: 23.183036, lng: 113.366548 },
      { label: "高滩村送瘟神纪念碑", lat: 23.564752, lng: 113.781339 },
      { label: "大田村苏塘路古井", lat: 23.290103, lng: 113.624265 },
      { label: "五联村凉亭", lat: 23.36866, lng: 113.822033 },
      { label: "龙岗村古桥", lat: 23.295692, lng: 113.710031 },
      { label: "木棉村公社礼堂", lat: 23.546277, lng: 113.585226 },
      { label: "钱岗村兰集堂", lat: 23.546277, lng: 113.585226 },
      { label: "广钢铁路专用线花地河大桥", lat: 23.093203, lng: 113.224566 },
      { label: "珠江电影制片厂行政楼旧址", lat: 23.094607, lng: 113.321088 }
    ]
  },
  {
    label: "Industrial Buildings",
    visible: false,
    items: [
      { label: "诚志堂货仓旧址", lat: 23.095412, lng: 113.250524 },
      { label: "东亚烟厂旧址", lat: 23.104509, lng: 113.251771 },
      { label: "西村电厂输送桥", lat: 23.138854, lng: 113.232305 },
      { label: "天成路96、98号广彩加工场旧址", lat: 23.114381, lng: 113.255557 },
      { label: "粤汉铁路黄沙车站旧址", lat: 22.989125, lng: 113.277732 },
      { label: "华侨糖厂旧址（拱形仓库）", lat: 23.153181, lng: 113.219818 },
      { label: "广州铁路局援外仓建筑群旧址（1号仓）", lat: 23.142746, lng: 113.374574 },
      { label: "广州铁路局援外仓建筑群旧址（9号仓）", lat: 23.142746, lng: 113.374574 },
      { label: "广州铁路局援外仓建筑群旧址（办公楼）", lat: 23.142746, lng: 113.374574 },
      { label: "广州造纸厂旧址大烟囱", lat: 23.073896, lng: 113.267857 },
      { label: "广州造纸厂旧址码头高层仓", lat: 23.073896, lng: 113.267857 },
      { label: "广州造纸厂旧址水塘及驳岸", lat: 23.073896, lng: 113.267857 },
      { label: "广州造纸厂旧址新浊水泵房", lat: 23.073896, lng: 113.267857 },
      { label: "广州造纸厂旧址1号煤仓", lat: 23.073896, lng: 113.267857 },
      { label: "广州造纸厂旧址2号煤仓", lat: 23.073896, lng: 113.267857 },
      { label: "广东省石油公司昌岗路油库", lat: 23.080911, lng: 113.258283 },
      { label: "第一棉纺厂旧址1号车间", lat: 23.081381, lng: 113.26426 },
      { label: "录顺船坞", lat: 23.259036, lng: 113.532165 },
      { label: "张安昌中药厂旧址", lat: 23.112236, lng: 113.251461 },
      { label: "广州市第二棉纺厂旧址（部分车间）", lat: 23.118862, lng: 113.354943 },
      { label: "广州啤酒厂麦仓旧址", lat: 23.145427, lng: 113.236568 },
      { label: "广东罐头厂冷库旧址", lat: 23.110456, lng: 113.370737 },
      { label: "广东罐头厂包装仓库及站台旧址", lat: 23.110456, lng: 113.370737 },
      { label: "增城糖纸厂蒸煮车间旧址", lat: 23.299662, lng: 113.843509 },
      { label: "大干围仓库旧址", lat: 23.061392, lng: 113.316089 },
      { label: "城安围船厂旧址（第13号、14号、15号、16号车间、下水滑道）", lat: 23.054588, lng: 113.299097 },
      { label: "广州纺织机械厂旧址（装配车间、木模车间、布配和机械车间、机装车间、铆杆开料车间、退火炉）", lat: 23.098818, lng: 113.324615 },
      { label: "广摩集团五羊钢管厂旧址（4号车间）", lat: 23.28153, lng: 113.244476 },
      { label: "广州纤维板厂旧址（水塔、纤维板车间、锅炉房、起木码头）", lat: 23.244831, lng: 113.218168 },
      { label: "广东省粮油储运公司第二仓库（10、16、18、22、26号仓库）", lat: 23.039813, lng: 113.417109 },
      { label: "黄埔老港（钢板桩码头、6号仓）", lat: 23.093402, lng: 113.450125 },
      { label: "文冲船厂（1号船坞、2号船坞）", lat: 23.090354, lng: 113.473726 },
      { label: "大濠洲西后导标塔", lat: 23.092354, lng: 113.459679 },
      { label: "鱼珠船厂旧址（港池船排、候工房）", lat: 23.09605, lng: 113.433396 }
    ]
  },
  {
    label: "GX Buildings",
    visible: false,
    items: [
      { label: "下仓街18号集合住宅", lat: 21.65, lng: 109.21 },
      { label: "下街7号民居", lat: 21.675592, lng: 109.18929 },
      { label: "合浦体育馆旧址构筑物", lat: 21.672901, lng: 109.196311 },
      { label: "合浦工艺厂旧址（厂房建筑）", lat: 21.67176, lng: 109.193703 },
      { label: "合浦菓菜副食品公司旧址", lat: 21.672955, lng: 109.199035 },
      { label: "合浦露天电影院旧址构筑物", lat: 21.673398, lng: 109.196325 },
      { label: "奎文路85号骑楼", lat: 21.66971, lng: 109.199789 },
      { label: "娄行街17、19号骑楼", lat: 21.66, lng: 109.2 },
      { label: "娄行街42号骑楼", lat: 21.674845, lng: 109.194953 },
      { label: "娄行街44号骑楼", lat: 21.675103, lng: 109.194978 },
      { label: "小洋房", lat: 21.673821, lng: 109.186554 },
      { label: "小礼堂", lat: 21.675742, lng: 109.194923 },
      { label: "康乐街81号民居", lat: 21.668157, lng: 109.187702 },
      { label: "惠爱西路110号", lat: 21.675785, lng: 109.186104 },
      { label: "玑屯街88号民居", lat: 21.666826, lng: 109.18738 },
      { label: "蒌行街16号民居", lat: 21.677072, lng: 109.190492 },
      { label: "蒌行街1号民居", lat: 21.677029, lng: 109.190256 },
      { label: "蒌行街41号民居", lat: 21.677877, lng: 109.19062 },
      { label: "蒌行街50号民居", lat: 21.677823, lng: 109.190781 },
      { label: "蒌行街5号民居", lat: 21.676976, lng: 109.190277 },
      { label: "蒌行街7号民居", lat: 21.676986, lng: 109.190266 },
      { label: "西华路46号民居", lat: 21.671289, lng: 109.188947 },
      { label: "西华路50号民居", lat: 21.671558, lng: 109.188968 },
      { label: "西华路77号", lat: 21.67, lng: 109.19 },
      { label: "钦州巷45号民居", lat: 21.676933, lng: 109.187413 },
      { label: "钦州汽车站职工宿舍旧址", lat: 21.670212, lng: 109.199029 },
      { label: "青云路16号骑楼", lat: 21.669878, lng: 109.195949 },
      { label: "万和祥", lat: 21.484285443192004, lng: 109.10496839805 },
      { label: "东一巷16号、18号", lat: 21.485605090027, lng: 109.11587962433 },
      { label: "东一药局", lat: 21.485315411452998, lng: 109.11585816667001 },
      { label: "中山东路183号", lat: 21.486345379714997, lng: 109.116555541 },
      { label: "中山东路220号", lat: 21.486463396912, lng: 109.11643752381 },
      { label: "中山东路242号", lat: 21.486720888978002, lng: 109.11731728835 },
      { label: "中山东路302号", lat: 21.487064211731, lng: 109.11837944311999 },
      { label: "中山东路382号", lat: 21.48771867073, lng: 109.12024626061 },
      { label: "中山东路47号", lat: 21.484328358536, lng: 109.10961398407001 },
      { label: "中山东路62、64、66、68、70号", lat: 21.484639494781998, lng: 109.10990366265 },
      { label: "中山中路55号", lat: 21.484242527848004, lng: 109.10944232268999 },
      { label: "中山中路75号", lat: 21.484049408797, lng: 109.10898098275001 },
      { label: "中山西路2号、4号", lat: 21.484167425995, lng: 109.10846599861 },
      { label: "中山路邮电局", lat: 21.48491844452, lng: 109.11130914017 },
      { label: "人民剧场", lat: 21.483652441865, lng: 109.11408790871 },
      { label: "介堂家庭图书馆", lat: 21.484403460388997, lng: 109.10636314674 },
      { label: "信和号", lat: 21.484263985519, lng: 109.10494694038 },
      { label: "公益财记", lat: 21.485905497436004, lng: 109.11110529228 },
      { label: "共产党万岁", lat: 21.480883, lng: 109.108856 },
      { label: "力生行", lat: 21.485487072829, lng: 109.10960325523999 },
      { label: "北部湾广场“南珠魂”雕塑", lat: 21.474554388886, lng: 109.10847672745 },
      { label: "合泰号", lat: 21.486034243469, lng: 109.11253222747 },
      { label: "合泰栈", lat: 21.486066429977, lng: 109.11254295632 },
      { label: "吴恒利", lat: 21.486334650878, lng: 109.11361583992 },
      { label: "基督教礼拜堂", lat: 21.484500019913, lng: 109.10673865600998 },
      { label: "天泰祥", lat: 21.485851853256996, lng: 109.11100873274997 },
      { label: "太和医局", lat: 21.487021296387, lng: 109.11584743782001 },
      { label: "安吉", lat: 21.4858947686, lng: 109.11109456343999 },
      { label: "宜仙楼旧址", lat: 21.48410305298, lng: 109.10659918114001 },
      { label: "宝华金铺", lat: 21.485615818861998, lng: 109.11076196953 },
      { label: "广成栏", lat: 21.484392731553996, lng: 109.10522589011998 },
      { label: "广珍祥", lat: 21.485776751404, lng: 109.11059030816 },
      { label: "广生祥", lat: 21.485476343994, lng: 109.10952815336 },
      { label: "德盛昌", lat: 21.483985035783, lng: 109.10493621154 },
      { label: "恒丰", lat: 21.486077158814, lng: 109.11270388885 },
      { label: "曾亮记", lat: 21.486227362517, lng: 109.11327251716 },
      { label: "梅园", lat: 21.486399023896, lng: 109.11605128570001 },
      { label: "民生路19号", lat: 21.484296172028, lng: 109.10864838883 },
      { label: "民生路9号", lat: 21.484478562240998, lng: 109.10856255812999 },
      { label: "永丰隆", lat: 21.485969870453996, lng: 109.11225327773 },
      { label: "永济隆", lat: 21.486109345321996, lng: 109.11207088753 },
      { label: "沙脊街房产界碑", lat: 21.48442491806, lng: 109.107393115 },
      { label: "源昌", lat: 21.48649558342, lng: 109.11350855156 },
      { label: "珠海楼", lat: 21.484961359864, lng: 109.10855182931 },
      { label: "瑞泰", lat: 21.486463396911002, lng: 109.11344417855001 },
      { label: "生兴庄", lat: 21.486506312256, lng: 109.1135514669 },
      { label: "电报局旧址", lat: 21.484017222288998, lng: 109.10653480813 },
      { label: "百货大楼", lat: 21.485229580764003, lng: 109.11246785447001 },
      { label: "皇都大厦", lat: 21.473138182525, lng: 109.10100945755 },
      { label: "祥和栈", lat: 21.486452668074996, lng: 109.11433467194 },
      { label: "荣昌泰", lat: 21.485626547699, lng: 109.11002167983997 },
      { label: "荣昌隆", lat: 21.484156697158, lng: 109.10696396157 },
      { label: "裕源记", lat: 21.486527769927996, lng: 109.11353000921999 },
      { label: "裕盛", lat: 21.487042754058, lng: 109.11577233596 },
      { label: "许永安", lat: 21.48649558342, lng: 109.11453851982 },
      { label: "金记栈", lat: 21.486259549026, lng: 109.11318668647 },
      { label: "陈永新", lat: 21.484221070175998, lng: 109.10477527900998 },
      { label: "陈海记", lat: 21.484628765946, lng: 109.1062022142 },
      { label: "陈英记", lat: 21.486270277863, lng: 109.11339053437001 },
      { label: "海泰别墅群", lat: 21.417262404327992, lng: 109.13467654511 },
      { label: "海滩公园“潮”雕塑11", lat: 21.413642179628, lng: 109.13306990073002 },
      { label: "银滩夜总会", lat: 21.414049875397996, lng: 109.13139620230001 },
      { label: "会师亭", lat: 23.699714, lng: 108.596602 },
      { label: "卢於春社斗牛场", lat: 23.676017, lng: 108.739932 },
      { label: "张鹏展故居", lat: 23.25, lng: 108.66 },
      { label: "拉厂石拱桥", lat: 23.561694, lng: 108.614277 },
      { label: "木山卢於春社卢於寺", lat: 23.68, lng: 108.73 },
      { label: "樊氏宗堂", lat: 23.23, lng: 108.67 },
      { label: "洋渡渡槽", lat: 23.46, lng: 108.71 },
      { label: "苏桥福赐寺", lat: 23.250918, lng: 108.68097 },
      { label: "西燕镇东敢水库蓄水坝", lat: 23.58, lng: 108.59 },
      { label: "黄宪义故居", lat: 23.528793888000052, lng: 108.72250089100004 },
      { label: "“三街两巷”骑楼建筑群", lat: 22.816759752365, lng: 108.3161494996 },
      { label: "三孔月桥", lat: 22.82793, lng: 108.3248 },
   
      { label: "人民公园白龙茶厅", lat: 22.82455, lng: 108.325814 },
      { label: "兴宁路中段骑楼建筑群", lat: 22.81717, lng: 108.31677 },
      { label: "兴宁路北段骑楼建筑群", lat: 22.81827, lng: 108.31621 },
      { label: "兴宁路南段骑楼建筑群", lat: 22.81606, lng: 108.31714 },
      { label: "创新村粮仓", lat: 22.877087997529006, lng: 108.46684673089003 },
      { label: "南宁百货大楼", lat: 22.81992, lng: 108.31647 },
      { label: "同仁村粮仓", lat: 22.94466, lng: 108.42655 },
      { label: "城隍庙", lat: 22.81669, lng: 108.31645 },
      { label: "广西少儿图书馆", lat: 22.830213712786, lng: 108.32644918221997 },
      { label: "广西自然博物馆", lat: 22.830213712783998, lng: 108.32764008302 },
      { label: "新华路清真寺", lat: 22.818211507482474, lng: 108.3138053856466 },
      { label: "明园饭店一号楼", lat: 22.826211856932996, lng: 108.32507589120996 },
      { label: "毛主席接见广西各族人民纪念馆", lat: 22.834119009109997, lng: 108.32754352350001 },
      { label: "民生路中段骑楼建筑群", lat: 22.81771, lng: 108.31495 },
      { label: "民生路西段骑楼建筑群", lat: 22.81718, lng: 108.31452 },
      { label: "湖心亭", lat: 22.82767, lng: 108.32553 },
      { label: "烈士陵园群雕", lat: 22.8511, lng: 108.37887 },
      { label: "宾阳县南街东—南段历史建筑群", lat: 23.22036, lng: 108.81015 },
      { label: "宾阳县南街东—接龙桥北历史建筑群", lat: 23.22345, lng: 108.80792 },
      { label: "宾阳县南街东—接龙桥南历史建筑群", lat: 23.22628, lng: 108.80887 },
      { label: "宾阳县南街西—打铜刘巷北历史建筑群", lat: 23.22431, lng: 108.8093 },
      { label: "宾阳县南街西—打铜刘巷南历史建筑群", lat: 23.22543, lng: 108.80921 },
      { label: "宾阳县南街西—打鱼张巷北历史建筑群", lat: 23.22706, lng: 108.8105 },
      { label: "宾阳县南街西—打鱼张巷南历史建筑群", lat: 23.22774, lng: 108.80861 },
      { label: "宾阳县桂西地委", lat: 23.25212, lng: 108.81479 },
      { label: "佛子旧学校", lat: 22.895859, lng: 108.933048 },
      { label: "刘四庙", lat: 22.79, lng: 108.87 },
      { label: "南面村覃氏祖屋", lat: 22.68, lng: 109.53 },
      { label: "南面村覃氏祖祠", lat: 22.67, lng: 109.53 },
      { label: "城隍廟", lat: 22.97, lng: 109.15 },
      { label: "榃僧村建筑群", lat: 22.84, lng: 109.23 },
      { label: "横州市人民政府门楼", lat: 22.682842, lng: 109.257132 },
      { label: "横州市怀古亭", lat: 22.68, lng: 109.26 },
      { label: "青桐村关帝庙", lat: 22.84, lng: 109.24 },
      { label: "龙头闭府老宅", lat: 22.66, lng: 109.52 },
      { label: "七十二道门", lat: 23.0508, lng: 108.31333 },
      { label: "三江坡古建筑群", lat: 22.831456714659, lng: 108.09711925795 },
      { label: "二冬三角市黄氏厅邸", lat: 22.80996, lng: 108.20484 },
      { label: "二冬二房黄氏厅邸", lat: 22.81047, lng: 108.20535 },
      { label: "二冬元宪黄氏厅邸", lat: 22.80944, lng: 108.20535 },
      { label: "二冬八角门楼", lat: 22.81039, lng: 108.20432 },
      { label: "二冬坡高寨上阁黄氏厅邸及阁楼", lat: 22.81039, lng: 108.20406 },
      { label: "二冬坡高寨下阁黄氏厅邸", lat: 22.81056, lng: 108.20364 },
      { label: "二冬头房楼屋", lat: 22.81081, lng: 108.20484 },
      { label: "二冬石大门黄氏厅邸", lat: 22.81116, lng: 108.20638 },
      { label: "五冬山九房黄氏厅邸", lat: 22.81047, lng: 108.20432 },
      { label: "八冬三房花井屋", lat: 22.80721, lng: 108.21342 },
      { label: "八冬二房三代举人屋", lat: 22.80798, lng: 108.21325 },
      { label: "古思朗灵大王庙", lat: 22.70885, lng: 108.22063 },
      { label: "吴圩机场老候机楼", lat: 22.601666503937, lng: 108.18771354962001 },
      { label: "富德杨氏民居", lat: 22.82185, lng: 108.2559 },
      { label: "广西体操训练馆", lat: 22.807099284318998, lng: 108.31432575487999 },
      { label: "开村二冬北井", lat: 22.81116, lng: 108.20346 },
      { label: "扬美古建筑群", lat: 22.841069751769, lng: 108.06310884761999 },
      { label: "高桥", lat: 22.812734627380998, lng: 108.26645688811999 },
      { label: "黄奇观进士屋", lat: 22.810063415558997, lng: 108.20895664502001 },
      { label: "南晓杨氏民居", lat: 22.414780193177, lng: 108.53449003864999 },
      { label: "坛僚村大寨屋", lat: 22.62313, lng: 108.37686 },
      { label: "大塘中学老校门", lat: 22.38391333183401, lng: 108.37935106920001 },
      { label: "新兰村陈氏民居", lat: 22.669772439803, lng: 108.42169778515 },
      { label: "祠堂坡淥天庵及莫氏宗祠", lat: 22.592487, lng: 108.316808 },
      { label: "那扭水利渡槽", lat: 22.645268225327005, lng: 108.37599830429001 },
      { label: "那陈文革标语建筑", lat: 22.449917131273, lng: 108.27655809093001 },
      { label: "上团坡卢氏民居", lat: 22.965587, lng: 108.015425 },
      { label: "上团坡李氏民居", lat: 22.96543, lng: 108.015892 },
      { label: "下愣村古码头", lat: 22.828669855789, lng: 108.03300654425001 },
      { label: "下愣村敬字亭", lat: 22.829557442322997, lng: 108.03182797232 },
      { label: "下楞村古巷门楼群", lat: 22.829699824051, lng: 108.03184782993003 },
      { label: "下楞村百间骑楼古宅群", lat: 22.829042458189004, lng: 108.03369478981 },
      { label: "丘屋坡民居建筑群", lat: 22.79896, lng: 108.19395 },
      { label: "南宁手拖厂工修车间", lat: 22.866378807680007, lng: 108.31573443216001 },
      { label: "南宁肉类联合加工厂礼堂", lat: 22.85033, lng: 108.278386 },
      { label: "南宁育才学校（越南中央学舍区）实验馆", lat: 22.840597414627, lng: 108.28335480494002 },
      { label: "南宁育才学校（越南中央学舍区）礼堂", lat: 22.841362068847996, lng: 108.2844690038 },
      { label: "定内坡邓氏民居群", lat: 22.910993, lng: 107.983038 },
      { label: "定内坡马氏宅院", lat: 22.913135075228, lng: 107.98060850897997 },
      { label: "广西华侨学校教学大楼", lat: 22.8351, lng: 108.24712 },
      { label: "广西大学学生爱国民主运动纪念碑", lat: 22.846780131057997, lng: 108.2932773782 },
      { label: "广西大学红楼群", lat: 22.84462, lng: 108.28854 },
      { label: "广西大学大礼堂", lat: 22.8386, lng: 108.2914 },
      { label: "广西大学老校门", lat: 22.836652109817, lng: 108.28447973263 },
      { label: "广西大学西校园水塔", lat: 22.842681715683003, lng: 108.2843188001 },
      { label: "广西民族大学办公楼", lat: 22.841227711819002, lng: 108.23318356779998 },
      { label: "广西民族大学理学院", lat: 22.842456410125003, lng: 108.22907602323 },
      { label: "广西民族大学相思湖校区东大门", lat: 22.842628071504997, lng: 108.23480522167995 },
      { label: "广西民族大学相思湖校区旧图书馆", lat: 22.843183064118, lng: 108.23057966034 },
      { label: "广西民族大学非通用语言人才培养基地", lat: 22.84299, lng: 108.23163 },
      { label: "那学坡古民居群", lat: 22.937371515881996, lng: 107.98507170478001 },
      { label: "陈东大塘坡中部民居建筑群", lat: 22.83235, lng: 108.25334 },
      { label: "陈东大塘坡南侧民居建筑群", lat: 22.83201, lng: 108.25343 },
      { label: "陈东岭头坡中部民居建筑群", lat: 22.83269, lng: 108.25266 },
      { label: "陈东岭头坡南侧民居建筑群", lat: 22.83235, lng: 108.2536 },
      { label: "陈东村大塘坡宋氏民居", lat: 22.834106468812, lng: 108.25214462084001 },
      { label: "陈西岭头坡中部民居建筑", lat: 22.83295, lng: 108.25103 },
      { label: "陈西岭头坡北侧民居建筑群", lat: 22.83278, lng: 108.25266 },
      { label: "陈西岭头坡南侧民居建筑", lat: 22.83312, lng: 108.25051 },
      { label: "黄屋坡民居建筑群", lat: 22.80325, lng: 108.18811 },
      { label: "和平街骑楼建筑群", lat: 22.75371, lng: 108.49102 },
      { label: "孙头坡古民居群", lat: 22.680316259993994, lng: 108.73938935903999 },
      { label: "汉林街骑楼建筑群", lat: 22.75451, lng: 108.48957 },
      { label: "胜利街骑楼建筑群", lat: 22.751623, lng: 108.494267 },
      { label: "蒲庙胜利街骑楼建筑群", lat: 22.754506161345997, lng: 108.49024432805999 },
      { label: "那蒙村古民居", lat: 22.55068, lng: 108.63362 },
      { label: "长江坡古民居群", lat: 22.7803, lng: 108.505669 },
      { label: "隆安县仁慈街骑楼建筑群", lat: 23.27177, lng: 107.63247 },
      { label: "隆安县富兴街骑楼建筑群", lat: 23.27074, lng: 107.63401 },
      { label: "隆安县隆靖街骑楼建筑群", lat: 23.2704, lng: 107.62749 },
      { label: "中山路东侧骑楼建筑群", lat: 22.8138, lng: 108.31896 },
      { label: "中山路西侧骑楼建筑群", lat: 22.81386, lng: 108.31862 },
      { label: "共和路37号骑楼建筑群", lat: 22.8148, lng: 108.31896 },
      { label: "共和路北段骑楼建筑群", lat: 22.81498, lng: 108.3189 },
      { label: "共和路南段骑楼建筑群", lat: 22.81444, lng: 108.31934 },
      { label: "南湖公园九孔桥", lat: 22.808087690643, lng: 108.34512921317001 },
      { label: "广西区图书馆", lat: 22.816713674834006, lng: 108.33472224218 },
      { label: "李明瑞、韦拔群烈士纪念馆", lat: 22.806617840102003, lng: 108.34634157163 },
      { label: "民族路中段民居", lat: 22.81371, lng: 108.31864 },

      { label: "青秀山万寿观音寺", lat: 22.790824993424007, lng: 108.39038344365999 },
      { label: "青秀山龙象塔", lat: 22.783477091445, lng: 108.38610486786999 },
      { label: "高才屯壮族传统民房", lat: 23.53, lng: 108.31 },
      { label: "龙岩神庙", lat: 23.511105, lng: 107.976957 },

      { label: "劳振光宅", lat: 22.07414, lng: 106.83894 },

      { label: "向都镇炮楼", lat: 23.22996, lng: 106.963565 },

      { label: "胜龙渡槽", lat: 23.068459, lng: 107.23876 },
      { label: "苏式瓦房", lat: 23.081394, lng: 107.143433 },
      { label: "观音庙", lat: 23.081394, lng: 107.143433 },
      { label: "红楼", lat: 22.136254, lng: 107.073548 },
      { label: "红楼", lat: 22.403281, lng: 107.66267 },
      { label: "中共崇左市江州区区委办公楼", lat: 22.41116, lng: 107.34863 },
      { label: "中共崇左市江州区区委组织部办公楼", lat: 22.41108, lng: 107.34854 },
      { label: "太平大桥(崇左二桥)", lat: 22.409629, lng: 107.354145 },
      { label: "崇左县委办公及住所旧址", lat: 22.406725, lng: 107.353621 },
      { label: "崇左县汽车站旧址", lat: 22.414764, lng: 107.358023 },
      { label: "崇左县糖厂旧址烟囱", lat: 22.421573, lng: 107.359259 },
      { label: "崇左大桥(崇左一桥)", lat: 22.418163, lng: 107.365395 },
      { label: "狮环村史馆", lat: 22.351105, lng: 107.357184 },
      { label: "红旗渠", lat: 22.312775, lng: 107.365615 },
      { label: "长征渡槽", lat: 22.432901, lng: 107.365286 },
      { label: "驮卢商会楼", lat: 22.65, lng: 107.64 },
      { label: "中山公园篑山", lat: 22.34138, lng: 106.85893 },
      { label: "中山纪念堂旧址", lat: 22.34193, lng: 106.86008 },
      { label: "人民礼堂", lat: 23.729535687802997, lng: 109.22795535051 },
      { label: "兴宾区革命烈士纪念塔", lat: 23.73124157274, lng: 109.22372818910996 },
      { label: "凤凰新城革命烈士纪念塔", lat: 23.919811595323, lng: 109.28007603608 },
      { label: "古三开元寺", lat: 23.748396981597, lng: 109.22361017189002 },
      { label: "古坝", lat: 23.919210780500997, lng: 109.27979708635002 },
      { label: "康宁寺", lat: 23.712927449584004, lng: 109.21336413347998 },
      { label: "月亮井", lat: 23.68747865045299, lng: 109.26930428469998 },
      { label: "老火车站", lat: 23.733108390213, lng: 109.23686028444 },
      { label: "郑氏祠堂", lat: 23.72775470102, lng: 109.23936010324 },
      { label: "灵台石拱桥", lat: 23.792309, lng: 108.968363 },
      { label: "里兰斜井口遗址", lat: 23.79597, lng: 108.875391 },
      { label: "里兰水池", lat: 23.796942, lng: 108.87581 },
      { label: "里兰风井口遗址", lat: 23.79729, lng: 108.876212 },
      { label: "中国人民解放总队粤桂边纵队独五团刁桑之战指挥部旧址", lat: 23.773543, lng: 108.48687 },
      { label: "傅家大院", lat: 23.5922, lng: 109.652521 },
      { label: "叶家大院", lat: 23.594367, lng: 109.651759 },
      { label: "张嘉荣故居", lat: 23.591975, lng: 109.651116 },
      { label: "期尚小学教学楼（原武宣镇第一小学教学楼）", lat: 23.594968, lng: 109.652049 },
      { label: "武宣县粮所仓库（现武宣县大米厂仓库）", lat: 23.592072, lng: 109.650568 },
      { label: "武氏宗祠", lat: 23.629144, lng: 109.708733 },
      { label: "汤氏祖宅", lat: 23.594196, lng: 109.651802 },
      { label: "沈家大院", lat: 23.593488, lng: 109.650815 },
      { label: "福田月楼", lat: 23.636982, lng: 109.852496 },

      { label: "覃氏宗祠", lat: 23.59411, lng: 109.663207 },
      { label: "郭家大院", lat: 23.775194, lng: 109.646462 },
      { label: "黄家大院", lat: 23.595355, lng: 109.652006 },
      { label: "黎世禹故居", lat: 23.591964, lng: 109.652146 },
      { label: "黎家大院", lat: 23.59175, lng: 109.651802 },
      { label: "寺村镇交址村韦纯束故居", lat: 23.973745, lng: 109.872082 },
      { label: "广西剿匪第一枪旧址", lat: 24.011104, lng: 109.948697 },
      { label: "桂中（象县）农民运动旧址", lat: 23.955789, lng: 109.681806 },
      { label: "象州县大乐镇红色革命教育基地（石朋村韦章平故居）", lat: 24.075829, lng: 109.979509 },
      { label: "象州县百丈乡屯鸾反围剿旧址", lat: 23.958528, lng: 109.683985 },
      { label: "“瑶族之乡”雕像", lat: 24.145727, lng: 110.179409 },
      { label: "三江庙村中共修仁支部旧址", lat: 24.416019, lng: 110.141998 },
      { label: "八一桥", lat: 24.133174, lng: 110.184355 },
      { label: "关帝庙", lat: 25.751398, lng: 109.161173 },
      { label: "县委办公楼", lat: 25.787275, lng: 109.602203 },
      { label: "县机关事务服务中心办公楼", lat: 25.787103, lng: 109.603212 },
      { label: "三中路66号柳州市委礼堂", lat: 24.328090365173, lng: 109.41172305291 },
      { label: "中共桂柳区工委驻地旧址", lat: 24.31530159259, lng: 109.40139118379 },
      { label: "中山西路骑楼群", lat: 24.315408880950997, lng: 109.40200272743999 },
      { label: "原曙光小学教学楼", lat: 24.313992674591, lng: 109.41203418916001 },
      { label: "原柳州市印刷厂托儿所", lat: 24.313713724854, lng: 109.41186252779 },
      { label: "城中水厂取水塔及取水泵房", lat: 24.318949396849998, lng: 109.39863387292 },
      { label: "小南路后街建筑群", lat: 24.314250166656, lng: 109.40193835443002 },
      { label: "小南路民居群", lat: 24.313499148132994, lng: 109.40476003830999 },
      { label: "曙光西路民居建筑", lat: 24.315280134917, lng: 109.40146628564 },
      { label: "柳州地委礼堂", lat: 24.326112, lng: 109.411571 },
      { label: "柳州市红星影剧院", lat: 24.313252384901997, lng: 109.41030684654999 },
      { label: "柳州消防队望火楼", lat: 24.324421241774, lng: 109.40860531883999 },
      { label: "柳州电灯公司旧址", lat: 24.316020424606997, lng: 109.4039553756 },
      { label: "柳州铁桥", lat: 24.320580179930996, lng: 109.39571562952 },
      { label: "柳州饭店旧建筑群", lat: 24.324700052979, lng: 109.41313925928 },
      { label: "柳江大桥", lat: 24.309851343873, lng: 109.40575782007 },
      { label: "环江村东流屯佘家祠堂", lat: 24.42201, lng: 109.4882 },
      { label: "罗池路东一巷3号民居", lat: 24.31418579364, lng: 109.41175523941999 },
      { label: "钟宅", lat: 24.314024861099, lng: 109.41176596826 },
      { label: "原柳州城市职业学院鹧鸪江校区礼堂", lat: 24.386294439331003, lng: 109.41415212708 },
      { label: "广西林校旧建筑群", lat: 24.46899230768, lng: 109.37754533844998 },
      { label: "柳州地区农经中专（柳州市机械电子工业职业技术学校）宿舍", lat: 24.448888, lng: 109.372328 },
      { label: "柳州市农业科学研究所办公楼", lat: 24.455988958375006, lng: 109.36394117432002 },
      { label: "柳州市空气压缩机厂老厂区工业厂房", lat: 24.382732465758, lng: 109.39612768250001 },
      { label: "柳州市空气压缩机厂老宿舍", lat: 24.380500867859002, lng: 109.39887426453001 },
      { label: "柳州畜牧兽医学校老校舍", lat: 24.451010778443003, lng: 109.36960599975998 },
      { label: "柳空影剧院（柳空剧场）", lat: 24.380565240875004, lng: 109.39801595764 },
      { label: "柳钢凤凰巷老宿舍区", lat: 24.382603719726003, lng: 109.40943143921 },
      { label: "柳钢铁路运输公司建筑群", lat: 24.378569677368002, lng: 109.39535520629 },
      { label: "沙塘农场场部旧址", lat: 24.45708, lng: 109.37007 },
      { label: "石碑坪垦区城堡建筑群", lat: 24.52190692712201, lng: 109.33784864504 },
      { label: "原柳州铁路印刷厂", lat: 24.312958154587, lng: 109.39264294714002 },
      { label: "原柳州铁道职业技术学院办公大楼", lat: 24.319449100403, lng: 109.35365435689 },
      { label: "市工人疗养院旧址", lat: 24.276834163573994, lng: 109.40843579382 },
      { label: "柳南水厂取水塔及取水泵房", lat: 24.308419856934, lng: 109.40783497902 },
      { label: "柳州市新圩贮木厂旧苏式建筑", lat: 24.365282688049, lng: 109.29097649663998 },
      { label: "柳州市造漆厂旧生产区工业厂房", lat: 24.288356933501994, lng: 109.41051718803003 },
      { label: "柳铁一中原印刷厂（铁一中教室）", lat: 24.302454624083992, lng: 109.38629147621 },
      { label: "柳铁中心医院旧楼", lat: 24.312368068603, lng: 109.39350125403 },
      { label: "柳铁工人文化宫", lat: 24.308119449523, lng: 109.39411279768002 },
      { label: "东泉镇老街张庐民居", lat: 24.55495, lng: 109.488986 },
      { label: "凤山镇供销社综合楼", lat: 24.533038, lng: 109.256284 },
      { label: "成团镇岩口屯古民居", lat: 24.27258, lng: 109.25656 },
      { label: "成团镇朝阳渡槽", lat: 24.25653, lng: 109.22628 },
      { label: "成团镇金磊屯古民居", lat: 24.325502, lng: 109.415953 },
      { label: "柳江县人民文化宫", lat: 24.255709, lng: 109.329933 },
      { label: "进德镇土垢曾氏祠堂", lat: 24.220028, lng: 109.362921 },
      { label: "进德镇山前凌家古屋", lat: 24.242555, lng: 109.363646 },
      { label: "中共融县办公旧址", lat: 25.12, lng: 109.36 },
      { label: "浮石镇谏村村黎家屯民房", lat: 24.98, lng: 109.35 },
      { label: "归秀红军桥", lat: 25.313269, lng: 109.123649 },
      { label: "柳北抗战指挥部旧址", lat: 25.065934, lng: 109.256334 },
      { label: "白马抗战指挥所", lat: 24.997739, lng: 109.128383 },
      { label: "原柳州机械厂招待所", lat: 24.27607, lng: 109.43857 },
      { label: "太平西街56号民居", lat: 24.306758195677997, lng: 109.40703756579003 },
      { label: "屏山小学1号教学楼", lat: 24.305320531648004, lng: 109.40579302083002 },
      { label: "广西机电技师学院教学大楼", lat: 24.305020124237, lng: 109.41819555530002 },
      { label: "柳东水厂取水塔及取水泵房", lat: 24.315598756591, lng: 109.419654677 },
      { label: "柳州军分区羊角山干休所老建筑", lat: 24.279292375365998, lng: 109.42463285695 },
      { label: "沙塘村罗氏大院", lat: 24.471295625488995, lng: 109.37296278245005 },
      { label: "洛埠镇鸣凤街73-2号民居", lat: 24.43396, lng: 109.50934 },
      { label: "洛埠镇鸣凤街74号民居", lat: 24.4337, lng: 109.50902 },
      { label: "蟠龙山工业供水设施", lat: 24.314482957641, lng: 109.42111379870002 },
      { label: "里雍镇河表屯孙家大院", lat: 24.18676, lng: 109.58325 },
      { label: "钢军亭", lat: 24.302466661253998, lng: 109.40995580921 },
      { label: "雒容中山街民居群", lat: 24.406064302245007, lng: 109.59414846669 },
      { label: "雒容大桥", lat: 24.402716905394993, lng: 109.60736639270002 },
      { label: "雒容铁桥", lat: 24.405635148804, lng: 109.61054212818003 },
      { label: "雒容镇中山街西门桥", lat: 24.410720617095993, lng: 109.61228019962003 },
      { label: "雒容镇莫道江石拱桥", lat: 24.442284852784006, lng: 109.52007658253 },
      { label: "鸡喇碉堡群", lat: 24.279378206055, lng: 109.45029623278 },
      { label: "中渡镇中码头", lat: 24.682224, lng: 109.697618 },
      { label: "中渡镇人民公社", lat: 24.68178, lng: 109.697413 },
      { label: "中渡镇电影院", lat: 24.681301, lng: 109.696684 },
      { label: "民俗文化协会", lat: 24.69, lng: 109.69 },
      { label: "英山大桥", lat: 24.680997, lng: 109.699709 },

      { label: "伴月亭", lat: 25.27553, lng: 110.30336 },
      { label: "博望亭", lat: 25.272182, lng: 110.310787 },
      { label: "小广寒", lat: 25.274170366512, lng: 110.30547668013 },
      { label: "忆昔亭", lat: 25.272074, lng: 110.310996 },
      { label: "护碑亭", lat: 25.271152, lng: 110.314678 },
      { label: "揽月亭", lat: 25.271622, lng: 110.306813 },
      { label: "摘星亭", lat: 25.274525, lng: 110.312372 },
      { label: "文昌亭", lat: 25.272331, lng: 110.307567 },
      { label: "普陀精舍", lat: 25.276900532125996, lng: 110.3062862816 },
      { label: "月牙楼", lat: 25.274945739704002, lng: 110.30442632680999 },
      { label: "栖霞寺", lat: 25.27868731323, lng: 110.30712098229999 },
      { label: "桂林市展览馆", lat: 25.278295174915996, lng: 110.30312716915 },
      { label: "桂林航天工业学院校史馆", lat: 25.28519, lng: 110.36651 },
      { label: "桂海碑林藏碑阁", lat: 25.270957, lng: 110.305624 },
      { label: "盆景园", lat: 25.27419, lng: 110.30756 },
      { label: "碧虚阁", lat: 25.2771, lng: 110.30675 },
      { label: "穿北亭", lat: 25.253422, lng: 110.304506 },
      { label: "襟江阁", lat: 25.274420670440996, lng: 110.30525995423001 },
      { label: "廖家大院", lat: 25.176255, lng: 109.987223 },
      { label: "廖汝梅祖屋", lat: 25.176148, lng: 109.987009 },
      { label: "朱家大院", lat: 25.17618, lng: 109.986784 },
      { label: "朱氏大院", lat: 25.176292, lng: 109.987107 },
      { label: "朱远章进士府", lat: 25.176363, lng: 109.987234 },
      { label: "状元桥", lat: 25.168901, lng: 110.192926 },
      { label: "田心村66号古屋", lat: 25.17035, lng: 110.201991 },
      { label: "田心村67号古屋", lat: 25.170468, lng: 110.201938 },
      { label: "田心村71号古屋", lat: 25.170468, lng: 110.202024 },
      { label: "翰林桥", lat: 25.169363, lng: 110.192657 },
      { label: "蒋丙才祖屋", lat: 25.166123, lng: 110.163743 },
      { label: "蒋成琢进士第", lat: 25.166005, lng: 110.163754 },
      { label: "西岭村古井房", lat: 25.175977, lng: 109.987266 },
      { label: "龙元胜祖屋", lat: 25.142889, lng: 110.004829 },
      { label: "龙氏大院", lat: 25.142803, lng: 110.004969 },
      { label: "龙氏祖屋", lat: 25.142857, lng: 110.005023 },
      { label: "克铭祠堂", lat: 26.184999, lng: 111.218757 },
      { label: "公堂", lat: 25.789214, lng: 110.677619 },
      { label: "大金桥", lat: 25.834526, lng: 110.731801 },
      { label: "张姓五村公堂", lat: 25.807077, lng: 110.781225 },
      { label: "稔田村公堂", lat: 25.800876, lng: 110.751289 },
      { label: "笏公祠堂", lat: 26.18464, lng: 111.21467 },
      { label: "蒋氏宗祠", lat: 25.810747, lng: 110.991656 },
      { label: "进士及第", lat: 26.138294, lng: 111.224627 },
      { label: "风雨亭", lat: 26.159544, lng: 111.194702 },
      { label: "驸马府", lat: 25.762796, lng: 110.724726 },
      { label: "龙田村委唐氏公祠（堂）", lat: 25.405576, lng: 110.592131 },
      { label: "三一〇核地质大队医院旧址", lat: 25.651616, lng: 110.687656 },
      { label: "三一〇核地质大队厂房01", lat: 25.653891, lng: 110.686862 },
      { label: "三一〇核地质大队厂房02", lat: 25.653472, lng: 110.68669 },
      { label: "三一〇核地质大队厂房03", lat: 25.65329, lng: 110.687152 },
      { label: "三一〇核地质大队厂房04", lat: 25.654105, lng: 110.687999 },
      { label: "三一〇核地质大队厂房05", lat: 25.653558, lng: 110.68772 },
      { label: "三一〇核地质大队厂房06", lat: 25.653322, lng: 110.687645 },
      { label: "三一〇核地质大队学校旧址", lat: 25.651015, lng: 110.690167 },
      { label: "三一〇核地质大队木材厂", lat: 25.650629, lng: 110.690231 },
      { label: "三一〇核地质大队检测中心建筑01", lat: 25.653547, lng: 110.688858 },
      { label: "三一〇核地质大队检测中心建筑02", lat: 25.653279, lng: 110.688654 },
      { label: "三一〇核地质大队检测中心建筑03", lat: 25.654191, lng: 110.689394 },
      { label: "三一〇核地质大队检测中心建筑04", lat: 25.653805, lng: 110.689233 },
      { label: "三一〇核地质大队检测中心建筑05", lat: 25.653483, lng: 110.689179 },
      { label: "三一〇核地质大队检测中心建筑06", lat: 25.653397, lng: 110.689255 },
      { label: "三一〇核地质大队检测中心建筑07", lat: 25.653376, lng: 110.689222 },
      { label: "三一〇核地质大队酒楼旧址", lat: 25.652131, lng: 110.687506 },
      { label: "临源阁", lat: 25.600461, lng: 110.685789 },
      { label: "佛音寺（龙王庙）", lat: 25.601824, lng: 110.685864 },

      { label: "北街里12号民居", lat: 25.614956, lng: 110.670232 },
      { label: "北街里13号民居", lat: 25.615417, lng: 110.669803 },
      { label: "北街里15号民居", lat: 25.615342, lng: 110.669803 },
      { label: "北街里17号民居", lat: 25.615482, lng: 110.669932 },
      { label: "北街里23号民居", lat: 25.61561, lng: 110.670039 },
      { label: "北街里25号民居", lat: 25.615653, lng: 110.670125 },
      { label: "北街里41号民居", lat: 25.615761, lng: 110.670297 },
      { label: "北街里46号民居", lat: 25.615524, lng: 110.67064 },
      { label: "北街里48号民居", lat: 25.615557, lng: 110.67064 },
      { label: "北街里一巷1号民居", lat: 25.61531, lng: 110.669717 },
      { label: "南陡阁", lat: 25.602264, lng: 110.682485 },
      { label: "县委宣传部办公楼", lat: 25.615074, lng: 110.667507 },
      { label: "县委政法委办公楼", lat: 25.615739, lng: 110.667421 },
      { label: "县委组织部办公楼", lat: 25.615642, lng: 110.667067 },
      { label: "县政府大礼堂", lat: 25.616265, lng: 110.667464 },
      { label: "县政府大院离退休干部活动室", lat: 25.615803, lng: 110.6677 },
      { label: "县纪委监委办公楼", lat: 25.615964, lng: 110.667529 },
      { label: "核工业中南三一〇纸箱厂1号厂房", lat: 25.652485, lng: 110.687334 },
      { label: "核工业中南三一〇纸箱厂2号厂房", lat: 25.652131, lng: 110.687184 },
      { label: "美龄亭", lat: 25.602843, lng: 110.684019 },
      { label: "南熏亭", lat: 25.302497754830995, lng: 110.29695521238 },
      { label: "叠彩琼楼", lat: 25.292434859956998, lng: 110.29831380626001 },
      { label: "听涛阁", lat: 25.286225652538, lng: 110.29925601599 },
      { label: "拿云亭", lat: 25.273566, lng: 110.290195 },
      { label: "木龙塔", lat: 25.292112, lng: 110.301009 },
      { label: "桂湖饭店", lat: 25.289252795531002, lng: 110.29020773973001 },
      { label: "芦笛半山阁", lat: 25.312738429997005, lng: 110.27003861167998 },
      { label: "芦笛水榭", lat: 25.312188900474, lng: 110.26951288891 },
      { label: "二塘中学教学楼", lat: 24.656075, lng: 110.775715 },
      { label: "二塘中心小学大门", lat: 24.656612, lng: 110.775748 },
      { label: "县城新华书店大楼", lat: 24.631443, lng: 110.648323 },
      { label: "平乐中学老教学楼（风雨楼）1", lat: 24.622788, lng: 110.665805 },

      { label: "平乐行政专员公署治所", lat: 24.659914, lng: 110.783279 },
      { label: "张家镇人民礼堂", lat: 25.058016, lng: 110.219869 },
      { label: "沙子大礼堂", lat: 24.632347, lng: 110.642596 },
      { label: "金字阁", lat: 24.638749, lng: 110.629418 },
      { label: "长滩关帝庙", lat: 24.627216, lng: 110.648728 },
      { label: "青龙乡人民礼堂", lat: 24.508396, lng: 110.845269 },
      { label: "马河体育馆", lat: 24.63728, lng: 110.645207 },
      { label: "周家祠堂", lat: 25.22174, lng: 111.05787 },
      { label: "托圣亭", lat: 25.20984, lng: 111.04406 },
      { label: "月崖庵", lat: 25.23216, lng: 111.07937 },
      { label: "焦山古井", lat: 25.19885, lng: 111.0182 },
      { label: "白马寺", lat: 25.21822, lng: 111.06286 },
      { label: "林田干", lat: 25.010576, lng: 110.112783 },
      { label: "王先觉", lat: 25.010831, lng: 110.111323 },
      { label: "王凤英", lat: 25.009927, lng: 110.111495 },
      { label: "王崔连", lat: 25.012193, lng: 110.10906 },
      { label: "王新德、王新荣", lat: 25.00957, lng: 110.11123 },
      { label: "王树生", lat: 25.012121, lng: 110.108348 },
      { label: "王瑞成", lat: 25.010538, lng: 110.11274 },
      { label: "王老务、王先孟", lat: 25.01, lng: 110.11 },
      { label: "王荣成", lat: 25.010821, lng: 110.110326 },
      { label: "王运明", lat: 25.012296, lng: 110.108767 },
      { label: "王锦华", lat: 25.012384, lng: 110.108622 },
      { label: "一号大祠堂", lat: 25.466059, lng: 111.142644 },
      { label: "九队祠堂", lat: 25.423368, lng: 111.114781 },
      { label: "传统民居", lat: 25.244658, lng: 110.850573 },
      { label: "传统民居（唐启昌）", lat: 25.243006, lng: 110.850616 },
      { label: "传统民居（唐昌林兄弟）", lat: 25.244444, lng: 110.85068 },
      { label: "传统民居（孔令荣、赵小兵宅）", lat: 25.512793, lng: 111.215182 },
      { label: "传统民居（孔友生、孔祥文宅）", lat: 25.513931, lng: 111.214892 },
      { label: "传统民居（孔吉祥、孔祥明宅）", lat: 25.513845, lng: 111.213894 },
      { label: "传统民居（孔庆松宅）", lat: 25.514059, lng: 111.214903 },
      { label: "传统民居（孔庆松，王美英，孔志平、孔小秋，陈光姣，孔银发宅）", lat: 25.514338, lng: 111.21486 },
      { label: "传统民居（孔庆松，陈光姣，孔志平，孔银发宅）", lat: 25.514145, lng: 111.214345 },
      { label: "传统民居（孔祥友，孔友生，伍珍姣宅）", lat: 25.514231, lng: 111.213336 },
      { label: "传统民居（孔祥顺宅）", lat: 25.513866, lng: 111.213744 },
      { label: "传统民居（易祖嫒，孔祥顺，孔冬祥宅）", lat: 25.5126, lng: 111.215096 },
      { label: "传统民居（桂蕊长荣）", lat: 25.440309, lng: 111.097937 },
      { label: "传统民居（王元密，廖胜方宅）", lat: 25.423808, lng: 111.115983 },
      { label: "传统民居（王品贤，王发基宅）", lat: 25.422564, lng: 111.114181 },
      { label: "传统民居（王小强，王志豪宅）", lat: 25.423551, lng: 111.114674 },
      { label: "传统民居（王晓彬，王进民宅）", lat: 25.420504, lng: 111.114545 },
      { label: "传统民居（王熙友，王宇能宅）", lat: 25.424216, lng: 111.115683 },
      { label: "传统民居（王熙雄宅）", lat: 25.422499, lng: 111.115178 },
      { label: "传统民居（王葵云、王继觉宅）", lat: 25.421191, lng: 111.114352 },
      { label: "刘友安故居", lat: 25.259046, lng: 110.906674 },
      { label: "卿氏宗祠", lat: 25.470297, lng: 111.135102 },
      { label: "古民居", lat: 25.243736, lng: 110.84862 },
      { label: "古民居(村史馆)", lat: 25.417028, lng: 111.11093 },
      { label: "唐世道民居", lat: 25.243864, lng: 110.849672 },
      { label: "唐文茂故居", lat: 25.24513, lng: 110.849371 },
      { label: "富水片凉亭", lat: 25.678373, lng: 111.166829 },
      { label: "德里新祠堂", lat: 25.61579, lng: 111.255157 },
      { label: "戴家三兄弟旧居", lat: 25.435868, lng: 111.109717 },
      { label: "戴昌新民居", lat: 25.436125, lng: 111.109396 },
      { label: "昭仪村唐氏宗祠", lat: 25.714058, lng: 111.18377 },
      { label: "月亮门楼", lat: 25.513609, lng: 111.215246 },
      { label: "桂剧院(绍夫公祠)", lat: 25.660368, lng: 111.205075 },
      { label: "水竹居", lat: 25.24453, lng: 110.849103 },
      { label: "炮楼", lat: 25.251246, lng: 110.863212 },
      { label: "王葆心宅（三博士宅）", lat: 25.422907, lng: 111.115575 },
      { label: "田湾屯石拱桥", lat: 25.678438, lng: 111.166743 },
      { label: "石笔", lat: 25.633509, lng: 111.208926 },
      { label: "秉禄公祠堂", lat: 25.422489, lng: 111.115178 },
      { label: "老屋堂屋（世系）", lat: 25.394497, lng: 111.103495 },
      { label: "良田公祠", lat: 25.633165, lng: 111.208754 },
      { label: "蒋德宽故居", lat: 25.340123, lng: 111.050838 },
      { label: "蒋柄大院", lat: 25.703577, lng: 111.17731 },
      { label: "谢氏彧之公祠", lat: 25.420933, lng: 111.130381 },
      { label: "邓氏宗祠", lat: 25.387295, lng: 111.075535 },
      { label: "陆氏大房祠堂", lat: 25.671636, lng: 111.183867 },
      { label: "龙川公凉亭", lat: 25.679489, lng: 111.179446 },
      { label: "中兴井", lat: 25.462451, lng: 110.385333 },
      { label: "义井", lat: 25.414667, lng: 110.327566 },
      { label: "全氏宗祠", lat: 25.435077, lng: 110.397319 },
      { label: "凤凰桥", lat: 24.848679, lng: 110.393203 },
      { label: "南寺井", lat: 25.463577, lng: 110.387688 },
      { label: "宅里井", lat: 25.505607, lng: 110.314757 },
      { label: "张家井", lat: 25.463457, lng: 110.389761 },
      { label: "涌胜泉井", lat: 25.466426, lng: 110.391607 },
      { label: "郭家井", lat: 25.459573, lng: 110.396671 },
      { label: "铺背井", lat: 25.398238, lng: 110.321522 },
      { label: "陆家井", lat: 25.463818, lng: 110.388538 },
      { label: "陈家大院", lat: 25.461975, lng: 110.3858 },
      { label: "双依水榭", lat: 25.284436877473, lng: 110.27647298714 },
      { label: "古榕桥", lat: 25.275901, lng: 110.290484 },
      { label: "基督教教堂", lat: 25.286320433624, lng: 110.29261409140999 },
      { label: "日月双塔", lat: 25.274400050357, lng: 110.29039666024 },
      { label: "桂林市非物质文化遗产体验馆", lat: 25.284139474451003, lng: 110.27484038033 },
      { label: "桂林熊本友谊馆", lat: 25.283209498366997, lng: 110.27522157815001 },
      { label: "榕湖湖心岛建筑群(九曲桥&湖心岛)", lat: 25.27752, lng: 110.286635 },
      { label: "逍遥楼", lat: 25.280563555243, lng: 110.29708468358001 },
      { label: "黄庭坚系舟亭", lat: 25.278557, lng: 110.286447 },
      { label: "中共荔蒙修阳工委旧址", lat: 24.401974, lng: 110.39601 },
      { label: "中共荔蒙特支旧址", lat: 24.397514, lng: 110.399585 },
      { label: "何氏天阁宗祠", lat: 24.52058, lng: 110.3427 },
      { label: "土围", lat: 24.633225, lng: 110.295032 },
      { label: "小成村抗日旧址", lat: 24.57, lng: 110.4 },

      { label: "游记队长生活旧址", lat: 24.401276, lng: 110.396635 },
      { label: "罗家屯炮楼", lat: 24.45, lng: 110.33 },
      { label: "荔蒙游击队活动场所旧址", lat: 24.401588, lng: 110.397496 },
      { label: "蒙北支部办公旧址", lat: 24.39643, lng: 110.401721 },
      { label: "韦氏祠堂", lat: 24.63, lng: 110.3 },
      { label: "南溪山公园白龙桥", lat: 25.25243, lng: 110.28188 },
      { label: "桂林国电厂旧址", lat: 25.237542120206, lng: 110.29690026376002 },
      { label: "桂林市少年宫", lat: 25.277279646478, lng: 110.2805813928 },
      { label: "桂林美术馆", lat: 25.252197881307996, lng: 110.28652988933 },
      { label: "龙脊亭", lat: 25.248877, lng: 110.287151 },
      { label: "大光亭", lat: 24.778481, lng: 110.496593 },
      { label: "忠孝祠", lat: 24.778748, lng: 110.55653 },
      { label: "陈公馆", lat: 25.07944, lng: 110.29908 },
      { label: "东正路塘尾巷16号", lat: 23.47879, lng: 111.31235 },
      { label: "五坊路小学内梧州商会", lat: 23.47474, lng: 111.31067 },
      { label: "冰西路3号民宅", lat: 23.47756, lng: 111.31433 },
      { label: "北环路12号市政府第二招待所", lat: 23.48104, lng: 111.31073 },
      { label: "南环路11号", lat: 23.478709, lng: 111.32472 },
      { label: "合益戏院", lat: 23.47437, lng: 111.30894 },
      { label: "四坊路78号", lat: 23.47954, lng: 111.30819 },
      { label: "国华公寓（梧州第一招待所）", lat: 23.478695, lng: 111.327816 },
      { label: "大东上路138号北部", lat: 23.477521, lng: 111.326373 },
      { label: "大中路68号", lat: 23.47821, lng: 111.31017 },
      { label: "大中路70号", lat: 23.47826, lng: 111.31017 },
      { label: "大中路76号", lat: 23.47837, lng: 111.31013 },
      { label: "大中路78号", lat: 23.47841, lng: 111.31014 },
      { label: "大中路82号", lat: 23.47849, lng: 111.31016 },
      { label: "大中路83号", lat: 23.47856, lng: 111.31012 },
      { label: "大中路84号", lat: 23.47868, lng: 111.31012 },
      { label: "大中路86号", lat: 23.47872, lng: 111.31011 },
      { label: "建设路111号金龙巷口养老院", lat: 23.47972, lng: 111.31093 },
      { label: "桂北路143号", lat: 23.48245, lng: 111.30979 },
      { label: "桂北路151号民宅", lat: 23.48255, lng: 111.30961 },
      { label: "桂北路84号", lat: 23.48224, lng: 111.30923 },
      { label: "高地路42号民宅", lat: 23.47436, lng: 111.31534 },
      { label: "可程覃公祠", lat: 22.678012, lng: 110.939019 },
      { label: "恊公祠", lat: 22.88075, lng: 110.79557 },
      { label: "钟家大屋", lat: 22.918113, lng: 110.984094 },
      { label: "古能莫黎家祠", lat: 23.55143, lng: 110.98909 },
      { label: "古能陈氏民居", lat: 23.55117, lng: 110.98894 },
      { label: "名山武婆总庙", lat: 23.59263, lng: 111.00997 },
      { label: "大凹董氏民居", lat: 23.65035, lng: 111.55173 },
      { label: "大塘潘氏祠", lat: 23.76746, lng: 111.49611 },
      { label: "大岸宋氏民居", lat: 23.66608, lng: 110.99182 },
      { label: "廊坡蒙氏宗祠", lat: 23.5787, lng: 110.9903 },
      { label: "思艾旧村委楼", lat: 23.98025, lng: 111.53082 },
      { label: "李树会山亭", lat: 23.81006, lng: 111.61553 },
      { label: "林焕曦故居", lat: 23.68614, lng: 111.59817 },
      { label: "桐木倪氏民居", lat: 23.6812, lng: 111.59574 },
      { label: "永安村委旧办公楼", lat: 23.88541, lng: 111.5481 },
      { label: "达坡全氏宗祠", lat: 23.53356, lng: 110.99057 },
      { label: "高营罗氏宗祠", lat: 23.66438, lng: 111.02081 },

      { label: "何氏家祠", lat: 23.962476, lng: 110.614167 },
      { label: "刘瑞球旧居", lat: 24.007664, lng: 110.60098 },
      { label: "历史文化园清风阁", lat: 24.20432, lng: 110.516356 },
      { label: "和合亭", lat: 24.203183, lng: 110.517171 },
      { label: "滨水长廊", lat: 24.199567, lng: 110.518673 },
      { label: "福禄亭", lat: 24.194332, lng: 110.519842 },
      { label: "蒙山中学东南门", lat: 24.20505, lng: 110.518061 },
      { label: "观景木构亭", lat: 24.198516, lng: 110.517911 },
      { label: "黄天祚堂", lat: 24.115107, lng: 110.489735 },
      { label: "黄氏天地君亲师社", lat: 24.13862, lng: 110.537412 },
      { label: "黄氏家祠", lat: 24.138277, lng: 110.537359 },
      { label: "三德堂祖居", lat: 23.233235, lng: 110.819663 },
      { label: "保安殿庙", lat: 23.417299, lng: 110.748852 },
      { label: "农之政故居", lat: 23.138735, lng: 110.59101 },
      { label: "唐有仕进士宅", lat: 23.470514, lng: 110.777262 },
      { label: "水口上帝庙", lat: 23.453262, lng: 110.597619 },
      { label: "白沙邓氏祖屋（中和堂）", lat: 23.375225, lng: 110.913647 },
      { label: "蒙民伟故居", lat: 23.136074, lng: 110.586332 },
      { label: "都坡小学（旧盐站）", lat: 23.374772, lng: 110.915997 },
      { label: "陈氏廓斋祠", lat: 23.374984, lng: 110.914849 },


      { label: "兰阳泉", lat: 24.596179, lng: 107.322517 },
      { label: "纳伦石古桥", lat: 24.298733, lng: 107.289053 },
      { label: "凤山县平乐瑶族乡谋爱村社坡屯传统村落建筑群", lat: 24.424264, lng: 106.91759 },
      { label: "六寨小学老校门", lat: 25.30026, lng: 107.399041 },
      { label: "龙马庄莫氏老宅", lat: 25.285686, lng: 107.401272 },
      { label: "覃国翰将军故居及附属建筑", lat: 23.868155, lng: 107.785667 },
  
      { label: "拉好屯防御战壕", lat: 24.839801, lng: 107.19562 },
      { label: "排六屯防御战壕", lat: 24.838482, lng: 107.196338 },
      { label: "王氏古堡", lat: 25.423697, lng: 107.00209 },
 
      { label: "碗厂屯防御战壕", lat: 24.837847, lng: 107.196432 },
      { label: "纳么屯防御战壕", lat: 24.999108, lng: 107.173802 },
      { label: "邵家坳碉堡", lat: 24.999108, lng: 107.173802 },
      { label: "巴根铜鼓楼", lat: 24.22023, lng: 107.53591 },
      { label: "武圣宫（原名水月宫）", lat: 24.29152, lng: 107.09246 },
      { label: "班表古建筑", lat: 23.95921, lng: 107.31609 },
      { label: "盘中滩渡槽", lat: 24.18421, lng: 107.23782 },
      { label: "“盛世祥傩”雕塑", lat: 24.825664, lng: 108.258028 },
      { label: "东岩圣母宫", lat: 24.89543, lng: 109.12177 },
      { label: "于成龙廉政文化展示馆", lat: 24.781082, lng: 108.872188 },
      { label: "双拱状元门", lat: 24.88337, lng: 109.04124 },
      { label: "文笔山三孔桥", lat: 24.77854, lng: 108.872939 },
      { label: "民族文化广场雕塑群（4个", lat: 24.783807, lng: 108.90328 },
      { label: "石围屯大门", lat: 24.807068, lng: 108.86648 },
      { label: "罗城公园于成龙雕塑", lat: 24.786032, lng: 108.895015 },
      { label: "自治县仫佬族博物馆", lat: 24.781544, lng: 108.873315 },
      { label: "覃家门楼", lat: 24.92152, lng: 109.11036 },
      { label: "和兴街、镇安街骑楼建筑", lat: 23.94129, lng: 108.09442 },
      { label: "下江石拱桥", lat: 24.71983, lng: 107.94546 },
      { label: "九圩渡边石拱桥", lat: 24.53971, lng: 107.78154 },
      { label: "九圩西龙寺遗址", lat: 24.53426, lng: 107.75747 },
      { label: "九坝石拱桥", lat: 24.642, lng: 107.61248 },
      { label: "九坝码头石拱桥", lat: 24.64406, lng: 107.61184 },
      { label: "侧岭凤凰寺", lat: 24.83355, lng: 107.79275 },
      { label: "保平牛洞渡槽", lat: 24.44217, lng: 107.82081 },
      { label: "加辽抽水站洪石渡槽", lat: 24.71296, lng: 108.0315 },
      { label: "塘街石拱桥", lat: 24.528, lng: 107.79206 },
      { label: "干沟石拱桥", lat: 24.6216, lng: 107.6328 },
      { label: "拉岜石拱桥", lat: 24.64782, lng: 107.60204 },
      { label: "拉见泥瓦房建筑群", lat: 24.80712, lng: 107.87832 },
      { label: "水任渡桥", lat: 24.67644, lng: 107.8654 },
      { label: "江潭石拱桥", lat: 24.54355, lng: 107.79249 },
      { label: "河池镇粮所", lat: 24.69977, lng: 107.8421 },
      { label: "肯塘石拱桥", lat: 24.56542, lng: 107.71378 },
      { label: "肯研村石拱桥", lat: 24.66111, lng: 108.02342 },
      { label: "足直石拱桥", lat: 24.689703, lng: 108.037277 },
      { label: "龙作石拱桥", lat: 24.63342, lng: 107.61984 },
      { label: "龙友渡槽", lat: 24.75905, lng: 108.125 },
      { label: "兴业国立小学堂", lat: 22.738771, lng: 109.872527 },
      { label: "龙村礼堂", lat: 22.671463, lng: 109.846687 },
      { label: "八角楼", lat: 22.824098, lng: 110.43803 },
      { label: "六祖阁", lat: 22.726073, lng: 110.367978 },
      { label: "司马第", lat: 22.736593, lng: 110.237622 },
      { label: "扶阳书院", lat: 22.331593, lng: 110.68212 },
      { label: "护国寺", lat: 22.047244, lng: 109.859007 },
      { label: "无锡国专旧址", lat: 22.802018, lng: 110.333378 },
      { label: "景苏楼", lat: 22.707298, lng: 110.353214 },
      { label: "犀牛井", lat: 22.702569, lng: 110.359216 },
      { label: "登龙桥", lat: 22.710546, lng: 110.355241 },
      { label: "粤东会馆", lat: 22.706379, lng: 110.354598 },
      { label: "陈柱故居", lat: 22.799566, lng: 110.33112 },
      { label: "博白县中学老校门", lat: 22.273885, lng: 109.980187 },
      { label: "博白县民主抗日自卫军美沙纪念馆、红色学堂", lat: 21.940935, lng: 109.923074 },
      { label: "博白镇西江村留山大科屯围屋", lat: 22.292407, lng: 109.979157 },
      { label: "大排莊围屋", lat: 21.795625, lng: 109.825599 },
      { label: "刘文轩故居", lat: 22.786714, lng: 110.577146 },
      { label: "宁冲龙湾小学旧址", lat: 22.8914, lng: 110.511102 },
      { label: "吴弘建故居", lat: 22.62355, lng: 110.14343 },
      { label: "攀龙里张宅", lat: 22.62394, lng: 110.14324 },
      { label: "文四德居", lat: 22.62703, lng: 110.12862 },
      { label: "曾寿侯祠堂", lat: 22.62471, lng: 110.14619 },
      { label: "苏宗经、苏玉霖旧居", lat: 22.64544, lng: 110.13118 },
      { label: "东山水电站灌溉渠道及蓄水前池", lat: 22.286821, lng: 110.289751 },
      { label: "乌石镇龙化村官垌屯古井", lat: 22.133298, lng: 110.233433 },
      { label: "文龙水电站灌溉渠道及蓄水前池", lat: 22.333872, lng: 110.280838 },
      { label: "沙坡镇沙坡村水利灌溉渠道", lat: 22.333143, lng: 110.380909 },
      { label: "谢氏客家围屋", lat: 22.063021, lng: 110.250541 },
      { label: "黎竣修故居", lat: 22.318712, lng: 110.268248 },
      { label: "新化镇百坭村旧村部（黄文秀陈列馆）", lat: 24.71546, lng: 106.63975 },
      { label: "三星塔", lat: 24.343416, lng: 106.567297 },
      { label: "凌云体育馆", lat: 24.329833, lng: 106.570537 },
      { label: "凌云图书馆", lat: 24.343351, lng: 106.566438 },
      { label: "凌云民族历史博物馆", lat: 24.347954, lng: 106.570183 },
      { label: "太平桥", lat: 24.346913, lng: 106.565441 },
      { label: "挹翠门", lat: 24.34348, lng: 106.565602 },
      { label: "文庙", lat: 24.34789, lng: 106.566556 },
      { label: "春熙门", lat: 24.352664, lng: 106.569324 },
      { label: "武庙", lat: 24.352707, lng: 106.563241 },
      { label: "浩坤村史馆", lat: 24.196774, lng: 106.656249 },
      { label: "浩坤村棕榈洞宣誓广场", lat: 24.196366, lng: 106.657226 },
      { label: "中国工商银行百胜宿舍", lat: 23.90912, lng: 106.61971 },
      { label: "交警直属二大队", lat: 23.911972361191, lng: 106.61820511771998 },
      { label: "传统民居", lat: 23.90518, lng: 106.62278 },
      { label: "右江区电影院", lat: 23.90694, lng: 106.62191 },
      { label: "合兴利", lat: 23.90458, lng: 106.6233 },

      { label: "百色市演出管理处", lat: 23.90163, lng: 106.6184 },
      { label: "百色市糖烟酒公司", lat: 23.90379, lng: 106.62348 },
      { label: "百色建材机械厂", lat: 23.91017, lng: 106.62179 },
      { label: "福音堂", lat: 23.90466, lng: 106.62332 },

      { label: "三宝风雨桥", lat: 24.282761, lng: 106.240297 },
      { label: "尚吉门", lat: 24.293855, lng: 106.225062 },
      { label: "尚吉风雨桥", lat: 24.294037, lng: 106.225834 },
      { label: "报晓楼", lat: 24.291063, lng: 106.228215 },
      { label: "揽月坊", lat: 24.290866, lng: 106.228332 },
      { label: "武门", lat: 24.28, lng: 106.24 },
      { label: "百花寨言立坊", lat: 24.294488, lng: 106.228538 },
      { label: "老街东门", lat: 24.294252, lng: 106.228613 },
      { label: "老街南门", lat: 24.295389, lng: 106.226929 },
      { label: "观日坊", lat: 24.291013, lng: 106.228005 },
      { label: "那坡县人民大会堂", lat: 23.387877, lng: 105.83316 },
      { label: "那坡县地方税务局", lat: 23.40237, lng: 105.833896 },
      { label: "那坡县宣传文化楼", lat: 23.388672, lng: 105.83227 },
      { label: "那坡县政府办公楼", lat: 23.387406, lng: 105.832356 },
      { label: "那坡县民族博物馆", lat: 23.410686, lng: 105.843218 },
      { label: "那坡县白马森林连心桥", lat: 23.879025, lng: 106.625366 },
      { label: "那坡县白马风雨桥", lat: 23.391312, lng: 105.832987 },
      { label: "那坡县税务局", lat: 23.396916, lng: 105.833064 },
      { label: "那坡县规硬风雨桥", lat: 23.39209, lng: 105.833563 },
      { label: "那坡高中风雨桥", lat: 23.405455, lng: 105.839642 },
      { label: "后龙山公园东大门", lat: 24.777076, lng: 105.347387 },
      { label: "后龙山公园五指书天亭", lat: 24.777162, lng: 105.347387 },
      { label: "后龙山公园西大门", lat: 24.777162, lng: 105.34713 },
      { label: "天生桥换流站", lat: 24.918615, lng: 105.098688 },
      { label: "张家寨大门", lat: 24.777162, lng: 105.347387 },
      { label: "隆林各族自治县头塘桥", lat: 24.774007, lng: 105.348267 },
      { label: "隆林各族自治县民族博物馆", lat: 24.779147, lng: 105.339723 },
      { label: "隆林各族自治县西河桥", lat: 24.770896, lng: 105.34404 },
      { label: "隆林各族自治县铜鼓桥", lat: 24.773857, lng: 105.348332 },
      { label: "靖西市文化馆群楼", lat: 23.130927, lng: 106.416387 },
      { label: "靖西市新靖镇七元桥", lat: 23.130971, lng: 106.424958 },
      { label: "靖西市新靖镇五元桥", lat: 23.147174, lng: 106.41673 },
      { label: "74号骑楼", lat: 23.38638611111111, lng: 110.51474166666667 },
      { label: "伯常马公祠", lat: 23.064866666666667, lng: 110.38951944444445 },
      { label: "吕氏大屋", lat: 23.915069444444445, lng: 110.32802777777778 },
      { label: "吴氏祖祠", lat: 23.625705555555555, lng: 110.25703055555556 },
      { label: "地主楼", lat: 23.386380555555554, lng: 110.51592222222222 },
      { label: "张氏祠堂", lat: 23.329355555555555, lng: 110.34185833333333 },
      { label: "植槐堂", lat: 23.15199722222222, lng: 110.43818055555556 },
      { label: "正街骑楼", lat: 23.465680555555554, lng: 110.52311388888889 },
      { label: "永安消防所", lat: 23.38889, lng: 110.51064 },
      { label: "江夏堂", lat: 23.657611111111112, lng: 110.2778888888889 },
      { label: "瑞书楼", lat: 23.423025, lng: 110.53453611111111 },
      { label: "福音堂", lat: 23.386186111111112, lng: 110.51475833333333 },
      { label: "積善堂", lat: 23.151994444444444, lng: 110.43822222222222 },
      { label: "经余堂", lat: 23.732858333333333, lng: 110.18841944444445 },
      { label: "荣積梁公祠", lat: 23.11868888888889, lng: 110.41174444444445 },
      { label: "谢氏民居", lat: 23.334913888888888, lng: 110.37095 },
      { label: "都閫府", lat: 23.33458611111111, lng: 110.37098055555556 },
      { label: "陈氏大屋", lat: 23.730555555555554, lng: 110.29090277777777 },
      { label: "候氏三民居", lat: 23.35514722222222, lng: 109.97115 },
      { label: "克昌祠", lat: 22.915622222222222, lng: 110.12638888888888 },
      { label: "城中街骑楼", lat: 23.39292222222222, lng: 110.08243888888889 },
      { label: "大夫第（兰芝庄）", lat: 22.918116666666666, lng: 110.12208333333334 },
      { label: "姚氏土楼", lat: 23.004827777777777, lng: 110.21980555555555 },
      { label: "封君祠", lat: 23.138158333333333, lng: 110.146525 },
      { label: "明府第", lat: 22.917575, lng: 110.12273055555555 },
      { label: "松柏庄", lat: 22.915622222222222, lng: 110.12638888888888 },
      { label: "桂平市政协办公楼", lat: 23.39443888888889, lng: 110.07796944444445 },
      { label: "人民电影院", lat: 23.088197222222224, lng: 109.60996944444445 },
      { label: "天主教堂", lat: 23.08786388888889, lng: 109.61019722222223 },
      { label: "贵糖影剧院", lat: 23.074944444444444, lng: 110.58624722222223 },
      { label: "贵糖苏式办公楼", lat: 23.072655555555556, lng: 109.58618333333334 },
      { label: "生砖屋", lat: 23.138158333333333, lng: 110.146525 },
      { label: "“全福店”旧址", lat: 24.329856, lng: 111.665667 },
      { label: "“合益”店", lat: 24.414676, lng: 111.530688 },
      { label: "“合益庄”店旧址", lat: 24.41292, lng: 111.53646 },
      { label: "“同泰店”旧址", lat: 24.33167, lng: 111.66281 },
      { label: "“和昌”店", lat: 24.413141, lng: 111.538456 },
      { label: "“广华隆”当铺", lat: 24.332761, lng: 111.6604 },
      { label: "“成昌”店旧址", lat: 24.33171, lng: 111.6629 },
      { label: "“成芝堂”药材店旧址", lat: 24.33175, lng: 111.66302 },
      { label: "“普安”药店旧址", lat: 24.33177, lng: 111.66292 },
      { label: "“梁记”染布店", lat: 24.412262, lng: 111.530849 },
      { label: "“生记”饮食店旧址", lat: 24.33172, lng: 111.66294 },
      { label: "“甫生堂”药店旧址", lat: 24.33175, lng: 111.663 },
      { label: "“百灵堂”药店旧址", lat: 24.41283, lng: 111.5364 },
      { label: "“祥盛店”旧址", lat: 24.41283, lng: 111.53661 },
      { label: "“绵昌”布店旧址", lat: 24.41286, lng: 111.5366 },
      { label: "“耀利店”旧址", lat: 24.41288, lng: 111.5365 },
      { label: "“裕兴店”旧址", lat: 24.329896, lng: 111.665527 },
      { label: "“贤就”店旧址", lat: 24.334484, lng: 111.664803 },
      { label: "“赞玉堂”药店旧址", lat: 24.33171, lng: 111.66289 },
      { label: "“锦记”店旧址", lat: 24.41294, lng: 111.53663 },
      { label: "“黄记”布匹店旧址", lat: 24.33166, lng: 111.66286 },
      { label: "中苏友好协会旧址", lat: 24.41288, lng: 111.53686 },
      { label: "供销社", lat: 24.33291, lng: 111.66027 },
      { label: "天一烟庄", lat: 24.41314, lng: 111.53905 },
      { label: "平乐师专旧址", lat: 24.41289, lng: 111.53621 },
      { label: "建成米店", lat: 24.41305, lng: 111.53821 },
      { label: "德昌店旧址", lat: 24.41288, lng: 111.53632 },
      { label: "旧居民住址", lat: 24.41283, lng: 111.5366 },
      { label: "李少枚旧居", lat: 24.334293, lng: 111.664701 },
      { label: "民国广东省银行八步办事处旧址", lat: 24.410392, lng: 111.544501 },
      { label: "河东街138号", lat: 24.33203, lng: 111.66177 },
      { label: "河东街177号", lat: 24.33301, lng: 111.66019 },
      { label: "河东街37号", lat: 24.33295, lng: 111.65996 },
      { label: "河边巷47号", lat: 24.41245, lng: 111.53673 },
      { label: "烟草公司", lat: 24.41301, lng: 111.53743 },
      { label: "老工商局银行", lat: 24.41286, lng: 111.53648 },
      { label: "苏明宗故居旧址", lat: 24.41283, lng: 111.53658 },
      { label: "大围神亭", lat: 24.876777, lng: 111.247364 },
      { label: "川岩黄家大屋", lat: 24.969484, lng: 111.219634 },
      { label: "濂溪祠", lat: 24.937194, lng: 111.25225 },
      { label: "留家湾杨家大屋", lat: 24.814444, lng: 111.277389 },
      { label: "福溪周家门楼", lat: 25.069421, lng: 111.224805 },
      { label: "胡氏明家石城围屋", lat: 24.800317, lng: 111.375418 },
      { label: "陈建伟民居", lat: 24.758914, lng: 111.37098 },
      { label: "上房门楼", lat: 24.961569, lng: 111.290852 },
      { label: "东门楼", lat: 24.957724, lng: 111.28505 },
      { label: "八字门楼", lat: 24.96266, lng: 111.289816 },
      { label: "商业巷门楼", lat: 24.956989, lng: 111.282746 },
      { label: "大夫第门楼", lat: 24.959351, lng: 111.289093 },
      { label: "孚在道门楼", lat: 24.962484, lng: 111.282574 },
      { label: "恕堂书屋", lat: 24.960605, lng: 111.28608 },
      { label: "汲古书屋", lat: 24.959613, lng: 111.285549 },
      { label: "玑公祠", lat: 24.960678, lng: 111.285034 },
      { label: "福溪周敦颐讲学堂", lat: 25.07035, lng: 111.224819 },
      { label: "红星戏台", lat: 24.958905, lng: 111.28342 },
      { label: "西门楼", lat: 24.958417, lng: 111.287999 },
      { label: "读书亭", lat: 24.96045, lng: 111.285594 },
      { label: "青山门楼", lat: 24.958881, lng: 111.284782 },
      { label: "驿站（三通门楼）", lat: 24.960447, lng: 111.287089 },
      { label: "何氏门楼旧址", lat: 24.518552, lng: 111.470521 },
      { label: "平桂矿务局西湾电厂幼儿园（旧址）", lat: 24.46337, lng: 111.49156 },
      { label: "歌舞厅", lat: 24.46332, lng: 111.49086 },
      { label: "电厂二号厂房", lat: 24.411805, lng: 111.552096 },
      { label: "西湾电厂1号厂房旧址", lat: 24.46474, lng: 111.48998 },
      { label: "西湾电厂原中心控制室旧址", lat: 24.46772, lng: 111.4891 },
      { label: "西湾电厂大礼堂", lat: 24.4635, lng: 111.49073 },
      { label: "观音岩山洞电厂遗址", lat: 24.46719, lng: 111.4886 },
      { label: "鹅塘凤田村黎氏16组祖屋", lat: 24.3686, lng: 111.54248 },
      { label: "黄田英石村土城脚朱家“仁义门”门楼", lat: 24.36867, lng: 111.54243 },
      { label: "黄田英石村土城脚朱家“积善家”门楼", lat: 24.44026, lng: 111.51826 },
      { label: "伏龙黄氏宗祠", lat: 24.255247, lng: 110.669122 },
      { label: "廷宣贝公祠", lat: 24.15564, lng: 111.217223 },
      { label: "护龙庙", lat: 24.288817, lng: 111.184436 },
      { label: "春甫村学校旧址", lat: 24.290223, lng: 111.185584 },
      { label: "李氏老屋", lat: 24.020748, lng: 110.95105 },
      { label: "金德庄商号旧址", lat: 24.249968, lng: 111.195658 },
      { label: "镬耳楼", lat: 24.205422, lng: 110.841283 },
      { label: "马圣宫", lat: 24.154824, lng: 110.780662 },
      { label: "马威龚家老屋", lat: 24.270308, lng: 110.680644 },
      { label: "黄姚街委卫生室旧址", lat: 24.250021, lng: 111.196281 },
      { label: "凤凰宫", lat: 24.519132, lng: 111.139853 },
      { label: "土地庙", lat: 24.662673, lng: 111.2209 },

      { label: "石合面", lat: 24.600561, lng: 111.193018 },
      { label: "石岩庙", lat: 24.37898, lng: 111.395108 },
      { label: "石龙庙", lat: 24.416047, lng: 111.319664 },
      { label: "老戏台", lat: 24.375619, lng: 111.361912 },
      { label: "莲花庙", lat: 24.366579, lng: 111.369742 },
      { label: "陇西堂", lat: 24.516556, lng: 111.140218 },
      { label: "陶氏宗祠", lat: 24.601377, lng: 111.187653 },
      { label: "中间坡马氏古宅", lat: 22.171959, lng: 109.284237 },
      { label: "佛子山白屋祖公厅", lat: 22.230442, lng: 109.347483 },
      { label: "大面塘祖公厅", lat: 22.271651, lng: 109.556953 },
      { label: "清朝光绪时期光裕塘四合院", lat: 22.19509, lng: 109.308999 },
      { label: "社根村张氏四合院", lat: 22.237608, lng: 109.380217 },
      { label: "罗十公忠义祠", lat: 22.210733, lng: 109.314889 },
      { label: "覃汉公故居", lat: 22.644274, lng: 109.544701 },
      { label: "郭氏院落", lat: 22.485048, lng: 109.681633 },
      { label: "陆氏院落", lat: 22.60506, lng: 109.583571 },
      { label: "雁鹅坪刘氏祠堂", lat: 22.281811, lng: 109.356624 },
      { label: "东岸私塾", lat: 22.31, lng: 109.2 },
      { label: "中共大塘支部旧址", lat: 22.400523, lng: 109.206088 },
      { label: "乃孚姚公祠", lat: 22.375279, lng: 109.302765 },
      { label: "儒林第", lat: 22.307854, lng: 109.194479 },
      { label: "六娘庙", lat: 22.38, lng: 109.3 },
      { label: "外翰第", lat: 22.307325, lng: 109.19481 },
      { label: "大观书屋", lat: 22.606105, lng: 109.487424 },
      { label: "平历炮楼", lat: 22.60524, lng: 109.486918 },
      { label: "张高村烈光楼", lat: 22.35, lng: 108.94 },
      { label: "德庆社", lat: 22.61, lng: 109.49 },
      { label: "思魁府", lat: 22.30737, lng: 109.194011 },
      { label: "恰恰堂", lat: 22.55, lng: 109.43 },
      { label: "水井园", lat: 22.307983, lng: 109.19409 },
      { label: "福如堂", lat: 22.554796, lng: 109.427821 },
      { label: "陆屋镇高州会馆", lat: 22.3, lng: 108.87 },
      { label: "古城墙遗址", lat: 21.95741, lng: 108.62108 },
      { label: "民居", lat: 21.95208, lng: 108.61918 },
      { label: "第一旅社", lat: 21.95036, lng: 108.61856 },
      { label: "许子平公馆", lat: 21.94483, lng: 108.61639 },
      { label: "钦州汽车站", lat: 21.95536, lng: 108.61784 },
      { label: "陈书涟旧居", lat: 21.95484, lng: 108.61873 },
      { label: "黄文澜旧居", lat: 21.94929, lng: 108.61881 },
      { label: "上思县叫安镇那布村那甫屯", lat: 22.100251, lng: 107.978463 },
      { label: "凤凰水库大坝", lat: 22.023744, lng: 107.944299 },
      { label: "叫安镇那工村那兴屯古民居", lat: 22.078256, lng: 107.916555 },
      { label: "叫安镇那布村那楼屯", lat: 22.099595, lng: 107.978007 },
      { label: "叫安镇那布村那楼屯古民居", lat: 22.100235, lng: 107.97818 },
      { label: "叫安镇那荡村平良屯古民居", lat: 21.955119, lng: 107.950307 },
      { label: "叫安镇那荡村那布屯古民居", lat: 21.95552, lng: 107.951181 },
      { label: "四佛水库大坝", lat: 22.146291, lng: 107.832446 },
      { label: "尚透水库大坝", lat: 22.023779, lng: 107.94387 },
      { label: "念伦水库大坝", lat: 22.154551, lng: 107.981802 },
      { label: "东兴乔批馆", lat: 21.535523, lng: 107.969842 },
      { label: "文昌塔", lat: 21.538044, lng: 107.967884 },

      { label: "邓氏民居", lat: 21.534764, lng: 107.969052 },
      { label: "修理一车间厂房", lat: 21.609431, lng: 108.344511 },
      { label: "建港门", lat: 21.62, lng: 108.34 },
      { label: "机修二车间厂房", lat: 21.64, lng: 108.38 },
      { label: "金工车间厂房", lat: 21.609401, lng: 108.344103 },
      { label: "叶寿尧故居", lat: 21.762438, lng: 108.356067 },
      { label: "巫剑雄故居", lat: 21.681517, lng: 107.851423 },
      { label: "杨伯图故居", lat: 21.681929, lng: 107.852438 },
      { label: "郑日东旧居", lat: 21.681869, lng: 107.851903 },
      { label: "陈维周旧居", lat: 21.769212, lng: 108.353499 },
      { label: "全州县永岁镇井头村", lat: 26.040098, lng: 111.1258 },
      { label: "全州县永岁镇慕道村", lat: 26.078396, lng: 111.164307 },
      { label: "全州县大西江镇鹿鸣村", lat: 26.242345, lng: 111.026845 },
      { label: "全州县龙水镇龙水村", lat: 26.037418, lng: 110.996003 },
      { label: "全州县龙水镇石脚村", lat: 25.982283, lng: 111.004386 },
      { label: "全州县两河镇大田村", lat: 25.752333, lng: 111.18447 },
      { label: "全州县两河镇鲁水村", lat: 25.696165, lng: 111.133049 },
      { label: "全州县全州镇大庾岭村", lat: 25.930584, lng: 111.066513 },
      { label: "全州县绍水镇张家村", lat: 25.873026, lng: 110.861456 },
      { label: "全州县绍水镇梅塘村", lat: 25.873026, lng: 110.861456 },
      { label: "全州县东山瑶族乡上塘村", lat: 25.849, lng: 111.336805 },
      { label: "全州县石塘镇沛田村", lat: 25.763723, lng: 111.037282 },
      { label: "灌阳县洞井瑶族乡洞井村", lat: 25.241949, lng: 110.854705 },
      { label: "灌阳县文市镇月岭村", lat: 25.659425, lng: 111.209232 },
      { label: "灌阳县文市镇桂岩村委白竹坪屯", lat: 25.691944, lng: 111.246236 },
      { label: "灌阳县文市镇桂岩村岩口屯", lat: 25.691944, lng: 111.246236 },
      { label: "灌阳县新街镇江口村", lat: 25.427128, lng: 111.114922 },
      { label: "灌阳县新街镇葛洞村大路坡屯", lat: 25.382975, lng: 111.073209 },
      { label: "灌阳县新街镇龙中村富瑞（水）坪村", lat: 25.437523, lng: 111.120069 },
      { label: "灌阳县新街镇青箱村", lat: 25.419487, lng: 111.119529 },
      { label: "灌阳县新街镇飞熊村委杉木屯", lat: 25.419191, lng: 111.135661 },
      { label: "灌阳县水车镇伍家湾村", lat: 25.631765, lng: 111.213636 },
      { label: "灌阳县灌阳镇秀凤村孔家村", lat: 25.489433, lng: 111.158348 },
      { label: "灌阳县灌阳镇仁义村唐家屯", lat: 25.487297, lng: 111.10708 },
      { label: "灌阳县黄关镇兴秀村桐子山屯", lat: 25.337359, lng: 111.056105 },
      { label: "灌阳县观音阁乡大井塘村", lat: 25.25384, lng: 110.905882 },
      { label: "兴安县白石乡水源头村", lat: 25.437261, lng: 110.73163 },
      { label: "兴安县漠川乡钟山坪村", lat: 25.452738, lng: 110.803596 },
      { label: "兴安县漠川乡榜上村", lat: 25.453224, lng: 110.802998 },
      { label: "兴安县榕江镇青山湾村", lat: 25.714182, lng: 110.321003 },
      { label: "兴安镇三桂村委东村", lat: 25.770922, lng: 110.479647 },
      { label: "兴安县高尚镇待漏村", lat: 25.416641, lng: 110.594608 },
      { label: "兴安县高尚镇菜子岩村", lat: 25.416641, lng: 110.594608 },
      { label: "灵川县大圩镇熊村", lat: 25.234445, lng: 110.461586 },
      { label: "灵川县大圩镇上桥村", lat: 25.182445, lng: 110.403816 },
      { label: "灵川县大圩镇秦岸村委大埠村", lat: 25.175205, lng: 110.441125 },
      { label: "灵川县灵田镇长岗岭村", lat: 25.344329, lng: 110.473366 },
      { label: "灵川县灵田镇迪塘村", lat: 25.306482, lng: 110.415565 },
      { label: "灵川县灵田镇宅庆村", lat: 25.344329, lng: 110.473366 },
      { label: "灵川县灵田镇金盆村", lat: 25.440146, lng: 110.473215 },
      { label: "灵川县九屋镇江头村", lat: 25.529779, lng: 110.275675 },
      { label: "灵川县九屋镇老寨村", lat: 25.756427, lng: 110.235899 },
      { label: "灵川县定江镇宝路村委路西村", lat: 25.337628, lng: 110.297497 },
      { label: "灵川县三街镇溶流村委上村", lat: 25.467051, lng: 110.377129 },
      { label: "灵川县潮田乡太平村", lat: 25.228487, lng: 110.536523 },
      { label: "灵川县海洋乡大庙塘村委大桐木湾村", lat: 25.300877, lng: 110.58021 },
      { label: "灵川县海洋乡小平乐村委画眉弄村", lat: 25.302638, lng: 110.666144 },
      { label: "灵川县兰田乡西洲壮寨", lat: 25.597738, lng: 110.213277 },
      { label: "临桂区四塘镇横山村", lat: 25.174557, lng: 110.139497 },
      { label: "桂林市临桂区两江镇(木田木)头村", lat: 25.210871, lng: 110.05046 },
      { label: "临桂区会仙镇山尾村", lat: 25.074812, lng: 110.224405 },
      { label: "临桂区茶洞乡垠头村", lat: 25.245121, lng: 109.961209 },
      { label: "临桂区宛田乡宛田村委东宅江村", lat: 25.535695, lng: 110.06796 },
      { label: "雁山区大埠村大岗埠村", lat: 25.040326, lng: 110.333553 },
      { label: "阳朔县高田镇朗梓村", lat: 24.705283, lng: 110.402351 },
      { label: "阳朔县高田镇龙潭村", lat: 24.710278, lng: 110.462437 },
      { label: "阳朔县普益乡留公村", lat: 24.736501, lng: 110.583905 },
      { label: "阳朔县白沙镇遇龙堡村", lat: 24.812323, lng: 110.404311 },
      { label: "阳朔县白沙镇旧县村", lat: 24.783781, lng: 110.432667 },
      { label: "阳朔县兴坪镇渔村", lat: 24.915543, lng: 110.535023 },
      { label: "平乐县张家镇榕津村", lat: 24.61276, lng: 110.854293 },
      { label: "平乐县同安镇屯塘村委屯塘村", lat: 24.580692, lng: 110.925953 },
      { label: "荔浦市马岭镇永明村委小青山屯", lat: 24.639835, lng: 110.433568 },
      { label: "贺州市富川瑶族自治县朝东镇秀水村", lat: 25.026272, lng: 111.150217 },
      { label: "贺州市富川瑶族自治县朝东镇福溪村", lat: 25.070425, lng: 111.224731 },
      { label: "贺州市富川瑶族自治县葛坡镇深坡村", lat: 24.963102, lng: 111.286275 },
      { label: "贺州市富川瑶族自治县朝东镇岔山村", lat: 25.049595, lng: 111.156401 },
      { label: "贺州市富川瑶族自治县福利镇红岩村", lat: 24.910964, lng: 111.43612 },
      { label: "贺州市富川瑶族自治县朝东镇油沐大村", lat: 25.082104, lng: 111.262024 },
      { label: "贺州市富川瑶族自治县福利镇毛家村", lat: 24.896932, lng: 111.351798 },
      { label: "贺州市富川瑶族自治县石家乡石枧村", lat: 24.964018, lng: 111.405788 },
      { label: "贺州市富川瑶族自治县葛坡镇义竹村", lat: 24.947529, lng: 111.282453 },
      { label: "贺州市富川瑶族自治县城北镇凤溪村", lat: 24.937399, lng: 111.251863 },
      { label: "贺州市富川瑶族自治县麦岭镇和睦村", lat: 25.046534, lng: 111.326157 },
      { label: "贺州市钟山县燕塘镇玉坡村", lat: 24.482761, lng: 111.07442 },
      { label: "贺州市钟山县回龙镇龙道村", lat: 24.444097, lng: 111.316092 },
      { label: "贺州市钟山县公安镇荷塘村", lat: 24.473263, lng: 111.164615 },
      { label: "贺州市钟山县石龙镇源头村", lat: 24.414156, lng: 111.321724 },
      { label: "贺州市钟山县清塘镇英家村英家街", lat: 24.4391, lng: 111.092369 },
      { label: "贺州市钟山县石龙镇松桂村", lat: 24.399625, lng: 111.307588 },
      { label: "贺州市钟山县珊瑚镇同乐村", lat: 24.334454, lng: 111.368231 },
      { label: "贺州市钟山县两安瑶族乡星寨村", lat: 24.661071, lng: 111.171281 },
      { label: "贺州市钟山县公安镇大田村", lat: 24.469263, lng: 111.241919 },
      { label: "贺州市八步区贺街镇河西村", lat: 24.33763, lng: 111.662924 },
      { label: "贺州市八步区莲塘镇仁化村", lat: 24.408836, lng: 111.598556 },
      { label: "贺州市八步区开山镇开山村上莫寨村", lat: 24.786736, lng: 111.708689 },
      { label: "贺州市八步区桂岭镇善华村田尾寨", lat: 24.693447, lng: 111.813506 },
      { label: "贺州市平桂区沙田镇龙井村", lat: 24.33601, lng: 111.4675 },
      { label: "贺州市平桂区羊头镇柿木园村", lat: 24.481267, lng: 111.395719 },
      { label: "贺州市平桂区黄田镇长龙村三角头寨", lat: 24.457839, lng: 111.545312 },
      { label: "贺州市昭平县樟木林镇新华村", lat: 24.145523, lng: 111.269683 },
      { label: "贺州市昭平县樟木林镇樟林村义塘寨", lat: 24.139081, lng: 111.279301 },
      { label: "贺州市昭平县凤凰乡美村村委马鞍山屯", lat: 24.217348, lng: 111.298192 },
      { label: "贺州市昭平县凤凰乡太平村太平寨", lat: 24.234484, lng: 111.306641 },
      { label: "桂林市恭城瑶族自治县恭城镇乐湾村乐湾屯", lat: 24.810269, lng: 110.810605 },
      { label: "桂林市恭城瑶族自治县西岭镇杨溪村杨溪屯", lat: 24.970936, lng: 110.793408 },
      { label: "桂林市恭城瑶族自治县西岭镇西岭村委西岭屯", lat: 24.949168, lng: 110.795066 },
      { label: "桂林市恭城瑶族自治县莲花镇凤岩村凤岩屯", lat: 24.750136, lng: 110.909653 },
      { label: "桂林市恭城瑶族自治县莲花镇朗山村朗山屯", lat: 24.709969, lng: 110.904132 },
      { label: "桂林市恭城瑶族自治县栗木镇大合村大合屯", lat: 24.831581, lng: 110.82841 },
      { label: "桂林市恭城瑶族自治县栗木镇石头村石头屯", lat: 25.165475, lng: 110.925703 },
      { label: "桂林市恭城瑶族自治县栗木镇常家村常家屯", lat: 25.062227, lng: 110.885635 },
      { label: "桂林市恭城瑶族自治县观音乡水滨村", lat: 25.225389, lng: 111.070618 },
      { label: "桂林市恭城瑶族自治县平安镇巨塘村委巨塘屯", lat: 24.778005, lng: 110.865869 },
      { label: "柳州市三江侗族自治县林溪镇平岩村", lat: 25.898798, lng: 109.64391 },
      { label: "柳州市三江侗族自治县林溪镇高友村", lat: 25.902704, lng: 109.648908 },
      { label: "柳州市三江侗族自治县丹洲镇丹洲村", lat: 25.367669, lng: 109.45131 },
      { label: "柳州市三江侗族自治县林溪镇高秀村", lat: 26.000467, lng: 109.710018 },
      { label: "柳州市三江侗族自治县独峒镇岜团村", lat: 25.899754, lng: 109.471342 },
      { label: "柳州市三江侗族自治县独峒镇高定村", lat: 25.981384, lng: 109.48179 },
      { label: "柳州市三江侗族自治县八江镇马胖村磨寨屯", lat: 25.940306, lng: 109.589616 },
      { label: "柳州市三江侗族自治县良口乡和里村", lat: 25.743263, lng: 109.481337 },
      { label: "柳州市三江侗族自治县八江镇归令村", lat: 25.961923, lng: 109.580351 },
      { label: "柳州市三江侗族自治县独峒镇知了村", lat: 25.898905, lng: 109.419103 },
      { label: "柳州市三江侗族自治县同乐苗族乡孟寨村坳寨屯", lat: 25.86423, lng: 109.461609 },
      { label: "柳州市融水苗族自治县杆洞乡党鸠村乌英屯", lat: 25.577792, lng: 108.797058 },
      { label: "柳州市融水苗族自治县杆洞乡尧告村", lat: 25.47957, lng: 108.804526 },
      { label: "柳州市融水苗族自治县拱洞乡平卯村", lat: 25.638728, lng: 109.160421 },
      { label: "柳州市融水苗族自治县杆洞乡杆洞村松美屯", lat: 25.574157, lng: 108.745178 },
      { label: "柳州市融水苗族自治县良寨乡大里村国里屯", lat: 25.563107, lng: 109.090367 },
      { label: "柳州市融水苗族自治县四荣乡东田村", lat: 25.280757, lng: 109.149342 },
      { label: "柳州市融水苗族自治县四荣乡荣地村", lat: 25.3119, lng: 109.120832 },
      { label: "柳州市融水苗族自治县安太乡寨怀村新寨屯", lat: 25.388467, lng: 109.066704 },
      { label: "柳州市鹿寨县平山镇青山村堡底屯", lat: 24.665476, lng: 109.590956 },
      { label: "柳州市鹿寨县中渡镇寨上村寨上屯", lat: 24.819501, lng: 109.769902 },
      { label: "柳州市融安县大将镇龙妙村龙妙屯", lat: 25.224549, lng: 109.397538 },
      { label: "柳州市融安县雅瑶乡大琴村坡伟屯", lat: 25.286341, lng: 109.639823 },
      { label: "桂林市龙胜各族自治县平等镇平等村委平等村", lat: 26.051975, lng: 109.92853 },
      { label: "桂林市龙胜各族自治县龙脊镇金江村委金竹壮寨", lat: 25.747262, lng: 110.113767 },
      { label: "桂林市龙胜各族自治县龙脊镇龙脊村", lat: 25.747322, lng: 110.112905 },
      { label: "桂林市龙胜各族自治县平等镇广南村委广南村", lat: 26.018784, lng: 109.920001 },
      { label: "桂林市龙胜各族自治县平等镇龙坪村委龙坪村", lat: 26.048741, lng: 109.928116 },
      { label: "桂林市龙胜各族自治县乐江镇地灵村委地灵村", lat: 25.949972, lng: 109.840296 },
      { label: "桂林市龙胜各族自治县乐江镇宝赠村委宝赠村", lat: 25.984412, lng: 109.843451 },
      { label: "桂林市龙胜各族自治县平等镇寨枕村寨枕屯", lat: 26.048741, lng: 109.928116 },
      { label: "桂林市龙胜各族自治县乐江镇独镜村委独镜村", lat: 25.952491, lng: 109.887876 },
      { label: "桂林市龙胜各族自治县龙胜镇金车村委金车屯", lat: 25.750144, lng: 110.004214 },
      { label: "桂林市龙胜各族自治县伟江乡布弄村委布弄村", lat: 26.002769, lng: 110.094085 },
      { label: "桂林市资源县两水苗族乡塘洞村西寨屯", lat: 25.878648, lng: 110.372089 },
      { label: "桂林市资源县资源镇马家村", lat: 26.091852, lng: 110.624883 },
      { label: "来宾市金秀瑶族自治县六巷乡下古陈村", lat: 23.935141, lng: 110.102493 },
      { label: "来宾市金秀瑶族自治县桐木镇那安村龙腾屯", lat: 24.259547, lng: 110.050757 },
      { label: "来宾市金秀瑶族自治县六巷乡门头村", lat: 23.866587, lng: 110.016504 },
      { label: "来宾市金秀瑶族自治县金秀镇六段村六段屯", lat: 24.13008, lng: 110.188761 },
      { label: "来宾市金秀瑶族自治县金秀镇共和村古卜屯", lat: 24.069905, lng: 110.289509 },
      { label: "来宾市象州县罗秀镇纳禄村", lat: 24.063915, lng: 109.849126 },
      { label: "来宾市象州县罗秀镇军田村委军田村", lat: 24.047117, lng: 109.925385 },
      { label: "梧州市长洲区长洲镇泗洲村", lat: 23.422848, lng: 111.205958 },
      { label: "梧州市龙圩区大坡镇料神村", lat: 23.310141, lng: 111.280683 },
      { label: "梧州市苍梧县沙头镇大寨村", lat: 23.938679, lng: 111.534489 },
      { label: "梧州市藤县天平镇新马村", lat: 23.451946, lng: 110.601093 },
      { label: "梧州市藤县象棋镇道家村", lat: 23.128712, lng: 110.692691 },
      { label: "梧州市岑溪市筋竹镇云龙村", lat: 22.898107, lng: 111.286851 },
      { label: "梧州市岑溪市归义镇谢村", lat: 22.887482, lng: 111.059936 },
      { label: "梧州市蒙山县长坪瑶族乡六坪村", lat: 24.33934, lng: 110.519301 },
      { label: "贵港市港南区木格镇云垌村", lat: 22.883666, lng: 109.725989 },
      { label: "贵港市港南区木梓镇回龙村", lat: 22.727349, lng: 109.595465 },
      { label: "贵港市港南区木格镇陈索村", lat: 22.78565, lng: 109.712017 },
      { label: "贵港市港北区港城镇龙井村", lat: 23.10551, lng: 109.605682 },
      { label: "贵港市桂平市中沙镇南乡村", lat: 22.915227, lng: 110.127911 },
      { label: "贵港市平南县大鹏镇大鹏村石门屯", lat: 23.74167, lng: 110.182469 },
      { label: "贵港市平南县思旺镇双上村上宋屯", lat: 23.724363, lng: 110.312624 },
      { label: "贵港市平南县镇隆镇富藏村中团屯", lat: 23.336431, lng: 110.381461 },
      { label: "贵港市平南县大安镇镇大社区", lat: 23.387523, lng: 110.515767 },
      { label: "南宁市江南区江西镇扬美村", lat: 22.836473, lng: 108.064108 },
      { label: "南宁市江南区江西镇同新村木村坡", lat: 22.710907, lng: 108.171652 },
      { label: "南宁市江南区江西镇同江村三江坡", lat: 22.820524, lng: 108.094809 },
      { label: "南宁市西乡塘区金陵镇刚德村大石坡", lat: 22.833852, lng: 108.31344 },
      { label: "南宁市西乡塘区坛洛镇下楞村", lat: 22.829121, lng: 108.037278 },
      { label: "南宁市邕宁区那楼镇那良村那蒙坡", lat: 22.619824, lng: 108.496216 },
      { label: "南宁市良庆区那马镇莲山村祠堂村", lat: 22.576375, lng: 108.319025 },
      { label: "南宁市宾阳县古辣镇古辣社区蔡村", lat: 23.10516, lng: 108.983366 },
      { label: "南宁市宾阳县中华镇上施村下施村", lat: 23.101742, lng: 108.943669 },
      { label: "南宁市宾阳县武陵镇武陵村委高荣村", lat: 23.140334, lng: 108.895843 },
      { label: "南宁市横州市平朗乡笔山村", lat: 22.683594, lng: 108.910586 },
      { label: "南宁市上林县巷贤镇长联村古民庄", lat: 23.204267, lng: 108.671487 },
      { label: "崇左市江州区驮卢镇连塘村花梨屯", lat: 22.656071, lng: 107.63995 },
      { label: "崇左市江州区驮卢镇灶瓦村红山屯", lat: 22.658772, lng: 107.67633 },
      { label: "崇左市扶绥县新宁镇长沙村", lat: 22.656589, lng: 107.910474 },
      { label: "崇左市扶绥县中东镇中东社区", lat: 22.824752, lng: 107.842126 },
      { label: "崇左市宁明县城中镇耀达村", lat: 22.252444, lng: 107.010788 },
      { label: "崇左市龙州县上金乡中山村", lat: 22.321792, lng: 107.00961 },
      { label: "河池市南丹县里湖瑶族乡巴哈屯", lat: 25.104827, lng: 107.668338 },
      { label: "河池市南丹县里湖瑶族乡怀里村蛮降屯", lat: 25.116247, lng: 107.700293 },
      { label: "河池市环江毛南族自治县下南乡中南村南昌屯", lat: 24.932084, lng: 107.992848 },
      { label: "河池市宜州区怀远镇怀远社区", lat: 24.567184, lng: 108.473355 },
      { label: "河池市宜州区三岔镇合林村合林屯", lat: 24.434501, lng: 108.907958 },
      { label: "河池市天峨县三堡乡三堡村堡上屯", lat: 25.37325, lng: 107.08216 },
      { label: "河池市凤山县平乐瑶族乡谋爱村社坡屯", lat: 24.546913, lng: 107.042157 },
      { label: "百色市西林县马蚌镇浪吉村那岩屯", lat: 24.630962, lng: 104.575669 },
      { label: "百色市隆林各族自治县金钟山乡平流屯", lat: 24.656295, lng: 104.91845 },
      { label: "百色市西林县那劳村岑氏家族建筑群", lat: 24.50762, lng: 105.097229 },
      { label: "百色市乐业县花坪镇浪筛村野猪坨屯", lat: 24.776123, lng: 106.418779 },
      { label: "百色市凌云县泗城镇品村龙洞屯", lat: 24.341985, lng: 106.644717 },
      { label: "百色市那坡县城厢镇达腊屯", lat: 23.399375, lng: 105.834098 },
      { label: "百色市德保县足荣镇那亮村那雷屯", lat: 23.339905, lng: 106.736176 },
      { label: "百色市靖西市新靖镇旧州街", lat: 23.058864, lng: 106.414706 },
      { label: "北海市合浦县山口镇永安村", lat: 21.601789, lng: 109.730346 },
      { label: "北海市合浦县曲樟乡璋嘉村委老屋村", lat: 21.792939, lng: 109.469104 },
      { label: "北海市海城区涠洲岛镇盛塘村", lat: 21.048925, lng: 109.131169 },
      { label: "北海市海城区涠洲岛镇荔枝山村圩仔村", lat: 21.026605, lng: 109.1134 },
      { label: "北海市银滩区银滩镇南万社区", lat: 21.446609, lng: 109.06014 },
      { label: "钦州市灵山县佛子镇大芦村", lat: 22.45139, lng: 109.341696 },
      { label: "钦州市灵山县佛子镇佛子村委马肚塘村", lat: 22.416671, lng: 109.290698 },
      { label: "钦州市灵山县新圩镇萍塘村", lat: 22.362271, lng: 109.285756 },
      { label: "钦州市灵山县太平镇华屏岭村", lat: 22.267585, lng: 109.286501 },
      { label: "钦州市灵山县新圩镇漂塘村", lat: 22.375249, lng: 109.302921 },
      { label: "钦州市灵山县石塘镇苏村", lat: 22.574222, lng: 109.492674 },
      { label: "钦州市浦北县小江镇余屋村", lat: 22.192132, lng: 109.564009 },
      { label: "钦州市浦北县石埇镇坡子坪村委老城村", lat: 21.946992, lng: 109.593367 },
      { label: "防城港市防城区大箓镇那厚村", lat: 21.851525, lng: 108.113074 },
      { label: "防城港市东兴市东兴镇竹山村", lat: 21.543296, lng: 108.058344 },
      { label: "防城港市港口区企沙镇簕山古渔村", lat: 21.586791, lng: 108.471199 },
      { label: "防城港市东兴市江平镇万尾村", lat: 21.527031, lng: 108.158989 },
      { label: "玉林市玉州区城北街道高山村", lat: 22.689852, lng: 110.147624 },
      { label: "玉林市福绵区福绵镇福西村", lat: 22.585316, lng: 110.059564 },
      { label: "玉林市福绵区新桥镇大楼村", lat: 22.516551, lng: 110.122654 },
      { label: "玉林市兴业县城隍镇谭良村", lat: 22.74194, lng: 109.908235 },
      { label: "玉林市兴业县城隍镇大西村", lat: 22.600015, lng: 109.739838 },
      { label: "玉林市兴业县石南镇庞村", lat: 22.745285, lng: 109.887142 },
      { label: "玉林市兴业县石南镇东山村", lat: 22.7418, lng: 109.875693 },
      { label: "玉林市兴业县葵阳镇葵联村榜山村", lat: 22.733507, lng: 109.823641 },
      { label: "玉林市兴业县蒲塘镇石山村石山坡", lat: 22.889722, lng: 109.952134 },
      { label: "玉林市容县杨村镇东华村", lat: 22.59988, lng: 110.79134 },
      { label: "玉林市博白县松旺镇松茂村", lat: 21.890881, lng: 109.758174 }
    ]
  },
  {
    label: "Residential Buildings",
    visible: false,
    items: [
      /*
      { label: "永安家塾", lat: 23.108895, lng: 113.437802 },
      { label: "冠英家塾旧址", lat: 23.123504, lng: 113.266766 },
      { label: "双溪别墅", lat: 23.19637, lng: 113.308289 },
      { label: "三元里大街二十七巷9号民居", lat: 23.158581, lng: 113.261146 },
      { label: "宝龙直街10号民居", lat: 23.10218, lng: 113.26965 },
      { label: "宝龙直街18、20号民居", lat: 23.102537, lng: 113.260447 },
      { label: "福居里3号民居", lat: 23.105898, lng: 113.259862 },
      { label: "龙福东二巷2号民居", lat: 23.092994, lng: 113.267038 },
      { label: "龙福东一巷4号民居", lat: 23.103547, lng: 113.259155 },
      { label: "顾庐、康庐", lat: 23.103471, lng: 113.259044 },
      { label: "龙延里2-1号民居", lat: 22.617597, lng: 110.154556 },
      { label: "龙骧大街11号民居", lat: 23.103414, lng: 113.260509 },
      { label: "龙骧大街12、14号民居", lat: 23.102172, lng: 113.269735 },
      { label: "龙骧大街15号民居", lat: 23.101523, lng: 113.261813 },
      { label: "龙骧大街16号民居", lat: 23.102845, lng: 113.259992 },
      { label: "龙骧大街19号民居", lat: 23.102988, lng: 113.260298 },
      { label: "龙骧大街21号民居", lat: 23.101651, lng: 113.261782 },
      { label: "龙骧大街22号民居", lat: 23.102573, lng: 113.260056 },
      { label: "龙骧大街24号民居", lat: 23.102514, lng: 113.260064 },
      { label: "龙骧大街3号民居", lat: 23.103204, lng: 113.260142 },
      { label: "龙骧大街4号民居", lat: 23.103218, lng: 113.260397 },
      { label: "龙骧大街8、10号民居", lat: 23.10218, lng: 113.26965 },
      { label: "关山月旧居", lat: 23.093763, lng: 113.277462 },
      { label: "大塘村西华大街10号民居", lat: 23.089533, lng: 113.263902 },
      { label: "昆仑三街10、12号民居", lat: 23.102175, lng: 113.269695 },
      { label: "昆仑三街29、29-1、29-2号民居", lat: 23.098259, lng: 113.258112 },
      { label: "肇昌堂", lat: 23.059144, lng: 113.312318 },
      { label: "梅园西路38号民居", lat: 23.093974, lng: 113.256174 },
      { label: "栖栅南街19号民居", lat: 23.103505, lng: 113.255396 },
      { label: "栖栅南街40号民居", lat: 23.104056, lng: 113.255345 },
      { label: "前进路18号民居", lat: 23.103562, lng: 113.271735 },
      { label: "前进路54号-28民居", lat: 23.099783, lng: 113.274614 },
      { label: "前进路54号-30民居", lat: 23.100231, lng: 113.274727 },
      { label: "同庆四街1号民居", lat: 23.10796, lng: 113.265824 },
      { label: "跃龙南27号民居", lat: 23.108746, lng: 113.265536 },
      { label: "溪峡街13、13-1号民居", lat: 23.103947, lng: 113.256861 },
      { label: "溪峡街1号民居", lat: 23.10334, lng: 113.25683 },
      { label: "溪峡街7号民居", lat: 23.103717, lng: 113.256848 },
      { label: "溪峡新街18号民居", lat: 23.104496, lng: 113.257102 },
      { label: "溪峡新街1—13（单号）号民居", lat: 23.10434, lng: 113.256767 },
      { label: "伍家祠道9、11号民居", lat: 23.103843, lng: 113.257292 },
      { label: "蟠龙西1-2号民居", lat: 23.066978, lng: 113.186086 },
      { label: "蟠龙西新巷1号民居", lat: 23.10525, lng: 113.263113 },
      { label: "蟠龙西新巷7、7-1号民居", lat: 23.10525, lng: 113.263113 },
      { label: "同和里18号民居", lat: 23.100417, lng: 113.260153 },
      { label: "存善东横街13号民居", lat: 22.545915, lng: 113.381893 },
      { label: "存善南街4号民居", lat: 23.119174, lng: 113.242457 },
      { label: "存善西街1号民居", lat: 23.119861, lng: 113.242475 },
      { label: "存善正街15、17号民居", lat: 23.119482, lng: 113.24243 },
      { label: "存善正街4、6、8号民居", lat: 23.119464, lng: 113.242759 },
      { label: "宝源路123号民居", lat: 23.118763, lng: 113.241065 },
      { label: "宝源路125号民居", lat: 23.118795, lng: 113.241122 },
      { label: "宝源路127号民居", lat: 23.118745, lng: 113.24118 },
      { label: "宝源路139号民居", lat: 23.118725, lng: 113.241592 },
      { label: "明勤第", lat: 23.11876, lng: 113.241584 },
      { label: "宝源中约11号民居", lat: 23.119061, lng: 113.241193 },
      { label: "宝源中约25号民居", lat: 23.119135, lng: 113.240781 },
      { label: "宝源中约48号民居", lat: 23.119336, lng: 113.240243 },
      { label: "宝源中约54号民居", lat: 23.119351, lng: 113.24001 },
      { label: "宝源中约56号民居", lat: 23.119358, lng: 113.239962 },
      { label: "昌华大街2-2号民居", lat: 23.115761, lng: 113.236122 },
      { label: "昌华大街24号民居", lat: 23.115827, lng: 113.234904 },
      { label: "昌华大街8号后座民居", lat: 23.115797, lng: 113.235333 },
      { label: "昌华庐", lat: 23.115587, lng: 113.234622 },
      { label: "昌华新街12号民居", lat: 23.115359, lng: 113.234943 },
      { label: "昌华新街14号民居", lat: 23.115359, lng: 113.234892 },
      { label: "昌华新街3-1号民居", lat: 23.115192, lng: 113.235285 },
      { label: "昌华新街8、10号民居", lat: 23.115348, lng: 113.235063 },
      { label: "昌华新街9号民居", lat: 23.115246, lng: 113.234916 },
      { label: "多宝街49号民居", lat: 23.116379, lng: 113.235945 },
      { label: "多宝街51号民居", lat: 23.116378, lng: 113.235863 },
      { label: "多宝街58、58-1号民居", lat: 23.116542, lng: 113.235603 },
      { label: "多宝街81号民居", lat: 23.116429, lng: 113.23509 },
      { label: "多宝路183、185号民居", lat: 23.116667, lng: 113.239873 },
      { label: "多宝路189、191号民居", lat: 23.116653, lng: 113.240226 },
      { label: "多宝南横20号民居", lat: 23.116141, lng: 113.235267 },
      { label: "多宝南横38号民居", lat: 23.11605, lng: 113.23496 },
      { label: "多宝南横6-1、6-2号民居", lat: 23.11612, lng: 113.23598 },
      { label: "多宝南横6号民居", lat: 23.116114, lng: 113.235974 },
      { label: "逢源正中约18、20号民居", lat: 23.120473, lng: 113.239308 },
      { label: "鸣谦里9号民居", lat: 23.116555, lng: 113.251259 },
      { label: "和平中路114号民居", lat: 23.1115, lng: 113.246503 },
      { label: "和息里27号民居", lat: 23.110619, lng: 113.244126 },
      { label: "民治大街32号民居", lat: 23.09873, lng: 113.23747 },
      { label: "民治大街34号民居", lat: 23.09901, lng: 113.23757 },
      { label: "富善西街15号民居", lat: 23.11277, lng: 113.247817 },
      { label: "富善西街19号民居", lat: 23.112927, lng: 113.247773 },
      { label: "富善一巷2-2、2-3号民居", lat: 23.112472, lng: 113.248106 },
      { label: "怀远驿37号民居", lat: 23.111981, lng: 113.248774 },
      { label: "怀远驿42号民居", lat: 23.111981, lng: 113.248774 },
      { label: "冼基东19号民居", lat: 23.111981, lng: 113.248774 },
      { label: "耀华大街11号民居", lat: 23.118601, lng: 113.24518 },
      { label: "耀华大街13、13-1号民居", lat: 23.11865, lng: 113.245185 },
      { label: "耀华大街15、15-1号民居", lat: 23.118699, lng: 113.24519 },
      { label: "耀华大街17、19号民居", lat: 23.118748, lng: 113.245195 },
      { label: "耀华大街1、3号民居", lat: 23.118403, lng: 113.245183 },
      { label: "耀华大街20号民居", lat: 23.118727, lng: 113.245167 },
      { label: "耀华大街23号民居", lat: 23.118706, lng: 113.245139 },
      { label: "耀华大街24、24-1号民居", lat: 23.118698, lng: 113.24513 },
      { label: "耀华大街28、28-1号民居", lat: 23.11867, lng: 113.245093 },
      { label: "耀华大街30号民居", lat: 23.118656, lng: 113.245075 },
      { label: "耀华大街32号民居", lat: 23.118642, lng: 113.245056 },
      { label: "耀华大街9、9-1号民居", lat: 23.118559, lng: 113.245186 },
      { label: "粤华西一街18、20号民居", lat: 21.643599, lng: 110.92898 },
      { label: "民兴里2、4、6号民居", lat: 23.119185, lng: 113.261895 },
      { label: "雅荷塘69号民居", lat: 23.129088, lng: 113.275981 },
      { label: "东皋大道11号院民居", lat: 23.128463, lng: 113.281971 },
      { label: "东皋二横路3、5号民居", lat: 23.129062, lng: 113.281999 },
      { label: "东皋二横路4号民居", lat: 23.129062, lng: 113.281999 },
      { label: "东皋二横路6号民居", lat: 23.129062, lng: 113.281999 },
      { label: "东皋二横路8号民居", lat: 23.129062, lng: 113.281999 },
      { label: "东皋一横路14、16号民居", lat: 23.128463, lng: 113.281971 },
      { label: "东皋一横路2号民居", lat: 23.128371, lng: 113.281453 },
      { label: "东皋一横路3号民居", lat: 23.128463, lng: 113.281971 },
      { label: "东皋一横路7号民居", lat: 23.128463, lng: 113.281971 },
      { label: "皋园4号民居", lat: 23.12847, lng: 113.281279 },
      { label: "皋园7号民居", lat: 23.12847, lng: 113.281279 },
      { label: "礼兴街10号民居", lat: 23.128095, lng: 113.280113 },
      { label: "仁兴街2号民居", lat: 23.12847, lng: 113.281279 },
      { label: "义兴园1号民居", lat: 23.12847, lng: 113.281279 },
      { label: "智兴街2号民居", lat: 23.128962, lng: 113.281089 },
      { label: "礼兴街11、13、15号民居", lat: 23.1281, lng: 113.28064 },
      { label: "连云里2、4、6、8号民居", lat: 23.119711, lng: 113.26872 },
      { label: "观绿路10、10-1号民居、广华道1—15号（单号）民居", lat: 23.118798, lng: 113.254811 },
      { label: "观绿路2-2、2-3号民居", lat: 23.118739, lng: 113.25561 },
      { label: "观绿路2-4号民居", lat: 23.11869, lng: 113.2554 },
      { label: "观绿路4-1、4-2号民居", lat: 23.118725, lng: 113.255245 },
      { label: "观绿路6、8号民居", lat: 23.118683, lng: 113.255166 },
      { label: "观绿路7号民居", lat: 23.118526, lng: 113.25512 },
      { label: "观绿新街16号民居", lat: 23.118664, lng: 113.254131 },
      { label: "广华道18号民居", lat: 23.118664, lng: 113.254131 },
      { label: "广华道2、4、6、8号民居", lat: 22.313372, lng: 114.178067 },
      { label: "杏花巷民居", lat: 23.123184, lng: 113.257064 },
      { label: "广福巷1、3号民居", lat: 23.127817, lng: 113.26656 },
      { label: "海珠中路151、153号民居", lat: 23.121429, lng: 113.256588 },
      { label: "海珠中路162、164、166号民居", lat: 23.120915, lng: 113.256688 },
      { label: "豪贤路86号民居", lat: 23.130353, lng: 113.275323 },
      { label: "进步里1号民居", lat: 23.122257, lng: 113.258025 },
      { label: "南濠街42、42-1号民居", lat: 23.119404, lng: 113.256584 },
      { label: "南濠街81-1、81-2、83号民居", lat: 23.11968, lng: 113.256529 },
      { label: "霍芝庭公馆旧址", lat: 23.126, lng: 113.262472 },
      { label: "金城巷1—12号民居", lat: 23.121911, lng: 113.260166 },
      { label: "南朝街1号民居", lat: 23.124107, lng: 113.266276 },
      { label: "模范住宅区旧址农林上路12号", lat: 23.125134, lng: 113.297128 },
      { label: "模范住宅区旧址农林上路14号", lat: 23.125219, lng: 113.297128 },
      { label: "模范住宅区旧址农林上路二横路2号", lat: 23.125901, lng: 113.297526 },
      { label: "模范住宅区旧址农林上路二横路4号", lat: 23.125889, lng: 113.297662 },
      { label: "模范住宅区旧址农林上路二横路6号", lat: 23.125868, lng: 113.297806 },
      { label: "模范住宅区旧址农林上路七横路7号", lat: 23.128215, lng: 113.298543 },
      { label: "模范住宅区旧址农林下路19号", lat: 23.127157, lng: 113.295605 },
      { label: "畸零里5号民居", lat: 23.116494, lng: 113.26488 },
      { label: "启明大马路5号民居", lat: 23.121351, lng: 113.293657 },
      { label: "秦牧旧居", lat: 23.120852, lng: 113.293344 },
      { label: "启明横马路11-2号民居", lat: 23.121763, lng: 113.292647 },
      { label: "启明横马路17号民居", lat: 23.121386, lng: 113.292689 },
      { label: "启明横马路1号民居", lat: 23.121193, lng: 113.292493 },
      { label: "启明四马路11号民居", lat: 23.121576, lng: 113.293092 },
      { label: "启明四马路4号民居", lat: 23.121577, lng: 113.293508 },
      { label: "模范住宅区旧址三育路32号", lat: 23.129294, lng: 113.299819 },
      { label: "模范住宅区旧址三育路44号", lat: 23.129764, lng: 113.299751 },
      { label: "诗书路117、119、121号民居", lat: 23.120369, lng: 113.254665 },
      { label: "诗书路68号民居", lat: 23.118894, lng: 113.254603 },
      { label: "诗书路78号后座民居", lat: 23.119061, lng: 113.254631 },
      { label: "仁亨里15、15-1号民居", lat: 23.119845, lng: 113.254532 },
      { label: "仁亨里1、1-1号民居", lat: 23.119845, lng: 113.254353 },
      { label: "木排横街11号民居", lat: 23.117704, lng: 113.266758 },
      { label: "木排头2、2-1号民居", lat: 23.118857, lng: 113.268261 },
      { label: "木排头57、59、61、63号民居", lat: 23.118154, lng: 113.267309 },
      { label: "宜安里29号民居", lat: 23.117433, lng: 113.265962 },
      { label: "文德路43、43-1号民居", lat: 23.121624, lng: 113.272114 },
      { label: "文德路45、47号民居", lat: 23.116962, lng: 113.272559 },
      { label: "仰忠街14、14-1号民居", lat: 23.121289, lng: 113.271033 },
      { label: "小北路222~228号（双号）民居", lat: 23.137015, lng: 113.273386 },
      { label: "学宫街28、30号民居", lat: 23.12128, lng: 113.261719 },
      { label: "盐运西二巷2号民居", lat: 23.121325, lng: 113.265609 },
      { label: "梧庐", lat: 23.12143, lng: 113.265294 },
      { label: "盐运西一巷18、20号民居", lat: 23.120894, lng: 113.265152 },
      { label: "盐运西一巷13、15号民居", lat: 23.121167, lng: 113.265381 },
      { label: "盐运西一巷14号民居", lat: 23.12093, lng: 113.265316 },
      { label: "盐运西一巷2、2-1、2-2号民居", lat: 23.12077, lng: 113.265731 },
      { label: "盐运西一巷5号民居", lat: 23.120988, lng: 113.265595 },
      { label: "盐运西正街19、21、23、25、27号民居", lat: 23.121842, lng: 113.265575 },
      { label: "盐运西正街1、3、5号民居", lat: 23.121276, lng: 113.265723 },
      { label: "盐运西正街26、28号民居", lat: 23.121952, lng: 113.265683 },
      { label: "越秀北路林克明旧居", lat: 23.134612, lng: 113.275094 },
      { label: "越秀北路78号", lat: 23.128631, lng: 113.278769 },
      { label: "模范住宅区旧址执信南路9号", lat: 23.125397, lng: 113.293067 },
      { label: "纸行路42号民居", lat: 23.122107, lng: 113.255201 },
      { label: "白沙巷10-1号民居", lat: 23.122038, lng: 113.254299 },
      { label: "白沙巷21、21-1号民居", lat: 23.121681, lng: 113.254288 },
      { label: "白沙巷27、29、31号民居", lat: 23.122006, lng: 113.253947 },
      { label: "侨星新街4、6号民居", lat: 23.121559, lng: 113.25469 },
      { label: "侨星新街8—18（双号）号民居", lat: 23.121566, lng: 113.254653 },
      { label: "通宁道14、16、18、20号民居", lat: 23.123288, lng: 113.254932 },
      { label: "通宁道17、19、21、23、25号民居", lat: 23.123266, lng: 113.254835 },
      { label: "通宁道22、24、26号民居", lat: 23.123364, lng: 113.2548 },
      { label: "通宁道2、4号民居", lat: 23.123283, lng: 113.25522 },
      { label: "通宁道6、8、10、12号民居", lat: 23.123313, lng: 113.255134 },
      { label: "通宁道9、11、13、15号民居", lat: 23.12333, lng: 113.255088 },
      { label: "模范住宅区旧址菜园西35号", lat: 23.125031, lng: 113.290929 },
      { label: "中山六路76号民居", lat: 23.125402, lng: 113.259081 },
      { label: "苏鸣一旧居", lat: 23.124852, lng: 113.258056 },
      { label: "玛瑙巷55号民居", lat: 23.124892, lng: 113.258054 },
      { label: "中山三路2号民居", lat: 23.126675, lng: 113.286422 },
      { label: "中山三路4号民居", lat: 23.126719, lng: 113.286379 },
      { label: "模范住宅区旧址梅花村29号", lat: 23.127492, lng: 113.30484 },
      { label: "模范住宅区旧址梅花村34号", lat: 23.127492, lng: 113.30484 },
      { label: "模范住宅区旧址梅花村69号", lat: 23.12826, lng: 113.3047 },
      { label: "咸虾栏14号、侨庆坊1、3号民居", lat: 23.118477, lng: 113.27444 },
      { label: "模范住宅区旧址竹丝岗大马路1号", lat: 23.127449, lng: 113.29327 },
      { label: "模范住宅区旧址竹丝岗二马路14号", lat: 23.127158, lng: 113.294139 },
      { label: "模范住宅区旧址竹丝岗二马路43号", lat: 23.129056, lng: 113.296189 },
      { label: "模范住宅区旧址竹丝岗三马路1号", lat: 23.126664, lng: 113.293439 },
      { label: "模范住宅区旧址竹丝岗四马路1号", lat: 23.126374, lng: 113.293567 },
      { label: "光复南路113号", lat: 23.114484, lng: 113.252138 },
      { label: "光复南路121号", lat: 23.114684, lng: 113.252117 },
      { label: "光复南路139、141、143号", lat: 23.115091, lng: 113.251975 },
      { label: "光复南路145号", lat: 23.114499, lng: 113.252183 },
      { label: "光复南路176号", lat: 23.115636, lng: 113.252041 },
      { label: "光复南路21号", lat: 23.112871, lng: 113.252674 },
      { label: "光复南路26号", lat: 23.112885, lng: 113.252914 },
      { label: "光复南路28号", lat: 23.112904, lng: 113.25291 },
      { label: "光复南路30号", lat: 23.112925, lng: 113.252905 },
      { label: "光复南路32号", lat: 23.112946, lng: 113.252903 },
      { label: "光复南路40号", lat: 23.113007, lng: 113.252808 },
      { label: "光复南路48号", lat: 23.113263, lng: 113.252816 },
      { label: "光复南路50号", lat: 23.113295, lng: 113.252809 },
      { label: "光复南路54号", lat: 23.11338, lng: 113.252749 },
      { label: "光复南路56号", lat: 23.113394, lng: 113.252782 },
      { label: "光复南路68号", lat: 23.113816, lng: 113.252619 },
      { label: "光复南路87号", lat: 23.114064, lng: 113.252243 },
      { label: "光复南路89号", lat: 23.114098, lng: 113.252234 },
      { label: "光复南路99号", lat: 23.114249, lng: 113.252187 },
      { label: "十八甫路107、109、111号", lat: 23.111922, lng: 113.247548 },
      { label: "十八甫路132、134号", lat: 23.112115, lng: 113.2469 },
      { label: "十八甫路136号", lat: 23.112108, lng: 113.246838 },
      { label: "十八甫路33号", lat: 23.112027, lng: 113.249472 },
      { label: "十八甫路55号", lat: 23.111965, lng: 113.248985 },
      { label: "十八甫路82、84号", lat: 23.112104, lng: 113.248267 },
      { label: "十八甫路90号", lat: 23.112123, lng: 113.248055 },
      { label: "十八甫路92号", lat: 23.112074, lng: 113.247913 },
      { label: "十八甫路93号", lat: 23.111898, lng: 113.248077 },
      { label: "十八甫路98号", lat: 23.112078, lng: 113.247807 },
      { label: "沿江西路47号", lat: 23.10837, lng: 113.252686 },
      { label: "杨巷路107号", lat: 23.114776, lng: 113.24963 },
      { label: "杨巷路29、29-2号", lat: 23.112958, lng: 113.249815 },
      { label: "惠福东路401、403号", lat: 23.120582, lng: 113.264855 },
      { label: "惠福东路413、415号", lat: 23.120662, lng: 113.265143 },
      { label: "纸行路11、13、15号", lat: 23.121336, lng: 113.254861 },
      { label: "纸行路41、43、45号", lat: 23.122652, lng: 113.255216 },
      { label: "纸行路56、58、60号", lat: 23.122411, lng: 113.255308 },
      { label: "纸行路59、61、63号", lat: 23.123033, lng: 113.25527 },
      { label: "钟落潭村福龙路129号民居", lat: 23.386005, lng: 113.402636 },
      { label: "梅田村迎龙门楼", lat: 23.358641, lng: 113.413964 },
      { label: "显扬梁公家塾", lat: 23.048437, lng: 113.372766 },
      { label: "大岭村龙津街上达巷1号民居", lat: 22.985158, lng: 113.477564 },
      { label: "大岭村昇平街永福巷2号民居", lat: 22.985158, lng: 113.477564 },
      { label: "大岭村中兴街仁厚一巷8号民居", lat: 22.985158, lng: 113.477564 },
      { label: "贝岗村民居", lat: 23.052602, lng: 113.380118 },
      { label: "庚辉坊北街10号民居", lat: 22.950782, lng: 113.443486 },
      { label: "穗石村西市大街13号民居", lat: 23.046805, lng: 113.410209 },
      { label: "秀发村得月街3号民居", lat: 23.039571, lng: 113.420563 },
      { label: "黄埔村盘石大街13号民居", lat: 23.090686, lng: 113.397309 },
      { label: "黄埔村盘石大街八巷4号民居", lat: 23.091421, lng: 113.398256 },
      { label: "同福西路歧兴中北4-1民居", lat: 23.102926, lng: 113.252755 },
      { label: "洛场村十队21号民居", lat: 23.424357, lng: 113.237597 },
      { label: "平东村平东七队141号民居", lat: 23.425514, lng: 113.29199 },
      { label: "平东村平东四队59号民居", lat: 23.431137, lng: 113.28859 },
      { label: "利明别墅", lat: 23.426236, lng: 113.295192 },
      { label: "大同别墅", lat: 23.384564, lng: 113.258936 },
      { label: "十五甫正街18号之一民居", lat: 23.115629, lng: 113.240936 },
      { label: "逢源路莲塘二巷13号民居", lat: 23.118211, lng: 113.240228 },
      { label: "九佛人民公社礼堂旧址", lat: 23.353943, lng: 113.521179 },
      { label: "保安南街3号民居", lat: 23.120022, lng: 113.30057 },
      { label: "保安前街13号民居", lat: 23.120438, lng: 113.300682 },
      { label: "龟岗三马路16、18、20号民居", lat: 23.120662, lng: 113.293617 },
      { label: "均益路5号民居", lat: 23.121521, lng: 113.291596 },
      { label: "启明二马路5号民居", lat: 23.120964, lng: 113.292375 },
      { label: "启明二马路6号民居", lat: 23.120867, lng: 113.293137 },
      { label: "横岭村大塘尾家驹家塾", lat: 23.612785, lng: 113.483824 },
      { label: "沙湾镇恒庐", lat: 22.906841, lng: 113.338301 },
      { label: "何炳林故居", lat: 22.907173, lng: 113.335969 },
      { label: "新民十一街22、24号民居", lat: 23.09399, lng: 113.25397 },
      { label: "新民十一街4、6号民居", lat: 23.093581, lng: 113.254067 },
      { label: "南福安街4号后座民居", lat: 23.105028, lng: 113.255301 },
      { label: "栖栅南街26、28号民居", lat: 23.103996, lng: 113.254849 },
      { label: "栖栅南街2号民居", lat: 23.103594, lng: 113.254789 },
      { label: "栖栅南街52号民居", lat: 23.103479, lng: 113.255227 },
      { label: "栖栅南街6号民居", lat: 23.104074, lng: 113.255881 },
      { label: "朗头村农家乐里13号民居", lat: 23.352072, lng: 113.075299 },
      { label: "朗头村农家乐里24号民居", lat: 23.352072, lng: 113.075299 },
      { label: "正吉坊康乐里1号民居", lat: 23.073367, lng: 113.407578 },
      { label: "宝源路63号民居", lat: 23.11894, lng: 113.238652 },
      { label: "宝源路70、72号及后座民居", lat: 23.118797, lng: 113.238495 },
      { label: "宝源路73、75号民居", lat: 23.118903, lng: 113.239123 },
      { label: "宝源路85号民居", lat: 23.118864, lng: 113.239756 },
      { label: "豆栏上街12号民居", lat: 23.11201, lng: 113.253006 },
      { label: "桨栏路102号", lat: 23.112203, lng: 113.251176 },
      { label: "桨栏路56号", lat: 23.112324, lng: 113.252252 },
      { label: "丁颖旧居", lat: 23.158908, lng: 113.356424 },
      { label: "华南农学院巢湖路独立住宅", lat: 23.154376, lng: 113.354889 },
      { label: "东昌大街17号之2民居", lat: 23.126451, lng: 113.281192 },
      { label: "东昌大街26、28号民居", lat: 23.126166, lng: 113.281321 },
      { label: "东昌大街34、36号民居", lat: 23.126185, lng: 113.280865 },
      { label: "麦栏街2号民居", lat: 23.118672, lng: 113.270838 },
      { label: "仁生里44号民居", lat: 23.129026, lng: 113.271884 },
      { label: "华安楼", lat: 23.116452, lng: 113.266759 },
      { label: "小东营19号（锦荣街5号民居）", lat: 23.129883, lng: 113.270178 },
      { label: "小东营38号民居", lat: 23.129597, lng: 113.270067 },
      { label: "越华路47号民居", lat: 23.129069, lng: 113.270209 },
      { label: "越秀北路408号民居", lat: 23.134946, lng: 113.274441 },
      { label: "红线女旧居", lat: 23.139514, lng: 113.291351 },
      { label: "詠沂别苑", lat: 23.329836, lng: 113.156881 },
      { label: "张升楼", lat: 22.825229, lng: 113.506211 },
      { label: "黄阁镇猎德上巷1号民居", lat: 22.825829, lng: 113.493671 },
      { label: "黄阁镇猎德上巷3号民居", lat: 22.825829, lng: 113.493671 },
      { label: "黄阁镇大塘西街34号民居", lat: 22.825829, lng: 113.493671 },
      { label: "美友家塾", lat: 22.965933, lng: 113.394927 },
      { label: "朗存家塾", lat: 23.033288, lng: 113.419668 },
      { label: "中约街石狮巷24号民居", lat: 22.98502, lng: 113.397329 },
      { label: "桂桂坊大街九市巷6号民居", lat: 23.020294, lng: 113.360667 },
      { label: "海傍后街78号民居", lat: 22.932232, lng: 113.362852 },
      { label: "耀滔家塾", lat: 22.982491, lng: 113.309122 },
      { label: "启明一马路9号民居", lat: 23.120664, lng: 113.292943 },
      { label: "耀庐", lat: 23.122343, lng: 113.294638 },
      { label: "文德路75号", lat: 23.123689, lng: 113.27144 },
      { label: "保宁路1号民居", lat: 23.11971, lng: 113.301303 },
      { label: "春园后街12号民居", lat: 23.118614, lng: 113.295604 },
      { label: "培正二横路22号民居", lat: 23.119264, lng: 113.298135 },
      { label: "新河浦二横路29号", lat: 23.116688, lng: 113.300661 },
      { label: "新河浦三横路1号民居", lat: 23.116957, lng: 113.29805 },
      { label: "恤孤院路12号民居", lat: 23.118396, lng: 113.296778 },
      { label: "农林上路二横路17、19号民居", lat: 23.125838, lng: 113.298844 },
      { label: "六和新街10、12号民居", lat: 23.121164, lng: 113.273381 },
      { label: "六和新街14号民居", lat: 23.121164, lng: 113.273381 },
      { label: "六和新街1、3号民居", lat: 23.121164, lng: 113.273381 },
      { label: "六和新街2、4号民居", lat: 23.121164, lng: 113.273381 },
      { label: "六和新街6、8号民居", lat: 23.121164, lng: 113.273381 },
      { label: "六和新街9、11号民居", lat: 23.121164, lng: 113.273381 },
      { label: "培真路二巷13号民居", lat: 23.078471, lng: 113.244879 },
      { label: "逢庆中约12、12-1、12-2号民居", lat: 23.114685, lng: 113.236153 },
      { label: "逢源中约22号民居", lat: 23.120473, lng: 113.239308 },
      { label: "多宝坊21、21-1号民居", lat: 23.11555, lng: 113.240172 },
      { label: "恩宁西街16、18号民居", lat: 23.113736, lng: 113.239163 },
      { label: "吉祥坊52号民居", lat: 23.114394, lng: 113.240169 },
      { label: "和平西路134号", lat: 23.112008, lng: 113.240759 },
      { label: "宝源路87号民居", lat: 23.11886, lng: 113.239827 },
      { label: "宝源中约38、38-1、40、40-1号民居", lat: 23.119323, lng: 113.24047 },
      { label: "幸福二巷新街7、9号民居", lat: 23.122639, lng: 113.24388 },
      { label: "小甫园18-1号民居", lat: 23.116845, lng: 113.249957 },
      { label: "西林巷18、20号民居", lat: 23.113434, lng: 113.242773 },
      { label: "和平西路50、50-1、50-2、50-3、50-5、50-6、50-7号民居", lat: 23.111469, lng: 113.244869 },
      { label: "和平中路12~20号（双号）民居", lat: 23.111702, lng: 113.249417 },
      { label: "和平中路66、68、70-1、70号民居", lat: 23.111656, lng: 113.248209 },
      { label: "富善三巷23号民居", lat: 23.113005, lng: 113.248183 },
      { label: "光雅里74、76、78、80号民居", lat: 23.113493, lng: 113.246569 },
      { label: "光雅里82、84、86、88号民居", lat: 23.113479, lng: 113.246371 },
      { label: "十七甫北11号民居", lat: 23.112292, lng: 113.24975 },
      { label: "少昆仑蟾宫女旧居", lat: 23.117033, lng: 113.245246 },
      { label: "李禄超旧居", lat: 23.11568, lng: 113.244396 },
      { label: "德昌堂旧址", lat: 23.112917, lng: 113.246187 },
      { label: "永安公司旧址", lat: 23.114911, lng: 113.249615 },
      { label: "豆栏上街14、16号民居", lat: 23.111348, lng: 113.253055 },
      { label: "扬仁东11、13号民居", lat: 23.113874, lng: 113.251592 },
      { label: "扬仁中13号民居", lat: 23.114821, lng: 113.252172 },
      { label: "和平东路39、41号民居", lat: 23.111798, lng: 113.251313 },
      { label: "和平东路43、45号民居", lat: 23.111689, lng: 113.252204 },
      { label: "和平东路54号民居", lat: 23.111894, lng: 113.25203 },
      { label: "和平东路57号民居", lat: 23.111657, lng: 113.252007 },
      { label: "和平东路61号民居", lat: 23.111646, lng: 113.25192 },
      { label: "和平东路62、64号民居", lat: 23.111877, lng: 113.251884 },
      { label: "和平东路65、67号民居", lat: 23.111627, lng: 113.251833 },
      { label: "豆栏上街5号民居", lat: 23.111888, lng: 113.253394 },
      { label: "故衣街39号民居", lat: 23.111706, lng: 113.252479 },
      { label: "和平中路25、27、29号民居", lat: 23.111485, lng: 113.249433 },
      { label: "沿江西路33号民居", lat: 23.10723, lng: 113.251459 },
      { label: "荣华楼", lat: 23.122026, lng: 113.250132 },
      { label: "龙津东路719-1、719-2、719-3、719-4号民居", lat: 23.12249, lng: 113.249069 },
      { label: "美华后街7-3号民居", lat: 23.143029, lng: 113.23756 },
      { label: "西增路30号民居", lat: 23.143726, lng: 113.239709 },
      { label: "联鹤大街10、10-1号民居", lat: 23.098588, lng: 113.257391 },
      { label: "联鹤大街6号民居", lat: 23.098662, lng: 113.257238 },
      { label: "兴隆新街1号民居", lat: 22.98648, lng: 113.880386 },
       */
      { label: "德和南约18号民居", lat: 23.101627, lng: 113.249685 },
      { label: "洪德四巷27、29号民居", lat: 23.101758, lng: 113.251511 },
      { label: "洪德四巷31、33号民居", lat: 23.101932, lng: 113.251328 },
      { label: "宜兴里9号民居", lat: 23.100076, lng: 113.251973 },
      { label: "基立南街15号民居", lat: 23.102847, lng: 113.275388 },
      { label: "广东省昆虫研究所", lat: 23.092844, lng: 113.294334 },
      { label: "颐乐家塾", lat: 23.182755, lng: 113.522842 },
      { label: "凌希天故居", lat: 23.07133, lng: 113.410196 },
      { label: "深井德星里2号民居", lat: 23.107746, lng: 113.450983 },
      { label: "黄沙塘大村九巷民居", lat: 23.407488, lng: 113.055066 },
      { label: "黄沙塘大村九巷31民居", lat: 23.407488, lng: 113.055066 },
      { label: "新屋庄杨氏孖楼（兄弟）", lat: 23.420194, lng: 113.200926 },
      { label: "杨氏更楼", lat: 23.420194, lng: 113.200926 },
      { label: "洛场村三队民居", lat: 23.410316, lng: 113.256926 },
      { label: "礼耕家塾", lat: 23.342885, lng: 113.091623 },
      { label: "叙伦堂", lat: 22.82582, lng: 113.503299 },
      { label: "新窑村辑瑞堂", lat: 23.369651, lng: 113.82431 },
      { label: "夏街路18号民居", lat: 23.284983, lng: 113.836165 },
      { label: "邓村石屋建筑群", lat: 23.470711, lng: 113.819206 },
      { label: "麻车村宁远楼", lat: 23.144172, lng: 113.828939 },
      { label: "黄屋大戏院", lat: 23.471064, lng: 113.934698 },
      { label: "莲舫家塾", lat: 23.58596, lng: 113.367523 },
      { label: "吕中村司马第", lat: 23.546277, lng: 113.585226 },
      { label: "木棉村德仁公楼", lat: 23.546277, lng: 113.585226 },
      { label: "木棉村墨西楼", lat: 23.546277, lng: 113.585226 },
      { label: "刘氏宗祠敦厚堂", lat: 23.546277, lng: 113.585226 },
      { label: "银林村民居", lat: 23.546277, lng: 113.585226 }

    
    ]
  }
])

/* 建筑信息处理函数 */
// 加载XLSX文件
const loadExcelFile = async () => {
  try {
    processingStatus.value = "正在加载建筑信息数据..."
    
    // 加载XLSX文件
    const response = await fetch("/py/建筑信息.xlsx")
    const arrayBuffer = await response.arrayBuffer()
    const data = new Uint8Array(arrayBuffer)
    
    // 解析工作簿
    const workbook = XLSX.read(data, { type: "array" })
    
    // 获取第一个工作表
    const worksheet = workbook.Sheets[workbook.SheetNames[0]]
    
    // 转换为JSON
    const jsonData = XLSX.utils.sheet_to_json(worksheet)
    
    // 更新数据
    processedData.value = jsonData as any[]
    processingStatus.value = `成功加载 ${jsonData.length} 条建筑信息数据`
    
    return true
  } catch (error) {
    console.error("加载Excel文件失败:", error)
    processingStatus.value = "加载Excel文件失败: " + (error as Error).message
    return false
  }
}

// 导出Excel文件
const exportToExcel = () => {
  if (processedData.value.length === 0) {
    processingStatus.value = "没有可导出的数据"
    return
  }
  
  processingStatus.value = "准备导出Excel..."
  
  try {
    // 创建工作表
    const worksheet = XLSX.utils.json_to_sheet(processedData.value)
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, "建筑信息")
    
    // 导出Excel
    XLSX.writeFile(workbook, "建筑信息.xlsx")
    
    processingStatus.value = `已导出 ${processedData.value.length} 条数据到Excel文件`
  } catch (error) {
    processingStatus.value = "导出失败: " + (error as Error).message
  }
}

// 创建知识图谱可视化
const createKnowledgeGraph = () => {
  if (knowledgeGraphNetwork.value) {
    // 如果已经存在，销毁之前的实例
    knowledgeGraphNetwork.value.destroy()
    knowledgeGraphNetwork.value = null
  }
  
  // 确保DOM元素已经渲染
  if (!graphNetworkContainer.value) { return }
  
  // 根据Excel数据创建知识图谱
  // @ts-ignore
  const nodes = new DataSet()
  // @ts-ignore
  const edges = new DataSet()
  
  // 用于跟踪添加过的节点
  const addedBuildings = new Set()
  const addedCategories = new Set()
  const addedBuildingTypes = new Set()
  
  // 建筑类型提取函数
  const extractBuildingType = (buildingName: string): string => {
    if (buildingName.includes("民居")) { return "民居" }
    if (buildingName.includes("骑楼")) { return "骑楼" }
    if (buildingName.includes("学校") || buildingName.includes("小学") || buildingName.includes("中学") || buildingName.includes("大学")) { return "学校" }
    if (buildingName.includes("祠堂") || buildingName.includes("宗祠")) { return "祠堂" }
    if (buildingName.includes("公园") || buildingName.includes("园林")) { return "园林" }
    if (buildingName.includes("寺庙") || buildingName.includes("庙宇") || buildingName.includes("观音") || buildingName.includes("佛")) { return "寺庙" }
    if (buildingName.includes("教堂") || buildingName.includes("天主") || buildingName.includes("基督")) { return "教堂" }
    if (buildingName.includes("码头") || buildingName.includes("港口")) { return "码头" }
    if (buildingName.includes("桥梁") || buildingName.includes("桥")) { return "桥梁" }
    if (buildingName.includes("楼") && !buildingName.includes("骑楼")) { return "楼宇" }
    if (buildingName.includes("旧址")) { return "旧址" }
    return "其他"
  }
  
  // 处理建筑数据
  processedData.value.forEach((item, index) => {
    const buildingName = item["建筑名称"]
    const address = item["地址"]
    const category = item["类别"]
    
    // 从建筑名称中提取建筑类型标签
    const buildingType = extractBuildingType(buildingName)
    
    // 添加建筑节点
    if (!addedBuildings.has(buildingName)) {
      // 检查是否是选中的建筑，如果是则高亮显示
      const isSelectedBuilding = buildingName === selectedBuildingForKG.value
      
      nodes.add({
        id: `building_${index}`,
        label: buildingName,
        group: "building",
        shape: "dot",
        size: isSelectedBuilding ? 25 : 15,
        color: isSelectedBuilding ? "#FF4757" : "#FECA57",
        font: { 
          color: "black", 
          size: isSelectedBuilding ? 14 : 12,
          face: "DengXian, 等线, sans-serif" 
        },
        title: `<b>${buildingName}</b><br>类别: ${category}<br>类型: ${buildingType}`,
        borderWidth: isSelectedBuilding ? 3 : 1,
        borderColor: isSelectedBuilding ? "#FF3742" : "#FECA57"
      } as any)
      addedBuildings.add(buildingName)
    }
    
    // 添加类别节点 - 增大尺寸
    if (!addedCategories.has(category)) {
      nodes.add({
        id: `category_${category}`,
        label: category,
        group: "category",
        shape: "dot",
        size: 40,
        color: "#96CEB4",
        font: { color: "black", size: 14, face: "DengXian, 等线, sans-serif" }
      } as any)
      addedCategories.add(category)
    }
    
    // 添加建筑类型标签节点
    if (buildingType && !addedBuildingTypes.has(buildingType)) {
      nodes.add({
        id: `type_${buildingType}`,
        label: buildingType,
        group: "buildingType",
        shape: "dot",
        size: 25,
        color: "#FF6B6B",
        font: { color: "black", size: 12, face: "DengXian, 等线, sans-serif" }
      } as any)
      addedBuildingTypes.add(buildingType)
    }
    
    // 添加关系边
    edges.add({
      from: `building_${index}`,
      to: `category_${category}`,
      color: "#cccccc",
      width: 0.5
    } as any)
    
    // 连接建筑到建筑类型标签
    if (buildingType) {
      edges.add({
        from: `building_${index}`,
        to: `type_${buildingType}`,
        color: "#ff9999",
        width: 0.8
      } as any)
    }
  })
  
  
  // 添加三个改造节点和连接关系
  const renovationProjects = [
    {
      id: "renovation_cultural",
      label: "文化展示类改造",
      targetBuilding: "粤赣湘边纵队东江第三支队六团增城人民常备第二大队部旧址",
      description: "改造为文化展示空间"
    },
    {
      id: "renovation_commercial",
      label: "商业空间类改造",
      targetBuilding: "广州啤酒厂麦仓旧址",
      description: "改造为体验馆+餐饮"
    },
    {
      id: "renovation_office",
      label: "创意办公类改造",
      targetBuilding: "珠江电影制片厂行政楼旧址",
      description: "改造为创意办公空间"
    }
  ]
  
  // 添加改造节点
  renovationProjects.forEach(project => {
    nodes.add({
      id: project.id,
      label: project.label,
      group: "renovation",
      shape: "box",
      size: 30,
      color: "#E67E22",
      font: {
        color: "white", 
        size: 12, 
        face: "DengXian, 等线, sans-serif" 
      },
      title: `<b>${project.label}</b><br>${project.description}`,
      borderWidth: 2,
      borderColor: "#D35400"
    } as any)
    
    // 查找目标建筑节点并创建连接
    const allNodes = nodes.get()
    const targetNode = allNodes.find((node: any) => 
      node.group === "building" && node.label === project.targetBuilding
    )
    
    if (targetNode) {
      // 添加改造项目到目标建筑的连接边
      edges.add({
        from: project.id,
        to: targetNode.id,
        color: "#E67E22",
        width: 2,
        label: "改造方案",
        font: { size: 10, color: "#E67E22", face: "DengXian, 等线, sans-serif" },
        arrows: { to: { enabled: true, scaleFactor: 1 } }
      } as any)
    }
  })

  // 配置选项
  const options = {
    nodes: {
      font: {
        size: 12,
        face: "DengXian, 等线, sans-serif"
      },
      shadow: {
        enabled: true,
        color: "rgba(0, 0, 0, 0.5)",
        size: 10,
        x: 5,
        y: 5
      }
    },
    edges: {
      font: {
        size: 10,
        face: "DengXian, 等线, sans-serif"
      },
      arrows: {
        to: { enabled: true, scaleFactor: 0.5 }
      },
      smooth: {
        enabled: true,
        type: "continuous",
        roundness: 0.5
      }
    },
    physics: {
      stabilization: {
        iterations: 100
      },
      barnesHut: {
        gravitationalConstant: -80000,
        centralGravity: 0.3,
        springLength: 250,
        springConstant: 0.001,
        damping: 0.09,
        avoidOverlap: 0.1
      }
    },
    interaction: {
      navigationButtons: false, // 移除导航按钮
      keyboard: true,
      hover: true,
      dragView: true, // 恢复拖动视图
      zoomView: true // 保留缩放功能
    }
  }
    // 创建网络
  const container = graphNetworkContainer.value
  const data = { nodes, edges }
  knowledgeGraphNetwork.value = new Network(container, data, options)
  
  // 如果有选中的建筑，聚焦到该建筑
  if (selectedBuildingForKG.value) {
    // 等待网络稳定后聚焦
    knowledgeGraphNetwork.value.on("stabilizationIterationsDone", function() {
      // 查找选中建筑的节点ID
      const allNodes = nodes.get()
      const selectedNode = allNodes.find((node: any) => 
        node.group === "building" && node.label === selectedBuildingForKG.value
      )
      
      if (selectedNode) {
        // 聚焦到选中的建筑节点
        knowledgeGraphNetwork.value.focus(selectedNode.id, {
          scale: 1.5, // 放大倍数
          animation: {
            duration: 1000,
            easingFunction: "easeInOutQuad"
          }
        })
        
        // 选中该节点
        knowledgeGraphNetwork.value.selectNodes([selectedNode.id])
      }
    })
  }
  
  // 添加事件监听
  // 注释掉KG内部悬浮窗功能 - 暂时不用
}

// 当对话框显示时创建知识图谱
watch(showKnowledgeGraphDialog, (newVal) => {
  if (newVal && processedData.value.length > 0) {
    // 使用nextTick确保DOM已更新
    nextTick(() => {
      createKnowledgeGraph()
    })
  }
})

// 页面加载时自动获取数据，但隐藏状态信息
onMounted(async () => {
  // 静默加载Excel数据用于知识图谱
  try {
    const response = await fetch("/py/建筑信息.xlsx")
    const arrayBuffer = await response.arrayBuffer()
    const data = new Uint8Array(arrayBuffer)
    
    // 解析工作簿
    const workbook = XLSX.read(data, { type: "array" })
    
    // 获取第一个工作表
    const worksheet = workbook.Sheets[workbook.SheetNames[0]]
    
    // 转换为JSON
    const jsonData = XLSX.utils.sheet_to_json(worksheet)
    
    // 更新数据，但不显示状态信息
    processedData.value = jsonData as any[]
  } catch (error) {
    console.error("加载Excel文件失败:", error)
  }
})

/** ECharts 容器 */
const pieChartContainer = ref(null)
const barChartContainer = ref(null)
/** 跟踪选中的类别索引 */
const selectedCategoryIndex = ref(null)
/** 选中建筑的图片 */
const selectedBuildingImage = ref<string[]>([]) // 改为数组

const ChatboximageInput = document.getElementById("ChatboximageInput")
const ChatboxuploadButton = document.getElementById("ChatboxuploadButton")
const ChatboxfileName = document.getElementById("ChatboxfileName")
/** 选中的建筑 */
const selectedBuilding = ref<{ label: string; lat: number; lng: number } | null>(null)

// 根据选中建筑计算要显示的关键词图片
const currentKeywordsImage = computed(() => {
  if (!selectedBuilding.value) {
    return "/src/GXcloud.png" // 默认显示GX关键词云
  }
  
  const buildingName = selectedBuilding.value.label
  
  // 特定建筑对应特定关键词图片
  if (buildingName === "粤赣湘边纵队东江第三支队六团增城人民常备第二大队部旧址") {
    return "/src/Keywordsred.png"
  } else if (buildingName === "广州啤酒厂麦仓旧址") {
    return "/src/Keywordsbeer.png"
  }
  
  // 对于GX Buildings，显示GX关键词云
  const buildingCategory = findBuildingCategory(selectedBuilding.value, coordinates.value)
  if (buildingCategory === "GX Buildings") {
    return "/src/GXcloud.png"
  }
  
  // 其他建筑的默认情况
  return showKeywords3.value ? "/src/Keywords3.png" : "/src/Keywords2.png"
})
/** 选中的建筑描述 */
const selectedBuildingDescription = ref<string | null>(null)
const selectedBuildingYear = ref<string>("")
const selectedBuildingStructure = ref<string>("")
const selectedBuildingCity = ref<string>("")

/** 获取建筑年份对应的颜色和样式 */
const getBuildingYearStyle = (buildYear: string) => {
  if (!buildYear) return { color: "#666", background: "#f5f5f5", borderColor: "#ddd" }
  
  // 定义年份颜色方案 - 简洁大气
  const yearColors = {
    "明（1368-1644年）及明代以前": { color: "#8B4513", background: "#FFF8DC", borderColor: "#DEB887" }, // 古铜色
    "清（1644-1911年）": { color: "#2F4F4F", background: "#E0FFFF", borderColor: "#87CEEB" }, // 深青色
    "民国（1911-1949年）": { color: "#B22222", background: "#FFE4E1", borderColor: "#F08080" }, // 火砖红
    "建国后（1949-1978年）": { color: "#8B0000", background: "#FFEBEE", borderColor: "#FF8A80" }, // 深红色
    "1949-1979年": { color: "#8B0000", background: "#FFEBEE", borderColor: "#FF8A80" }, // 深红色 (同上)
    "1980年以后": { color: "#4169E1", background: "#F0F8FF", borderColor: "#87CEFA" } // 皇家蓝
  }
  
  // 匹配年份范围
  for (const [period, style] of Object.entries(yearColors)) {
    if (buildYear.includes(period) || buildYear === period) {
      return style
    }
  }
  
  // 默认样式
  return { color: "#666", background: "#f9f9f9", borderColor: "#e0e0e0" }
}

/** 获取年份简化显示文本 */
const getSimplifiedYear = (buildYear: string) => {
  if (!buildYear) return "未知年代"
  
  const yearMap = {
    "明（1368-1644年）及明代以前": "明代及以前",
    "清（1644-1911年）": "清代",
    "民国（1911-1949年）": "民国",
    "建国后（1949-1978年）": "建国后",
    "1949-1979年": "建国后",
    "1980年以后": "改革开放后"
  }
  
  for (const [period, simple] of Object.entries(yearMap)) {
    if (buildYear.includes(period) || buildYear === period) {
      return simple
    }
  }
  
  return buildYear
}

/** 获取建筑结构类型对应的颜色和样式 */
const getBuildingStructureStyle = (structureType: string) => {
  if (!structureType) return { color: "#666", background: "#f5f5f5", borderColor: "#ddd" }
  
  // 定义结构类型颜色方案 - 简洁大气
      const structureColors = {
      砖木结构: { color: "#8B4513", background: "#FDF5E6", borderColor: "#D2B48C" }, // 棕色系 - 传统木色
      砖混结构: { color: "#2F4F4F", background: "#F0F8FF", borderColor: "#B0C4DE" }, // 深蓝灰 - 现代混凝土
      钢混结构: { color: "#708090", background: "#F8F8FF", borderColor: "#C0C0C0" }, // 钢灰色 - 钢筋混凝土  
      木结构: { color: "#8FBC8F", background: "#F0FFF0", borderColor: "#90EE90" }, // 绿色系 - 自然木材
      砖石结构: { color: "#A0522D", background: "#FFF8DC", borderColor: "#DEB887" }, // 土黄色 - 砖石
      混合结构: { color: "#9932CC", background: "#F8F0FF", borderColor: "#DDA0DD" }, // 紫色系 - 混合材料
      其他: { color: "#696969", background: "#F5F5F5", borderColor: "#D3D3D3" } // 灰色系 - 其他类型
    }
  
  // 匹配结构类型
  for (const [type, style] of Object.entries(structureColors)) {
    if (structureType.includes(type) || structureType === type) {
      return style
    }
  }
  
  // 默认样式
  return { color: "#666", background: "#f9f9f9", borderColor: "#e0e0e0" }
}

/** 获取结构类型简化显示文本 */
const getSimplifiedStructure = (structureType: string) => {
  if (!structureType) return "未知结构"
  
  // 直接返回原始结构类型，因为通常已经比较简洁
  return structureType
}

/** 获取GX Buildings基于城市的标记颜色 */
const getGXBuildingMarkerColor = async (buildingName: string) => {
  // 默认红色 (原来的颜色)
  const defaultColor = "#ff0000"
  
  try {
    // 尝试获取建筑的JSON数据
    const jsonFileName = `${buildingName}.json`
    const descriptionJsonPath = `/buildingDescriptions/${encodeURIComponent(jsonFileName)}`
    const response = await fetch(descriptionJsonPath)
    
    if (response.ok) {
      const data = await response.json()
      const city = data.city || ""
      
              const cityColors = {
  北海市: "#FDD8A3", // 海滨 → 柔和米黄
  防城港市: "#79C5BE", // 港口 → 青绿色
  钦州市: "#C4FFB5", // 钦州 → 浅嫩绿
  南宁市: "#98D8C8", // 保留薄荷绿
  桂林市: "#FDF4A7", // 山水 → 浅黄色
  柳州市: "#7FA4CA", // 柳州 → 蓝紫
  百色市: "#EEFEAC", // 革命老区 → 柔和浅黄绿
  玉林市: "#D7FEB0", // 玉林 → 浅绿色
  贵港市: "#8190CC", // 贵港 → 蓝紫
  来宾市: "#8C84CF", // 来宾 → 紫色
  贺州市: "#AD85C6", // 保留薰衣草紫
  河池市: "#7CB8C7", // 河池 → 湖蓝
  崇左市: "#FDD8A3", // 原红色 → 柔和米黄，避免突兀
  梧州市: "#E26A30"
}


      // 根据城市返回对应颜色
      return cityColors[city] || defaultColor
    }
  } catch (error) {
    console.log(`无法获取 ${buildingName} 的城市信息，使用默认颜色`)
  }
  
  return defaultColor
}

/** 创建基于颜色的SVG标记图标 */
const createColoredMarkerIcon = (color: string) => {
  const svgIcon = `
    <svg width="29" height="29" viewBox="0 0 29 29" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur in="SourceAlpha" stdDeviation="2"/>
          <feOffset dx="1" dy="1" result="offset"/>
          <feComponentTransfer>
            <feFuncA type="linear" slope="0.3"/>
          </feComponentTransfer>
          <feMerge> 
            <feMergeNode/>
            <feMergeNode in="SourceGraphic"/> 
          </feMerge>
        </filter>
      </defs>
      <circle cx="14.5" cy="14.5" r="10.8" fill="${color}" stroke="rgba(255, 255, 255, 0.5)" stroke-width="1" filter="url(#shadow)"/>
    </svg>
  `
  
  // 转换为Data URL
  const dataUrl = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svgIcon)))
  return dataUrl
}

/** 获取GX建筑城市对应的样式 */
const getGXBuildingCityStyle = (city: string) => {
  const cityColors = {
    北海市: "#FDD8A3", // 海滨 → 柔和米黄
    防城港市: "#79C5BE", // 港口 → 青绿色
    钦州市: "#C4FFB5", // 钦州 → 浅嫩绿
    南宁市: "#98D8C8", // 保留薄荷绿
    桂林市: "#FDF4A7", // 山水 → 浅黄色
    柳州市: "#7FA4CA", // 柳州 → 蓝紫
    百色市: "#EEFEAC", // 革命老区 → 柔和浅黄绿
    玉林市: "#D7FEB0", // 玉林 → 浅绿色
    贵港市: "#8190CC", // 贵港 → 蓝紫
    来宾市: "#8C84CF", // 来宾 → 紫色
    贺州市: "#AD85C6", // 保留薰衣草紫
    河池市: "#7CB8C7", // 河池 → 湖蓝
    崇左市: "#FDD8A3", // 原红色 → 柔和米黄，避免突兀
    梧州市: "#E26A30"
  }
  
  const color = cityColors[city] || "#ff0000" // 默认红色
  return {
    color: "#333", // 深色文字便于阅读
    background: color,
    borderColor: color
  }
}

/** 创建彩色圆形图标用于building-category显示 */
const createColoredDotIcon = (color: string, size: number = 20) => {
  const svgIcon = `
    <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
      <circle cx="${size / 2}" cy="${size / 2}" r="${size / 2 - 1}" fill="${color}" stroke="#fff" stroke-width="1"/>
    </svg>
  `
  
  // 转换为Data URL
  const dataUrl = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svgIcon)))
  return dataUrl
}

/** 获取GX建筑城市对应的颜色 */
const getGXBuildingCityColor = (city: string) => {
  const cityColors = {
    北海市: "#FDD8A3", // 海滨 → 柔和米黄
    防城港市: "#79C5BE", // 港口 → 青绿色
    钦州市: "#C4FFB5", // 钦州 → 浅嫩绿
    南宁市: "#98D8C8", // 保留薄荷绿
    桂林市: "#FDF4A7", // 山水 → 浅黄色
    柳州市: "#7FA4CA", // 柳州 → 蓝紫
    百色市: "#EEFEAC", // 革命老区 → 柔和浅黄绿
    玉林市: "#D7FEB0", // 玉林 → 浅绿色
    贵港市: "#8190CC", // 贵港 → 蓝紫
    来宾市: "#8C84CF", // 来宾 → 紫色
    贺州市: "#AD85C6", // 保留薰衣草紫
    河池市: "#7CB8C7", // 河池 → 湖蓝
    崇左市: "#FDD8A3", // 原红色 → 柔和米黄，避免突兀
    梧州市: "#E26A30"
  }
  
  return cityColors[city] || "#ff0000" // 默认红色
}

/** 关键词列表 */
const keywordsList = ref<{text: string, count: number, left?: string, top?: string, rotate?: number, vertical?: boolean}[]>([])
/** 控制右侧详情弹窗 */
const showDetailModal = ref(false)
/** 地图上所有 Marker */
const markers = ref<CustomMarker[]>([])
/** 用户输入 & 消息列表 */
const userInput = ref("")
const chatMessages = ref<string[]>([])
/** 主题搜索结果 */
const themeSearchResults = ref<any[]>([])
/** 图表中被"置灰"的类别列表 */
const selectedCategoriesChart = ref<string[]>([])
/** 原x 轴短名 <-> 长名 映射（已注释） */
// const selectedDistricts = ref<string[]>([])

/** 新增筛选变量 */
const selectedYearPeriods = ref<string[]>([]) // 选中的年代
const selectedCities = ref<string[]>([]) // 选中的城市

/** 原筛选变量（已注释，保留备用） */
const selectedDistricts = ref<string[]>([]) // 原行政区筛选
const shortToLongMapping: Record<string, string> = {
  Commercial: "Commercial Buildings",
  Industrial: "Industrial Buildings",
  Military: "Military Buildings",
  Public: "Public Buildings",
  Religious: "Religious Buildings",
  Residential: "Residential Buildings"
}

/** 地图悬浮信息 */
const hoveredBuilding = ref<{ label: string; lat: number; lng: number } | null>(null)
const hoveredBuildingDescription = ref<string>("")
const hoveredBuildingYear = ref<string>("")
const hoveredBuildingStructure = ref<string>("")
const hoveredBuildingCity = ref<string>("")
/** 选中类别（用于控制地图上是否灰掉 Marker） */
const selectedCategories = ref<string[]>(
  coordinates.value.map((category) => category.label) // 默认全部选中
)
/** coordinate-list 用的选中存储 */
const selectedCategoriesList = ref<string[]>([])
/** 浮动窗口样式 */
const floatingWindowStyle = ref({
  position: "absolute" as const,
  top: "30px",
  left: "calc(100% - 290px)",
  zIndex: 9999,
  backgroundColor: "#fff",
  padding: "15px",
  borderRadius: "10px",
  boxShadow: "0 2px 8px rgba(0, 0, 0, 0.2)",
  maxHeight: "550px",
  maxWidth: "500px",
  overflowY: "hidden" as const,
  wordWrap: "break-word" as const,
  lineHeight: "1.2"
})

/* =========================================
 * 4. 所有函数定义
 * ========================================= */

/** 图片加载失败的处理 */
const onImageError = (index: number) => {
  selectedBuildingImage.value.splice(index, 1, "https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png")
}

/** 更新浮动窗口位置 */
const updateFloatingWindowPosition = (latLng: L.LatLng) => {
  const point = map.latLngToContainerPoint(latLng) // 获取建筑物的屏幕坐标
  floatingWindowStyle.value.top = `${point.y - 210}px`
  floatingWindowStyle.value.left = `${point.x + 500}px`
  floatingWindowStyle.value.zIndex = 6
}

/** 根据 label 返回对应的图标路径 */
function getIconUrlByLabel(label: string, isGray = false): string {
  switch (label) {
    case "Commercial Buildings":
      return isGray ? "gray.ico" : "blue.ico"
    case "Industrial Buildings":
      return isGray ? "gray.ico" : "yellow.ico"
    case "Military Buildings":
      return isGray ? "gray.ico" : "red.ico"
    case "Public Buildings":
      return isGray ? "gray.ico" : "pink.ico"
    case "Religious Buildings":
      return isGray ? "gray.ico" : "orange.ico"
    case "Residential Buildings":
      return isGray ? "gray.ico" : "green.ico"
    default:
      return isGray ? "gray.ico" : "red.ico"
  }
}

/** 在坐标列表中查找建筑所属的类别 */
function findBuildingCategory(building, coordinates) {
  for (const category of coordinates) {
    const found = category.items.find((item) => item.label === building.label)
    if (found) {
      return category.label
    }
  }
  return "Unknown Category"
}

/** 动态获取建筑图片列表 */
const getBuildingImages = async (buildingLabel: string, buildingCategory: string): Promise<string[]> => {
  // 为兰圃建筑特殊处理（因为文件名不规范）
  if (buildingLabel === "兰圃") {
    return [
      `/buildingPic/public_buildings/兰圃/0.png`,
      `/buildingPic/public_buildings/兰圃/2.png`,
      `/buildingPic/public_buildings/兰圃/3.png`,
      `/buildingPic/public_buildings/兰圃/u=1645659605,572011017&fm=253&app=138&f=JPEG.jpg`,
      `/buildingPic/public_buildings/兰圃/u=1993817016,2233430189&fm=253&app=138&f=JPEG.jpg`,
      `/buildingPic/public_buildings/兰圃/u=2416644976,2348204302&fm=253&app=138&f=JPEG.jpg`,
      `/buildingPic/public_buildings/兰圃/u=2686393133,933280446&fm=253&app=138&f=JPEG.jpg`,
      `/buildingPic/public_buildings/兰圃/u=2811305362,513849778&fm=253&app=138&f=JPEG.jpg`,
      `/buildingPic/public_buildings/兰圃/u=3092559651,3647505292&fm=3074&app=3074&f=JPEG.jpg`,
      `/buildingPic/public_buildings/兰圃/u=3617778192,4234437083&fm=253&fmt=auto&app=138&f=JPEG.webp`
    ]
  }
  
  // 其他建筑使用标准命名规则，但支持多种格式
  const categoryPath = buildingCategory.toLowerCase().replace(" ", "_")
  const labelPath = buildingLabel.replace(" ", "_")
  const folderPath = `/buildingPic/${categoryPath}/${labelPath}`
  
  // 并行检查所有图片格式
  const imagePromises = []
  for (let index = 1; index <= 10; index++) {
    imagePromises.push(getFirstAvailableImageForBuilding(folderPath, labelPath, index))
  }
  
  const resolvedImages = await Promise.all(imagePromises)
  return resolvedImages
}

/** 获取普通建筑的第一个可用图片格式 */
const getFirstAvailableImageForBuilding = async (folderPath: string, labelPath: string, index: number): Promise<string> => {
  const supportedFormats = ["jpg", "jpeg", "png", "webp", "gif", "bmp"]
  
  for (const format of supportedFormats) {
    const imagePath = `${folderPath}/${labelPath}_${index}.${format}`
    const exists = await checkImageExists(imagePath)
    if (exists) {
      return imagePath
    }
  }
  
  // 如果没有找到任何格式，返回默认jpg路径
  return `${folderPath}/${labelPath}_${index}.jpg`
}

/** 检查图片URL是否可访问 */
const checkImageExists = async (url: string): Promise<boolean> => {
  return new Promise((resolve) => {
    const img = new Image()
    img.onload = () => resolve(true)
    img.onerror = () => resolve(false)
    img.src = url
  })
}

/** 获取第一个可用的图片格式 */
const getFirstAvailableImage = async (folderPath: string, index: number): Promise<string> => {
  const supportedFormats = ["jpg", "jpeg", "png", "webp", "gif", "bmp"]
  
  for (const format of supportedFormats) {
    const imagePath = `${folderPath}/${index}.${format}`
    const exists = await checkImageExists(imagePath)
    if (exists) {
      return imagePath
    }
  }
  
  // 如果没有找到任何格式，返回默认jpg路径
  return `${folderPath}/${index}.jpg`
}

const getGXBuildingImages = async (buildingLabel: string): Promise<string[]> => {
  // 新的基础路径：使用image文件夹
  const folderPath = `/GXbuildingsData/image/${buildingLabel}`
  
  const images = []
  
  // 并行检查所有图片
  const imagePromises = []
  for (let i = 1; i <= 5; i++) {
    imagePromises.push(getFirstAvailableImage(folderPath, i))
  }
  
  const resolvedImages = await Promise.all(imagePromises)
  images.push(...resolvedImages)
  
  console.log(`为GX建筑 "${buildingLabel}" 生成图片路径:`, images)
  return images
}

/** 初始化 Mars2D 地图 */
function initMars3d(option: any) {
  // 移除硬编码的center，让config.json中的配置生效
  const defaultOptions = {
    zoom: 7 // 只保留默认缩放级别
  }
  const finalOptions = { ...defaultOptions, ...option }
  
  // 如果config.json中有center配置，转换为L.LatLng格式
  if (finalOptions.center && finalOptions.center.lat && finalOptions.center.lng) {
    finalOptions.center = new L.LatLng(finalOptions.center.lat, finalOptions.center.lng)
  }
  
  map = new mars2d.Map(withKeyId.value, finalOptions)
  onMapLoad()
  emit("onload", map)
}

/** 地图加载完成后的逻辑 */
function onMapLoad() {
  // 地图加载完成后的逻辑
}

/** 地图组件销毁前回收资源 */
onBeforeUnmount(() => {
  if (map) {
    map.destroy()
    map = null
  }
  console.log("map销毁完成", map)
})

/** 生成随机位置和旋转 */
const generateWordCloudData = () => {
  const baseKeywords = [
    { text: "第一批", count: 35 },
    { text: "民居", count: 32 },
    { text: "旧址", count: 30 },
    { text: "风景区", count: 25 },
    { text: "骑楼", count: 23 },
    { text: "大街", count: 20 },
    { text: "酒店", count: 18 },
    { text: "文化", count: 16 },
    { text: "学校", count: 15 },
    { text: "西路", count: 14 },
    { text: "东路", count: 13 },
    { text: "门楼", count: 12 },
    { text: "学院", count: 11 },
    { text: "书院", count: 10 },
    { text: "博物馆", count: 9 },
    { text: "宾馆", count: 8 },
    { text: "展览馆", count: 7 },
    { text: "交易会", count: 6 },
    { text: "南路", count: 5 },
    { text: "华南", count: 4 }
  ]
  
  // 词云布局算法 - 模拟图片中的效果
  // 先按词频排序
  const sortedKeywords = [...baseKeywords].sort((a, b) => b.count - a.count)
  
  // 定义大致的活动区域，给整体词云留出边距
  const layoutArea = {
    minX: 5,
    maxX: 95,
    minY: 5,
    maxY: 95
  }
  
  // 中心区域，重要词语会出现在这里
  const centerArea = {
    minX: 30,
    maxX: 70,
    minY: 30,
    maxY: 70
  }
  
  // 按照词频大小分组
  const highFrequencyWords = sortedKeywords.slice(0, 5) // 最重要的词
  const mediumFrequencyWords = sortedKeywords.slice(5, 12) // 中等重要的词
  const lowFrequencyWords = sortedKeywords.slice(12) // 其余词语
  
  // 定义不同重要程度词语的颜色组
  const colorGroups = {
    high: ["#FFC107", "#FF9800", "#FF5722"], // 黄色、橙色
    medium: ["#03A9F4", "#00BCD4", "#4DD0E1"], // 蓝色系
    low: ["#0D47A1", "#1565C0", "#1976D2"] // 深蓝色系
  }
  
  // 处理所有词语的位置和样式
  const processedWords = []
  
  // 处理高频词 - 放在中心位置，较大字体，旋转幅度小
  highFrequencyWords.forEach(word => {
    const x = centerArea.minX + Math.random() * (centerArea.maxX - centerArea.minX)
    const y = centerArea.minY + Math.random() * (centerArea.maxY - centerArea.minY)
    // 中心词语旋转角度较小
    const rotation = Math.random() * 50 - 25 // -25到25度之间
    const colorIndex = Math.floor(Math.random() * colorGroups.high.length)
    
    processedWords.push({
      ...word,
      left: x + "%",
      top: y + "%",
      color: colorGroups.high[colorIndex],
      rotation: rotation
    })
  })
  
  // 处理中频词 - 分布在中心周围，中等字体，旋转幅度适中
  mediumFrequencyWords.forEach(word => {
    let x, y
    
    // 50%概率将中频词也放在中心区域
    if (Math.random() < 0.5) {
      x = centerArea.minX + Math.random() * (centerArea.maxX - centerArea.minX)
      y = centerArea.minY + Math.random() * (centerArea.maxY - centerArea.minY)
    } else {
      // 其余放在中心区域周围
      x = layoutArea.minX + Math.random() * (layoutArea.maxX - layoutArea.minX)
      y = layoutArea.minY + Math.random() * (layoutArea.maxY - layoutArea.minY)
      
      // 避开正中心
      while (x > centerArea.minX && x < centerArea.maxX && y > centerArea.minY && y < centerArea.maxY) {
        x = layoutArea.minX + Math.random() * (layoutArea.maxX - layoutArea.minX)
        y = layoutArea.minY + Math.random() * (layoutArea.maxY - layoutArea.minY)
      }
    }
    
    // 中频词语旋转角度适中
    const rotation = Math.random() * 70 - 35 // -35到35度之间
    const colorIndex = Math.floor(Math.random() * colorGroups.medium.length)
    
    processedWords.push({
      ...word,
      left: x + "%",
      top: y + "%",
      color: colorGroups.medium[colorIndex],
      rotation: rotation
    })
  })
  
  // 处理低频词 - 分布在外围，较小字体，旋转幅度大
  lowFrequencyWords.forEach(word => {
    const x = layoutArea.minX + Math.random() * (layoutArea.maxX - layoutArea.minX)
    const y = layoutArea.minY + Math.random() * (layoutArea.maxY - layoutArea.minY)
    
    // 低频词语旋转角度较大
    const rotation = Math.random() * 90 - 45 // -45到45度之间
    const colorIndex = Math.floor(Math.random() * colorGroups.low.length)
    
    processedWords.push({
      ...word,
      left: x + "%",
      top: y + "%",
      color: colorGroups.low[colorIndex],
      rotation: rotation
    })
  })
  
  return processedWords
}

/** 全局关键词数据 */
const commonKeywords = generateWordCloudData()

/** 从文本中提取关键词并计算频率 */
const extractKeywords = (text: string) => {
  if (!text) { return commonKeywords }
  
  // 预处理文本：去除标点符号，转为小写
  const cleanedText = text.replace(/[.,，。、；：""！？《》()（）【】]/g, " ").toLowerCase()
  
  // 停用词列表（常见的无意义词汇）
  const stopWords = [
    "的", "是", "在", "了", "和", "与", "这", "那", "有", "为", "以", "于",
    "及", "等", "之", "对", "由", "也", "被", "到", "从", "或", "所", "并",
    "且", "而", "但", "个", "地", "位于", "广州市", "广东省", "属于", "历史建筑",
    "位", "区", "内", "号", "第", "批", "一", "二", "三", "四", "五", "六", "七", "八",
    "宾馆", "建筑", "大楼", "广州"
  ]
  
  // 分词（简单按空格和中文字符拆分）
  const words = cleanedText.split(/[\s]+|(?=[\u4e00-\u9fa5])/g)
    .filter(word => word.trim().length > 1) // 过滤掉长度小于2的词
    .filter(word => !stopWords.includes(word)) // 过滤掉停用词
  
  // 统计词频
  const wordFreq: Record<string, number> = {}
  words.forEach(word => {
    if (word in wordFreq) {
      wordFreq[word]++
    } else {
      wordFreq[word] = 1
    }
  })
  
  // 转换为数组并排序
  const sortedWords = Object.keys(wordFreq)
    .map(word => ({ text: word, count: wordFreq[word] }))
    .sort((a, b) => b.count - a.count)
  
  // 取前15-20个词
  return sortedWords.slice(0, 20)
}

/** 根据词频计算字体大小 */
const calculateFontSize = (count: number) => {
  // 调整字体大小范围，保持层次感但不过于极端
  const minSize = 14
  const maxSize = 26
  const minCount = 4
  const maxCount = 35
  
  // 将count映射到0-1范围
  const normalized = Math.min(Math.max((count - minCount) / (maxCount - minCount), 0), 1)
  // 使用稍缓和的指数增长，保持差异但避免过大差距
  const exponential = Math.pow(normalized, 1.2)
  // 映射回字体大小范围
  return minSize + exponential * (maxSize - minSize)
}

/** 根据词频计算字体粗细 */
const calculateFontWeight = (count: number) => {
  // 词频越高字体越粗
  if (count > 25) { return "900" }
  if (count > 15) { return "700" }
  if (count > 10) { return "bold" }
  if (count > 5) { return "500" }
  return "normal"
}

/** 根据词频计算透明度 */
const calculateOpacity = (count: number) => {
  // 词频越高透明度越高
  const minCount = 4
  const maxCount = 35
  const minOpacity = 0.65
  const maxOpacity = 1
  
  // 映射到透明度范围
  const normalized = Math.min(Math.max((count - minCount) / (maxCount - minCount), 0), 1)
  return minOpacity + normalized * (maxOpacity - minOpacity)
}

/** 获取随机颜色 */
const getRandomColor = (index: number) => {
  // 使用更多的颜色，增加渐变效果
  const colors = [
    "#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
    "#EDC948", "#B07AA1", "#FF9DA7", "#9D755D", "#BAB0AC",
    "#8DD3C7", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462",
    "#B3DE69", "#FCCDE5", "#BC80BD", "#CCEBC5", "#FFED6F"
  ]
  
  // 如果是最重要的几个词，使用固定的醒目颜色
  if (index < 5) {
    return ["#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00"][index]
  }
  
  return colors[index % colors.length]
}



/** 更新地图上各 Marker 的可见性（置灰与否） */
const updateMarkersVisibility = () => {
  markers.value.forEach((marker) => {
    const markerCategory = marker.category
    const isSelected = selectedCategories.value.length === 0 || selectedCategories.value.includes(markerCategory)
    const newIconUrl = isSelected ? getIconUrlByLabel(markerCategory) : getIconUrlByLabel(markerCategory, true)

    const newIcon = L.icon({
      iconUrl: newIconUrl,
      iconSize: [32, 32],
      iconAnchor: [16, 32]
    })
    marker.setIcon(newIcon)

    // 设置 zIndexOffset，使选中类别的标记位于上层
    marker.setZIndexOffset(isSelected ? 1000 : 0)
  })
}
/** === 原建筑类别筛选逻辑（已注释） === */
// const toggleCategory = (categoryLabel: string) => {
//   console.log("toggleCategory调用:", categoryLabel)
//   if (selectedCategories.value.includes(categoryLabel)) {
//     // 如果已经选中该类别，取消选择该类别
//     const index = selectedCategories.value.indexOf(categoryLabel)
//     selectedCategories.value.splice(index, 1)
//     console.log("取消选择类别:", categoryLabel)
//   } else {
//     // 选择该类别，保持其他已选择的类别
//     selectedCategories.value.push(categoryLabel)
//     console.log("选择类别:", categoryLabel)
//   }
//   console.log("当前选中类别:", selectedCategories.value)
//   console.log("当前选中行政区:", selectedDistricts.value)
//   
//   // 使用统一的筛选函数
//   updateMarkersVisibilityByBoth()
//   updateChartBarColors()
// }

/** 新增年代筛选函数 */
const toggleYearPeriod = async (yearPeriod: string) => {
  console.log("toggleYearPeriod调用:", yearPeriod)
  
  // 添加过渡动画效果 - 现在年代筛选对应饼图
  const pieChartInstance = echarts.getInstanceByDom(pieChartContainer.value as HTMLDivElement)
  if (pieChartInstance) {
    // 显示加载状态
    pieChartInstance.showLoading({
      text: "筛选中...",
      color: "#4fc3f7",
      textColor: "#333",
      maskColor: "rgba(255, 255, 255, 0.8)",
      zlevel: 0,
      fontSize: 10,
      showSpinner: true,
      spinnerRadius: 10,
      lineWidth: 3
    })
    
    // 先显示选中状态的临时反馈
    setTimeout(() => {
      pieChartInstance.hideLoading()
      const yearIndex = ["明代及以前", "清代", "民国", "建国后", "改革开放后", "现代"].indexOf(yearPeriod)
      if (yearIndex !== -1) {
        pieChartInstance.dispatchAction({
          type: "highlight",
          seriesIndex: 0,
          dataIndex: yearIndex
        })
      }
    }, 100)
  }
  
  if (selectedYearPeriods.value.includes(yearPeriod)) {
    // 如果已经选中该年代，取消选择
    const index = selectedYearPeriods.value.indexOf(yearPeriod)
    selectedYearPeriods.value.splice(index, 1)
    console.log("取消选择年代:", yearPeriod)
  } else {
    // 选择该年代
    selectedYearPeriods.value.push(yearPeriod)
    console.log("选择年代:", yearPeriod)
  }
  console.log("当前选中年代:", selectedYearPeriods.value)
  
  // 延迟执行更新，让用户看到反馈效果
  setTimeout(async () => {
    // 调用统一筛选更新函数
    await updateMarkersVisibilityByYearAndCity()
    updateChartColors()
    
    // 取消高亮
    if (pieChartInstance) {
      pieChartInstance.dispatchAction({
        type: "downplay",
        seriesIndex: 0
      })
    }
  }, 300)
}

/** === 原行政区筛选逻辑（已注释） === */
// const toggleDistrict = (districtName: string) => {
//   console.log("toggleDistrict调用:", districtName)
//   if (selectedDistricts.value.includes(districtName)) {
//     // 如果已经选中该行政区，取消选择该行政区
//     const index = selectedDistricts.value.indexOf(districtName)
//     selectedDistricts.value.splice(index, 1)
//     console.log("取消选择行政区:", districtName)
//   } else {
//     // 选择该行政区，保持其他已选择的行政区
//     selectedDistricts.value.push(districtName)
//     console.log("选择行政区:", districtName)
//   }
//   console.log("当前选中行政区:", selectedDistricts.value)
//   console.log("当前选中类别:", selectedCategories.value)
//   
//   // 使用统一的筛选函数
//   updateMarkersVisibilityByBoth()
//   updateChartPieColors()
// }

/** 新增城市筛选函数 */
const toggleCity = async (cityName: string) => {
  console.log("toggleCity调用:", cityName)
  
  // 添加过渡动画效果 - 现在城市筛选对应柱状图
  const barChartInstance = echarts.getInstanceByDom(barChartContainer.value as HTMLDivElement)
  if (barChartInstance) {
    // 显示加载状态
    barChartInstance.showLoading({
      text: "筛选中...",
      color: "#81c784",
      textColor: "#333",
      maskColor: "rgba(255, 255, 255, 0.8)",
      zlevel: 0,
      fontSize: 12,
      showSpinner: true,
      spinnerRadius: 10,
      lineWidth: 3
    })
    
    // 找到对应城市的数据索引
    const cityIndex = ["北海市", "防城港市", "钦州市", "南宁市", "桂林市", "柳州市", "梧州市", "百色市", "玉林市", "贵港市", "来宾市", "贺州市", "河池市", "崇左市"].indexOf(cityName)
    
    setTimeout(() => {
      barChartInstance.hideLoading()
      if (cityIndex !== -1) {
        // 先显示选中状态的临时反馈
        barChartInstance.dispatchAction({
          type: "highlight",
          seriesIndex: 0,
          dataIndex: cityIndex
        })
      }
    }, 100)
  }
  
  if (selectedCities.value.includes(cityName)) {
    // 如果已经选中该城市，取消选择
    const index = selectedCities.value.indexOf(cityName)
    selectedCities.value.splice(index, 1)
    console.log("取消选择城市:", cityName)
  } else {
    // 选择该城市
    selectedCities.value.push(cityName)
    console.log("选择城市:", cityName)
  }
  console.log("当前选中城市:", selectedCities.value)
  
  // 延迟执行更新，让用户看到反馈效果
  setTimeout(async () => {
    // 调用统一筛选更新函数
    await updateMarkersVisibilityByYearAndCity()
    updateChartColors()
    
    // 取消高亮
    if (barChartInstance) {
      barChartInstance.dispatchAction({
        type: "downplay",
        seriesIndex: 0
      })
    }
  }, 300)
}

/** === 原筛选更新函数（已注释） === */
/** 根据行政区筛选更新地图标记可见性 */
/** 统一的重叠筛选函数：同时考虑行政区和建筑类型 */
// const updateMarkersVisibilityByBoth = () => {
//   console.log("=== 开始重叠筛选 ===")
//   console.log("选中的行政区:", selectedDistricts.value)
//   console.log("选中的建筑类型:", selectedCategories.value)
//   
//   // 定义广州各行政区的地理坐标范围
//   const districtBounds: { [key: string]: { north: number, south: number, east: number, west: number } } = {
//     Tianhe: { north: 23.2, south: 23.08, east: 113.4, west: 113.26 },
//     Yuexiu: { north: 23.15, south: 23.1, east: 113.3, west: 113.24 },
//     Baiyun: { north: 23.4, south: 23.1, east: 113.4, west: 113.15 },
//     Nansha: { north: 22.9, south: 22.6, east: 113.7, west: 113.5 },
//     Panyu: { north: 23.1, south: 22.9, edge: 113.5, west: 113.3 },
//     Liwan: { north: 23.15, south: 23.08, east: 113.26, west: 113.2 },
//     Haizhu: { north: 23.12, south: 23.05, east: 113.35, west: 113.25 }
//   }
// 
//   let visibleCount = 0
//   let totalCount = 0
// 
//   markers.value.forEach((marker) => {
//     totalCount++
//     let isVisible = true
//     
//     // 1. 检查行政区筛选条件
//     let passDistrictFilter = true
//     if (selectedDistricts.value.length > 0) {
//       const markerLatLng = marker.getLatLng()
//       const lat = markerLatLng.lat
//       const lng = markerLatLng.lng
//       
//       passDistrictFilter = selectedDistricts.value.some(district => {
//         const bounds = districtBounds[district]
//         if (bounds) {
//           return lat >= bounds.south && lat <= bounds.north && 
//                  lng >= bounds.west && lng <= bounds.east
//         }
//         return false
//       })
//     }
//     
//     // 2. 检查建筑类型筛选条件
//     let passCategoryFilter = true
//     if (selectedCategories.value.length > 0) {
//       passCategoryFilter = selectedCategories.value.includes(marker.category)
//     }
//     
//     // 3. 只有同时满足两个条件才显示
//     isVisible = passDistrictFilter && passCategoryFilter
//     
//     if (isVisible) {
//       visibleCount++
//       console.log(`✅ 显示建筑: ${marker.category}, 坐标: ${marker.getLatLng().lat}, ${marker.getLatLng().lng}`)
//     }
// 
//     // 4. 根据可见性设置图标和层级
//     const iconUrl = getIconUrlByLabel(marker.category, !isVisible)
//     
//     const newIcon = L.icon({
//       iconUrl: iconUrl,
//       iconSize: [32, 32],
//       iconAnchor: [16, 32]
//     })
//     
//     marker.setIcon(newIcon)
//     marker.setZIndexOffset(isVisible ? 1000 : 0)
//   })
//   
//   console.log(`筛选结果: ${visibleCount}/${totalCount} 个建筑可见`)
//   console.log("=== 重叠筛选结束 ===")
// }
const updateMarkersVisibilityByDistrict = () => {
  console.log("updateMarkersVisibilityByDistrict调用, 选中区域:", selectedDistricts.value)
  
  // 定义广州各行政区的地理坐标范围
  const districtBounds: { [key: string]: { north: number, south: number, east: number, west: number } } = {
    Tianhe: { north: 23.2, south: 23.08, east: 113.4, west: 113.26 },
    Yuexiu: { north: 23.15, south: 23.1, east: 113.3, west: 113.24 },
    Baiyun: { north: 23.4, south: 23.1, east: 113.4, west: 113.15 },
    Nansha: { north: 22.9, south: 22.6, east: 113.7, west: 113.5 },
    Panyu: { north: 23.1, south: 22.9, east: 113.5, west: 113.3 },
    Liwan: { north: 23.15, south: 23.08, east: 113.26, west: 113.2 },
    Haizhu: { north: 23.12, south: 23.05, east: 113.35, west: 113.25 }
  }

  markers.value.forEach((marker) => {
    let isVisible = true
    
    // 如果选中了特定行政区，检查marker是否在该行政区内
    if (selectedDistricts.value.length > 0) {
      const markerLatLng = marker.getLatLng()
      const lat = markerLatLng.lat
      const lng = markerLatLng.lng
      
      isVisible = selectedDistricts.value.some(district => {
        const bounds = districtBounds[district]
        if (bounds) {
          const inBounds = lat >= bounds.south && lat <= bounds.north && 
                          lng >= bounds.west && lng <= bounds.east
          if (inBounds) {
            console.log(`建筑在${district}区域内:`, lat, lng)
          }
          return inBounds
        }
        return false
      })
    }

    // 根据可见性设置图标和层级
    const iconUrl = getIconUrlByLabel(marker.category, !isVisible)
    
    const newIcon = L.icon({
      iconUrl: iconUrl,
      iconSize: [32, 32],
      iconAnchor: [16, 32]
    })
    
    marker.setIcon(newIcon)
    marker.setZIndexOffset(isVisible ? 1000 : 0)
  })
}

/** === 新的年代和城市叠加筛选函数 === */
const updateMarkersVisibilityByYearAndCity = async () => {
  console.log("=== 开始年代&城市筛选 ===")
  console.log("选中的年代:", selectedYearPeriods.value)
  console.log("选中的城市:", selectedCities.value)
  
  let visibleCount = 0
  let totalCount = 0

  // 使用 Promise.all 来处理异步操作
  const markerUpdates = markers.value.map(async (marker) => {
    totalCount++
    let isVisible = true
    
    // 只对GX Buildings进行筛选
    if (marker.category === "GX Buildings") {
      // 1. 检查年代筛选条件
      let passYearFilter = true
      if (selectedYearPeriods.value.length > 0 && marker.buildingYear) {
        const simplifiedYear = getSimplifiedYear(marker.buildingYear)
        passYearFilter = selectedYearPeriods.value.includes(simplifiedYear)
      }
      
      // 2. 检查城市筛选条件
      let passCityFilter = true
      if (selectedCities.value.length > 0 && marker.buildingCity) {
        passCityFilter = selectedCities.value.includes(marker.buildingCity)
      }
      
      // 3. 只有同时满足两个条件才显示（对于GX Buildings）
      isVisible = passYearFilter && passCityFilter
    }
    // 其他类别的建筑保持可见
    
    if (isVisible) {
      visibleCount++
    }

    // 4. 根据可见性设置图标和层级
    let iconUrl
    if (marker.category === "GX Buildings") {
      // GX Buildings保持基于城市的颜色，但在不可见时变灰
      if (isVisible) {
        // 保持原有的基于城市的颜色
        try {
          const color = await getGXBuildingMarkerColor(marker.buildingName || "")
          iconUrl = createColoredMarkerIcon(color)
        } catch {
          iconUrl = getIconUrlByLabel(marker.category)
        }
      } else {
        // 被筛选掉的点变灰
        iconUrl = createColoredMarkerIcon("#D3D3D3")
      }
    } else {
      // 其他类别使用原有逻辑
      iconUrl = getIconUrlByLabel(marker.category, !isVisible)
    }
    
    const newIcon = L.icon({
      iconUrl: iconUrl,
      iconSize: [32, 32],
      iconAnchor: [16, 32]
    })
    
    marker.setIcon(newIcon)
    marker.setZIndexOffset(isVisible ? 1000 : 0)
  })

  await Promise.all(markerUpdates)
  
  console.log(`筛选结果: ${visibleCount}/${totalCount} 个建筑可见`)
  console.log("=== 年代&城市筛选结束 ===")
}

/** 更新图表颜色 */
const updateChartColors = () => {
  updateChartBarColors()
  updateChartPieColors()
}

/** 添加图表平滑状态切换效果 */
const smoothChartTransition = (chartType: "bar" | "pie", callback: () => void) => {
  const chartInstance = chartType === "bar" 
    ? echarts.getInstanceByDom(barChartContainer.value as HTMLDivElement)
    : echarts.getInstanceByDom(pieChartContainer.value as HTMLDivElement)
  
  if (!chartInstance) return
  
  // 第一阶段：淡出效果
  chartInstance.setOption({
    animation: true,
    animationDuration: 300,
    animationEasing: "cubicIn",
    series: [{
      animationType: "scale",
      animationEasing: "cubicIn"
    }]
  }, false)
  
  // 第二阶段：执行更新并淡入
  setTimeout(() => {
    callback()
    
    // 第三阶段：淡入效果
    chartInstance.setOption({
      animation: true,
      animationDuration: 400,
      animationEasing: "cubicOut",
      series: [{
        animationType: "scale",
        animationEasing: "cubicOut"
      }]
    }, false)
  }, 300)
}

/** 更新柱状图颜色 - 现在处理城市筛选 */
const updateChartBarColors = () => {
  const barChartInstance = echarts.getInstanceByDom(barChartContainer.value as HTMLDivElement)
  if (barChartInstance) {
    // 定义城市颜色映射
    const cityColors = {
      北海市: "#FDD8A3",
      防城港市: "#79C5BE", 
      钦州市: "#C4FFB5",
      南宁市: "#98D8C8",
      桂林市: "#FDF4A7",
      柳州市: "#7FA4CA",
      梧州市: "#E26A30",
      百色市: "#EEFEAC",
      玉林市: "#D7FEB0",
      贵港市: "#8190CC",
      来宾市: "#8C84CF",
      贺州市: "#AD85C6",
      河池市: "#7CB8C7",
      崇左市: "#FDD8A3"
    }
    
    // 添加更流畅的动画配置
    barChartInstance.setOption({
      // 启用动画
      animation: true,
      animationDuration: 750,
      animationEasing: "cubicInOut",
      animationDurationUpdate: 600, // 更新时的动画时长
      animationEasingUpdate: "cubicInOut", // 更新时的缓动效果
      series: [
        {
          itemStyle: {
            color: (params: any) => {
              const cityName = params.name
              const isSelected = selectedCities.value.length === 0 || selectedCities.value.includes(cityName)
              return isSelected ? (cityColors[cityName] || "#D3D3D3") : "#D3D3D3"
            },
            // 添加阴影和高光效果
            shadowBlur: isSelected => isSelected ? 8 : 0,
            shadowColor: "rgba(0, 0, 0, 0.3)",
            borderWidth: 1,
            borderColor: "#fff"
          },
          // 添加更细腻的动画延迟
          animationDelay: (idx) => idx * 40, // 城市较多，减少延迟
          animationDelayUpdate: (idx) => idx * 30,
          // 高亮效果
          emphasis: {
            itemStyle: {
              shadowBlur: 15,
              shadowColor: "rgba(0, 0, 0, 0.5)"
            },
            animationDuration: 200,
            animationEasing: "cubicOut"
          }
        }
      ]
    }, false) // 使用增量更新，不替换整个配置
  }
}

/** 更新饼图颜色 - 现在处理年代筛选 */
const updateChartPieColors = () => {
  console.log("updateChartPieColors调用")
  const pieChartInstance = echarts.getInstanceByDom(pieChartContainer.value as HTMLDivElement)
  if (pieChartInstance) {
    // 定义年代颜色映射
    const yearColors = {
      明代及以前: "#9EBCDA",
      清代: "#F5C44F",
      民国: "#FF6B6B",
      建国后: "#CE90FF",
      改革开放后: "#F97B56",
      现代: "#50CF8C"
    }
    
    pieChartInstance.setOption({
      // 启用动画
      animation: true,
      animationDuration: 900,
      animationEasing: "cubicInOut",
      animationDurationUpdate: 700, // 更新时的动画时长
      animationEasingUpdate: "cubicInOut", // 更新时的缓动效果
      series: [{
        itemStyle: {
          color: (params: any) => {
            const yearPeriod = params.name
            const isSelected = selectedYearPeriods.value.length === 0 || selectedYearPeriods.value.includes(yearPeriod)
            console.log(`饼图颜色更新: ${yearPeriod}, 选中: ${isSelected}`)
            return isSelected ? (yearColors[yearPeriod] || "#D3D3D3") : "#D3D3D3"
          },
          // 添加阴影和边框效果
          shadowBlur: 6,
          shadowColor: "rgba(0, 0, 0, 0.2)",
          borderWidth: 2,
          borderColor: "rgba(255, 255, 255, 0.5)"
        },
        // 添加扇形变化动画
        animationType: "scale",
        animationEasing: "cubicInOut",
        animationDelay: (idx) => idx * 100, // 年代较少，增加延迟
        animationDelayUpdate: (idx) => idx * 80,
        // 增强高亮效果
        emphasis: {
          itemStyle: {
            shadowBlur: 20,
            shadowColor: "rgba(0, 0, 0, 0.4)",
            scale: true,
            scaleSize: 5,
            borderWidth: 3,
            borderColor: "rgba(255, 255, 255, 0.5)"
          },
          label: {
            fontSize: 12,
            fontWeight: "bold"
          },
          animationDuration: 300,
          animationEasing: "elasticOut"
        }
      }]
    }, false) // 使用增量更新
  } else {
    console.warn("未找到饼图实例")
  }
}

/** 切换 coordinate-list 中的选中状态 */
const toggleCategoryList = (categoryLabel: string) => {
  const index = selectedCategoriesList.value.indexOf(categoryLabel)
  if (index === -1) {
    selectedCategoriesList.value.push(categoryLabel)
  } else {
    selectedCategoriesList.value.splice(index, 1)
  }
}

/** 判断 coordinate-list 中某类别是否为灰状态 */
const isGrayList = (label: string): boolean => {
  return selectedCategoriesList.value.includes(label)
}

/** 点击 coordinate-list 时，对地图和列表进行同步切换 */
const handleCategoryClick = (categoryLabel: string) => {
  // toggleCategory(categoryLabel) // 已注释 - 原建筑类别筛选
  toggleCategoryList(categoryLabel)
}

/** 地图上点击某 Marker 时，执行飞行并加载描述、图片等 */
const flyTo = async (coord: { label: string; lat: number; lng: number }, subIndex: number) => {
  console.log("flyTo function called")
  console.log("Received coord:", coord)
  console.log("subIndex:", subIndex)

  const latLng = new L.LatLng(coord.lat, coord.lng)
  selectedBuilding.value = coord
  showDetailModal.value = true
  console.log("selectedBuilding set to:", selectedBuilding.value)

  // 请求 JSON 描述
  const jsonFileName = `${coord.label}.json`
  const descriptionJsonPath = `/buildingDescriptions/${encodeURIComponent(jsonFileName)}`
  console.log("Constructed descriptionJsonPath:", descriptionJsonPath)

  fetch(descriptionJsonPath)
    .then((response) => {
      console.log("Fetch response status:", response.status)
      if (!response.ok) {
        throw new Error("Network response was not ok")
      }
      return response.json()  
    })
    .then((data) => {
      console.log("Received JSON data:", data)
      selectedBuildingDescription.value = data.A2_content || "描述不可用"
      selectedBuildingYear.value = data.build_year || ""
      selectedBuildingStructure.value = data.structureType || ""
      
      // 检查是否为GX Buildings，如果是则设置城市信息
      const buildingCategory = findBuildingCategory(coord, coordinates.value)
      if (buildingCategory === "GX Buildings") {
        selectedBuildingCity.value = data.city || ""
      } else {
        selectedBuildingCity.value = ""
      }
      
      console.log("selectedBuildingDescription set to:", selectedBuildingDescription.value)
      console.log("selectedBuildingYear set to:", selectedBuildingYear.value)
      console.log("selectedBuildingStructure set to:", selectedBuildingStructure.value)
      console.log("selectedBuildingCity set to:", selectedBuildingCity.value)
    })
    .catch((error) => {
      console.error("Error loading building description:", error)
      selectedBuildingDescription.value = "暂无"
      selectedBuildingCity.value = ""
    })

  // 构造图片路径
  const buildingCategory = findBuildingCategory(coord, coordinates.value)
  const buildingLabel = coord.label.replace(" ", "_")
  
  // 判断是否为GX历史建筑，如果是则使用新的图片加载逻辑
  if (buildingCategory === "GX Buildings") {
    // 使用新的GX建筑图片加载逻辑
    try {
      const images = await getGXBuildingImages(coord.label)
      selectedBuildingImage.value = images
      console.log("GX建筑图片路径:", selectedBuildingImage.value)
    } catch (error) {
      console.error("加载GX建筑图片失败:", error)
      // 提供默认图片路径
      selectedBuildingImage.value = [`/GXbuildingsData/image/${coord.label}/1.jpg`]
    }
  } else {
    // 使用原有的图片加载逻辑
    const categoryPath = buildingCategory.toLowerCase().replace(" ", "_")
    const labelPath = buildingLabel
    try {
      const images = await getBuildingImages(labelPath, categoryPath)
      selectedBuildingImage.value = images
      console.log("原有逻辑图片路径:", selectedBuildingImage.value)
    } catch (error) {
      console.error("加载建筑图片失败:", error)
      // 提供默认图片路径
      selectedBuildingImage.value = [`/buildingPic/${categoryPath}/${labelPath}/${labelPath}_1.jpg`]
    }
  }

  // 地图视角飞行 (已禁用缩放)
  console.log("Setting map view to:", latLng)
  // map.setView(latLng, 14) // 已注释：不再缩放地图
}


/** 发送聊天消息 */
/** 跳转到指定建筑 */
const jumpToBuilding = (coordinate: {lat: number, lng: number}) => {
  console.log("jumpToBuilding 被调用:", coordinate)
  
  // 在所有markers中查找匹配的marker
  const targetMarker = markers.value.find(marker => {
    const markerLatLng = marker.getLatLng()
    const latDiff = Math.abs(markerLatLng.lat - coordinate.lat)
    const lngDiff = Math.abs(markerLatLng.lng - coordinate.lng)
    console.log(`比较建筑: lat差值=${latDiff}, lng差值=${lngDiff}`)
    return latDiff < 0.001 && lngDiff < 0.001
  })
  
  if (targetMarker) {
    console.log("找到目标marker，触发点击")
    // 模拟点击marker事件
    targetMarker.fire("click")
    // 地图视角跳转 (已禁用缩放)
    // map.setView(new L.LatLng(coordinate.lat, coordinate.lng), 16) // 已注释：不再缩放地图
  } else {
    console.log("未找到目标marker")
    // 即使没找到marker，也可以跳转地图 (已禁用缩放)
    // map.setView(new L.LatLng(coordinate.lat, coordinate.lng), 16) // 已注释：不再缩放地图
  }
}

/** 跳转到指定建筑并切换关键词图片 */
const jumpToBuildingAndSwitchKeywords = (coordinate: {lat: number, lng: number}) => {
  // 先跳转到建筑
  jumpToBuilding(coordinate)
  // 然后切换关键词图片从Keywords3切换到Keywords2
  showKeywords3.value = false
}

/** 智能搜索函数 - 直接根据用户输入搜索建筑 */
const performSmartSearch = async (input: string) => {
  const results: any[] = []
  
  // 解析用户输入的各种条件
  const cityKeywords = ["南宁", "桂林", "柳州", "梧州", "北海", "防城港", "钦州", "百色", "玉林", "贵港", "来宾", "贺州", "河池", "崇左"]
  const structureKeywords = ["砖木结构", "砖混结构", "钢混结构", "木结构", "砖石结构", "混合结构"]
  const yearKeywords = ["明代", "清代", "民国", "建国后", "改革开放后", "现代"]

  
  // 提取筛选条件
  const cities = cityKeywords.filter(city => input.includes(city)).map(city => city + "市")
  const structures = structureKeywords.filter(structure => input.includes(structure))
  const years = yearKeywords.filter(year => input.includes(year))
  
  // 遍历所有建筑数据进行匹配
  for (const category of coordinates.value) {
    for (const building of category.items) {
      let isMatch = true
      let buildingData: any = null
      
      // 获取建筑详细数据
      try {
        const jsonFileName = `${building.label}.json`
        const descriptionJsonPath = `/buildingDescriptions/${encodeURIComponent(jsonFileName)}`
        const response = await fetch(descriptionJsonPath)
        if (response.ok) {
          buildingData = await response.json()
        }
      } catch (error) {
        console.log(`无法加载 ${building.label} 的描述文件`)
        continue
      }
      
      if (!buildingData) { continue }
      
      // 城市筛选
      if (cities.length > 0) {
        const buildingCity = buildingData.city || ""
        const cityMatch = cities.some(city => buildingCity.includes(city.replace("市", "")))
        if (!cityMatch) {
          isMatch = false
        }
      }
      
      // 结构类型筛选
      if (structures.length > 0) {
        const buildingStructure = buildingData.structureType || ""
        const structureMatch = structures.some(structure => 
          buildingStructure.includes(structure)
        )
        if (!structureMatch) {
          isMatch = false
        }
      }
      
      // 年代筛选
      if (years.length > 0) {
        const buildingYear = buildingData.build_year || ""
        const yearMatch = years.some(year => {
          if (year === "明代" && buildingYear.includes("明")) { return true }
          if (year === "清代" && buildingYear.includes("清")) { return true }
          if (year === "民国" && buildingYear.includes("民国")) { return true }
          return buildingYear.includes(year)
        })
        if (!yearMatch) {
          isMatch = false
        }
      }
      
      // 如果没有任何筛选条件，则使用关键词搜索
      if (cities.length === 0 && structures.length === 0 && years.length === 0) {
        // 关键词搜索（建筑名称和描述）
        const nameMatch = building.label.includes(input)
        const content = buildingData.A2_content || ""
        const descriptionMatch = content.includes(input)
        if (!nameMatch && !descriptionMatch) {
          isMatch = false
        }
      }
      
      // 如果所有条件都匹配，添加到结果中
      if (isMatch && results.length < 20) {
        results.push({
          name: building.label,
          category: category.label,
          coordinate: { lat: building.lat, lng: building.lng },
          city: buildingData.city || "",
          structure: buildingData.structureType || "",
          year: buildingData.build_year || "",
          description: buildingData.A2_content || "",
          matchedConditions: {
            cities,
            structures, 
            years,
            searchKeyword: (cities.length === 0 && structures.length === 0 && years.length === 0) ? input : ""
          }
        })
      }
    }
  }
  
  return results
}



const sendMessage = async () => {
  if (userInput.value.trim() === "") {
    return
  }
  
  const input = userInput.value.trim()
  chatMessages.value.push(`User: ${userInput.value}`)
  const documentContent = `
  
Religious Buildings (宗教建筑): 84 座
Commercial Buildings (商业建筑): 67 座
Industrial Buildings (工业建筑): 33 座
Public Buildings (公共建筑): 141 座
Military Buildings (军事建筑): 9 座
Residential Buildings (住宅建筑): 414 座
总计：
总建筑数量: 748 座历史建筑
最多的类别: 住宅建筑 (414座，占55.3%)
最少的类别: 军事建筑 (9座，占1.2%)
数据来源说明：
根据代码中的描述，这个数据库包含了广州市831座历史文化建筑的信息，分为8个批次收集。数据包括：
精确的地理坐标（经纬度）
完整的地址描述
建筑名称
批次编号
基本描述（建筑特色和历史背景简介）
建筑摄影文档
这些数据为研究广州历史文化建筑的空间分布提供了必要的信息支持。
`
  try {
    const response = await fetch("http://localhost:8000/question", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question: userInput.value
      })
    })

    const data = await response.json()
    const content = data.answer || data.response || data.result || ""
    
    const htmlContent = content
      .replace(
        /(https?:\/\/[^\s]+)/g,
        '<a href="$1" target="_blank" style="color: blue;">$1</a>'
      )
      .replace(
        /!\[([^\]]*)\]\(([^\)]+)\)/g,
        '<img src="$2" alt="$1" style="max-width: 100%; height: auto;"/>'
      )

    chatMessages.value.push(`BOT: <div>${htmlContent}</div>`)
    
    // API响应后，检查是否需要进行主题搜索
    const themeKeywords = ["中山", "革命", "民国", "看看", "寻找", "想看", "历史建筑", "活动过", "建筑", "旧址", "宗教", "商业", "住宅", "公共", "工业", "军事", "广西", "桂林", "南宁", "柳州"]
    const isThemeSearch = themeKeywords.some(keyword => input.includes(keyword)) || input.length > 0
    
    if (isThemeSearch) {
      // 使用智能搜索，直接处理用户输入
      console.log("执行智能搜索，用户输入:", input)
      
      const searchResults = await performSmartSearch(input)
      
      if (searchResults.length > 0) {
        // 从第一个结果中获取匹配条件来生成描述
        const matchedConditions = searchResults[0].matchedConditions
        const conditionsDesc = []
        
        if (matchedConditions.cities.length > 0) { 
          conditionsDesc.push(`城市：${matchedConditions.cities.join(", ")}`) 
        }
        if (matchedConditions.structures.length > 0) { 
          conditionsDesc.push(`结构：${matchedConditions.structures.join(", ")}`) 
        }
        if (matchedConditions.years.length > 0) { 
          conditionsDesc.push(`年代：${matchedConditions.years.join(", ")}`) 
        }
        if (matchedConditions.searchKeyword) { 
          conditionsDesc.push(`关键词：${matchedConditions.searchKeyword}`) 
        }
        
        if (conditionsDesc.length > 0) {
          chatMessages.value.push(`BOT: 根据条件【${conditionsDesc.join(" | ")}】找到 ${searchResults.length} 个相关建筑，请点击下方列表查看详情。`)
        } else {
          chatMessages.value.push(`BOT: 找到 ${searchResults.length} 个相关建筑，请点击下方列表查看详情。`)
        }
        } else {
          chatMessages.value.push(`BOT: 未找到相关建筑，请尝试其他关键词。`)
      }
      
      console.log("搜索结果:", searchResults)
      themeSearchResults.value = searchResults
    }
    
  } catch (error) {
    console.error("Error calling GraphRAG API:", error)
    chatMessages.value.push("BOT: 抱歉，问答服务暂时不可用，请确保后端服务已启动。")
  } finally {
    userInput.value = ""
  }
}

/* =========================================
 * 5. 所有 watch
 * ========================================= */

/** 监听 selectedCategoriesChart => 更新图表置灰 */
watch(selectedCategoriesChart, () => {
  updateChartBarColors()
})

/** 监听 selectedCategories => 更新地图标记灰度 */
watch(selectedCategories, () => {
  updateMarkersVisibility()
})

/* =========================================
 * 6. 生命周期钩子
 * ========================================= */

/** 计算 map 的 DOM 容器 ID */
const withKeyId = computed(() => `mars2d-container-${props.mapKey}`)

/** onMounted - 初始化地图并创建标记 */
onMounted(() => {
  // Step 2: Initialize Mars2D Map
  mars2d.Util.fetchJson({ url: props.url })
    .then((data: any) => {
      console.log("Config loaded:", data) // 添加调试日志
      console.log("Mars2D config:", data.mars2d) // 查看mars2d配置
      console.log("Center from config:", data.mars2d?.center) // 查看center配置
      
      initMars3d({
        ...data.mars2d,
        ...props.options
      })
    })
    .then(() => {
      // Step 3: Initialize Map Markers
      coordinates.value.forEach((category) => {
        category.items.forEach(async (coord, subIndex) => {
          // 根据 label 选择对应的图标路径
          let iconUrl = getIconUrlByLabel(category.label)
          
          // 如果是GX Buildings，根据城市创建颜色化的图标
          if (category.label === "GX Buildings") {
            const cityColor = await getGXBuildingMarkerColor(coord.label)
            // 创建基于城市颜色的SVG图标
            const coloredIcon = createColoredMarkerIcon(cityColor)
            iconUrl = coloredIcon
          }
          
          // 创建标记
          const marker = L.marker([coord.lat, coord.lng], {
            icon: L.icon({
              iconUrl: iconUrl,
              iconSize: [29, 29],
              iconAnchor: [14.5, 29]
            })
          }) as CustomMarker

          // 添加到地图
          marker.addTo(map)
          // 添加类别信息
          marker.category = category.label
          // 添加建筑名称信息
          marker.buildingName = coord.label
          
          // 为GX Buildings添加年代和城市信息用于筛选
          if (category.label === "GX Buildings") {
            try {
              const jsonFileName = `${coord.label}.json`
              const descriptionJsonPath = `/buildingDescriptions/${encodeURIComponent(jsonFileName)}`
              const response = await fetch(descriptionJsonPath)
              if (response.ok) {
                const data = await response.json()
                marker.buildingYear = data.build_year || ""
                marker.buildingCity = data.city || ""
              }
            } catch (error) {
              console.log(`无法获取 ${coord.label} 的筛选信息`)
            }
          }
          
          // 点击事件
          // 点击事件：飞行到标记，加载描述和图片
          marker.on("click", () => {
            // toggleCategory(marker.category) // 已注释 - 原建筑类别筛选
            flyTo(coord, subIndex)
            selectedBuilding.value = coord
            selectedBuildingDescription.value = "loading"
            
            // 记录选中的建筑，用于知识图谱高亮
            selectedBuildingForKG.value = coord.label

            const jsonFileName = `${coord.label}.json`
            const descriptionJsonPath = `/buildingDescriptions/${encodeURIComponent(jsonFileName)}`
            // 获取建筑描述
            fetch(descriptionJsonPath)
              .then((response) => response.json())
              .then((data) => {
                selectedBuildingDescription.value = data.A2_content || "描述不可用"
                selectedBuildingYear.value = data.build_year || ""
                selectedBuildingStructure.value = data.structureType || ""
                // 如果是GX Buildings，设置城市信息
                if (category.label === "GX Buildings") {
                  selectedBuildingCity.value = data.city || ""
                } else {
                  selectedBuildingCity.value = ""
                }
              })
              .catch(() => {
                selectedBuildingDescription.value = "None"
                selectedBuildingCity.value = ""
              })
          })

          
          // 悬停事件
          marker.on("mouseover", async () => {
            hoveredBuilding.value = coord
            updateFloatingWindowPosition(new L.LatLng(coord.lat, coord.lng))

            const jsonFileName = `${coord.label}.json`
            const descriptionJsonPath = `/buildingDescriptions/${encodeURIComponent(jsonFileName)}`
            try {
              const response = await fetch(descriptionJsonPath)
              if (!response.ok) {
                throw new Error("Network response was not ok")
              }
              const data = await response.json()
              hoveredBuildingDescription.value = data.A2_content || "暂无描述"
              hoveredBuildingYear.value = data.build_year || ""
              hoveredBuildingStructure.value = data.structureType || ""
              
              // 如果是GX Buildings，设置城市信息
              if (category.label === "GX Buildings") {
                hoveredBuildingCity.value = data.city || ""
              } else {
                hoveredBuildingCity.value = ""
              }
            } catch (error) {
              console.error("Error loading building description:", error)
              hoveredBuildingDescription.value = "暂无描述"
              hoveredBuildingCity.value = ""
            }
            floatingWindowStyle.value.zIndex = 9999
          })

          // 鼠标离开
          marker.on("mouseout", () => {
            hoveredBuilding.value = null
            hoveredBuildingDescription.value = ""
            hoveredBuildingYear.value = ""
            hoveredBuildingStructure.value = ""
            hoveredBuildingCity.value = ""
            floatingWindowStyle.value.zIndex = -1
          })

          // 将 marker 添加到 markers 数组
          markers.value.push(marker)
        })
      })
    })
})

/** onMounted - 初始化 ECharts */
onMounted(() => {
  if (!pieChartContainer.value || !barChartContainer.value) {
    return
  }
  // 直接用 ref 初始化 ECharts
  const barChart = echarts.init(barChartContainer.value)
  const pieChart = echarts.init(pieChartContainer.value)
  
  // 现在柱状图显示城市数据（原来的饼图数据）
  const barData = [25, 18, 15, 30, 22, 20, 28, 35, 12, 18, 16, 25, 10, 8] // 城市分布数据
  const categories = ["北海市", "防城港市", "钦州市", "南宁市", "桂林市", "柳州市", "梧州市", "百色市", "玉林市", "贵港市", "来宾市", "贺州市", "河池市", "崇左市"] // 城市类别
  const total = barData.reduce((a, b) => a + b, 0) // 总和
  
  // 现在饼图显示年代数据（原来的柱状图数据）
  const pieData = [15, 25, 35, 45, 30, 50] // 年代分布数据
  console.log("饼图数据:", pieData)
  console.log("饼图数据总和:", pieData.reduce((a, b) => a + b, 0))
  
  // 为饼图准备数据 - 年代分类
  const pieCategories = ["明代及以前", "清代", "民国", "建国后", "改革开放后", "现代"]
  const pieSeriesData = pieCategories.map((category, index) => ({
  name: category,
  value: pieData[index]
}))
  
  // 柱状图配置 - 现在显示城市数据
  const barChartOptions = {
    animation: true,
    animationDuration: 800,
    animationEasing: "cubicOut" as const,
    animationDelay: (idx) => idx * 30, // 城市较多，减少延迟
    grid: {
      top: "5%",
      bottom: "15%", // 增加底部空间给城市标签
      left: "10%",
      right: "10%"
    },
    tooltip: {
      show: true,
      trigger: "axis",
      axisPointer: { type: "shadow" },
      formatter: "{b}: {c} 个建筑"
    },
    xAxis: {
      type: "category",
      data: categories,
      axisLabel: {
        show: true,
        rotate: 45, // 倾斜显示城市名称
        fontSize: 9,
        color: "#333",
        margin: 8,
        interval: 0 // 显示所有标签
      },
      axisLine: { show: true }
    },
    yAxis: {
      type: "value",
      axisLabel: {
        show: true,
        fontSize: 12,
        color: "#333"
      },
      axisLine: { show: true }
    },
    series: [
      {
        name: "城市建筑分布",
        type: "bar",
        data: barData,
        label: {
          show: true,
          position: "top",
          fontSize: 10,
          color: "#333",
          fontFamily: "DengXian, 等线, sans-serif"
        },
        itemStyle: {
          color: (params) => {
            const cityName = categories[params.dataIndex]
            return cityColors[cityName] || "#D3D3D3"
          },
          // 添加初始阴影效果
          shadowBlur: 4,
          shadowColor: "rgba(0, 0, 0, 0.2)",
          borderRadius: [4, 4, 0, 0],
          borderWidth: 1,
          borderColor: "#fff"
        },
        // 添加柱状图动画配置
        animationDelay: (idx) => idx * 50,
        animationEasing: "elasticOut",
        // 增强悬停效果
        emphasis: {
          itemStyle: {
            shadowBlur: 15,
            shadowColor: "rgba(0, 0, 0, 0.4)",
            borderWidth: 2,
            borderColor: "#fff"
          },
          label: {
            show: true,
            fontSize: 12,
            fontWeight: "bold",
            color: "#fff"
          }
        }
      }
    ]
  }
  
  // 定义城市颜色映射（现在用于柱状图）
  const cityColors = {
    北海市: "#FDD8A3",
    防城港市: "#79C5BE", 
    钦州市: "#C4FFB5",
    南宁市: "#98D8C8",
    桂林市: "#FDF4A7",
    柳州市: "#7FA4CA",
    梧州市: "#E26A30",
    百色市: "#EEFEAC",
    玉林市: "#D7FEB0",
    贵港市: "#8190CC",
    来宾市: "#8C84CF",
    贺州市: "#AD85C6",
    河池市: "#7CB8C7",
    崇左市: "#FDD8A3"
  }
  
  // 定义年代颜色映射（现在用于饼图）
  const yearColors = {
    明代及以前: "#9EBCDA",
    清代: "#F5C44F",
    民国: "#FF6B6B",
    建国后: "#CE90FF",
    改革开放后: "#F97B56",
    现代: "#50CF8C"
  }

  // 饼图配置 - 现在显示年代数据
  const pieChartOptions = {
    animation: true,
    animationDuration: 1000,
    animationEasing: "cubicInOut" as const,
    tooltip: {
      trigger: "item",
      position: function (point, params, dom, rect, size) {
        // 获取tooltip的宽度和高度
        const tooltipWidth = size.contentSize[0]
        const tooltipHeight = size.contentSize[1]
        
        // 获取容器的宽度和高度
        const containerWidth = size.viewSize[0]
        const containerHeight = size.viewSize[1]
        
        // 默认位置：鼠标右下方
        let x = point[0] + 15
        let y = point[1] + 15
        
        // 如果tooltip会超出右边界，则放在鼠标左边
        if (x + tooltipWidth > containerWidth) {
          x = point[0] - tooltipWidth - 15
        }
        
        // 如果tooltip会超出下边界，则放在鼠标上方
        if (y + tooltipHeight > containerHeight) {
          y = point[1] - tooltipHeight - 15
        }
        
        return [x, y]
      },
      backgroundColor: "rgba(255, 255, 255, 0.95)", // 白色半透明背景
      borderColor: "#ccc", // 边框颜色
      borderWidth: 1, // 边框宽度
      borderRadius: 6, // 圆角
      padding: [8, 12], // 内边距
      textStyle: {
        color: "#333", // 文字颜色
        fontSize: 12 // 字体大小
      },
      extraCssText: "box-shadow: 0 2px 8px rgba(0,0,0,0.15);", // 阴影效果
      formatter: "年代分布<br/>{b}: {c}个 ({d}%)"
    },
    legend: {
      show: true,
      orient: "vertical", // 垂直排列
      right: "5%", // 距离右边的距离
      top: "center", // 垂直居中
      itemWidth: 14, // 图例标记的宽度
      itemHeight: 14, // 图例标记的高度
      textStyle: {
        fontSize: 12,
        color: "#333"
      }
    },
    series: [
      {
        name: "年代分布",
        type: "pie",
        radius: ["55%", "15%"], // 调整饼图大小 - 增大外圈，减小内圈
        center: ["32%", "50%"], // 向左移动饼图，为右侧图例留空间
        avoidLabelOverlap: true, // 避免标签重叠
        label: {
          show: false // 隐藏标签，使用右侧图例代替
        },
        labelLine: {
          show: false // 隐藏标签引导线
        },

        data: pieSeriesData,
        itemStyle: {
          color: (params) => {
            return yearColors[params.name] || "#D3D3D3"
          },
          // 添加初始阴影和边框效果
          shadowBlur: 8,
          shadowColor: "rgba(0, 0, 0, 0.2)",
          borderWidth: 2,
          borderColor: "rgba(255, 255, 255, 0.5)"
        },
        // 添加饼图动画配置
        animationType: "scale",
        animationEasing: "elasticOut",
        animationDelay: (idx) => idx * 100, // 年代较少，增加延迟展示效果
        // 增强悬停效果
        emphasis: {
          itemStyle: {
            shadowBlur: 20,
            shadowColor: "rgba(0, 0, 0, 0.4)",
            borderWidth: 3,
            borderColor: "rgba(255, 255, 255, 0.5)"
          },
          label: {
            show: false // 悬停时不显示标签
          },
          labelLine: {
            show: false // 悬停时不显示连接线
          }
        }
      }
    ]
  }
  

    // 设置图表配置
  barChart.setOption(barChartOptions)
  pieChart.setOption(pieChartOptions)
  
  console.log("添加ECharts点击事件监听器")
  
  // 为柱状图添加点击事件 - 城市筛选
  barChart.on("click", (params: any) => {
    console.log("柱状图点击事件 - 城市筛选:", params)
    const clickedCity = params.name // 获取点击的城市
    
    // 调用城市筛选函数
    toggleCity(clickedCity)
    console.log(`柱状图城市筛选: ${clickedCity}`)
  })
  
  // === 原建筑类型筛选逻辑（已注释） ===
  // barChart.on("click", (params: any) => {
  //   console.log("柱状图点击事件:", params)
  //   const clickedCategory = params.name // 获取点击的类别名称
  //   // 将英文类别名映射为完整的类别名
  //   const categoryMapping: { [key: string]: string } = {
  //     Commercial: "Commercial Buildings",
  //     Industrial: "Industrial Buildings", 
  //     Military: "Military Buildings",
  //     Public: "Public Buildings",
  //     Religious: "Religious Buildings",
  //     Residential: "Residential Buildings"
  //   }
  //   const fullCategoryName = categoryMapping[clickedCategory] || clickedCategory
  //   
  //   // 调用现有的toggleCategory函数
  //   toggleCategory(fullCategoryName)
  //   console.log(`柱状图筛选: ${fullCategoryName}`)
  // })
  
  // 为饼图添加点击事件 - 年代筛选
  pieChart.on("click", (params: any) => {
    console.log("饼图点击事件 - 年代筛选:", params)
    const clickedYearPeriod = params.name // 获取点击的年代名称
    
    // 调用年代筛选函数
    toggleYearPeriod(clickedYearPeriod)
    console.log(`饼图年代筛选: ${clickedYearPeriod}`)
  })
  
  // === 原行政区筛选逻辑（已注释） ===
  // pieChart.on("click", (params: any) => {
  //   console.log("饼图点击事件:", params)
  //   const clickedDistrict = params.name // 获取点击的行政区名称
  //   
  //   // 调用行政区筛选函数
  //   toggleDistrict(clickedDistrict)
  //   console.log(`饼图筛选: ${clickedDistrict}`)
  // })
})

// 组件挂载时直接使用预定义的关键词
onMounted(() => {
  keywordsList.value = commonKeywords
})

</script>

<style scoped>
/* 以下为原样保留的 style，未做任何修改 */

/* ===========================
 * 页面布局与容器样式
 * =========================== */
.page_container {
  width: 100%;
  height: 100%;
  display: flex;
  overflow: hidden; /* 防止页面级别的滚动 */
}

.gpt4-chatbox {
  width: 15% !important;
  height: 98%;
  bottom: 30px;
  top: 60px; /* 离页面底部30px */
  display: absolute;
  flex-direction: column;
  overflow: hidden; /* 防止整个chatbox溢出 */
  max-height: calc(100vh - 90px); /* 确保不超出视口 */
}

.map-container {
  width: 55%;
  margin: 0 20px 0 20px;
  overflow: hidden;
  max-height: 100%;
  z-index: 1;
}

.side-panel {
  width: 25%;
  margin: 0 10px 0 10px;
}

.component-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  z-index: 999;
}

.mars2d-container {
  width: 100%;
  height: 94.25%;
  border: 0px solid #add8e6;
  border-radius: 10px;
  margin-top: 30px; /* 设置与 header 元素的距离为 20px */
}

/* ===========================================
 * 右侧各个组件的样式
 * =========================================== */
.coordinate-list,
.building-info,
.gpt4-chatbox {
  background-color: #ffffff;
  padding: 15px; /* 增加一点填充 */
  border-radius: 10px; /* 与地图容器保持一致 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  pointer-events: auto;
  border: 2px solid #add8e6; /* 与地图容器的边框颜色一致 */
}

.building-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 1.2em;
}

.building-info h3 {
  margin-bottom: 10px;
}

.building-info p {
  margin: 0;
}

.coordinate-list {
  position: absolute;
  top: 3%;
  right: 1%;
  width: 10%;
  max-height: 250px; /* 保留固定高度 */
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  overflow-y: hidden; /* 去掉滚动条 */
}

.coordinate-list ul {
  list-style-type: none;
  padding-left: 10px;
}

.coordinate-list ul li {
  cursor: pointer;
  padding: 5px;
  border-radius: 8px;
  transition: background-color 0.3s ease, color 0.3s ease; /* 添加过渡效果 */
}

.coordinate-list ul li:hover {
  background-color: #f0f8ff; /* 设置浅色背景 */
}

.coordinate-list ul li .gray {
  color: #999; /* 文字变灰 */
}

.coordinate-list ul li .gray img {
  filter: grayscale(100%); /* 图标变灰 */
}

/* hover时的效果 */
.gpt4-chatbox:hover {
  box-shadow: 0 0 20px rgb(157, 180, 189); /* 鼠标悬停时增加发光效果 */
}

.chat-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden; /* 防止水平滚动 */
  margin-bottom: 10px;
  max-height: 90%; /* 限制最大宽度 */
}

.chat-content::-webkit-scrollbar {
  width: 8px; /* 滚动条宽度 */
}

.chat-content::-webkit-scrollbar-track {
  background: transparent; /* 滚动条轨道背景 */
}

.chat-content::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2); /* 滚动条滑块颜色 */
  border-radius: 4px;
  border: none;
}

.chat-content::-webkit-scrollbar-button {
  display: none; /* 隐藏上下箭头按钮 */
}

.chat-content p {
  padding: 10px;
  margin: 5px 0;
  border-radius: 8px;
  background-color: #bdd0e2;
  border: 1px solid #add8e6;
}

.chat-content p.user-message {
  background-color: #e0ffe0;
  border: 1px solid #90ee90;
}

.input-container {
  display: flex;
  align-items: center;
  padding: 10px;
  position: fixed; /* 固定定位 */
  bottom: 4%; /* 距离窗口底部0px */
  left: 0.5%; /* 距离窗口左侧0px */
  width: 15%; /* 占据窗口宽度 */
  background-color: #ffffff; /* 背景色 */
  z-index: 999; /* 确保位于其他元素之上 */
}
textarea {
  flex: 1;
  padding: 8px;
  border-radius: 4px;
  border: 2px solid #add8e6; /* 默认边框颜色 */
  outline: none; /* 移除默认的点击高亮 */
}

textarea:focus {
  border-color: #0561c4; /* 深蓝色边框 */
  box-shadow: 0 0 5px rgba(0, 86, 179, 0.5); /* 可选的蓝色阴影效果 */
}

button {
  background-color: #64a4e9;
  color: #fff;
  border: none;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}

button svg {
  vertical-align: middle;
}

button:hover {
  background-color: #1f6abb;
}

.modal {
  position: absolute;
  top: 0;
  right: 0;
  width: 30%;
  height: 100%;
  background-color: #ffffff;
  padding: 20px;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.15);
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  border-radius: 8px;
  border: 1px solid #0c0c0c;
}

.description-container {
  position: absolute;
  top: 0; /* 改为 0，贴合顶部 */
  left: 0; /* 改为 0，贴合左侧 */
  bottom: 0; /* 改为 0，贴合底部 */
  width: 17%; /* 占据左侧 16% 的宽度 */
  overflow: hidden;
  background-color: #e6edf0; /* 修改为淡蓝色 */
  padding: 15px; /* 添加内边距 */
}

.arrow {
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 8px solid black; /* 黑色实心箭头 */
  margin-right: 5px; /* 箭头与文字之间的间距 */
}

.component-header span {
  font-weight: bold;
  font-size: 16px;  /* 设置字体大小 */
  font-family: "DengXian", "等线", sans-serif;  /* 设置字体族 */
  color: #16293b;  /* 设置字体颜色 */
}

.LatitudeandLongitude {
  font-size: 12px; /* 设置较小的字体大小 */
  font-family: "DengXian", "等线", sans-serif; /* 设置字体 */
}

.description-box {
  width: 152%;
  background-color: #5592cf; /* 设置深蓝色背景 */
  color: white; /* 文字颜色设置为白色（可选）以确保对比度 */
  padding: 18px; /* 添加一些内边距让文本不贴边 */
  margin: 30px 0 0 25px; /* 负的左边和右边边距，正的 margin-top 控制下移 */
  width:95%; /* 确保描述部分占据容器的全部宽度 */
  font-family: "DengXian", "等线", sans-serif; /* 设置字体 */
}

.image-display {
  margin-top: 20px;
  width: 40%;
  height: 50%;
  object-fit: cover; /* 确保图片覆盖整个矩形区域 */
}

.oldfont {
  font-family: "oldfont", sans-serif; /* 使用本地字体，替换 YourLocalFont 为实际的字体名称 */
  font-size: 35px; /* 可根据需要调整字体大小 */
  font-weight: bold; /* 设置字体粗细（可选） */
}

.label-icon {
  width: 20px; /* 设置图标的宽度 */
  height: 20px; /* 设置图标的高度 */
  margin-right: 8px; /* 图标与文本之间的间距 */
  vertical-align: middle; /* 保持图标与文本垂直居中对齐 */
}

.chart-box {
  margin: 10px 0;
  width: 48%;
}

.charts-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  gap: 20px;
  margin: 10px 0;
}

.chart-container {
  width: 93%;
  height: 280px;
  position: relative; /* 保持相对布局 */
  z-index: 1; /* 设置较高的层级，确保在side-panel前面显示 */
  border: 2px solid rgba(177, 177, 177, 0.308);
  background-color: rgba(236, 232, 232, 0.2);
  box-shadow: 0 0 10px rgba(216, 214, 214, 0.8);
  border-radius: 8px;
  transition: all 0.3s ease-in-out;
  padding: 10px;
}

.chart-container:hover {
  box-shadow: 0 0 20px rgba(169, 169, 169, 1);
}

.chart-container .component-header {
  padding: 10px; /* 为RAG部分添加内边距 */
}
.rag-box {
  width: 48%;
  height: 20vh;
  margin: 20px 0;
  border: 2px solid rgba(177, 177, 177, 0.308);
  background-color: rgba(236, 232, 232, 0.2);
  box-shadow: 0 0 10px rgba(216, 214, 214, 0.8);
  border-radius: 8px;
  transition: all 0.3s ease-in-out;
  
}

.rag-box:hover {
  box-shadow: 0 0 20px rgba(169, 169, 169, 1);
}

.rag-box .component-header {
  padding: 15px; /* 为RAG部分添加内边距 */
}


.floating-window {
  position: flex;
  top: 5%;
  left: 5%;
  background-color: #fff;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 99999;
  max-height: 250px;
}

.building-info-row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.year-tag {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid;
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 8px;
  text-align: center;
}

.year-tag-detail {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid;
  margin: 10px 0;
  font-size: 14px;
}

.year-label {
  font-weight: 500;
  margin-right: 6px;
}

.year-value {
  font-weight: 600;
}

.tag-container {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.structure-tag {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid;
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 8px;
  text-align: center;
}

.structure-tag-detail {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid;
  margin: 10px 0;
  font-size: 14px;
}

.structure-label {
  font-weight: 500;
  margin-right: 6px;
}

.structure-value {
  font-weight: 600;
}

.draggable-text {
  position: absolute;
  top: 312px; /* 初始位置：距离顶部 310px */
  left: 2220px; /* 初始位置：距离左侧 390px */
  z-index: 999; /* 保证文字位于其他内容之上 */
  background-color: rgba(255, 255, 255, 0.8); /* 可选：设置背景色 */
  font-size: 12px; /* 设置文字大小 */
  color: #333; /* 设置文字颜色 */
  font-family: "DengXian", "等线", sans-serif; /* 设置字体 */
  font-style: italic; /* 设置斜体 */
  cursor: move; /* 鼠标变为移动样式 */
}

.knowledge-container {
  display: flex;
  width: 100%;
  gap: 20px; /* 两个元素之间的间距 */
  margin: 20px 0;
}


/* 新增的词义图容器样式 */
.keyword-graph {
  width: 48%;
  height: 20vh;
  margin: 20px 0;
  border: 2px solid rgba(177, 177, 177, 0.308);
  background-color: rgba(236, 232, 232, 0.2);
  box-shadow: 0 0 10px rgba(216, 214, 214, 0.8);
  border-radius: 8px;
  transition: all 0.3s ease-in-out;
  position: relative;
}

.keyword-graph:hover {
  box-shadow: 0 0 20px rgba(169, 169, 169, 1);
}

.keyword-graph .component-header {
  padding: 15px; /* 为RAG部分添加内边距 */
}

.word-cloud-container {
  position: relative;
  width: 100%;
  height: calc(100% - 50px); /* 减去标题的高度 */
  overflow: hidden;
}

.keyword-item {
  position: absolute;
  transform: translate(-50%, -50%);
  transition: all 0.3s ease;
  cursor: default;
  text-align: center;
  padding: 2px 4px;
  margin: 0;
  border-radius: 3px;
  white-space: nowrap;
  line-height: 1.2;
}

.keyword-item:hover {
  transform: translate(-50%, -50%) scale(1.15);
  z-index: 10;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
  background-color: rgba(255, 255, 255, 0.2);
}

.rag-box {
  width: 48%;
  height: 20vh;
  margin: 20px 0;
  border: 2px solid rgba(177, 177, 177, 0.308);
  background-color: rgba(236, 232, 232, 0.2);
  box-shadow: 0 0 10px rgba(216, 214, 214, 0.8);
  border-radius: 8px;
  transition: all 0.3s ease-in-out;
  
}

.rag-box:hover {
  box-shadow: 0 0 20px rgba(169, 169, 169, 1);
}

.rag-box .component-header {
  padding: 15px; /* 为RAG部分添加内边距 */
}

.batch-greencontainer {
  background-color: lightgreen; /* 浅绿色背景 */
  color: #333; /* 文本颜色 */
  font-size: 14px; /* 字体大小 */
  padding: 5px 10px; /* 内边距 */
  border-radius: 5px; /* 边角圆润 */
  display: inline-block; /* 让矩形不占据整行 */
  margin-top: 10px; /* 上边距 */
}
.new-description-container {
  width: 95%; /* 宽度100% */
  height: 40vh; /* 高度300px */
  border: 2px solid rgba(177, 177, 177, 0.308);
  background-color: rgba(236, 232, 232, 0.2);
  box-shadow: 0 0 10px rgba(216, 214, 214, 0.8);
  border-radius: 8px;
  transition: all 0.3s ease-in-out;
  padding: 15px; /* 为容器内部添加内边距 */
}
.new-description-container:hover {
  box-shadow: 0 0 20px rgba(169, 169, 169, 1);
}

.new-description-container .description-box {
  font-size: 16px; 
  padding: 10px;
  background-color: #eceaea;
  border-radius: 8px;
  border: 1px solid #ddd;
  margin: 15px 2px 15px 2px; /* 上边距15px，右边距2px，下边距20px，左边距2px */
  max-width: 855px;
  color: #030303;
  line-height: 1.5; /* 设置行高 */
  max-height: calc(1.5em * 4); /* 限制最大高度为4行 */
  overflow-y: auto; /* 垂直方向添加滚动条 */
  word-wrap: break-word; /* 长单词自动换行 */
}
.new-description-container .building-category {
  display: flex;
  align-items: center;
}

.new-description-container .label-icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}

.new-description-container .oldfont {
  font-size: 28px;
    font-weight: bold;
  }
.image-gallery {
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 每行5列 */
  gap: 10px;
  margin-top: 30px;
}

.gallery-image {
  width: 110px;
  height: 130px; /* 根据需要调整高度 */
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.gallery-image:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.word-cloud-container {
  position: relative;
  width: 100%;
  height: calc(20vh - 60px);
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  margin: 5px;
  padding: 10px;
}

.keyword-item {
  position: absolute;
  padding: 2px 6px;
  transition: all 0.3s;
  cursor: default;
  display: inline-block;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
  transform-origin: center;
  line-height: 1.2;
  white-space: nowrap;
  text-align: center;
  transform: translate(-50%, -50%); /* 确保居中对齐 */
}

.keyword-item:hover {
  transform: translate(-50%, -50%) scale(1.15) !important;
  z-index: 10;
}

.no-keywords {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(20vh - 60px);
  color: #999;
  font-style: italic;
}

/* 知识图谱对话框样式 */
.knowledge-graph-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80vw;
  height: 80vh;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.dialog-header {
  padding: 12px 16px;
  background-color: #f8f8f8;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.dialog-content {
  flex: 1;
  padding: 16px;
  overflow: hidden; /* 修改为hidden以移除滚动条 */
  position: relative; /* 添加相对定位 */
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  line-height: 1;
}

.close-button:hover {
  color: #333;
}

.knowledge-graph-network {
  width: 100%;
  height: 100%; /* 修改为100%以填充整个容器 */
  background-color: #f0f0f0;
  border: 1px solid lightgray;
}

/* 修改悬浮窗样式 */
.building-popup {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 1001;
  max-width: 300px;
  font-size: 14px;
  line-height: 1.5;
  cursor: move; /* 恢复拖动光标 */
  user-select: text; /* 恢复文本选择功能 */
  /* 移除 pointer-events: none 以恢复鼠标事件 */
}

.building-popup b {
  display: block;
  margin-bottom: 8px;
  font-size: 16px;
  color: #333;
}

.graph-legend {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  border-top: 1px solid #eee;
  height: 60px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-right: 20px;
}
.legend-color {
  width: 16px;
  height: 16px;
  margin-right: 5px;
  border: 1px solid #ccc;
  border-radius: 50%;
}

.building-color {
  background-color: #FECA57;
  border-color: #FECA57;
}

.category-color {
  background-color: #96CEB4;
  border-color: #96CEB4;
}

.address-color {
  background-color: #4ECDC4;
  border-color: #4ECDC4;
}

.type-color {
  background-color: #45B7D1;
  border-color: #45B7D1;
}


.renovation-color {
  background-color: #E67E22;
  border-color: #E67E22;
}

.graph-tip {
  margin-left: auto;
  font-style: italic;
  color: #666;
  font-size: 12px;
}

/* 数据处理相关样式 */
.action-button {
  padding: 4px 8px;
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.action-button:hover {
  background-color: #3367d6;
}

.action-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
.close-button-small {
  padding: 2px 5px;
  font-size: 12px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 3px;
  cursor: pointer;
}

.status-message {
  margin-bottom: 8px;
  padding: 5px;
  border-radius: 4px;
  background-color: #f8f9fa;
  border-left: 3px solid #4285f4;
  font-size: 12px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.data-table th, .data-table td {
  padding: 5px;
  border: 1px solid #ddd;
  text-align: left;
}

.data-table th {
  background-color: #f8f9fa;
  font-weight: bold;
}

.data-table tr:nth-child(even) {
  background-color: #f8f9fa;
}

.empty-data {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #999;
  font-style: italic;
}

/* KGlogo 样式类 */
.kg-logo-container {
  width: 70%;
  height: 70%;
  display: flex;
  justify-content: flex-end;  /* 水平右对齐 - 可调整为 center, flex-start, flex-end */
  align-items: flex-end;    /* 垂直上对齐 - 可调整为 center, flex-start, flex-end */
  padding: 0px;
  position: relative;
  left: 40px;
}
.kg-logo-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  max-width: 100%;
  max-height: 100%;
}

.kg-logo-overlay {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  top: 0;
  left: 30px;
  border-radius: 8px;
  pointer-events: none;
}

.kg-logo-text {
  color: #333;
  font-size: 16px;
  font-weight: bold;
  background-color: rgba(255,255,255,0.7);
  padding: 5px 15px;
  border-radius: 20px;
  position: relative;
  left: 20px;
}
/* 主题搜索结果样式 */
.theme-results {
  margin: 15px 0;
  padding: 10px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 8px;
  border-left: 4px solid #4CAF50;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.theme-results-header {
  font-weight: bold;
  font-size: 14px;
  color: #2c3e50;
  margin-bottom: 10px;
  padding-bottom: 5px;
  border-bottom: 1px solid rgba(76, 175, 80, 0.3);
}

.theme-results-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.result-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
}

.result-item:hover {
  background: #e3f2fd;
  border-color: #2196F3;
  transform: translateX(5px);
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.2);
}

.result-number {
  background: #4CAF50;
  color: white;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: bold;
  margin-right: 10px;
  flex-shrink: 0;
}

.result-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.result-name {
  font-size: 13px;
  color: #2c3e50;
  font-weight: 500;
  line-height: 1.2;
}

.result-details {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
}

.result-category {
  font-size: 10px;
  color: #7f8c8d;
  background: #ecf0f1;
  padding: 2px 6px;
  border-radius: 12px;
  font-weight: 500;
}

.result-city {
  font-size: 10px;
  color: #e67e22;
  background: #fef9e7;
  padding: 2px 6px;
  border-radius: 12px;
  font-weight: 500;
  border: 1px solid #f39c12;
}

.result-structure {
  font-size: 10px;
  color: #3498db;
  background: #ebf3fd;
  padding: 2px 6px;
  border-radius: 12px;
  font-weight: 500;
  border: 1px solid #3498db;
}

.result-year {
  font-size: 10px;
  color: #9b59b6;
  background: #f4ecf7;
  padding: 2px 6px;
  border-radius: 12px;
  font-weight: 500;
  border: 1px solid #9b59b6;
}
</style>
