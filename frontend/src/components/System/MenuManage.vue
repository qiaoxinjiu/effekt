<template>
  <div class="page-wrap">
    <page-section title="菜单管理">
      <template slot="extra">
        <el-button size="small" :loading="initPermissionMenuLoading" @click="initPermissionMenu">初始化权限管理菜单</el-button>
        <el-button size="small" :loading="initBugMenuLoading" @click="initBugManagementMenu">初始化 Bug 管理菜单</el-button>
        <el-button type="primary" size="small" @click="openCreate(0)">新建菜单</el-button>
      </template>
      <el-form :inline="true" :model="queryForm" size="small" @submit.native.prevent>
        <el-form-item label="状态">
          <el-select v-model="queryForm.status" clearable placeholder="全部状态">
            <el-option label="启用" :value="1"></el-option>
            <el-option label="禁用" :value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchTree">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      <el-table
        v-loading="loading"
        :data="tableData"
        border
        row-key="id"
        default-expand-all
        :tree-props="{ children: 'children' }"
        style="width: 100%; margin-top: 16px;">
        <el-table-column prop="name" label="菜单名称" min-width="180"></el-table-column>
        <el-table-column prop="code" label="菜单编码" min-width="160"></el-table-column>
        <el-table-column prop="type" label="类型" width="90">
          <template slot-scope="scope">{{ formatType(scope.row.type) }}</template>
        </el-table-column>
        <el-table-column prop="path" label="路径" min-width="180" show-overflow-tooltip></el-table-column>
        <el-table-column prop="component" label="组件" min-width="180" show-overflow-tooltip></el-table-column>
        <el-table-column label="权限标识" min-width="160" show-overflow-tooltip>
          <template slot-scope="scope">{{ scope.row.permission_code || scope.row.permissionCode }}</template>
        </el-table-column>
        <el-table-column prop="sort" label="排序" width="80"></el-table-column>
        <el-table-column prop="visible" label="显示" width="80">
          <template slot-scope="scope">{{ scope.row.visible === 0 ? '否' : '是' }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="80">
          <template slot-scope="scope">{{ scope.row.status === 0 ? '禁用' : '启用' }}</template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" @click="openCreate(scope.row.id)">新增下级</el-button>
            <el-button type="text" @click="openEdit(scope.row)">编辑</el-button>
            <el-button type="text" style="color: #F56C6C;" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </page-section>

    <el-dialog :title="dialogMode === 'create' ? '新建菜单' : '编辑菜单'" :visible.sync="dialogVisible" width="620px" @close="resetDialogForm">
      <el-form ref="menuForm" :model="menuForm" :rules="menuRules" label-width="100px" size="small">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="上级菜单" prop="parentId">
              <el-input :value="getParentName(menuForm.parentId)" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="菜单类型" prop="type">
              <el-select v-model="menuForm.type" placeholder="请选择类型" style="width: 100%;">
                <el-option label="目录" :value="1"></el-option>
                <el-option label="菜单" :value="2"></el-option>
                <el-option label="按钮" :value="3"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="菜单名称" prop="name">
              <el-input v-model.trim="menuForm.name" maxlength="64" placeholder="请输入菜单名称"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="菜单编码" prop="code">
              <el-input v-model.trim="menuForm.code" maxlength="64" placeholder="请输入菜单编码"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="访问路径" prop="path">
              <el-input v-model.trim="menuForm.path" maxlength="128" placeholder="请输入访问路径"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="组件路径" prop="component">
              <el-input v-model.trim="menuForm.component" maxlength="128" placeholder="请输入组件路径"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="图标" prop="icon">
              <el-input v-model.trim="menuForm.icon" maxlength="64" placeholder="请输入图标"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="权限标识" prop="permissionCode">
              <el-input v-model.trim="menuForm.permissionCode" maxlength="64" placeholder="请输入权限标识"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="排序" prop="sort">
              <el-input-number v-model="menuForm.sort" :min="0" :max="9999" controls-position="right" style="width: 100%;"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="是否显示" prop="visible">
              <el-select v-model="menuForm.visible" placeholder="请选择" style="width: 100%;">
                <el-option label="是" :value="1"></el-option>
                <el-option label="否" :value="0"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="状态" prop="status">
              <el-select v-model="menuForm.status" placeholder="请选择" style="width: 100%;">
                <el-option label="启用" :value="1"></el-option>
                <el-option label="禁用" :value="0"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer">
        <el-button size="small" @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="submitting" @click="submitForm">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { createMenu, deleteMenu, getMenuTree, updateMenu } from '@/api/rbacApi'

const getDefaultForm = () => ({
  menuId: undefined,
  parentId: 0,
  name: '',
  code: '',
  type: 2,
  path: '',
  component: '',
  icon: '',
  permissionCode: '',
  sort: 0,
  visible: 1,
  status: 1
})

export default {
  name: 'MenuManage',
  components: { PageSection },
  data() {
    return {
      loading: false,
      submitting: false,
      initPermissionMenuLoading: false,
      initBugMenuLoading: false,
      dialogVisible: false,
      dialogMode: 'create',
      queryForm: {
        status: ''
      },
      menuForm: getDefaultForm(),
      menuRules: {
        name: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
        code: [{ required: true, message: '请输入菜单编码', trigger: 'blur' }],
        type: [{ required: true, message: '请选择菜单类型', trigger: 'change' }],
        sort: [{ required: true, message: '请输入排序', trigger: 'change' }],
        status: [{ required: true, message: '请选择状态', trigger: 'change' }]
      },
      tableData: []
    }
  },
  methods: {
    fetchTree() {
      this.loading = true
      getMenuTree({ status: this.queryForm.status }).then(res => {
        const data = res && res.data ? res.data : res || []
        this.tableData = Array.isArray(data) ? data : (data.list || data.items || [])
      }).catch(() => {
        this.tableData = []
      }).finally(() => {
        this.loading = false
      })
    },
    resetSearch() {
      this.queryForm = {
        status: ''
      }
      this.fetchTree()
    },
    formatType(type) {
      const map = {
        1: '目录',
        2: '菜单',
        3: '按钮'
      }
      return map[type] || type
    },
    flattenMenus(list, result) {
      (list || []).forEach(item => {
        result.push(item)
        if (item.children && item.children.length) {
          this.flattenMenus(item.children, result)
        }
      })
    },
    getParentName(parentId) {
      if (!parentId) {
        return '顶级菜单'
      }
      const result = []
      this.flattenMenus(this.tableData, result)
      const target = result.find(item => item.id === parentId)
      return target ? target.name : '顶级菜单'
    },
    openCreate(parentId) {
      this.dialogMode = 'create'
      this.dialogVisible = true
      this.$nextTick(() => {
        this.menuForm = Object.assign(getDefaultForm(), { parentId: parentId || 0, sort: 0 })
        if (this.$refs.menuForm) {
          this.$refs.menuForm.clearValidate()
        }
      })
    },
    openEdit(row) {
      this.dialogMode = 'edit'
      this.dialogVisible = true
      this.$nextTick(() => {
        this.menuForm = Object.assign(getDefaultForm(), row, {
          menuId: row.menuId || row.id,
          parentId: row.parentId !== undefined ? row.parentId : (row.parent_id || 0),
          permissionCode: row.permissionCode !== undefined ? row.permissionCode : (row.permission_code || ''),
          sort: row.sort !== undefined && row.sort !== null ? Number(row.sort) : 0
        })
        if (this.$refs.menuForm) {
          this.$refs.menuForm.clearValidate()
        }
      })
    },
    resetDialogForm() {
      this.menuForm = getDefaultForm()
      this.submitting = false
      this.$nextTick(() => {
        if (this.$refs.menuForm) {
          this.$refs.menuForm.resetFields()
        }
      })
    },
    submitForm() {
      this.$refs.menuForm.validate(valid => {
        if (!valid) {
          return
        }
        this.submitting = true
        const basePayload = {
          parentId: Number(this.menuForm.parentId || 0),
          name: this.menuForm.name,
          code: this.menuForm.code,
          type: Number(this.menuForm.type),
          path: this.menuForm.path,
          component: this.menuForm.component,
          icon: this.menuForm.icon,
          permissionCode: this.menuForm.permissionCode,
          sort: Number(this.menuForm.sort || 0),
          visible: Number(this.menuForm.visible),
          status: Number(this.menuForm.status)
        }
        const payload = this.dialogMode === 'create'
          ? basePayload
          : Object.assign({ menuId: Number(this.menuForm.menuId) }, basePayload)
        const request = this.dialogMode === 'create'
          ? createMenu(payload)
          : updateMenu(payload)
        request.then(res => {
          if (res && res.code === 20000) {
            this.$message.success((res && res.message) || (this.dialogMode === 'create' ? '菜单创建成功' : '菜单更新成功'))
            this.dialogVisible = false
            this.fetchTree()
            return
          }
          this.$message.error((res && res.message) || (this.dialogMode === 'create' ? '菜单创建失败' : '菜单更新失败'))
        }).finally(() => {
          this.submitting = false
        })
      })
    },
    handleDelete(row) {
      this.$confirm('确认删除该菜单吗？', '提示', {
        type: 'warning'
      }).then(() => {
        deleteMenu({ menuId: row.menuId || row.id }).then(res => {
          if (res && res.code !== 20000) {
            this.$message.error((res && res.message) || '菜单删除失败')
            return
          }
          this.$message.success((res && res.message) || '菜单删除成功')
          this.fetchTree()
        })
      }).catch(() => {})
    },
    initPermissionMenu() {
      this.initPermissionMenuLoading = true
      getMenuTree({}).then(res => {
        const data = res && res.data ? res.data : res || []
        const tree = Array.isArray(data) ? data : (data.list || data.items || [])
        const flattened = []
        this.flattenMenus(tree, flattened)

        let systemMenu = flattened.find(item => {
          const path = item.path || ''
          const name = item.name || ''
          return path === '/system' || name === '系统管理'
        })
        const hasPermissionMenu = flattened.some(item => (item.path || '') === '/system/permission')

        const createPermissionChild = parentId => {
          if (hasPermissionMenu) {
            this.$message.success('权限管理菜单已存在')
            return Promise.resolve()
          }
          return createMenu({
            parentId: Number(parentId || 0),
            name: '权限管理',
            code: 'system_permission_manage',
            type: 2,
            path: '/system/permission',
            component: '@/components/System/PermissionManage',
            icon: 'lock',
            permissionCode: 'permission:list',
            sort: 40,
            visible: 1,
            status: 1
          })
        }

        if (systemMenu) {
          return createPermissionChild(systemMenu.id || systemMenu.menuId)
        }

        return createMenu({
          parentId: 0,
          name: '系统管理',
          code: 'system_manage',
          type: 1,
          path: '/system',
          component: '',
          icon: 'setting',
          permissionCode: '',
          sort: 90,
          visible: 1,
          status: 1
        }).then(createRes => {
          const created = (createRes && createRes.data) || {}
          const parentId = created.id || created.menuId
          if (parentId) {
            return createPermissionChild(parentId)
          }
          // 如果接口不返回id，则重新拉取菜单树定位系统管理菜单
          return getMenuTree({}).then(latestRes => {
            const latestData = latestRes && latestRes.data ? latestRes.data : latestRes || []
            const latestTree = Array.isArray(latestData) ? latestData : (latestData.list || latestData.items || [])
            const latestFlattened = []
            this.flattenMenus(latestTree, latestFlattened)
            const latestSystem = latestFlattened.find(item => (item.path || '') === '/system' || (item.name || '') === '系统管理')
            return createPermissionChild(latestSystem ? (latestSystem.id || latestSystem.menuId) : 0)
          })
        })
      }).then(() => {
        this.$message.success('权限管理菜单初始化完成')
        this.fetchTree()
      }).catch(() => {
        this.$message.error('初始化权限管理菜单失败')
      }).finally(() => {
        this.initPermissionMenuLoading = false
      })
    },
    initBugManagementMenu() {
      this.initBugMenuLoading = true
      getMenuTree({}).then(res => {
        const data = res && res.data ? res.data : res || []
        const tree = Array.isArray(data) ? data : (data.list || data.items || [])
        const flattened = []
        this.flattenMenus(tree, flattened)
        const hasBugMenu = flattened.some(item => String(item.path || '').indexOf('/bug') === 0)
        if (hasBugMenu) {
          this.$message.success('Bug 管理菜单已存在')
          return Promise.resolve()
        }
        return createMenu({
          parentId: 0,
          name: 'Bug管理',
          code: 'bug_manage_root',
          type: 1,
          path: '/bug',
          component: '',
          icon: 'el-icon-s-claim',
          permissionCode: '',
          sort: 88,
          visible: 1,
          status: 1
        }).then(parentRes => {
          const created = (parentRes && parentRes.data) || {}
          let parentId = created.id || created.menuId
          const resolveParentId = () => {
            if (parentId) return Promise.resolve(parentId)
            return getMenuTree({}).then(latestRes => {
              const latestData = latestRes && latestRes.data ? latestRes.data : latestRes || []
              const latestTree = Array.isArray(latestData) ? latestData : (latestData.list || latestData.items || [])
              const flat = []
              this.flattenMenus(latestTree, flat)
              const p = flat.find(item => (item.path || '') === '/bug' || (item.code || '') === 'bug_manage_root')
              return p ? (p.id || p.menuId) : 0
            })
          }
          return resolveParentId().then(pid => {
            if (!pid) {
              return Promise.reject(new Error('未获取到 Bug 管理父菜单 ID'))
            }
            const children = [
              {
                name: '新建 Bug',
                code: 'bug_create',
                path: '/bug/create',
                component: '@/components/Bug/BugEditor',
                permissionCode: 'bug:create',
                sort: 5,
                icon: 'el-icon-document-add'
              },
              {
                name: 'Bug 列表',
                code: 'bug_list',
                path: '/bug/list',
                component: '@/components/Bug/BugList',
                permissionCode: 'bug:list',
                sort: 10,
                icon: 'el-icon-document'
              },
              {
                name: 'Bug 统计',
                code: 'bug_stats',
                path: '/bug/stats',
                component: '@/components/Bug/BugStats',
                permissionCode: 'bug:stats',
                sort: 20,
                icon: 'el-icon-data-line'
              }
            ]
            return children.reduce((chain, c) => {
              return chain.then(() => createMenu({
                parentId: Number(pid),
                name: c.name,
                code: c.code,
                type: 2,
                path: c.path,
                component: c.component,
                icon: c.icon,
                permissionCode: c.permissionCode,
                sort: c.sort,
                visible: 1,
                status: 1
              }))
            }, Promise.resolve())
          })
        })
      }).then(() => {
        this.$message.success('Bug 管理菜单初始化完成')
        this.fetchTree()
      }).catch(() => {
        this.$message.error('初始化 Bug 管理菜单失败')
      }).finally(() => {
        this.initBugMenuLoading = false
      })
    }
  },
  created() {
    this.fetchTree()
  }
}
</script>

<style scoped>
.page-wrap {
  padding: 20px;
}
</style>
