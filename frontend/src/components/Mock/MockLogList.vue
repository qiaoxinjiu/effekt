<template>
  <div class="mock-page">
    <page-section title="Mock 调用日志">
      <template slot="extra">
        <el-button size="small" @click="goInterfaces">Mock接口</el-button>
        <el-button size="small" @click="fetchList">刷新</el-button>
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
            <el-option v-for="item in productOptions" :key="'ml-p-' + item.id" :label="item.name" :value="item.id" />
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
            <el-option v-for="item in projectOptions" :key="'ml-j-' + item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="接口ID">
          <el-input v-model="query.interfaceId" clearable style="width: 110px;"></el-input>
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
        <el-table-column prop="interface_id" label="接口ID" width="90"></el-table-column>
        <el-table-column prop="scene_id" label="场景ID" width="90"></el-table-column>
        <el-table-column prop="method" label="方法" width="90"></el-table-column>
        <el-table-column prop="path" label="Path" min-width="220" show-overflow-tooltip></el-table-column>
        <el-table-column prop="http_status" label="HTTP" width="90"></el-table-column>
        <el-table-column prop="duration_ms" label="耗时ms" width="90"></el-table-column>
        <el-table-column prop="created_time" label="调用时间" width="170"></el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" @click="showDetail(scope.row)">查看报文</el-button>
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

    <el-dialog title="调用报文" :visible.sync="dialogVisible" width="900px">
      <el-tabs>
          <el-tab-pane label="Query"><pre class="log-payload-pre">{{ prettyLogPayload('query') }}</pre></el-tab-pane>
          <el-tab-pane label="Body"><pre class="log-payload-pre">{{ prettyLogPayload('body') }}</pre></el-tab-pane>
          <el-tab-pane label="Response"><pre class="log-payload-pre">{{ prettyLogPayload('response') }}</pre></el-tab-pane>
      </el-tabs>
    </el-dialog>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { getMockLogList } from '@/api/mockApi'
import mockProductProjectFilter from '@/mixins/mockProductProjectFilter'

export default {
  name: 'MockLogList',
  components: { PageSection },
  mixins: [mockProductProjectFilter],
  data() {
    return {
      loading: false,
      dialogVisible: false,
      activeRow: {},
      tableData: [],
      total: 0,
      pageNo: 1,
      pageSize: 10,
      query: {
        interfaceId: this.$route.query.interfaceId || ''
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
      getMockLogList(
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
    showDetail(row) {
      this.activeRow = row || {}
      this.dialogVisible = true
    },
    isMeaningfulPayload(value) {
      if (value === undefined || value === null) return false
      if (typeof value === 'string') {
        const text = value.trim()
        if (!text || text === '[]' || text === '{}' || text === 'null') return false
        return true
      }
      if (Array.isArray(value)) return value.length > 0
      if (typeof value === 'object') return Object.keys(value).length > 0
      return true
    },
    pickPayload(candidates) {
      for (let i = 0; i < candidates.length; i++) {
        const value = candidates[i]
        if (this.isMeaningfulPayload(value)) return value
      }
      return null
    },
    getLogPayload(row, type) {
      if (!row) return null
      const keyMap = {
        query: [
          'request_query',
          'requestQuery',
          'query_params',
          'queryParams',
          'request_params',
          'requestParams',
          'req_query',
          'reqQuery',
          'path_params',
          'pathParams',
          'url_params',
          'urlParams',
          'params',
          'query'
        ],
        body: [
          'request_body',
          'requestBody',
          'request_payload',
          'requestPayload',
          'req_body',
          'reqBody',
          'payload',
          'body'
        ],
        response: [
          'response_body',
          'responseBody',
          'resp_body',
          'respBody',
          'response_data',
          'responseData',
          'result',
          'response'
        ]
      }
      const keys = keyMap[type] || []
      const direct = []
      for (let i = 0; i < keys.length; i++) {
        const k = keys[i]
        if (row[k] !== undefined && row[k] !== null) direct.push(row[k])
      }
      const picked = this.pickPayload(direct)
      if (picked != null) return picked

      const req = this.parseMaybeJson(row.request || row.req || row.request_data || row.requestData)
      if (req && typeof req === 'object') {
        if (type === 'query') {
          return this.pickPayload([
            req.request_query,
            req.requestQuery,
            req.query_params,
            req.queryParams,
            req.request_params,
            req.requestParams,
            req.path_params,
            req.pathParams,
            req.params,
            req.query
          ])
        }
        if (type === 'body') {
          return this.pickPayload([
            req.request_body,
            req.requestBody,
            req.body,
            req.payload
          ])
        }
      }
      if (type === 'response') {
        const resp = this.parseMaybeJson(
          row.response || row.resp || row.response_data || row.responseData
        )
        return this.pickPayload([resp])
      }
      return null
    },
    parseMaybeJson(value) {
      if (value === undefined || value === null) return null
      if (typeof value === 'object') return value
      const text = String(value).trim()
      if (!text) return null
      try {
        return JSON.parse(text)
      } catch (e) {
        return value
      }
    },
    prettyLogPayload(type) {
      return this.pretty(this.getLogPayload(this.activeRow, type))
    },
    pretty(value) {
      if (value === undefined || value === null) return '—'
      if (typeof value === 'object') {
        if (Array.isArray(value) && value.length === 0) return '（空）'
        if (!Array.isArray(value) && Object.keys(value).length === 0) return '（空）'
        try {
          return JSON.stringify(value, null, 2)
        } catch (e) {
          return String(value)
        }
      }
      const text = String(value).trim()
      if (!text) return '—'
      try {
        return JSON.stringify(JSON.parse(text), null, 2)
      } catch (e) {
        return String(value)
      }
    },
    goInterfaces() {
      this.$router.push({
        path: '/mock/interface',
        query: {
          productId: this.mockProductId || undefined,
          projectId: this.mockProjectId || undefined
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
    }
  }
}
</script>

<style scoped>
.mock-page { padding: 20px; }
.pager { margin-top: 16px; text-align: right; }
.log-payload-pre {
  margin: 0;
  min-height: 120px;
  max-height: 420px;
  overflow: auto;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
