<template>
  <el-container>
    <el-header class="m-header">
      <img
        src="../assets/logo.png"
        style="height: 75px; float: left; margin-left: 10px"
      />
      <span style="float: right; margin-right: 20px">
      </span>
    </el-header>
    <hr/>
    <el-container>
      <el-main>
        <el-upload
          class="avatar-uploader"
          action="http://127.0.0.1:8000/api/sketchProcess/"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload">
          <img v-if="imageUrl" :src="imageUrl" class="avatar" id="uploadImage">
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
        <el-row>
          <el-button type="primary" icon="el-icon-edit" circle @click="RequestAPI"></el-button>
          <hr/>
          <el-input
            type="textarea"
            :rows="2"
            :autosize="{ minRows: 2, maxRows: 6}"
            placeholder="请输入内容"
            v-model="textarea"
            id="result_str">
          </el-input>
          <el-button type="primary" icon="el-icon-search" circle @click="copyToClip"></el-button>
        </el-row>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'ColorizationPage',
  data() {
    return {
      background: null,
      imageUrl: ''
    }
  },
  methods: {
    copyToClip() {
      let input = document.getElementById('result_str')
      // 选中元素中的文本（必须可编辑）
      input.select()
      // 检测复制命令返回值（是否可用）
      if (document.execCommand('copy')) {
        document.execCommand('copy')
        window.alert('已复制！')
        // eslint-disable-next-line brace-style
      }
      // 无法复制（不可用）
      else {
        window.alert('复制失败！')
      }
    },
    handleAvatarSuccess(res, file) {
      // console.log(this.imageUrl)
      this.imageUrl = URL.createObjectURL(file.raw)
      // console.log(res.data)

    },
    beforeAvatarUpload(file) {
      const isIMAGE = file.type === 'image/jpeg' || file.type === 'image/png'
      const isLt1M = file.size / 1024 / 1024 < 1
      if (!isIMAGE) {
        this.$message.error('The uploaded file can only be in image format!')
      }
      if (!isLt1M) {
        this.$message.error('The size of the uploaded file cannot exceed 1MB!')
      }
      return isIMAGE && isLt1M
    },

    RequestAPI() {
      this.$axios.post('http://127.0.0.1:8000/api/XunFeiAPI/').then(res => {
        console.log(res.data)
        document.getElementById('result_str').innerText = res.data
      })
    }
  }
}
</script>

<style>
.el-header {
  background-color: #ffffff;
  color: rgb(63, 58, 58);
  text-align: center;
  line-height: 80px;
  border-bottom: 1px solid rgb(211, 200, 200);
}

.m-header {
  height: 80px !important;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 240px;
  min-height: 400px;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}

.el-submenu {
  background-color: rgb(255, 255, 255);
}

.board {
  position: relative;
  min-height: 30%;
}

canvas {
  width: 512px;
  height: 512px;
  position: absolute;
  margin: 0 auto;
  left: 0;
  right: 0;
  top: 0;
  float: center;
  border: 1px solid rgb(233, 229, 229);
}

#ctx_front {
  z-index: 5;
}

#ctx_back {
  z-index: 3;
}

#ctx_base {
  z-index: 1;
}

.el-card {
  width: 555px;
  height: 555px;
  margin-left: 3em;
  float: left;
}

.inline-block {
  display: inline-block;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
