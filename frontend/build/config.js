'use strict'

module.exports = {
  port: 4000,
  title: 'Vue-Element-Starter',
  // when you use electron please set to relative path like ./
  // otherwise only set to absolute path when you're using history mode
  publicPath: '/',
  // backend rest api proxy
  backendProxyTarget: 'http://localhost:5000',
  // add these dependencies to a standalone vendor bundle
  vendor: [
    'vue',
    'vuex',
    'vue-router',
    'vuex-router-sync',
    'whatwg-fetch',
    'normalize.css',
    'offline-plugin/runtime',
    'element-ui',
    'material-design-icons'
  ]
}
