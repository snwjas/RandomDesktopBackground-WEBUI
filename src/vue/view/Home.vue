<template>
  <div class="container">
    <div class="container" @contextmenu="showBGOnly=!showBGOnly">
      <v-background :mask="!showBGOnly"></v-background>
    </div>
    <div class="menu" :style="showHideStyle">
      <div class="intro">
        <div class="title">‖ 随机桌面壁纸 ‖</div>
        <div class="subtitle">
          <v-typer content="让你的桌面壁纸就像一盒巧克力一样, 永远不知道下一颗是什么味道" lside="「" rside="」"></v-typer>
        </div>
      </div>
      <div class="action">
        <div class="button-group">
          <div class="button" @click="toggleUd">
            <i :class="['iconfont','icon-qidong',status.running?'shutdown':'startup']"></i>
            {{ status.running ? '关闭程序' : '启动程序' }}
          </div>
          <div class="button" @click="settingDialogVisible=true">
            <i class="iconfont icon-shezhi"></i>程序设置
          </div>
          <!-- 舍弃此功能：存在一个进程间通信问题，处理起来比较麻烦 -->
          <!--<div class="button" @click="testDialogVisible=true">-->
          <!--  <i class="iconfont icon-ceshi"></i>测试运行-->
          <!--</div>-->
          <div class="button" @click="aboutDialogVisible=true">
            <i class="iconfont icon-guanyuwomen"></i>关于程序
          </div>
        </div>
      </div>
    </div>
    <el-dialog
      title="程序设置"
      :visible.sync="settingDialogVisible"
      append-to-body
      width="45vw"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <v-setting @close="settingDialogVisible=false"></v-setting>
    </el-dialog>
    <!--<el-dialog title="测试运行" :visible.sync="testDialogVisible" append-to-body destroy-on-close>-->
    <!--  <v-test></v-test>-->
    <!--</el-dialog>-->
    <el-dialog title="关于程序" :visible.sync="aboutDialogVisible" append-to-body width="45vw">
      <v-about></v-about>
    </el-dialog>
  </div>
</template>

<script>

import { mapGetters } from 'vuex'
import { toggleUd } from '../api'

export default {
  name: 'Home',
  components: {
    'v-background': () => import('../component/Background'),
    'v-typer': () => import('../component/Typewriter'),
    'v-about': () => import('../view/About'),
    // 'v-test': () => import('../view/Test'),
    'v-setting': () => import('../view/Setting')
  },
  data() {
    return {
      aboutDialogVisible: false,
      testDialogVisible: false,
      settingDialogVisible: false,
      showBGOnly: false
    }
  },
  computed: {
    showHideStyle() {
      return this.showBGOnly
        ? { opacity: 0, visibility: 'hidden' }
        : { opacity: 1, visibility: 'visible' }
    },
    ...mapGetters(['status'])
  },

  methods: {
    toggleUd() {
      this.$tips({
        tipsName: 'ToggleUd',
        spinner: `<i class="el-icon-loading" style="color: ${this.status.running ? '#de7d01' : '#52c41a'}"></i>`,
        text: `<span style="color: ${this.status.running ? '#de7d01' : '#52c41a'}">
                  程序${this.status.running ? '关闭' : '启动'}中...
              </span>`
      })
      toggleUd().then(resp => {
        if (this.$tipsInstance && this.$tipsInstance.tipsName === 'ToggleUd') {
          this.$tipsInstance.close()
        }
        if (!this.status.running) {
          if (resp && resp.running) {
            this.$message.success('程序已启动')
          } else {
            this.$message.error('程序启动错误，原因请查看日志')
          }
        } else {
          this.$message.success('程序已关闭')
        }
        this.$store.commit('app/SET_STATUS', resp)
      }).catch(() => {
        if (this.$tipsInstance && this.$tipsInstance.tipsName === 'ToggleUd') {
          this.$tipsInstance.close()
        }
      })
    }
  }
}
</script>

<style lang="scss">
.startup-loading {
  user-select: none;

  .el-icon-loading, .el-loading-text {
    font-size: 20px;
  }

  .el-icon-loading {
    font-size: 24px;
  }

}
</style>

<style scoped lang="scss">

.container {
  position: relative;
}

.menu {
  position: absolute;
  top: 45%;
  left: 50%;
  transform: translate(-50%, -55%);
  color: #f0f0f0;
  min-width: 80%;
  transition: all 1s ease;

  .intro {
    text-align: center;
    margin-bottom: 3.25vw;
    user-select: none;

    .title {
      font-size: 2.5vw;
      margin-bottom: 0.85vw;
    }

    .subtitle {
      font-size: 1.55vw;
    }
  }

  .action {
    width: fit-content;
    margin: 0 auto;
  }

  .button-group {
    text-align: left;
    user-select: none;

    .button {
      display: flex;
      align-items: center;
      justify-content: center;
      float: left;
      font-size: 1vw;
      font-weight: 500;
      border-radius: 7px;
      border: #f0f0f0 2px solid;
      transition: all .3s ease;
      padding: 0.65vw 1.5vw;
      margin: 0 1.875vw 1.875vw 0;

      .iconfont {
        margin-right: 5px;
        font-size: 1vw;

        &.startup {
          color: #52c41a;
        }

        &.shutdown {
          color: #de7d01;
        }
      }

      &:last-child {
        margin-right: 0;
      }

      &:hover {
        cursor: pointer;
        border-color: #3a8ee6;
        background-color: #3a8ee6;
      }

      &:active {
        transform: translateY(2px);
        box-shadow: 5px 5px 10px rgba(58, 142, 230, 0.36);
      }
    }
  }

}
</style>
