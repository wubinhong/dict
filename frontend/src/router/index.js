import Vue from 'vue'
import VueRouter from "vue-router";
import Dashboard from "../views/Dashboard.vue";
import Post from "../views/Post.vue";
import Settings from "../views/Settings.vue";

Vue.use(VueRouter)

const router = new VueRouter({
    mode: "history",
    routes: [{
        path: "/dashboard", component: Dashboard, alias: "/"
    }, {
        path: '/post/:id', component: Post, props: true
    }, {
        path: '/settings', component: Settings
    }]
});

export default router