import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '../views/Layout.vue'
import Dashboard from '../views/Dashboard/index.vue'
import WordDetail from '../views/Dashboard/WordDetail.vue'
// @ is an alias to /src
import Settings from '@/views/Home/Settings.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'layout',
    redirect: {name: 'myBoard'},
    component: Layout,
    children: [{
      path: 'dashboard', component: Dashboard, name: 'myBoard'
    }, {
      path: 'dashboard/word/:name', component: WordDetail, name: 'wordDetail'
    }, {
      path: 'home/settings', component: Settings
    }]
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/login',
    component: () => import('../views/Login.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

// eslint-disable-next-line no-console
// console.log(router)

export default router
