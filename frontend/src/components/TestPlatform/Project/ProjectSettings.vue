<template>
  <div class="page-wrap">
    <page-section title="项目设置">
      <template slot="extra">
        <el-button size="small" @click="goBackToList">返回</el-button>
      </template>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="项目成员" name="members">
          <div class="toolbar-wrap">
            <el-button type="primary" size="small" @click="openMemberDialog">新增成员</el-button>
          </div>
          <el-table :data="members" border>
            <el-table-column prop="project_name" label="项目名称"></el-table-column>
            <el-table-column prop="username" label="用户名"></el-table-column>
            <el-table-column prop="role_name" label="角色"></el-table-column>
            <el-table-column prop="joined_time" label="加入时间"></el-table-column>
          </el-table>
          <div style="margin-top: 16px; text-align: right;">
            <el-pagination
              :current-page="memberPageNo"
              :page-size="memberPageSize"
              :page-sizes="[10, 20, 50, 100]"
              :total="memberTotal"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleMemberSizeChange"
              @current-change="handleMemberCurrentChange">
            </el-pagination>
          </div>
        </el-tab-pane>
        <el-tab-pane label="环境配置" name="environments">
          <div class="toolbar-wrap">
            <el-button type="primary" size="small" @click="openEnvironmentDialog">新增环境</el-button>
          </div>
          <el-table :data="environments" border>
            <el-table-column prop="name" label="环境"></el-table-column>
            <el-table-column prop="variables" label="变量">
              <template slot-scope="scope">
                <json-viewer :value="scope.row.variables"></json-viewer>
              </template>
            </el-table-column>
          </el-table>
          <div style="margin-top: 16px; text-align: right;">
            <el-pagination
              :current-page="environmentPageNo"
              :page-size="environmentPageSize"
              :page-sizes="[10, 20, 50, 100]"
              :total="environmentTotal"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleEnvironmentSizeChange"
              @current-change="handleEnvironmentCurrentChange">
            </el-pagination>
          </div>
        </el-tab-pane>
        <el-tab-pane label="Hook 配置" name="hooks">
          <div class="toolbar-wrap hook-toolbar">
            <div class="hook-toolbar-left">
              <el-select
                v-model="hookTypeFilter"
                clearable
                placeholder="Hook 类型"
                size="small"
                style="width: 140px;"
                @change="onHookTypeFilterChange">
                <el-option label="飞书" :value="1" />
                <el-option label="钉钉" :value="2" />
                <el-option label="企微" :value="3" />
              </el-select>
            </div>
            <el-button type="primary" size="small" @click="openHookDialog('create')">新增 Hook</el-button>
          </div>
          <el-table v-loading="hookLoading" :data="hooks" border>
            <el-table-column prop="hook_type_name" label="类型" width="100">
              <template slot-scope="scope">{{ scope.row.hook_type_name || hookTypeLabel(scope.row.hook_type) }}</template>
            </el-table-column>
            <el-table-column label="Webhook" min-width="220" show-overflow-tooltip>
              <template slot-scope="scope">{{ scope.row.webhook_url || scope.row.webhookUrl || '-' }}</template>
            </el-table-column>
            <el-table-column label="启用" width="80">
              <template slot-scope="scope">
                <el-tag size="mini" :type="(scope.row.enabled === 1 || scope.row.enabled === true) ? 'success' : 'info'">
                  {{ (scope.row.enabled === 1 || scope.row.enabled === true) ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" min-width="140" show-overflow-tooltip />
            <el-table-column label="创建时间" width="170">
              <template slot-scope="scope">{{ scope.row.created_time || scope.row.createdTime || '-' }}</template>
            </el-table-column>
            <el-table-column label="操作" width="140" fixed="right">
              <template slot-scope="scope">
                <el-button type="text" size="small" @click="openHookDialog('edit', scope.row)">编辑</el-button>
                <el-button type="text" size="small" style="color: #f56c6c;" @click="handleHookDelete(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div style="margin-top: 16px; text-align: right;">
            <el-pagination
              :current-page="hookPageNo"
              :page-size="hookPageSize"
              :page-sizes="[10, 20, 50, 100]"
              :total="hookTotal"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleHookSizeChange"
              @current-change="handleHookCurrentChange">
            </el-pagination>
          </div>
        </el-tab-pane>
      </el-tabs>
    </page-section>

    <el-dialog title="新增成员" :visible.sync="memberDialogVisible" width="520px" @close="resetMemberForm">
      <el-form ref="memberForm" :model="memberForm" :rules="memberRules" label-width="94px" size="small">
        <el-form-item label="选择用户" prop="user_ids">
          <el-select
            v-model="memberForm.user_ids"
            multiple
            filterable
            placeholder="请选择用户"
            style="width: 100%;"
            @focus="loadUserOptions">
            <el-option
              v-for="item in userOptions"
              :key="item.id"
              :label="item.username + (item.real_name ? ' (' + item.real_name + ')' : '')"
              :value="item.id">
            </el-option>
            <el-option v-if="userHasMore" disabled style="text-align: center;">
              <span v-if="userLoading">加载中...</span>
              <span v-else @click.stop="loadMoreUsers">加载更多</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button size="small" @click="memberDialogVisible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="memberSubmitting" @click="submitMember">确定</el-button>
      </span>
    </el-dialog>

    <el-dialog title="新增环境" :visible.sync="environmentDialogVisible" width="520px" @close="resetEnvironmentForm">
      <el-form ref="environmentForm" :model="environmentForm" :rules="environmentRules" label-width="94px" size="small">
        <el-form-item label="环境名称" prop="name">
          <el-input v-model.trim="environmentForm.name" maxlength="64" placeholder="请输入环境名称"></el-input>
        </el-form-item>
        <el-form-item label="变量JSON" prop="variablesText">
          <el-input v-model.trim="environmentForm.variablesText" type="textarea" :rows="6" placeholder='请输入 JSON，例如 {"baseUrl":"https://test.com"}'></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button size="small" @click="environmentDialogVisible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="environmentSubmitting" @click="submitEnvironment">确定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :title="hookDialogMode === 'create' ? '新增 Hook' : '编辑 Hook'"
      :visible.sync="hookDialogVisible"
      width="560px"
      @close="resetHookForm">
      <el-form ref="hookFormRef" :model="hookForm" :rules="hookRules" label-width="100px" size="small">
        <el-form-item label="Hook 类型" prop="hookType">
          <el-select v-model="hookForm.hookType" placeholder="请选择" style="width: 100%;" :disabled="hookDialogMode === 'edit'">
            <el-option label="飞书" :value="1" />
            <el-option label="钉钉" :value="2" />
            <el-option label="企微" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="Webhook" prop="webhookUrl">
          <el-input v-model.trim="hookForm.webhookUrl" type="textarea" :rows="2" placeholder="Webhook 地址" />
        </el-form-item>
        <el-form-item label="签名密钥" prop="secret">
          <el-input v-model.trim="hookForm.secret" show-password placeholder="可选，飞书/钉钉等签名校验用" />
        </el-form-item>
        <el-form-item label="启用" prop="enabled">
          <el-switch v-model="hookForm.enabled" :active-value="1" :inactive-value="0" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model.trim="hookForm.description" maxlength="200" show-word-limit placeholder="说明用途" />
        </el-form-item>
        <el-form-item label="扩展配置" prop="configText">
          <el-input v-model.trim="hookForm.configText" type="textarea" :rows="4" placeholder='JSON，默认 {}' />
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button size="small" @click="hookDialogVisible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="hookSubmitting" @click="submitHook">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import JsonViewer from '@/components/TestPlatform/common/JsonViewer'
import {
  createEnvironment,
  createProjectMember,
  createProjectHook,
  deleteProjectHook,
  getProjectEnvironments,
  getProjectHookDetail,
  getProjectHookList,
  getProjectMembers,
  updateProjectHook
} from '@/api/projectApi'
import { getUserList } from '@/api/rbacApi'

const getDefaultMemberForm = () => ({
  user_ids: []
})

const getDefaultEnvironmentForm = () => ({
  name: '',
  variablesText: '{}'
})

const getDefaultHookForm = () => ({
  hookId: null,
  hookType: 1,
  webhookUrl: '',
  secret: '',
  enabled: 1,
  description: '',
  configText: '{}'
})

export default {
  name: 'ProjectSettings',
  components: { PageSection, JsonViewer },
  data() {
    return {
      activeTab: 'members',
      memberPageNo: 1,
      memberPageSize: 10,
      memberTotal: 0,
      environmentPageNo: 1,
      environmentPageSize: 10,
      environmentTotal: 0,
      members: [],
      environments: [],
      memberDialogVisible: false,
      environmentDialogVisible: false,
      memberSubmitting: false,
      environmentSubmitting: false,
      memberForm: getDefaultMemberForm(),
      environmentForm: getDefaultEnvironmentForm(),
      memberRules: {
        user_ids: [{ required: true, message: '请选择用户', trigger: 'change' }]
      },
      environmentRules: {
        name: [{ required: true, message: '请输入环境名称', trigger: 'blur' }],
        variablesText: [{ required: true, message: '请输入变量JSON', trigger: 'blur' }]
      },
      userOptions: [],
      userLoading: false,
      userPageNo: 1,
      userPageSize: 10,
      userTotal: 0,
      userHasMore: false,
      hooks: [],
      hookPageNo: 1,
      hookPageSize: 10,
      hookTotal: 0,
      hookLoading: false,
      hookTypeFilter: '',
      hookDialogVisible: false,
      hookDialogMode: 'create',
      hookSubmitting: false,
      hookForm: getDefaultHookForm(),
      hookRules: {
        hookType: [{ required: true, message: '请选择类型', trigger: 'change' }],
        webhookUrl: [{ required: true, message: '请输入 Webhook 地址', trigger: 'blur' }],
        configText: [
          {
            validator: (rule, value, callback) => {
              const s = (value || '').trim()
              if (!s) {
                callback()
                return
              }
              try {
                JSON.parse(s)
                callback()
              } catch (e) {
                callback(new Error('扩展配置须为合法 JSON'))
              }
            },
            trigger: 'blur'
          }
        ]
      }
    }
  },
  methods: {
    goBackToList() {
      this.$router.push({ path: '/test-platform/project' })
    },
    getProjectId() {
      return this.$route.query.projectId || 1
    },
    hookTypeLabel(type) {
      const map = { 1: '飞书', 2: '钉钉', 3: '企微' }
      return map[Number(type)] || type || '-'
    },
    onHookTypeFilterChange() {
      this.hookPageNo = 1
      this.fetchHooks()
    },
    fetchHooks() {
      const projectId = this.getProjectId()
      this.hookLoading = true
      const params = {
        projectId,
        pageNo: this.hookPageNo,
        pageSize: this.hookPageSize
      }
      if (this.hookTypeFilter !== '' && this.hookTypeFilter !== null && this.hookTypeFilter !== undefined) {
        params.hookType = this.hookTypeFilter
      }
      getProjectHookList(params)
        .then(res => {
          const data = (res && res.data) || res || {}
          const list = data.list || data.items || []
          this.hooks = Array.isArray(list) ? list : []
          this.hookTotal = Number(data.total != null ? data.total : this.hooks.length)
        })
        .catch(() => {
          this.hooks = []
          this.hookTotal = 0
        })
        .finally(() => {
          this.hookLoading = false
        })
    },
    openHookDialog(mode, row) {
      this.hookDialogMode = mode
      if (mode === 'create') {
        this.hookForm = getDefaultHookForm()
        this.hookDialogVisible = true
        this.$nextTick(() => {
          if (this.$refs.hookFormRef) this.$refs.hookFormRef.clearValidate()
        })
        return
      }
      const id = row && (row.id != null ? row.id : row.hookId)
      if (id == null) {
        this.$message.warning('缺少 Hook ID')
        return
      }
      getProjectHookDetail(id)
        .then(res => {
          const d = (res && res.data) || res || {}
          const cfg = d.config
          let configText = '{}'
          if (cfg != null && typeof cfg === 'object') {
            try {
              configText = JSON.stringify(cfg, null, 0)
            } catch (e) {
              configText = '{}'
            }
          } else if (typeof cfg === 'string' && cfg.trim()) {
            configText = cfg.trim()
          }
          this.hookForm = {
            hookId: d.id,
            hookType: d.hook_type != null ? d.hook_type : d.hookType,
            webhookUrl: d.webhook_url || d.webhookUrl || '',
            secret: d.secret != null ? String(d.secret) : '',
            enabled: d.enabled === 0 || d.enabled === false ? 0 : 1,
            description: d.description || '',
            configText
          }
          this.hookDialogVisible = true
          this.$nextTick(() => {
            if (this.$refs.hookFormRef) this.$refs.hookFormRef.clearValidate()
          })
        })
        .catch(() => {})
    },
    resetHookForm() {
      this.hookForm = getDefaultHookForm()
      this.hookSubmitting = false
      this.$nextTick(() => {
        if (this.$refs.hookFormRef) this.$refs.hookFormRef.resetFields()
      })
    },
    submitHook() {
      this.$refs.hookFormRef.validate(valid => {
        if (!valid) return
        let config = {}
        const ct = (this.hookForm.configText || '').trim()
        if (ct) {
          try {
            config = JSON.parse(ct)
          } catch (e) {
            this.$message.error('扩展配置 JSON 无效')
            return
          }
        }
        this.hookSubmitting = true
        const done = () => {
          this.hookDialogVisible = false
          this.hookPageNo = 1
          this.fetchHooks()
        }
        if (this.hookDialogMode === 'create') {
          createProjectHook({
            projectId: Number(this.getProjectId()),
            hookType: this.hookForm.hookType,
            webhookUrl: this.hookForm.webhookUrl,
            secret: this.hookForm.secret || undefined,
            enabled: this.hookForm.enabled,
            description: this.hookForm.description || undefined,
            config
          })
            .then(res => {
              if (res && res.code === 20000) {
                this.$message.success((res && res.message) || '创建成功')
                done()
              } else {
                this.$message.error((res && res.message) || '创建失败')
              }
            })
            .finally(() => {
              this.hookSubmitting = false
            })
          return
        }
        const payload = {
          hookId: this.hookForm.hookId,
          hookType: this.hookForm.hookType,
          webhookUrl: this.hookForm.webhookUrl,
          enabled: this.hookForm.enabled,
          description: this.hookForm.description || undefined,
          config
        }
        if (String(this.hookForm.secret || '').trim() !== '') {
          payload.secret = this.hookForm.secret
        }
        updateProjectHook(payload)
          .then(res => {
            if (res && res.code === 20000) {
              this.$message.success((res && res.message) || '更新成功')
              done()
            } else {
              this.$message.error((res && res.message) || '更新失败')
            }
          })
          .finally(() => {
            this.hookSubmitting = false
          })
      })
    },
    handleHookDelete(row) {
      const id = row && (row.id != null ? row.id : row.hookId)
      if (id == null) {
        this.$message.warning('缺少 Hook ID')
        return
      }
      this.$confirm('确认删除该 Hook 配置？', '提示', { type: 'warning' })
        .then(() => deleteProjectHook({ hookId: id }))
        .then(res => {
          if (res && res.code === 20000) {
            this.$message.success((res && res.message) || '已删除')
            this.hookPageNo = 1
            this.fetchHooks()
          } else {
            this.$message.error((res && res.message) || '删除失败')
          }
        })
        .catch(() => {})
    },
    handleHookSizeChange(val) {
      this.hookPageSize = val
      this.hookPageNo = 1
      this.fetchHooks()
    },
    handleHookCurrentChange(val) {
      this.hookPageNo = val
      this.fetchHooks()
    },
    fetchData() {
      const projectId = this.getProjectId()
      getProjectMembers(projectId, {
        pageNo: this.memberPageNo,
        pageSize: this.memberPageSize
      }).then(res => {
        const data = (res && res.data) || res || []
        this.members = data.items || data.list || data.data || data || []
        this.memberTotal = data.total || data.totalCount || this.members.length
      }).catch(() => {
        this.members = []
        this.memberTotal = 0
      })
      getProjectEnvironments(projectId, {
        pageNo: this.environmentPageNo,
        pageSize: this.environmentPageSize
      }).then(res => {
        const data = (res && res.data) || res || []
        this.environments = data.items || data.list || data.data || data || []
        this.environmentTotal = data.total || data.totalCount || this.environments.length
      }).catch(() => {
        this.environments = []
        this.environmentTotal = 0
      })
    },
    openMemberDialog() {
      this.memberDialogVisible = true
      this.userOptions = []
      this.userPageNo = 1
      this.userHasMore = false
      this.$nextTick(() => {
        this.memberForm = getDefaultMemberForm()
        if (this.$refs.memberForm) {
          this.$refs.memberForm.clearValidate()
        }
      })
    },
    resetMemberForm() {
      this.memberForm = getDefaultMemberForm()
      this.memberSubmitting = false
      this.userOptions = []
      this.userPageNo = 1
      this.userHasMore = false
      this.$nextTick(() => {
        if (this.$refs.memberForm) {
          this.$refs.memberForm.resetFields()
        }
      })
    },
    loadMoreUsers() {
      if (this.userHasMore && !this.userLoading) {
        this.userPageNo++
        this.loadUserOptions()
      }
    },
    loadUserOptions() {
      this.userLoading = true
      getUserList({
        pageNo: this.userPageNo,
        pageSize: this.userPageSize,
        keyword: '',
        status: 1
      }).then(res => {
        const data = res && res.data ? res.data : res || {}
        const list = data.list || data.items || data.data || []
        this.userTotal = data.total || data.totalCount || 0
        if (this.userPageNo === 1) {
          this.userOptions = list
        } else {
          this.userOptions = [...this.userOptions, ...list]
        }
        this.userHasMore = this.userOptions.length < this.userTotal
      }).catch(() => {
        this.userOptions = []
        this.userHasMore = false
      }).finally(() => {
        this.userLoading = false
      })
    },
    submitMember() {
      this.$refs.memberForm.validate(valid => {
        if (!valid) {
          return
        }
        if (!this.memberForm.user_ids || this.memberForm.user_ids.length === 0) {
          this.$message.error('请选择用户')
          return
        }
        this.memberSubmitting = true
        createProjectMember({
          project_id: this.getProjectId(),
          user_ids: this.memberForm.user_ids
        }).then(res => {
          const message = (res && res.message) || ''
          if (res && res.code === 20000) {
            this.$message.success(message || '成员新增成功')
            this.memberDialogVisible = false
            this.memberPageNo = 1
            this.fetchData()
            return
          }
          this.$message.error(message || '成员新增失败')
        }).finally(() => {
          this.memberSubmitting = false
        })
      })
    },
    openEnvironmentDialog() {
      this.environmentDialogVisible = true
      this.$nextTick(() => {
        this.environmentForm = getDefaultEnvironmentForm()
        if (this.$refs.environmentForm) {
          this.$refs.environmentForm.clearValidate()
        }
      })
    },
    resetEnvironmentForm() {
      this.environmentForm = getDefaultEnvironmentForm()
      this.environmentSubmitting = false
      this.$nextTick(() => {
        if (this.$refs.environmentForm) {
          this.$refs.environmentForm.resetFields()
        }
      })
    },
    submitEnvironment() {
      this.$refs.environmentForm.validate(valid => {
        if (!valid) {
          return
        }
        let variables = {}
        try {
          variables = JSON.parse(this.environmentForm.variablesText || '{}')
        } catch (e) {
          this.$message.error('变量JSON格式不正确')
          return
        }
        this.environmentSubmitting = true
        createEnvironment({
          project_id: this.getProjectId(),
          name: this.environmentForm.name,
          variables
        }).then(res => {
          const message = (res && res.message) || ''
          if (res && res.code === 20000) {
            this.$message.success(message || '环境新增成功')
            this.environmentDialogVisible = false
            this.environmentPageNo = 1
            this.fetchData()
            return
          }
          this.$message.error(message || '环境新增失败')
        }).finally(() => {
          this.environmentSubmitting = false
        })
      })
    },
    handleMemberSizeChange(val) {
      this.memberPageSize = val
      this.memberPageNo = 1
      this.fetchData()
    },
    handleMemberCurrentChange(val) {
      this.memberPageNo = val
      this.fetchData()
    },
    handleEnvironmentSizeChange(val) {
      this.environmentPageSize = val
      this.environmentPageNo = 1
      this.fetchData()
    },
    handleEnvironmentCurrentChange(val) {
      this.environmentPageNo = val
      this.fetchData()
    }
  },
  created() {
    this.fetchData()
    this.fetchHooks()
  }
}
</script>

<style scoped>
.page-wrap {
  padding: 20px;
}

.toolbar-wrap {
  margin-bottom: 16px;
  text-align: right;
}

.hook-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.hook-toolbar-left {
  text-align: left;
}
</style>
