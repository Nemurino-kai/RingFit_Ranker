import Vue from 'vue'
import Vuex from 'vuex'
import view from '@/store/view.js'
import userRank from '@/store/userRank.js'
import dailyRank from '@/store/dailyRank.js'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    view,
    userRank,
    dailyRank
  }
})
