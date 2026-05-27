<template>
  <div style="margin-top: 20px;margin-right: 20px;margin-left: 20px">
    <el-breadcrumb separator="/" class="el-breadcrumb-div">
      <el-breadcrumb-item :to="{ path: '/dashboard' }">数据监控</el-breadcrumb-item>
      <el-breadcrumb-item>数据分析</el-breadcrumb-item>
    </el-breadcrumb>
  </div>
</template>

<style>
</style>

<script>
export default {
  name: 'DataAnalysis'
}
</script>
