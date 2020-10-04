export default {
  namespaced: true,
  state: {
    wait_num: 0,
    loading: false
  },
  mutations: {
    start (state) {
      state.wait_num = state.wait_num + 1
      state.loading = true
    },
    end (state) {
      state.wait_num = state.wait_num - 1
      state.loading = (state.wait_num !== 0)
    }
  }
}
