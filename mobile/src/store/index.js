import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    snackbar: {
      showed: false,
      color: "success",
      timeout: 2000,
      message: "Default snackbar message!"
    }
  },
  mutations: {
    showSnackbar(state, payload) {
      // expand operator can makes it easy to implement the apply method
      state.snackbar = {...state.snackbar, ...payload, showed: true}
      state.snackbar.multiline = (state.snackbar.message.length > 50) ? true : false
    },
    closeSnackbar(state) {
      state.snackbar.visible = false
      state.snackbar.color = null
      state.snackbar.text = null
    }
  },
  actions: {
  },
  modules: {
  }
})
