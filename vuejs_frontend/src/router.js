import Vue from 'vue'
import VueRouter from 'vue-router'
// ルート用のコンポーネントを読み込む
import Ranking from '@/views/Ranking'
import MonthlyRanking from '@/views/MonthlyRanking'
import User from '@/views/User'
import About from '@/views/About'
import Questions from '@/views/Questions'
import NotFound from '@/views/NotFound'
import store from './store.js'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    // 当日のランキングを表示
    {
      path: '/',
      component: Ranking,
      meta: { title: 'Ranking', desc: '運動記録のデイリーランキングを表示します' }
    },
    // 月別のランキングを表示
    {
      path: '/monthly',
      component: MonthlyRanking,
      meta: { title: 'Monthly Ranking', desc: '運動記録の月別ランキングを表示します' }
    },
    // ユーザ毎の結果ページ
    {
      path: '/user',
      component: User,
      meta: { title: 'User', desc: '今までの運動記録をユーザ毎に表示します' }
    },
    {
      path: '/user/:Username',
      component: User,
      meta: { title: 'User', desc: '今までの運動記録をユーザ毎に表示します' }
    },
    {
      path: '/about',
      component: About,
      meta: { title: 'About', desc: 'RingFitRankerについての説明です' }
    },
    {
      path: '/questions',
      component: Questions,
      meta: { title: 'Q&A', desc: 'よくある質問に対しての回答です' }
    },
    { path: '*',
      component: NotFound,
      meta: { title: 'URL Not Found', desc: 'ページが見つかりません' }
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
