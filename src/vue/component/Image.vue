<template>
  <div class="image-container" :style="{cursor: loaded?'pointer':'default'}">
    <el-image
      v-if="updated"
      :src="data.thumbs.small"
      :preview-src-list="previewSrcList"
      :alt="data.id"
      fit="cover"
      class="image"
      @load="loaded=true"
    >
      <div slot="placeholder" class="placeholder-slot">
        <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M64 896V128h896v768H64z m64-128l192-192 116.352 116.352L640 448l256 307.2V192H128v576z m224-480a96 96 0 1 1-0.064 192.064A96 96 0 0 1 352 288z"
          />
        </svg>
      </div>
      <div slot="error" class="error-slot">
        加载失败，
        <el-button type="text" @click="refreshBg">点击重试</el-button>
      </div>
    </el-image>
    <div v-if="loaded">
      <div class="image-info clearfix">
        <div class="wall-favs el-icon-star-off">{{ data.favorites }}</div>
        <div class="wall-res">{{ data.dimension_x }} x {{ data.dimension_x }}</div>
        <div v-if="fileType === 'png'" class="wall-typ png">PNG</div>
        <div v-else-if="fileType === 'jpg'" class="wall-typ jpg">JPG</div>
        <div v-else class="wall-typ udf">{{ fileType }}</div>
      </div>
      <div class="image-dwn" @click="dwnBg">{{ fileSize }} <i class="el-icon-download"></i></div>
    </div>
  </div>
</template>

<script>
import { convertBit, downloadFile } from '../util/common'

export default {
  name: 'TImage',
  props: {
    data: {
      type: Object,
      required: true
    },
    dataList: {
      type: Array,
      required: false,
      default: function() {
        return [this.data.path]
      }
    }
  },
  data() {
    return {
      previewSrcList: [],
      loaded: false,
      updated: true
    }
  },
  computed: {
    fileType: function() {
      const t = this.data.file_type || ''
      const fileType = t.substring(t.lastIndexOf('/') + 1)
      return fileType === 'jpeg' ? 'jpg' : fileType
    },
    fileSize: function() {
      return convertBit(this.data.file_size)
    }
  },
  created() {
    this.setPreviewSrcList()
  },
  methods: {
    // data.path
    setPreviewSrcList() {
      if (this.dataList && this.dataList.length > 1) {
        this.previewSrcList.push(this.data.path)
        let arriveSelf = false
        const tmp = []
        for (const item of this.dataList) {
          if (arriveSelf) {
            this.previewSrcList.push(item.path)
          } else {
            if (item.path === this.data.path) {
              arriveSelf = true
              this.previewSrcList.push(item.path)
            } else {
              tmp.push(item.path)
            }
          }
        }
        this.previewSrcList.push(...tmp)
      }
    },
    refreshBg() {
      this.updated = false
      this.$nextTick(() => {
        this.updated = true
      })
    },
    dwnBg() {
      const fileName = 'wallhaven-' + this.data.id
      downloadFile(this.data.path, fileName)
    }
  }

}
</script>

<style lang="scss">
.image-container {
  // 3 : 2
  width: 100%;
  padding-top: 66.66667%;
  background-color: #ddd;
  position: relative;
  border-radius: 5px;
  overflow: hidden;
  user-select: none;

  &:hover {
    .image-info {
      transform: translateY(0);
    }

    .image-dwn {
      opacity: 1;
    }
  }

  .image {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    overflow: hidden;

    .error-slot {
      z-index: 1;
      position: absolute;
      top: 50%;
      left: 50%;
      width: 100%;
      transform: translateX(-50%) translateY(-50%);
      text-align: center;
      color: #606266;

      * {
        font-size: 16px;
      }
    }

    .placeholder-slot {
      z-index: 1;
      position: absolute;
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(90deg, #f2f2f2 25%, #e6e6e6 37%, #f2f2f2 63%);
      background-size: 400% 100%;
      animation: el-skeleton-loading 1.4s ease infinite;
      @keyframes el-skeleton-loading {
        0% {
          background-position: 100% 50%
        }
        to {
          background-position: 0 50%
        }
      }

      svg {
        fill: #dcdde0 !important;
        width: 36%;
        height: 36%;
      }
    }
  }

  .image-info {
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    left: 0;
    bottom: 0;
    padding: 5px 7px;
    transform: translateY(100%);
    transition: all .3s ease;
    background-color: rgba(0, 0, 0, .2333);
    color: #fff;
    font-size: 14px;
    user-select: none;
    cursor: default;

    .wall-res {
      width: 100%;
      text-align: center;
      font-style: italic;
    }

    .wall-typ {
      border-radius: 3px;
      font-size: 12px;
      padding: 2px 6px;
      line-height: inherit;
      text-transform: uppercase;
    }

    .wall-typ.png {
      background-color: #db7c0f;
    }

    .wall-typ.jpg {
      background-color: #5daf34;
    }

    .wall-typ.unk {
      background-color: #3a8ee6;
    }
  }

  .image-dwn {
    color: #fff;
    font-size: 12px;
    position: absolute;
    top: 0;
    right: 0;
    padding: 4px 7px;
    background-color: #409EFF;
    border-bottom-left-radius: 5px;
    opacity: 0;
    transition: all .3s ease;

    &:hover {
      background-color: #3c9cfd;
    }

    &:active {
      background-color: #3a8ee6;
    }
  }
}
</style>
