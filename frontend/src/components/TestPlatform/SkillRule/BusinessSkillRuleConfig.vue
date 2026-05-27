<template>
  <div class="page-wrap">
    <page-section title="业务技能配置">
      <el-form :inline="true" size="small" class="filter-bar" @submit.native.prevent>
        <el-form-item label="产品">
          <el-select
            v-model="selectedProductId"
            filterable
            clearable
            placeholder="请选择产品"
            style="width: 200px;"
            @change="handleProductChange"
            @focus="loadProductOptions">
            <el-option v-for="p in productOptions" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目">
          <el-select
            v-model="selectedProjectId"
            filterable
            clearable
            placeholder="请选择项目"
            style="width: 220px;"
            :disabled="!selectedProductId"
            @change="handleProjectChange">
            <el-option v-for="p in projectOptions" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
      </el-form>

      <el-tabs v-model="configActiveTab" class="skill-rule-tabs" style="margin-top: 8px;" @tab-click="onConfigTabClick">
        <el-tab-pane label="Skills 配置" name="skills">
          <el-form :inline="true" size="small" class="toolbar-form" @submit.native.prevent>
            <el-form-item label="模块">
              <el-select v-model="skillQuery.moduleId" clearable filterable placeholder="全部" style="width: 180px;" :disabled="!projectId">
                <el-option v-for="m in flatModuleOptions" :key="m.id" :label="m.name" :value="m.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="关键字">
              <el-input v-model="skillQuery.keyword" clearable style="width: 160px;" @keyup.enter.native="fetchSkillList" />
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="skillQuery.status" clearable placeholder="全部" style="width: 100px;">
                <el-option v-for="o in statusOptions" :key="'s-' + o.value" :label="o.label" :value="o.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="类型">
              <el-select v-model="skillQuery.skillType" clearable placeholder="全部" style="width: 130px;">
                <el-option v-for="o in skillTypeOptions" :key="'t-' + o.value" :label="o.label" :value="o.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="风险">
              <el-select v-model="skillQuery.riskLevel" clearable placeholder="全部" style="width: 100px;">
                <el-option v-for="o in riskLevelOptions" :key="'r-' + o.value" :label="o.label" :value="o.value" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :disabled="!projectId" @click="skillPageNo = 1; fetchSkillList()">查询</el-button>
            </el-form-item>
            <el-form-item>
              <el-button size="small" @click="resetSkillQuery">重置</el-button>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="small" plain :disabled="!projectId" @click="openSkillCreate">新建 Skill</el-button>
            </el-form-item>
          </el-form>
          <el-table v-loading="skillLoading" :data="skillList" border size="small" style="margin-top: 8px;">
            <el-table-column prop="id" label="ID" width="72" />
            <el-table-column prop="name" label="名称" min-width="140" show-overflow-tooltip />
            <el-table-column prop="code" label="编码" min-width="120" show-overflow-tooltip />
            <el-table-column label="类型" width="100">
              <template slot-scope="scope">{{ formatSkillType(scope.row.skill_type) }}</template>
            </el-table-column>
            <el-table-column label="风险" width="88">
              <template slot-scope="scope">{{ formatRiskLevel(scope.row.risk_level) }}</template>
            </el-table-column>
            <el-table-column label="状态" width="88">
              <template slot-scope="scope">{{ formatConfigStatus(scope.row.status) }}</template>
            </el-table-column>
            <el-table-column label="标签" min-width="120" show-overflow-tooltip>
              <template slot-scope="scope">{{ formatTagsCol(scope.row.tags) }}</template>
            </el-table-column>
            <el-table-column prop="updated_time" label="更新时间" min-width="150" show-overflow-tooltip />
            <el-table-column label="操作" width="140" fixed="right">
              <template slot-scope="scope">
                <el-button type="text" @click="openSkillEdit(scope.row)">编辑</el-button>
                <el-button type="text" style="color: #F56C6C;" @click="removeSkill(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="pager-wrap">
            <el-pagination
              :current-page="skillPageNo"
              :page-size="skillPageSize"
              :page-sizes="[10, 20, 50]"
              :total="skillTotal"
              layout="total, sizes, prev, pager, next"
              @size-change="onSkillSize"
              @current-change="onSkillPage" />
          </div>
        </el-tab-pane>

        <el-tab-pane label="业务规则配置" name="rules">
          <el-form :inline="true" size="small" class="toolbar-form" @submit.native.prevent>
            <el-form-item label="模块">
              <el-select v-model="ruleQuery.moduleId" clearable filterable placeholder="全部" style="width: 180px;" :disabled="!projectId">
                <el-option v-for="m in flatModuleOptions" :key="'r-' + m.id" :label="m.name" :value="m.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="关键字">
              <el-input v-model="ruleQuery.keyword" clearable style="width: 160px;" @keyup.enter.native="fetchRuleList" />
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="ruleQuery.status" clearable placeholder="全部" style="width: 100px;">
                <el-option v-for="o in statusOptions" :key="'rs-' + o.value" :label="o.label" :value="o.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="优先级">
              <el-select v-model="ruleQuery.priority" clearable placeholder="全部" style="width: 100px;">
                <el-option v-for="o in priorityOptions" :key="'p-' + o.value" :label="o.label" :value="o.value" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :disabled="!projectId" @click="rulePageNo = 1; fetchRuleList()">查询</el-button>
            </el-form-item>
            <el-form-item>
              <el-button size="small" @click="resetRuleQuery">重置</el-button>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="small" plain :disabled="!projectId" @click="openRuleCreate">新建规则</el-button>
            </el-form-item>
          </el-form>
          <el-table v-loading="ruleLoading" :data="ruleList" border size="small" style="margin-top: 8px;">
            <el-table-column prop="id" label="ID" width="72" />
            <el-table-column prop="name" label="名称" min-width="140" show-overflow-tooltip />
            <el-table-column prop="rule_code" label="规则编码" min-width="120" show-overflow-tooltip />
            <el-table-column label="优先级" width="100">
              <template slot-scope="scope">{{ formatPriority(scope.row.priority) }}</template>
            </el-table-column>
            <el-table-column label="状态" width="88">
              <template slot-scope="scope">{{ formatConfigStatus(scope.row.status) }}</template>
            </el-table-column>
            <el-table-column label="标签" min-width="120" show-overflow-tooltip>
              <template slot-scope="scope">{{ formatTagsCol(scope.row.tags) }}</template>
            </el-table-column>
            <el-table-column prop="updated_time" label="更新时间" min-width="150" show-overflow-tooltip />
            <el-table-column label="操作" width="140" fixed="right">
              <template slot-scope="scope">
                <el-button type="text" @click="openRuleEdit(scope.row)">编辑</el-button>
                <el-button type="text" style="color: #F56C6C;" @click="removeRule(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="pager-wrap">
            <el-pagination
              :current-page="rulePageNo"
              :page-size="rulePageSize"
              :page-sizes="[10, 20, 50]"
              :total="ruleTotal"
              layout="total, sizes, prev, pager, next"
              @size-change="onRuleSize"
              @current-change="onRulePage" />
          </div>
        </el-tab-pane>
      </el-tabs>
    </page-section>

    <el-dialog :title="skillDialogMode === 'create' ? '新建 Skill' : '编辑 Skill'" :visible.sync="skillDialogVisible" width="720px" @close="resetSkillForm">
      <el-form ref="skillFormRef" :model="skillForm" :rules="skillFormActiveRules" label-width="120px" size="small">
        <el-form-item label="模块" prop="moduleId">
          <el-select v-model="skillForm.moduleId" clearable filterable placeholder="可选" style="width: 100%;" :disabled="!projectId">
            <el-option v-for="m in flatModuleOptions" :key="'sf-' + m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="skillForm.name" />
        </el-form-item>
        <template v-if="skillDialogMode === 'edit'">
          <el-form-item label="编码">
            <el-input v-model="skillForm.code" disabled placeholder="创建后不可修改" />
          </el-form-item>
          <el-form-item label="触发条件" prop="triggerCondition">
            <el-input v-model="skillForm.triggerCondition" type="textarea" :rows="2" />
          </el-form-item>
          <el-form-item label="推理路径">
            <el-input v-model="skillForm.reasoningPath" type="textarea" :rows="2" />
          </el-form-item>
          <el-form-item label="输出规范">
            <el-input v-model="skillForm.outputSpec" type="textarea" :rows="2" />
          </el-form-item>
        </template>
        <el-form-item label="描述">
          <el-input v-model="skillForm.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="skillForm.skillType" style="width: 100%;">
            <el-option v-for="o in skillTypeOptions" :key="'sfo-' + o.value" :label="o.label" :value="o.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="风险等级">
          <el-select v-model="skillForm.riskLevel" style="width: 100%;">
            <el-option v-for="o in riskLevelOptions" :key="'sfr-' + o.value" :label="o.label" :value="o.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="skillForm.status" style="width: 100%;">
            <el-option v-for="o in statusOptions" :key="'sfs-' + o.value" :label="o.label" :value="o.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="skillForm.tags" multiple filterable allow-create default-first-option placeholder="输入后回车可新增" style="width: 100%;" />
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button size="small" @click="skillDialogVisible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="skillSubmitting" @click="submitSkill">保存</el-button>
      </span>
    </el-dialog>

    <el-dialog :title="ruleDialogMode === 'create' ? '新建业务规则' : '编辑业务规则'" :visible.sync="ruleDialogVisible" width="720px" @close="resetRuleForm">
      <el-form ref="ruleFormRef" :model="ruleForm" :rules="ruleRules" label-width="120px" size="small">
        <el-form-item label="模块" prop="moduleId">
          <el-select v-model="ruleForm.moduleId" clearable filterable placeholder="可选" style="width: 100%;" :disabled="!projectId">
            <el-option v-for="m in flatModuleOptions" :key="'rf-' + m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="ruleForm.name" />
        </el-form-item>
        <el-form-item v-if="ruleDialogMode === 'edit'" label="规则编码">
          <el-input v-model="ruleForm.ruleCode" disabled placeholder="由系统分配" />
        </el-form-item>
        <el-form-item label="规则内容" prop="ruleContent">
          <el-input v-model="ruleForm.ruleContent" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="适用场景">
          <el-input v-model="ruleForm.applicableScene" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="示例">
          <el-input v-model="ruleForm.example" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="ruleForm.priority" style="width: 100%;">
            <el-option v-for="o in priorityOptions" :key="'rfo-' + o.value" :label="o.label" :value="o.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="ruleForm.status" style="width: 100%;">
            <el-option v-for="o in statusOptions" :key="'rfs-' + o.value" :label="o.label" :value="o.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="ruleForm.tags" multiple filterable allow-create default-first-option placeholder="输入后回车可新增" style="width: 100%;" />
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button size="small" @click="ruleDialogVisible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="ruleSubmitting" @click="submitRule">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { getModuleTree } from '@/api/caseApi'
import {
  createSkill,
  createBusinessRule,
  deleteSkill,
  deleteBusinessRule,
  getSkillDetail,
  getSkillList,
  getBusinessRuleDetail,
  getBusinessRuleList,
  updateSkill,
  updateBusinessRule
} from '@/api/skillRuleApi'
import { getProductList } from '@/api/productApi'
import { getProjectList } from '@/api/projectApi'
import {
  readLastProductProjectCache,
  saveLastProductProjectCache,
  pickIdFromOptions
} from '@/utils/lastProductProjectCache'

export default {
  name: 'BusinessSkillRuleConfig',
  components: { PageSection },
  data() {
    const routeTab = this.$route.query && this.$route.query.tab
    const initialTab =
      routeTab === 'rules' || routeTab === 'business-rules' ? 'rules' : 'skills'
    return {
      configActiveTab: initialTab,
      selectedProductId: '',
      selectedProjectId: '',
      productOptions: [],
      projectOptions: [],
      moduleTree: [],
      skillQuery: { moduleId: '', keyword: '', status: '', skillType: '', riskLevel: '' },
      skillPageNo: 1,
      skillPageSize: 20,
      skillList: [],
      skillTotal: 0,
      skillLoading: false,
      skillDialogVisible: false,
      skillDialogMode: 'create',
      skillSubmitting: false,
      skillForm: {},
      ruleQuery: { moduleId: '', keyword: '', status: '', priority: '' },
      rulePageNo: 1,
      rulePageSize: 20,
      ruleList: [],
      ruleTotal: 0,
      ruleLoading: false,
      ruleDialogVisible: false,
      ruleDialogMode: 'create',
      ruleSubmitting: false,
      ruleForm: {},
      ruleRules: {
        name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
        ruleContent: [{ required: true, message: '请输入规则内容', trigger: 'blur' }]
      },
      statusOptions: [
        { value: 1, label: '启用' },
        { value: 2, label: '停用' },
        { value: 3, label: '草稿' }
      ],
      skillTypeOptions: [
        { value: 1, label: '通用测试策略' },
        { value: 2, label: '历史缺陷模式' },
        { value: 3, label: '边界场景' },
        { value: 4, label: '接口测试' },
        { value: 5, label: 'UI 测试' },
        { value: 6, label: '性能测试' },
        { value: 7, label: '安全测试' },
        { value: 8, label: '数据一致性' },
        { value: 9, label: '并发/幂等' },
        { value: 99, label: '其他' }
      ],
      riskLevelOptions: [
        { value: 0, label: '高风险' },
        { value: 1, label: '中高风险' },
        { value: 2, label: '中风险' },
        { value: 3, label: '低风险' }
      ],
      priorityOptions: [
        { value: 0, label: '高优先级' },
        { value: 1, label: '中高优先级' },
        { value: 2, label: '中优先级' },
        { value: 3, label: '低优先级' }
      ]
    }
  },
  computed: {
    projectId() {
      return this.selectedProjectId || ''
    },
    flatModuleOptions() {
      const out = []
      const walk = (list, prefix) => {
        ;(list || []).forEach(item => {
          const name = prefix ? `${prefix} / ${item.name}` : item.name
          out.push({ id: item.id, name })
          const ch = item.children || item.child_list || item.childList || []
          if (Array.isArray(ch) && ch.length) walk(ch, name)
        })
      }
      walk(this.moduleTree, '')
      return out
    },
    skillFormActiveRules() {
      if (this.skillDialogMode === 'create') {
        return {
          name: [{ required: true, message: '请输入名称', trigger: 'blur' }]
        }
      }
      return {
        name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
        triggerCondition: [{ required: true, message: '请输入触发条件', trigger: 'blur' }]
      }
    }
  },
  watch: {
    '$route.query.tab'(val) {
      const next = val === 'rules' || val === 'business-rules' ? 'rules' : 'skills'
      if (this.configActiveTab !== next) {
        this.configActiveTab = next
      }
      if (!this.projectId) return
      if (next === 'rules') this.fetchRuleList()
      else this.fetchSkillList()
    }
  },
  created() {
    this.resetSkillFormModel()
    this.resetRuleFormModel()
    this.bootstrap()
  },
  methods: {
    cleanParams(obj) {
      const r = {}
      Object.keys(obj || {}).forEach(k => {
        const v = obj[k]
        if (v !== '' && v !== undefined && v !== null) r[k] = v
      })
      return r
    },
    /** 新建 Skill 时后端要求 code 唯一，由前端自动生成 */
    generateAutoSkillCode() {
      const t = Date.now()
      const r = Math.random().toString(36).slice(2, 10).toUpperCase()
      return `SKILL_AUTO_${t}_${r}`
    },
    onConfigTabClick(tab) {
      const name = tab && tab.name
      const q = Object.assign({}, this.$route.query || {})
      if (name === 'rules') {
        q.tab = 'rules'
      } else {
        delete q.tab
      }
      const prev = JSON.stringify(this.$route.query || {})
      const next = JSON.stringify(q)
      if (prev !== next) {
        this.$router.replace({ path: this.$route.path, query: q }).catch(() => {})
      }
    },
    formatTagsCol(tags) {
      if (Array.isArray(tags)) return tags.join('、')
      return tags || '—'
    },
    formatSkillType(v) {
      const o = this.skillTypeOptions.find(x => x.value === v)
      return o ? o.label : (v === undefined || v === null ? '—' : v)
    },
    formatRiskLevel(v) {
      const o = this.riskLevelOptions.find(x => x.value === v)
      return o ? o.label : (v === undefined || v === null ? '—' : v)
    },
    formatPriority(v) {
      const o = this.priorityOptions.find(x => x.value === v)
      return o ? o.label : (v === undefined || v === null ? '—' : v)
    },
    formatConfigStatus(v) {
      const o = this.statusOptions.find(x => x.value === v)
      return o ? o.label : (v === undefined || v === null ? '—' : v)
    },
    resetSkillFormModel() {
      this.skillForm = {
        skillId: null,
        moduleId: '',
        name: '',
        code: '',
        description: '',
        triggerCondition: '',
        reasoningPath: '',
        outputSpec: '',
        skillType: 1,
        riskLevel: 2,
        tags: [],
        status: 1
      }
    },
    resetRuleFormModel() {
      this.ruleForm = {
        ruleId: null,
        moduleId: '',
        name: '',
        ruleCode: '',
        ruleContent: '',
        applicableScene: '',
        example: '',
        priority: 2,
        tags: [],
        status: 1
      }
    },
    bootstrap() {
      this.loadProductOptions().then(() => {
        const routePid = this.$route.query.productId ? Number(this.$route.query.productId) : ''
        const routeProj = this.$route.query.projectId ? Number(this.$route.query.projectId) : ''
        if (routePid) {
          this.selectedProductId = routePid
          return this.loadProjectOptions(routePid).then(() => {
            if (routeProj) this.selectedProjectId = pickIdFromOptions(this.projectOptions, routeProj)
          })
        }
        const cached = readLastProductProjectCache()
        if (cached && cached.productId != null && cached.projectId != null) {
          this.selectedProductId = pickIdFromOptions(this.productOptions, cached.productId)
          return this.loadProjectOptions(this.selectedProductId).then(() => {
            this.selectedProjectId = pickIdFromOptions(this.projectOptions, cached.projectId)
          })
        }
        return Promise.resolve()
      }).then(() => {
        if (this.projectId) {
          this.loadModuleTree()
          if (this.configActiveTab === 'rules') this.fetchRuleList()
          else this.fetchSkillList()
        }
      })
    },
    loadProductOptions() {
      if (this.productOptions.length) return Promise.resolve()
      return getProductList({ pageNo: 1, pageSize: 1000, status: 1 }).then(res => {
        const data = (res && res.data) || res || {}
        this.productOptions = data.items || data.list || data.data || []
      }).catch(() => { this.productOptions = [] })
    },
    loadProjectOptions(productId) {
      if (!productId) {
        this.projectOptions = []
        return Promise.resolve()
      }
      return getProjectList({ pageNo: 1, pageSize: 1000, status: 1, productId }).then(res => {
        const data = (res && res.data) || res || {}
        this.projectOptions = data.items || data.list || data.data || []
      }).catch(() => { this.projectOptions = [] })
    },
    loadModuleTree() {
      if (!this.projectId) {
        this.moduleTree = []
        return
      }
      getModuleTree({ projectId: this.projectId }).then(res => {
        const data = (res && res.data) || res || {}
        const list = data.list || data.items || []
        this.moduleTree = Array.isArray(list) ? list : []
      }).catch(() => { this.moduleTree = [] })
    },
    handleProductChange() {
      this.selectedProjectId = ''
      this.projectOptions = []
      this.moduleTree = []
      this.skillList = []
      this.ruleList = []
      this.skillTotal = 0
      this.ruleTotal = 0
      this.loadProjectOptions(this.selectedProductId)
    },
    handleProjectChange() {
      if (this.selectedProductId && this.selectedProjectId) {
        saveLastProductProjectCache(this.selectedProductId, this.selectedProjectId)
      }
      this.skillPageNo = 1
      this.rulePageNo = 1
      this.loadModuleTree()
      if (this.projectId) {
        if (this.configActiveTab === 'rules') this.fetchRuleList()
        else this.fetchSkillList()
      } else {
        this.skillList = []
        this.ruleList = []
        this.skillTotal = 0
        this.ruleTotal = 0
      }
    },
    resetSkillQuery() {
      this.skillQuery = { moduleId: '', keyword: '', status: '', skillType: '', riskLevel: '' }
      this.skillPageNo = 1
      this.fetchSkillList()
    },
    resetRuleQuery() {
      this.ruleQuery = { moduleId: '', keyword: '', status: '', priority: '' }
      this.rulePageNo = 1
      this.fetchRuleList()
    },
    fetchSkillList() {
      if (!this.projectId) return
      this.skillLoading = true
      const params = this.cleanParams(Object.assign({}, this.skillQuery, {
        pageNo: this.skillPageNo,
        pageSize: this.skillPageSize,
        projectId: this.projectId
      }))
      getSkillList(params).then(res => {
        const data = (res && res.data) || res || {}
        const list = data.list || data.items || []
        this.skillList = Array.isArray(list) ? list : []
        this.skillTotal = Number(data.total || 0)
      }).catch(() => {
        this.skillList = []
        this.skillTotal = 0
      }).finally(() => { this.skillLoading = false })
    },
    fetchRuleList() {
      if (!this.projectId) return
      this.ruleLoading = true
      const params = this.cleanParams(Object.assign({}, this.ruleQuery, {
        pageNo: this.rulePageNo,
        pageSize: this.rulePageSize,
        projectId: this.projectId
      }))
      getBusinessRuleList(params).then(res => {
        const data = (res && res.data) || res || {}
        const list = data.list || data.items || []
        this.ruleList = Array.isArray(list) ? list : []
        this.ruleTotal = Number(data.total || 0)
      }).catch(() => {
        this.ruleList = []
        this.ruleTotal = 0
      }).finally(() => { this.ruleLoading = false })
    },
    onSkillSize(s) {
      this.skillPageSize = s
      this.skillPageNo = 1
      this.fetchSkillList()
    },
    onSkillPage(p) {
      this.skillPageNo = p
      this.fetchSkillList()
    },
    onRuleSize(s) {
      this.rulePageSize = s
      this.rulePageNo = 1
      this.fetchRuleList()
    },
    onRulePage(p) {
      this.rulePageNo = p
      this.fetchRuleList()
    },
    openSkillCreate() {
      if (!this.projectId) {
        this.$message.warning('请先选择项目')
        return
      }
      this.skillDialogMode = 'create'
      this.resetSkillFormModel()
      this.skillDialogVisible = true
      this.$nextTick(() => this.$refs.skillFormRef && this.$refs.skillFormRef.clearValidate())
    },
    openSkillEdit(row) {
      if (!row || !row.id) return
      getSkillDetail(row.id).then(res => {
        const d = (res && res.data) || res || {}
        this.skillDialogMode = 'edit'
        this.skillForm = {
          skillId: d.id,
          moduleId: d.module_id != null && d.module_id !== '' ? d.module_id : '',
          name: d.name || '',
          code: d.code || '',
          description: d.description || '',
          triggerCondition: d.trigger_condition || '',
          reasoningPath: d.reasoning_path || '',
          outputSpec: d.output_spec || '',
          skillType: d.skill_type !== undefined ? d.skill_type : 1,
          riskLevel: d.risk_level !== undefined ? d.risk_level : 2,
          tags: Array.isArray(d.tags) ? d.tags.slice() : [],
          status: d.status !== undefined ? d.status : 1
        }
        this.skillDialogVisible = true
        this.$nextTick(() => this.$refs.skillFormRef && this.$refs.skillFormRef.clearValidate())
      })
    },
    resetSkillForm() {
      this.resetSkillFormModel()
    },
    submitSkill() {
      const form = this.$refs.skillFormRef
      if (!form) return
      form.validate(valid => {
        if (!valid) return
        const tags = Array.isArray(this.skillForm.tags) ? this.skillForm.tags.filter(Boolean) : []
        this.skillSubmitting = true
        const done = () => { this.skillSubmitting = false }
        if (this.skillDialogMode === 'create') {
          createSkill(this.cleanParams({
            projectId: this.projectId,
            moduleId: this.skillForm.moduleId || undefined,
            name: this.skillForm.name,
            code: this.generateAutoSkillCode(),
            description: this.skillForm.description || undefined,
            triggerCondition: '由系统自动创建，可在编辑中完善。',
            skillType: this.skillForm.skillType,
            riskLevel: this.skillForm.riskLevel,
            tags,
            status: this.skillForm.status
          })).then(() => {
            this.$message.success('创建成功')
            this.skillDialogVisible = false
            this.fetchSkillList()
          }).finally(done)
        } else {
          updateSkill(this.cleanParams({
            skillId: this.skillForm.skillId,
            name: this.skillForm.name,
            description: this.skillForm.description || undefined,
            triggerCondition: this.skillForm.triggerCondition,
            reasoningPath: this.skillForm.reasoningPath || undefined,
            outputSpec: this.skillForm.outputSpec || undefined,
            skillType: this.skillForm.skillType,
            riskLevel: this.skillForm.riskLevel,
            tags,
            status: this.skillForm.status
          })).then(() => {
            this.$message.success('保存成功')
            this.skillDialogVisible = false
            this.fetchSkillList()
          }).finally(done)
        }
      })
    },
    removeSkill(row) {
      this.$confirm('确认删除该 Skill？', '提示', { type: 'warning' }).then(() => {
        deleteSkill(row.id).then(() => {
          this.$message.success('已删除')
          this.fetchSkillList()
        })
      }).catch(() => {})
    },
    openRuleCreate() {
      if (!this.projectId) {
        this.$message.warning('请先选择项目')
        return
      }
      this.ruleDialogMode = 'create'
      this.resetRuleFormModel()
      this.ruleDialogVisible = true
      this.$nextTick(() => this.$refs.ruleFormRef && this.$refs.ruleFormRef.clearValidate())
    },
    openRuleEdit(row) {
      if (!row || !row.id) return
      getBusinessRuleDetail(row.id).then(res => {
        const d = (res && res.data) || res || {}
        this.ruleDialogMode = 'edit'
        this.ruleForm = {
          ruleId: d.id,
          moduleId: d.module_id != null && d.module_id !== '' ? d.module_id : '',
          name: d.name || '',
          ruleCode: d.rule_code || '',
          ruleContent: d.rule_content || '',
          applicableScene: d.applicable_scene || '',
          example: d.example || '',
          priority: d.priority !== undefined ? d.priority : 2,
          tags: Array.isArray(d.tags) ? d.tags.slice() : [],
          status: d.status !== undefined ? d.status : 1
        }
        this.ruleDialogVisible = true
        this.$nextTick(() => this.$refs.ruleFormRef && this.$refs.ruleFormRef.clearValidate())
      })
    },
    resetRuleForm() {
      this.resetRuleFormModel()
    },
    submitRule() {
      const form = this.$refs.ruleFormRef
      if (!form) return
      form.validate(valid => {
        if (!valid) return
        const tags = Array.isArray(this.ruleForm.tags) ? this.ruleForm.tags.filter(Boolean) : []
        this.ruleSubmitting = true
        const done = () => { this.ruleSubmitting = false }
        if (this.ruleDialogMode === 'create') {
          createBusinessRule(this.cleanParams({
            projectId: this.projectId,
            moduleId: this.ruleForm.moduleId || undefined,
            name: this.ruleForm.name,
            ruleContent: this.ruleForm.ruleContent,
            applicableScene: this.ruleForm.applicableScene || undefined,
            example: this.ruleForm.example || undefined,
            priority: this.ruleForm.priority,
            tags,
            status: this.ruleForm.status
          })).then(() => {
            this.$message.success('创建成功')
            this.ruleDialogVisible = false
            this.fetchRuleList()
          }).finally(done)
        } else {
          updateBusinessRule(this.cleanParams({
            ruleId: this.ruleForm.ruleId,
            name: this.ruleForm.name,
            ruleContent: this.ruleForm.ruleContent,
            applicableScene: this.ruleForm.applicableScene || undefined,
            example: this.ruleForm.example || undefined,
            priority: this.ruleForm.priority,
            tags,
            status: this.ruleForm.status
          })).then(() => {
            this.$message.success('保存成功')
            this.ruleDialogVisible = false
            this.fetchRuleList()
          }).finally(done)
        }
      })
    },
    removeRule(row) {
      this.$confirm('确认删除该业务规则？', '提示', { type: 'warning' }).then(() => {
        deleteBusinessRule(row.id).then(() => {
          this.$message.success('已删除')
          this.fetchRuleList()
        })
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.page-wrap {
  padding: 20px;
}
.filter-bar {
  margin-bottom: 8px;
}
.toolbar-form {
  margin-top: 0;
}
.pager-wrap {
  margin-top: 12px;
  text-align: right;
}

.skill-rule-tabs /deep/ .el-tabs__header {
  margin-bottom: 12px;
}
</style>
