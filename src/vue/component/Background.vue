<template>
  <div class="container" :style="maskBG" @dblclick.stop="changeBackground">
    <div :class="['background',backgroundLoading?'loading':'loaded']">
      <el-image
        style="height: 100%;width: 100%"
        fit="cover"
        :src="backgroundUrl"
        @load="backgroundLoaded"
      >
        <el-image slot="placeholder" class="background" fit="cover" :src="lastBackgroundUrl" />
        <el-image slot="error" class="background" fit="cover" :src="defaultBackground" />
      </el-image>
    </div>
    <el-image
      class="background"
      fit="cover"
      :src="lastBackgroundUrl"
      :style="{display:backgroundLoading?'block':'none'}"
    >
      <el-image slot="error" class="background" fit="cover" :src="defaultBackground" />
    </el-image>
  </div>
</template>

<script>

import background from '../asset/background.jpg'

export default {
  name: 'Background',
  props: {
    mask: {
      type: Boolean,
      required: false,
      default: () => {
        return true
      }
    }
  },
  data() {
    return {
      defaultBackground: background,
      lastBackgroundUrl: background,
      backgroundUrl: background,
      backgroundLoading: true
    }
  },
  computed: {
    maskBG() {
      const rgba = `rgba(0, 0, 0, ${this.mask ? 0.37 : 0})`
      return { backgroundColor: rgba }
    }
  },
  created() {
    this.changeBackground()
    this.setBackgroundChangeInterval()
  },
  methods: {
    getRandomBackgroundUrl() {
      const img_api = 'https://api.btstu.cn/sjbz/api.php?method=zsy&lx=suiji'
      return `${img_api}&_t=${new Date().getTime()}`
    },
    changeBackground() {
      this.backgroundUrl = this.getRandomBackgroundUrl()
      this.backgroundLoading = true
    },
    setBackgroundChangeInterval() {
      setInterval(this.changeBackground, 1000 * 60 * 5)
    },
    backgroundLoaded() {
      this.backgroundLoading = false
      this.lastBackgroundUrl = this.backgroundUrl
    }
  }
}
</script>

<style scoped lang="scss">

.container {
  user-select: none;
  position: relative;
  transition: all 1s ease;
}

.background {
  z-index: -1024;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  position: absolute;
  transition: all 1s ease;
}

.loading {
  opacity: .36;
  filter: blur(5px);
}

.loaded {
  opacity: 1;
  filter: blur(0px);
}

</style>
