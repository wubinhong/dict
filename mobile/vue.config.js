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
        }
    }
}
}