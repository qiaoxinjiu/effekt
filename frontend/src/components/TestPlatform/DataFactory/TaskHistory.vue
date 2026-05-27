<template>
  <div class="page-wrap">
    <page-section title="造数任务历史">
      <el-form :inline="true" size="small">
        <el-form-item label="项目ID">
          <el-input v-model="projectId" style="width: 120px;"></el-input>
        </el-form-item>
        <el-form-item label="任务ID">
          <el-input v-model="taskId" style="width: 160px;"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchStatus">查询状态</el-button>
        </el-form-item>
      </el-form>
      <json-viewer :value="taskResult"></json-viewer>
    </page-section>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import JsonViewer from '@/components/TestPlatform/common/JsonViewer'
import { getDataTaskStatus } from '@/api/dataFactoryApi'

export default {
  name: 'TaskHistory',
  components: { PageSection, JsonViewer },
  data() {
    return {
      projectId: this.$route.query.projectId || 1,
      taskId: this.$route.query.taskId || '',
      taskResult: {}
    }
  },
  methods: {
    fetchStatus() {
      if (!this.taskId) {
        this.$message({ type: 'warning', message: '请输入任务ID' })
        return
      }
      getDataTaskStatus(this.projectId, this.taskId).then(res => {
        this.taskResult = (res && res.data) || res || {}
      }).catch(() => {
        this.taskResult = {}
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
