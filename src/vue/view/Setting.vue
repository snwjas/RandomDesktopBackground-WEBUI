<template>
  <el-scrollbar class="setting clearfix">
    <div class="content">
      <el-form ref="form" :model="form" label-width="80px" label-position="left" size="mini">
        <el-divider content-position="left">基本设置</el-divider>
        <el-form-item label="启动">
          <el-checkbox v-model="form.run.startup">开机启动程序</el-checkbox>
          <el-button type="text" style="margin-left: 30px;" @click="createDesktopLnk">创建桌面快捷方式</el-button>
        </el-form-item>
        <el-form-item label="轮播">
          <el-radio-group v-model="form.run.rotation">
            <el-radio label="network">在线壁纸</el-radio>
            <el-radio label="local">本地壁纸</el-radio>
          </el-radio-group>
          <el-checkbox
            v-if="form.run.rotation==='local'"
            v-model="form.run.local.disorder"
            style="margin-left: 30px;"
          >无序
          </el-checkbox>
        </el-form-item>
        <el-form-item label="工作目录">
          <el-input v-model="form.run.workdir" readonly clearable placeholder="存放壁纸、日志等的目录，默认为程序所在路径run目录" @click.native="selectWorkdir">
            <i
              v-if="form.run.workdir"
              slot="suffix"
              class="clearbtn el-input__icon el-icon-circle-close"
              @click="clearWorkdir"
            ></i>
            <el-button slot="append" icon="el-icon-folder-opened" title="打开工作目录" @click="locateWorkdir"></el-button>
          </el-input>
        </el-form-item>
        <el-form-item label="用户代理" :class="[form.run.rotation==='local'?'disabled':'']">
          <el-radio-group v-model="form.run.proxy">
            <el-radio label="none">不使用代理</el-radio>
            <el-radio label="system">使用系统代理</el-radio>
          </el-radio-group>
        </el-form-item>
        <!--///////////////////////////////////////////////////////-->
        <el-divider content-position="left">图源设置</el-divider>
        <el-form-item label="在线图源" :class="[form.run.rotation==='local'?'disabled':'']">
          <el-popover trigger="hover" placement="top">
            <div>{{
              form.api.name === 'wallhaven'
                ? '点击下方API输入框右侧按钮跳转跳转至wallhaven图源设置页面'
                : '可输入多个自定义图源API，但API须指向一张图片'
            }}
            </div>
            <span slot="reference" class="form-tips" style="left: 220px">
              <i class="el-icon-question"></i>
            </span>
          </el-popover>
          <el-radio-group v-model="form.api.name">
            <el-radio label="wallhaven">wallhaven</el-radio>
            <el-radio label="custom">自定义</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="API地址" class="api-form-item" :class="[form.run.rotation==='local'?'disabled':'']">
          <el-input
            v-if="form.api.name==='wallhaven'"
            v-model="form.api.wallhaven.url"
            placeholder="请输入wallhaven api，或点击右侧按钮去设置"
          >
            <el-popconfirm
              slot="append"
              confirm-button-text="保存"
              cancel-button-text="不用了"
              placement="top-end"
              hide-icon
              width="290"
              title="即将跳转至wallhaven图源设置页面，是否需要保存当前设置？"
              @cancel="toWallhavenSetting"
              @confirm="updateConfigAndToWallhavenSetting"
            >
              <el-button slot="reference" icon="el-icon-picture" title="点击跳转至wallhaven图源类型设置页面"></el-button>
            </el-popconfirm>
          </el-input>
          <div v-else class="custom-api">
            <div v-for="(item,index) in customApiInput" :key="index" class="custom-api-item">
              <el-input v-model="item.url" placeholder="请输入自定义图源API" clearable @change="item.valid=false">
                <i
                  slot="prefix"
                  :style="{color: item.valid ? '#67c23a' : '#909399'}"
                  :class="['el-input__icon',item.valid?'el-icon-success':'el-icon-question']"
                ></i>
              </el-input>
              <i class="iconfont icon-ceshi" style="color: #de7d01;" title="点击测试API是否可用" @click="isImageUrl(item)"></i>
              <i class="el-icon-remove" @click="customApiInput.splice(index,1)"></i>
            </div>
            <i class="el-icon-circle-plus" @click="customApiInput.push({url:'',valid:false})"></i>
          </div>
        </el-form-item>
        <!--///////////////////////////////////////////////////////-->
        <el-divider content-position="left">任务设置</el-divider>
        <el-form-item label="切换频率">
          <el-radio-group
            v-model="timeUnit"
            style="margin-right: 30px"
            @change="timeUnitChange"
          >
            <el-radio label="minute">分钟</el-radio>
            <el-radio label="second">秒</el-radio>
          </el-radio-group>
          <el-input-number
            v-model="timeValue"
            :min="1"
            :precision="0"
            controls-position="right"
          ></el-input-number>
        </el-form-item>
        <el-form-item label="任务模式" :class="[form.run.rotation==='local'?'disabled':'']">
          <el-radio-group v-model="form.task.mode">
            <el-radio label="multiple">多张</el-radio>
            <el-radio label="single">一张</el-radio>
          </el-radio-group>
          <el-popover trigger="hover" placement="top">
            <div style="line-height: 150%;">
              <div>
                <div><strong>多张</strong>：一次性最多获取24张壁纸，全部切换完毕后再次拉取</div>
                <p>- 可以通过调整<strong>线程数量</strong>与<strong>随机间隔</strong>（拉取每张壁纸前的随机间隔时间）</p>
                <p>&nbsp;&nbsp;以提高获取壁纸的成功率，因为大多网站设有限流机制</p>
              </div>
              <div><strong>一张</strong>：一次获取一张壁纸，切换下一张前再次拉取</div>
            </div>
            <span slot="reference" class="form-tips" style="left: 180px">
              <i class="el-icon-question"></i>
            </span>
          </el-popover>
          <div style="margin-top: 16px;">
            <div :class="[form.task.mode==='multiple'?'':'disabled']">
              <el-form-item label="线程数量">
                <el-input-number
                  v-model="form.task.threads"
                  :disabled="form.task.mode==='single'"
                  :min="1"
                  :max="32"
                  :precision="0"
                  controls-position="right"
                ></el-input-number>
              </el-form-item>
              <el-form-item label="随机间隔">
                <el-input-number
                  v-model="form.task.rnd_sleep_l"
                  :disabled="form.task.mode==='single'"
                  :min="0"
                  :precision="2"
                  controls-position="right"
                  @change="rndSleepChange"
                ></el-input-number>
                &nbsp;-&nbsp;
                <el-input-number
                  v-model="form.task.rnd_sleep_r"
                  :disabled="form.task.mode==='single'"
                  :min="0"
                  :precision="2"
                  controls-position="right"
                  @change="rndSleepChange"
                ></el-input-number>
                &nbsp;&nbsp;秒
              </el-form-item>
            </div>
          </div>
          <div style="margin-top:16px;">
            <el-checkbox v-model="form.task.retain_bgs" style="margin-right: 45px;">保留壁纸</el-checkbox>
            <span :class="[form.task.retain_bgs?'':'disabled']" style="position:relative;">
              最大占用空间：
              <el-input-number
                v-model="form.task.max_retain_mb"
                :disabled="!form.task.retain_bgs"
                :min="-1"
                :precision="0"
                controls-position="right"
              ></el-input-number>&nbsp;&nbsp;MB
              <el-popover trigger="hover" placement="top">
                <div><strong>-1</strong>表示无限制</div>
                <span slot="reference" class="form-tips" style="left: 300px;top:-5px;">
                  <i class="el-icon-question"></i>
                </span>
              </el-popover>
            </span>
          </div>
        </el-form-item>
        <!--///////////////////////////////////////////////////////-->
        <el-divider content-position="left">快捷键设置</el-divider>
        <el-form-item label="右键菜单">
          <el-checkbox v-model="form.ctxmenu.enable">启用桌面右键菜单</el-checkbox>
          <div style="margin-top: 5px;" :class="[form.ctxmenu.enable?'':'disabled']">
            <el-checkbox v-model="form.ctxmenu.prev_bg" label="上一张壁纸" :disabled="!form.ctxmenu.enable"></el-checkbox>
            <el-checkbox v-model="form.ctxmenu.next_bg" label="下一张壁纸" :disabled="!form.ctxmenu.enable"></el-checkbox>
            <el-checkbox v-model="form.ctxmenu.fav_bg" label="收藏当前壁纸" :disabled="!form.ctxmenu.enable"></el-checkbox>
            <el-checkbox v-model="form.ctxmenu.loc_bg" label="定位当前壁纸" :disabled="!form.ctxmenu.enable"></el-checkbox>
          </div>
        </el-form-item>
        <el-form-item label="全局热键">
          <el-checkbox v-model="form.hotkey.enable">启用全局热键</el-checkbox>
          <el-popover trigger="hover" placement="top">
            <div style="line-height: 150%;">
              <div>快捷键组合至少含有一个特殊按键（<strong><em>Ctrl</em></strong>、<strong><em>Alt</em></strong>、
                <strong><em>Shift</em></strong>）和一个非特殊按键
              </div>
              <div>点击下面的输入框，快速按下键盘按键然后松开，即可输入快捷键组合</div>
            </div>
            <span slot="reference" class="form-tips" style="left: 150px">
              <i class="el-icon-question"></i>
            </span>
          </el-popover>
        </el-form-item>
        <div :class="[form.hotkey.enable?'':'disabled']">
          <el-form-item label="控制" style="margin-bottom: 0">
            <el-form-item label="上一张壁纸" label-width="100px">
              <el-input
                v-model="form.hotkey.prev_bg"
                clearable
                readonly
                :disabled="!form.hotkey.enable"
                @keydown.native.prevent="keyDown($event)"
                @keyup.native.prevent="setHotkey($event,'prev_bg')"
              ></el-input>
            </el-form-item>
            <el-form-item label="下一张壁纸" label-width="100px">
              <el-input
                v-model="form.hotkey.next_bg"
                clearable
                readonly
                :disabled="!form.hotkey.enable"
                @keydown.native.prevent="keyDown($event)"
                @keyup.native.prevent="setHotkey($event,'next_bg')"
              ></el-input>
            </el-form-item>
          </el-form-item>
          <el-form-item label="其他">
            <el-form-item label="收藏当前壁纸" label-width="100px">
              <el-input
                v-model="form.hotkey.fav_bg"
                clearable
                readonly
                :disabled="!form.hotkey.enable"
                @keydown.native.prevent="keyDown($event)"
                @keyup.native.prevent="setHotkey($event,'fav_bg')"
              >
                <el-button
                  slot="append"
                  icon="el-icon-folder-opened"
                  title="打开收藏文件夹"
                  :disabled="!form.hotkey.enable"
                  @click="locateFavoritePath"
                ></el-button>
              </el-input>
            </el-form-item>
            <el-form-item label="定位当前壁纸" label-width="100px">
              <el-input
                v-model="form.hotkey.loc_bg"
                clearable
                readonly
                :disabled="!form.hotkey.enable"
                @keydown.native.prevent="keyDown($event)"
                @keyup.native.prevent="setHotkey($event,'loc_bg')"
              ></el-input>
            </el-form-item>
          </el-form-item>
        </div>
      </el-form>
      <div class="ctrl">
        <el-button type="primary" size="mini" @click="updateConfig">保存</el-button>
        <el-button size="mini" @click="close">放弃</el-button>
      </div>
    </div>
  </el-scrollbar>
</template>

<script>
import { mapGetters } from 'vuex'
import { deepClone, hashCode, isImageUrl } from '../util/common'
import hkMap from '../util/hkmap'
import { selectFolder, updateConfig, createDesktopLnk, locateFavoritePath, locateWorkdir } from '../api/index'

export default {
  name: 'Setting',
  data() {
    return {
      form: {
        run: {
          startup: false,
          workdir: '',
          proxy: 'none',
          rotation: 'network',
          local: {
            disorder: true
          }
        },
        api: {
          name: 'wallhaven',
          wallhaven: {
            url: ''
          },
          custom: {}
        },
        task: {
          seconds: 300,
          mode: 'multiple',
          threads: 2,
          rnd_sleep_l: 0,
          rnd_sleep_r: 5,
          retain_bgs: false,
          max_retain_mb: -1
        },
        hotkey: {
          enable: false,
          prev_bg: '',
          next_bg: '',
          fav_bg: '',
          loc_bg: ''
        },
        ctxmenu: {
          enable: false,
          prev_bg: false,
          next_bg: false,
          fav_bg: false,
          loc_bg: false
        }
      },
      customApiInput: [{ url: '', valid: false }],
      timeUnit: 'minute', // minute | second
      timeValue: '',
      isKeyPress: false,
      keyPressSet: {}
    }
  },
  computed: {
    ...mapGetters(['config'])
  },
  created() {
    this.form = deepClone(this.config)
    // 自定义图源
    const cApi = this.config['api']['custom']
    if (cApi && Object.keys(cApi).length > 0) {
      const obj = []
      for (const key in cApi) {
        obj.push({ url: cApi[key], valid: true })
      }
      this.customApiInput = obj
    }
    // 切换频率
    const seconds = parseInt(this.config['task']['seconds']) || 0
    this.timeUnit = seconds % 60 === 0 ? 'minute' : 'second'
    this.timeValue = parseInt(seconds % 60 === 0 ? seconds / 60 : seconds)
  },
  methods: {
    isImageUrl(customApiObj) {
      isImageUrl(customApiObj.url).then(res => {
        customApiObj.valid = !!res
        this.$message.success(`图源[${customApiObj.url}]可用`)
      }).catch(() => {
        customApiObj.valid = false
        this.$message.warning(`图源[${customApiObj.url}]不可用`)
      })
    },
    close() { // 主动关闭对话框
      this.$emit('close')
    },
    toWallhavenSetting() {
      this.$router.push({ name: 'Type' })
    },
    selectWorkdir() {
      selectFolder().then(res => {
        if (res) this.form.run.workdir = res
      }).catch(err => {
        console.log(err)
      })
    },
    clearWorkdir(event) {
      this.form.run.workdir = ''
      event.stopPropagation()
      return false
    },
    timeUnitChange() {
      this.timeValue = parseInt(this.timeUnit === 'minute'
        ? this.timeValue / 60
        : this.timeValue * 60
      )
    },
    rndSleepChange() {
      const l = this.form.task.rnd_sleep_l
      const r = this.form.task.rnd_sleep_r
      if (l > r) {
        this.form.task.rnd_sleep_r = l
        setTimeout(() => {
          this.form.task.rnd_sleep_l = r
        }, 20)
      }
    },
    keyDown(event) {

    },
    setHotkey(event, name) {
      event.preventDefault()
      if (!this.isKeyPress) {
        this.isKeyPress = true
        setTimeout(() => {
          this.isKeyPress = false
          this.form.hotkey[name] = this.getValidHotkey(this.keyPressSet)
          this.keyPressSet = {}
        }, 360)
      }
      if (event.keyCode === 8 || /^backspace$/i.test(event.key)) {
        this.form.hotkey[name] = ''
        return
      }
      this.keyPressSet[event.keyCode] = event.key
    },
    /**
     *  转换成后台热键组合字符串
     * @param codeKeyObj {event.keyCode:event.key}
     */
    getValidHotkey(codeKeyObj) {
      const validHotkey = []
      let specificHotkeys = 0
      for (const keycode in codeKeyObj) {
        const name = hkMap[keycode]
        if (name) {
          validHotkey.push(name)
          if (/.*(shift|control|alt|super).*/i.test(name)) {
            ++specificHotkeys
          }
        }
      }
      if (specificHotkeys < validHotkey.length) {
        return validHotkey.join('+')
      }
      return ''
    },
    getConfig() {
      const config = deepClone(this.form)
      // 自定义图源
      config['api']['custom'] = {}
      for (const item of this.customApiInput) {
        const url = item['url']
        if (url) {
          const name = `url-${hashCode(url)}`
          config['api']['custom'][name] = url
        }
      }
      // 切换频率
      config['task']['seconds'] = parseInt(this.timeUnit === 'minute'
        ? this.timeValue * 60
        : this.timeValue
      )

      return config
    },
    checkConfig(config) {
      const api_custom = config['api']['custom']
      if (Object.keys(api_custom).length === 0) {
        this.$message.warning('请输入自定义图源API')
        return false
      }
      return true
    },
    updateConfig() {
      const config = this.getConfig()
      if (!this.checkConfig(config)) {
        return
      }
      updateConfig(config).then(resp => {
        this.$store.commit('app/SET_CONFIG', config)
        this.$message.success('程序设置已保存，重启程序后生效')
        this.close()
      })
    },
    updateConfigAndToWallhavenSetting() {
      const config = this.getConfig()
      if (!this.checkConfig(config)) {
        return
      }
      updateConfig(config).then(resp => {
        this.$store.commit('app/SET_CONFIG', config)
        this.$message.success('程序设置保存成功，部分设置重启后生效')
        this.$router.push({ name: 'Type' })
      })
    },
    createDesktopLnk() {
      createDesktopLnk().then(resp => {
        this.$message.success('创建桌面快捷方式成功')
      })
    },
    locateFavoritePath() {
      locateFavoritePath().then(resp => {

      })
    },
    locateWorkdir(event) {
      event.stopPropagation()
      locateWorkdir().then(resp => {

      })
      return false
    }
  }

}
</script>

<style scoped lang="scss">
.setting {
  position: relative;
  width: 100%;
  height: 50vh;
  padding-bottom: 36px;
}

.content {
  padding-right: 16px;
}

.ctrl {
  position: absolute;
  width: 100%;
  height: 30px;
  bottom: 0;
  right: 16px;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  background-color: #fff;
}

.form-tips {
  position: absolute;
  top: 0;
  color: #c0c4cc;
  font-size: 16px;
  cursor: help;
}

.custom-api {
  .custom-api-item {
    display: flex;
    align-items: center;
    margin-bottom: 12px;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .el-input__icon {
    font-size: 15px;
  }

  i.icon-ceshi, i.el-icon-remove {
    margin-left: 7px;
    font-size: 20px;
    cursor: pointer;
  }

  i.el-icon-remove {
    color: #F56C6C;
  }

  i.el-icon-circle-plus {
    color: #64a5ff;
    margin-left: 0;
    cursor: pointer;
    font-size: 16px;
  }
}

.clearbtn:hover {
  cursor: pointer;
  color: #909399;
}

</style>

<style lang="scss">
.el-divider {
  margin-top: 36px;

  &:first-child {
    margin-top: 12px;
  }

  .el-divider__text {
    font-size: 16px;
  }
}

.el-scrollbar__wrap {
  overflow-x: hidden;
}

.disabled {
  position: relative;

  &::after {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    user-select: none;
    z-index: 1;
  }

  &, & * {
    color: #c0c4cc;
  }
}

</style>
