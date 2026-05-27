<template>
  <div class="page-wrap">
    <page-section :title="form.id ? '编辑用例' : '新建用例'">
      <el-form ref="form" :model="form" :rules="rules" label-width="120px" size="small">
        <el-form-item label="产品" prop="productId">
          <el-select
            v-model="form.productId"
            filterable
            clearable
            placeholder="请选择产品"
            style="width: 360px;"
            @change="handleProductChange"
            @focus="loadProductOptions">
            <el-option v-for="item in productOptions" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="项目" prop="projectId">
          <el-select
            v-model="form.projectId"
            filterable
            clearable
            placeholder="请选择项目"
            style="width: 360px;"
            :disabled="!form.productId"
            @change="handleProjectChange">
            <el-option v-for="item in projectOptions" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="模块" prop="moduleId">
          <el-select
            v-model="form.moduleId"
            filterable
            clearable
            placeholder="请选择模块"
            style="width: 360px;"
            :disabled="!form.projectId"
            @focus="loadModuleOptions">
            <el-option v-for="item in moduleOptions" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item v-if="form.id" label="用例编号">
          <el-input v-model="form.caseKey" placeholder="不填则由后端自动生成"></el-input>
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
        <el-form-item label="前置条件">
          <el-input v-model="form.preconditions" type="textarea" :rows="3"></el-input>
        </el-form-item>
        <el-form-item label="步骤">
          <el-input v-model="stepsText" type="textarea" :rows="10"></el-input>
        </el-form-item>
        <el-form-item label="预期结果">
          <el-input v-model="expectedResultText" type="textarea" :rows="3" placeholder="请输入预期结果"></el-input>
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="form.priority">
            <el-option label="P0" :value="0"></el-option>
            <el-option label="P1" :value="1"></el-option>
            <el-option label="P2" :value="2"></el-option>
            <el-option label="P3" :value="3"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.caseType">
            <el-option label="功能" :value="1"></el-option>
            <el-option label="性能" :value="2"></el-option>
            <el-option label="安全" :value="3"></el-option>
            <el-option label="接口" :value="4"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status">
            <el-option label="正常" :value="1"></el-option>
            <el-option label="已废弃" :value="2"></el-option>
            <el-option label="评审中" :value="3"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="是否自动化">
          <el-select v-model="form.isAuto">
            <el-option label="未实现" :value="0"></el-option>
            <el-option label="已实现" :value="1"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="tagsText" placeholder="多个标签用逗号分隔"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="submitForm">保存</el-button>
          <el-button @click="backList">返回</el-button>
        </el-form-item>
      </el-form>
    </page-section>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { createCase, getCaseDetail, getModuleTree, updateCase } from '@/api/caseApi'
import { getProductList } from '@/api/productApi'
import { getProjectDetail, getProjectList } from '@/api/projectApi'

export default {
  name: 'CaseEditor',
  components: { PageSection },
  data() {
    return {
      saving: false,
      productOptions: [],
      projectOptions: [],
      moduleOptions: [],
      form: {
        productId: this.$route.query.productId ? Number(this.$route.query.productId) : '',
        projectId: this.$route.query.projectId ? Number(this.$route.query.projectId) : '',
        id: '',
        moduleId: '',
        caseKey: '',
        title: '',
        preconditions: '',
        steps: [],
        priority: 2,
        caseType: 1,
        tags: [],
        status: 1,
        isAuto: 0
      },
      stepsText: '',
      expectedResultText: '',
      tagsText: '',
      rules: {
        productId: [{ required: true, message: '请选择产品', trigger: 'change' }],
        projectId: [{ required: true, message: '请选择项目', trigger: 'change' }],
        moduleId: [{ required: true, message: '请选择模块', trigger: 'change' }],
        title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
        // 步骤为文本输入，不做 JSON 校验；是否为空在 submitForm 里校验
      }
    }
  },
  methods: {
    loadProductOptions() {
      if (this.productOptions && this.productOptions.length > 0) {
        return Promise.resolve()
      }
      return getProductList({ pageNo: 1, pageSize: 1000, status: 1 }).then(res => {
        const data = res && res.data ? res.data : res || {}
        this.productOptions = data.items || data.list || data.data || []
      }).catch(() => {
        this.productOptions = []
      })
    },
    loadProjectOptions() {
      if (!this.form.productId) {
        this.projectOptions = []
        return Promise.resolve()
      }
      return getProjectList({ pageNo: 1, pageSize: 1000, status: 1, productId: this.form.productId }).then(res => {
        const data = res && res.data ? res.data : res || {}
        this.projectOptions = data.items || data.list || data.data || []
      }).catch(() => {
        this.projectOptions = []
      })
    },
    loadModuleOptions() {
      if (!this.form.projectId) {
        this.moduleOptions = []
        return Promise.resolve()
      }
      return getModuleTree({ projectId: this.form.projectId }).then(res => {
        const data = (res && res.data) || res || {}
        const list = data.list || data.items || []
        this.moduleOptions = Array.isArray(list) ? list : []
      }).catch(() => {
        this.moduleOptions = []
      })
    },
    handleProductChange() {
      this.form.projectId = ''
      this.form.moduleId = ''
      this.projectOptions = []
      this.moduleOptions = []
      this.loadProjectOptions()
    },
    handleProjectChange() {
      this.form.moduleId = ''
      this.moduleOptions = []
      this.loadModuleOptions()
    },
    fetchDetail() {
      const caseId = this.$route.query.caseId
      if (!caseId) {
        return
      }
      getCaseDetail(this.form.projectId, caseId).then(res => {
        const data = (res && res.data) || res || {}
        this.form = Object.assign({}, this.form, {
          id: data.id || caseId,
          moduleId: data.moduleId || data.module_id || '',
          caseKey: data.caseKey || data.case_key || '',
          title: data.title || '',
          preconditions: data.preconditions || '',
          steps: data.steps || [],
          priority: data.priority !== undefined ? data.priority : 2,
          caseType: data.caseType || data.case_type || 1,
          tags: data.tags || [],
          status: data.status || 1,
          isAuto: data.isAuto !== undefined ? data.isAuto : (data.is_auto !== undefined ? data.is_auto : 0)
        })
        this.stepsText = this.formatStepsToText(this.form.steps || [])
        this.expectedResultText = data.expectedResults || data.expected_results || this.extractExpectedResultFromSteps(this.form.steps || [])
        this.tagsText = Array.isArray(this.form.tags) ? this.form.tags.join(',') : (this.form.tags || '')
        if (this.form.projectId) {
          this.loadModuleOptions()
        }
      })
    },
    submitForm() {
      const expectedResult = (this.expectedResultText || '').trim()
      const stepsText = String(this.stepsText || '').trim()

      if (!stepsText) {
        this.$message({ type: 'error', message: '请输入步骤' })
        return
      }
      const tags = this.tagsText ? this.tagsText.split(',').map(item => item.trim()).filter(Boolean) : []
      const payload = this.cleanParams({
        projectId: this.form.projectId,
        moduleId: this.form.moduleId,
        caseKey: this.form.caseKey,
        title: this.form.title,
        preconditions: this.form.preconditions,
        steps: stepsText,
        expectedResults: expectedResult,
        priority: this.form.priority,
        caseType: this.form.caseType,
        tags,
        status: this.form.status,
        isAuto: this.form.isAuto
      })
      this.saving = true
      const caseId = this.form.id || this.$route.query.caseId
      const request = caseId ? updateCase(this.form.projectId, caseId, payload) : createCase(this.form.projectId, payload)
      request.then(() => {
        this.$message({ type: 'success', message: '保存成功' })
        this.backList()
      }).finally(() => {
        this.saving = false
      })
    },
    cleanParams(params) {
      return Object.keys(params).reduce((result, key) => {
        if (params[key] !== '' && params[key] !== undefined && params[key] !== null) {
          result[key] = params[key]
        }
        return result
      }, {})
    },
    formatStepsToText(steps) {
      if (typeof steps === 'string') return steps
      if (!Array.isArray(steps)) return ''
      return steps
        .map(item => {
          if (item === null || item === undefined) return ''
          if (typeof item === 'string') return item
          return item.action || item.step || item.description || item.text || item.content || ''
        })
        .filter(Boolean)
        .join('\n')
    },
    extractExpectedResultFromSteps(steps) {
      if (!Array.isArray(steps) || steps.length === 0) return ''
      const first = steps[0]
      if (first && typeof first === 'object') {
        return first.expected || first.expected_result || first.expectedResult || ''
      }
      return ''
    },
    backList() {
      this.$router.push({
        path: '/test-platform/case',
        query: {
          productId: this.form.productId || undefined,
          projectId: this.form.projectId || undefined,
          tab: 'cases'
        }
      })
    }
  },
  created() {
    this.loadProductOptions().then(() => {
      if (this.form.projectId && !this.form.productId) {
        return getProjectDetail(this.form.projectId).then(res => {
          const data = res && res.data ? res.data : res || {}
          const pid = data.productId || data.product_id || ''
          if (pid) {
            this.form.productId = pid
          }
        }).catch(() => {})
      }
    }).then(() => {
      return this.loadProjectOptions()
    }).then(() => {
      if (this.form.projectId) {
        return this.loadModuleOptions()
      }
    }).finally(() => {
      this.fetchDetail()
    })
  }
}
</script>

<style scoped>
.page-wrap {
  padding: 20px;
}
</style>
