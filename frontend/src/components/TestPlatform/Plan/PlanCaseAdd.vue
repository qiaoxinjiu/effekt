<template>
  <div class="page-wrap">
    <page-section title="关联用例">
      <el-form :inline="true" size="small" @submit.native.prevent>
        <el-form-item label="产品名称">
          <el-input :value="productName" disabled style="width: 220px;"></el-input>
        </el-form-item>
        <el-form-item label="项目名称">
          <el-input :value="projectName" disabled style="width: 220px;"></el-input>
        </el-form-item>
        <el-form-item label="计划名称">
          <el-input :value="planName" disabled style="width: 220px;"></el-input>
        </el-form-item>
      </el-form>

      <div class="query-toolbar">
        <el-form :inline="true" :model="queryForm" size="small" class="query-toolbar-form" @submit.native.prevent>
          <el-form-item label="用例名称">
            <el-input v-model="queryForm.keyword" clearable style="width: 180px;"></el-input>
          </el-form-item>
          <el-form-item label="模块名称">
            <el-input v-model="queryForm.moduleName" clearable style="width: 160px;"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="fetchCases">查询</el-button>
          </el-form-item>
        </el-form>
        <div class="query-toolbar-actions">
          <el-button size="small" @click="goBack">返回</el-button>
          <el-button type="primary" size="small" :loading="submitting" @click="submitAssociate">关联用例</el-button>
        </div>
      </div>

      <el-table
        ref="caseTable"
        v-loading="loading"
        :data="tableData"
        border
        style="margin-top: 12px;"
        @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="52"></el-table-column>
        <el-table-column label="模块名称" min-width="160">
          <template slot-scope="scope">{{ scope.row.module_name || '-' }}</template>
        </el-table-column>
        <el-table-column prop="case_key" label="用例编号" min-width="130"></el-table-column>
        <el-table-column prop="title" label="用例名称" min-width="220"></el-table-column>
        <el-table-column label="优先级" width="90">
          <template slot-scope="scope">{{ formatPriority(scope.row.priority) }}</template>
        </el-table-column>
        <el-table-column label="是否已关联计划" width="130">
          <template slot-scope="scope">
            <el-tag size="mini" :type="isCaseAssociated(scope.row.id) ? 'success' : 'info'">
              {{ isCaseAssociated(scope.row.id) ? '已关联' : '未关联' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

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
import { getCaseList } from '@/api/caseApi'
import { addPlanCases, getPlanCaseList, getPlanDetail } from '@/api/planApi'

export default {
  name: 'PlanCaseAdd',
  components: { PageSection },
  data() {
    return {
      loading: false,
      submitting: false,
      pageNo: 1,
      pageSize: 20,
      total: 0,
      tableData: [],
      selectedRows: [],
      associatedCaseIdMap: {},
      /** 自动化测试计划（is_auto=1）：用例列表只按是否实现自动化过滤，不按评审通过状态过滤 */
      planIsAutomation: false,
      queryForm: {
        keyword: '',
        moduleName: ''
      },
      ownerId: this.$route.query.ownerId || ''
    }
  },
  computed: {
    projectId() {
      return this.$route.query.projectId || ''
    },
    planId() {
      return this.$route.query.planId || ''
    },
    productName() {
      return this.$route.query.productName || ''
    },
    projectName() {
      return this.$route.query.projectName || ''
    },
    planName() {
      return this.$route.query.planName || ''
    }
  },
  methods: {
    loadAssociatedCaseIds() {
      if (!this.projectId || !this.planId) {
        this.associatedCaseIdMap = {}
        return Promise.resolve()
      }
      return getPlanCaseList(this.projectId, this.planId, {
        pageNo: 1,
        pageSize: 2000
      }).then(res => {
        const data = (res && res.data) || res || {}
        const list = data.list || data.items || []
        this.associatedCaseIdMap = (Array.isArray(list) ? list : []).reduce((map, item) => {
          const caseId = item.case_id || item.caseId || (item.case && item.case.id) || (item.case && item.case.case_id)
          if (caseId !== undefined && caseId !== null && caseId !== '') {
            map[caseId] = true
          }
          return map
        }, {})
      }).catch(() => {
        this.associatedCaseIdMap = {}
      })
    },
    fetchCases() {
      if (!this.projectId) {
        this.tableData = []
        this.total = 0
        return
      }
      this.loading = true
      const params = {
        keyword: this.queryForm.keyword || undefined,
        module_name: this.queryForm.moduleName || undefined,
        pageNo: this.pageNo,
        pageSize: this.pageSize
      }
      if (this.planIsAutomation) {
        params.isAuto = 1
      } else {
        params.status = 4
      }
      Promise.all([this.loadAssociatedCaseIds(), getCaseList(this.projectId, params)]).then(([, res]) => {
        const data = (res && res.data) || res || {}
        const list = data.list || data.items || []
        this.tableData = Array.isArray(list) ? list : []
        this.total = Number(data.total || this.tableData.length || 0)
        this.$nextTick(() => {
          this.$refs.caseTable && this.$refs.caseTable.clearSelection()
        })
        this.selectedRows = []
      }).catch(() => {
        this.tableData = []
        this.total = 0
      }).finally(() => {
        this.loading = false
      })
    },
    isCaseAssociated(caseId) {
      return !!this.associatedCaseIdMap[caseId]
    },
    /** 拉计划详情：负责人 + 是否自动化测试计划（关联用例列表筛选依赖） */
    loadPlanContext() {
      if (!this.projectId || !this.planId) {
        return Promise.resolve()
      }
      return getPlanDetail(this.projectId, this.planId).then(res => {
        const raw = (res && res.data) || res || {}
        const inner = raw.plan || raw.detail
        const data = inner && typeof inner === 'object' ? Object.assign({}, raw, inner) : raw
        if (!this.ownerId) {
          this.ownerId = data.owner_id || data.ownerId || ''
        }
        const autoRaw = data.isAuto !== undefined && data.isAuto !== null ? data.isAuto : data.is_auto
        this.planIsAutomation = autoRaw === 1 || autoRaw === true || autoRaw === '1'
      }).catch(() => {})
    },
    handleSelectionChange(rows) {
      this.selectedRows = rows || []
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.pageNo = 1
      this.fetchCases()
    },
    handleCurrentChange(page) {
      this.pageNo = page
      this.fetchCases()
    },
    formatPriority(value) {
      const map = { 0: 'P0', 1: 'P1', 2: 'P2', 3: 'P3' }
      return map[value] || value
    },
    submitAssociate() {
      if (!this.planId) {
        this.$message.warning('缺少计划ID')
        return
      }
      if (!this.ownerId) {
        this.$message.warning('缺少负责人信息，无法关联')
        return
      }
      const caseIds = this.selectedRows.map(item => item.id).filter(Boolean)
      if (caseIds.length === 0) {
        this.$message.warning('请先选择要关联的用例')
        return
      }
      this.submitting = true
      addPlanCases(this.projectId, this.planId, {
        planId: Number(this.planId),
        caseIds,
        assigneeId: Number(this.ownerId),
        roundNo: 1
      }).then(() => {
        this.$message.success('关联用例成功')
        this.goBack()
      }).finally(() => {
        this.submitting = false
      })
    },
    goBack() {
      this.$router.push({
        path: '/test-platform/plan',
        query: {
          productId: this.$route.query.productId || undefined,
          projectId: this.projectId || undefined
        }
      })
    }
  },
  created() {
    this.loadPlanContext().finally(() => {
      this.fetchCases()
    })
  }
}
</script>

<style scoped>
.page-wrap {
  padding: 20px;
}

.query-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-top: 8px;
}

.query-toolbar-form {
  flex: 1;
  min-width: 0;
}

.query-toolbar-actions {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding-top: 4px;
}
</style>
