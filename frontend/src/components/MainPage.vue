<template>
  <el-upload
    class="upload-demo"
    :show-file-list="false"
    drag
    :before-upload="onBeforeUpload"
    :on-success="onSuccess"
    action="https://jsonplaceholder.typicode.com/posts/"
  >
<!--    <i class="el-icon-upload"></i>-->
    <img v-if="model.icon" :src="model.icon" class="avatar">
    <i v-else class="el-icon-plus avatar-uploader-icon"></i>
<!--    <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>-->
<!--          <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>-->
  </el-upload>
</template>

<script>
export default {
  name: 'MainPage',
  methods: {
    onBeforeUpload (file) {
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
    onSuccess (res, file) {
      // const reader = new FileReader()
      // reader.onload = function (ev) {
      //   // base64码
      //   var imgFile = ev.target.result// 或e.target都是一样的
      //   document.querySelector('img').src = ev.target.result
      // }
      // 发起异步读取文件请求，读取结果为data:url的字符串形式，
      // this.$message.success(file.files[0])
      // reader.readAsDataURL(file.files[0])
      // this.background = 'data:image/png;base64,' + res
      this.$set(this.model, 'icon', res.url)
      this.$message.success('Uploaded successfully!')
      // this.iconVal = res
    }
  }
}
</script>

<style scoped>

</style>
