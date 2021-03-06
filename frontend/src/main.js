import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import axios from 'axios'

import globalVariable from './components/globalVariable.js'
Vue.prototype.globalVariable = globalVariable

Vue.use(ElementUI);
Vue.prototype.$axios = axios
Vue.prototype.$url = 'http://localhost:8000/'

new Vue({
  el: '#app',
  render: h => h(App)
});
