import Vue from 'vue'
import Tips from './Tips.vue'

const Constructor = Vue.extend(Tips)

const GlobalTips = function(options = {}) {
  const instance = new Constructor()
  instance.$mount()
  document.body.appendChild(instance.$el)
  // set options start
  instance.tipsName = options.tipsName || 'default'
  if (options.background) {
    instance.background = options.background
  }
  if (options.text) {
    instance.text = options.text
  }
  if (options.spinner) {
    instance.spinner = options.spinner
  }
  if (options.customClass) {
    instance.customClass = options.customClass
  }
  if (options.buttons && options.buttons.length > 0) {
    instance.buttons = options.buttons
  }
  // set options end
  Vue.prototype.$tipsInstance = instance
  instance.getCurrentInstance = () => { return Vue.prototype.$tipsInstance }
  instance.close = () => {
    Vue.prototype.$tipsInstance = undefined
    document.body.removeChild(instance.$el)
  }
  return instance
}

export default GlobalTips
