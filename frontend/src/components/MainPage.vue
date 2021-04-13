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
          <el-col :span="9" :offset="2">
            <!--          <el-upload-->
            <!--            class="avatar-uploader"-->
            <!--            action="http://127.0.0.1:8000/api/sketchProcess/"-->
            <!--            :show-file-list="false"-->
            <!--            :on-success="handleAvatarSuccess"-->
            <!--            :before-upload="beforeAvatarUpload">-->
            <!--            <img v-if="imageUrl" :src="imageUrl" class="avatar" id="uploadImage">-->
            <!--            <i v-else class="el-icon-plus avatar-uploader-icon"></i>-->
            <!--          </el-upload>-->
            <el-row>
              <el-upload
                class="upload-demo"
                drag
                action="http://127.0.0.1:8000/api/sketchProcess/"
                multiple
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload">
                <img v-if="imageUrl" :src="imageUrl" class="avatar" id="uploadImage">
                <i v-else class="el-icon-upload"></i>
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              </el-upload>
            </el-row>
            <!--            <el-button type="primary" icon="el-icon-edit" circle @click="RequestAPI"></el-button>-->
            <el-row>
              <el-input
                type="textarea"
                id="result_str"
                :rows="3"
                :autosize="{ minRows: 3, maxRows: 6}"
                v-model="textarea"
                @input="convert"
                placeholder="公式识别结果（Latex源码）">
              </el-input>
              <el-button type="primary" icon="el-icon-view" id="render" round plain size="small" @click="convert">
                预览
              </el-button>
              <el-button type="info" icon="el-icon-document-copy" round plain size="small" @click="copyToClip">
                复制
              </el-button>
              <div id="output"></div>
              <!--              <el-pagination @current-change="handleCurrentChange"-->
              <!--                             :current-page="currentPage"-->
              <!--                             layout="prev, pager, next"-->
              <!--                             :page-size="1"-->
              <!--                             :total="totalCount">-->
              <!--              </el-pagination>-->
            </el-row>
          </el-col>
          <el-col :span="10" offset="2" style="display:inline-block;">
            <el-tabs tab-position="right">
              <el-tab-pane label="高等数学" name="first">
                <el-row>
                  <el-col :span="8"><span>\(\sum\)</span></el-col>
                  <el-col :span="8"><span>\(\sum_{i=1}^\infty\)</span></el-col>
                  <el-col :span="8"><span>\(\prod_{i=1}^n\)</span></el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8"><span>\(\lim_{n\to\infty}\)</span></el-col>
                  <el-col :span="8"><span></span></el-col>
                  <el-col :span="8"><span></span></el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8"><span>\(\partial x\)</span></el-col>
                  <el-col :span="8"><span>\(\frac{\partial}{\partial x}h(x,y)\)</span></el-col>
                  <el-col :span="8"><span></span></el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8"><span>\(\mathrm{d}x\)</span></el-col>
                  <el-col :span="8"><span>\(\frac{\mathrm{d}y}{\mathrm{d}x}\)</span></el-col>
                  <el-col :span="8"><span></span></el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8"><span>\(\int_{-N}^ {N} e^x \mathrm{d}x\)</span></el-col>
                  <el-col :span="8"><span>\(\iint_{a}^{b} \mathrm{d}x \mathrm{d}y\)</span></el-col>
                  <el-col :span="8"><span>\(\oint_{D} x^ 2 \mathrm{d}x + 4y^2 \mathrm{d}y\)</span></el-col>
                </el-row>
              </el-tab-pane>
              <el-tab-pane label="字母符号" name="second">
                <el-row>
                  <el-col :span="8"><span>\(\alpha\)</span></el-col>
                  <el-col :span="8"><span>\(\beta\)</span></el-col>
                  <el-col :span="8"><span>\(\eta\)</span></el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8"><span>\(\gamma\)</span></el-col>
                  <el-col :span="8"><span>\(\phi\)</span></el-col>
                  <el-col :span="8"><span>\(\pi\)</span></el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8"><span>\(\rho\)</span></el-col>
                  <el-col :span="8"><span>\(\sigma\)</span></el-col>
                  <el-col :span="8"><span>\(\tau\)</span></el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8"><span>\(\lambda\)</span></el-col>
                  <el-col :span="8"><span>\(\varepsilon\)</span></el-col>
                  <el-col :span="8"><span>\(\theta\)</span></el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8"><span>\(\delta\)</span></el-col>
                  <el-col :span="8"><span>\(\psi\)</span></el-col>
                  <el-col :span="8"><span>\(\varphi\)</span></el-col>
                </el-row>
                <el-divider></el-divider>
              </el-tab-pane>
            </el-tabs>

            <!--            <el-tabs v-model="activeName" tab-position="right" @tab-click="handleClick">-->
            <!--              <el-tab-pane label="高等数学" name="first">-->
            <!--                <el-row>-->
            <!--                  <el-col :span="8"><span>\(\sum\)</span></el-col>-->
            <!--                  <el-col :span="8"><span>\(\sum_{i=1}^\infty\)</span></el-col>-->
            <!--                  <el-col :span="8"><span>\(\sum_{k=1}^{n}\)</span></el-col>-->
            <!--                </el-row>-->
            <!--                <el-divider></el-divider>-->
            <!--                <el-row>-->
            <!--                  <el-col :span="8"><span>\(\prod_{i=1}^n\)</span></el-col>-->
            <!--                  <el-col :span="8"><span>\(\lim_{n\to\infty}\)</span></el-col>-->
            <!--                  <el-col :span="8"><span>\(\int_{-N}^ {N} e^x, dx`\)</span></el-col>-->
            <!--                </el-row>-->
            <!--              </el-tab-pane>-->
            <!--              <el-tab-pane label="线性代数" name="second">配置管理</el-tab-pane>-->
            <!--              <el-tab-pane label="常用函数" name="third">角色管理</el-tab-pane>-->
            <!--              <el-tab-pane label="字母符号" name="fourth">定时任务补偿</el-tab-pane>-->
            <!--            </el-tabs>-->
          </el-col>
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
      imageUrl: '',
      textarea: '',
      aaaa: ['\\sum', '\\sum_{k=1}^{n}', '\\sum_{i=1}^\\infty'],
      currentPage: 1,
      totalCount: 10
    }
  },
  methods: {
    // 显示第几页
    handleCurrentChange(val) {
      // 改变默认的页数
      this.currentPage = val
      console.log(this.currentPage)
      // 切换页码时，要获取每页显示的条数
      // this.getData(this.PageSize, (val) * (this.pageSize))
    },
    convert() {
      console.log(1)
      // var currentPage = document.getElementById('pagination').getAttribute('current-page')
      // console.log(currentPage)

      var input = document.getElementById('result_str').value
      console.log(input)
      //
      //  Disable the display and render buttons until MathJax is done
      //
      // var display = document.getElementById('display')
      // var button = document.getElementById('render')
      // button.disabled = display.disabled = true
      // var display
      // display.disabled = true
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
        // display.disabled = false
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
    handleAvatarSuccess(res, file) {
      // console.log(this.imageUrl)
      this.imageUrl = URL.createObjectURL(file.raw)
      // console.log(res.data)
      this.$axios.post('http://127.0.0.1:8000/api/XunFeiAPI/').then(res => {
        console.log(res.data)
        console.log(document.getElementById('result_str').innerText)

        document.getElementById('result_str').innerText = res.data
      })
      this.convert()
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
    // handleClick() {
    //   var b = document.querySelectorAll('.latex')
    //   var c = document.querySelectorAll('.formula')
    //
    //   this.$data.aaaa.forEach(function (v, i) {
    //     b[i].innerHTML = v
    //     var input = b[i].innerHTML
    //     var out = c[i]
    //     out.innerHTML = ''
    //
    //     MathJax.texReset()
    //     var options = MathJax.getMetricsFor(out)
    //     MathJax.tex2chtmlPromise(input, options).then(function (node) {
    //       out.appendChild(node)
    //       MathJax.startup.document.clear()
    //       MathJax.startup.document.updateDocument()
    //     })
    //   })
    // }
  }
}
</script>

<style>
.formula {
  display: inline-block;
  width: 70px;
  height: 20px;
}

.latex {
  display: inline-block;
  width: 70px;
  height: 20px;
}

.el-tab-pane {
  font-family: Arial;
  font-size: 14px;
}

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
  width: 350px;
  height: 150px;
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
  width: 360px;
  height: 180px;
  display: block;
}

#result_str {
  width: 360px;
  display: inline-block;
  position: relative;
  overflow: hidden;
}
</style>
