<template>
  <div class="mock-page">
    <page-section :title="detail.name || 'Mock 接口详情'">
      <template slot="extra">
        <el-button size="small" @click="backList">返回列表</el-button>
        <el-button type="primary" size="small" @click="saveInterface">保存接口</el-button>
        <el-button v-if="Number(detail.status) !== 1" size="small" type="success" @click="enableInterface">启用接口</el-button>
        <el-button v-if="Number(detail.status) === 1" size="small" @click="disableInterface">停用接口</el-button>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="接口信息" name="info">
          <el-form :model="detail" label-width="110px" size="small">
            <el-form-item label="接口ID">
              <span>{{ detail.id }}</span>
              <el-tag size="mini" :type="statusType(detail.status)" style="margin-left: 8px;">{{ detail.status_text }}</el-tag>
            </el-form-item>
            <el-form-item label="接口名称">
              <el-input v-model="detail.name"></el-input>
            </el-form-item>
            <el-form-item label="Method">
              <el-select v-model="detail.method" style="width: 160px;">
                <el-option label="GET" value="GET"></el-option>
                <el-option label="POST" value="POST"></el-option>
                <el-option label="PUT" value="PUT"></el-option>
                <el-option label="DELETE" value="DELETE"></el-option>
                <el-option label="PATCH" value="PATCH"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Path">
              <el-input v-model="detail.path"></el-input>
            </el-form-item>
            <el-form-item label="描述">
              <el-input v-model="detail.description" type="textarea" :rows="2"></el-input>
            </el-form-item>
            <el-form-item label="Query Schema">
              <el-input v-model="detail.query_schema" type="textarea" :rows="6"></el-input>
            </el-form-item>
            <el-form-item label="Body Schema">
              <el-input v-model="detail.body_schema" type="textarea" :rows="6"></el-input>
            </el-form-item>
            <el-form-item label="Response Schema">
              <el-input v-model="detail.response_schema" type="textarea" :rows="8"></el-input>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="Mock 场景" name="scenes">
          <el-table v-loading="sceneLoading" :data="scenes" border>
            <el-table-column prop="id" label="ID" width="70"></el-table-column>
            <el-table-column prop="scene_name" label="场景" width="130"></el-table-column>
            <el-table-column prop="scene_code_text" label="类型" width="120"></el-table-column>
            <el-table-column prop="http_status" label="HTTP" width="80"></el-table-column>
            <el-table-column prop="delay_ms" label="延迟ms" width="90"></el-table-column>
            <el-table-column prop="priority" label="优先级" width="90"></el-table-column>
            <el-table-column prop="status_text" label="状态" width="100">
              <template slot-scope="scope">
                <el-tag size="mini" :type="statusType(scope.row.status)">{{ scope.row.status_text }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="240" fixed="right">
              <template slot-scope="scope">
                <el-button type="text" @click="editScene(scope.row)">编辑</el-button>
                <el-button v-if="Number(scope.row.status) !== 1" type="text" @click="enableScene(scope.row)">启用</el-button>
                <el-button v-if="Number(scope.row.status) === 1" type="text" @click="disableScene(scope.row)">停用</el-button>
                <el-button type="text" @click="setRunScene(scope.row)">运行</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="运行测试" name="run">
          <el-form label-width="100px" size="small">
            <el-form-item label="Mock URL">
              <el-input :value="mockUrl" readonly>
                <el-button slot="append" @click="runMock">发送</el-button>
              </el-input>
            </el-form-item>
            <el-form-item label="项目ID">
              <el-input v-model="runForm.projectId" style="width: 160px;"></el-input>
            </el-form-item>
            <el-form-item label="请求Path">
              <el-input v-model="runForm.path" placeholder="例如 /api/user/10001"></el-input>
            </el-form-item>
            <el-form-item label="场景">
              <el-select v-model="runForm.mockScene" clearable placeholder="默认 success" style="width: 220px;">
                <el-option v-for="scene in scenes" :key="scene.id" :label="scene.scene_name + ' / ' + scene.scene_code" :value="scene.scene_code"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Query JSON">
              <el-input v-model="runForm.queryText" type="textarea" :rows="4" placeholder='例如 {"id":"10001", "pageNo":1, "pageSize":10}'></el-input>
            </el-form-item>
            <el-form-item label="Body JSON">
              <el-input v-model="runForm.bodyText" type="textarea" :rows="5" placeholder='POST/PUT 时填写 body'></el-input>
            </el-form-item>
            <el-form-item label="响应结果">
              <el-input v-model="runResult" type="textarea" :rows="14" readonly></el-input>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </page-section>

    <el-dialog title="编辑场景" :visible.sync="sceneDialogVisible" width="980px">
      <el-form :model="sceneForm" label-width="120px" size="small">
        <el-form-item label="场景名称"><el-input v-model="sceneForm.scene_name"></el-input></el-form-item>
        <el-form-item label="场景编码"><el-input v-model="sceneForm.scene_code"></el-input></el-form-item>
        <el-form-item label="HTTP状态"><el-input-number v-model="sceneForm.http_status" :min="100" :max="599"></el-input-number></el-form-item>
        <el-form-item label="延迟ms"><el-input-number v-model="sceneForm.delay_ms" :min="0"></el-input-number></el-form-item>
        <el-form-item label="优先级"><el-input-number v-model="sceneForm.priority"></el-input-number></el-form-item>
        <el-form-item label="请求示例"><el-input v-model="sceneForm.request_example" type="textarea" :rows="4"></el-input></el-form-item>
        <el-form-item label="响应模板"><el-input v-model="sceneForm.response_template" type="textarea" :rows="10"></el-input></el-form-item>
        <el-form-item label="响应Header"><el-input v-model="sceneForm.response_headers" type="textarea" :rows="4"></el-input></el-form-item>
        <el-form-item label="响应规则"><el-input v-model="sceneForm.response_rule" type="textarea" :rows="6"></el-input></el-form-item>
        <el-form-item label="匹配规则"><el-input v-model="sceneForm.match_rule" type="textarea" :rows="6"></el-input></el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="sceneDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveScene">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import {
  disableMockInterface,
  disableMockScene,
  enableMockInterface,
  enableMockScene,
  getMockInterfaceDetail,
  getMockSceneList,
  runMockRuntime,
  updateMockInterface,
  updateMockScene
} from '@/api/mockApi'

export default {
  name: 'MockInterfaceDetail',
  components: { PageSection },
  data() {
    return {
      activeTab: this.$route.query.tab || 'info',
      detail: {},
      scenes: [],
      sceneLoading: false,
      sceneDialogVisible: false,
      sceneForm: {},
      runForm: {
        projectId: this.$route.query.projectId || 1,
        path: '',
        mockScene: '',
        queryText: '{}',
        bodyText: '{}'
      },
      runResult: ''
    }
  },
  computed: {
    mockUrl() {
      const base = '/it/api/mock/runtime' + this.normalizePath(this.runForm.path || this.detail.path)
      const query = '?projectId=' + encodeURIComponent(this.runForm.projectId || '') + (this.runForm.mockScene ? '&mockScene=' + encodeURIComponent(this.runForm.mockScene) : '')
      return base + query
    }
  },
  created() {
    this.fetchDetail()
  },
  methods: {
    fetchDetail() {
      getMockInterfaceDetail({ id: this.$route.query.id }).then(res => {
        this.detail = (res && res.data) || {}
        this.runForm.path = this.detail.path || ''
        this.fetchScenes()
      })
    },
    fetchScenes() {
      this.sceneLoading = true
      getMockSceneList({ interfaceId: this.$route.query.id }).then(res => {
        const data = (res && res.data) || {}
        this.scenes = data.list || []
      }).finally(() => {
        this.sceneLoading = false
      })
    },
    saveInterface() {
      updateMockInterface(Object.assign({}, this.detail, { interfaceId: this.detail.id })).then(() => {
        this.$message.success('接口已保存')
        this.fetchDetail()
      })
    },
    enableInterface() {
      enableMockInterface(this.detail.id).then(() => {
        this.$message.success('接口已启用')
        this.fetchDetail()
      })
    },
    disableInterface() {
      disableMockInterface(this.detail.id).then(() => {
        this.$message.success('接口已停用')
        this.fetchDetail()
      })
    },
    editScene(row) {
      this.sceneForm = Object.assign({}, row)
      this.sceneDialogVisible = true
    },
    saveScene() {
      const payload = Object.assign({}, this.sceneForm, { sceneId: this.sceneForm.id })
      try {
        ;['request_example', 'response_template', 'response_headers', 'response_rule', 'match_rule'].forEach(key => {
          if (payload[key] && typeof payload[key] === 'string') JSON.parse(payload[key])
        })
      } catch (e) {
        this.$message.warning('JSON 格式不正确：' + e.message)
        return
      }
      updateMockScene(payload).then(() => {
        this.$message.success('场景已保存')
        this.sceneDialogVisible = false
        this.fetchScenes()
      })
    },
    enableScene(row) {
      enableMockScene(row.id).then(() => {
        this.$message.success('场景已启用')
        this.fetchScenes()
      })
    },
    disableScene(row) {
      disableMockScene(row.id).then(() => {
        this.$message.success('场景已停用')
        this.fetchScenes()
      })
    },
    setRunScene(row) {
      this.runForm.mockScene = row.scene_code
      this.activeTab = 'run'
    },
    runMock() {
      let query = {}
      let body = {}
      try {
        query = this.runForm.queryText ? JSON.parse(this.runForm.queryText) : {}
        body = this.runForm.bodyText ? JSON.parse(this.runForm.bodyText) : {}
      } catch (e) {
        this.$message.warning('Query 或 Body JSON 格式不正确')
        return
      }
      runMockRuntime({
        method: this.detail.method,
        path: this.runForm.path || this.detail.path,
        projectId: this.runForm.projectId,
        mockScene: this.runForm.mockScene,
        query,
        body
      }).then(res => {
        this.runResult = JSON.stringify((res && res.data) || res, null, 2)
      }).catch(err => {
        const data = err && err.response && err.response.data
        this.runResult = data ? JSON.stringify(data, null, 2) : String(err && err.message || err)
      })
    },
    backList() {
      this.$router.push({ path: '/mock/interface', query: { projectId: this.runForm.projectId } })
    },
    normalizePath(path) {
      const value = String(path || '').trim()
      if (!value) return '/'
      return value.charAt(0) === '/' ? value : '/' + value
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
</style>
