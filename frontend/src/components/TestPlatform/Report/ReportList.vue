<template>
  <div class="page-wrap">
    <page-section title="测试报告">
      <template slot="extra">
        <el-button type="primary" size="small" :loading="generating" @click="handleGenerate">生成报告</el-button>
      </template>
      <el-form :inline="true" :model="queryForm" size="small" @submit.native.prevent>
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
        <el-form-item label="计划名称">
          <el-select
            v-model="queryForm.plan_id"
            filterable
            clearable
            placeholder="请选择计划"
            style="width: 260px;"
            :disabled="!selectedProjectId"
            @focus="loadPlanOptions">
            <el-option
              v-for="item in planOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :disabled="!selectedProjectId" @click="fetchList">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
      <el-table v-loading="loading" :data="tableData" border style="margin-top: 16px;">
        <el-table-column prop="name" label="报告名称" min-width="180"></el-table-column>
        <el-table-column label="计划名称" min-width="180">
          <template slot-scope="scope">{{ formatPlanName(scope.row) }}</template>
        </el-table-column>
        <el-table-column label="类型" width="120">
          <template slot-scope="scope">{{ formatReportType(scope.row.report_type || scope.row.type) }}</template>
        </el-table-column>
        <el-table-column label="生成时间" min-width="180">
          <template slot-scope="scope">{{ formatDateTime(scope.row.generated_time || scope.row.generated_at || scope.row.created_at || scope.row.create_time) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template slot-scope="scope">
            <el-button type="text" @click="goViewer(scope.row)">查看链接</el-button>
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
import { getPlanList } from '@/api/planApi'
import { getProductList } from '@/api/productApi'
import { getProjectDetail, getProjectList } from '@/api/projectApi'
import { generateReport, getReportList } from '@/api/reportApi'
import {
  readLastProductProjectCache,
  saveLastProductProjectCache,
  pickIdFromOptions
} from '@/utils/lastProductProjectCache'

export default {
  name: 'ReportList',
  components: { PageSection },
  data() {
    return {
      loading: false,
      generating: false,
      projectId: this.$route.query.projectId || '',
      selectedProductId: '',
      selectedProjectId: this.$route.query.projectId ? Number(this.$route.query.projectId) : '',
      productOptions: [],
      projectOptions: [],
      planOptions: [],
      queryForm: {
        plan_id: this.$route.query.planId || ''
      },
      tableData: [],
      pageNo: 1,
      pageSize: 10,
      total: 0
    }
  },
  beforeRouteLeave(to, from, next) {
    this.savePageCache()
    next()
  },
  methods: {
    getCacheKey() {
      return 'test-platform-report-list-cache'
    },
    savePageCache() {
      const cache = {
        projectId: this.projectId,
        selectedProductId: this.selectedProductId,
        selectedProjectId: this.selectedProjectId,
        productOptions: this.productOptions,
        projectOptions: this.projectOptions,
        planOptions: this.planOptions,
        queryForm: this.queryForm,
        tableData: this.tableData,
        pageNo: this.pageNo,
        pageSize: this.pageSize,
        total: this.total
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
        this.planOptions = cache.planOptions || []
        this.queryForm = cache.queryForm || { plan_id: '' }
        this.tableData = cache.tableData || []
        this.pageNo = Number(cache.pageNo || 1)
        this.pageSize = Number(cache.pageSize || 10)
        this.total = Number(cache.total || 0)
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
        const data = (res && res.data) || res || {}
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
        const data = (res && res.data) || res || {}
        this.projectOptions = data.items || data.list || data.data || []
      }).catch(() => {
        this.projectOptions = []
      })
    },
    loadPlanOptions() {
      if (!this.selectedProjectId) {
        this.planOptions = []
        return Promise.resolve()
      }
      return getPlanList(this.selectedProjectId, { pageNo: 1, pageSize: 1000 }).then(res => {
        const data = (res && res.data) || res || {}
        this.planOptions = data.items || data.list || data.data || []
      }).catch(() => {
        this.planOptions = []
      })
    },
    handleProductChange(val) {
      this.selectedProjectId = ''
      this.projectId = ''
      this.queryForm.plan_id = ''
      this.projectOptions = []
      this.planOptions = []
      this.tableData = []
      this.total = 0
      this.loadProjectOptionsByProduct(val)
    },
    handleProjectChange(val) {
      this.selectedProjectId = val || ''
      this.projectId = val || ''
      this.queryForm.plan_id = ''
      this.planOptions = []
      this.pageNo = 1
      if (!val) {
        this.tableData = []
        this.total = 0
        return
      }
      saveLastProductProjectCache(this.selectedProductId, val)
      this.loadPlanOptions().finally(() => {
        this.fetchList()
      })
    },
    restoreSharedProductProjectCache() {
      const cached = readLastProductProjectCache()
      if (!cached) return Promise.resolve()
      const { productId: pid, projectId: projId } = cached
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
    fetchList() {
      if (!this.projectId) {
        this.tableData = []
        this.total = 0
        return
      }
      this.loading = true
      getReportList(Object.assign({}, this.queryForm, {
        product_id: this.selectedProductId || undefined,
        project_id: this.projectId || undefined,
        plan_id: this.queryForm.plan_id || undefined,
        pageNo: this.pageNo,
        pageSize: this.pageSize
      })).then(res => {
        const data = (res && res.data) || res || {}
        this.tableData = data.items || data.list || data.data || []
        this.total = data.total || data.totalCount || this.tableData.length
        this.savePageCache()
      }).catch(() => {
        this.tableData = []
        this.total = 0
        this.savePageCache()
      }).finally(() => {
        this.loading = false
      })
    },
    handleGenerate() {
      if (!this.queryForm.plan_id) {
        this.$message({ type: 'warning', message: '请先选择计划名称' })
        return
      }
      if (!this.projectId) {
        this.$message({ type: 'warning', message: '请先选择项目名称' })
        return
      }
      this.generating = true
      generateReport({
        planId: this.queryForm.plan_id,
        plan_id: this.queryForm.plan_id
      }).then(() => {
        this.$message({ type: 'success', message: '报告生成任务已提交' })
        this.fetchList()
      }).finally(() => {
        this.generating = false
      })
    },
    goViewer(row) {
      const type = String(row.report_type || row.type || '').toLowerCase()
      const isAuto = type.indexOf('auto') > -1 || type.indexOf('automation') > -1 || type.indexOf('自动') > -1 || Number(row.report_type || row.type) === 2
      if (isAuto) {
        const externalUrl = row.external_url || row.externalUrl || row.report_url || row.reportUrl || 'https://example.com/automation-report'
        window.open(externalUrl, '_blank')
        this.$message.info('自动化报告外部链接暂未实现，先跳转占位链接')
        return
      }
      this.$router.push({
        path: '/test-platform/report/viewer',
        query: {
          projectId: this.projectId,
          reportId: row.id
        }
      })
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
    resetQuery() {
      this.queryForm.plan_id = ''
      this.pageNo = 1
      this.fetchList()
    },
    formatDateTime(value) {
      if (!value) return '-'
      return String(value).replace('T', ' ').slice(0, 19)
    },
    formatPlanName(row) {
      if (!row) return '-'
      const directName = row.plan_name || row.planName || row.name || ''
      if (directName) return directName
      const planId = row.plan_id || row.planId
      if (!planId) return '-'
      const matched = (this.planOptions || []).find(item => String(item.id) === String(planId))
      return (matched && matched.name) || String(planId)
    },
    formatReportType(value) {
      const map = {
        manual: '手工',
        auto: '自动化',
        automation: '自动化',
        1: '手工',
        2: '自动化'
      }
      return map[value] || value || '-'
    },
    initByRouteProject() {
      if (!this.selectedProjectId) return Promise.resolve()
      return getProjectDetail(this.selectedProjectId).then(res => {
        const data = (res && res.data) || res || {}
        const productId = data.productId || data.product_id || ''
        if (productId) {
          this.selectedProductId = productId
          return this.loadProjectOptionsByProduct(productId)
        }
      }).catch(() => {})
    }
  },
  created() {
    if (this.restorePageCache()) {
      return
    }
    this.loadProductOptions()
      .then(() => {
        if (this.selectedProjectId) {
          return this.initByRouteProject()
        }
        return this.restoreSharedProductProjectCache()
      })
      .finally(() => {
        if (this.selectedProjectId) {
          this.projectId = this.selectedProjectId
          this.loadPlanOptions().finally(() => {
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
</style>
