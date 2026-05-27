<template>
  <div class="page-wrap">
    <page-section title="造数器编辑">
      <el-form :model="form" label-width="120px" size="small">
        <el-form-item label="项目ID">
          <el-input v-model="projectId" style="width: 200px;"></el-input>
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.builder_type">
            <el-option label="流程编排" :value="1"></el-option>
            <el-option label="SQL" :value="2"></el-option>
            <el-option label="脚本" :value="3"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3"></el-input>
        </el-form-item>
        <el-form-item label="定义(JSON)">
          <el-input v-model="definitionText" type="textarea" :rows="14"></el-input>
        </el-form-item>
        <el-form-item label="输入Schema(JSON)">
          <el-input v-model="inputSchemaText" type="textarea" :rows="8"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="submitForm">保存</el-button>
        </el-form-item>
      </el-form>
    </page-section>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { createBuilder } from '@/api/dataFactoryApi'

export default {
  name: 'BuilderEditor',
  components: { PageSection },
  data() {
    return {
      saving: false,
      projectId: this.$route.query.projectId || 1,
      definitionText: '{\n  "steps": [],\n  "output": {}\n}',
      inputSchemaText: '{\n  "type": "object",\n  "properties": {}\n}',
      form: {
        name: '',
        builder_type: 1,
        description: ''
      }
    }
  },
  methods: {
    submitForm() {
      let definition = {}
      let input_schema = {}
      try {
        definition = JSON.parse(this.definitionText || '{}')
        input_schema = JSON.parse(this.inputSchemaText || '{}')
      } catch (e) {
        this.$message({ type: 'error', message: 'JSON 格式错误' })
        return
      }
      this.saving = true
      createBuilder(this.projectId, Object.assign({}, this.form, { definition, input_schema })).then(() => {
        this.$message({ type: 'success', message: '造数器保存成功' })
        this.$router.push({ path: '/data-tools/factory/builders', query: { projectId: this.projectId } })
      }).finally(() => {
        this.saving = false
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
