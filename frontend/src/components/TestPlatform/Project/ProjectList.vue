<template>
  <div class="page-wrap">
    <page-section title="项目管理">
      <template slot="extra">
        <el-button type="primary" size="small" @click="openCreate">新建项目</el-button>
      </template>
      <el-form :inline="true" :model="queryForm" size="small" @submit.native.prevent>
        <el-form-item label="关键词">
          <el-input v-model="queryForm.keyword" placeholder="项目名称" clearable @keyup.enter.native="fetchList"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryForm.status" clearable placeholder="全部状态">
            <el-option label="启用" :value="1"></el-option>
            <el-option label="禁用" :value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchList">查询</el-button>
        </el-form-item>
      </el-form>
      <el-table v-loading="loading" :data="tableData" border style="width: 100%; margin-top: 16px;">
        <el-table-column prop="product_name" label="产品名称" min-width="160"></el-table-column>
        <el-table-column prop="key" label="项目编码" min-width="120"></el-table-column>
        <el-table-column prop="name" label="项目名称" min-width="160"></el-table-column>
        <el-table-column prop="description" label="描述" min-width="220" show-overflow-tooltip></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">{{ scope.row.status === 0 ? '禁用' : '启用' }}</template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" @click="openEdit(scope.row)">编辑</el-button>
            <el-button type="text" style="color: #F56C6C;" @click="handleDelete(scope.row)">删除</el-button>
            <el-button type="text" @click="goSettings(scope.row)">设置</el-button>
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

    <el-dialog :title="dialogMode === 'create' ? '新建项目' : '编辑项目'" :visible.sync="createDialogVisible" width="520px" @close="resetCreateForm">
      <el-form ref="createForm" :model="createForm" :rules="createRules" label-width="94px" size="small">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model.trim="createForm.name" maxlength="64" placeholder="请输入项目名称"></el-input>
        </el-form-item>
        <el-form-item label="所属产品" prop="productId">
          <el-select v-model="createForm.productId" placeholder="请选择所属产品" filterable clearable style="width: 100%;">
            <el-option
              v-for="item in productOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="createForm.status" placeholder="请选择状态" style="width: 100%;">
            <el-option label="启用" :value="1"></el-option>
            <el-option label="禁用" :value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model.trim="createForm.description" type="textarea" :rows="4" maxlength="255" show-word-limit placeholder="请输入描述"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button size="small" @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="createSubmitting" @click="submitCreate">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { createProject, deleteProject, getProjectList, updateProject } from '@/api/projectApi'
import { getProductList } from '@/api/productApi'

const getDefaultCreateForm = () => ({
  id: undefined,
  name: '',
  productId: '',
  status: 1,
  description: ''
})

export default {
  name: 'ProjectList',
  components: { PageSection },
  data() {
    return {
      loading: false,
      createSubmitting: false,
      createDialogVisible: false,
      dialogMode: 'create',
      queryForm: {
        keyword: '',
        status: ''
      },
      createForm: getDefaultCreateForm(),
      createRules: {
        name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
        productId: [{ required: true, message: '请选择所属产品', trigger: 'change' }],
        status: [{ required: true, message: '请选择状态', trigger: 'change' }]
      },
      productOptions: [],
      pageNo: 1,
      pageSize: 10,
      total: 0,
      tableData: []
    }
  },
  methods: {
    fetchList() {
      this.loading = true
      getProjectList({
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
    handleSizeChange(val) {
      this.pageSize = val
      this.pageNo = 1
      this.fetchList()
    },
    handleCurrentChange(val) {
      this.pageNo = val
      this.fetchList()
    },
    goSettings(row) {
      this.$router.push({ path: '/test-platform/project/setting', query: { projectId: row.id } })
    },
    fetchProductOptions() {
      return getProductList({
        pageNo: 1,
        pageSize: 1000,
        status: 1
      }).then(res => {
        const data = res && res.data ? res.data : res || {}
        this.productOptions = data.items || data.list || data.data || []
      }).catch(() => {
        this.productOptions = []
      })
    },
    openCreate() {
      this.dialogMode = 'create'
      this.createForm = getDefaultCreateForm()
      this.fetchProductOptions()
      this.createDialogVisible = true
      this.$nextTick(() => {
        if (this.$refs.createForm) {
          this.$refs.createForm.clearValidate()
        }
      })
    },
    openEdit(row) {
      this.dialogMode = 'edit'
      this.fetchProductOptions()
      this.createDialogVisible = true
      this.$nextTick(() => {
        this.createForm = Object.assign(getDefaultCreateForm(), row, {
          id: row.id,
          productId: row.productId || row.product_id || row.productId
        })
        if (this.$refs.createForm) {
          this.$refs.createForm.clearValidate()
        }
      })
    },
    resetCreateForm() {
      this.createForm = getDefaultCreateForm()
      this.createSubmitting = false
      this.$nextTick(() => {
        if (this.$refs.createForm) {
          this.$refs.createForm.resetFields()
        }
      })
    },
    submitCreate() {
      this.$refs.createForm.validate(valid => {
        if (!valid) {
          return
        }
        this.createSubmitting = true
        const request = this.dialogMode === 'create'
          ? createProject(this.createForm)
          : updateProject(this.createForm)
        request.then(res => {
          const message = (res && res.message) || ''
          if (res && res.code === 20000) {
            this.$message.success(message || (this.dialogMode === 'create' ? '项目创建成功' : '项目更新成功'))
            this.createDialogVisible = false
            this.pageNo = 1
            this.fetchList()
            return
          }
          this.$message.error(message || (this.dialogMode === 'create' ? '项目创建失败' : '项目更新失败'))
        }).finally(() => {
          this.createSubmitting = false
        })
      })
    },
    handleDelete(row) {
      this.$confirm('确认删除该项目吗？', '提示', {
        type: 'warning'
      }).then(() => {
        deleteProject({ id: row.id }).then(() => {
          this.$message.success('项目删除成功')
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
