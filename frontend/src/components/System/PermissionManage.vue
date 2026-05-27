<template>
  <div class="page-wrap">
    <page-section title="权限管理">
      <template slot="extra">
        <el-button type="primary" size="small" @click="openCreate">新建权限</el-button>
      </template>

      <el-form :inline="true" :model="queryForm" size="small" @submit.native.prevent>
        <el-form-item label="关键词">
          <el-input
            v-model.trim="queryForm.keyword"
            placeholder="权限名称"
            clearable
            @keyup.enter.native="handleSearch">
          </el-input>
        </el-form-item>
        <el-form-item label="模块">
          <el-input
            v-model.trim="queryForm.module"
            placeholder="模块"
            clearable
            @keyup.enter.native="handleSearch">
          </el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryForm.status" clearable placeholder="全部状态">
            <el-option label="启用" :value="1"></el-option>
            <el-option label="禁用" :value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table v-loading="loading" :data="tableData" border style="width: 100%; margin-top: 16px;">
        <el-table-column prop="code" label="权限编码" min-width="180"></el-table-column>
        <el-table-column prop="name" label="权限名称" min-width="160"></el-table-column>
        <el-table-column prop="module" label="模块" min-width="120"></el-table-column>
        <el-table-column prop="action" label="操作类型" min-width="120"></el-table-column>
        <el-table-column prop="description" label="描述" min-width="220" show-overflow-tooltip></el-table-column>
        <el-table-column label="状态" width="100">
          <template slot-scope="scope">{{ formatStatus(scope.row.status) }}</template>
        </el-table-column>
        <el-table-column label="创建时间" min-width="170">
          <template slot-scope="scope">{{ formatDateTime(scope.row.created_time || scope.row.createdTime) }}</template>
        </el-table-column>
        <el-table-column label="已有角色" min-width="180">
          <template slot-scope="scope">
            <div v-if="getRolesForRow(scope.row).length" class="role-tag-wrap">
              <el-tag
                v-for="role in getRolesForRow(scope.row)"
                :key="`${scope.row.id || scope.row.permission_id || ''}-${role.id}`"
                size="mini">
                {{ role.name || role.role_name || role.roleName || role.id || '-' }}
              </el-tag>
            </div>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" @click="openAssignRoles(scope.row)">权限分配</el-button>
            <el-button type="text" @click="openEdit(scope.row)">编辑</el-button>
            <el-button type="text" style="color: #F56C6C;" @click="handleDelete(scope.row)">删除</el-button>
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

    <el-dialog :title="dialogMode === 'create' ? '新建权限' : '编辑权限'" :visible.sync="dialogVisible" width="560px" @close="resetDialogForm">
      <el-form ref="permissionForm" :model="permissionForm" :rules="permissionRules" label-width="94px" size="small">
        <el-form-item label="权限编码" prop="code">
          <el-input
            v-model.trim="permissionForm.code"
            maxlength="64"
            placeholder="请输入权限编码"
            :disabled="dialogMode === 'edit'">
          </el-input>
        </el-form-item>
        <el-form-item label="权限名称" prop="name">
          <el-input v-model.trim="permissionForm.name" maxlength="64" placeholder="请输入权限名称"></el-input>
        </el-form-item>
        <el-form-item label="模块" prop="module">
          <el-input v-model.trim="permissionForm.module" maxlength="64" placeholder="请输入模块名"></el-input>
        </el-form-item>
        <el-form-item label="操作类型" prop="action">
          <el-input v-model.trim="permissionForm.action" maxlength="64" placeholder="请输入操作类型"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="permissionForm.status" placeholder="请选择状态" style="width: 100%;">
            <el-option label="启用" :value="1"></el-option>
            <el-option label="禁用" :value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model.trim="permissionForm.description"
            type="textarea"
            :rows="4"
            maxlength="255"
            show-word-limit
            placeholder="请输入描述">
          </el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button size="small" @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="submitting" @click="submitForm">确定</el-button>
      </span>
    </el-dialog>

    <el-dialog title="分配权限到角色" :visible.sync="assignDialogVisible" width="520px" @close="resetAssignDialog">
      <el-form label-width="90px" size="small">
        <el-form-item label="权限">
          <el-input :value="assignPermissionName" disabled></el-input>
        </el-form-item>
        <el-form-item label="角色选择">
          <el-select
            v-model="selectedRoleIds"
            multiple
            filterable
            clearable
            placeholder="请选择角色"
            style="width: 100%;">
            <el-option
              v-for="item in roleOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button size="small" @click="assignDialogVisible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="assignSubmitting" @click="submitAssignRoles">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { assignRolePermissions, createPermission, deletePermission, getPermissionDetail, getPermissionList, getRolePageList, updatePermission } from '@/api/rbacApi'

const getDefaultForm = () => ({
  id: undefined,
  code: '',
  name: '',
  module: '',
  action: '',
  description: '',
  status: 1
})

export default {
  name: 'PermissionManage',
  components: { PageSection },
  data() {
    return {
      loading: false,
      submitting: false,
      assignSubmitting: false,
      dialogVisible: false,
      assignDialogVisible: false,
      dialogMode: 'create',
      queryForm: {
        keyword: '',
        module: '',
        status: ''
      },
      pageNo: 1,
      pageSize: 20,
      total: 0,
      tableData: [],
      roleOptions: [],
      assignPermissionId: undefined,
      assignPermissionName: '',
      selectedRoleIds: [],
      permissionForm: getDefaultForm(),
      permissionRules: {
        code: [{ required: true, message: '请输入权限编码', trigger: 'blur' }],
        name: [{ required: true, message: '请输入权限名称', trigger: 'blur' }],
        status: [{ required: true, message: '请选择状态', trigger: 'change' }]
      }
    }
  },
  methods: {
    fetchList() {
      this.loading = true
      getPermissionList({
        keyword: this.queryForm.keyword,
        module: this.queryForm.module,
        status: this.queryForm.status,
        pageNo: this.pageNo,
        pageSize: this.pageSize
      }).then(res => {
        const data = (res && res.data) || res || {}
        this.tableData = data.list || data.items || data.data || []
        this.total = Number(data.total || data.totalCount || this.tableData.length || 0)
      }).catch(() => {
        this.tableData = []
        this.total = 0
      }).finally(() => {
        this.loading = false
      })
    },
    handleSearch() {
      this.pageNo = 1
      this.fetchList()
    },
    resetSearch() {
      this.queryForm = {
        keyword: '',
        module: '',
        status: ''
      }
      this.pageNo = 1
      this.fetchList()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.pageNo = 1
      this.fetchList()
    },
    handleCurrentChange(val) {
      this.pageNo = val
      this.fetchList()
    },
    openCreate() {
      this.dialogMode = 'create'
      this.dialogVisible = true
      this.$nextTick(() => {
        this.permissionForm = getDefaultForm()
        if (this.$refs.permissionForm) {
          this.$refs.permissionForm.clearValidate()
        }
      })
    },
    openEdit(row) {
      const permissionId = row.permissionId || row.permission_id || row.id
      this.dialogMode = 'edit'
      this.dialogVisible = true
      this.$nextTick(() => {
        this.permissionForm = Object.assign(getDefaultForm(), row, { id: permissionId })
        if (this.$refs.permissionForm) {
          this.$refs.permissionForm.clearValidate()
        }
      })
      if (!permissionId) return
      getPermissionDetail(permissionId).then(res => {
        const data = (res && res.data) || res || {}
        this.permissionForm = Object.assign(getDefaultForm(), data, {
          id: data.id || data.permissionId || data.permission_id || permissionId
        })
      }).catch(() => {})
    },
    openAssignRoles(row) {
      const permissionId = row.permissionId || row.permission_id || row.id
      if (!permissionId) return
      this.assignPermissionId = permissionId
      this.assignPermissionName = row.name || row.code || `权限#${permissionId}`
      const roles = this.getRolesForRow(row)
      this.selectedRoleIds = roles
        .map(r => this.normalizeRoleId(r.id !== undefined && r.id !== null ? r.id : r.roleId))
        .filter(id => id !== null && id !== undefined)
      this.assignDialogVisible = true
      this.fetchRoleOptions().then(() => {
        const optionIdSet = new Set(this.roleOptions.map(o => this.normalizeRoleId(o.id)))
        roles.forEach(r => {
          const rawId = r.id !== undefined && r.id !== null ? r.id : r.roleId
          const nid = this.normalizeRoleId(rawId)
          if (nid === null || nid === undefined) return
          if (!optionIdSet.has(nid)) {
            this.roleOptions.push({
              id: nid,
              name: r.name || r.role_name || r.roleName || String(rawId)
            })
            optionIdSet.add(nid)
          }
        })
        this.$nextTick(() => {
          this.selectedRoleIds = roles
            .map(r => this.normalizeRoleId(r.id !== undefined && r.id !== null ? r.id : r.roleId))
            .filter(id => id !== null && id !== undefined)
        })
      })
    },
    normalizeRoleId(id) {
      if (id === undefined || id === null || id === '') return null
      const n = Number(id)
      return Number.isFinite(n) && String(id) === String(n) ? n : id
    },
    fetchRoleOptions() {
      return getRolePageList({ pageNo: 1, pageSize: 9999 }).then(res => {
        const data = (res && res.data) || res || {}
        const list = data.list || data.items || data.data || []
        this.roleOptions = (Array.isArray(list) ? list : []).map(item => ({
          id: this.normalizeRoleId(item.id !== undefined && item.id !== null ? item.id : item.roleId),
          name: item.name || item.code || `角色${item.id || item.roleId}`
        })).filter(item => item.id !== undefined && item.id !== null)
      }).catch(() => {
        this.roleOptions = []
      })
    },
    resetAssignDialog() {
      this.assignSubmitting = false
      this.assignPermissionId = undefined
      this.assignPermissionName = ''
      this.selectedRoleIds = []
    },
    submitAssignRoles() {
      if (!this.assignPermissionId) return
      if (!this.selectedRoleIds.length) {
        this.$message.warning('请至少选择一个角色')
        return
      }
      const permissionId = Number(this.assignPermissionId)
      if (Number.isNaN(permissionId)) {
        this.$message.warning('权限 ID 无效')
        return
      }
      const roleIds = Array.from(new Set(
        (this.selectedRoleIds || []).map(id => Number(id)).filter(id => !Number.isNaN(id))
      ))
      if (!roleIds.length) {
        this.$message.warning('请至少选择一个有效角色')
        return
      }
      this.assignSubmitting = true
      assignRolePermissions({
        roleIds,
        permissionId
      }).then(res => {
        if (res && res.code && res.code !== 20000) {
          this.$message.error((res && res.message) || '权限分配失败')
          return
        }
        const data = (res && res.data) || {}
        const assignedCount = data.id
        if (assignedCount !== undefined && assignedCount !== null && assignedCount !== '') {
          this.$message.success(`权限分配成功，本次处理角色数：${assignedCount}`)
        } else {
          this.$message.success((res && res.message) || '权限分配成功')
        }
        this.assignDialogVisible = false
        this.fetchList()
      }).finally(() => {
        this.assignSubmitting = false
      })
    },
    getRolesForRow(row) {
      if (!row) return []
      const roles = row.roles
      return Array.isArray(roles) ? roles : []
    },
    resetDialogForm() {
      this.permissionForm = getDefaultForm()
      this.submitting = false
      this.$nextTick(() => {
        if (this.$refs.permissionForm) {
          this.$refs.permissionForm.resetFields()
        }
      })
    },
    submitForm() {
      this.$refs.permissionForm.validate(valid => {
        if (!valid) {
          return
        }
        this.submitting = true
        const basePayload = {
          code: this.permissionForm.code,
          name: this.permissionForm.name,
          module: this.permissionForm.module,
          action: this.permissionForm.action,
          description: this.permissionForm.description,
          status: Number(this.permissionForm.status)
        }
        const payload = this.dialogMode === 'create'
          ? basePayload
          : Object.assign({
            id: this.permissionForm.id,
            permissionId: this.permissionForm.id,
            permission_id: this.permissionForm.id
          }, basePayload)
        const request = this.dialogMode === 'create'
          ? createPermission(payload)
          : updatePermission(payload)
        request.then(res => {
          if (res && res.code && res.code !== 20000) {
            this.$message.error((res && res.message) || (this.dialogMode === 'create' ? '权限创建失败' : '权限更新失败'))
            return
          }
          this.$message.success((res && res.message) || (this.dialogMode === 'create' ? '权限创建成功' : '权限更新成功'))
          this.dialogVisible = false
          this.pageNo = 1
          this.fetchList()
        }).finally(() => {
          this.submitting = false
        })
      })
    },
    handleDelete(row) {
      const permissionId = row.permissionId || row.permission_id || row.id
      if (!permissionId) return
      this.$confirm('确认删除该权限吗？', '提示', { type: 'warning' }).then(() => {
        return deletePermission({
          id: permissionId,
          permissionId: permissionId,
          permission_id: permissionId
        }).then(res => {
          if (res && res.code && res.code !== 20000) {
            this.$message.error((res && res.message) || '权限删除失败')
            return
          }
          this.$message.success((res && res.message) || '权限删除成功')
          if (this.tableData.length === 1 && this.pageNo > 1) {
            this.pageNo = this.pageNo - 1
          }
          this.fetchList()
        })
      }).catch(() => {})
    },
    formatStatus(value) {
      return Number(value) === 0 ? '禁用' : '启用'
    },
    formatDateTime(value) {
      if (!value) return '-'
      return String(value).replace('T', ' ').slice(0, 19)
    }
  },
  created() {
    this.fetchList()
  }
}
</script>

<style scoped>
.page-wrap {
  padding: 20px;
}

.role-tag-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  line-height: 1.4;
}
</style>
