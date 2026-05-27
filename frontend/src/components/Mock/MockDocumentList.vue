<template>
  <div class="mock-page">
    <page-section title="Mock 文档">
      <template slot="extra">
        <el-button type="primary" size="small" :loading="importing" @click="handlePrimaryImport">导入并生成 Mock</el-button>
        <el-button size="small" @click="fetchList">刷新</el-button>
        <el-button size="small" @click="goInterfaces">Mock接口</el-button>
      </template>

      <el-form :inline="true" size="small" class="filter-form">
        <el-form-item label="产品名称">
          <el-select
            v-model="selectedProductId"
            filterable
            clearable
            placeholder="请选择产品"
            style="width: 200px;"
            @change="handleMockProductChange"
            @focus="loadMockProductOptions">
            <el-option v-for="item in productOptions" :key="'md-p-' + item.id" :label="item.name" :value="item.id" />
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
            <el-option v-for="item in projectOptions" :key="'md-j-' + item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="文档名称">
          <el-input v-model="form.name" style="width: 220px;"></el-input>
        </el-form-item>
        <el-form-item label="来源">
          <el-select v-model="form.sourceType" style="width: 150px;">
            <el-option label="手动录入" value="manual"></el-option>
            <el-option label="OpenAPI/Swagger" value="openapi"></el-option>
            <el-option label="Apifox" value="apifox"></el-option>
            <el-option label="YApi" value="yapi"></el-option>
            <el-option label="Markdown" value="markdown"></el-option>
            <el-option label="文本" value="text"></el-option>
            <el-option label="PDF路径" value="pdf"></el-option>
            <el-option label="Word路径" value="word"></el-option>
          </el-select>
        </el-form-item>
      </el-form>

      <el-alert class="tips" type="info" :closable="false" title="导入后会调用后端 Faker + 当前 AI 大模型生成请求示例和响应模板，并自动入库为草稿。确认后启用接口和场景即可运行。"></el-alert>

      <el-radio-group v-model="importMode" size="small" class="import-tabs">
        <el-radio-button label="content">粘贴内容</el-radio-button>
        <el-radio-button label="file">上传文件</el-radio-button>
        <el-radio-button label="url">Swagger/YApi/Apifox URL</el-radio-button>
      </el-radio-group>

      <el-input
        v-if="importMode === 'content'"
        v-model="contentText"
        type="textarea"
        :rows="14"
        placeholder="粘贴 OpenAPI / Apifox / YApi JSON、Markdown、文本；manual 模式可粘贴单接口 Schema JSON。">
      </el-input>

      <div v-if="importMode === 'file'" class="upload-panel">
        <el-upload
          ref="upload"
          action=""
          :auto-upload="false"
          :limit="1"
          :file-list="fileList"
          :on-change="handleFileChange"
          :on-remove="handleFileRemove"
          accept=".json,.md,.markdown,.txt,.pdf,.doc,.docx">
          <el-button size="small" type="primary">选择接口文档文件</el-button>
          <div slot="tip" class="el-upload__tip">支持 json、md、txt、pdf、doc、docx。文件会保存到后端 attachment/interface_address，并自动解析批量录入 Mock。</div>
        </el-upload>
      </div>

      <el-form v-if="importMode === 'url'" size="small" label-width="110px" class="url-panel">
        <el-form-item label="文档地址">
          <el-input v-model="urlForm.url" placeholder="请输入 Swagger / YApi / Apifox 导出 JSON 地址"></el-input>
        </el-form-item>
      </el-form>

      <div class="table-title">导入记录</div>
      <el-table v-loading="loading" :data="tableData" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column label="产品名称" min-width="140" show-overflow-tooltip>
          <template slot-scope="scope">{{ formatMockProductName(scope.row) }}</template>
        </el-table-column>
        <el-table-column label="项目名称" min-width="160" show-overflow-tooltip>
          <template slot-scope="scope">{{ formatMockProjectName(scope.row) }}</template>
        </el-table-column>
        <el-table-column prop="name" label="名称" min-width="180"></el-table-column>
        <el-table-column prop="source_type_text" label="来源" width="140"></el-table-column>
        <el-table-column prop="parse_status_text" label="解析状态" width="110">
          <template slot-scope="scope">
            <el-tag :type="parseStatusType(scope.row.parse_status)" size="mini">{{ scope.row.parse_status_text }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="interface_count" label="接口数" width="90"></el-table-column>
        <el-table-column prop="parse_error" label="错误" min-width="220" show-overflow-tooltip></el-table-column>
        <el-table-column prop="created_time" label="创建时间" width="170"></el-table-column>
        <el-table-column label="操作" width="190" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" @click="goInterfaces(scope.row)">查看接口</el-button>
            <el-button type="text" @click="goIssues(scope.row)">解析问题</el-button>
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

    <el-dialog title="解析问题" :visible.sync="issueDialogVisible" width="820px">
      <el-table :data="issues" border size="small">
        <el-table-column prop="issue_type_text" label="类型" width="140"></el-table-column>
        <el-table-column prop="status_text" label="状态" width="100"></el-table-column>
        <el-table-column prop="error_message" label="错误" min-width="220" show-overflow-tooltip></el-table-column>
        <el-table-column prop="suggestion" label="建议" min-width="220" show-overflow-tooltip></el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { getMockDocumentList, getMockParseIssueList, importMockDocument, uploadImportMockDocument, urlImportMockDocument } from '@/api/mockApi'
import mockProductProjectFilter from '@/mixins/mockProductProjectFilter'

export default {
  name: 'MockDocumentList',
  components: { PageSection },
  mixins: [mockProductProjectFilter],
  data() {
    return {
      loading: false,
      importing: false,
      issueDialogVisible: false,
      issues: [],
      tableData: [],
      total: 0,
      pageNo: 1,
      pageSize: 10,
      importMode: 'content',
      fileList: [],
      selectedFile: null,
      urlForm: {
        url: ''
      },
      form: {
        name: 'Mock接口文档',
        sourceType: 'manual'
      },
      contentText: '{\n  "name": "用户详情",\n  "path": "/api/user/{id}",\n  "method": "GET",\n  "query": [{"name": "id", "type": "integer", "required": true, "description": "用户ID"}],\n  "response": {\n    "type": "object",\n    "properties": {\n      "code": {"type": "integer"},\n      "message": {"type": "string"},\n      "data": {\n        "type": "object",\n        "properties": {\n          "id": {"type": "integer", "description": "用户ID"},\n          "name": {"type": "string", "description": "姓名"},\n          "phone": {"type": "string", "description": "手机号"}\n        }\n      }\n    }\n  }\n}'
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
      getMockDocumentList({ projectId: this.mockProjectId, pageNo: this.pageNo, pageSize: this.pageSize }).then(res => {
        const data = (res && res.data) || {}
        this.tableData = data.list || []
        this.total = data.total || 0
      }).finally(() => {
        this.loading = false
      })
    },
    handlePrimaryImport() {
      if (this.importMode === 'file') {
        this.uploadImportDocument()
        return
      }
      if (this.importMode === 'url') {
        this.urlImportDocument()
        return
      }
      this.importDocument()
    },
    handleFileChange(file, fileList) {
      this.fileList = fileList.slice(-1)
      this.selectedFile = file.raw
    },
    handleFileRemove() {
      this.fileList = []
      this.selectedFile = null
    },
    uploadImportDocument() {
      if (!this.mockProductId || !this.mockProjectId) {
        this.$message.warning('请先选择产品名称和项目名称')
        return
      }
      if (!this.selectedFile) {
        this.$message.warning('请选择接口文档文件')
        return
      }
      const formData = new FormData()
      formData.append('file', this.selectedFile)
      formData.append('productId', this.mockProductId)
      formData.append('projectId', this.mockProjectId)
      formData.append('name', this.form.name)
      formData.append('sourceType', this.form.sourceType === 'manual' ? '' : this.form.sourceType)
      formData.append('createdBy', this.currentUserId())
      this.importing = true
      uploadImportMockDocument(formData).then(res => {
        this.handleImportSuccess(res)
        this.fileList = []
        this.selectedFile = null
      }).finally(() => {
        this.importing = false
      })
    },
    urlImportDocument() {
      if (!this.mockProductId || !this.mockProjectId) {
        this.$message.warning('请先选择产品名称和项目名称')
        return
      }
      if (!this.urlForm.url) {
        this.$message.warning('请填写文档地址')
        return
      }
      this.importing = true
      urlImportMockDocument({
        productId: this.mockProductId,
        projectId: this.mockProjectId,
        name: this.form.name,
        sourceType: this.form.sourceType === 'manual' ? 'openapi' : this.form.sourceType,
        url: this.urlForm.url,
        createdBy: this.currentUserId()
      }).then(res => {
        this.handleImportSuccess(res)
      }).finally(() => {
        this.importing = false
      })
    },
    importDocument() {
      let content = this.contentText
      const trimmed = String(this.contentText || '').trim()
      if (!trimmed) {
        this.$message.warning('请填写接口文档内容')
        return
      }
      if (trimmed.charAt(0) === '{' || trimmed.charAt(0) === '[') {
        try {
          content = JSON.parse(trimmed)
        } catch (e) {
          this.$message.warning('JSON 格式不正确，如为文本请切换来源为 markdown/text')
          return
        }
      }
      if (!this.mockProductId || !this.mockProjectId) {
        this.$message.warning('请先选择产品名称和项目名称')
        return
      }
      this.importing = true
      importMockDocument({
        productId: this.mockProductId,
        projectId: this.mockProjectId,
        name: this.form.name,
        sourceType: this.form.sourceType,
        source: ['pdf', 'word'].indexOf(this.form.sourceType) >= 0 ? trimmed : '',
        content,
        createdBy: this.currentUserId()
      }).then(res => {
        this.handleImportSuccess(res)
      }).finally(() => {
        this.importing = false
      })
    },
    handleImportSuccess(res) {
      const data = (res && res.data) || {}
      this.$message.success('导入完成，接口数：' + (data.interfaceCount || 0) + '，问题数：' + (data.issueCount || 0))
      this.fetchList()
      if (data.interfaceCount > 0) {
        this.$router.push({
          path: '/mock/interface',
          query: {
            productId: this.mockProductId,
            projectId: this.mockProjectId,
            documentId: data.documentId
          }
        })
      }
    },
    goInterfaces(row) {
      const query = {
        productId: this.mockProductId || undefined,
        projectId: this.mockProjectId || undefined
      }
      if (row && row.id) query.documentId = row.id
      this.$router.push({ path: '/mock/interface', query })
    },
    goIssues(row) {
      getMockParseIssueList({ documentId: row.id, pageNo: 1, pageSize: 100 }).then(res => {
        const data = (res && res.data) || {}
        this.issues = data.list || []
        this.issueDialogVisible = true
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
    parseStatusType(status) {
      if (Number(status) === 1) return 'success'
      if (Number(status) === 2) return 'danger'
      if (Number(status) === 3) return 'warning'
      return 'info'
    },
    currentUserId() {
      try {
        const user = JSON.parse(localStorage.getItem('authUser') || '{}')
        return user.id || user.userId || ''
      } catch (e) {
        return ''
      }
    }
  }
}
</script>

<style scoped>
.mock-page { padding: 20px; }
.filter-form { margin-bottom: 12px; }
.tips { margin-bottom: 12px; }
.import-tabs { margin-bottom: 12px; }
.upload-panel, .url-panel { padding: 16px; border: 1px dashed #dcdfe6; background: #fafafa; margin-bottom: 12px; }
.table-title { margin: 18px 0 10px; font-weight: 600; color: #303133; }
.pager { margin-top: 16px; text-align: right; }
</style>
