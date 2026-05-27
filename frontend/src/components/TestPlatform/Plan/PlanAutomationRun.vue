<template>
  <div class="page-wrap">
    <page-section title="计划自动化执行">
      <div class="filter-toolbar">
        <el-form :inline="true" size="small" class="filter-toolbar-form" @submit.native.prevent>
          <el-form-item label="产品">
            <el-input :value="productName" disabled style="width: 200px;" />
          </el-form-item>
          <el-form-item label="项目">
            <el-input :value="projectName" disabled style="width: 200px;" />
          </el-form-item>
          <el-form-item label="计划">
            <div class="plan-title-row">
              <el-input :value="planNameDisplay" disabled class="plan-name-input" />
              <template v-if="planJenkinsUrl">
                <span class="plan-jenkins-sep">·</span>
                <el-link
                  :href="planJenkinsUrl"
                  :title="planJenkinsUrl"
                  target="_blank"
                  type="primary"
                  class="plan-jenkins-link">
                  自动化执行 Jenkins
                </el-link>
              </template>
            </div>
          </el-form-item>
        </el-form>
        <div class="filter-toolbar-actions">
          <el-button size="small" @click="goExecutionResultList">执行结果列表</el-button>
          <el-button size="small" @click="goBack">返回</el-button>
        </div>
      </div>

      <el-card v-if="!executionId" class="run-card" shadow="never">
        <el-form ref="runFormRef" :model="runForm" :rules="runRules" label-width="108px" size="small">
          <el-form-item label="执行环境" prop="envCode">
            <el-select v-model="runForm.envCode" placeholder="请选择环境编码" filterable style="width: 280px;">
              <el-option
                v-for="opt in envOptions"
                :key="'env-' + opt.value"
                :label="opt.label"
                :value="opt.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="执行模式">
            <el-radio-group v-model="runForm.runMode">
              <el-radio :label="1">串行</el-radio>
              <el-radio :label="2">并行</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="计划轮次">
            <el-input-number v-model="runForm.roundNo" :min="1" :step="1" controls-position="right" placeholder="可选" />
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model.trim="runForm.remark" maxlength="200" show-word-limit style="width: 420px;" placeholder="可选" />
          </el-form-item>
        </el-form>

        <div class="table-toolbar">
          <span class="hint">勾选后点击「执行已选用例」将传 caseIds；翻页会保留已勾选项。不勾选可「执行计划内全部自动化用例」。</span>
          <el-button size="small" :loading="casesLoading" @click="refreshPlanCaseList">刷新用例列表</el-button>
        </div>

        <el-table
          ref="caseTable"
          v-loading="casesLoading"
          :data="planCaseRows"
          border
          row-key="planCaseId"
          @selection-change="onSelectionChange">
          <el-table-column type="selection" width="48" :reserve-selection="true" />
          <el-table-column prop="caseKey" label="用例编号" min-width="120" />
          <el-table-column prop="caseTitle" label="用例名称" min-width="200" />
          <el-table-column label="自动化" width="88">
            <template slot-scope="scope">{{ formatAuto(scope.row) }}</template>
          </el-table-column>
        </el-table>

        <el-pagination
          class="plan-case-pager"
          background
          layout="total, sizes, prev, pager, next, jumper"
          :current-page="planCasePageNo"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="planCasePageSize"
          :total="planCaseTotal"
          @size-change="handlePlanCaseSizeChange"
          @current-change="handlePlanCaseCurrentChange" />

        <div class="run-actions">
          <el-button type="primary" :loading="runSubmitting" @click="submitRun(true)">执行计划内全部自动化用例</el-button>
          <el-button type="success" :loading="runSubmitting" :disabled="!selectedRows.length" @click="submitRun(false)">
            执行已选用例（{{ selectedRows.length }}）
          </el-button>
        </div>
      </el-card>

      <template v-else>
        <el-card class="exec-card" shadow="never">
          <div class="exec-head">
            <div>
              <span class="exec-no">{{ executionSummary.execution_no || executionSummary.executionNo || '-' }}</span>
              <el-tag size="small" class="exec-tag" :type="mainStatusTag(executionSummary.status)">
                {{ mainStatusLabel(executionSummary.status) }}
              </el-tag>
            </div>
            <div class="exec-actions">
              <el-button size="small" :loading="detailLoading" @click="refreshExecution">刷新</el-button>
              <el-button size="small" @click="resetRunAnother">再跑一轮</el-button>
            </div>
          </div>
          <div class="exec-desc">
            <el-row :gutter="12" type="flex" class="exec-desc-row">
              <el-col :span="12">
                <div class="exec-desc-item"><span class="exec-desc-label">环境</span>{{ executionSummary.env_code || executionSummary.envCode || '-' }}</div>
              </el-col>
              <el-col :span="12">
                <div class="exec-desc-item"><span class="exec-desc-label">模式</span>{{ (executionSummary.run_mode || executionSummary.runMode) === 2 ? '并行' : '串行' }}</div>
              </el-col>
            </el-row>
            <el-row :gutter="12" type="flex" class="exec-desc-row">
              <el-col :span="12">
                <div class="exec-desc-item"><span class="exec-desc-label">总数</span>{{ pickCount(executionSummary, 'total_count', 'totalCount') }}</div>
              </el-col>
              <el-col :span="12">
                <div class="exec-desc-item">
                  <span class="exec-desc-label">通过 / 失败</span>
                  {{ pickCount(executionSummary, 'passed_count', 'passedCount') }} /
                  {{ pickCount(executionSummary, 'failed_count', 'failedCount') }}
                </div>
              </el-col>
            </el-row>
            <div class="exec-desc-item exec-desc-block">
              <span class="exec-desc-label">Jenkins</span>
              <el-link v-if="jenkinsLink" :href="jenkinsLink" target="_blank" type="primary">{{ jenkinsLink }}</el-link>
              <span v-else>-</span>
            </div>
            <div class="exec-desc-item exec-desc-block">
              <span class="exec-desc-label">控制台</span>
              <el-link v-if="consoleLink" :href="consoleLink" target="_blank" type="primary">打开</el-link>
              <span v-else>-</span>
            </div>
            <div class="exec-desc-item exec-desc-block">
              <span class="exec-desc-label">报告</span>
              <el-link v-if="reportLink" :href="reportLink" target="_blank" type="primary">打开</el-link>
              <span v-else>-</span>
            </div>
          </div>
          <div v-if="polling" class="poll-hint">执行中，每 5 秒自动刷新状态…</div>
        </el-card>

        <el-card class="case-list-card" shadow="never">
          <div slot="header" class="card-header">执行明细</div>
          <el-table v-loading="caseListLoading" :data="executionCaseRows" border max-height="420">
            <el-table-column prop="run_order" label="#" width="56">
              <template slot-scope="scope">{{ scope.row.run_order != null ? scope.row.run_order : scope.row.runOrder }}</template>
            </el-table-column>
            <el-table-column prop="case_key" label="编号" min-width="100">
              <template slot-scope="scope">{{ scope.row.case_key || scope.row.caseKey }}</template>
            </el-table-column>
            <el-table-column prop="case_title" label="标题" min-width="160">
              <template slot-scope="scope">{{ scope.row.case_title || scope.row.caseTitle }}</template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template slot-scope="scope">
                <el-tag size="mini" :type="caseStatusTag(scope.row.status)">{{ caseStatusLabel(scope.row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="result_message" label="结果" min-width="120" show-overflow-tooltip>
              <template slot-scope="scope">{{ scope.row.result_message || scope.row.resultMessage || '-' }}</template>
            </el-table-column>
            <el-table-column label="耗时(s)" width="88">
              <template slot-scope="scope">{{ scope.row.duration_seconds != null ? scope.row.duration_seconds : scope.row.durationSeconds }}</template>
            </el-table-column>
          </el-table>
          <el-pagination
            class="case-pager"
            background
            layout="total, sizes, prev, pager, next, jumper"
            :page-sizes="[20, 50, 100, 200]"
            :page-size="casePageSize"
            :current-page="casePageNo"
            :total="caseListTotal"
            @size-change="handleCaseListSizeChange"
            @current-change="handleCasePageChange" />
        </el-card>
      </template>
    </page-section>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { getPlanCaseList } from '@/api/planApi'
import { getProjectEnvironments } from '@/api/projectApi'
import {
  getAutomationExecutionCaseList,
  getAutomationExecutionDetail,
  postAutomationExecutionPoll,
  runAutomationPlan
} from '@/api/automationApi'

const MAIN_STATUS_LABELS = {
  0: '待触发',
  1: '触发中',
  2: '排队中',
  3: '执行中',
  4: '成功',
  5: '失败',
  6: '已取消',
  7: '触发失败',
  8: '回调异常'
}

const CASE_STATUS_LABELS = {
  0: '待执行',
  1: '执行中',
  2: '通过',
  3: '失败',
  4: '阻塞',
  5: '跳过',
  6: '未找到',
  7: '已取消'
}

/** 主单终态：文档 4~8 */
const MAIN_TERMINAL = new Set([4, 5, 6, 7, 8])

function pickEnvCode(item) {
  if (!item) return ''
  const c = item.code || item.env_code || item.envCode
  if (c != null && String(c).trim() !== '') return String(c).trim()
  const name = (item.name || '').trim()
  if (name) return name
  if (item.id != null) return String(item.id)
  return ''
}

export default {
  name: 'PlanAutomationRun',
  components: { PageSection },
  data() {
    return {
      projectId: this.$route.query.projectId || '',
      planId: this.$route.query.planId || '',
      routeEnvId: this.$route.query.environmentId || '',
      casesLoading: false,
      planCaseRows: [],
      planCasePageNo: 1,
      planCasePageSize: 10,
      planCaseTotal: 0,
      selectedRows: [],
      envOptions: [],
      runForm: {
        envCode: '',
        runMode: 1,
        roundNo: null,
        remark: ''
      },
      runRules: {
        envCode: [{ required: true, message: '请选择执行环境', trigger: 'change' }]
      },
      runSubmitting: false,
      executionId: null,
      executionSummary: {},
      executionCaseRows: [],
      caseListLoading: false,
      caseListTotal: 0,
      casePageNo: 1,
      casePageSize: 50,
      detailLoading: false,
      pollTimer: null,
      polling: false
    }
  },
  computed: {
    productName() {
      return this.$route.query.productName || ''
    },
    projectName() {
      return this.$route.query.projectName || ''
    },
    planNameDisplay() {
      return this.$route.query.planName || ''
    },
    /** 与计划列表入口一致，由路由 query 传入（计划级 jenkins_url） */
    planJenkinsUrl() {
      const q = this.$route.query || {}
      const raw = q.jenkinsUrl != null && String(q.jenkinsUrl).trim() !== '' ? q.jenkinsUrl : q.jenkins_url
      if (raw == null || String(raw).trim() === '') return ''
      return String(raw).trim()
    },
    jenkinsLink() {
      const e = this.executionSummary
      return e.jenkins_build_url || e.jenkinsBuildUrl || ''
    },
    consoleLink() {
      const e = this.executionSummary
      return e.console_url || e.consoleUrl || ''
    },
    reportLink() {
      const e = this.executionSummary
      return e.report_url || e.reportUrl || ''
    }
  },
  watch: {
    '$route.query': {
      handler() {
        this.projectId = this.$route.query.projectId || ''
        this.planId = this.$route.query.planId || ''
        this.routeEnvId = this.$route.query.environmentId || ''
        this.applyRouteExecutionContext()
      },
      deep: true
    }
  },
  created() {
    this.bootstrap()
  },
  beforeDestroy() {
    this.stopPolling()
  },
  methods: {
    /** 兼容下划线 / 驼峰；0 为有效计数（Vue2 模板不支持 ??） */
    pickCount(row, snakeKey, camelKey) {
      const o = row || {}
      const a = o[snakeKey]
      if (a != null && a !== '') return a
      const b = o[camelKey]
      if (b != null && b !== '') return b
      return '-'
    },
    parseRouteExecutionId() {
      const q = this.$route.query || {}
      const raw = q.executionId != null && q.executionId !== '' ? q.executionId : q.execution_id
      if (raw === '' || raw === undefined || raw === null) return null
      const n = Number(raw)
      return Number.isNaN(n) ? null : n
    },
    /** 与路由同步：带 executionId 则进入执行详情；去掉则回到选例执行 */
    applyRouteExecutionContext() {
      const exId = this.parseRouteExecutionId()
      if (exId != null) {
        if (this.executionId !== exId) {
          this.stopPolling()
          this.executionId = exId
          this.loadEnvironments().then(() => this.applyDefaultEnvFromRoute())
          return this.refreshExecution().then(() => this.startPollingIfNeeded())
        }
        return Promise.resolve()
      }
      if (this.executionId != null) {
        this.resetRunAnother()
      }
      return Promise.resolve()
    },
    syncRouteExecutionId(id) {
      if (id == null) return
      const q = Object.assign({}, this.$route.query || {}, { executionId: id })
      this.$router.replace({ path: '/test-platform/plan/automation', query: q }).catch(() => {})
    },
    bootstrap() {
      const exId = this.parseRouteExecutionId()
      if (exId != null) {
        this.executionId = exId
        this.loadEnvironments().then(() => {
          this.applyDefaultEnvFromRoute()
        })
        return this.refreshExecution().then(() => this.startPollingIfNeeded())
      }
      this.executionId = null
      return this.loadEnvironments().then(() => {
        this.applyDefaultEnvFromRoute()
        this.fetchPlanCases()
      })
    },
    loadEnvironments() {
      const pid = Number(this.projectId)
      if (!pid || Number.isNaN(pid)) {
        this.envOptions = []
        return Promise.resolve()
      }
      return getProjectEnvironments(pid, { pageNo: 1, pageSize: 1000 })
        .then(res => {
          const data = (res && res.data) || res || {}
          const list = data.items || data.list || data.data || []
          this.envOptions = (Array.isArray(list) ? list : []).map(item => {
            const value = pickEnvCode(item)
            const labelName = (item.name || value || '').trim() || value
            return {
              value,
              label: value && labelName !== value ? `${labelName}（${value}）` : labelName,
              raw: item
            }
          }).filter(o => o.value)
        })
        .catch(() => {
          this.envOptions = []
        })
    },
    applyDefaultEnvFromRoute() {
      const eid = this.routeEnvId
      if (!eid || !this.envOptions.length) return
      const found = this.envOptions.find(
        o => o.raw && String(o.raw.id) === String(eid)
      )
      if (found && found.value) {
        this.runForm.envCode = found.value
      }
    },
    fetchPlanCases() {
      if (!this.planId || !this.projectId) {
        this.planCaseRows = []
        this.planCaseTotal = 0
        return
      }
      this.casesLoading = true
      getPlanCaseList(this.projectId, this.planId, {
        pageNo: this.planCasePageNo,
        pageSize: this.planCasePageSize
      })
        .then(listRes => {
          const data = (listRes && listRes.data) || listRes || {}
          const list = data.list || data.items || []
          this.planCaseTotal = Number(data.total != null ? data.total : (Array.isArray(list) ? list.length : 0))
          this.planCaseRows = (Array.isArray(list) ? list : []).map(item => ({
            planCaseId: item.id,
            caseId: item.case_id != null ? item.case_id : item.caseId,
            caseKey: item.case_key || item.caseKey || '',
            caseTitle: item.case_title || item.caseTitle || item.title || '',
            isAuto: item.is_auto != null ? item.is_auto : item.isAuto
          }))
        })
        .catch(() => {
          this.planCaseRows = []
          this.planCaseTotal = 0
        })
        .finally(() => {
          this.casesLoading = false
        })
    },
    refreshPlanCaseList() {
      this.planCasePageNo = 1
      this.fetchPlanCases()
    },
    handlePlanCaseSizeChange(size) {
      this.planCasePageSize = size
      this.planCasePageNo = 1
      this.fetchPlanCases()
    },
    handlePlanCaseCurrentChange(page) {
      this.planCasePageNo = page
      this.fetchPlanCases()
    },
    onSelectionChange(rows) {
      this.selectedRows = rows || []
    },
    formatAuto(row) {
      const v = row && row.isAuto
      if (v === 1 || v === true || v === '1') return '是'
      if (v === 0 || v === false || v === '0') return '否'
      return '-'
    },
    submitRun(runAll) {
      if (!this.$refs.runFormRef) return
      this.$refs.runFormRef.validate(valid => {
        if (!valid) return
        const planId = Number(this.planId)
        if (!planId || Number.isNaN(planId)) {
          this.$message.warning('计划 ID 无效')
          return
        }
        if (!runAll && (!this.selectedRows || !this.selectedRows.length)) {
          this.$message.warning('请先勾选要执行的用例')
          return
        }
        const payload = {
          planId,
          envCode: this.runForm.envCode,
          runMode: this.runForm.runMode || 1
        }
        const rn = this.runForm.roundNo
        if (rn != null && rn !== '' && !Number.isNaN(Number(rn))) {
          payload.roundNo = Number(rn)
        }
        if (this.runForm.remark) {
          payload.remark = this.runForm.remark
        }
        if (!runAll) {
          const ids = this.selectedRows.map(r => Number(r.caseId)).filter(id => !Number.isNaN(id))
          if (!ids.length) {
            this.$message.warning('勾选用例缺少 caseId')
            return
          }
          payload.caseIds = ids
        }
        this.runSubmitting = true
        runAutomationPlan(payload)
          .then(res => {
            const body = (res && res.data) || res || {}
            const id = body.id
            if (id == null) {
              this.$message.error('未返回 execution id')
              return
            }
            this.$message.success((res && res.msg) || (res && res.message) || '已提交自动化执行')
            this.executionId = id
            this.executionSummary = body
            this.casePageNo = 1
            this.refreshExecution().then(() => {
              this.startPollingIfNeeded()
              this.syncRouteExecutionId(id)
            })
          })
          .catch(() => {})
          .finally(() => {
            this.runSubmitting = false
          })
      })
    },
    refreshExecution() {
      if (!this.executionId) return Promise.resolve()
      this.detailLoading = true
      const d1 = getAutomationExecutionDetail(this.executionId)
        .then(res => {
          const data = (res && res.data) || res || {}
          this.executionSummary = data && typeof data === 'object' ? data : {}
        })
        .catch(() => {})
      const d2 = this.loadExecutionCasePage()
      return Promise.all([d1, d2]).finally(() => {
        this.detailLoading = false
      })
    },
    loadExecutionCasePage() {
      if (!this.executionId) return Promise.resolve()
      this.caseListLoading = true
      return getAutomationExecutionCaseList({
        executionId: this.executionId,
        pageNo: this.casePageNo,
        pageSize: this.casePageSize
      })
        .then(res => {
          const data = (res && res.data) || res || {}
          const list = data.list || data.items || []
          this.executionCaseRows = Array.isArray(list) ? list : []
          this.caseListTotal = Number(data.total != null ? data.total : this.executionCaseRows.length)
        })
        .catch(() => {
          this.executionCaseRows = []
          this.caseListTotal = 0
        })
        .finally(() => {
          this.caseListLoading = false
        })
    },
    handleCasePageChange(p) {
      this.casePageNo = p
      this.loadExecutionCasePage()
    },
    handleCaseListSizeChange(size) {
      this.casePageSize = size
      this.casePageNo = 1
      this.loadExecutionCasePage()
    },
    mainStatusLabel(s) {
      return MAIN_STATUS_LABELS[s] != null ? MAIN_STATUS_LABELS[s] : s == null ? '-' : String(s)
    },
    mainStatusTag(s) {
      const map = { 0: 'info', 1: 'warning', 2: 'warning', 3: 'primary', 4: 'success', 5: 'danger', 6: 'info', 7: 'danger', 8: 'danger' }
      return map[s] || 'info'
    },
    caseStatusLabel(s) {
      return CASE_STATUS_LABELS[s] != null ? CASE_STATUS_LABELS[s] : s == null ? '-' : String(s)
    },
    caseStatusTag(s) {
      const map = { 0: 'info', 1: 'warning', 2: 'success', 3: 'danger', 4: 'warning', 5: 'info', 6: 'info', 7: 'info' }
      return map[s] || 'info'
    },
    isTerminalMainStatus(s) {
      return s != null && MAIN_TERMINAL.has(Number(s))
    },
    /** 与执行结果列表页 poll 一致：合并返回字段到主单摘要 */
    mergePollIntoExecutionSummary(d) {
      if (!d || typeof d !== 'object') return
      const next = Object.assign({}, this.executionSummary)
      if (d.status !== undefined && d.status !== null) next.status = d.status
      const setUrlPair = (snake, camel) => {
        if (d[snake] != null && String(d[snake]).trim() !== '') next[snake] = d[snake]
        if (d[camel] != null && String(d[camel]).trim() !== '') next[camel] = d[camel]
      }
      setUrlPair('report_url', 'reportUrl')
      setUrlPair('console_url', 'consoleUrl')
      setUrlPair('jenkins_build_url', 'jenkinsBuildUrl')
      if (d.jenkins_build_number != null || d.jenkinsBuildNumber != null) {
        const n = d.jenkins_build_number != null ? d.jenkins_build_number : d.jenkinsBuildNumber
        next.jenkins_build_number = n
        next.jenkinsBuildNumber = n
      }
      if (d.end_time != null && String(d.end_time).trim() !== '') next.end_time = d.end_time
      if (d.endTime != null && String(d.endTime).trim() !== '') next.endTime = d.endTime
      if (d.duration_seconds != null || d.durationSeconds != null) {
        const sec = d.duration_seconds != null ? d.duration_seconds : d.durationSeconds
        next.duration_seconds = sec
        next.durationSeconds = sec
      }
      if (d.id != null) next.id = d.id
      this.executionSummary = next
    },
    /** 仅轮询 poll 更新主单；不轮询执行明细列表（与执行结果列表页一致） */
    startPollingIfNeeded() {
      this.stopPolling()
      const s = this.executionSummary && this.executionSummary.status
      if (this.isTerminalMainStatus(s)) {
        this.polling = false
        return
      }
      if (!this.executionId) {
        this.polling = false
        return
      }
      this.polling = true
      const tick = () => {
        postAutomationExecutionPoll({ executionId: this.executionId })
          .then(res => {
            if (!res || res.code !== 20000) return
            const d = res.data
            if (!d || typeof d !== 'object') return
            this.mergePollIntoExecutionSummary(d)
            if (this.isTerminalMainStatus(this.executionSummary.status)) {
              this.stopPolling()
              this.loadExecutionCasePage()
            }
          })
          .catch(() => {})
      }
      tick()
      this.pollTimer = window.setInterval(tick, 5000)
    },
    stopPolling() {
      if (this.pollTimer != null) {
        clearInterval(this.pollTimer)
        this.pollTimer = null
      }
      this.polling = false
    },
    resetRunAnother() {
      this.stopPolling()
      this.executionId = null
      this.executionSummary = {}
      this.executionCaseRows = []
      this.caseListTotal = 0
      this.casePageNo = 1
      this.planCasePageNo = 1
      if (this.$refs.caseTable) {
        this.$refs.caseTable.clearSelection()
      }
      this.selectedRows = []
      const q = Object.assign({}, this.$route.query || {})
      delete q.executionId
      delete q.execution_id
      this.$router.replace({ path: '/test-platform/plan/automation', query: q }).catch(() => {})
      this.fetchPlanCases()
    },
    goExecutionResultList() {
      const q = this.$route.query || {}
      this.$router.push({
        path: '/test-platform/plan/automation/executions',
        query: {
          productId: q.productId || undefined,
          productName: q.productName || '',
          projectId: this.projectId || undefined,
          projectName: q.projectName || '',
          planId: this.planId || undefined,
          planName: this.planNameDisplay || q.planName || '',
          environmentId: q.environmentId || undefined,
          jenkinsUrl: q.jenkinsUrl || undefined
        }
      })
    },
    goBack() {
      this.stopPolling()
      this.$router.push({
        path: '/test-platform/plan',
        query: {
          productId: this.$route.query.productId || undefined,
          projectId: this.projectId || undefined
        }
      })
    }
  }
}
</script>

<style scoped>
.page-wrap {
  padding: 20px;
}

.filter-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.filter-toolbar-form {
  flex: 1;
  min-width: 0;
}

.plan-title-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  max-width: 560px;
}

.plan-name-input {
  width: 220px;
  flex-shrink: 0;
}

.plan-jenkins-sep {
  color: #c0c4cc;
  user-select: none;
}

.plan-jenkins-link {
  flex-shrink: 0;
}

.filter-toolbar-actions {
  flex-shrink: 0;
  padding-top: 4px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.run-card,
.exec-card,
.case-list-card {
  margin-top: 12px;
}

.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 12px 0 8px;
  gap: 12px;
}

.hint {
  font-size: 12px;
  color: #909399;
}

.run-actions {
  margin-top: 16px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.exec-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.exec-no {
  font-weight: 600;
  margin-right: 8px;
}

.exec-tag {
  vertical-align: middle;
}

.exec-actions {
  display: flex;
  gap: 8px;
}

.exec-desc {
  margin-top: 8px;
  padding: 12px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background: #fafafa;
}

.exec-desc-row {
  margin-bottom: 8px;
}

.exec-desc-item {
  font-size: 13px;
  color: #606266;
  line-height: 1.6;
}

.exec-desc-block {
  margin-top: 6px;
}

.exec-desc-label {
  display: inline-block;
  min-width: 88px;
  margin-right: 8px;
  color: #909399;
  font-weight: 500;
}

.poll-hint {
  margin-top: 10px;
  font-size: 12px;
  color: #909399;
}

.card-header {
  font-weight: 600;
}

.plan-case-pager {
  margin-top: 12px;
  text-align: right;
}

.case-pager {
  margin-top: 12px;
  text-align: right;
}
</style>
