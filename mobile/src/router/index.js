import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '../views/Layout.vue'
import Dashboard from '../views/Dashboard/index.vue'
import Dashboard2 from '../views/Dashboard/index2.vue'
import WordDetail from '../views/Dashboard/WordDetail.vue'
import Admin from '../views/Admin/index.vue'
import AdminDetail from '../views/Admin/AdminDetail.vue'
import Tool from '../views/Tool/index.vue'
import History from '../views/Tool/History.vue'
import Dict from '../views/Tool/Dict.vue'
// @ is an alias to /src
import Settings from '@/views/Home/Settings.vue'

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'layout',
        redirect: {name: 'myBoard2'},
        component: Layout,
        children: [{
            path: 'dashboard', component: Dashboard, name: 'myBoard'
        }, {
            path: 'dashboard2', component: Dashboard2, name: 'myBoard2'
        }, {
            path: 'dashboard/word', component: WordDetail, name: 'wordDetail'
        }, {
            path: 'home/settings', component: Settings
        }, {
            path: 'admin', component: Admin
        }, {
            path: 'admin/detail', component: AdminDetail, name: 'adminDetail'
        }, {
            path: 'tool', component: Tool
        }, {
            path: 'tool/history', component: History
        }, {
            path: 'tool/dict', component: Dict
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
];

const router = new VueRouter({
    mode: 'history',
    routes
});

// eslint-disable-next-line no-console
// console.log(router)

export default router
