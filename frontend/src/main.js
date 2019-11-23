import Vue from 'vue'
import './plugins/element.js'
import router from './router/index.js'
import axios from 'axios' // http request component
import App from './App.vue'

Vue.config.productionTip = false
Vue.prototype.$axios = axios

new Vue({
  // render: h => h(App),
  ...App,
  router
}).$mount('#app')
