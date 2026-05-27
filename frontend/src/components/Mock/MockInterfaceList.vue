<template>
  <div class="mock-page">
    <page-section title="Mock 接口">
      <template slot="extra">
        <el-button type="primary" size="small" @click="goImport">导入文档</el-button>
        <el-button size="small" @click="fetchList">刷新</el-button>
        <el-button size="small" @click="goLogs">调用日志</el-button>
      </template>

      <el-form :inline="true" size="small">
        <el-form-item label="产品名称">
          <el-select
            v-model="selectedProductId"
            filterable
            clearable
            placeholder="请选择产品"
            style="width: 200px;"
            @change="handleMockProductChange"
            @focus="loadMockProductOptions">
            <el-option v-for="item in productOptions" :key="'mi-p-' + item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目名称">
          <el-select
            v-model="selectedProjectId"
            filterable
            clearable
            placeholder="请选择项目"
            style="width: 220px;"
            :disabled="!selectedProductId"
            @change="handleMockProjectChange">
            <el-option v-for="item in projectOptions" :key="'mi-j-' + item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="文档ID">
          <el-input v-model="query.documentId" clearable style="width: 110px;"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="query.status" clearable style="width: 120px;">
            <el-option label="草稿" value="0"></el-option>
            <el-option label="已启用" value="1"></el-option>
            <el-option label="已停用" value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input v-model="query.keyword" clearable placeholder="名称" style="width: 180px;"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="search">查询</el-button>
        </el-form-item>
      </el-form>

      <el-table v-loading="loading" :data="tableData" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column label="产品名称" min-width="120" show-overflow-tooltip>
          <template slot-scope="scope">{{ formatMockProductName(scope.row) }}</template>
        </el-table-column>
        <el-table-column label="项目名称" min-width="140" show-overflow-tooltip>
          <template slot-scope="scope">{{ formatMockProjectName(scope.row) }}</template>
        </el-table-column>
        <el-table-column prop="name" label="接口名称" min-width="180" show-overflow-tooltip></el-table-column>
        <el-table-column prop="method" label="方法" width="90">
          <template slot-scope="scope">
            <el-tag size="mini">{{ scope.row.method }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="path" label="Path" min-width="260" show-overflow-tooltip></el-table-column>
        <el-table-column prop="status_text" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag size="mini" :type="statusType(scope.row.status)">{{ scope.row.status_text }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_time" label="创建时间" width="170"></el-table-column>
        <el-table-column label="操作" width="300" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" @click="goDetail(scope.row)">详情</el-button>
            <el-button type="text" @click="goRun(scope.row)">运行测试</el-button>
            <el-button v-if="Number(scope.row.status) !== 1" type="text" @click="enableRow(scope.row)">启用</el-button>
            <el-button v-if="Number(scope.row.status) === 1" type="text" @click="disableRow(scope.row)">停用</el-button>
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
          @current-change="handleCurrentChange">
        </el-pagination>
      </div>
    </page-section>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { disableMockInterface, enableMockInterface, getMockInterfaceList } from '@/api/mockApi'
import mockProductProjectFilter from '@/mixins/mockProductProjectFilter'

export default {
  name: 'MockInterfaceList',
  components: { PageSection },
  mixins: [mockProductProjectFilter],
  data() {
    return {
      loading: false,
      tableData: [],
      total: 0,
      pageNo: 1,
      pageSize: 10,
      query: {
        documentId: this.$route.query.documentId || '',
        status: this.$route.query.status || '',
        keyword: ''
      }
    }
  },
  created() {
    this.bootstrapMockProductProject().then(() => {
      this.fetchList()
    })
  },
  methods: {
    onMockProductProjectChange() {
      this.pageNo = 1
      this.fetchList()
    },
    fetchList() {
      if (!this.mockProjectId) {
        this.tableData = []
        this.total = 0
        return
      }
      this.loading = true
      getMockInterfaceList(
        Object.assign({}, this.query, {
          projectId: this.mockProjectId,
          pageNo: this.pageNo,
          pageSize: this.pageSize
        })
      ).then(res => {
        const data = (res && res.data) || {}
        this.tableData = data.list || []
        this.total = data.total || 0
      }).finally(() => {
        this.loading = false
      })
    },
    search() {
      this.pageNo = 1
      this.fetchList()
    },
    enableRow(row) {
      enableMockInterface(row.id).then(() => {
        this.$message.success('接口已启用')
        this.fetchList()
      })
    },
    disableRow(row) {
      disableMockInterface(row.id).then(() => {
        this.$message.success('接口已停用')
        this.fetchList()
      })
    },
    mockRouteQuery(extra) {
      return Object.assign(
        {
          productId: this.mockProductId || undefined,
          projectId: this.mockProjectId || undefined
        },
        extra || {}
      )
    },
    goDetail(row) {
      this.$router.push({ path: '/mock/interface/detail', query: this.mockRouteQuery({ id: row.id }) })
    },
    goRun(row) {
      this.$router.push({ path: '/mock/interface/detail', query: this.mockRouteQuery({ id: row.id, tab: 'run' }) })
    },
    goImport() {
      this.$router.push({ path: '/mock/document', query: this.mockRouteQuery() })
    },
    goLogs() {
      this.$router.push({ path: '/mock/log', query: this.mockRouteQuery() })
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
    statusType(status) {
      if (Number(status) === 1) return 'success'
      if (Number(status) === 2) return 'info'
      return 'warning'
    }
  }
}
</script>

<style scoped>
.mock-page { padding: 20px; }
.pager { margin-top: 16px; text-align: right; }
</style>
