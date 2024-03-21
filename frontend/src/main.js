import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
// import './assets/js/rem'
import './assets/css/base.css'
import './assets/css/mine.css'
Vue.config.productionTip = false

import axios from 'axios'
axios.defaults.baseURL = "http://web:8000"; // 开发线上环境
// axios.defaults.baseURL = "http://localhost:8000"; // 开发线下本地环境
import api from "./views/api/api";
Vue.prototype.api = api;
Vue.prototype.$axios = axios

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
