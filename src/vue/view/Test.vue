<template>
  <div class="container">
    <div v-for="(value,key) in tests" :key="key" class="test-item">
      <el-button class="test-btn" :loading="value.loading">{{ value.btnName }}</el-button>
      <el-alert
        :title="value.cur.title"
        :type="value.cur.type"
        :closable="false"
        show-icon
      >
        <div slot v-html="value.cur.msg"></div>
      </el-alert>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Test',
  data() {
    return {
      tests: {
        lastBG: {
          btnName: '切换上个桌面壁纸',
          loading: false,
          cur: {
            type: 'info',
            title: '测试切换上一个桌面壁纸',
            msg: '点击左侧按钮开始测试“切换上一个桌面壁纸”'
          },
          success: {
            type: 'success',
            title: '测试切换上一个桌面壁纸：成功',
            msg: '已成功切换到上一个壁纸'
          },
          error: {
            type: 'error',
            title: '测试切换上一个桌面壁纸：失败',
            msg: '尝试切换上一个壁纸失败'
          }
        },
        nextBG: {
          btnName: '切换下个桌面壁纸',
          loading: false,
          cur: {
            type: 'info',
            title: '测试切换下一个桌面壁纸',
            msg: '点击左侧按钮开始测试“切换下一个桌面壁纸”'
          },
          success: {
            type: 'success',
            title: '测试切换下一个桌面壁纸：成功',
            msg: '已成功切换到下一个壁纸'
          },
          error: {
            type: 'error',
            title: '测试切换下一个桌面壁纸：失败',
            msg: '尝试切换下一个壁纸失败'
          }
        },
        favoriteBG: {
          btnName: '收藏当前桌面壁纸',
          loading: false,
          cur: {
            type: 'info',
            title: '测试收藏当前壁纸',
            msg: '点击左侧按钮开始测试“收藏当前桌面壁纸”'
          },
          success: {
            type: 'success',
            title: '测试收藏前桌面壁纸：成功',
            msg: '已成功收藏当前桌面壁纸'
          },
          error: {
            type: 'error',
            title: '测试收藏当前桌面壁纸：失败',
            msg: '尝试收藏当前桌面壁纸失败'
          }
        },
        locateBG: {
          btnName: '定位当前桌面壁纸',
          loading: false,
          cur: {
            type: 'info',
            title: '测试定位到当前壁纸',
            msg: '点击左侧按钮开始测试“定位到当前桌面壁纸”'
          },
          success: {
            type: 'success',
            title: '测试定位到当前桌面壁纸：成功',
            msg: '已成功定位到当前桌面壁纸'
          },
          error: {
            type: 'error',
            title: '测试定位到当前桌面壁纸：失败',
            msg: '尝试定位到当前桌面壁纸失败'
          }
        }
      }
    }
  }
}
</script>

<style scoped lang="scss">
.test-item {
  display: flex;
  width: 100%;
  margin-bottom: 1.35vw;

  &:last-child {
    margin-bottom: 0;
  }

  .test-btn {

    margin-right: 5%;
  }
}
</style>
