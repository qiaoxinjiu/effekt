<template>
  <div class="page-wrap">
    <page-section :title="isEditMode ? '编辑计划' : '计划构建'">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="200px" size="small">
        <el-form-item label="产品名称" prop="productId">
          <el-select
            v-model="form.productId"
            filterable
            clearable
            placeholder="请选择产品"
            style="width: 360px;"
            @change="handleProductChange"
            @focus="loadProductOptions">
            <el-option
              v-for="item in productOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目名称" prop="projectId">
          <el-select
            v-model="form.projectId"
            filterable
            clearable
            placeholder="请选择项目"
            style="width: 360px;"
            :disabled="!form.productId"
            @change="handleProjectChange">
            <el-option
              v-for="item in projectOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="计划名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="版本" prop="version">
          <el-input v-model="form.version"></el-input>
        </el-form-item>
        <el-form-item label="负责人" prop="owner_id">
          <el-select
            v-model="form.owner_id"
            filterable
            clearable
            placeholder="请选择负责人"
            style="width: 360px;"
            :disabled="!form.projectId">
            <el-option
              v-for="item in ownerOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="环境名称" prop="environment_id">
          <el-select
            v-model="form.environment_id"
            filterable
            clearable
            placeholder="请选择环境"
            style="width: 360px;"
            :disabled="!form.projectId">
            <el-option
              v-for="item in environmentOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否自动化测试计划" prop="isAuto">
          <el-select v-model.number="form.isAuto" placeholder="请选择" style="width: 200px;">
            <el-option :value="0" label="否" />
            <el-option :value="1" label="是" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker
            v-model="form.start_time"
            type="datetime"
            value-format="yyyy-MM-dd HH:mm:ss"
            format="yyyy-MM-dd HH:mm:ss"
            placeholder="请选择开始时间"
            style="width: 360px;">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker
            v-model="form.end_time"
            type="datetime"
            value-format="yyyy-MM-dd HH:mm:ss"
            format="yyyy-MM-dd HH:mm:ss"
            placeholder="请选择结束时间"
            style="width: 360px;">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="4"></el-input>
        </el-form-item>
        <el-form-item label="自动化执行 Jenkins URL">
          <el-input
            v-model.trim="form.jenkins_url"
            maxlength="512"
            show-word-limit
            placeholder="选填，自动化触发时使用的 Jenkins 地址"
            style="width: 480px;" />
        </el-form-item>
        <el-form-item>
          <el-button @click="goBack">返回</el-button>
          <el-button type="primary" :loading="saving" @click="submitForm">保存计划</el-button>
        </el-form-item>
      </el-form>
    </page-section>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { createPlan, getPlanDetail, updatePlan } from '@/api/planApi'
import { getProductList } from '@/api/productApi'
import { getProjectDetail, getProjectEnvironments, getProjectList, getProjectMembers } from '@/api/projectApi'

export default {
  name: 'PlanBuilder',
  components: {PageSection},
  data() {
    return {
      saving: false,
      planId: this.$route.query.planId || '',
      productOptions: [],
      projectOptions: [],
      ownerOptions: [],
      environmentOptions: [],
      form: {
        productId: '',
        projectId: this.$route.query.projectId ? Number(this.$route.query.projectId) : '',
        name: '',
        version: '',
        owner_id: '',
        environment_id: '',
        start_time: '',
        end_time: '',
        description: '',
        jenkins_url: '',
        /** 是否自动化测试计划：0 否，1 是，提交字段名 isAuto */
        isAuto: 0
      },
      rules: {
        productId: [{ required: true, message: '请选择产品', trigger: 'change' }],
        projectId: [{ required: true, message: '请选择项目', trigger: 'change' }],
        name: [{ required: true, message: '请输入计划名称', trigger: 'blur' }],
        version: [{ required: true, message: '请输入版本', trigger: 'blur' }],
        owner_id: [{ required: true, message: '请选择负责人', trigger: 'change' }],
        environment_id: [{ required: true, message: '请选择环境', trigger: 'change' }],
        start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
        end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }]
      }
    }
  },
  computed: {
    isEditMode() {
      return !!this.planId
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
    loadProjectOptionsByProduct(productId) {
      if (!productId) {
        this.projectOptions = []
        return Promise.resolve()
      }
      return getProjectList({ pageNo: 1, pageSize: 1000, status: 1, productId }).then(res => {
        const data = res && res.data ? res.data : res || {}
        this.projectOptions = data.items || data.list || data.data || []
      }).catch(() => {
        this.projectOptions = []
      })
    },
    loadProjectMeta(projectId) {
      if (!projectId) {
        this.ownerOptions = []
        this.environmentOptions = []
        return Promise.resolve()
      }
      const memberReq = getProjectMembers(projectId, { pageNo: 1, pageSize: 1000 }).then(res => {
        const data = (res && res.data) || res || {}
        const list = data.items || data.list || data.data || data || []
        this.ownerOptions = (Array.isArray(list) ? list : []).map(item => ({
          id: item.user_id || item.userId || item.id,
          name:
            item.real_name ||
            item.realName ||
            item.username ||
            item.name ||
            item.user_name ||
            `用户${item.user_id || item.id}`
        })).filter(item => item.id !== undefined && item.id !== null && item.id !== '')
      }).catch(() => {
        this.ownerOptions = []
      })
      const envReq = getProjectEnvironments(projectId, { pageNo: 1, pageSize: 1000 }).then(res => {
        const data = (res && res.data) || res || {}
        const list = data.items || data.list || data.data || data || []
        this.environmentOptions = (Array.isArray(list) ? list : []).map(item => ({
          id: item.id,
          name: item.name
        }))
      }).catch(() => {
        this.environmentOptions = []
      })
      return Promise.all([memberReq, envReq])
    },
    handleProductChange() {
      this.form.projectId = ''
      this.form.owner_id = ''
      this.form.environment_id = ''
      this.projectOptions = []
      this.ownerOptions = []
      this.environmentOptions = []
      this.loadProjectOptionsByProduct(this.form.productId)
    },
    handleProjectChange() {
      this.form.owner_id = ''
      this.form.environment_id = ''
      this.ownerOptions = []
      this.environmentOptions = []
      this.loadProjectMeta(this.form.projectId)
    },
    goBack() {
      this.$router.push({
        path: '/test-platform/plan',
        query: {
          productId: this.form.productId || undefined,
          projectId: this.form.projectId || undefined
        }
      })
    },
    submitForm() {
      this.$refs.formRef.validate(valid => {
        if (!valid) {
          return
        }
        const projectId = this.form.projectId
        const payload = {
          name: this.form.name,
          version: this.form.version,
          owner_id: this.form.owner_id,
          environment_id: this.form.environment_id,
          start_time: this.form.start_time,
          end_time: this.form.end_time,
          description: this.form.description
        }
        payload.jenkins_url = (this.form.jenkins_url || '').trim()
        payload.isAuto = this.form.isAuto === 1 ? 1 : 0
        this.saving = true
        const request = this.isEditMode
          ? updatePlan(projectId, this.planId, payload)
          : createPlan(projectId, payload)
        request.then(() => {
          this.$message({ type: 'success', message: this.isEditMode ? '计划更新成功' : '计划创建成功' })
          this.$router.push({
            path: '/test-platform/plan',
            query: {
              productId: this.form.productId || undefined,
              projectId: projectId || undefined
            }
          })
        }).finally(() => {
          this.saving = false
        })
      })
    },
    /** 与 PlanList 列表行一致，兼容详情接口多种时间字段名 */
    pickPlanDetailStartRaw(plan) {
      if (!plan) return ''
      return (
        plan.start_date ||
        plan.startDate ||
        plan.start_time ||
        plan.startTime ||
        plan.begin_time ||
        plan.beginTime ||
        plan.planned_start_time ||
        plan.plannedStartTime ||
        ''
      )
    },
    pickPlanDetailEndRaw(plan) {
      if (!plan) return ''
      return (
        plan.end_date ||
        plan.endDate ||
        plan.end_time ||
        plan.endTime ||
        plan.finish_time ||
        plan.finishTime ||
        plan.planned_end_time ||
        plan.plannedEndTime ||
        ''
      )
    },
    /** 将接口返回的时间戳 / ISO 串等转为 date-picker 的 value-format 字符串 */
    toDatePickerValue(value) {
      if (value === undefined || value === null || value === '') return ''
      if (typeof value === 'number' || (typeof value === 'string' && /^\d+$/.test(value.trim()))) {
        const raw = Number(value)
        if (Number.isNaN(raw) || raw <= 0) return ''
        const ms = raw < 1000000000000 ? raw * 1000 : raw
        const d = new Date(ms)
        if (Number.isNaN(d.getTime())) return ''
        const pad = n => String(n).padStart(2, '0')
        return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
      }
      const s = String(value).trim()
      if (!s) return ''
      let normalized = s
      if (s.includes('T')) {
        normalized = s.replace('T', ' ').replace(/\.\d+/, '').replace(/Z$/i, '').trim()
      }
      if (normalized.length >= 19) {
        return normalized.slice(0, 19)
      }
      if (/^\d{4}-\d{2}-\d{2}$/.test(normalized)) {
        return `${normalized} 00:00:00`
      }
      const parsed = new Date(s)
      if (!Number.isNaN(parsed.getTime())) {
        const pad = n => String(n).padStart(2, '0')
        return `${parsed.getFullYear()}-${pad(parsed.getMonth() + 1)}-${pad(parsed.getDate())} ${pad(parsed.getHours())}:${pad(parsed.getMinutes())}:${pad(parsed.getSeconds())}`
      }
      return normalized
    },
    unwrapPlanDetailPayload(res) {
      const raw = (res && res.data) || res || {}
      const inner = raw.plan || raw.detail
      if (inner && typeof inner === 'object') {
        return Object.assign({}, raw, inner)
      }
      return raw
    },
    loadPlanDetail() {
      if (!this.isEditMode || !this.form.projectId) {
        return Promise.resolve()
      }
      return getPlanDetail(this.form.projectId, this.planId).then(res => {
        const data = this.unwrapPlanDetailPayload(res)
        this.form.name = data.name || ''
        this.form.version = data.version || ''
        this.form.owner_id = data.owner_id || data.ownerId || ''
        this.form.environment_id = data.environment_id || data.environmentId || ''
        this.form.start_time = this.toDatePickerValue(this.pickPlanDetailStartRaw(data))
        this.form.end_time = this.toDatePickerValue(this.pickPlanDetailEndRaw(data))
        this.form.description = data.description || ''
        this.form.jenkins_url = data.jenkins_url || data.jenkinsUrl || ''
        const autoRaw = data.isAuto !== undefined && data.isAuto !== null ? data.isAuto : data.is_auto
        this.form.isAuto =
          autoRaw === true || autoRaw === 1 || autoRaw === '1' ? 1 : 0
      }).catch(() => {})
    },
    initByRouteProject() {
      if (!this.form.projectId) {
        return Promise.resolve()
      }
      return getProjectDetail(this.form.projectId).then(res => {
        const data = res && res.data ? res.data : res || {}
        const productId = data.productId || data.product_id || ''
        if (productId) {
          this.form.productId = productId
          return this.loadProjectOptionsByProduct(productId)
        }
      }).catch(() => {})
    }
  },
  created() {
    this.loadProductOptions().then(() => this.initByRouteProject()).finally(() => {
      if (this.form.projectId) {
        this.loadProjectMeta(this.form.projectId).then(() => {
          this.loadPlanDetail()
        })
      }
    })
  }
}
</script>

<style scoped>
.page-wrap {
  padding: 20px;
}
</style>
