const STOP_WORDS = new Set([
  "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都",
  "一", "上", "也", "到", "说", "要", "去", "你", "会", "着", "没有",
  "好", "自己", "这", "他", "她", "它", "们", "那", "些", "什么",
  "怎么", "这个", "那个", "可以", "没", "被", "从", "把", "又", "但",
  "很", "做", "能", "与", "为", "以", "而", "等", "对", "中", "之",
  "其", "所", "或", "更", "已", "于", "及", "则", "每", "并", "且",
  "最", "将", "此", "该", "因", "地", "得", "里", "后", "还", "多",
  "大", "小", "如", "个", "下", "过", "前", "来", "时", "用", "第",
  "经", "让", "向", "却",
  "平方米", "平方", "公里", "公顷", "余", "约", "米", "亩",
  "年", "月", "日", "百", "千", "万", "十",
  "二", "三", "四", "五", "六", "七", "八", "九", "零",
  "号", "层", "处", "座", "条", "间", "栋", "幢",
  "省", "市", "县", "区", "镇", "乡", "村", "街", "路",
  "人民政府", "委", "委会", "社区",
  "位于", "距", "称", "名为", "属于", "成为", "进行",
  "通过", "根据", "按照", "由于", "目前", "至今",
  "附近", "左右", "现有", "具有", "主要", "其中",
  "包括", "分别", "以及", "一个", "不同", "之间",
  "以上", "以下", "之后", "之前", "东", "西", "南", "北",
  "东南", "西北", "东北", "西南", "上下",
  "面积", "人口", "形成", "建设", "修建", "建于", "始建",
  "保存", "部分", "结构", "整体", "方面", "方向",
  "左右", "相关", "较为", "比较", "相对", "一般",
  "称为", "作为", "其他", "另外", "同时", "一直",
])

function segmentChinese(text: string): string[] {
  const cleaned = text
    .replace(/[\da-zA-Z\s\n\r\t]/g, "")
    .replace(/[，。、；：""''【】（）《》？！…—·\-.,;:'"[\](){}<>/\\|@#$%^&*+=~`─\u3000]/g, "")

  if ("Segmenter" in Intl) {
    const segmenter = new (Intl as any).Segmenter("zh-CN", { granularity: "word" })
    const segments = segmenter.segment(cleaned)
    const words: string[] = []
    for (const seg of segments) {
      if (seg.isWordLike && seg.segment.length >= 2 && !STOP_WORDS.has(seg.segment)) {
        words.push(seg.segment)
      }
    }
    return words
  }

  const words: string[] = []
  for (let i = 0; i <= cleaned.length - 2; i++) {
    const bi = cleaned.slice(i, i + 2)
    if (!STOP_WORDS.has(bi)) words.push(bi)
    if (i <= cleaned.length - 3) {
      const tri = cleaned.slice(i, i + 3)
      if (!STOP_WORDS.has(tri)) words.push(tri)
    }
    if (i <= cleaned.length - 4) {
      const quad = cleaned.slice(i, i + 4)
      if (!STOP_WORDS.has(quad)) words.push(quad)
    }
  }
  return words
}

export function getWordFrequencies(text: string, maxWords = 40): [string, number][] {
  const words = segmentChinese(text)
  const freq = new Map<string, number>()
  for (const w of words) {
    freq.set(w, (freq.get(w) || 0) + 1)
  }
  return Array.from(freq.entries())
    .filter(([, count]) => count >= 2)
    .sort((a, b) => b[1] - a[1])
    .slice(0, maxWords)
}

function parseColor(raw: string): [number, number, number] | null {
  const hex = raw.trim().replace("#", "")
  if (!/^[0-9a-fA-F]{6}$/.test(hex) && !/^[0-9a-fA-F]{3}$/.test(hex)) return null
  const full = hex.length === 3
    ? hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2]
    : hex
  return [
    parseInt(full.slice(0, 2), 16),
    parseInt(full.slice(2, 4), 16),
    parseInt(full.slice(4, 6), 16),
  ]
}

export function getGradientColorFn(maxCount: number): (word: string, weight: number) => string {
  const style = getComputedStyle(document.documentElement)
  const activeRaw = style.getPropertyValue("--header-active").trim()
  const rgb = parseColor(activeRaw) || [139, 37, 0]

  return (_word: string, weight: number) => {
    const t = Math.pow(weight / maxCount, 0.4)
    const alpha = 0.3 + t * 0.7
    return `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, ${alpha})`
  }
}
