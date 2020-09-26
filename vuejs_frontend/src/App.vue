<template>
  <div id="app">
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
  }
}
</script>
