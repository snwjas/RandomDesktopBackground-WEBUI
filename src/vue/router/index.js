import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/404',
      component: () => import('../view/404.vue'),
      meta: { title: '404' },
      hidden: true
    },
    // 首页
    {
      path: '/',
      name: 'Index',
      meta: { title: '' },
      component: () => import('../view/Home.vue')
      // component: () => import('../component/Tips.vue')
    },
    {
      path: '/type',
      name: 'Type',
      meta: { title: '设置wallhaven图源' },
      component: () => import('../view/Type.vue')
    },
    // 404 page must be placed at the end !!!
    { path: '*', redirect: '/404', hidden: true }
  ]
})
