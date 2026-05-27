<template>
  <div class="page-wrap">
    <page-section title="产品管理">
      <template slot="extra">
        <el-button type="primary" size="small" @click="openCreate">新建产品</el-button>
      </template>
      <el-form :inline="true" :model="queryForm" size="small" @submit.native.prevent>
        <el-form-item label="产品名称">
          <el-input v-model="queryForm.name" placeholder="请输入产品名称" clearable @keyup.enter.native="handleSearch"></el-input>
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
        <el-table-column prop="code" label="产品编码" min-width="120"></el-table-column>
        <el-table-column prop="name" label="产品名称" min-width="160"></el-table-column>
        <el-table-column prop="description" label="描述" min-width="220" show-overflow-tooltip></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">{{ scope.row.status === 0 ? '禁用' : '启用' }}</template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template slot-scope="scope">
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

    <el-dialog :title="dialogMode === 'create' ? '新建产品' : '编辑产品'" :visible.sync="dialogVisible" width="520px" @close="resetDialogForm">
      <el-form ref="productForm" :model="productForm" :rules="productRules" label-width="94px" size="small">
        <el-form-item label="产品名称" prop="name">
          <el-input v-model.trim="productForm.name" maxlength="64" placeholder="请输入产品名称"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="productForm.status" placeholder="请选择状态" style="width: 100%;">
            <el-option label="启用" :value="1"></el-option>
            <el-option label="禁用" :value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model.trim="productForm.description" type="textarea" :rows="4" maxlength="255" show-word-limit placeholder="请输入描述"></el-input>
        </el-form-item>
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
import { createProduct, deleteProduct, getProductList, updateProduct } from '@/api/productApi'

const getDefaultForm = () => ({
  id: undefined,
  name: '',
  status: 1,
  description: ''
})

export default {
  name: 'ProductList',
  components: { PageSection },
  data() {
    return {
      loading: false,
      submitting: false,
      dialogVisible: false,
      dialogMode: 'create',
      queryForm: {
        name: '',
        status: ''
      },
      productForm: getDefaultForm(),
      productRules: {
        name: [{ required: true, message: '请输入产品名称', trigger: 'blur' }],
        status: [{ required: true, message: '请选择状态', trigger: 'change' }]
      },
      pageNo: 1,
      pageSize: 10,
      total: 0,
      tableData: []
    }
  },
  methods: {
    fetchList() {
      this.loading = true
      getProductList({
        pageNo: this.pageNo,
        pageSize: this.pageSize,
        name: this.queryForm.name,
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
    handleSearch() {
      this.pageNo = 1
      this.fetchList()
    },
    resetSearch() {
      this.queryForm = {
        name: '',
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
        this.productForm = getDefaultForm()
        if (this.$refs.productForm) {
          this.$refs.productForm.clearValidate()
        }
      })
    },
    openEdit(row) {
      this.dialogMode = 'edit'
      this.dialogVisible = true
      this.$nextTick(() => {
        this.productForm = Object.assign(getDefaultForm(), row, { id: row.id })
        if (this.$refs.productForm) {
          this.$refs.productForm.clearValidate()
        }
      })
    },
    resetDialogForm() {
      this.productForm = getDefaultForm()
      this.submitting = false
      this.$nextTick(() => {
        if (this.$refs.productForm) {
          this.$refs.productForm.resetFields()
        }
      })
    },
    submitForm() {
      this.$refs.productForm.validate(valid => {
        if (!valid) {
          return
        }
        this.submitting = true
        const request = this.dialogMode === 'create'
          ? createProduct(this.productForm)
          : updateProduct(this.productForm)
        request.then(res => {
          if (res && res.code === 20000) {
            this.$message.success(res.message || (this.dialogMode === 'create' ? '产品创建成功' : '产品更新成功'))
            this.dialogVisible = false
            this.pageNo = 1
            this.fetchList()
            return
          }
          this.$message.error((res && res.message) || (this.dialogMode === 'create' ? '产品创建失败' : '产品更新失败'))
        }).finally(() => {
          this.submitting = false
        })
      })
    },
    handleDelete(row) {
      this.$confirm('确认删除该产品吗？', '提示', {
        type: 'warning'
      }).then(() => {
        deleteProduct({ id: row.id }).then(() => {
          this.$message.success('产品删除成功')
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
