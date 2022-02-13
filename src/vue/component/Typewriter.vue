<template>
  <div class="slogon">
    <span>{{ lside }}</span>
    <span class="typed-quotes" @click="toggleTyping">{{ typeQuotes }}</span>
    <span class="typed-cursor" :style="{'display' : typedCursorShow ? 'inline-block' : 'none'}">|</span>
    <span>{{ rside }}</span>
  </div>
</template>

<script>
import { sleep } from '../util/common'

export default {
  name: 'Typing',
  props: {
    content: {
      type: String,
      required: true
    },
    lside: {
      type: String,
      required: false,
      default: () => {
        return ''
      }
    },
    rside: {
      type: String,
      required: false,
      default: () => {
        return ''
      }
    }
  },
  data() {
    return {
      isTyping: true,
      typedCursorShow: true,
      typeQuotes: '',
      typeQuotesIndex: 0
    }
  },
  created() {
    this.typingInterval()
  },
  methods: {
    async typingInterval() {
      while (this.isTyping) {
        // 往前打字
        while (this.isTyping && this.typeQuotesIndex < this.content.length) {
          this.typeQuotes += this.content.charAt(this.typeQuotesIndex)
          this.typeQuotesIndex++
          await sleep(100)
        }
        if (!this.isTyping) return
        await sleep(3600)
        if (!this.isTyping) return
        // 删除
        while (this.typeQuotesIndex > 0) {
          this.typeQuotes = this.typeQuotes.substring(0, this.typeQuotes.length - 1)
          this.typeQuotesIndex--
          await sleep(36)
        }
      }
    },
    async toggleTyping() {
      if (this.isTyping) {
        this.isTyping = false
        // 继续打完
        while (this.typeQuotesIndex < this.content.length) {
          await sleep(100)
          this.typeQuotes += this.content.charAt(this.typeQuotesIndex)
          this.typeQuotesIndex++
        }
        this.typedCursorShow = false
      } else {
        this.typedCursorShow = true
        while (this.typeQuotesIndex > 0) {
          this.typeQuotes = this.typeQuotes.substring(0, this.typeQuotes.length - 1)
          this.typeQuotesIndex--
          await sleep(36)
        }
        this.isTyping = true
        await this.typingInterval()
      }
    }
  }
}
</script>

<style scoped lang="scss">
.slogon {
  color: #f0f0f0;
}

.typed-cursor {
  animation: blink .7s infinite;
  @keyframes blink {
    0% {
      opacity: 1
    }
    50% {
      opacity: 0
    }
    100% {
      opacity: 1
    }
  }
}

</style>
