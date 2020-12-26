export default {
  namespaced: true,
  state: {
    user: '',
    exercise_data: [],
    errored: false
  },
  mutations: {
    reset_exercise_data (state) {
      state.exercise_data = []
    },
    set_modified_exercise_data (state, exerciseData) {
      var modifyResult = exerciseData['data']['user_exercise_data_list']
      modifyResult = modifyResult.map(function (value) {
        value['daily_rank'] = value['daily_rank'] + '位'
        // 曜日に合わせて列の色を変える
        if (value['weeknumber'] === '6') {
          value['_rowVariant'] = 'info'
        }
        if (value['weeknumber'] === '0') {
          value['_rowVariant'] = 'danger'
        }
        return value
      })
      state.exercise_data = modifyResult
    },
    set_user (state, user) {
      state.user = user
    },
    set_errored (state, errored) {
      state.errored = errored
    }
  },
  actions: {
    search ({ commit, state }, userName) {
      if (userName !== state.user) {
        commit('view/start', null, { root: true })
        commit('set_user', userName)

        this._vm.$api.get('https://api.ringfit.work/api/user?user=' + userName).then(res => {
          commit('set_modified_exercise_data', res)
          commit('set_errored', false)
          commit('view/end', null, { root: true })
        }).catch(
          error => {
            console.log(error)
            commit('set_errored', true)
            commit('view/end', null, { root: true })
          })
      }
    },
    reset ({commit}) {
      console.log('reset')
      commit('set_user', '')
      commit('reset_exercise_data')
      commit('set_errored', false)
    }
  }
}
