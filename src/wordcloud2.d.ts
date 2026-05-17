declare module "wordcloud" {
  interface Options {
    list: [string, number][]
    gridSize?: number
    weightFactor?: number | ((size: number) => number)
    fontFamily?: string
    fontWeight?: string | number | ((word: string, weight: number) => string | number)
    color?: string | ((word: string, weight: number, fontSize: number, distance: number, theta: number) => string)
    backgroundColor?: string
    minSize?: number
    rotateRatio?: number
    rotationSteps?: number
    shuffle?: boolean
    shape?: string
    ellipticity?: number
    classes?: string | ((word: string, weight: number) => string)
    hover?: (item: [string, number] | null, dimension: object | undefined, event: MouseEvent) => void
    click?: (item: [string, number]) => void
    clearCanvas?: boolean
    drawOutOfBound?: boolean
    shrinkToFit?: boolean
    origin?: [number, number]
    minRotation?: number
    maxRotation?: number
    wait?: number
  }

  function WordCloud(canvas: HTMLCanvasElement | HTMLElement | HTMLElement[], options: Options): void
  export default WordCloud
}
