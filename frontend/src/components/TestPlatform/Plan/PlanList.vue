<template>
  <div class="page-wrap">
    <page-section title="测试计划">
      <template slot="extra">
        <el-button type="primary" size="small" @click="goBuilder()">新建计划</el-button>
      </template>
      <el-form :inline="true" size="small" @submit.native.prevent>
        <el-form-item label="产品名称">
          <el-select
            v-model="selectedProductId"
            filterable
            clearable
            placeholder="请选择产品"
            style="width: 220px;"
            @change="handleProductChange"
            @focus="loadProductOptions">
            <el-option
              v-for="item in productOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目名称">
          <el-select
            v-model="selectedProjectId"
            filterable
            clearable
            placeholder="请选择项目"
            style="width: 240px;"
            :disabled="!selectedProductId"
            @change="handleProjectChange">
            <el-option
              v-for="item in projectOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <el-form :inline="true" :model="queryForm" size="small" style="margin-top: 8px;" @submit.native.prevent>
        <el-form-item label="计划名称">
          <el-input v-model="queryForm.planName" clearable style="width: 180px;"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryForm.status" clearable style="width: 120px;">
            <el-option label="草稿" :value="0"></el-option>
            <el-option label="进行中" :value="1"></el-option>
            <el-option label="已完成" :value="2"></el-option>
            <el-option label="已归档" :value="3"></el-option>
            <el-option label="已通过" :value="4"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="版本">
          <el-input v-model="queryForm.version" clearable style="width: 140px;"></el-input>
        </el-form-item>
        <el-form-item label="负责人">
          <el-select
            v-model="queryForm.owner"
            filterable
            clearable
            placeholder="请选择负责人"
            style="width: 180px;"
            :disabled="!selectedProjectId">
            <el-option v-for="u in ownerMemberOptions" :key="'plan-owner-' + u.id" :label="u.name" :value="u.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :disabled="!selectedProjectId" @click="fetchList">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button size="small" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
      <el-table v-loading="loading" :data="tableData" border style="margin-top: 16px;">
        <el-table-column prop="name" label="计划名称" min-width="180"></el-table-column>
        <el-table-column label="是否自动化测试" width="140">
          <template slot-scope="scope">{{ formatPlanIsAuto(scope.row) }}</template>
        </el-table-column>
        <el-table-column label="开始时间" min-width="170">
          <template slot-scope="scope">{{ formatDateTime(getStartTimeValue(scope.row)) }}</template>
        </el-table-column>
        <el-table-column label="结束时间" min-width="170">
          <template slot-scope="scope">{{ formatDateTime(getEndTimeValue(scope.row)) }}</template>
        </el-table-column>
        <el-table-column label="负责人" width="140">
          <template slot-scope="scope">{{ formatOwner(scope.row) }}</template>
        </el-table-column>
        <el-table-column label="环境" width="160">
          <template slot-scope="scope">{{ formatEnvironment(scope.row) }}</template>
        </el-table-column>
        <el-table-column label="状态" width="110">
          <template slot-scope="scope">{{ formatStatus(scope.row.status) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="660">
          <template slot-scope="scope">
            <el-button type="text" @click="goEdit(scope.row)">编辑</el-button>
            <el-button type="text" @click="goAssociateCases(scope.row)">关联用例</el-button>
            <el-button v-if="!isPlanAutomation(scope.row)" type="text" @click="goExecute(scope.row)">执行</el-button>
            <el-button type="text" @click="goProgress(scope.row)">进度</el-button>
            <el-button type="text" @click="openHookSendDialog(scope.row)">发送消息</el-button>
            <el-button v-if="isPlanAutomation(scope.row)" type="text" @click="runAutoCases(scope.row)">执行自动化用例</el-button>
            <el-button type="text" class="danger-text" @click="confirmDeletePlan(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-dialog
        title="发送消息"
        :visible.sync="hookSendDialogVisible"
        width="600px"
        append-to-body
        @close="resetHookSendForm">
        <el-form ref="hookSendFormRef" :model="hookSendForm" label-width="108px" size="small">
          <el-form-item label="计划">
            <el-input :value="hookSendPlanName" disabled />
          </el-form-item>
          <el-form-item label="消息标题">
            <el-input :value="hookSendPreviewTitle" disabled />
          </el-form-item>
          <el-form-item label="消息正文" prop="content">
            <el-input
              v-model.trim="hookSendForm.content"
              type="textarea"
              :rows="5"
              maxlength="4000"
              show-word-limit
              placeholder="默认含待执行说明与计划执行链接，可自行修改" />
          </el-form-item>
          <el-form-item label="消息类型">
            <el-select
              v-model="hookSendForm.hookType"
              clearable
              placeholder="不选则加载全部类型下的配置"
              style="width: 100%;"
              @change="onHookSendTypeChange">
              <el-option label="飞书" :value="1" />
              <el-option label="钉钉" :value="2" />
              <el-option label="企微" :value="3" />
            </el-select>
          </el-form-item>
          <el-form-item label="Webhook 配置">
            <el-select
              v-model="hookSendForm.hookId"
              filterable
              clearable
              :loading="hookSendHookListLoading"
              placeholder="选择当前项目、当前类型下的配置；不选则按类型发全部（未选类型则发全部 Hook）"
              style="width: 100%;">
              <el-option
                v-for="h in hookSendHookOptions"
                :key="'hook-opt-' + h.id"
                :label="formatHookSendOptionLabel(h)"
                :value="h.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="@ 真实姓名" prop="realName">
            <el-input v-model.trim="hookSendForm.realName" maxlength="64" placeholder="默认计划负责人，可改" />
          </el-form-item>
        </el-form>
        <div v-if="hookSendResultLines.length" class="hook-send-result">
          <div class="hook-send-result-title">发送结果</div>
          <div v-for="(line, idx) in hookSendResultLines" :key="'hr-' + idx" class="hook-send-result-line">{{ line }}</div>
        </div>
        <span slot="footer">
          <el-button size="small" @click="hookSendDialogVisible = false">取消</el-button>
          <el-button type="primary" size="small" :loading="hookSendSubmitting" @click="submitHookSend">发送</el-button>
        </span>
      </el-dialog>
      <div style="margin-top: 16px; text-align: right;">
        <el-pagination
          :current-page="pageNo"
          :page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange">
        </el-pagination>
      </div>
    </page-section>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { deletePlan, getPlanList } from '@/api/planApi'
import { getProductList } from '@/api/productApi'
import {
  getProjectDetail,
  getProjectEnvironments,
  getProjectHookList,
  getProjectList,
  getProjectMembers,
  sendProjectHookMessage
} from '@/api/projectApi'
import {
  readLastProductProjectCache,
  saveLastProductProjectCache,
  pickIdFromOptions
} from '@/utils/lastProductProjectCache'

export default {
  name: 'PlanList',
  components: { PageSection },
  computed: {
    hookSendPreviewTitle() {
      const row = this.hookSendPlanRow
      if (!row) return ''
      return (row.name || '').trim() || this.hookSendPlanName || '测试计划'
    }
  },
  data() {
    return {
      loading: false,
      projectId: this.$route.query.projectId || '',
      selectedProductId: '',
      selectedProjectId: this.$route.query.projectId ? Number(this.$route.query.projectId) : '',
      productOptions: [],
      projectOptions: [],
      ownerMap: {},
      /** 负责人筛选下拉（label 优先 real_name，与 ownerMap 同源） */
      ownerMemberOptions: [],
      environmentMap: {},
      queryForm: {
        planName: '',
        status: '',
        version: '',
        owner: ''
      },
      pageNo: 1,
      pageSize: 10,
      total: 0,
      tableData: [],
      hookSendDialogVisible: false,
      hookSendSubmitting: false,
      hookSendPlanName: '',
      /** 当前要推送机器人消息的计划行 */
      hookSendPlanRow: null,
      hookSendHookOptions: [],
      hookSendHookListLoading: false,
      hookSendForm: {
        hookType: '',
        hookId: '',
        content: '',
        realName: ''
      },
      hookSendResultLines: []
    }
  },
  beforeRouteLeave(to, from, next) {
    this.savePageCache()
    next()
  },
  methods: {
    getCacheKey() {
      return 'test-platform-plan-list-cache'
    },
    savePageCache() {
      const cache = {
        projectId: this.projectId,
        selectedProductId: this.selectedProductId,
        selectedProjectId: this.selectedProjectId,
        productOptions: this.productOptions,
        projectOptions: this.projectOptions,
        ownerMap: this.ownerMap,
        ownerMemberOptions: this.ownerMemberOptions,
        environmentMap: this.environmentMap,
        queryForm: this.queryForm,
        pageNo: this.pageNo,
        pageSize: this.pageSize,
        total: this.total,
        tableData: this.tableData
      }
      window.sessionStorage.setItem(this.getCacheKey(), JSON.stringify(cache))
    },
    restorePageCache() {
      const raw = window.sessionStorage.getItem(this.getCacheKey())
      if (!raw) return false
      try {
        const cache = JSON.parse(raw)
        this.projectId = cache.projectId || ''
        this.selectedProductId = cache.selectedProductId || ''
        this.selectedProjectId = cache.selectedProjectId || ''
        this.productOptions = cache.productOptions || []
        this.projectOptions = cache.projectOptions || []
        this.ownerMap = cache.ownerMap || {}
        this.ownerMemberOptions = Array.isArray(cache.ownerMemberOptions) ? cache.ownerMemberOptions : []
        if (!this.ownerMemberOptions.length && this.ownerMap && Object.keys(this.ownerMap).length) {
          this.ownerMemberOptions = Object.keys(this.ownerMap).map(k => ({
            id: /^\d+$/.test(String(k)) ? Number(k) : k,
            name: this.ownerMap[k]
          }))
        }
        this.environmentMap = cache.environmentMap || {}
        this.queryForm = cache.queryForm || {
          planName: '',
          status: '',
          version: '',
          owner: ''
        }
        this.syncOwnerFilterWithMemberOptions()
        this.pageNo = Number(cache.pageNo || 1)
        this.pageSize = Number(cache.pageSize || 10)
        this.total = Number(cache.total || 0)
        this.tableData = Array.isArray(cache.tableData) ? cache.tableData : []
        return true
      } catch (e) {
        return false
      }
    },
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
    handleProductChange(val) {
      this.selectedProjectId = ''
      this.projectId = ''
      this.queryForm.owner = ''
      this.ownerMap = {}
      this.ownerMemberOptions = []
      this.tableData = []
      this.total = 0
      this.loadProjectOptionsByProduct(val)
    },
    handleProjectChange(val) {
      this.selectedProjectId = val || ''
      this.projectId = val || ''
      this.pageNo = 1
      this.queryForm.owner = ''
      this.ownerMap = {}
      this.ownerMemberOptions = []
      this.environmentMap = {}
      if (!val) {
        this.tableData = []
        this.total = 0
        return
      }
      saveLastProductProjectCache(this.selectedProductId, val)
      this.loadProjectMetaMaps(val).finally(() => {
        this.fetchList()
      })
    },
    restoreSharedProductProjectCache() {
      const cached = readLastProductProjectCache()
      const q = this.$route.query || {}
      const fromPlanSelf = q.planOwnerSelf === '1' || q.planOwnerSelf === 'true'
      let pid = cached && cached.productId
      let projId = cached && cached.projectId
      if (fromPlanSelf) {
        if (q.productId !== undefined && q.productId !== null && String(q.productId).trim() !== '') {
          pid = q.productId
        }
        if (q.projectId !== undefined && q.projectId !== null && String(q.projectId).trim() !== '') {
          projId = q.projectId
        }
      }
      if (pid === '' || pid === undefined || pid === null || projId === '' || projId === undefined || projId === null) {
        return Promise.resolve()
      }
      const hasProduct = (this.productOptions || []).some(p => String(p.id) === String(pid))
      if (!hasProduct) return Promise.resolve()
      this.selectedProductId = pickIdFromOptions(this.productOptions, pid)
      return this.loadProjectOptionsByProduct(this.selectedProductId).then(() => {
        const hasProject = (this.projectOptions || []).some(p => String(p.id) === String(projId))
        if (!hasProject) return
        const picked = pickIdFromOptions(this.projectOptions, projId)
        this.selectedProjectId = picked
        this.projectId = picked
      })
    },
    mergeCurrentUserIntoOwnerMemberOptionsIfNeeded() {
      const u = this.$store.state.currentUser
      if (!u || u.id == null || u.id === '') return
      const id = u.id
      if ((this.ownerMemberOptions || []).some(m => String(m.id) === String(id))) return
      const name = u.realName || u.username || '当前用户'
      this.ownerMemberOptions = [{ id, name }, ...(this.ownerMemberOptions || [])]
      this.ownerMap = Object.assign({}, this.ownerMap, { [id]: name })
    },
    applyPlanOwnerSelfFromRoute() {
      const q = this.$route.query || {}
      if (q.planOwnerSelf !== '1' && q.planOwnerSelf !== 'true') return
      const u = this.$store.state.currentUser
      const uid = u && u.id != null && u.id !== '' ? u.id : null
      if (uid == null) {
        this.$message.warning('请先登录')
        return
      }
      if (!this.selectedProjectId) {
        this.$message.warning('请先选择项目，或从首页在已选过产品/项目时进入')
        return
      }
      this.mergeCurrentUserIntoOwnerMemberOptionsIfNeeded()
      this.queryForm.owner = uid
      this.pageNo = 1
    },
    /** 负责人筛选值为成员 id；若不在当前项目成员列表中则清空（避免缓存里旧姓名或无效 id） */
    syncOwnerFilterWithMemberOptions() {
      const cur = this.queryForm.owner
      if (cur === '' || cur === undefined || cur === null) return
      const idSet = new Set(this.ownerMemberOptions.map(u => String(u.id)))
      if (!idSet.has(String(cur))) {
        this.queryForm.owner = ''
      }
    },
    loadProjectMetaMaps(projectId) {
      if (!projectId) {
        this.ownerMap = {}
        this.ownerMemberOptions = []
        this.environmentMap = {}
        return Promise.resolve()
      }
      const memberReq = getProjectMembers(projectId, { pageNo: 1, pageSize: 1000 }).then(res => {
        const data = (res && res.data) || res || {}
        const list = data.items || data.list || data.data || data || []
        const arr = Array.isArray(list) ? list : []
        this.ownerMemberOptions = arr
          .map(item => {
            const id = item.user_id || item.userId || item.id
            const name =
              item.real_name ||
              item.realName ||
              item.username ||
              item.name ||
              item.user_name ||
              (id !== undefined && id !== null ? String(id) : '')
            return { id, name }
          })
          .filter(u => u.id !== undefined && u.id !== null && u.id !== '')
        this.ownerMap = this.ownerMemberOptions.reduce((map, u) => {
          map[u.id] = u.name || String(u.id)
          return map
        }, {})
        this.syncOwnerFilterWithMemberOptions()
      }).catch(() => {
        this.ownerMap = {}
        this.ownerMemberOptions = []
      })
      const envReq = getProjectEnvironments(projectId, { pageNo: 1, pageSize: 1000 }).then(res => {
        const data = (res && res.data) || res || {}
        const list = data.items || data.list || data.data || data || []
        this.environmentMap = (Array.isArray(list) ? list : []).reduce((map, item) => {
          if (item.id !== undefined && item.id !== null && item.id !== '') {
            map[item.id] = item.name || String(item.id)
          }
          return map
        }, {})
      }).catch(() => {
        this.environmentMap = {}
      })
      return Promise.all([memberReq, envReq])
    },
    fetchList() {
      if (!this.projectId) {
        this.tableData = []
        this.total = 0
        return
      }
      this.loading = true
      const params = this.cleanParams({
        planName: this.queryForm.planName,
        keyword: this.queryForm.planName,
        status: this.queryForm.status,
        version: this.queryForm.version,
        owner: this.queryForm.owner,
        owner_id: this.queryForm.owner,
        pageNo: this.pageNo,
        pageSize: this.pageSize
      })
      getPlanList(this.projectId, params).then(res => {
        const data = (res && res.data) || res || {}
        this.tableData = data.items || data.list || []
        this.total = Number(data.total || this.tableData.length || 0)
        this.savePageCache()
      }).catch(() => {
        this.tableData = []
        this.total = 0
        this.savePageCache()
      }).finally(() => {
        this.loading = false
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
    resetQuery() {
      this.queryForm = {
        planName: '',
        status: '',
        version: '',
        owner: ''
      }
      this.pageNo = 1
      this.fetchList()
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.pageNo = 1
      this.fetchList()
    },
    handleCurrentChange(page) {
      this.pageNo = page
      this.fetchList()
    },
    goBuilder() {
      this.$router.push({ path: '/test-platform/plan/builder', query: { projectId: this.projectId } })
    },
    goEdit(row) {
      this.$router.push({
        path: '/test-platform/plan/builder',
        query: {
          projectId: this.projectId,
          planId: row.id
        }
      })
    },
    confirmDeletePlan(row) {
      if (!row || row.id == null) {
        this.$message.warning('缺少计划信息')
        return
      }
      if (!this.projectId) {
        this.$message.warning('请先选择项目')
        return
      }
      const name = (row.name || '').trim() || `计划 #${row.id}`
      this.$confirm(`确定删除计划「${name}」吗？删除后不可恢复。`, '删除确认', {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => deletePlan(row.id))
        .then(() => {
          this.$message.success('删除成功')
          this.fetchList()
        })
        .catch(() => {})
    },
    goAssociateCases(row) {
      const project = (this.projectOptions || []).find(item => String(item.id) === String(this.projectId))
      const product = (this.productOptions || []).find(item => String(item.id) === String(this.selectedProductId))
      this.$router.push({
        path: '/test-platform/plan/case/add',
        query: {
          productId: this.selectedProductId || undefined,
          productName: (product && product.name) || '',
          projectId: this.projectId || undefined,
          projectName: (project && project.name) || '',
          planId: row.id,
          planName: row.name || '',
          ownerId: row.owner_id || row.ownerId || undefined
        }
      })
    },
    goExecute(row) {
      const project = (this.projectOptions || []).find(item => String(item.id) === String(this.projectId))
      const product = (this.productOptions || []).find(item => String(item.id) === String(this.selectedProductId))
      this.$router.push({
        path: '/test-platform/plan/execute',
        query: {
          productId: this.selectedProductId || undefined,
          productName: (product && product.name) || '',
          projectId: this.projectId,
          projectName: (project && project.name) || '',
          planId: row.id,
          planName: row.name || ''
        }
      })
    },
    openHookSendDialog(row) {
      if (!this.projectId) {
        this.$message.warning('请先选择项目')
        return
      }
      const name = (row && row.name) || ''
      this.hookSendPlanName = name || `计划 #${row && row.id != null ? row.id : ''}`
      this.hookSendPlanRow = row || null
      const defaultContent = this.buildPlanExecuteMessageBody(row)
      const defaultReal = this.getPlanOwnerRealName(row)
      this.hookSendForm = {
        hookType: '',
        hookId: '',
        content: defaultContent,
        realName: defaultReal
      }
      this.hookSendHookOptions = []
      this.hookSendResultLines = []
      this.hookSendDialogVisible = true
      this.loadHookSendOptions()
      this.$nextTick(() => {
        if (this.$refs.hookSendFormRef) {
          this.$refs.hookSendFormRef.clearValidate()
        }
      })
    },
    resetHookSendForm() {
      this.hookSendSubmitting = false
      this.hookSendPlanName = ''
      this.hookSendPlanRow = null
      this.hookSendHookOptions = []
      this.hookSendForm = {
        hookType: '',
        hookId: '',
        content: '',
        realName: ''
      }
      this.hookSendResultLines = []
      this.$nextTick(() => {
        if (this.$refs.hookSendFormRef) {
          this.$refs.hookSendFormRef.resetFields()
        }
      })
    },
    /** 与「执行」入口一致的计划执行页链接（绝对地址，便于 IM 中点击） */
    buildPlanExecuteUrl(row) {
      if (!row || row.id == null) return ''
      const project = (this.projectOptions || []).find(item => String(item.id) === String(this.projectId))
      const product = (this.productOptions || []).find(item => String(item.id) === String(this.selectedProductId))
      const loc = this.$router.resolve({
        path: '/test-platform/plan/execute',
        query: {
          productId: this.selectedProductId || undefined,
          productName: (product && product.name) || '',
          projectId: this.projectId,
          projectName: (project && project.name) || '',
          planId: row.id,
          planName: row.name || ''
        }
      })
      const href = (loc && loc.href) || ''
      if (!href) return ''
      if (/^https?:\/\//i.test(href)) return href
      const origin = typeof window !== 'undefined' && window.location ? window.location.origin : ''
      return origin + (href.charAt(0) === '/' ? href : `/${href}`)
    },
    buildPlanExecuteMessageBody(row) {
      const url = this.buildPlanExecuteUrl(row)
      if (!url) return '你有一条测试计划待执行：'
      return `你有一条测试计划待执行：\n${url}`
    },
    /** 计划负责人展示名（优先真实姓名类字段，用于 @） */
    getPlanOwnerRealName(row) {
      if (!row) return ''
      const oid = row.owner_id != null ? row.owner_id : row.ownerId
      const fromMap = oid != null && oid !== '' ? this.ownerMap[oid] : ''
      const s = (
        row.owner_real_name ||
        row.ownerRealName ||
        row.owner_name ||
        row.ownerName ||
        fromMap ||
        ''
      ).trim()
      return s
    },
    onHookSendTypeChange() {
      this.hookSendForm.hookId = ''
      this.loadHookSendOptions()
    },
    loadHookSendOptions() {
      const pid = Number(this.projectId)
      if (!pid || Number.isNaN(pid)) {
        this.hookSendHookOptions = []
        return
      }
      const params = { projectId: pid, pageNo: 1, pageSize: 500 }
      const ht = this.hookSendForm.hookType
      if (ht === 1 || ht === 2 || ht === 3) {
        params.hookType = ht
      }
      this.hookSendHookListLoading = true
      getProjectHookList(params)
        .then(res => {
          const data = (res && res.data) || res || {}
          const list = data.list || data.items || []
          this.hookSendHookOptions = Array.isArray(list) ? list : []
        })
        .catch(() => {
          this.hookSendHookOptions = []
        })
        .finally(() => {
          this.hookSendHookListLoading = false
        })
    },
    formatHookSendOptionLabel(item) {
      if (!item) return ''
      const typeName = item.hook_type_name || this.hookTypeSendLabel(item.hook_type != null ? item.hook_type : item.hookType)
      const desc = (item.description || '').trim()
      const url = String(item.webhook_url || item.webhookUrl || '').trim()
      const shortUrl = url.length > 42 ? `${url.slice(0, 42)}…` : url
      if (desc) return `${desc}（${typeName} #${item.id}）`
      if (shortUrl) return `${shortUrl}（${typeName} #${item.id}）`
      return `${typeName} #${item.id}`
    },
    hookTypeSendLabel(type) {
      const map = { 1: '飞书', 2: '钉钉', 3: '企微' }
      return map[Number(type)] || String(type || '-')
    },
    submitHookSend() {
      const row = this.hookSendPlanRow
      if (!row || row.id == null) {
        this.$message.warning('缺少计划信息')
        return
      }
      const pid = Number(this.projectId)
      if (!pid || Number.isNaN(pid)) {
        this.$message.warning('项目 ID 无效')
        return
      }
      const title = (this.hookSendPreviewTitle || '').trim() || '测试计划'
      const content = (this.hookSendForm.content || '').trim()
      if (!content) {
        this.$message.warning('消息正文不能为空')
        return
      }
      if (content === '你有一条测试计划待执行：') {
        this.$message.warning('无法生成计划执行链接，请检查项目与计划')
        return
      }
      const payload = {
        projectId: pid,
        title,
        content
      }
      const rn = (this.hookSendForm.realName || '').trim()
      if (rn) payload.realName = rn
      const hid = this.hookSendForm.hookId
      if (hid !== '' && hid !== null && hid !== undefined) {
        const n = Number(hid)
        if (!Number.isNaN(n)) {
          payload.hookId = n
          const found = (this.hookSendHookOptions || []).find(h => String(h.id) === String(hid))
          const fht = found && (found.hook_type != null ? found.hook_type : found.hookType)
          if (fht === 1 || fht === 2 || fht === 3) {
            payload.hookType = fht
          }
        }
      } else {
        const ht = this.hookSendForm.hookType
        if (ht === 1 || ht === 2 || ht === 3) {
          payload.hookType = ht
        }
      }
      this.hookSendSubmitting = true
      this.hookSendResultLines = []
      sendProjectHookMessage(payload)
        .then(res => {
          const msg = (res && res.message) || ''
          if (res && res.code === 20000) {
            const list = res.data
            const lines = []
            if (Array.isArray(list)) {
              list.forEach(item => {
                const hid = item.hook_id != null ? item.hook_id : item.hookId
                const htype = item.hook_type != null ? item.hook_type : item.hookType
                const ok = item.success === true || item.success === 1
                lines.push(
                  `Hook #${hid}（${this.hookTypeSendLabel(htype)}）：${ok ? '成功' : '失败'}`
                )
              })
            }
            this.hookSendResultLines = lines
            this.$message.success(msg || '已提交发送')
            return
          }
          this.$message.error(msg || '发送失败')
        })
        .catch(() => {})
        .finally(() => {
          this.hookSendSubmitting = false
        })
    },
    runAutoCases(row) {
      if (!row || row.id == null) {
        this.$message.warning('缺少计划信息')
        return
      }
      if (!this.projectId) {
        this.$message.warning('请先选择项目')
        return
      }
      const project = (this.projectOptions || []).find(item => String(item.id) === String(this.projectId))
      const product = (this.productOptions || []).find(item => String(item.id) === String(this.selectedProductId))
      const jenkinsUrl = (row.jenkins_url || row.jenkinsUrl || '').trim()
      this.$router.push({
        path: '/test-platform/plan/automation',
        query: {
          productId: this.selectedProductId || undefined,
          productName: (product && product.name) || '',
          projectId: this.projectId,
          projectName: (project && project.name) || '',
          planId: row.id,
          planName: row.name || '',
          environmentId: row.environment_id != null ? row.environment_id : row.environmentId,
          jenkinsUrl: jenkinsUrl || undefined
        }
      })
    },
    goProgress(row) {
      const project = (this.projectOptions || []).find(item => String(item.id) === String(this.projectId))
      const product = (this.productOptions || []).find(item => String(item.id) === String(this.selectedProductId))
      this.$router.push({
        path: '/test-platform/plan/progress',
        query: {
          productId: this.selectedProductId || undefined,
          productName: (product && product.name) || '',
          projectId: this.projectId || undefined,
          projectName: (project && project.name) || '',
          planId: row.id,
          planName: row.name || ''
        }
      })
    },
    formatPlanIsAuto(row) {
      if (!row) return '-'
      const v = row.isAuto !== undefined && row.isAuto !== null ? row.isAuto : row.is_auto
      if (v === 1 || v === true || v === '1') return '是'
      if (v === 0 || v === false || v === '0') return '否'
      return '-'
    },
    /** 列表 is_auto === 1：自动化测试计划，只展示「执行自动化用例」 */
    isPlanAutomation(row) {
      if (!row) return false
      const v = row.isAuto !== undefined && row.isAuto !== null ? row.isAuto : row.is_auto
      return v === 1 || v === true || v === '1'
    },
    formatStatus(value) {
      const map = { 0: '草稿', 1: '进行中', 2: '已完成', 3: '已归档', 4: '已通过' }
      return map[value] || value
    },
    formatOwner(row) {
      const ownerId = row.owner_id || row.ownerId
      return row.owner_name || row.ownerName || row.username || row.owner || this.ownerMap[ownerId] || ownerId || '-'
    },
    formatEnvironment(row) {
      const envId = row.environment_id || row.environmentId
      return row.environment_name || row.environmentName || row.env_name || row.environment || this.environmentMap[envId] || envId || '-'
    },
    getStartTimeValue(row) {
      if (!row) return ''
      return row.start_date || row.startDate || row.start_time || row.startTime || row.begin_time || row.beginTime || row.planned_start_time || row.plannedStartTime || ''
    },
    getEndTimeValue(row) {
      if (!row) return ''
      return row.end_date || row.endDate || row.end_time || row.endTime || row.finish_time || row.finishTime || row.planned_end_time || row.plannedEndTime || ''
    },
    formatDateTime(value) {
      if (!value) return '-'
      if (typeof value === 'number' || /^\d+$/.test(String(value))) {
        const raw = Number(value)
        if (!Number.isNaN(raw) && raw > 0) {
          const ms = raw < 1000000000000 ? raw * 1000 : raw
          const date = new Date(ms)
          if (!Number.isNaN(date.getTime())) {
            const pad = n => String(n).padStart(2, '0')
            return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
          }
        }
      }
      return String(value).replace('T', ' ').slice(0, 19)
    }
  },
  created() {
    const planOwnerSelf = this.$route.query.planOwnerSelf === '1' || this.$route.query.planOwnerSelf === 'true'
    if (planOwnerSelf) {
      try {
        window.sessionStorage.removeItem(this.getCacheKey())
      } catch (e) {}
    }
    // 若存在缓存（通常是从二级页返回），直接恢复，不自动刷新数据
    if (this.restorePageCache()) {
      if (planOwnerSelf && this.selectedProjectId) {
        this.$nextTick(() => {
          this.loadProjectMetaMaps(this.selectedProjectId).finally(() => {
            this.applyPlanOwnerSelfFromRoute()
            this.fetchList()
          })
        })
      }
      return
    }
    this.loadProductOptions().then(() => {
      if (this.selectedProjectId) {
        return getProjectDetail(this.selectedProjectId).then(res => {
          const data = res && res.data ? res.data : res || {}
          const productId = data.productId || data.product_id || ''
          if (productId) {
            this.selectedProductId = productId
            return this.loadProjectOptionsByProduct(productId)
          }
        }).catch(() => {})
      }
      return this.restoreSharedProductProjectCache()
    }).finally(() => {
      if (this.selectedProjectId) {
        this.projectId = this.selectedProjectId
        this.loadProjectMetaMaps(this.selectedProjectId).finally(() => {
          this.applyPlanOwnerSelfFromRoute()
          this.fetchList()
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

.danger-text {
  color: #f56c6c;
}

.danger-text:hover {
  color: #f78989;
}

.hook-send-result {
  margin-top: 12px;
  padding: 10px 12px;
  background: #f5f7fa;
  border-radius: 4px;
  font-size: 13px;
  color: #606266;
}

.hook-send-result-title {
  font-weight: 600;
  margin-bottom: 6px;
  color: #303133;
}

.hook-send-result-line {
  line-height: 1.6;
}
</style>
