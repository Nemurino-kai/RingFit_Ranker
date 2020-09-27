<template>
  <div id="app">
    <go-top :size=60 :bottom=50 bg-color="#000000"></go-top>
    <navbar></navbar>
    <!-- ここにパスと一致したコンポーネントが埋め込まれる -->
    <router-view />
    <!-- オーバーレイ用のコンポーネント -->
    <Loading
    :active.sync="this.$store.state.view.loading"
    :is-full-page="true"
    loader="bars"></Loading >
    <app-footer></app-footer>
  </div>
</template>

<script>
import Footer from './components/Footer.vue'
import Navbar from './components/Navbar.vue'

export default {
  components: {
    'app-footer': Footer,
    Navbar
  },
  methods: {
    createTitleDesc: function (routeInstance) {
      // タイトルを設定
      if (routeInstance.meta.title) {
        var setTitle = routeInstance.meta.title
        document.title = setTitle
      } else {
        document.title = 'RingFitRanker'
      }
      // メタタグdescription設定
      if (routeInstance.meta.desc) {
        var setDesc = routeInstance.meta.desc
        document.querySelector("meta[name='description']").setAttribute('content', setDesc)
      } else {
        document.querySelector("meta[name='description']").setAttribute('content', 'description is not set')
      }
    }
  },
  mounted: function () {
    var routeInstance = this.$route
    this.createTitleDesc(routeInstance)
  },
  watch: {
    '$route' (routeInstance, from) {
      this.createTitleDesc(routeInstance)
    }
  }
}
</script>
