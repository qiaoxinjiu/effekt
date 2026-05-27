<template>
  <div class="page-wrap">
    <page-section title="用例评审">
      <el-form :model="form" label-width="120px" size="small">
        <el-form-item label="项目ID">
          <el-input v-model="projectId" style="width: 200px;"></el-input>
        </el-form-item>
        <el-form-item label="用例ID">
          <el-input v-model="caseId" disabled style="width: 200px;"></el-input>
        </el-form-item>
        <el-form-item label="评审人ID">
          <el-input v-model="reviewersText" placeholder="多个 ID 用逗号分隔"></el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.comments" type="textarea" :rows="4"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="submitReview">提交评审</el-button>
        </el-form-item>
      </el-form>
    </page-section>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { submitCaseReview } from '@/api/caseApi'

export default {
  name: 'CaseReview',
  components: { PageSection },
  data() {
    return {
      projectId: this.$route.query.projectId || 1,
      caseId: this.$route.query.caseId || '',
      reviewersText: '',
      submitting: false,
      form: {
        comments: ''
      }
    }
  },
  methods: {
    submitReview() {
      const reviewer_ids = this.reviewersText.split(',').map(item => item.trim()).filter(Boolean)
      this.submitting = true
      submitCaseReview(this.projectId, this.caseId, {
        reviewer_ids,
        comments: this.form.comments
      }).then(() => {
        this.$message({ type: 'success', message: '评审提交成功' })
      }).finally(() => {
        this.submitting = false
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
