<template>
  <div class="container">
    <v-type-header ref="typeHeader" @refresh="refresh"></v-type-header>
    <el-scrollbar id="bg-container" class="content-area">
      <div class="find-bgs" :style="{transform:firstInit ?'translateY(-120%)':'translateY(0)'}">
        <i class="el-icon-search"></i>共找到 {{ total }} 张壁纸
      </div>
      <el-row
        v-infinite-scroll="getBgsWhenScrollToBottom"
        infinite-scroll-disabled="loading"
        type="flex"
        justify="center"
      >
        <el-col :span="20">
          <el-row v-for="(value,key) of data" :key="key" :gutter="20">
            <el-col :data-page="key">
              <div class="page-divider">
                <div class="page-info">第<span> {{ key }} </span>页，共 {{ last_page }} 页</div>
                <div class="divider"></div>
                <div class="to-top" @click="toTop"><i class="el-icon-arrow-up"></i></div>
              </div>
            </el-col>
            <el-col v-for="(bg) of value" :key="bg.id" class="bgItem">
              <v-image :data="bg" :data-list="value"></v-image>
            </el-col>
          </el-row>
          <div v-if="dataLoading" class="loading">
            <span><i class="el-icon-loading"></i> 正在加载壁纸···</span>
          </div>
          <div v-else-if="noMore" class="loading">
            <span>— 已经到底了 —</span>
          </div>
        </el-col>
      </el-row>
      <el-backtop />
    </el-scrollbar>
  </div>
</template>

<script>

import { getBgs } from '../api/index'

export default {
  name: 'Type',
  components: {
    'v-type-header': () => import('../component/TypeHeader.vue'),
    'v-image': () => import('../component/Image')
  },
  data() {
    return {
      dataLoading: false,
      firstInit: true,
      data: {}, // {1:[],2:{}}
      params: {},
      total: 0,
      current_page: 0,
      last_page: 1
    }
  },
  computed: {
    loading: function() {
      return this.dataLoading || this.firstInit || this.current_page >= this.last_page
    },
    noMore: function() {
      return this.total > 0 && this.current_page >= this.last_page
    }
  },
  created() {
    // this.$nextTick(() => {
    //   this.$refs.typeHeader.refresh()
    // })
  },
  methods: {
    toTop() {
      document.querySelector('#bg-container .el-scrollbar__view').scrollIntoView(true, {
        behavior: 'smooth',
        block: 'start'
      })
    },
    refresh(params) {
      this.data = {}
      this.params = params
      this.firstInit = true
      this.getBgs()
    },
    getBgsWhenScrollToBottom() {
      if (this.dataLoading || this.firstInit) return
      if (Object.keys(this.params).length === 0) {
        this.params = this.$refs.typeHeader.getParams()
      }
      this.getBgs()
    },
    getBgs() {
      this.dataLoading = true
      getBgs(this.params).then(resp => {
        if (!resp || !(resp instanceof Object)) {
          this.$message.error('数据加载失败，请重试')
          this.dataLoading = false
        }
        this.data['' + resp.meta.current_page] = resp.data
        if (!this.params.seed && this.params.sorting === 'random') {
          this.params.seed = resp.meta.seed
        }
        this.total = resp.meta.total
        this.current_page = resp.meta.current_page
        this.last_page = resp.meta.last_page
        this.params.page = (resp.meta.current_page || 0) + 1
        this.$nextTick(() => {
          setTimeout(() => {
            this.dataLoading = false
            this.firstInit = false
          }, 200)
        })
      }).catch(() => {
        this.$message.error('数据加载失败，请重试')
        this.dataLoading = false
      })
    }
  }
}
</script>

<style scoped lang="scss">
.container {
  background: url(../asset/blue-gradients.jpg) top center/cover no-repeat fixed,
  #171717 url(../asset/bg-dark-grain.png) top left repeat;
}

.content-area {
  position: absolute;
  top: 60px;
  left: 0;
  width: 100vw;
  height: calc(100vh - 60px);
  overflow: hidden;
  @media only screen and (max-width: 1000px) {
    top: 96px;
    height: calc(100vh - 96px);
  }

  .loading {
    color: #ffffff;
    font-size: 16px;
    text-align: center;
    padding: 24px 0 36px 0;
  }

  .find-bgs {
    display: flex;
    align-items: center;
    font-size: 32px;
    color: #ddd;
    padding: 16px 0 6px 1%;
    transition: all .3s ease;
    transform: translateY(-120%);
    user-select: none;

    i {
      margin-right: 10px;
      color: #4499ff;
      font-size: 36px;
    }
  }
}

.el-col {
  margin: 10px 0;
}

div[data-page="1"] {
  display: none;
}

.page-divider {
  display: flex;
  align-items: center;
  margin: 0 -5%;
  color: #ddd;
  font-size: 14px;

  .page-info {
    padding-right: 20px;
    white-space: nowrap;

    span {
      font-size: 18px;
    }
  }

  .divider {
    background-color: #ddd;
    height: 1px;
    width: 100%;
  }

  .to-top {
    font-size: 20px;
    font-weight: 600 !important;
    margin-left: 7px;
    transition: all .25s ease;

    &:hover {
      cursor: pointer;
      color: #64a5ff;
    }
  }
}

.bgItem {
  @media only screen and (max-width: 768px) {
    width: 50%;
  }
  @media only screen and (min-width: 768px) {
    width: 33.33333%;
  }
  @media only screen and (min-width: 992px) {
    width: 25%;
  }
  @media only screen and (min-width: 1200px) {
    width: 20%;
  }
}

</style>

<style lang="scss">
.el-scrollbar__wrap {
  overflow-x: hidden;
}
</style>

