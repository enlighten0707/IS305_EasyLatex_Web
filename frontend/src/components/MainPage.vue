<!--图片上传，常用公式加载-->
<!--显示结果能修改，查看渲染后的结果，计算结果-->
<template>
  <el-container>
    <el-header class="m-header">
      <img
        src="../assets/panda.png"
        style="height: 75px; float: left; margin-left: 10px"
      />
      <span style="float: right; margin-right: 50px">
        <el-button type="success" icon="el-icon-view" round plain size="small" @click="handleAvatarSuccess"
                   style="margin:10px">
            识别公式
        </el-button>
        <el-button type="primary" icon="el-icon-view" id="render" round plain size="small" @click="convert"
                   style="margin:10px">
            预览公式
          </el-button>
        <el-button type="info" icon="el-icon-document-copy" round plain size="small" @click="copyToClip"
                   style="margin:10px">
            复制公式
        </el-button>
        <!--        <el-button type="info" icon="el-icon-document-copy" round plain size="small" @click="save"-->
        <!--                   style="margin:10px">-->
        <!--            保存公式-->
        <!--        </el-button>-->
      </span>
    </el-header>
    <hr/>
    <el-container>
      <!--      <el-col :span="2" :offset="1">-->
      <!--        <el-row style="display:inline-block;margin:20px;">-->
      <!--          <el-button type="primary" icon="el-icon-view" id="render" round plain size="small" @click="convert">-->
      <!--            预览-->
      <!--          </el-button>-->
      <!--        </el-row>-->
      <!--        <el-row style="display:inline-block;margin:20px;">-->
      <!--          <el-button type="info" icon="el-icon-document-copy" round plain size="small" @click="copyToClip">-->
      <!--            复制-->
      <!--          </el-button>-->
      <!--        </el-row>-->
      <!--      </el-col>-->
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
                <div class="el-upload__text">
                  <em>拖曳</em>或<em>点击</em>上传，支持多行公式识别
                </div>
              </el-upload>
            </el-row>
            <!--            <el-button type="primary" icon="el-icon-edit" circle @click="RequestAPI"></el-button>-->
            <el-row>
              <el-input
                type="textarea"
                id="result_str"
                :rows="3"
                :autosize="{ minRows: 6, maxRows: 12}"
                v-model="textarea"
                @input="convert"
                placeholder="公式识别结果/公式编辑框（以Latex源码形式显示）">
              </el-input>
              <div id="output"></div>
            </el-row>
          </el-col>
          <el-col :span="9" offset="2" style="display:inline-block;">
            <el-tabs type="border-card" value="first">
              <el-tab-pane label="高等数学" name="first">
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\sum</div>
                      <span>\(\sum\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\sum_{i=1}^\infty</div>
                      <span>\(\sum_{i=1}^\infty\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\prod_{i=1}^n</div>
                      <span>\(\prod_{i=1}^n\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\int_{-N}^ {N} e^x \mathrm{d}x</div>
                      <span>\(\int_{-N}^ {N} e^x \mathrm{d}x\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\iint_{a}^{b} \mathrm{d}x \mathrm{d}y</div>
                      <span>\(\iint_{a}^{b} \mathrm{d}x \mathrm{d}y\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\oint_{D} x^ 2 \mathrm{d}x + 4y^2 \mathrm{d}y</div>
                      <span>\(\oint_{D} x^ 2 \mathrm{d}x + 4y^2 \mathrm{d}y\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\partial x</div>
                      <span>\(\partial x\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\frac{\partial}{\partial x}h(x,y)</div>
                      <span>\(\frac{\partial}{\partial x}h(x,y)\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\mathrm{d}x</div>
                      <span>\(\mathrm{d}x\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\frac{\mathrm{d}y}{\mathrm{d}x}</div>
                      <span>\(\frac{\mathrm{d}y}{\mathrm{d}x}\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\lim_{n\to\infty}</div>
                      <span>\(\lim_{n\to\infty}\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
              </el-tab-pane>
              <el-tab-pane label="希腊字母" name="second">
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\alpha</div>
                      <span>\(\alpha\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\beta</div>
                      <span>\(\beta\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\eta</div>
                      <span>\(\eta\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\gamma</div>
                      <span>\(\gamma\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\phi</div>
                      <span>\(\phi\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\pi</div>
                      <span>\(\pi\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\rho</div>
                      <span>\(\rho\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\sigma</div>
                      <span>\(\sigma\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\tau</div>
                      <span>\(\tau\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\lambda</div>
                      <span>\(\lambda\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\varepsilon</div>
                      <span>\(\varepsilon\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\theta</div>
                      <span>\(\theta\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\delta</div>
                      <span>\(\delta\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\psi</div>
                      <span>\(\psi\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\varphi</div>
                      <span>\(\varphi\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\Gamma</div>
                      <span>\(\Gamma\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\Lambda</div>
                      <span>\(\Lambda\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\Theta</div>
                      <span>\(\Theta\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
              </el-tab-pane>
              <el-tab-pane label="集合逻辑" name="third">
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\le</div>
                      <span>\(\le\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\ge</div>
                      <span>\(\ge\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\sim</div>
                      <span>\(\sim\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\subset</div>
                      <span>\(\subset\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\subseteq</div>
                      <span>\(\subseteq\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\supset</div>
                      <span>\(\supset\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\cup</div>
                      <span>\(\cup\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\cap</div>
                      <span>\(\cap\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\lor</div>
                      <span>\(\lor\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\land</div>
                      <span>\(\land\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
              </el-tab-pane>
              <el-tab-pane label="矩阵运算" name="forth">
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\begin{matrix}0 & 1 \\1 & 0\end{matrix}</div>
                      <span>\(\begin{matrix}0 & 1 \\1 & 0\end{matrix}\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\begin{bmatrix}0 & 1 \\1 & 0\end{bmatrix}</div>
                      <span>\(\begin{bmatrix}0 & 1 \\1 & 0\end{bmatrix}\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\begin{pmatrix}0 & 1 \\1 & 0\end{pmatrix}</div>
                      <span>\(\begin{pmatrix}0 & 1 \\1 & 0\end{pmatrix}\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\begin{vmatrix}0 & 1 \\1 & 0\end{vmatrix}</div>
                      <span>\(\begin{vmatrix}0 & 1 \\1 & 0\end{vmatrix}\)</span>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\begin{Vmatrix}0 & 1 \\1 & 0\end{Vmatrix}</div>
                      <span>\(\begin{Vmatrix}0 & 1 \\1 & 0\end{Vmatrix}\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
                <el-row>
                  <el-col :span="8">
                    <el-tooltip placement="bottom" enterable="true">
                      <div slot="content" style="font-size:8px">\begin{bmatrix}a_{11}&\dots&a_{1n}\\& \ddots&\vdots\\0 &&a_{nn}\end{bmatrix}_{n \times n}</div>
                      <span>\(\begin{bmatrix}a_{11}&\dots&a_{1n}\\& \ddots&\vdots\\0 &&a_{nn}\end{bmatrix}_{n \times n}\)</span>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-divider></el-divider>
              </el-tab-pane>
            </el-tabs>
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
