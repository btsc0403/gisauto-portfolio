# GISauto · Portfolio Edition

> **在线作品集**（部署完成后填写）：`https://<vercel-domain>/portfolio.html`
> **完整源码**（含 FastAPI 后端 / Neo4j / AI 检索）：https://github.com/btsc0403/GISauto

这是 GISauto 项目的对外作品集展示版本，包含作品集页（`/portfolio`）和地图主界面静态原型。智能问答、知识图谱、图像检索等需后端服务的功能未包含在本仓库。

## 本地运行

```bash
npm install
npm run build:portfolio
npx http-server ./dist
```

打开 `http://127.0.0.1:8080/portfolio.html` 即可访问作品集页。

## 部署到 Vercel

仓库已带 `vercel.json`，导入仓库即可：

1. 打开 https://vercel.com/new
2. Import 本仓库
3. 直接 Deploy（无需手动填 Build Command / Output Directory）

部署完成后，对外分享 `https://<your-domain>/portfolio.html`，会自动跳转到作品集页。

## 项目概览

GISauto 是一个面向广西 2,036 座历史建筑的智能 GIS 可视化平台：

- **交互式地图**：基于 Mars2D + Leaflet，呈现 1,294 个建筑点位、按类目分图标、点击查看详情
- **知识图谱**：以 Neo4j 管理建筑、城市、年代、结构、功能、构件等实体与关系
- **多模态融合检索**：关键词 + bge 文本向量 + Chinese-CLIP 图像向量 + 构件向量四路加权
- **GraphRAG 问答**：DeepSeek-V3 在 Neo4j 召回结果上生成自然语言回答
- **构件零样本检测**：Grounding DINO 识别 28 类传统建筑构件，9,636 个构件样本

## 技术栈

| 层级 | 选型 |
|------|------|
| 前端 | Vue 3、Vite、Pinia、TypeScript、Mars2D、Leaflet、ECharts、vis-network |
| 后端（本仓库不含） | FastAPI、Python 3.12、Docker Compose、nginx |
| 数据 / AI（本仓库不含） | Neo4j 5、bge-large-zh、Chinese-CLIP、Grounding DINO、DeepSeek-V3 |

## 仓库内容说明

- `src/` Vue 前端代码（含作品集页 `src/views/PortfolioView.vue`）
- `public/portfolio.html` 分享入口（自动跳转到 `#/portfolio`）
- `public/buildingPic/` 部分类目建筑图（工业、公共、宗教等）
- `public/GXbuildingsData/image/` 仅保留作品集页引用的 4 个建筑图片
- `public/coordinates/` 地图点位坐标
- `docs/PORTFOLIO_DEPLOY.md` 详细部署说明
- `vercel.json` Vercel 一键部署配置

## 备注

- 由于不含后端，地图页点击建筑可能因图片缺失而显示加载失败，作品集页 (`/portfolio`) 不受影响。
- 作品集 hero 图、媒体墙、模块卡片等所有引用图都已包含在仓库内。
