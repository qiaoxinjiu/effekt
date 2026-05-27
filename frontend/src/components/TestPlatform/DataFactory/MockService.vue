<template>
  <div class="page-wrap">
    <page-section title="Mock 服务">
      <el-form :model="form" label-width="120px" size="small">
        <el-form-item label="项目ID">
          <el-input v-model="projectId" style="width: 200px;"></el-input>
        </el-form-item>
        <el-form-item label="Path">
          <el-input v-model="form.path"></el-input>
        </el-form-item>
        <el-form-item label="Method">
          <el-select v-model="form.method">
            <el-option label="GET" value="GET"></el-option>
            <el-option label="POST" value="POST"></el-option>
            <el-option label="PUT" value="PUT"></el-option>
            <el-option label="DELETE" value="DELETE"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态码">
          <el-input v-model="form.status_code"></el-input>
        </el-form-item>
        <el-form-item label="延迟(ms)">
          <el-input v-model="form.delay_ms"></el-input>
        </el-form-item>
        <el-form-item label="响应体(JSON)">
          <el-input v-model="responseBodyText" type="textarea" :rows="10"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="submitForm">创建 Mock</el-button>
        </el-form-item>
      </el-form>
      <el-alert v-if="mockUrl" :title="'Mock 地址：' + mockUrl" type="success" :closable="false"></el-alert>
    </page-section>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'

export default {
  name: 'MockService',
  components: { PageSection },
  data() {
    return {
      saving: false,
      mockUrl: '',
      projectId: this.$route.query.projectId || 1,
      responseBodyText: '{\n  "code": 0,\n  "message": "success"\n}',
      form: {
        path: '',
        method: 'POST',
        status_code: 200,
        delay_ms: 0
      }
    }
  },
  methods: {
    submitForm() {
      this.$message({
        type: 'warning',
        message: '当前后端未提供 Mock 服务接口，页面暂为占位状态'
      })
    }
  }
}
</script>

<style scoped>
.page-wrap {
  padding: 20px;
}
</style>
