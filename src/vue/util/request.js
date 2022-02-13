import axios from 'axios'
import store from '../store/index'
import { Message } from 'element-ui'
import { uuid } from './common'
import Vue from 'vue'
import GlobalTips from '../component/Tips'
import { breathe } from '../api'

export const baseURL = 'http://127.6.6.6:23333'

// create an axios instance
const service = axios.create({
  baseURL: baseURL + '/api'
  // withCredentials: true, // send cookies when cross-domain requests
  // timeout: 7000 // request timeout
})

// request interceptor
service.interceptors.request.use(config => {
  if (store.getters.token) {
    config.headers['X-Token'] = store.getters.token
  }
  config.params = { ...config.params, rid: uuid() }
  return config
}, error => {
  console.log(error) // for debug
  return Promise.reject(error)
})

// response interceptor
service.interceptors.response.use(
  response => {
    const resp = response.data
    if (resp.status === 200) {
      return resp.data
    } else if (resp.status === 401) { // 非最近请求客户端
      const tips = Vue.prototype.$tipsInstance
      console.log(tips)
      if (tips && tips.tipsName !== 'NOT_CURRENT_CLIENT') {
        tips.close()
      }
      GlobalTips({
        tipsName: 'NOT_CURRENT_CLIENT',
        spinner: '<i class="el-icon-connection" style="color: #de7d01"></i>',
        text: '<span style="color: #de7d01">与WEBUI服务端失去连接...</span>',
        buttons: [{
          text: '重新连接',
          click: async function() {
            await store.dispatch('app/getToken').then(async() => {
              const tips = Vue.prototype.$tipsInstance
              if (tips && tips.tipsName === 'NOT_CURRENT_CLIENT') {
                tips.close()
              }
              Message({ message: '已重新连接上WEBUI服务端', type: 'success', duration: 3.6 * 1000 })
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
        }]
      })
      return Promise.reject(new Error(resp.message || 'Error'))
    } else {
      const message = resp.message
      Message({ message: message || 'Error', type: 'error', duration: 3.6 * 1000 })
      return Promise.reject(new Error(message || 'Error'))
    }
  },
  error => {
    const errMsg = error.message
    if (/.*Network Error.*/i.test(errMsg)) {
      Message({ message: 'WEBUI服务可能已关闭，请重新启动', type: 'info', duration: 3.6 * 1000 })
    } else {
      Message({ message: errMsg, type: 'error', duration: 3.6 * 1000 })
    }
    return Promise.reject(error)
  }
)

export default service

