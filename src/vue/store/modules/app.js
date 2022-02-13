import { connect, getConfig, getStatus } from '../../api/index'

const state = () => {
  return {
    config: {},
    status: {},
    token: ''
  }
}

const mutations = {
  SET_CONFIG: (state, config) => {
    state.config = config
  },
  SET_STATUS: (state, status) => {
    state.status = status
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  }
}

const actions = {
  getToken({ commit }) {
    return new Promise((resolve, reject) => {
      connect().then(resp => {
        commit('SET_TOKEN', resp)
        resolve(resp)
      }).catch(error => {
        reject(error)
      })
    })
  },
  getConfig({ commit }) {
    return new Promise((resolve, reject) => {
      getConfig().then(resp => {
        commit('SET_CONFIG', resp)
        resolve(resp)
      }).catch(error => {
        reject(error)
      })
    })
  },
  getStatus({ commit }) {
    return new Promise((resolve, reject) => {
      getStatus().then(resp => {
        commit('SET_STATUS', resp)
        resolve(resp)
      }).catch(error => {
        reject(error)
      })
    })
  }
}

export default {
  namespaced: true,
  state: state,
  mutations: mutations,
  actions: actions
}

