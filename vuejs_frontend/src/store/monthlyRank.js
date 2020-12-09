export default {

  namespaced: true,
  state: {
    // 4時間前の日付にシフトする
    defaultDate: new Date(new Date() - (1000 * 60 * 60 * 4)),
    disabledDates: {
      to: new Date(2020, 5 - 1, 18),
      from: new Date(new Date() - (1000 * 60 * 60 * 4))
    },
    errored: false,
    exercise_data: [],
    start_day: '',
    stop_day: ''
  },
  mutations: {
    set_modified_data (state, exerciseData) {
      var modifyResult = exerciseData['data']['exercise_data_list']
      modifyResult = modifyResult.map(function (value) {
        value['days'] = value['days'] + '日'
        return value
      })

      state.exercise_data = modifyResult
      state.start_day = exerciseData['data']['start_day']
      state.stop_day = exerciseData['data']['stop_day']
    },
    set_errored (state, errored) {
      state.errored = errored
    },
    set_default_date (state, defaultDate) {
      state.defaultDate = defaultDate
    }
  },
  actions: {
    search ({ commit }, date) {
      var url = 'https://ringfit.work/api/monthly'
      if (typeof date !== 'undefined') {
        url = url + '?month=' + date
        commit('set_default_date', date)
      }
      commit('view/start', null, { root: true })
      this._vm.$api.get(url).then(res => {
        commit('set_modified_data', res)
        commit('set_errored', false)
        commit('view/end', null, { root: true })
      })
        .catch(
          error => {
            console.log(error)
            commit('set_errored', true)
            commit('view/end', null, { root: true })
          })
    }
  }
}
