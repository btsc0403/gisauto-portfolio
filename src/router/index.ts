import { createRouter, createWebHashHistory } from "vue-router"

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      name: "Map",
      component: () => import("../views/MapView.vue")
    },
    {
      path: "/introduce",
      name: "Introduce",
      component: () => import("../views/IntroduceView.vue")
    },
    {
      path: "/portfolio",
      name: "Portfolio",
      component: () => import("../views/PortfolioView.vue")
    }
  ]
})

export default router
