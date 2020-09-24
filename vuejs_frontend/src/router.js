import Vue from 'vue'
import VueRouter from 'vue-router'
// ルート用のコンポーネントを読み込む
import Ranking from '@/views/Ranking'
import User from '@/views/User'
import About from '@/views/About'
import store from './store.js'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    // 当日のランキングを表示
    {
      path: '/',
      component: Ranking
    },
    // ユーザ毎の結果ページ
    {
      path: '/user',
      component: User
    },
    {
      path: '/about',
      component: About
    }
  ]
})

// ルーターナビゲーションの前にフック
router.beforeEach((to, from, next) => {
  store.commit('view/start')
  next()
})
// ルーターナビゲーションの後にフック
router.afterEach(() => {
  store.commit('view/end')
})

export default router
