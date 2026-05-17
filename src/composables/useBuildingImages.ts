async function checkImageExists(url: string): Promise<boolean> {
  return new Promise((resolve) => {
    const img = new Image()
    img.onload = () => resolve(true)
    img.onerror = () => resolve(false)
    img.src = url
  })
}

async function getFirstAvailableImage(folderPath: string, index: number): Promise<string> {
  const formats = ["jpg", "jpeg", "png", "webp", "gif", "bmp"]
  for (const fmt of formats) {
    const path = `${folderPath}/${index}.${fmt}`
    if (await checkImageExists(path)) return path
  }
  return `${folderPath}/${index}.jpg`
}

async function getFirstAvailableImageForBuilding(folderPath: string, labelPath: string, index: number): Promise<string> {
  const formats = ["jpg", "jpeg", "png", "webp", "gif", "bmp"]
  for (const fmt of formats) {
    const path = `${folderPath}/${labelPath}_${index}.${fmt}`
    if (await checkImageExists(path)) return path
  }
  return `${folderPath}/${labelPath}_${index}.jpg`
}

export async function getBuildingImages(buildingLabel: string, buildingCategory: string): Promise<string[]> {
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
  const categoryPath = buildingCategory.toLowerCase().replace(" ", "_")
  const labelPath = buildingLabel.replace(" ", "_")
  const folderPath = `/buildingPic/${categoryPath}/${labelPath}`
  const promises = Array.from({ length: 10 }, (_, i) =>
    getFirstAvailableImageForBuilding(folderPath, labelPath, i + 1)
  )
  return Promise.all(promises)
}

export async function getGXBuildingImages(buildingLabel: string): Promise<string[]> {
  const folderPath = `/GXbuildingsData/image/${buildingLabel}`
  const found: string[] = []
  const MAX_PROBE = 40
  let misses = 0

  for (let i = 1; i <= MAX_PROBE && misses < 3; i++) {
    const url = await getFirstAvailableImage(folderPath, i)
    if (await checkImageExists(url)) {
      found.push(url)
      misses = 0
    } else {
      misses++
    }
  }

  return found.length > 0 ? found : [`${folderPath}/1.jpg`]
}
