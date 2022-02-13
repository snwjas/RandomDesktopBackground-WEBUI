import Vue from 'vue'
import App from './App.vue'
import router from './router/index.js'
import store from './store/index.js'
import { breathe } from './api'
import GlobalTips from './component/Tips.js'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

import './asset/style.scss' // 全局样式
import './asset/icon/iconfont.css' // 图标

Vue.use(ElementUI)

// 全局组件
Vue.prototype.$tips = GlobalTips

// 禁用按键
document.oncontextmenu = () => { return false }
document.onkeydown = (e) => {
  const kc = e.keyCode
  if (kc === 123) { return false }
  if ((e.ctrlKey) && (kc === 83)) { return false }
}

const appName = '随机桌面壁纸'
router.beforeEach(async(to, from, next) => {
  // 修改页面title
  document.title = to.meta && to.meta.title ? `${to.meta.title} | ${appName}` : appName
  try {
    if (!store.getters.token) {
      await store.dispatch('app/getToken').then(async() => {
        const tips = Vue.prototype.$tipsInstance
        if (tips && tips.tipsName === 'NOT_CURRENT_CLIENT') {
          tips.close()
        }
        await store.dispatch('app/getStatus')
        await store.dispatch('app/getConfig')
        const loop = setInterval(() => {
          breathe().then(resp => {
            if (!(typeof resp === 'boolean' && resp)) {
              clearInterval(loop)
            }
          }).catch(() => {
            clearInterval(loop)
          })
        }, 60000)
      })
    }
    if (store.getters.token && Object.keys(store.getters.status).length === 0) {
      await store.dispatch('app/getStatus')
    }
    if (store.getters.token && Object.keys(store.getters.config).length === 0) {
      await store.dispatch('app/getConfig')
    }
  } catch (e) {
    // Message.error(e || 'Has Error!')
  }
  next()
})
router.afterEach(() => {

})

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})

