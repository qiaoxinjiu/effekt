<template>
  <div class="page-wrap">
    <page-section title="造数工厂">
      <template slot="extra">
        <el-button type="primary" size="small" @click="goEditor()">新建造数器</el-button>
        <el-button size="small" @click="goTasks">任务历史</el-button>
        <el-button size="small" @click="goMock">Mock服务</el-button>
      </template>
      <el-form :inline="true" size="small">
        <el-form-item label="项目ID">
          <el-input v-model="projectId" style="width: 120px;"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchList">查询</el-button>
        </el-form-item>
      </el-form>
      <el-table v-loading="loading" :data="tableData" border style="margin-top: 16px;">
        <el-table-column prop="name" label="名称" min-width="160"></el-table-column>
        <el-table-column prop="builder_type" label="类型" width="120"></el-table-column>
        <el-table-column prop="description" label="描述" min-width="220"></el-table-column>
        <el-table-column label="操作" width="240">
          <template slot-scope="scope">
            <el-button type="text" @click="goEditor(scope.row)">编辑</el-button>
            <el-button type="text" @click="execute(scope.row)">执行</el-button>
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
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import { executeBuilder, getBuilderList } from '@/api/dataFactoryApi'

export default {
  name: 'BuilderList',
  components: { PageSection },
  data() {
    return {
      loading: false,
      projectId: this.$route.query.projectId || 1,
      tableData: []
    }
  },
  methods: {
    fetchList() {
      this.loading = true
      getBuilderList(this.projectId, {
        pageNo: this.pageNo,
        pageSize: this.pageSize
      }).then(res => {
        const data = (res && res.data) || res || []
        this.tableData = data.items || data.list || data.data || data || []
        this.total = data.total || data.totalCount || this.tableData.length
      }).catch(() => {
        this.tableData = []
        this.total = 0
      }).finally(() => {
        this.loading = false
      })
    },
    goEditor(row) {
      this.$router.push({ path: '/data-tools/factory/editor', query: { projectId: this.projectId, builderId: row && row.id } })
    },
    goTasks() {
      this.$router.push({ path: '/data-tools/factory/task', query: { projectId: this.projectId } })
    },
    goMock() {
      this.$router.push({ path: '/data-tools/factory/mock', query: { projectId: this.projectId } })
    },
    execute(row) {
      executeBuilder(this.projectId, row.id, { params: { count: 1 }, async: true }).then(() => {
        this.$message({ type: 'success', message: '造数任务已提交' })
      })
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
style>
