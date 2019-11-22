import Vue from 'vue'
import './plugins/element.js'
import router from './router/index.js'
import App from './App.vue'

Vue.config.productionTip = false

new Vue({
  // render: h => h(App),
  ...App,
  router
}).$mount('#app')
