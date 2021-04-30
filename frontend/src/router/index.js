import Vue from 'vue'
import Router from 'vue-router'
import EasyLatexPage from '@/components/EasyLatex_Page'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'EasyLatexPage',
      component: EasyLatexPage
    }
  ]
})
