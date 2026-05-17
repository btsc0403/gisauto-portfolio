import { defineStore } from "pinia"
import { ref } from "vue"
import { useBuildingStore } from "./buildingStore"

const API_BASE = "http://localhost:8000"

const COMPONENT_HINTS = [
  "构件", "斗拱", "飞檐", "翘角", "柱础", "雀替", "栏杆", "瓦当", "脊饰",
  "花窗", "门窗", "梁架", "穿斗", "抬梁", "柱廊", "马头墙",
]

const VISUAL_SEARCH_TRIGGERS = [
  "搜图", "搜索相似", "找相似", "找类似", "类似的建筑", "相似建筑",
  "像这样的", "这种风格", "视觉搜索", "以图搜", "图片搜索",
]

const COMPONENT_SEARCH_TRIGGERS = [
  "搜构件", "搜索构件", "找构件", "查构件", "相似构件", "类似构件",
]

function detectIntent(text: string, hasImage: boolean) {
  if (hasImage) {
    return COMPONENT_HINTS.some(k => text.includes(k))
      ? "image-component" as const
      : "image-building" as const
  }
  if (COMPONENT_SEARCH_TRIGGERS.some(k => text.includes(k))) return "text-component" as const
  if (VISUAL_SEARCH_TRIGGERS.some(k => text.includes(k))) return "text-building" as const
  return "chat" as const
}

export const useChatStore = defineStore("chat", () => {
  const userInput = ref("")
  const chatMessages = ref<string[]>([])
  const themeSearchResults = ref<any[]>([])
  const isSearching = ref(false)
  const uploadedFile = ref<File | null>(null)
  const uploadPreviewUrl = ref("")

  function setUploadFile(file: File | null) {
    uploadedFile.value = file
    if (file) {
      uploadPreviewUrl.value = URL.createObjectURL(file)
    } else {
      uploadPreviewUrl.value = ""
    }
  }

  async function searchByTextImage(query: string, limit = 10) {
    const res = await fetch(`${API_BASE}/search/by-text-image?query=${encodeURIComponent(query)}&limit=${limit}`)
    return await res.json()
  }

  async function searchByComponent(query: string, limit = 10) {
    const res = await fetch(`${API_BASE}/search/by-component?query=${encodeURIComponent(query)}&limit=${limit}`)
    return await res.json()
  }

  async function searchImageToBuilding(file: File, limit = 10) {
    const fd = new FormData()
    fd.append("file", file)
    const res = await fetch(`${API_BASE}/search/image-to-building?limit=${limit}`, { method: "POST", body: fd })
    return await res.json()
  }

  async function searchImageToComponent(file: File, limit = 10) {
    const fd = new FormData()
    fd.append("file", file)
    const res = await fetch(`${API_BASE}/search/image-to-component?limit=${limit}`, { method: "POST", body: fd })
    return await res.json()
  }

  function findCoordinate(name: string) {
    const store = useBuildingStore()
    for (const cat of store.coordinates) {
      for (const item of cat.items) {
        if (item.label === name) return { lat: item.lat, lng: item.lng }
      }
    }
    return undefined
  }

  function formatBuildingResults(results: any[]) {
    themeSearchResults.value = results
      .map((r: any) => {
        const coord = findCoordinate(r.name)
        if (!coord) return null
        return {
          name: r.name,
          city: r.city || "",
          structure: r.structure || "",
          year: r.era || "",
          image_path: r.image_path || "",
          description: r.visual_summary || "",
          features: r.features || [],
          score: r.score,
          coordinate: coord,
          _type: "building",
        }
      })
      .filter(Boolean)
  }

  function formatComponentResults(results: any[]) {
    themeSearchResults.value = results
      .map((r: any) => {
        const coord = findCoordinate(r.building)
        if (!coord) return null
        return {
          name: `${r.building} — ${r.component}`,
          building: r.building,
          component: r.component,
          city: r.city || "",
          crop_path: r.crop_path || "",
          building_image: r.building_image || "",
          confidence: r.confidence,
          score: r.score,
          coordinate: coord,
          _type: "component",
        }
      })
      .filter(Boolean)
  }

  async function performSmartSearch(input: string) {
    const store = useBuildingStore()
    const results: any[] = []

    const cityKeywords = ["南宁", "桂林", "柳州", "梧州", "北海", "防城港", "钦州", "百色", "玉林", "贵港", "来宾", "贺州", "河池", "崇左"]
    const structureKeywords = ["砖木结构", "砖混结构", "钢混结构", "木结构", "砖石结构", "混合结构"]
    const yearKeywords = ["明代", "清代", "民国", "建国后", "改革开放后", "现代"]
    const featureKeywords = [
      "飞檐", "翘角", "歇山顶", "硬山顶", "悬山顶", "攒尖顶", "马头墙", "风火墙", "琉璃瓦", "灰瓦", "筒瓦",
      "斗拱", "穿斗", "抬梁", "梁架", "柱础", "石柱", "木柱", "骑楼柱廊",
      "青砖墙", "夯土墙", "石砌墙", "白灰墙",
      "花窗", "木雕门", "石门框", "趟栊门", "满洲窗",
      "灰塑", "砖雕", "木雕", "石雕", "壁画", "对联", "彩绘",
      "天井", "院落", "风雨桥", "鼓楼", "牌坊", "门楼", "碉楼", "戏台", "古井", "石板路",
    ]

    const cities = cityKeywords.filter((c) => input.includes(c)).map((c) => c + "市")
    const structures = structureKeywords.filter((s) => input.includes(s))
    const years = yearKeywords.filter((y) => input.includes(y))
    const features = featureKeywords.filter((f) => input.includes(f))

    for (const category of store.coordinates) {
      for (const building of category.items) {
        let isMatch = true
        const data = await store.loadBuildingDescription(building.label)
        if (!data) continue

        if (cities.length > 0) {
          const bc = data.city || ""
          if (!cities.some((c) => bc.includes(c.replace("市", "")))) isMatch = false
        }
        if (structures.length > 0) {
          const bs = data.structureType || ""
          if (!structures.some((s) => bs.includes(s))) isMatch = false
        }
        if (years.length > 0) {
          const by = data.build_year || ""
          if (!years.some((y) => {
            if (y === "明代" && by.includes("明")) return true
            if (y === "清代" && by.includes("清")) return true
            if (y === "民国" && by.includes("民国")) return true
            return by.includes(y)
          })) isMatch = false
        }
        if (features.length > 0) {
          const text = (data.A2_content || "") + (data.valueIntroduction || "")
          if (!features.some((f) => text.includes(f))) isMatch = false
        }
        if (cities.length === 0 && structures.length === 0 && years.length === 0 && features.length === 0) {
          const nameMatch = building.label.includes(input)
          const descMatch = (data.A2_content || "").includes(input)
          if (!nameMatch && !descMatch) isMatch = false
        }

        if (isMatch && results.length < 20) {
          const text = (data.A2_content || "") + (data.valueIntroduction || "")
          const matchedFeatures = features.length > 0
            ? features.filter((f) => text.includes(f))
            : featureKeywords.filter((f) => text.includes(f)).slice(0, 5)

          results.push({
            name: building.label,
            category: category.label,
            coordinate: { lat: building.lat, lng: building.lng },
            city: data.city || "",
            structure: data.structureType || "",
            year: data.build_year || "",
            description: data.A2_content || "",
            features: matchedFeatures,
            matchedConditions: { cities, structures, years, features, searchKeyword: (cities.length === 0 && structures.length === 0 && years.length === 0 && features.length === 0) ? input : "" }
          })
        }
      }
    }
    return results
  }

  async function sendMessage() {
    const text = userInput.value.trim()
    const file = uploadedFile.value
    const hasImage = !!file

    if (!hasImage && !text) return

    const intent = detectIntent(text, hasImage)

    if (hasImage) {
      chatMessages.value.push(`User: [图片] ${file!.name}${text ? ' — ' + text : ''}`)
    } else {
      chatMessages.value.push(`User: ${text}`)
    }

    isSearching.value = true

    try {
      if (intent === "image-building" || intent === "image-component") {
        const data = intent === "image-building"
          ? await searchImageToBuilding(file!)
          : await searchImageToComponent(file!)

        if (data.error) {
          chatMessages.value.push(`BOT: 搜索出错: ${data.error}`)
          themeSearchResults.value = []
        } else if (!data.results?.length) {
          chatMessages.value.push("BOT: 未找到相似结果，请尝试其他图片。")
          themeSearchResults.value = []
        } else {
          const label = intent === "image-building" ? "建筑" : "构件"
          if (intent === "image-building") formatBuildingResults(data.results)
          else formatComponentResults(data.results)
          const count = themeSearchResults.value.length
          if (count > 0) {
            chatMessages.value.push(`BOT: 通过图片搜索找到 ${count} 个相似${label}：`)
          } else {
            chatMessages.value.push("BOT: 未找到匹配的已知建筑。")
          }
        }

      } else if (intent === "text-building" || intent === "text-component") {
        const data = intent === "text-building"
          ? await searchByTextImage(text)
          : await searchByComponent(text)

        if (data.error) {
          chatMessages.value.push(`BOT: 搜索出错: ${data.error}`)
          themeSearchResults.value = []
        } else if (!data.results?.length) {
          chatMessages.value.push("BOT: 未找到相似结果，请尝试其他描述。")
          themeSearchResults.value = []
        } else {
          const label = intent === "text-building" ? "建筑" : "构件"
          if (intent === "text-building") formatBuildingResults(data.results)
          else formatComponentResults(data.results)
          const count = themeSearchResults.value.length
          if (count > 0) {
            chatMessages.value.push(`BOT: 根据「${text}」找到 ${count} 个相似${label}：`)
          } else {
            chatMessages.value.push("BOT: 未找到匹配的已知建筑。")
          }
        }

      } else {
        const response = await fetch(`${API_BASE}/question`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: text })
        })
        const data = await response.json()
        const content = data.answer || data.response || data.result || ""
        const html = content
          .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" style="color: blue;">$1</a>')
          .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" style="max-width: 100%; height: auto;"/>')
        chatMessages.value.push(`BOT: <div>${html}</div>`)

        const searchResults = await performSmartSearch(text)
        if (searchResults.length > 0) {
          const mc = searchResults[0].matchedConditions
          const desc: string[] = []
          if (mc.cities.length > 0) desc.push(`城市：${mc.cities.join(", ")}`)
          if (mc.structures.length > 0) desc.push(`结构：${mc.structures.join(", ")}`)
          if (mc.years.length > 0) desc.push(`年代：${mc.years.join(", ")}`)
          if (mc.features.length > 0) desc.push(`构件：${mc.features.join(", ")}`)
          if (mc.searchKeyword) desc.push(`关键词：${mc.searchKeyword}`)
          chatMessages.value.push(desc.length > 0
            ? `BOT: 根据条件【${desc.join(" | ")}】找到 ${searchResults.length} 个相关建筑，请点击下方列表查看详情。`
            : `BOT: 找到 ${searchResults.length} 个相关建筑，请点击下方列表查看详情。`
          )
        }
        themeSearchResults.value = searchResults
      }
    } catch {
      chatMessages.value.push("BOT: 抱歉，服务暂时不可用，请确保后端已启动。")
    } finally {
      isSearching.value = false
      userInput.value = ""
      uploadedFile.value = null
      uploadPreviewUrl.value = ""
    }
  }

  return {
    userInput, chatMessages, themeSearchResults,
    isSearching, uploadedFile, uploadPreviewUrl,
    setUploadFile, sendMessage, performSmartSearch,
  }
})
