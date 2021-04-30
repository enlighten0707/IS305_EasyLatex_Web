<template>
  <div id="app">
    <easy-latex-page></easy-latex-page>
  </div>
</template>

<script>
import EasyLatexPage from './components/EasyLatex_Page'

export default {
  name: 'App',
  components: {
    EasyLatexPage
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>
