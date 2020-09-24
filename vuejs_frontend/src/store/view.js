export default {
  namespaced: true,
  state: {
    loading: false
  },
  mutations: {
    start (state) {
      console.log('state true')
      state.loading = true
    },
    end (state) {
      console.log('state false')
      state.loading = false
    }
  }
}
