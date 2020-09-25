import Vue from 'vue'
import Datepicker from 'vuejs-datepicker'
import {ja} from 'vuejs-datepicker/dist/locale'
import { BootstrapVue, IconsPlugin, NavbarPlugin } from 'bootstrap-vue'
import router from './router.js'
import App from './App.vue'
import store from './store.js'
import axios from 'axios'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)

// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(NavbarPlugin)

Vue.use({
  install (Vue) {
    Vue.prototype.$api = axios.create({
      baseURL: 'https://ringfit.work/api'
    })
  }
})

Datepicker.props.language.default = () => ja
Datepicker.props.format.default = () => 'yyyy-MM-dd'

Vue.use({
  install (Vue) {
    Vue.component('Datepicker', Datepicker)
  }
})

// eslint-disable-next-line no-new
new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App)
})
