# GISauto 作品集展示版部署

这个版本只用于对外展示作品集页面，不依赖本机 FastAPI、Neo4j 或 AI 模型服务。适合发给老师、同学、面试官或评审快速查看项目能力。

## 本地构建

```bash
npm run build:portfolio
```

构建产物在 `dist/` 目录。部署时上传整个 `dist/` 文件夹即可。

## 推荐访问地址

部署完成后，优先分享：

```text
https://你的域名/portfolio.html
```

它会自动跳转到作品集路由：

```text
https://你的域名/index.html#/portfolio
```

## 最省事的上线方式

### Vercel

1. 把项目推到 GitHub。
2. 在 Vercel 导入仓库。
3. Build Command 填：

```bash
npm run build:portfolio
```

4. Output Directory 填：

```text
dist
```

### Netlify

1. 把项目推到 GitHub。
2. 在 Netlify 新建站点并导入仓库。
3. Build command 填：

```bash
npm run build:portfolio
```

4. Publish directory 填：

```text
dist
```

### GitHub Pages

1. 执行 `npm run build:portfolio`。
2. 把 `dist/` 的内容发布到 GitHub Pages 对应分支或目录。
3. 分享 `portfolio.html` 地址。

## 注意

- 这个展示版主要展示作品集页面和本地静态图片。
- 如果要让别人真实体验智能问答、图谱接口和图像检索，需要另行部署 FastAPI + Neo4j + AI API。
- 当前项目的 `npm run build` 会先跑 lint/type-check，可能被 `@types/leaflet` 与 TypeScript 版本兼容问题卡住；展示版请用 `npm run build:portfolio`。
