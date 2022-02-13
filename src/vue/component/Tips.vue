<!-- 类似于el-loding效果 -->
<template>
  <div class="mytips tips-modal" :style="{background:background}">
    <div class="tips-container">
      <div :class="['tips-content',customClass]">
        <div v-if="spinner" class="tips-icon" v-html="spinner"></div>
        <div v-if="text" class="tips-text" v-html="text"></div>
        <div v-if="buttons.length > 0" class="tips-button">
          <el-button
            v-for="(button, index) in buttons"
            :key="index"
            :size="button.size || 'mini'"
            :type="button.type || 'primary'"
            :plain="button.plain || false"
            :round="button.round || false"
            :circle="button.circle || false"
            :loading="button.loading || false"
            :disabled="button.disabled || false"
            :icon="button.icon || ''"
            :autofocus="button.autofocus || false"
            @click="button.click"
          >{{ button.text }}</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Tips',
  props: {
    background: { // 遮罩背景色
      type: String,
      required: false,
      default: () => {
        return 'rgba(0, 0, 0, .5)'
      }
    },
    text: { // 显示在加载图标下方的加载文案
      type: String,
      required: false,
      default: () => {
        return ''
      }
    },
    spinner: { // 自定义图标元素
      type: String,
      required: false,
      default: () => {
        return ''
      }
    },
    customClass: { // 自定义类名
      type: String,
      required: false,
      default: () => {
        return ''
      }
    },
    buttons: {
      type: Array,
      required: false,
      default: () => {
        return []
      }
    }
  },
  data() {
    return {}
  },
  methods: {
    close() {

    },
    getCurrentInstance() {

    }
  }
}
</script>

<style scoped lang="scss">
.tips-modal {
  width: 100vw;
  height: 100vh;
  position: absolute;
  left: 0;
  top: 0;
  z-index: 999999;
}

.tips-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  min-width: 300px;
  min-height: 200px;
  background-color: #F5F5F5;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.tips-content {
  text-align: center;
}

.tips-icon, .tips-text {
  color: #409eff;
}

.tips-icon {
  font-size: 20px;
  font-weight: bold;
}

.tips-text {
  font-size: 18px;
  margin-top: 10px;
}

.tips-button {
  margin-top: 20px;
}
</style>
