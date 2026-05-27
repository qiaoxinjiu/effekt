// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import ElementUI from 'element-ui';
import store from '@/vuex/store'
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'

function applyInitialTheme() {
  const theme = localStorage.getItem('uiTheme') || 'dark'
  document.body.classList.remove('theme-dark', 'theme-light')
  document.body.classList.add(theme === 'light' ? 'theme-light' : 'theme-dark')
}
applyInitialTheme()

Vue.use(ElementUI);
Vue.prototype.$axios = axios

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
