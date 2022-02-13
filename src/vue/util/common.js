// 睡眠函数，在调用的函数上需加上 async，调用它需要加 await
// e.g. async function exec() { ... await sleep(1000) ... }
import { Message } from 'element-ui'
import axios from 'axios'

export function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * 十六进制颜色转换为RGB颜色
 * @param color
 * @param isArr
 * @return string | []
 */
export function colorHexToRGB(color, isArr) {
  color = color.toUpperCase()
  color = color.startsWith('#') ? color : '#' + color
  if (/^#[0-9a-fA-F]{3,6}/.test(color)) {
    const hexArray = []
    let count = 1
    for (var i = 1; i <= 3; i++) {
      if (color.length - 2 * i > 3 - i) {
        hexArray.push(Number('0x' + color.substring(count, count + 2)))
        count += 2
      } else {
        hexArray.push(Number('0x' + color.charAt(count) + color.charAt(count)))
        count += 1
      }
    }
    return isArr ? hexArray : 'RGB(' + hexArray.join(',') + ')'
  } else {
    return color
  }
}

/**
 * 获取UUID
 * @returns {string}
 */
export function uuid() {
  const url = URL.createObjectURL(new Blob())
  const uuid = url.toString()
  URL.revokeObjectURL(url)
  return uuid.substr(uuid.lastIndexOf('/') + 1)
}

/**
 * 字节单位转换 -> B|KB|MB|GM
 * @param byte 字节数
 * @returns {string}
 */
export function convertBit(byte) {
  byte = parseInt(byte)
  let size
  if (byte < 0.1 * 1024) { // 如果小于0.1KB转化成B
    size = byte.toFixed(2) + 'B'
  } else if (byte < 0.1 * 1024 * 1024) { // 如果小于0.1MB转化成KB
    size = (byte / 1024).toFixed(2) + 'KB'
  } else if (byte < 0.1 * 1024 * 1024 * 1024) { // 如果小于0.1GB转化成MB
    size = (byte / (1024 * 1024)).toFixed(2) + 'MB'
  } else { // 其他转化成GB
    size = (byte / (1024 * 1024 * 1024)).toFixed(2) + 'GB'
  }

  const sizeStr = size + ''
  const len = sizeStr.indexOf('\.')
  const dec = sizeStr.substr(len + 1, 2)
  if (dec === '00') { // 当小数点后为00时 去掉小数部分
    return sizeStr.substring(0, len) + sizeStr.substr(len + 3, 2)
  }
  return sizeStr
}

/**
 * 下载文件
 * @param url
 * @param fileName
 */
export function downloadFile(url, fileName) {
  axios.request({
    url: url,
    method: 'get',
    responseType: 'blob',
    timeout: 1000 * 60 * 5
  }).then(resp => {
    const blob = resp.data
    if (window.navigator.msSaveOrOpenBlob) {
      navigator.msSaveBlob(blob, fileName)
    } else {
      const link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = fileName
      link.click()
      window.URL.revokeObjectURL(link.href)
    }
  }).catch((err) => {
    console.log(err)
    Message({
      message: '文件下载失败',
      type: 'error',
      duration: 3.6 * 1000
    })
  })
}

/**
 * 判断是否为指向图片的URL
 * @param url
 */
export function isImageUrl(url) {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.onload = () => {
      resolve(true)
    }
    img.onerror = () => {
      reject(new Error('图片加载失败'))
    }
    img.src = url
  })
}

/**
 * 字符串Hash值
 * @param str
 * @returns {number}
 */
export function hashCode(str) {
  let hash = 0
  if (!str || str.length === 0) return hash
  for (let i = 0; i < str.length; i++) {
    const chr = str.charCodeAt(i)
    hash = ((hash << 5) - hash) + chr
    hash |= 0 // Convert to 32bit integer
  }
  return hash
}

/**
 * 深拷贝
 * @param target
 * @return {{}}
 */
export function deepClone(target) {
  // 定义一个变量
  let result
  // 如果当前需要深拷贝的是一个对象的话
  if (typeof target === 'object') {
    // 如果是一个数组的话
    if (Array.isArray(target)) {
      result = [] // 将result赋值为一个数组，并且执行遍历
      for (const i in target) {
        // 递归克隆数组中的每一项
        result.push(deepClone(target[i]))
      }
      // 判断如果当前的值是null的话；直接赋值为null
    } else if (target === null) {
      result = null
      // 判断如果当前的值是一个RegExp对象的话，直接赋值
    } else if (target.constructor === RegExp) {
      result = target
    } else {
      // 否则是普通对象，直接for in循环，递归赋值对象的所有值
      result = {}
      for (const i in target) {
        result[i] = deepClone(target[i])
      }
    }
    // 如果不是对象的话，就是基本数据类型，那么直接赋值
  } else {
    result = target
  }
  // 返回最终结果
  return result
}

/**
 * URL参数拼接
 * @param url e.g.https://www.baidu.com  https://www.baidu.com?a=1&
 * @param data e.g.{b=2}
 * @return {String}
 */
export function formatURL(url, data) {
  let tmpURL = ''
  for (const k in data) {
    const value = data[k] !== undefined ? data[k] : ''
    tmpURL += ('&' + k + '=' + encodeURIComponent(value))
  }
  const params = tmpURL ? tmpURL.substring(1) : ''
  url += ((url.indexOf('?') < 0 ? '?' : (url.endsWith('&') ? '' : '&')) + params)
  return url
}

/**
 * 获取URL参数
 * @param url url
 * @return {Object}
 */
export function getURLParams(url) {
  const params = {}
  const idx = url.indexOf('?')
  if (idx !== -1) {
    const str = url.substr(idx + 1)
    const strArr = str.split('&')
    for (let i = 0; i < strArr.length; i++) {
      params[strArr[i].split('=')[0]] = unescape(strArr[i].split('=')[1])
    }
  }
  return params
}

