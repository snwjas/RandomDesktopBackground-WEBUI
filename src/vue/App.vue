<template>
  <div id="app">
    <transition name="fade-transform" mode="out-in">
      <router-view :key="key" />
    </transition>
  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {}
  },
  computed: {
    key() {
      return this.$route.path
    }
  },
  methods: {}
}
</script>

<style scoped lang="scss">

#app {
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

/* fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.28s;
}

.fade-enter,
.fade-leave-active {
  opacity: 0;
}

/* fade-transform */
.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all .5s;
}

.fade-transform-enter {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>

