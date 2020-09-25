<template>
  <div id="app">
    <navbar></navbar>
    <!-- ここにパスと一致したコンポーネントが埋め込まれる -->
    <transition name="view">
    <router-view />
    </transition>
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
