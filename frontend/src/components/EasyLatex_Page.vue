<template>
  <el-container>
    <!--    顶部菜单栏    -->
    <el-header class="m-header">
      <img
        src="../assets/logo.png"
        style="height: 75px; float: left; margin-left: 10px"
      />
      <span style="float: right; margin-right: 50px">
        <el-button type="success" icon="el-icon-view" round plain size="small" @click="handleAvatarSuccess"
                   style="margin:10px">
            识别公式
        </el-button>
        <el-button type="primary" icon="el-icon-view" round plain size="small" @click="formulaRender"
                   style="margin:10px">
            预览公式
          </el-button>
        <el-button type="info" icon="el-icon-document-copy" round plain size="small" @click="copyToClip"
                   style="margin:10px">
            复制公式
        </el-button>
      </span>
    </el-header>
    <hr/>
    <el-container>
      <el-main>
        <el-row>
          <!--          页面主体左部分，包括图片上传框，公式编辑框，公式显示框    -->
          <el-col :span="9" :offset="2">
            <el-row>
              <el-upload
                class="upload-demo"
                drag
                action="/api/uploadImg/"
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
            <el-row>
              <el-input
                type="textarea"
                id="result_str"
                :rows="3"
                :autosize="{ minRows: 6, maxRows: 12}"
                v-model="textarea"
                @input="formulaRender"
                placeholder="公式识别结果/公式编辑框（以Latex源码形式显示）">
              </el-input>
              <div id="output"></div>
            </el-row>
          </el-col>
          <!--          页面主体部分右部分，显示常用公式      -->
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
                      <div slot="content" style="font-size:8px">\begin{bmatrix}a_{11}&\dots&a_{1n}\\& \ddots&\vdots\\0
                        &&a_{nn}\end{bmatrix}_{n \times n}
                      </div>
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
  name: 'EasyLatexPage',
  data () {
    return {
      background: null,
      imageUrl: '',
      textarea: ''
    }
  },
  methods: {
    formulaRender () {
      // formulaRender: 利用MathJax渲染整个页面，显示预览公式
      var input = document.getElementById('result_str').value // 获取当前公式Latex源码
      var out = document.getElementById('output')
      out.innerHTML = '' // 清空原先的渲染结果

      MathJax.texReset()
      var options = MathJax.getMetricsFor(out)
      MathJax.tex2chtmlPromise(input, options).then(function (node) {
        out.appendChild(node)
        MathJax.startup.document.clear()
        MathJax.startup.document.updateDocument()
      }).catch(function (err) {
        // 如果渲染出现错误，在页面上显示提示文字
        out.appendChild(document.createElement('pre')).appendChild(document.createTextNode(err.message))
      }).then(function () {
      })
    },

    copyToClip () {
      // copyToClip: 将公式Latex源码复制到系统剪贴板
      let input = document.getElementById('result_str')
      input.select() // 选中元素中的文本（必须可编辑）

      if (document.execCommand('copy')) { // 检测复制命令返回值（是否可用）
        document.execCommand('copy')
        window.alert('已复制！')
      } else { // 无法复制（不可用）
        window.alert('复制失败！')
      }
    },

    handleAvatarSuccess (res, file) {
      // handleAvatarSuccess: 上传图片成功后的操作
      this.imageUrl = URL.createObjectURL(file.raw)
      this.$axios.post('/api/Formula_Recognition/').then(res => {
        document.getElementById('result_str').innerText = res.data
      }) // 向后端发出请求，进行图片公式识别，并返回到页面中的result_str元素
      this.formulaRender() // 在页面上渲染公式
    },

    beforeAvatarUpload (file) {
      // beforeAvatarUpload: 上传图片的操作，包括文件类型、大小检查等
      const isIMAGE = file.type === 'image/jpeg' || file.type === 'image/png'
      const isLt1M = file.size / 1024 / 1024 < 1
      if (!isIMAGE) {
        this.$message.error('The uploaded file can only be in image format!')
      }
      if (!isLt1M) {
        this.$message.error('The size of the uploaded file cannot exceed 1MB!')
      }
      return isIMAGE && isLt1M
    }
  }
}
</script>

<style>
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

body > .el-container {
  margin-bottom: 40px;
}

.el-card {
  width: 555px;
  height: 555px;
  margin-left: 3em;
  float: left;
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
