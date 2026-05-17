export const CITY_COLORS: Record<string, string> = {
  北海市: "#FDD8A3",
  防城港市: "#79C5BE",
  钦州市: "#C4FFB5",
  南宁市: "#98D8C8",
  桂林市: "#FDF4A7",
  柳州市: "#7FA4CA",
  百色市: "#EEFEAC",
  玉林市: "#D7FEB0",
  贵港市: "#8190CC",
  来宾市: "#8C84CF",
  贺州市: "#AD85C6",
  河池市: "#7CB8C7",
  崇左市: "#FDD8A3",
  梧州市: "#E26A30"
}

export const YEAR_COLORS: Record<string, string> = {
  明代及以前: "#C4B0D9",
  清代: "#A8CBE8",
  民国: "#A8E6B4",
  建国后: "#E8B0B8",
  改革开放后: "#D4C4A0",
  现代: "#A0CCC8"
}

export const CITY_LIST = Object.keys(CITY_COLORS)
export const YEAR_LIST = Object.keys(YEAR_COLORS)

export function getGXBuildingCityColor(city: string): string {
  return CITY_COLORS[city] || "#ff0000"
}

export function getGXBuildingCityStyle(city: string) {
  const color = CITY_COLORS[city] || "#ff0000"
  return { color: "#333", background: color, borderColor: color }
}

export function getBuildingYearStyle(buildYear: string) {
  if (!buildYear) return { color: "#666", background: "#f5f5f5", borderColor: "#ddd" }
  const yearColors: Record<string, { color: string; background: string; borderColor: string }> = {
    "明（1368-1644年）及明代以前": { color: "#8B4513", background: "#FFF8DC", borderColor: "#DEB887" },
    "清（1644-1911年）": { color: "#2F4F4F", background: "#E0FFFF", borderColor: "#87CEEB" },
    "民国（1911-1949年）": { color: "#B22222", background: "#FFE4E1", borderColor: "#F08080" },
    "建国后（1949-1978年）": { color: "#8B0000", background: "#FFEBEE", borderColor: "#FF8A80" },
    "1949-1979年": { color: "#8B0000", background: "#FFEBEE", borderColor: "#FF8A80" },
    "1980年以后": { color: "#4169E1", background: "#F0F8FF", borderColor: "#87CEFA" }
  }
  for (const [period, style] of Object.entries(yearColors)) {
    if (buildYear.includes(period) || buildYear === period) return style
  }
  return { color: "#666", background: "#f9f9f9", borderColor: "#e0e0e0" }
}

export function getSimplifiedYear(buildYear: string): string {
  if (!buildYear) return "未知年代"
  const yearMap: Record<string, string> = {
    "明（1368-1644年）及明代以前": "明代及以前",
    "清（1644-1911年）": "清代",
    "民国（1911-1949年）": "民国",
    "建国后（1949-1978年）": "建国后",
    "1949-1979年": "建国后",
    "1980年以后": "改革开放后"
  }
  for (const [period, simple] of Object.entries(yearMap)) {
    if (buildYear.includes(period) || buildYear === period) return simple
  }
  return buildYear
}

export function getBuildingStructureStyle(structureType: string) {
  if (!structureType) return { color: "#666", background: "#f5f5f5", borderColor: "#ddd" }
  const structureColors: Record<string, { color: string; background: string; borderColor: string }> = {
    砖木结构: { color: "#8B4513", background: "#FDF5E6", borderColor: "#D2B48C" },
    砖混结构: { color: "#2F4F4F", background: "#F0F8FF", borderColor: "#B0C4DE" },
    钢混结构: { color: "#708090", background: "#F8F8FF", borderColor: "#C0C0C0" },
    木结构: { color: "#8FBC8F", background: "#F0FFF0", borderColor: "#90EE90" },
    砖石结构: { color: "#A0522D", background: "#FFF8DC", borderColor: "#DEB887" },
    混合结构: { color: "#9932CC", background: "#F8F0FF", borderColor: "#DDA0DD" },
    其他: { color: "#696969", background: "#F5F5F5", borderColor: "#D3D3D3" }
  }
  for (const [type, style] of Object.entries(structureColors)) {
    if (structureType.includes(type) || structureType === type) return style
  }
  return { color: "#666", background: "#f9f9f9", borderColor: "#e0e0e0" }
}

export function getSimplifiedStructure(structureType: string): string {
  if (!structureType) return "未知结构"
  return structureType
}

export function getIconUrlByLabel(label: string, isGray = false): string {
  switch (label) {
    case "Commercial Buildings": return isGray ? "gray.ico" : "blue.ico"
    case "Industrial Buildings": return isGray ? "gray.ico" : "yellow.ico"
    case "Military Buildings": return isGray ? "gray.ico" : "red.ico"
    case "Public Buildings": return isGray ? "gray.ico" : "pink.ico"
    case "Religious Buildings": return isGray ? "gray.ico" : "orange.ico"
    case "Residential Buildings": return isGray ? "gray.ico" : "green.ico"
    default: return isGray ? "gray.ico" : "red.ico"
  }
}

export function createColoredMarkerIcon(color: string): string {
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
  return "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svgIcon)))
}

export function createColoredDotIcon(color: string, size = 20): string {
  const svgIcon = `
    <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
      <circle cx="${size / 2}" cy="${size / 2}" r="${size / 2 - 1}" fill="${color}" stroke="#fff" stroke-width="1"/>
    </svg>
  `
  return "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svgIcon)))
}

export async function getGXBuildingMarkerColor(buildingName: string): Promise<string> {
  try {
    const path = `/buildingDescriptions/${encodeURIComponent(buildingName + ".json")}`
    const resp = await fetch(path)
    if (resp.ok) {
      const data = await resp.json()
      return CITY_COLORS[data.city || ""] || "#ff0000"
    }
  } catch {
    // ignore
  }
  return "#ff0000"
}
