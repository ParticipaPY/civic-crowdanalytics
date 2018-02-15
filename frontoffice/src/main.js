// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue'
import App from './App'
import router from './router'
import Snotify from 'vue-snotify'
import ReadMore from 'vue-read-more'
import VueGoodTable from 'vue-good-table'

Vue.use(Snotify, {
  toast: {
    timeout: 5000,
    showProgressBar: false,
    position: 'rightTop'
  }
})
Vue.use(ReadMore)
Vue.use(VueGoodTable)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
