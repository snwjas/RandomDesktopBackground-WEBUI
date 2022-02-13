import request, { baseURL } from '../util/request'
import { uuid } from '../util/common'
import axios from 'axios'

export const wallhaven_url = 'https://wallhaven.cc'

/**
 * 连接服务，认证
 * @return {AxiosPromise}
 */
export function connect() {
  return request({
    url: '/connect',
    method: 'get',
    headers: { 'X-Init': uuid() }
  })
}

/**
 * 获取 wallhaven 壁纸列表数据
 * @data data
 * @returns {AxiosPromise}
 */
export function getBgs(data) {
  return request({
    method: 'post',
    url: '/wallhaven',
    data
  })
}

/**
 * 用来验证apikey是否可以
 * @return {Promise<AxiosResponse<any>>}
 * @param data
 */
export function getBgsWF(data) {
  return request({
    method: 'post',
    url: '/wallhaven',
    timeout: 5000,
    data
  })
}

/**
 * App心跳
 * @return {AxiosPromise}
 */
export function breathe() {
  return request({
    url: '/breathe',
    method: 'get'
  })
}

/**
 * 选择工作目录
 * @return {AxiosPromise}
 */
export function selectFolder() {
  return request({
    url: '/config/workdir',
    method: 'get'
  })
}

/**
 * 获取配置信息
 * @return {AxiosPromise}
 */
export function getConfig() {
  return request({
    url: '/config',
    method: 'get'
  })
}

/**
 * 更新配置信息
 * @return {AxiosPromise}
 */
export function updateConfig(data) {
  return request({
    url: '/config',
    method: 'post',
    data
  })
}

/**
 * 获取状态信息
 * @return {AxiosPromise}
 */
export function getStatus() {
  return request({
    url: '/status',
    method: 'get'
  })
}

/**
 * 创建桌面快捷方式
 * @return {AxiosPromise}
 */
export function createDesktopLnk() {
  return request({
    url: '/create-desktop-lnk',
    method: 'get'
  })
}

/**
 * 打开收藏文件夹
 * @return {AxiosPromise}
 */
export function locateFavoritePath() {
  return request({
    url: '/locate-favorite-path',
    method: 'get'
  })
}

/**
 * 切换程序开关
 * @return {AxiosPromise}
 */
export function toggleUd() {
  return request({
    url: '/toggle-ud',
    method: 'get'
  })
}
