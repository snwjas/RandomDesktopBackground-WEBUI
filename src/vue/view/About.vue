<template>
  <div class="container">
    <img :src="logo" alt="" class="icon">
    <div class="intro">
      <div class="title">‖ 随机桌面壁纸 ‖</div>
      <div class="subtitle">「让你的桌面壁纸就像一盒巧克力一样, 永远不知道下一颗是什么味道」</div>
    </div>
    <div class="info">
      <div>版本：2.2022.01.01</div>
      <div>版权：Copyright © 2022 By
        <a title="作者主页" target="_blank" href="http://refrain.xyz">Myles Yang</a>
      </div>
      <div>GitHub：
        <a title="项目主页" target="_blank" href="https://github.com/snwjas/RandomDesktopBackground">
          https://github.com/snwjas/RandomDesktopBackground
        </a>
      </div>
      <div>
        Gitee：
        <a title="项目主页" target="_blank" href="https://github.com/snwjas/RandomDesktopBackground">
          https://gitee.com/snwjas/random-desktop-background
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import logo from '../asset/logo.png'

export default {
  name: 'About',
  data() {
    return {
      logo: logo
    }
  }
}
</script>

<style scoped lang="scss">
.container {
  position: relative;
}

.icon {
  width: 3.6vw;
  height: 3.6vw;
  position: absolute;
  top: -0.66vw;
  left: -0.52vw;
}

.intro {
  text-align: center;

  .title {
    font-size: 1.75vw;
    margin-bottom: 0.55vw;
  }

  .subtitle {
    font-size: 1.15vw;
    margin-bottom: 1vw;
  }
}

.info {
  font-size: 0.9vw;
  line-height: 200%;
  width: fit-content;
  margin: 0 auto;
}
</style>
