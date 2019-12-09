module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  // backend proxy
  devServer: {
    proxy: {
      '^/backend': {
        target: 'http://localhost:5000', pathRewrite: { '^/backend': '' },
        secure: false, changeOrigin: true
      },
      '^/youdao': {
        target: 'http://dict.youdao.com', pathRewrite: { '^/youdao': '' },
        secure: false, changeOrigin: true
      }
    }
  }
}