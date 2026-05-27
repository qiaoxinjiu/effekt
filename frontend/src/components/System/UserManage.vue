<template>
  <div class="page-wrap">
    <page-section title="用户管理">
      <template slot="extra">
        <el-button type="primary" size="small" @click="openCreate">新建用户</el-button>
      </template>
      <el-form :inline="true" :model="queryForm" size="small" @submit.native.prevent>
        <el-form-item label="关键词">
          <el-input v-model="queryForm.keyword" placeholder="用户名" clearable @keyup.enter.native="handleSearch"></el-input>
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
        <el-table-column prop="username" label="用户名" min-width="140"></el-table-column>
        <el-table-column prop="real_name" label="姓名" min-width="120">
          <template slot-scope="scope">{{ scope.row.real_name || scope.row.realName }}</template>
        </el-table-column>
        <el-table-column prop="mobile" label="手机号" min-width="140"></el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip></el-table-column>
        <el-table-column label="角色" min-width="180" show-overflow-tooltip>
          <template slot-scope="scope">{{ getRoleNames(scope.row) }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">{{ scope.row.status === 0 ? '禁用' : '启用' }}</template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" @click="openAssignRoles(scope.row)">分配角色</el-button>
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

    <el-dialog :title="dialogMode === 'create' ? '新建用户' : '编辑用户'" :visible.sync="dialogVisible" width="620px" @close="resetDialogForm">
      <el-form ref="userForm" :model="userForm" :rules="userRules" label-width="100px" size="small">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input v-model.trim="userForm.username" maxlength="64" placeholder="请输入用户名" :disabled="dialogMode === 'edit'"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="密码" prop="password">
              <el-input v-model.trim="userForm.password" maxlength="64" placeholder="请输入密码" :disabled="dialogMode === 'edit'"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="姓名" prop="realName">
              <el-input v-model.trim="userForm.realName" maxlength="64" placeholder="请输入姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号" prop="mobile">
              <el-input v-model.trim="userForm.mobile" maxlength="20" placeholder="请输入手机号"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model.trim="userForm.email" maxlength="128" placeholder="请输入邮箱"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="userForm.status" placeholder="请选择状态" style="width: 100%;">
                <el-option label="启用" :value="1"></el-option>
                <el-option label="禁用" :value="0"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="头像" prop="avatar">
          <el-input v-model.trim="userForm.avatar" maxlength="255" placeholder="请输入头像地址"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button size="small" @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="submitting" @click="submitForm">确定</el-button>
      </span>
    </el-dialog>

    <el-dialog title="分配角色" :visible.sync="assignDialogVisible" width="520px" @close="resetAssignForm">
      <el-form label-width="90px" size="small">
        <el-form-item label="用户">
          <el-input :value="assignUserName" disabled></el-input>
        </el-form-item>
        <el-form-item label="角色选择">
          <el-select v-model="selectedRoleIds" multiple filterable clearable collapse-tags placeholder="请选择角色" style="width: 100%;">
            <el-option v-for="item in roleOptions" :key="item.id" :label="item.name" :value="item.id"></el-option>
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
import { assignUserRoles, createUser, deleteUser, getRolePageList, getUserList, getUserRoleList, updateUser } from '@/api/rbacApi'

const getDefaultForm = () => ({
  userId: undefined,
  username: '',
  password: '',
  realName: '',
  mobile: '',
  email: '',
  avatar: '',
  status: 1,
  createdBy: 1
})

export default {
  name: 'UserManage',
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
        status: ''
      },
      userForm: getDefaultForm(),
      userRules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
        realName: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
        status: [{ required: true, message: '请选择状态', trigger: 'change' }]
      },
      pageNo: 1,
      pageSize: 10,
      total: 0,
      tableData: [],
      roleOptions: [],
      assignUserId: undefined,
      assignUserName: '',
      selectedRoleIds: []
    }
  },
  methods: {
    fetchList() {
      this.loading = true
      getUserList({
        pageNo: this.pageNo,
        pageSize: this.pageSize,
        keyword: this.queryForm.keyword,
        status: this.queryForm.status
      }).then(res => {
        const data = res && res.data ? res.data : res || {}
        this.tableData = data.items || data.list || data.data || []
        this.total = data.total || data.totalCount || this.tableData.length
      }).catch(() => {
        this.tableData = []
        this.total = 0
      }).finally(() => {
        this.loading = false
      })
    },
    fetchRoleOptions() {
      return getRolePageList({ pageNo: 1, pageSize: 9999 }).then(res => {
        const data = res && res.data ? res.data : res || {}
        const list = data.list || data.items || data.data || []
        this.roleOptions = list.map(item => ({
          id: item.id,
          name: item.name
        }))
      }).catch(() => {
        this.roleOptions = []
      })
    },
    getRoleNames(row) {
      const roleNames = row.role_names || row.roleNames || []
      return Array.isArray(roleNames) ? roleNames.join('，') : ''
    },
    handleSearch() {
      this.pageNo = 1
      this.fetchList()
    },
    resetSearch() {
      this.queryForm = {
        keyword: '',
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
        this.userForm = getDefaultForm()
        if (this.$refs.userForm) {
          this.$refs.userForm.clearValidate()
        }
      })
    },
    openEdit(row) {
      this.dialogMode = 'edit'
      this.dialogVisible = true
      this.$nextTick(() => {
        this.userForm = Object.assign(getDefaultForm(), row, {
          userId: row.userId || row.id,
          realName: row.realName || row.real_name || '',
          password: ''
        })
        if (this.$refs.userForm) {
          this.$refs.userForm.clearValidate()
        }
      })
    },
    openAssignRoles(row) {
      this.assignUserId = row.userId || row.id
      this.assignUserName = row.username
      this.assignDialogVisible = true
      this.fetchRoleOptions()
      getUserRoleList(this.assignUserId).then(res => {
        const data = res && res.data ? res.data : res || {}
        const roleIds = data.roleIds || data.role_ids || []
        this.selectedRoleIds = roleIds.map(id => Number(id))
      }).catch(() => {
        this.selectedRoleIds = []
      })
    },
    resetDialogForm() {
      this.userForm = getDefaultForm()
      this.submitting = false
      this.$nextTick(() => {
        if (this.$refs.userForm) {
          this.$refs.userForm.resetFields()
        }
      })
    },
    resetAssignForm() {
      this.assignSubmitting = false
      this.assignUserId = undefined
      this.assignUserName = ''
      this.selectedRoleIds = []
    },
    submitForm() {
      this.$refs.userForm.validate(valid => {
        if (!valid) {
          return
        }
        this.submitting = true
        const payload = this.dialogMode === 'create'
          ? this.userForm
          : {
            userId: this.userForm.userId,
            realName: this.userForm.realName,
            mobile: this.userForm.mobile,
            email: this.userForm.email,
            avatar: this.userForm.avatar,
            status: this.userForm.status
          }
        const request = this.dialogMode === 'create'
          ? createUser(payload)
          : updateUser(payload)
        request.then(res => {
          if (res && res.code === 20000) {
            this.$message.success((res && res.message) || (this.dialogMode === 'create' ? '用户创建成功' : '用户更新成功'))
            this.dialogVisible = false
            this.pageNo = 1
            this.fetchList()
            return
          }
          this.$message.error((res && res.message) || (this.dialogMode === 'create' ? '用户创建失败' : '用户更新失败'))
        }).finally(() => {
          this.submitting = false
        })
      })
    },
    submitAssignRoles() {
      this.assignSubmitting = true
      assignUserRoles({
        userId: this.assignUserId,
        roleIds: this.selectedRoleIds
      }).then(res => {
        if (res && res.code !== 20000) {
          this.$message.error((res && res.message) || '分配角色失败')
          return
        }
        this.$message.success((res && res.message) || '分配角色成功')
        this.assignDialogVisible = false
        this.fetchList()
      }).finally(() => {
        this.assignSubmitting = false
      })
    },
    handleDelete(row) {
      this.$confirm('确认删除该用户吗？', '提示', {
        type: 'warning'
      }).then(() => {
        deleteUser({ userId: row.userId || row.id }).then(res => {
          if (res && res.code !== 20000) {
            this.$message.error((res && res.message) || '用户删除失败')
            return
          }
          this.$message.success((res && res.message) || '用户删除成功')
          if (this.tableData.length === 1 && this.pageNo > 1) {
            this.pageNo = this.pageNo - 1
          }
          this.fetchList()
        })
      }).catch(() => {})
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
</style>
