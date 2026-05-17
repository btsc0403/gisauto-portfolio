
import "leaflet/dist/leaflet.css"
import "leaflet"
import "mars2d/dist/mars2d.css"
import "mars2d"

import "./styles/glass.css"
import { createApp } from "vue"
import { createPinia } from "pinia"
import App from "./App.vue"
import router from "./router"

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount("#app")
