<template>
  <div class="page-wrap">
    <page-section title="角色管理">
      <template slot="extra">
        <el-button type="primary" size="small" @click="openCreate">新建角色</el-button>
      </template>
      <el-form :inline="true" :model="queryForm" size="small" @submit.native.prevent>
        <el-form-item label="关键词">
          <el-input v-model="queryForm.keyword" placeholder="角色名称" clearable @keyup.enter.native="handleSearch"></el-input>
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
        <el-table-column prop="code" label="角色编码" min-width="140"></el-table-column>
        <el-table-column prop="name" label="角色名称" min-width="160"></el-table-column>
        <el-table-column prop="description" label="描述" min-width="220" show-overflow-tooltip></el-table-column>
        <el-table-column prop="is_system" label="系统角色" width="100">
          <template slot-scope="scope">{{ (scope.row.is_system !== undefined ? scope.row.is_system : scope.row.isSystem) === 1 ? '是' : '否' }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">{{ scope.row.status === 0 ? '禁用' : '启用' }}</template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" @click="openAssignMenus(scope.row)">分配菜单</el-button>
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

    <el-dialog :title="dialogMode === 'create' ? '新建角色' : '编辑角色'" :visible.sync="dialogVisible" width="520px" @close="resetDialogForm">
      <el-form ref="roleForm" :model="roleForm" :rules="roleRules" label-width="94px" size="small">
        <el-form-item label="角色编码" prop="code">
          <el-input v-model.trim="roleForm.code" maxlength="64" placeholder="请输入角色编码" :disabled="dialogMode === 'edit'"></el-input>
        </el-form-item>
        <el-form-item label="角色名称" prop="name">
          <el-input v-model.trim="roleForm.name" maxlength="64" placeholder="请输入角色名称"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="roleForm.status" placeholder="请选择状态" style="width: 100%;">
            <el-option label="启用" :value="1"></el-option>
            <el-option label="禁用" :value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="系统角色" prop="isSystem">
          <el-select v-model="roleForm.isSystem" placeholder="请选择" style="width: 100%;" :disabled="dialogMode === 'edit'">
            <el-option label="否" :value="0"></el-option>
            <el-option label="是" :value="1"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model.trim="roleForm.description" type="textarea" :rows="4" maxlength="255" show-word-limit placeholder="请输入描述"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button size="small" @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="submitting" @click="submitForm">确定</el-button>
      </span>
    </el-dialog>

    <el-dialog title="分配菜单权限" :visible.sync="assignDialogVisible" width="620px" @close="resetAssignForm">
      <el-form label-width="90px" size="small">
        <el-form-item label="角色">
          <el-input :value="assignRoleName" disabled></el-input>
        </el-form-item>
        <el-form-item label="菜单权限">
          <el-tree
            ref="menuTree"
            :data="menuTreeData"
            node-key="id"
            show-checkbox
            default-expand-all
            :props="treeProps">
          </el-tree>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button size="small" @click="assignDialogVisible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="assignSubmitting" @click="submitAssignMenus">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { assignRoleMenus, createRole, deleteRole, getMenuTree, getRoleMenuList, getRoleMenuTree, getRolePageList, updateRole } from '@/api/rbacApi'

const getDefaultForm = () => ({
  roleId: undefined,
  code: '',
  name: '',
  description: '',
  status: 1,
  isSystem: 0,
  createdBy: 1
})

export default {
  name: 'RoleManage',
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
      roleForm: getDefaultForm(),
      roleRules: {
        code: [{ required: true, message: '请输入角色编码', trigger: 'blur' }],
        name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
        status: [{ required: true, message: '请选择状态', trigger: 'change' }]
      },
      pageNo: 1,
      pageSize: 10,
      total: 0,
      tableData: [],
      assignRoleId: undefined,
      assignRoleName: '',
      menuTreeData: [],
      treeProps: {
        children: 'children',
        label: 'name'
      }
    }
  },
  methods: {
    fetchList() {
      this.loading = true
      getRolePageList({
        pageNo: this.pageNo,
        pageSize: this.pageSize,
        keyword: this.queryForm.keyword,
        status: this.queryForm.status
      }).then(res => {
        const data = res && res.data ? res.data : res || {}
        this.tableData = Array.isArray(data) ? data : (data.items || data.list || data.data || [])
        this.total = Array.isArray(data) ? data.length : (data.total || data.totalCount || this.tableData.length)
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
        this.roleForm = getDefaultForm()
        if (this.$refs.roleForm) {
          this.$refs.roleForm.clearValidate()
        }
      })
    },
    openEdit(row) {
      this.dialogMode = 'edit'
      this.dialogVisible = true
      this.$nextTick(() => {
        this.roleForm = Object.assign(getDefaultForm(), row, {
          roleId: row.roleId || row.id,
          isSystem: row.isSystem !== undefined ? row.isSystem : (row.is_system || 0)
        })
        if (this.$refs.roleForm) {
          this.$refs.roleForm.clearValidate()
        }
      })
    },
    openAssignMenus(row) {
      this.assignRoleId = row.roleId || row.id
      this.assignRoleName = row.name
      this.assignDialogVisible = true
      Promise.all([getMenuTree({}), getRoleMenuList(this.assignRoleId)]).then(([menuRes, assignRes]) => {
        const menuData = menuRes && menuRes.data ? menuRes.data : menuRes || []
        this.menuTreeData = Array.isArray(menuData) ? menuData : (menuData.list || menuData.items || [])
        const assignData = assignRes && assignRes.data ? assignRes.data : assignRes || {}
        const menuIds = Array.isArray(assignData)
          ? assignData.map(item => item.menuId || item.id)
          : (assignData.menuIds || assignData.menu_ids || [])
        this.$nextTick(() => {
          if (this.$refs.menuTree) {
            this.$refs.menuTree.setCheckedKeys(menuIds)
          }
        })
      }).catch(() => {
        this.menuTreeData = []
      })
    },
    resetDialogForm() {
      this.roleForm = getDefaultForm()
      this.submitting = false
      this.$nextTick(() => {
        if (this.$refs.roleForm) {
          this.$refs.roleForm.resetFields()
        }
      })
    },
    resetAssignForm() {
      this.assignSubmitting = false
      this.assignRoleId = undefined
      this.assignRoleName = ''
      this.menuTreeData = []
    },
    submitForm() {
      this.$refs.roleForm.validate(valid => {
        if (!valid) {
          return
        }
        this.submitting = true
        const payload = this.dialogMode === 'create'
          ? this.roleForm
          : {
            roleId: this.roleForm.roleId,
            name: this.roleForm.name,
            description: this.roleForm.description,
            status: this.roleForm.status
          }
        const request = this.dialogMode === 'create'
          ? createRole(payload)
          : updateRole(payload)
        request.then(res => {
          if (res && res.code === 20000) {
            this.$message.success((res && res.message) || (this.dialogMode === 'create' ? '角色创建成功' : '角色更新成功'))
            this.dialogVisible = false
            this.pageNo = 1
            this.fetchList()
            return
          }
          this.$message.error((res && res.message) || (this.dialogMode === 'create' ? '角色创建失败' : '角色更新失败'))
        }).finally(() => {
          this.submitting = false
        })
      })
    },
    submitAssignMenus() {
      this.assignSubmitting = true
      const checkedKeys = this.$refs.menuTree ? this.$refs.menuTree.getCheckedKeys() : []
      const halfCheckedKeys = this.$refs.menuTree ? this.$refs.menuTree.getHalfCheckedKeys() : []
      const menuIds = Array.from(new Set([].concat(checkedKeys, halfCheckedKeys)))
      assignRoleMenus({
        roleId: this.assignRoleId,
        menuIds
      }).then(res => {
        if (res && res.code !== 20000) {
          this.$message.error((res && res.message) || '分配菜单失败')
          return
        }
        this.$message.success((res && res.message) || '分配菜单成功')
        this.assignDialogVisible = false
      }).finally(() => {
        this.assignSubmitting = false
      })
    },
    handleDelete(row) {
      this.$confirm('确认删除该角色吗？', '提示', {
        type: 'warning'
      }).then(() => {
        deleteRole({ roleId: row.roleId || row.id }).then(res => {
          if (res && res.code !== 20000) {
            this.$message.error((res && res.message) || '角色删除失败')
            return
          }
          this.$message.success((res && res.message) || '角色删除成功')
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

  created() {
    this.fetchList()
  }
}

<style scoped>
.page-wrap {
  padding: 20px;
}
</style>
reated() {
    this.fetchList()
  }
}

<style scoped>
.page-wrap {
  padding: 20px;
}
</style>
