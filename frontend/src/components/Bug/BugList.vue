<template>
  <div class="page-wrap">
    <page-section title="Bug 列表">
      <template slot="extra">
        <el-button type="primary" size="small" @click="goCreate">新建 Bug</el-button>
      </template>
      <el-form :inline="true" size="small" class="filter-form" @submit.native.prevent>
        <el-form-item label="产品">
          <el-select
            v-model="queryForm.productId"
            filterable
            clearable
            placeholder="产品"
            style="width: 200px;"
            @change="onProductChange"
            @focus="loadProductOptions">
            <el-option v-for="p in productOptions" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目">
          <el-select
            v-model="queryForm.projectId"
            filterable
            clearable
            placeholder="项目"
            style="width: 200px;"
            :disabled="!queryForm.productId"
            @change="onProjectChange">
            <el-option v-for="p in projectOptions" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="模块">
          <el-select v-model="queryForm.moduleId" filterable clearable placeholder="模块" style="width: 180px;" :disabled="!queryForm.projectId">
            <el-option v-for="m in flatModules" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="当前指派">
          <el-select v-model="queryForm.assigneeId" filterable clearable placeholder="当前指派" style="width: 140px;" :disabled="!queryForm.projectId">
            <el-option v-for="u in memberOptions" :key="'a-' + u.id" :label="u.name" :value="u.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryForm.status" clearable placeholder="全部" style="width: 120px;">
            <el-option v-for="(label, key) in statusOptions" :key="key" :label="label" :value="Number(key)" />
          </el-select>
        </el-form-item>
        <el-form-item label="创建人">
          <el-select v-model="queryForm.reporterId" filterable clearable placeholder="创建人" style="width: 140px;" :disabled="!queryForm.projectId">
            <el-option v-for="u in memberOptions" :key="'r-' + u.id" :label="u.name" :value="u.id" />
          </el-select>
        </el-form-item>
        <el-form-item class="more-filter-item">
          <el-popover v-model="moreFilterVisible" placement="bottom-start" width="560" trigger="click">
            <div class="more-filter-wrap">
              <el-form :inline="true" :model="queryForm" size="small" @submit.native.prevent>
                <el-form-item label="类型">
                  <el-select v-model="queryForm.bugType" clearable placeholder="全部" style="width: 180px;">
                    <el-option v-for="(label, key) in bugTypeOptions" :key="key" :label="label" :value="Number(key)" />
                  </el-select>
                </el-form-item>
                <el-form-item label="严重程度">
                  <el-select v-model="queryForm.severity" clearable placeholder="全部" style="width: 180px;">
                    <el-option v-for="(label, key) in severityOptions" :key="key" :label="label" :value="Number(key)" />
                  </el-select>
                </el-form-item>
                <el-form-item label="优先级">
                  <el-select v-model="queryForm.priority" clearable placeholder="全部" style="width: 180px;">
                    <el-option v-for="(label, key) in priorityOptions" :key="key" :label="label" :value="Number(key)" />
                  </el-select>
                </el-form-item>
                <el-form-item label="解决人">
                  <el-select
                    v-model="queryForm.resolvedBy"
                    filterable
                    clearable
                    placeholder="全部"
                    style="width: 180px;"
                    :disabled="!queryForm.projectId">
                    <el-option v-for="u in memberOptions" :key="'rb-' + u.id" :label="u.name" :value="u.id" />
                  </el-select>
                </el-form-item>
                <el-form-item label="复现率">
                  <el-select v-model="queryForm.reproduceRate" clearable placeholder="全部" style="width: 180px;">
                    <el-option v-for="(label, key) in reproduceRateOptions" :key="'rr-' + key" :label="label" :value="Number(key)" />
                  </el-select>
                </el-form-item>
                <el-form-item label="关键词">
                  <el-input v-model.trim="queryForm.keyword" clearable placeholder="标题/描述" style="width: 180px;" @keyup.enter.native="applyMoreFilters" />
                </el-form-item>
              </el-form>
              <div class="more-filter-footer">
                <el-button size="small" @click="moreFilterVisible = false">取消</el-button>
                <el-button type="primary" size="small" @click="applyMoreFilters">搜索</el-button>
              </div>
            </div>
            <el-button slot="reference" size="small">更多筛选</el-button>
          </el-popover>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
        <el-form-item class="bug-column-setting-item">
          <div class="bug-table-toolbar-actions">
            <el-button size="small" @click="fillCreatedByMe">由我创建的</el-button>
            <el-button size="small" @click="fillAssignedToMe">指派给我的</el-button>
            <el-popover v-model="columnSettingVisible" placement="bottom-end" width="300" trigger="click">
              <div class="column-setting-wrap">
                <div class="column-setting-title">自定义列表展示字段</div>
                <el-checkbox-group v-model="selectedBugColumnKeys" @change="handleBugColumnSelectionChange">
                  <el-checkbox v-for="item in allBugColumns" :key="item.key" :label="item.key">{{ item.label }}</el-checkbox>
                </el-checkbox-group>
              </div>
              <el-button slot="reference" size="small">自定义列表展示字段</el-button>
            </el-popover>
          </div>
        </el-form-item>
      </el-form>

      <el-table v-loading="loading" :data="tableData" border class="bug-table">
        <el-table-column
          v-for="column in visibleBugColumns"
          :key="column.key"
          :label="column.label"
          :min-width="column.minWidth"
          :width="column.width"
          :show-overflow-tooltip="column.key === 'title' || column.key === 'solution' || column.key === 'bugKey' || column.key === 'creator' || column.key === 'assignee' || column.key === 'resolvedBy' || column.key === 'reproduceRate'">
          <template slot-scope="scope">
            <template v-if="column.key === 'bugType'">
              <el-tag size="mini" :type="bugTypeTagType(scope.row.bug_type || scope.row.bugType)">{{ formatBugType(scope.row.bug_type || scope.row.bugType) }}</el-tag>
            </template>
            <template v-else-if="column.key === 'severity'">
              <el-tag size="mini" :type="severityTagType(scope.row.severity)">{{ formatSeverity(scope.row.severity) }}</el-tag>
            </template>
            <template v-else-if="column.key === 'priority'">
              <el-tag size="mini" :type="priorityTagType(scope.row.priority)">{{ formatPriority(scope.row.priority) }}</el-tag>
            </template>
            <template v-else-if="column.key === 'status'">
              <el-tag size="mini" :type="statusTagType(scope.row.status)">{{ formatStatus(scope.row.status) }}</el-tag>
            </template>
            <template v-else>
              {{ formatBugListCell(column.key, scope.row) }}
            </template>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="260" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" @click="goDetail(scope.row)">详情</el-button>
            <el-button type="text" @click="goEdit(scope.row)">编辑</el-button>
            <el-button type="text" @click="copyBug(scope.row)">复制</el-button>
            <el-button type="text" style="color: #F56C6C;" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pager">
        <el-pagination
          :current-page="pageNo"
          :page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange" />
      </div>
    </page-section>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { getBugList, deleteBug } from '@/api/bugApi'
import { recordBugHistory } from '@/utils/bugHistory'
import { getProductList } from '@/api/productApi'
import { getProjectList, getProjectMembers } from '@/api/projectApi'
import { getModuleTree } from '@/api/caseApi'
import {
  BUG_TYPE_MAP,
  SEVERITY_MAP,
  PRIORITY_MAP,
  STATUS_MAP,
  REPRODUCE_RATE_MAP,
  formatBugType,
  formatSeverity,
  formatPriority,
  formatStatus,
  formatReproduceRate,
  statusTagType,
  severityTagType,
  priorityTagType,
  bugTypeTagType
} from '@/utils/bugMaps'
import {
  readLastProductProjectCache,
  saveLastProductProjectCache,
  pickIdFromOptions
} from '@/utils/lastProductProjectCache'

/** 与 BugDetail 解决弹窗 solutionOptions 的 value 一致，用于列表展示 */
const BUG_SOLUTION_LABEL_MAP = {
  by_design: '设计如此',
  duplicate_bug: '重复Bug',
  external_reason: '外部原因',
  solution_resolved: '已解决',
  cannot_reproduce: '无法重现',
  deferred: '延期处理',
  wont_fix: '不予解决'
}

export default {
  name: 'BugList',
  components: { PageSection },
  data() {
    return {
      columnSettingVisible: false,
      moreFilterVisible: false,
      loading: false,
      productOptions: [],
      projectOptions: [],
      moduleTree: [],
      memberOptions: [],
      assigneeMap: {},
      queryForm: {
        productId: '',
        projectId: '',
        moduleId: '',
        bugType: '',
        severity: '',
        priority: '',
        status: '',
        assigneeId: '',
        reporterId: '',
        resolvedBy: '',
        reproduceRate: '',
        keyword: ''
      },
      allBugColumns: [
        { key: 'bugKey', label: '编号', width: 120 },
        { key: 'title', label: '标题', minWidth: 200 },
        { key: 'status', label: '状态', width: 100 },
        { key: 'assignee', label: '当前指派', width: 110 },
        { key: 'creator', label: '创建人', width: 110 },
        { key: 'resolvedBy', label: '解决人', width: 110 },
        { key: 'reproduceRate', label: '复现率', width: 100 },
        { key: 'solution', label: '解决方案', minWidth: 120 },
        { key: 'createdTime', label: '创建时间', width: 170 },
        { key: 'bugType', label: '类型', width: 100 },
        { key: 'severity', label: '严重程度', width: 100 },
        { key: 'priority', label: '优先级', width: 80 }
      ],
      selectedBugColumnKeys: ['bugKey', 'title', 'status', 'assignee', 'creator', 'solution', 'createdTime'],
      pageNo: 1,
      pageSize: 20,
      total: 0,
      tableData: []
    }
  },
  computed: {
    bugTypeOptions() {
      return BUG_TYPE_MAP
    },
    severityOptions() {
      return SEVERITY_MAP
    },
    priorityOptions() {
      return PRIORITY_MAP
    },
    statusOptions() {
      return STATUS_MAP
    },
    flatModules() {
      const out = []
      const walk = (nodes, prefix) => {
        ;(nodes || []).forEach(n => {
          const name = prefix ? `${prefix} / ${n.name}` : n.name
          out.push({ id: n.id, name })
          const ch = n.children || n.child_list || n.childList || []
          if (ch.length) walk(ch, name)
        })
      }
      walk(this.moduleTree, '')
      return out
    },
    currentUser() {
      return this.$store.state.currentUser
    },
    visibleBugColumns() {
      return this.allBugColumns.filter(item => this.selectedBugColumnKeys.includes(item.key))
    },
    reproduceRateOptions() {
      return REPRODUCE_RATE_MAP
    }
  },
  methods: {
    formatBugType,
    formatSeverity,
    formatPriority,
    formatStatus,
    formatReproduceRate,
    statusTagType,
    severityTagType,
    priorityTagType,
    bugTypeTagType,
    loadProductOptions() {
      if (this.productOptions.length) return Promise.resolve()
      return getProductList({ pageNo: 1, pageSize: 1000, status: 1 }).then(res => {
        const data = (res && res.data) || res || {}
        this.productOptions = data.items || data.list || data.data || []
      }).catch(() => { this.productOptions = [] })
    },
    restoreBugListFromCache() {
      const cached = readLastProductProjectCache()
      const q = this.$route.query || {}
      const fromAssignDeepLink = q.assignToMe === '1' || q.assignToMe === 'true'
      let pid = cached && cached.productId
      let projId = cached && cached.projectId
      if (fromAssignDeepLink) {
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
      this.queryForm.productId = pickIdFromOptions(this.productOptions, pid)
      return this.loadProjects(this.queryForm.productId).then(() => {
        const hasProject = (this.projectOptions || []).some(p => String(p.id) === String(projId))
        if (!hasProject) return
        this.queryForm.projectId = pickIdFromOptions(this.projectOptions, projId)
        return Promise.all([
          this.loadModules(this.queryForm.projectId),
          this.loadMembers(this.queryForm.projectId)
        ])
      })
    },
    loadProjects(productId) {
      if (!productId) {
        this.projectOptions = []
        return Promise.resolve()
      }
      return getProjectList({ pageNo: 1, pageSize: 1000, status: 1, productId }).then(res => {
        const data = (res && res.data) || res || {}
        this.projectOptions = data.items || data.list || data.data || []
      }).catch(() => { this.projectOptions = [] })
    },
    loadModules(projectId) {
      if (!projectId) {
        this.moduleTree = []
        return Promise.resolve()
      }
      return getModuleTree({ projectId, pageNo: 1, pageSize: 1000 }).then(res => {
        const data = (res && res.data) || res || {}
        this.moduleTree = data.list || data.items || []
      }).catch(() => { this.moduleTree = [] })
    },
    loadMembers(projectId) {
      if (!projectId) {
        this.memberOptions = []
        this.assigneeMap = {}
        return Promise.resolve()
      }
      return getProjectMembers(projectId, { pageNo: 1, pageSize: 1000 }).then(res => {
        const data = (res && res.data) || res || {}
        const list = data.items || data.list || data.data || data || []
        const arr = Array.isArray(list) ? list : []
        this.memberOptions = arr.map(item => ({
          id: item.user_id || item.userId || item.id,
          name:
            item.real_name ||
            item.realName ||
            item.username ||
            item.name ||
            item.user_name ||
            String(item.user_id || item.id)
        })).filter(u => u.id !== undefined && u.id !== null)
        this.assigneeMap = this.memberOptions.reduce((m, u) => { m[u.id] = u.name; return m }, {})
      }).catch(() => {
        this.memberOptions = []
        this.assigneeMap = {}
      })
    },
    rebuildAssigneeMap() {
      this.assigneeMap = (this.memberOptions || []).reduce((m, u) => {
        m[u.id] = u.name
        return m
      }, {})
    },
    mergeCurrentUserIntoMemberOptionsIfNeeded() {
      const u = this.currentUser
      if (!u || u.id == null || u.id === '') return
      const id = u.id
      if ((this.memberOptions || []).some(m => String(m.id) === String(id))) return
      const name = u.realName || u.username || '当前用户'
      this.memberOptions = [{ id, name }, ...(this.memberOptions || [])]
      this.rebuildAssigneeMap()
    },
    fillCreatedByMe() {
      const u = this.currentUser
      const uid = u && u.id != null && u.id !== '' ? u.id : null
      if (uid == null) {
        this.$message.warning('请先登录')
        return
      }
      if (!this.queryForm.projectId) {
        this.$message.warning('请先选择项目')
        return
      }
      this.mergeCurrentUserIntoMemberOptionsIfNeeded()
      this.queryForm.reporterId = uid
      this.pageNo = 1
      this.fetchList()
    },
    fillAssignedToMe() {
      const u = this.currentUser
      const uid = u && u.id != null && u.id !== '' ? u.id : null
      if (uid == null) {
        this.$message.warning('请先登录')
        return
      }
      if (!this.queryForm.projectId) {
        this.$message.warning('请先选择项目')
        return
      }
      this.mergeCurrentUserIntoMemberOptionsIfNeeded()
      this.queryForm.assigneeId = uid
      this.pageNo = 1
      this.fetchList()
    },
    onProductChange(val) {
      this.queryForm.projectId = ''
      this.queryForm.moduleId = ''
      this.queryForm.assigneeId = ''
      this.queryForm.reporterId = ''
      this.moduleTree = []
      this.memberOptions = []
      this.loadProjects(val)
    },
    onProjectChange(val) {
      this.queryForm.moduleId = ''
      this.queryForm.assigneeId = ''
      this.queryForm.reporterId = ''
      this.queryForm.resolvedBy = ''
      this.loadModules(val)
      this.loadMembers(val)
      if (val) {
        saveLastProductProjectCache(this.queryForm.productId, val)
      }
    },
    cleanParams(obj) {
      return Object.keys(obj).reduce((acc, k) => {
        const v = obj[k]
        if (v !== '' && v !== undefined && v !== null) acc[k] = v
        return acc
      }, {})
    },
    fetchList() {
      this.loading = true
      const params = this.cleanParams({
        productId: this.queryForm.productId,
        projectId: this.queryForm.projectId,
        moduleId: this.queryForm.moduleId,
        bugType: this.queryForm.bugType,
        severity: this.queryForm.severity,
        priority: this.queryForm.priority,
        status: this.queryForm.status,
        assigneeId: this.queryForm.assigneeId,
        reporterId: this.queryForm.reporterId,
        resolvedBy: this.queryForm.resolvedBy,
        reproduceRate: this.queryForm.reproduceRate,
        keyword: this.queryForm.keyword,
        pageNo: this.pageNo,
        pageSize: this.pageSize
      })
      getBugList(params).then(res => {
        const data = (res && res.data) || res || {}
        this.tableData = data.list || data.items || []
        this.total = Number(data.total || 0)
      }).catch(() => {
        this.tableData = []
        this.total = 0
      }).finally(() => { this.loading = false })
    },
    handleSearch() {
      this.pageNo = 1
      saveLastProductProjectCache(this.queryForm.productId, this.queryForm.projectId)
      this.fetchList()
    },
    applyMoreFilters() {
      this.moreFilterVisible = false
      this.pageNo = 1
      saveLastProductProjectCache(this.queryForm.productId, this.queryForm.projectId)
      this.fetchList()
    },
    resetQuery() {
      this.moreFilterVisible = false
      this.queryForm = {
        productId: '',
        projectId: '',
        moduleId: '',
        bugType: '',
        severity: '',
        priority: '',
        status: '',
        assigneeId: '',
        reporterId: '',
        resolvedBy: '',
        reproduceRate: '',
        keyword: ''
      }
      this.projectOptions = []
      this.moduleTree = []
      this.memberOptions = []
      this.pageNo = 1
      this.fetchList()
    },
    handleSizeChange(s) {
      this.pageSize = s
      this.pageNo = 1
      this.fetchList()
    },
    handleCurrentChange(p) {
      this.pageNo = p
      this.fetchList()
    },
    assigneeLabel(row) {
      const name = row.assignee_name || row.assigneeName
      if (name) return name
      const id = row.assignee_id || row.assigneeId
      if (this.assigneeMap[id]) return this.assigneeMap[id]
      if (id !== undefined && id !== null && id !== '') return String(id)
      return '-'
    },
    solutionLabel(row) {
      const d = row || {}
      const name = d.solution_name || d.solutionName || d.solution_label || d.solutionLabel
      if (name) return name
      const code = String(d.solution_type || d.solutionType || d.solution_code || d.solutionCode || '').trim()
      if (code && BUG_SOLUTION_LABEL_MAP[code]) return BUG_SOLUTION_LABEL_MAP[code]
      const sol = d.solution
      if (sol != null && sol !== '') {
        const s = String(sol).trim()
        if (BUG_SOLUTION_LABEL_MAP[s]) return BUG_SOLUTION_LABEL_MAP[s]
        return s
      }
      if (code) return code
      return '-'
    },
    formatBugListCell(key, row) {
      if (key === 'bugKey') return row.bug_key || row.bugKey || ''
      if (key === 'title') return row.title || ''
      if (key === 'assignee') return this.assigneeLabel(row)
      if (key === 'creator') return this.creatorLabel(row)
      if (key === 'solution') return this.solutionLabel(row)
      if (key === 'createdTime') return this.formatTime(row.created_time || row.createdTime)
      if (key === 'resolvedBy') return this.resolvedByLabel(row)
      if (key === 'reproduceRate') {
        return this.formatReproduceRate(row.reproduce_rate != null ? row.reproduce_rate : row.reproduceRate)
      }
      return ''
    },
    resolvedByLabel(row) {
      const d = row || {}
      const name =
        d.resolved_by_name ||
        d.resolvedByName ||
        d.resolver_name ||
        d.resolverName ||
        ''
      const id = d.resolved_by != null && d.resolved_by !== '' ? d.resolved_by : d.resolvedBy
      if (name) return name
      if (id !== undefined && id !== null && id !== '') {
        if (this.assigneeMap[id]) return this.assigneeMap[id]
        return String(id)
      }
      return '-'
    },
    handleBugColumnSelectionChange(value) {
      if (!value || value.length === 0) {
        this.$message.warning('至少保留一个展示字段')
        this.selectedBugColumnKeys = ['bugKey', 'title']
      }
    },
    creatorLabel(row) {
      const d = row || {}
      const name =
        d.reporter_real_name ||
        d.reporterRealName ||
        d.reporter_name ||
        d.reporterName ||
        d.creator_real_name ||
        d.creatorRealName ||
        d.creator_name ||
        d.creatorName ||
        ''
      const id = d.reporter_id || d.reporterId || d.creator_id || d.creatorId || d.created_by || d.createdBy
      if (name) return name
      if (id !== undefined && id !== null && id !== '') return String(id)
      return '-'
    },
    formatTime(v) {
      if (!v) return '-'
      return String(v).replace('T', ' ').slice(0, 19)
    },
    goCreate() {
      this.$router.push({ path: '/bug/create' })
    },
    goDetail(row) {
      this.$router.push({ path: '/bug/detail', query: { bugId: row.id } })
    },
    goEdit(row) {
      this.$router.push({ path: '/bug/edit', query: { bugId: row.id } })
    },
    copyBug(row) {
      const id = row && (row.id != null ? row.id : row.bugId)
      if (id === undefined || id === null || id === '') {
        this.$message.warning('无法复制：缺少 Bug ID')
        return
      }
      this.$router.push({ path: '/bug/create', query: { copyFrom: String(id) } })
    },
    handleDelete(row) {
      this.$confirm('确认删除该 Bug？', '提示', { type: 'warning' }).then(() => {
        const bid = row.id
        recordBugHistory(this.$store, {
          bugId: bid,
          fieldName: 'delete',
          oldValue: '0',
          newValue: '1'
        })
          .then(() => deleteBug({ bugId: bid, id: bid }))
          .then(() => {
            this.$message.success('已删除')
            this.fetchList()
          })
          .catch(() => {})
      }).catch(() => {})
    }
  },
  created() {
    this.loadProductOptions()
      .then(() => this.restoreBugListFromCache())
      .then(() => {
        const q = this.$route.query || {}
        if (q.assignToMe !== '1' && q.assignToMe !== 'true') return
        const u = this.currentUser
        const uid = u && u.id != null && u.id !== '' ? u.id : null
        if (uid == null) {
          this.$message.warning('请先登录')
          return
        }
        if (!this.queryForm.projectId) {
          this.$message.warning('请先在列表中选择产品、项目，或从首页在已选过产品/项目时再次进入')
          return
        }
        this.mergeCurrentUserIntoMemberOptionsIfNeeded()
        this.queryForm.assigneeId = uid
        this.pageNo = 1
      })
      .finally(() => this.fetchList())
  }
}
</script>

<style scoped>
.page-wrap {
  padding: 20px;
}
.filter-form {
  margin-bottom: 4px;
}

.filter-form::after {
  content: '';
  display: table;
  clear: both;
}

.bug-table-toolbar-actions {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.bug-table {
  margin-top: 8px;
}
.pager {
  margin-top: 16px;
  text-align: right;
}

.more-filter-wrap {
  padding: 4px 0;
}

.more-filter-footer {
  border-top: 1px solid #ebeef5;
  text-align: right;
  padding-top: 10px;
}

.bug-column-setting-item {
  float: right;
  margin-right: 0 !important;
}

.column-setting-wrap {
  max-height: 320px;
  overflow-y: auto;
}

.column-setting-title {
  color: #606266;
  font-weight: 500;
  margin-bottom: 8px;
}
</style>
