import Vue from 'vue'
import { BootstrapVue, IconsPlugin, NavbarPlugin } from 'bootstrap-vue'
import router from './router.js'
import App from './App.vue'
import store from './store.js'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(NavbarPlugin)

// eslint-disable-next-line no-new
new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App)
})
