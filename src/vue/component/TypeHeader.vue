<template>
  <header class="header clearfix">
    <div class="control-bar">
      <router-link to="/" class="btn el-icon-back">返回</router-link>
      <span class="btn el-icon-finished" @click="updateWallhavenURL">保存</span>
    </div>
    <div class="apikey">
      <el-popover v-model="apikeyDialogVisible" placement="left-end">
        <el-input v-model="apikeyInput" size="mini" clearable placeholder="请输入API密钥">
          <i
            slot="prefix"
            :style="{color: apikeyValid ? '#67c23a' : '#909399'}"
            :class="['el-input__icon',apikeyValid?'el-icon-success':'el-icon-question']"
          ></i>
        </el-input>
        <div style="text-align: center;margin-top: 12px;">
          <el-button size="mini" type="warning" :disabled="!apikeyInput" @click="checkApikey">测试</el-button>
          <el-button size="mini" type="primary" :disabled="!apikeyInput" @click="setApikey">保存</el-button>
        </div>
        <i slot="reference" class="el-icon-key" title="设置API密钥"></i>
      </el-popover>

    </div>
    <div class="search-bar">
      <div class="search-item">
        <div class="search-category-checks">
          <el-checkbox-button
            v-for="(val,key) in category"
            :key="key"
            v-model="category[key]['value']"
            true-label="1"
            false-label="0"
            class="el-checkbox-button--small"
          >{{ category[key]['name'] }}
          </el-checkbox-button>
        </div>
        <div class="search-purity-checks">
          <el-checkbox-button
            v-for="(val,key) in purity"
            :key="key"
            v-model="purity[key]['value']"
            true-label="1"
            false-label="0"
            class="el-checkbox-button--small"
            :title="purity[key]['tips']"
          >{{ purity[key]['name'] }}
          </el-checkbox-button>
        </div>
        <div class="search-resolutions" style="flex-wrap: wrap">
          <el-dropdown trigger="click">
            <el-button size="small" :type="resolutionSelectedEffect">
              {{
                resolutionSelectedEffect ? (isResolutionRadio ? `≥ ${resolutionRadioSelected}` :
                  `${resolutionCheckboxSelected[0]} +${resolutionCheckboxSelected.length}`) : '分辨率'
              }}
              <i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown" class="dropdown">
              <el-radio-group
                v-model="isResolutionRadio"
                size="small"
                class="resolution-framed"
                @change="resolutionSelectionChange"
              >
                <el-radio-button :label="true"><i class="el-icon-plus" /> 最低分辨率</el-radio-button>
                <el-radio-button :label="false"><i class="el-icon-aim" /> 精确分辨率</el-radio-button>
              </el-radio-group>
              <div class="native-info">当前显示器分辨率为 <strong>
                <em>{{ `${screen.width} × ${screen.height}` }}</em></strong>.
              </div>
              <div class="resolution-head clearfix">
                <span class="resolution-head-item">Ultrawide</span>
                <span class="resolution-head-item">16:9</span>
                <span class="resolution-head-item">16:10</span>
                <span class="resolution-head-item">4:3</span>
                <span class="resolution-head-item">5:4</span>
              </div>
              <div class="selected-group">
                <el-radio-group
                  v-if="isResolutionRadio"
                  v-model="resolutionRadioSelected"
                  @change="resolutionRadioSelectionChange"
                >
                  <div v-for="(items,index) in resolution" :key="index">
                    <el-radio-button
                      v-for="(val,key) in items"
                      :key="key"
                      :label="`${val[0]}x${val[1]}`"
                      class="el-radio-button--mini"
                      :style="{visibility: val.length > 0?'visibility': 'hidden'}"
                    >{{ val.length > 0 ? `${val[0]} × ${val[1]}` : '' }}
                    </el-radio-button>
                  </div>
                </el-radio-group>
                <el-checkbox-group v-else v-model="resolutionCheckboxSelected" @change="resolutionRadioSelectionChange">
                  <div v-for="(items,index) in resolution" :key="index">
                    <el-checkbox-button
                      v-for="(val,key) in items"
                      :key="key"
                      :label="`${val[0]}x${val[1]}`"
                      class="resolution-item el-checkbox-button--mini"
                      :style="{visibility: val.length > 0?'visibility': 'hidden'}"
                    >{{ val.length > 0 ? `${val[0]} × ${val[1]}` : '' }}
                    </el-checkbox-button>
                  </div>
                </el-checkbox-group>
              </div>
              <div class="custom-resolution">
                <span class="title">自定义分辨率</span>
                <el-input-number
                  v-model="customResolution.width"
                  placeholder="Width"
                  :min="0"
                  size="mini"
                  @input="customResolutionChange"
                ></el-input-number>
                <span class="x">x</span>
                <el-input-number
                  v-model="customResolution.height"
                  placeholder="Height"
                  :min="0"
                  size="mini"
                  @input="customResolutionChange"
                ></el-input-number>
              </div>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </div>
      <div class="search-item">
        <div class="search-ratios">
          <el-dropdown trigger="click">
            <el-button size="small" :type="ratioSelectedEffect">
              {{ ratioSelectedText }}
              <i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <div class="ratio-head clearfix">
                <span class="ratio-head-item">Wide</span>
                <span class="ratio-head-item">Ultrawide</span>
                <span class="ratio-head-item">Portrait</span>
                <span class="ratio-head-item">Square</span>
              </div>
              <div class="selected-group">
                <el-checkbox-group v-model="ratioCheckboxSelected">
                  <el-checkbox-button
                    class="ratio-item ratio-all-wide el-checkbox-button--mini"
                    label="landscape"
                  >All Wide
                  </el-checkbox-button>
                  <el-checkbox-button
                    class="ratio-item ratio-all-portrait el-checkbox-button--mini"
                    label="portrait"
                  >All Portrait
                  </el-checkbox-button>
                  <div v-for="(items,index) in ratio" :key="index">
                    <el-checkbox-button
                      v-for="(val,key) in items"
                      :key="key"
                      :label="`${val[0]}x${val[1]}`"
                      class="ratio-item el-checkbox-button--mini"
                      :style="{visibility: val.length > 0?'visibility': 'hidden'}"
                    >{{ val.length > 0 ? `${val[0]} × ${val[1]}` : '' }}
                    </el-checkbox-button>
                  </div>
                </el-checkbox-group>
              </div>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
        <div class="search-colors">
          <el-dropdown trigger="click">
            <el-button
              size="small"
              :style="colorCheckboxSelected.length > 0
                ? {backgroundColor: `#${colorCheckboxSelected[0]}`,borderColor: `#${colorCheckboxSelected[0]}`,color:textHexColor}
                : {}"
            >
              {{ colorCheckboxSelected.length > 0 ? `色调 +${colorCheckboxSelected.length}` : '色调' }}
              <i class="el-icon-arrow-down el-icon--right" />
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <div class="selected-group">
                <el-checkbox-group v-model="colorCheckboxSelected">
                  <div v-for="(items,index) in color" :key="index">
                    <el-checkbox-button
                      v-for="(val,key) in items"
                      :key="key"
                      :label="val"
                      class="color-item el-checkbox-button--mini"
                    >
                      <div class="color" :style="val ? {backgroundColor: `#${val}`}:{}" />
                    </el-checkbox-button>
                    <span v-if="index===color.length-1" class="color-item">
                      <div class="el-checkbox-button__inner" style="margin: 3px 3px">
                        <span
                          class="color"
                          :style="{background:'linear-gradient(18deg, rgba(255,255,255,1) 42%,rgba(255,0,0,1) 45%,rgba(255,0,0,1) 55%,rgba(255,255,255,1) 58%)'}"
                          @click="colorCheckboxSelected=[]"
                        />
                      </div>
                    </span>
                  </div>
                </el-checkbox-group>
              </div>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
        <div class="search-sorting">
          <el-dropdown trigger="click" style="display: table-cell">
            <el-button size="small" type="primary" title="排序模式">
              {{ sortingText }}<i class="el-icon-arrow-down el-icon--right" />
            </el-button>
            <el-dropdown-menu slot="dropdown" style="padding: 10px">
              <div class="selected-group">
                <el-radio-group v-model="sortingRadioSelected">
                  <div v-for="(item,index) in sorting" :key="index">
                    <el-radio-button
                      :label="item.value"
                      class="sorting-item el-radio-button--mini"
                    >{{ item.name }}
                    </el-radio-button>
                  </div>
                </el-radio-group>
              </div>
            </el-dropdown-menu>
          </el-dropdown>
          <div
            :class="['search-order',order==='desc'?'el-icon-bottom':'el-icon-top']"
            @click="order=order==='desc'?'asc':'desc'"
          ><i /></div>
        </div>
        <div class="search-submit el-button el-button--primary el-button--small" @click="refresh">
          <i class="el-icon-refresh" />
        </div>
      </div>
    </div>
  </header>
</template>

<script>

import { colorHexToRGB, formatURL, getURLParams } from '../util/common'
import { getBgsWF, updateConfig, wallhaven_url } from '../api/index'
import { mapGetters } from 'vuex'

const category = {
  General: { name: '常规', tips: '常规', value: '1' },
  Anime: { name: '动画', tips: '动画', value: '1' },
  People: { name: '人物', tips: '人物', value: '1' }
}
const purity = {
  SFW: { name: 'SFW', tips: '工作时可以看的', value: '1' },
  Sketchy: { name: 'Sketchy', tips: '不确定的？', value: '0' },
  NSFW: { name: 'NSFW', tips: '工作时不要看的', value: '0' }
}

const resolution = [
  [[2560, 1080], [1280, 720], [1280, 800], [1280, 960], [1280, 1024]],
  [[3440, 1440], [1600, 900], [1600, 1000], [1600, 1200], [1600, 1280]],
  [[3840, 1600], [1920, 1080], [1920, 1200], [1920, 1440], [1920, 1536]],
  [[], [2560, 1440], [2560, 1600], [2560, 1920], [2560, 2048]],
  [[], [3840, 2160], [3840, 2400], [3840, 2280], [3840, 3072]]
]

const ratio = [
  [[16, 9], [21, 9], [9, 16], [1, 1]],
  [[16, 10], [32, 9], [10, 16], [3, 2]],
  [[], [48, 9], [9, 18], [4, 3]],
  [[], [], [], [5, 4]]
]

const color = [
  ['660000', '990000', 'cc0000', 'cc3333', 'ea4c88', '993399'],
  ['663399', '333399', '0066cc', '0099cc', '66cccc', '77cc33'],
  ['669900', '336600', '666600', '999900', 'cccc33', 'ffff00'],
  ['ffcc33', 'ff9900', 'ff6600', 'cc6633', '996633', '663300'],
  ['000000', '999999', 'cccccc', 'ffffff', '424153']
]

const sorting = [
  { name: '相关的', value: 'relevance' },
  { name: '随机的', value: 'random' },
  { name: '最新的', value: 'date_added' },
  { name: '浏览量', value: 'views' },
  { name: '收藏数', value: 'favorites' },
  { name: '排行榜', value: 'toplist' },
  { name: '热门的', value: 'hot' }
]

export default {
  name: 'TypeHeader',
  data() {
    return {
      category: category,
      purity: purity,
      // 分辨率-开始
      resolution: resolution,
      ratio: ratio,
      color: color,
      sorting: sorting,
      screen: window.screen,
      isResolutionRadio: true,
      resolutionCheckboxSelected: [],
      resolutionRadioSelected: '',
      customResolution: { width: undefined, height: undefined },
      customResolutionCheckboxInput: undefined,
      // 分辨率-结束
      ratioCheckboxSelected: [],
      colorCheckboxSelected: [],
      sortingRadioSelected: 'random',
      order: 'desc',
      apikey: '',
      apikeyInput: '',
      apikeyValid: false,
      apikeyDialogVisible: false
    }
  },
  computed: {
    ...mapGetters(['config']),
    resolutionSelectedEffect: function() {
      return this.isResolutionRadio && !!this.resolutionRadioSelected ||
      !this.isResolutionRadio && this.resolutionCheckboxSelected.length > 0
        ? 'primary' : ''
    },
    ratioSelectedEffect: function() {
      return this.ratioCheckboxSelected.length > 0 ? 'primary' : ''
    },
    ratioSelectedText: function() {
      if (this.ratioCheckboxSelected.length > 0) {
        const name = this.ratioCheckboxSelected[0].indexOf('x') > -1
          ? this.ratioCheckboxSelected[0]
          : this.ratioCheckboxSelected[0] === 'landscape' ? 'All Wide' : 'All Portrait'
        return `${name} +${this.ratioCheckboxSelected.length}`
      } else {
        return '比例'
      }
    },
    textHexColor: function() {
      const hexColor = this.colorCheckboxSelected[0]
      const rgbArr = colorHexToRGB(hexColor, true)
      if (rgbArr[0] + rgbArr[1] + rgbArr[2] > 500) {
        return '#777'
      } else {
        return '#fff'
      }
    },
    sortingText: function() {
      for (const obj of sorting) {
        if (this.sortingRadioSelected === obj.value) {
          return obj.name
        }
      }
      return '排序'
    }
  },
  watch: {
    apikeyValid() {
      if (this.apikeyValid) {
        this.purity = purity
      } else {
        const p = {}
        p.SFW = purity.SFW
        p.Sketchy = purity.Sketchy
        this.purity = p
      }
    }
  },
  created() {
    const p = {}
    p.SFW = purity.SFW
    p.Sketchy = purity.Sketchy
    this.purity = p
    // API Key
    try {
      const apikey = this.config.api.wallhaven.apikey
      if (apikey) {
        this.apikeyInput = apikey
        this.checkApikey()
      }
      // eslint-disable-next-line no-empty
    } catch (ignored) {
    }
    // URL
    try {
      const url = this.config.api.wallhaven.url
      if (url) {
        this.setParams(getURLParams(url))
      }
      // eslint-disable-next-line no-empty
    } catch (ignored) {
    }
  },
  mounted() {
    this.refresh()
  },
  methods: {
    isResolutionInDefinition(width, height) {
      if (!(width && height)) {
        return false
      }
      for (const items of resolution) {
        for (const item of items) {
          if (item.length === 0) continue
          if ((item[0] + '' === width + '') && (item[1] + '' === height + '')) {
            return true
          }
        }
      }
      return false
    },
    isRatioInDefinition(width, height) {
      if (!(width && height)) {
        return false
      }
      for (const items of ratio) {
        for (const item of items) {
          if (item.length === 0) continue
          if ((item[0] + '' === width + '') && (item[1] + '' === height + '')) {
            return true
          }
        }
      }
      return false
    },
    isColorInDefinition(cr) {
      if (!cr) {
        return false
      }
      for (const c of color) {
        if (c.indexOf(cr) >= 0) {
          return true
        }
      }
      return false
    },
    customResolutionChange() {
      const resolution = this.customResolution.width || this.customResolution.height
        ? ((this.customResolution.width === undefined ? 0 : this.customResolution.width) + 'x' +
              (this.customResolution.height === undefined ? 0 : this.customResolution.height))
        : ''
      if (this.isResolutionRadio) {
        this.resolutionRadioSelected = resolution
      } else {
        if (resolution && this.customResolutionCheckboxInput &&
            this.resolutionCheckboxSelected.indexOf(resolution) < 0) {
          const index = this.resolutionCheckboxSelected.indexOf(this.customResolutionCheckboxInput)
          if (index >= 0) {
            this.resolutionCheckboxSelected.splice(index, 1)
          }
          this.resolutionCheckboxSelected.push(resolution)
          this.customResolutionCheckboxInput = resolution
        } else if (resolution && this.resolutionCheckboxSelected.indexOf(resolution) < 0) {
          this.resolutionCheckboxSelected.push(resolution)
          this.customResolutionCheckboxInput = resolution
        } else if (!resolution && this.customResolutionCheckboxInput) {
          const index = this.resolutionCheckboxSelected.indexOf(this.customResolutionCheckboxInput)
          if (index >= 0) {
            this.resolutionCheckboxSelected.splice(index, 1)
            this.customResolutionCheckboxInput = undefined
          }
        }
      }
    },
    resolutionSelectionChange() {
      if (this.customResolution.width === undefined && this.customResolution.height === undefined) {
        return
      }
      const resolution = this.customResolution.width || this.customResolution.height
        ? ((this.customResolution.width === undefined ? 0 : this.customResolution.width) + 'x' +
              (this.customResolution.height === undefined ? 0 : this.customResolution.height))
        : ''
      if (this.isResolutionRadio) {
        this.resolutionRadioSelected = resolution
      } else {
        if (this.customResolutionCheckboxInput) {
          const index = this.resolutionCheckboxSelected.indexOf(this.customResolutionCheckboxInput)
          if (index >= 0) {
            this.resolutionCheckboxSelected.splice(index, 1)
          }
          this.resolutionCheckboxSelected.push(resolution)
          this.customResolutionCheckboxInput = resolution
        } else {
          this.resolutionCheckboxSelected.push(resolution)
          this.customResolutionCheckboxInput = resolution
        }
      }
    },
    resolutionRadioSelectionChange() {
      if (this.isResolutionRadio) {
        this.customResolution.width = undefined
        this.customResolution.height = undefined
      }
    },
    getParams() {
      const params = {}
      params.categories = this.category.General.value + this.category.Anime.value + this.category.People.value
      params.purity = this.purity.SFW.value + this.purity.Sketchy.value + (this.purity.NSFW ? this.purity.NSFW.value : '0')
      params.sorting = this.sortingRadioSelected
      params.order = this.order
      if (this.isResolutionRadio && this.resolutionRadioSelected) {
        params.atleast = this.resolutionRadioSelected
      } else if (!this.isResolutionRadio && this.resolutionCheckboxSelected.length > 0) {
        params.resolutions = this.resolutionCheckboxSelected.join(',')
      }
      if (this.ratioCheckboxSelected.length > 0) {
        params.ratios = this.ratioCheckboxSelected.join(',')
      }
      if (this.colorCheckboxSelected.length > 0) {
        params.colors = this.colorCheckboxSelected.join(',')
      }
      if (this.apikeyValid && this.apikey) {
        params.apikey = this.apikey
      }
      return params
    },
    setParams(params) {
      if (!params || Object.keys(params).length === 0) {
        return
      }
      if (/^[0|1]{3}$/.test(params.categories)) {
        this.category.General.value = params.categories.charAt(0)
        this.category.Anime.value = params.categories.charAt(1)
        this.category.People.value = params.categories.charAt(2)
      }
      if (/^[0|1]{2,3}$/.test(params.purity)) {
        this.purity.SFW.value = params.purity.charAt(0)
        this.purity.Sketchy.value = params.purity.charAt(1)
        if (params.purity.length === 3 && this.apikeyValid) {
          this.purity.NSFW.value = params.purity.charAt(2)
        }
      }
      if (/^(relevance|random|date_added|views|favorites|toplist|hot)$/i.test(params.sorting)) {
        this.sortingRadioSelected = params.sorting.toLowerCase()
      }
      if (/^(desc|asc)$/i.test(params.order)) {
        this.order = params.order.toLowerCase()
      }
      // 优先使用resolutions
      if (params.atleast) {
        const whArr = params.atleast.split('x')
        if (whArr.length === 2) {
          this.isResolutionRadio = true
          this.customResolution.width = /^\d+$/.test(whArr[0]) ? whArr[0] : 0
          this.customResolution.height = /^\d+$/.test(whArr[1]) ? whArr[1] : 0
        }
      }
      if (params.resolutions) {
        const resolutions = params.resolutions.split(',')
        if (resolutions.length > 0) {
          this.isResolutionRadio = false
          for (const wh of resolutions) {
            const whArr = wh.split('x')
            if (whArr.length !== 2) continue
            if (this.isResolutionInDefinition(whArr[0], whArr[1])) {
              if (this.resolutionCheckboxSelected.indexOf(wh) < 0) {
                this.resolutionCheckboxSelected.push(wh)
              }
            } else {
              const w = /^\d+$/.test(whArr[0]) ? whArr[0] : 0
              const h = /^\d+$/.test(whArr[1]) ? whArr[1] : 0
              this.customResolution.width = w
              this.customResolution.height = h
              this.customResolutionCheckboxInput = w + 'x' + h
            }
          }
        }
      }
      if (params.ratios) {
        const ratios = params.ratios.split(',')
        if (ratios.length > 0) {
          for (const wh of ratios) {
            if (/^(landscape|portrait)$/i.test(wh)) {
              const whL = wh.toLowerCase()
              if (this.ratioCheckboxSelected.indexOf(whL) < 0) {
                this.ratioCheckboxSelected.push(whL)
              }
              continue
            }
            const whArr = wh.split('x')
            if (whArr.length !== 2) continue
            if (this.isRatioInDefinition(whArr[0], whArr[1])) {
              if (this.ratioCheckboxSelected.indexOf(wh) < 0) {
                this.ratioCheckboxSelected.push(wh)
              }
            }
          }
        }
      }
      if (params.colors) {
        const colors = params.colors.split(',')
        if (colors.length > 0) {
          for (const c of colors) {
            const cL = c.toLowerCase()
            if (this.colorCheckboxSelected.indexOf(cL) < 0 && this.isColorInDefinition(cL)) {
              this.colorCheckboxSelected.push(cL)
            }
          }
        }
      }
      if (params.apikey) {
        this.apikey = this.apikeyInput = params.apikey
        this.apikeyValid = true
      }
    },
    notify(typ, msg) {
      this.$notify({
        title: msg,
        message: undefined,
        type: typ,
        duration: 2400,
        offset: 105
      })
    },
    checkApikey() {
      return getBgsWF({ purity: '001', apikey: this.apikeyInput }).then(resp => {
        if (resp instanceof Object && resp.data.length > 0) {
          this.apikeyValid = true
          this.notify('success', 'API密钥可用')
        } else {
          this.notify('warning', '输入的API密钥似乎不正确')
          this.apikeyValid = false
        }
      }).catch((err) => {
        const msg = /.*401.*/.test(err.toString())
          ? '输入的API密钥似乎不正确' : '检查API密钥出错'
        this.notify('warning', msg)
        this.apikeyValid = false
      })
    },
    setApikey() {
      if (this.apikeyValid) {
        // this.notify('success', 'API密钥已设置')
        this.apikeyDialogVisible = false
        this.updateWallhavenApikey()
      } else {
        this.checkApikey().then(() => {
          if (this.apikeyValid) {
            this.apikey = this.apikeyInput
            this.apikeyDialogVisible = false
            // this.notify('success', 'API密钥已设置')
            this.updateWallhavenApikey()
          }
        })
      }
    },
    updateWallhavenApikey() {
      updateConfig({
        api: {
          wallhaven: { apikey: this.apikey }
        }
      }).then(resp => {
        this.$message.success('Wallhaven API密钥已保存')
        this.$store.dispatch('app/getConfig')
      })
    },
    updateWallhavenURL() {
      updateConfig({
        api: {
          wallhaven: { url: formatURL(wallhaven_url, this.getParams()) }
        }
      }).then(resp => {
        this.$message.success('Wallhaven 参数已保存')
        this.$store.dispatch('app/getConfig')
      })
    },
    refresh() {
      this.$emit('refresh', this.getParams())
    }
  }
}
</script>

<style scoped lang="scss">

.header {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 55px;
  background-color: rgba(39, 42, 44, .75);
  background-image: linear-gradient(to bottom, #292c2f 0, rgba(34, 34, 34, .5) 100%);
  box-shadow: 0 0 0 1px #222, 0 5px 5px rgba(0, 0, 0, .5);
  @media only screen and (max-width: 1000px) {
    height: 96px;
  }

  .control-bar, .search-bar, .apikey {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
  }

  .control-bar {
    float: left;
    padding: 0 1vw;
    user-select: none;

    > * {
      margin-right: 12px;

      &:last-child {
        margin-right: 0;
      }
    }

    .btn {
      font-size: 16px;
      color: #f0f0f0;
      font-weight: 600;
      transition: all .2s ease;
      opacity: 1;

      &:hover {
        color: #409eff;
        cursor: pointer;
      }
    }
  }

  .search-bar {
    //> div {
    //  margin: 0 5px;
    //}

    @media only screen and (max-width: 1000px) {
      flex-direction: column;
      .search-item {
        &:nth-child(1) {
          align-items: flex-end;
        }

        &:nth-child(2) {
          align-items: flex-start;
        }
      }
    }

    .search-item {
      display: flex;
      height: 100%;
      align-items: center;
      justify-content: center;
      margin: 5px 0;

      > div {
        margin: 0 5px;
      }
    }
  }

  .apikey {
    float: right;
    font-size: 24px;
    color: #f0f0f0;
    padding: 0 1vw;

    i {
      transition: all .3s ease;

      &:hover {
        cursor: pointer;
        color: #64a5ff;
      }
    }
  }
}

.dropdown {
  text-align: center;
  color: #606266;
  user-select: none;

  .native-info {
    margin: 10px;
    font-size: 14px;
  }
}

.resolution-head {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 3px;
  width: 100%;

  .resolution-head-item {
    width: calc(100% / 5);
    float: left;
    text-align: center;
    display: inline-block;
  }
}

.ratio-head {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 3px;
  width: 100%;
  user-select: none;

  .ratio-head-item {
    width: 25%;
    float: left;
    text-align: center;
    display: inline-block;
  }
}

.sorting-item {
  margin: 4px 0;
  user-select: none;
}

.search-submit {
  font-size: 18px;
  height: 31.79px;
  width: 40px;
  display: flex;
  justify-content: center;
  align-items: center;

  i {
    font-weight: 600 !important;
  }

  &:hover i {
    animation: spin 1s infinite ease-in-out;
    @keyframes spin {
      from {
        transform: rotate(0)
      }
      to {
        transform: rotate(360deg)
      }
    }
  }
}

</style>

<style lang="scss">
.el-dropdown-menu {
  padding: 1em;
}

.search-bar {
  .el-radio-button__inner, .el-checkbox-button__inner {
    background: #f0f0f0;
  }
}

.selected-group {
  .el-radio-button, .el-checkbox-button {
    margin: 3px 3px;
  }

  .el-radio-button__inner, .el-checkbox-button__inner {
    border: 1px solid #DCDFE6;
    border-radius: 4px !important;
    min-width: 90px;
    padding: 7px 10px;
    text-align: center;
    display: inline-block;
  }

  .ratio-item {
    .el-radio-button__inner, .el-checkbox-button__inner {
      min-width: 64px;
    }

    &.ratio-all-wide {
      .el-radio-button__inner, .el-checkbox-button__inner {
        min-width: 134px;
      }
    }
  }

  .color-item {
    position: relative;

    .el-radio-button__inner, .el-checkbox-button__inner {
      border: none;
      min-width: 64px;
      height: 24px;
    }

    .el-checkbox-button__original {
      z-index: 1;
    }

    &.is-checked {
      .el-checkbox-button__inner {
        box-shadow: none;
      }

      .el-checkbox-button__original {
        opacity: 1;

        &:after {
          content: "✔";
          color: #ffffff;
          text-align: center;
          font-size: 12px;
          line-height: 13px;
          background-color: #409EFF;
          position: absolute;
          border-radius: 3px;
          top: 0;
          left: 0;
          width: 13px;
          height: 13px;
        }
      }
    }

    .color {
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      border-radius: 3px !important;
      box-shadow: 0 2px 3px rgba(0, 0, 0, .3);
    }
  }

  .sorting-item {
    .el-radio-button__inner, .el-checkbox-button__inner {
      min-width: 78px;
      height: 28px;
    }
  }
}

.resolution-framed {
  width: 100%;
  padding: 0 3px;

  .el-radio-button {
    width: 50%;

    .el-radio-button__inner {
      width: 100%;
    }
  }
}

.custom-resolution {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 3px;
  margin-top: 12px;
  font-weight: 600;

  span.title {
    padding-right: 24px;
  }

  span.x {
    padding: 0 10px;
  }

  .el-input {
    width: auto;
  }

  .el-input-number__decrease, .el-input-number__increase {
    display: none;
  }

  .el-input__inner {
    padding: 0 15px;
  }
}

.search-sorting {
  position: relative;
  display: table;
  user-select: none;

  .el-button {
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
  }

  .search-order {
    display: table-cell;
    vertical-align: middle;
    position: relative;
    z-index: 1;
    font-weight: 600;
    font-size: 16px;
    color: white;
    height: 100%;
    padding: 0 5px;
    background-color: #409EFF;
    border-radius: 0 3px 3px 0;
    border-left: #ffffff 1px solid;
    cursor: pointer;

    &:hover {
      background-color: #66b1ff;
    }
  }
}
</style>
