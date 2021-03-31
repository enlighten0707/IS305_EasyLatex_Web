<!--图片上传，常用公式加载-->
<!--显示结果能修改，查看渲染后的结果，计算结果-->
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
        <el-row>
          <el-col :span="8" :offset="3">
          <el-upload
            class="avatar-uploader"
            action="http://127.0.0.1:8000/api/sketchProcess/"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload">
            <img v-if="imageUrl" :src="imageUrl" class="avatar" id="uploadImage">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
          </el-col>
        </el-row>
        <el-row>
          <el-button type="primary" icon="el-icon-edit" circle @click="RequestAPI"></el-button>
          <hr/>
          <el-button type="primary" icon="el-icon-search" circle @click="copyToClip"></el-button>
          <el-input
            type="textarea"
            id="result_str"
            :rows="2"
            :autosize="{ minRows: 2, maxRows: 6}"
            v-model="textarea"
          placeholder="请输入内容">
          </el-input>
          <el-button type="primary" icon="el-icon-search" id="render" @click="convert"></el-button>
          <div id="output"></div>
        </el-row>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'ColorizationPage',
  data () {
    return {
      background: null,
      imageUrl: '',
      textarea: '',
      // textarea: 'x = {-b \\pm \\sqrt{b^2-4ac} \\over 2a}'
    }
  },
  methods: {
    convert() {
      console.log(1)
      //
      //  Get the TeX input
      //
      var input = document.getElementById('result_str').value.trim()
      //
      //  Disable the display and render buttons until MathJax is done
      //
      // var display = document.getElementById('display')
      var button = document.getElementById('render')
      // button.disabled = display.disabled = true
      //
      //  Clear the old output
      //
      var out = document.getElementById('output')
      out.innerHTML = ''
      //
      //  Reset the tex labels (and automatic equation numbers, though there aren't any here).
      //  Get the conversion options (metrics and display settings)
      //  Convert the input to CommonHTML output and use a promise to wait for it to be ready
      //    (in case an extension needs to be loaded dynamically).
      //
      MathJax.texReset()
      var options = MathJax.getMetricsFor(out)
      // options.display = display.checked
      MathJax.tex2chtmlPromise(input, options).then(function (node) {
        //
        //  The promise returns the typeset node, which we add to the output
        //  Then update the document to include the adjusted CSS for the
        //    content of the new equation.
        //
        out.appendChild(node)
        MathJax.startup.document.clear()
        MathJax.startup.document.updateDocument()
      }).catch(function (err) {
        //
        //  If there was an error, put the message into the output instead
        //
        out.appendChild(document.createElement('pre')).appendChild(document.createTextNode(err.message))
      }).then(function () {
        //
        //  Error or not, re-enable the display and render buttons
        //
        // button.disabled = display.disabled = false
      })
    },
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
    ZhMathJax: function (Id) {
      let _this = this
      setTimeout(function () {
        if (_this.globalVariable.isMathjaxConfig == false) { // 判断是否初始配置，若无则配置。
          _this.globalVariable.initMathjaxConfig()
        }
        _this.globalVariable.MathQueue(Id)// 传入组件id，让组件被MathJax渲染
      }, 500)
    },
    confirm: function () {
      // 每次点击先清空上次显示的latex公式
      document.getElementById('ShowLatexData').innerHTML = ''
      // var latexData="$$\left\{\begin{array}{l}x^2-2 x-3=0 \\ x+2=1\end{array}\right.$$"
      // 由于动态赋值单斜杠会不能识别，所以转移双斜杠   但是从后台拿取的数据可以直接赋值渲染
      var latexData = '$$\\left\\{\\begin{array}{l}x^2-2 x-3=0 \\\\ x+2=1\\end{array}\\right.$$'
      // this.$axios.post('mathAnalysisOne',{sectiontext:latexData}).then(successResponse=>{
      //     console.log(successResponse.data)
      //     console.log(successResponse.data.answer[0])
      document.getElementById('ShowLatexData').innerHTML = latexData
      this.ZhMathJax('KatexData')
      // }).
      // catch();
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
        console.log(document.getElementById('result_str').innerText)
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
