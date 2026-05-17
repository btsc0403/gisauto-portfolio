<template>
  <div class="portfolio-page">
    <section class="hero-band">
      <img
        class="hero-image"
        src="/GXbuildingsData/image/“三街两巷”骑楼建筑群/1.jpg"
        alt="广西历史建筑街区"
      />
      <div class="hero-scrim"></div>
      <div class="hero-content">
        <p class="eyebrow">GIS + Knowledge Graph + Multimodal AI</p>
        <h1>GISauto 广西历史建筑智能 GIS 平台</h1>
        <p class="hero-copy">
          面向 2036 座广西历史建筑的可视化检索系统，将地图浏览、知识图谱、自然语言问答、图文检索和建筑构件识别整合成一个面向文化遗产研究的交互式前端作品。
        </p>
        <div class="hero-actions">
          <router-link class="primary-action" to="/">查看地图系统</router-link>
          <a class="secondary-action" href="#architecture">系统架构</a>
        </div>
      </div>
      <div class="hero-metrics" aria-label="项目关键指标">
        <div v-for="metric in heroMetrics" :key="metric.label" class="metric-tile">
          <strong>{{ metric.value }}</strong>
          <span>{{ metric.label }}</span>
        </div>
      </div>
    </section>

    <section class="overview-band">
      <div class="section-heading">
        <p class="eyebrow">Project Snapshot</p>
        <h2>把历史建筑资料变成可查询、可理解、可探索的空间知识库</h2>
      </div>
      <div class="overview-grid">
        <article v-for="item in overviewItems" :key="item.title" class="overview-card">
          <span class="card-index">{{ item.index }}</span>
          <h3>{{ item.title }}</h3>
          <p>{{ item.text }}</p>
        </article>
      </div>
    </section>

    <section class="showcase-band">
      <div class="showcase-copy">
        <p class="eyebrow">Frontend Experience</p>
        <h2>作品集重点展示的是“系统能力”，不是静态介绍页</h2>
        <p>
          这个项目的前端价值在于多源数据被组织成连续体验：用户从地图进入，查看建筑详情和统计分布，再通过知识图谱、构件筛选和智能问答继续追问。页面结构强调研究者的浏览节奏，也保留给评审快速判断技术深度的入口。
        </p>
        <div class="feature-list">
          <div v-for="feature in experienceFeatures" :key="feature.title" class="feature-row">
            <span>{{ feature.tag }}</span>
            <div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.text }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="media-wall" aria-label="历史建筑图片组合">
        <img src="/GXbuildingsData/image/一号大祠堂/1.jpg" alt="一号大祠堂" />
        <img src="/GXbuildingsData/image/七十二道门/1.jpg" alt="七十二道门" />
        <img src="/GXbuildingsData/image/万和祥/1.jpg" alt="万和祥" />
      </div>
    </section>

    <section id="architecture" class="architecture-band">
      <div class="section-heading narrow">
        <p class="eyebrow">Architecture</p>
        <h2>从地图交互到多模态检索的端到端链路</h2>
      </div>
      <div class="architecture-flow">
        <div v-for="(node, index) in architectureNodes" :key="node.title" class="flow-node">
          <span class="flow-step">{{ String(index + 1).padStart(2, "0") }}</span>
          <h3>{{ node.title }}</h3>
          <p>{{ node.text }}</p>
        </div>
      </div>
    </section>

    <section class="capability-band">
      <div class="section-heading">
        <p class="eyebrow">Core Modules</p>
        <h2>可以在作品集中被重点讲述的功能模块</h2>
      </div>
      <div class="capability-grid">
        <article v-for="module in modules" :key="module.title" class="module-card">
          <img :src="module.image" :alt="module.title" />
          <div class="module-body">
            <p>{{ module.kicker }}</p>
            <h3>{{ module.title }}</h3>
            <span>{{ module.text }}</span>
          </div>
        </article>
      </div>
    </section>

    <section class="tech-band">
      <div class="section-heading narrow">
        <p class="eyebrow">Tech Stack</p>
        <h2>前端、后端、图数据库和 AI 模型协同工作</h2>
      </div>
      <div class="tech-grid">
        <div v-for="group in techStack" :key="group.name" class="tech-group">
          <h3>{{ group.name }}</h3>
          <div class="tech-tags">
            <span v-for="tech in group.items" :key="tech">{{ tech }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="closing-band">
      <div>
        <p class="eyebrow">Portfolio Framing</p>
        <h2>适合对外呈现的项目定位</h2>
        <p>
          GISauto 可以被包装成一个“文化遗产智能检索与空间分析平台”案例：既有真实数据规模，也有复杂前端交互和 AI 检索链路，适合作为 WebGIS、数据可视化、AI 应用开发方向的综合作品。
        </p>
      </div>
      <router-link class="primary-action dark-action" to="/">进入项目原型</router-link>
    </section>
  </div>
</template>

<script setup lang="ts">
const heroMetrics = [
  { value: "2036", label: "历史建筑记录" },
  { value: "14", label: "广西城市覆盖" },
  { value: "9636", label: "建筑构件样本" },
  { value: "4", label: "融合检索通道" }
]

const overviewItems = [
  {
    index: "01",
    title: "空间数据可视化",
    text: "基于 Mars2D 和 Leaflet 构建地图主界面，支持建筑点位浏览、分类图标、详情面板和筛选联动。"
  },
  {
    index: "02",
    title: "知识图谱组织",
    text: "以 Neo4j 管理建筑、城市、区县、年代、结构、功能和构件关系，让建筑档案具备可扩展的语义结构。"
  },
  {
    index: "03",
    title: "多模态智能检索",
    text: "融合关键词、文本向量、图像向量和构件向量，让用户可以用文字、图片和建筑元素描述寻找目标。"
  }
]

const experienceFeatures = [
  {
    tag: "MAP",
    title: "地图即入口",
    text: "研究者可以从地理分布进入建筑档案，减少传统表格检索带来的上下文丢失。"
  },
  {
    tag: "GRAPH",
    title: "关系可展开",
    text: "建筑与城市、年代、结构、功能、特征形成网络，支持围绕单个建筑继续扩展探索。"
  },
  {
    tag: "AI",
    title: "自然语言检索",
    text: "GraphRAG 把图数据库召回结果交给大模型生成回答，适合做研究型问答和辅助分析。"
  }
]

const architectureNodes = [
  { title: "Vue 3 前端", text: "负责地图、面板、图谱、统计图表和检索入口的组合体验。" },
  { title: "FastAPI 服务", text: "提供问答、图文检索、知识图谱查询和构件搜索接口。" },
  { title: "Neo4j 图数据库", text: "存储建筑实体、关系网络和 3 类向量索引。" },
  { title: "AI 检索模型", text: "bge、Chinese-CLIP、Grounding DINO 和 DeepSeek-V3 组成智能检索链路。" }
]

const modules = [
  {
    kicker: "Interactive GIS",
    title: "历史建筑地图",
    text: "2036 个建筑点位在地图中可视化，结合详情卡片、图标分类和区域浏览。",
    image: "/GXbuildingsData/image/“三街两巷”骑楼建筑群/2.jpg"
  },
  {
    kicker: "Knowledge Graph",
    title: "建筑关系网络",
    text: "将城市、年代、结构类型、功能和建筑特征转化为可探索的知识图谱。",
    image: "/GXbuildingsData/image/一号大祠堂/3.jpg"
  },
  {
    kicker: "Visual Retrieval",
    title: "图像与构件检索",
    text: "通过 CLIP 向量和 Grounding DINO 构件检测，实现按图片和建筑元素搜索。",
    image: "/GXbuildingsData/image/七十二道门/3.jpg"
  }
]

const techStack = [
  { name: "Frontend", items: ["Vue 3", "Vite", "Pinia", "Mars2D", "Leaflet", "ECharts", "vis-network"] },
  { name: "Backend", items: ["FastAPI", "Python 3.12", "Docker Compose", "nginx"] },
  { name: "Data & AI", items: ["Neo4j 5", "bge-large-zh", "Chinese-CLIP", "Grounding DINO", "DeepSeek-V3"] }
]
</script>

<style scoped>
.portfolio-page {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  background: #f3f0ea;
  color: #17212b;
  scroll-behavior: smooth;
}

.hero-band {
  position: relative;
  min-height: calc(100vh - 112px);
  display: flex;
  align-items: center;
  padding: 64px;
  box-sizing: border-box;
  overflow: hidden;
}

.hero-image,
.hero-scrim {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.hero-image {
  object-fit: cover;
}

.hero-scrim {
  background:
    linear-gradient(90deg, rgba(12, 18, 22, 0.82), rgba(12, 18, 22, 0.42) 54%, rgba(12, 18, 22, 0.1)),
    linear-gradient(0deg, rgba(12, 18, 22, 0.5), rgba(12, 18, 22, 0.05) 36%);
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 760px;
  color: #fffaf1;
}

.eyebrow {
  margin: 0 0 12px;
  color: #a33a2b;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0;
  text-transform: uppercase;
}

.hero-content .eyebrow {
  color: #f4c067;
}

h1,
h2,
h3,
p {
  margin-top: 0;
}

h1 {
  margin-bottom: 22px;
  max-width: 840px;
  font-size: clamp(42px, 7vw, 88px);
  line-height: 0.98;
  font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
  font-weight: 900;
  letter-spacing: 0;
}

.hero-copy {
  max-width: 680px;
  margin-bottom: 30px;
  color: rgba(255, 250, 241, 0.86);
  font-size: 18px;
  line-height: 1.8;
}

.hero-actions,
.hero-metrics,
.overview-grid,
.architecture-flow,
.capability-grid,
.tech-grid,
.tech-tags {
  display: flex;
}

.hero-actions {
  gap: 14px;
  flex-wrap: wrap;
}

.primary-action,
.secondary-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 0 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 800;
  text-decoration: none;
}

.primary-action {
  background: #b63a28;
  color: #fff;
}

.secondary-action {
  border: 1px solid rgba(255, 255, 255, 0.62);
  color: #fff;
}

.primary-action:hover,
.secondary-action:hover {
  text-decoration: none;
  filter: brightness(1.05);
}

.hero-metrics {
  position: absolute;
  right: 48px;
  bottom: 42px;
  z-index: 1;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-end;
  max-width: 560px;
}

.metric-tile {
  width: 128px;
  min-height: 84px;
  padding: 14px;
  box-sizing: border-box;
  border: 1px solid rgba(255, 255, 255, 0.32);
  border-radius: 8px;
  background: rgba(7, 14, 18, 0.34);
  backdrop-filter: blur(12px);
}

.metric-tile strong {
  display: block;
  color: #fffaf1;
  font-size: 28px;
  line-height: 1;
}

.metric-tile span {
  display: block;
  margin-top: 8px;
  color: rgba(255, 250, 241, 0.74);
  font-size: 12px;
  line-height: 1.4;
}

.overview-band,
.architecture-band,
.capability-band,
.tech-band,
.closing-band {
  padding: 78px 64px;
  box-sizing: border-box;
}

.overview-band {
  background: #f3f0ea;
}

.section-heading {
  max-width: 980px;
  margin-bottom: 32px;
}

.section-heading.narrow {
  max-width: 760px;
}

.section-heading h2,
.showcase-copy h2,
.closing-band h2 {
  margin-bottom: 18px;
  font-size: clamp(28px, 4vw, 48px);
  line-height: 1.14;
  color: #17212b;
  letter-spacing: 0;
}

.overview-grid {
  gap: 18px;
}

.overview-card,
.flow-node,
.tech-group {
  border: 1px solid rgba(23, 33, 43, 0.12);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.54);
}

.overview-card {
  flex: 1;
  min-width: 0;
  padding: 24px;
}

.card-index,
.flow-step {
  display: inline-block;
  margin-bottom: 20px;
  color: #2b6c74;
  font-size: 13px;
  font-weight: 900;
}

.overview-card h3,
.flow-node h3,
.module-body h3,
.tech-group h3 {
  margin-bottom: 10px;
  color: #17212b;
  font-size: 20px;
  line-height: 1.35;
}

.overview-card p,
.flow-node p,
.module-body span,
.showcase-copy p,
.closing-band p {
  color: #52606b;
  line-height: 1.75;
}

.showcase-band {
  display: grid;
  grid-template-columns: minmax(0, 0.95fr) minmax(320px, 1.05fr);
  gap: 44px;
  align-items: center;
  padding: 78px 64px;
  background: #e4ece8;
  box-sizing: border-box;
}

.showcase-copy {
  max-width: 720px;
}

.feature-list {
  display: grid;
  gap: 14px;
  margin-top: 26px;
}

.feature-row {
  display: grid;
  grid-template-columns: 58px minmax(0, 1fr);
  gap: 16px;
  align-items: start;
  padding: 18px 0;
  border-top: 1px solid rgba(23, 33, 43, 0.16);
}

.feature-row span {
  color: #2b6c74;
  font-size: 12px;
  font-weight: 900;
}

.feature-row h3 {
  margin-bottom: 6px;
  font-size: 18px;
}

.feature-row p {
  margin-bottom: 0;
  color: #52606b;
  line-height: 1.7;
}

.media-wall {
  display: grid;
  grid-template-columns: 1fr 0.75fr;
  grid-template-rows: 220px 220px;
  gap: 12px;
  min-height: 452px;
}

.media-wall img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 18px 45px rgba(27, 43, 48, 0.16);
}

.media-wall img:first-child {
  grid-row: span 2;
}

.architecture-band {
  background: #17212b;
}

.architecture-band .eyebrow,
.architecture-band h2 {
  color: #fffaf1;
}

.architecture-flow {
  gap: 0;
}

.flow-node {
  position: relative;
  flex: 1;
  min-width: 0;
  padding: 24px;
  border-color: rgba(255, 255, 255, 0.16);
  background: rgba(255, 255, 255, 0.06);
}

.flow-node + .flow-node {
  margin-left: 12px;
}

.flow-node h3 {
  color: #fffaf1;
}

.flow-node p {
  color: rgba(255, 250, 241, 0.72);
}

.flow-step {
  color: #f4c067;
}

.capability-band {
  background: #f8f6f1;
}

.capability-grid {
  gap: 18px;
}

.module-card {
  flex: 1;
  min-width: 0;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 16px 36px rgba(23, 33, 43, 0.08);
}

.module-card img {
  width: 100%;
  height: 240px;
  object-fit: cover;
  display: block;
}

.module-body {
  padding: 22px;
}

.module-body p {
  margin-bottom: 8px;
  color: #a33a2b;
  font-size: 12px;
  font-weight: 900;
  text-transform: uppercase;
}

.tech-band {
  background: #dfe7e6;
}

.tech-grid {
  gap: 16px;
}

.tech-group {
  flex: 1;
  padding: 24px;
}

.tech-tags {
  gap: 8px;
  flex-wrap: wrap;
}

.tech-tags span {
  padding: 8px 10px;
  border-radius: 8px;
  background: #fffaf1;
  color: #31404a;
  font-size: 13px;
  font-weight: 700;
}

.closing-band {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  background: #fffaf1;
}

.closing-band > div {
  max-width: 820px;
}

.dark-action {
  flex-shrink: 0;
}

@media (max-width: 980px) {
  .hero-band,
  .overview-band,
  .showcase-band,
  .architecture-band,
  .capability-band,
  .tech-band,
  .closing-band {
    padding-left: 28px;
    padding-right: 28px;
  }

  .hero-band {
    align-items: flex-start;
    padding-top: 58px;
    padding-bottom: 220px;
  }

  .hero-metrics {
    left: 28px;
    right: 28px;
    justify-content: flex-start;
  }

  .overview-grid,
  .architecture-flow,
  .capability-grid,
  .tech-grid,
  .closing-band {
    flex-direction: column;
  }

  .flow-node + .flow-node {
    margin-left: 0;
    margin-top: 12px;
  }

  .showcase-band {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .hero-band {
    min-height: auto;
    padding: 42px 20px 280px;
  }

  h1 {
    font-size: 40px;
  }

  .hero-copy {
    font-size: 15px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .hero-metrics {
    left: 20px;
    right: 20px;
    bottom: 24px;
  }

  .metric-tile {
    width: calc(50% - 5px);
  }

  .overview-band,
  .showcase-band,
  .architecture-band,
  .capability-band,
  .tech-band,
  .closing-band {
    padding: 52px 20px;
  }

  .media-wall {
    grid-template-columns: 1fr;
    grid-template-rows: repeat(3, 190px);
    min-height: 0;
  }

  .media-wall img:first-child {
    grid-row: auto;
  }

  .module-card img {
    height: 210px;
  }
}
</style>
