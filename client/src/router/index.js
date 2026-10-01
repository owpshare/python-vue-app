import { createRouter, createWebHistory } from 'vue-router'

// 1. Define your page/view components
// (Using lazy-loading to keep initial bundle sizes small)
const HomeView = () => import('../views/HomeView.vue')
const AboutView = () => import('../views/AboutView.vue')

// 2. Define the route paths
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  }
]

// 3. Create the router instance
const router = createRouter({
  // Using HTML5 History mode. Flask is already configured with 
  // a catch-all route to gracefully support this on Azure!
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
