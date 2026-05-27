<template>
  <el-tabs v-model="activeName">
    <el-tab-pane label="菜单管理" name="first">
      <keep-alive>
        <div class="create-data">
          <div class="search">
            <el-form :inline="true" class="search" size="small" @submit.native.prevent>
              <el-form-item label="业务线">
                <el-select
                  v-model="team_name"
                  placeholder="请选择业务线"
                  style="width:160px"
                  clearable
                  @change="getTeamName(team_name)">
                  <el-option v-for="item in dict_data" :key="item.value" :value="item.value" :label="item.label"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="" labelWidth="110px">
                <el-input v-model="keyword" placeholder="名称" clearable @change="search" @keyup.enter="search"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="search">搜索</el-button>
              </el-form-item>
            </el-form>
          </div>
          <div class="api-form">
            <el-table ref="table" :data="tableData" :header-cell-style="{ textAlign: 'center' }" :stripe="true" :height="tableHeight" border>
              <el-table-column label="业务线" prop="team_name"></el-table-column>
              <el-table-column label="业务名称" prop="dict_key"></el-table-column>
              <el-table-column label="对应名称" prop="dict_value"></el-table-column>
              <el-table-column label="创建时间" prop="created_time">
                <template slot-scope="props">
                  {{ formatTimeValue(props.row.created_time) }}
                </template>
              </el-table-column>
              <el-table-column label="操作">
                <template slot-scope="props">
                  <el-button type="primary" @click.native.prevent="addData(props.row)">修改</el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-dialog
              :title="dialog.title"
              :visible="dialog.dialogVisible"
              :close-on-click-modal="false"
              width="40%"
              @close="cancel">
              <el-form :model="dialog.moduleForm" label-width="120px" class="demo-ruleForm">
                <el-form-item label="业务名称：">
                  <span>{{ dialog.moduleForm.dict_key }}</span>
                </el-form-item>
                <el-form-item label="对应名称:">
                  <el-input v-model="dialog.moduleForm.dict_value"></el-input>
                </el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
                <el-button @click.native.prevent="cancel">取消</el-button>
                <el-button type="primary" @click.native.prevent="submit">确定</el-button>
              </span>
            </el-dialog>
          </div>
          <div class="block">
            <el-pagination
              :current-page="pageNo"
              :page-size="10"
              :total="total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange">
            </el-pagination>
          </div>
        </div>
      </keep-alive>
    </el-tab-pane>

    <el-tab-pane label="数据管理" name="second">
      <div class="search">
        <el-form :inline="true" class="search" size="small" @submit.native.prevent>
          <el-form-item label="业务线">
            <el-select
              v-model="manage_team_name"
              placeholder="请选择业务线"
              style="width:160px"
              clearable
              @change="manageGetFileName(manage_team_name)">
              <el-option v-for="item in dict_data" :key="item.value" :value="item.value" :label="item.label"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="业务系统">
            <el-select v-model="file_name" placeholder="请选择" style="width:160px" clearable>
              <el-option v-for="item in dict_file_data" :key="item.value" :value="item.value" :label="item.label"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="" labelWidth="110px">
            <el-input v-model="detail_name" placeholder="场景名称" clearable @change="manageSearch" @keyup.enter="manageSearch"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="manageSearch">搜索</el-button>
            <el-button type="primary" @click.native.prevent="managePullGit">更新关键字</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table ref="table" :data="manage_tableData" :header-cell-style="{ textAlign: 'center' }" :stripe="true" :height="tableHeight" border>
        <el-table-column label="场景名称" prop="method_function_detail"></el-table-column>
        <el-table-column label="业务系统" prop="file_name"></el-table-column>
        <el-table-column label="业务线" prop="team_name"></el-table-column>
        <el-table-column label="负责人" prop="creator"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="props">
            <el-button type="text" class="delete_button" @click.native.prevent="manageHandleDelete(props.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-dialog
        :title="pullmaster.title"
        :visible="pullmaster.dialogVisible"
        :close-on-click-modal="false"
        width="30%"
        @close="manageGitCancel">
        <el-form :model="pullmaster.moduleForm" label-width="60px" class="demo-ruleForm">
          <el-form-item label="业务线:" label-suffix="*">
            <el-select v-model="pullmaster.moduleForm.team" placeholder="请选择">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click.native.prevent="manageGitCancel">取消</el-button>
          <el-button type="primary" @click.native.prevent="manageGitSubmit">确定</el-button>
        </span>
      </el-dialog>

      <div class="block">
        <el-pagination
          :current-page="manage_pageNo"
          :page-size="10"
          :total="manage_total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="manageHandleSizeChange"
          @current-change="manageHandleCurrentChange">
        </el-pagination>
      </div>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import { DataDelete, DictAdd, DictQuery, GetTeam, InfoQuery, ScrapyDetail, getGitPull } from '@/api/CreateDtapi'
import { formatTime } from '@/utils/util'

const defaultDialogForm = () => ({
  team_name: '',
  data_type: '',
  dict_key: '',
  dict_value: ''
})

const defaultPullForm = () => ({
  team: '',
  fileName: '',
  username: '',
  password: ''
})

export default {
  name: 'CreateManage',
  data() {
    return {
      activeName: 'first',
      tableHeight: null,
      keyword: '',
      total: 0,
      team_name: '',
      tableData: [],
      pageNo: 1,
      pageSize: 10,
      dialog: {
        title: '编辑',
        dialogVisible: false,
        moduleForm: defaultDialogForm()
      },
      manage_tableData: [],
      manage_total: 0,
      manage_pageNo: 1,
      manage_pageSize: 10,
      loading: false,
      get_team: '',
      manage_team_name: '',
      file_name: '',
      detail_name: '',
      module_name: '',
      dict_data: {},
      dict_file_data: {},
      options: [
        { value: 'CC', label: '销售' },
        { value: 'PBE', label: '公共基础' },
        { value: 'TO', label: '教师' },
        { value: 'TMO', label: '教务' },
        { value: 'USER', label: '用户组' }
      ],
      pullmaster: {
        title: '编辑',
        dialogVisible: false,
        moduleForm: defaultPullForm()
      }
    }
  },
  methods: {
    formatTimeValue(str) {
      return str ? formatTime(str) : ''
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.search()
    },
    handleCurrentChange(val) {
      this.pageNo = val
      this.search(true)
    },
    dataList(data) {
      DictQuery(data).then(data => {
        this.tableData = data.data
        this.total = data.totalCount
      })
    },
    getTeamName(team) {
      this.pageNo = 1
      GetTeam({ data_type: 2, team_name: team }).then(data => {
        if (data.code === 200) {
          this.dict_data = data.data
        }
      })
    },
    search(keepPage) {
      if (!keepPage) {
        this.pageNo = 1
      }
      this.dataList({
        pageNo: this.pageNo,
        pageSize: this.pageSize,
        keyword: this.keyword,
        team_name: this.team_name
      })
    },
    addData(row) {
      this.dialog.dialogVisible = true
      this.dialog.title = '修改业务对应展示名称'
      this.dialog.moduleForm = { ...row }
    },
    cancel() {
      this.dialog = {
        title: '编辑',
        dialogVisible: false,
        moduleForm: defaultDialogForm()
      }
    },
    submit() {
      if (!this.dialog.moduleForm.dict_value) {
        this.$message({ type: 'info', message: '请输入名称' })
        return
      }
      DictAdd(this.dialog.moduleForm).then(data => {
        if (data.code === 200) {
          this.$message({ type: 'success', message: '修改成功!' })
          this.cancel()
          this.search()
        }
      })
    },
    manageHandleSizeChange(val) {
      this.manage_pageSize = val
      this.manageSearch()
    },
    manageHandleCurrentChange(val) {
      this.manage_pageNo = val
      this.manageSearch(true)
    },
    manageDataList(data) {
      InfoQuery(data).then(data => {
        this.manage_tableData = data.data
        this.manage_total = data.totalCount
      })
    },
    manageSearch(keepPage) {
      if (!keepPage) {
        this.manage_pageNo = 1
      }
      this.manageDataList({
        pageNo: this.manage_pageNo,
        pageSize: this.manage_pageSize,
        detail_name: this.detail_name,
        team_name: this.manage_team_name,
        file_name: this.file_name,
        module_name: this.module_name
      })
    },
    manageHandleDelete(row) {
      this.$confirm('是否删除该数据?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        DataDelete({ create_data_detail_id: row.create_data_detail_id }).then(data => {
          if (data.code === 200) {
            this.$message({ type: 'success', message: '删除成功!' })
            this.manageSearch()
          }
        })
      })
    },
    managePullGit() {
      this.pullmaster.dialogVisible = true
      this.pullmaster.title = '更新关键字'
    },
    manageGitCancel() {
      this.pullmaster = {
        title: '编辑',
        dialogVisible: false,
        moduleForm: defaultPullForm()
      }
    },
    manageSubmit(team) {
      this.pullmaster.moduleForm.team = team
      ScrapyDetail(this.pullmaster.moduleForm).then(data => {
        this.loading = false
        if (data.code === 200) {
          this.$message({ type: 'success', message: '更新关键字成功!' })
          this.pullmaster.moduleForm = defaultPullForm()
          this.manageSearch()
        } else {
          this.$message({ type: 'error', message: data.message })
        }
      })
    },
    loadingShow() {
      const loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      setTimeout(() => {
        loading.close()
        this.pullmaster.dialogVisible = false
        this.search()
      }, 10000)
    },
    manageGitSubmit() {
      this.loadingShow()
      this.get_team = this.pullmaster.moduleForm.team
      if (!this.pullmaster.moduleForm.team) {
        this.$message({ type: 'info', message: '请输入组名' })
        return
      }
      getGitPull(this.pullmaster.moduleForm).then(data => {
        if (data.code === 200) {
          this.manageSubmit(this.get_team)
        }
      })
    },
    manageGetTeamName(manageTeam) {
      this.manage_pageNo = 1
      GetTeam({ data_type: 2, team_name: manageTeam }).then(data => {
        if (data.code === 200) {
          this.dict_data = data.data
        }
      })
    },
    manageGetFileName(manageTeam) {
      this.manage_pageNo = 1
      GetTeam({ data_type: 3, team_name: manageTeam }).then(data => {
        if (data.code === 200) {
          this.dict_file_data = data.data
        }
      })
    }
  },
  created() {
    this.dataList({ pageNo: 1, pageSize: 10, keyword: '', team_name: '' })
    this.manageDataList({ pageNo: 1, pageSize: 10, detail_name: '', team_name: '', file_name: '', module_name: '' })
    this.tableHeight = document.getElementById('app').clientHeight - 250
    this.getTeamName('')
    this.manageGetTeamName('')
  }
}
</script>

<style scoped>
.data {
  padding-left: 100px;
}

.delete_button {
  color: #cf9236;
}
</style>
