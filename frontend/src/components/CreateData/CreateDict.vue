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
                  placeholder="请选择业务线" @change="get_file_name(team_name)"
                  style="width:160px"
                  clearable>
                  <el-option v-for="item in dict_data" :key="item.value" :value="item.value"
                             :label="item.label"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="" labelWidth="110px">
                <el-input placeholder="名称" v-model="keyword" clearable @change="search" @keyup.enter="search">
                </el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="search" @keyup.enter="search">搜索</el-button>
              </el-form-item>
            </el-form>
          </div>
          <div class="api-form">
            <el-table ref="table" :data="tableData" :header-cell-style="{textAlign: 'center'}" :stripe="true" :height="tableHeight" border>
              <el-table-column label="业务线" prop="team_name"></el-table-column>
              <el-table-column label="业务名称" prop="dict_key"></el-table-column>
              <el-table-column label="对应名称" prop="dict_value"></el-table-column>
              <el-table-column label="创建时间" prop="created_time">
                <template slot-scope="props">
                  {{ formatTime(props.row.created_time) }}
                </template>
              </el-table-column>
              <el-table-column label="操作">
                <template slot-scope="props">
                  <el-button type="primary" @click.native.prevent="addData(props.row)" style="right: 0">修改</el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-dialog
              :title="dialog.title"
              :visible="dialog.dialogVisible"
              :close-on-click-modal="false"
              width="40%"
              @close="cancel()">
              <el-form :model="dialog.moduleForm" ref="dialog.moduleForm" :rules="rules" label-width="120px"
                       class="demo-ruleForm">
                <el-form-item label="业务名称：" prop="module_name">
                  <span>{{ dialog.moduleForm.dict_key }}</span>
                </el-form-item>
                <el-form-item label="对应名称:" prop="class_name">
                  <el-input v-model="dialog.moduleForm.dict_value">{{ dialog.moduleForm.dict_value }}</el-input>
                </el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
              <el-button @click.native.prevent="cancel()">取消</el-button>
              <el-button type="primary" @click.native.prevent="submit">确定</el-button>
            </span>
            </el-dialog>
          </div>
          <div class="block">
            <span class="demonstration"></span>
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="pageNo"
              :page-size="10"
              layout="total, sizes, prev, pager, next, jumper"
              :total="total">
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
              placeholder="请选择业务线" @change="manage_get_file_name(manage_team_name)"
              style="width:160px"
              clearable>
              <el-option v-for="item in dict_data" :key="item.value" :value="item.value"
                         :label="item.label"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="业务系统">
            <el-select
              v-model="file_name"
              placeholder="请选择"
              style="width:160px"
              clearable>
              <el-option v-for="item in dict_file_data" :key="item.value" :value="item.value"
                         :label="item.label"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="" labelWidth="110px">
            <el-input placeholder="场景名称" v-model="detail_name" clearable @change="manage_search()"
                      @keyup.enter="manage_search()">
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="manage_search" @keyup.enter="manage_search">搜索</el-button>
            <el-button type="primary" @click.native.prevent="manage_pullGit" style="right: 0">更新关键字</el-button>
          </el-form-item>
        </el-form>
      </div>
        <el-table ref="table" :data="manage_tableData" :header-cell-style="{textAlign: 'center'}" :stripe="true" :height="tableHeight" border>
          <el-table-column label="场景名称" prop="method_function_detail"></el-table-column>
          <el-table-column label="业务系统" prop="file_name"></el-table-column>
          <el-table-column label="业务线" prop="team_name"></el-table-column>
          <el-table-column label="负责人" prop="creator"></el-table-column>
          <el-table-column label="操作"  align="center">
            <template slot-scope="props" >
              <el-button type="text" class="delete_button" @click.native.prevent="manage_handleDelete(props.row)">删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      <el-dialog
        :title="pullmaster.title"
        :visible="pullmaster.dialogVisible"
        :close-on-click-modal="false"
        width="30%"
        @close="manage_gitcancel()"
      >
        <el-form :model="pullmaster.moduleForm" ref="dialog.scrapy" :rules="rules" label-width="60px"
                 class="demo-ruleForm">
          <el-form-item label="业务线:" prop="baseOrUbrd" label-suffix="*">
            <el-select v-model="pullmaster.moduleForm.team" placeholder="请选择">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
        <el-button @click.native.prevent="manage_gitcancel()">取消</el-button>
        <el-button type="primary" @click.native.prevent="manage_gitsubmit()">确定</el-button>
      </span>
      </el-dialog>
        <div class="block">
          <span class="demonstration"></span>
          <el-pagination
            @size-change="manage_handleSizeChange"
            @current-change="manage_handleCurrentChange"
            :current-page="manage_pageNo"
            :page-size="10"
            layout="total, sizes, prev, pager, next, jumper"
            :total="manage_total">
          </el-pagination>
        </div>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import {DictAdd, DictQuery, GetTeam} from '@/api/CreateDtapi'
import {
  DataAdd,
  DataDelete,
  DataAdvance,
  InfoQuery,
  ScrapyDetail,
  getEureka,
  getGitPull
} from '@/api/CreateDtapi'
import {formatTime} from '@/utils/util'
// import CreateData from '@/components/User/EditPassword'

export default {
  name: "CreateManage",
  // components: {CreateData},
  data() {
    return {
      roles: [
        {
          value: 1,
          label: '初始路径'
        }, {
          value: 2,
          label: '描述简称'
        }
      ],
      activeName: 'first',
      tableHeight: null,
      keyword: '',
      currentPage1: 0,
      total: 0,
      team_name: '',
      tableData: [],
      pageNo: 1,
      pageSize: 10,
      create_dict_data_id: '',
      drawer: false,
      dialog: {
        title: "编辑",
        dialogVisible: false,
        moduleForm: {
          team_name: '',
          data_type: '',
          dict_key: '',
          dict_value: '',
        },
      },
      manage_tableData: [],
      manage_total: 0,
      manage_pageNo: 1,
      manage_pageSize: 10,
      loading: false,
      get_team: '',
      manage_team_name: '',
      initial_team_name: '',
      file_name: '',
      detail_name: '',
      module_name: '',
      create_data_detail_id: "",
      manage_drawer: false,
      onfocus_create_data_info_id: '',
      dict_data: {},
      dict_file_data: {},
      options: [{
        value: 'CC',
        label: '销售'
      }, {
        value: 'PBE',
        label: '公共基础'
      }, {
        value: 'TO',
        label: '教师'
      }, {
        value: 'TMO',
        label: '教务'
      }, {
        value: 'USER',
        label: '用户组'
      }],
      scrapy: {
        title: "编辑",
        dialogVisible: false,
        moduleForm: {
          fileName: '',
          team: ''
        }
      },
      pullmaster: {
        title: "编辑",
        dialogVisible: false,
        moduleForm: {
          team: '',
          fileName: '',
          username: '',
          password: ''
        }
      },
    }
  },
  methods: {
    formatTime(str) {
      if (str === undefined || str === null) {
        return ''
      } else {
        return formatTime(str)
      }
    },
    handleSizeChange(val) {
      this.pageSize = val;
      this.search()
    },
    handleCurrentChange(val) {
      this.pageNo = val;
      this.search(true)
    },
    dataList(data) {
      DictQuery(data).then(data => {
        this.tableData = data.data;
        this.total = data.totalCount
      })
    },
    get_team_name(team) {
      let request_data = {"data_type": 2, "team_name": team}
      this.pageNo = 1
      GetTeam(request_data).then((data) => {
        if (data.code === 200) {
          this.dict_data = data.data
        }
      })
    },
    search(val) {
      if (!val) {
        this.pageNo = 1
      }
      let data = {
        pageNo: this.pageNo,
        pageSize: this.pageSize,
        keyword: this.keyword,
        team_name: this.team_name
      };
      this.dataList(data)
    },
    openDrawer(row) {
      this.drawer = true
      this.onfocus_create_data_info_id = row.create_data_info_id
    },
    closeDrwaer() {
      this.drawer = false
    },
    addData(row) {
      this.dialog.dialogVisible = true;
      this.dialog.title = "修改业务对应展示名称"
      this.dialog.moduleForm = row
    },
    cancel() {
      this.dialog.dialogVisible = false;
      this.dialog = {
        title: "编辑",
        dialogVisible: false,
        moduleForm: {
          data_type: '',
          team_name: '',
          dict_key: '',
          dict_value: '',
        },
      }
    },
    submit() {
      // if (this.dialog.moduleForm.dict_key !== '' && this.dialog.moduleForm.dict_value !== '' && this.dialog.moduleForm.data_type !== '') {
      if (this.dialog.moduleForm.dict_value !== '') {
        console.log(this.dialog.moduleForm, "$$$$")
        DictAdd(this.dialog.moduleForm).then((data) => {
          if (data.code === 200) {
            this.$message({
              type: 'success',
              message: '修改成功!'
            });
            this.dialog.dialogVisible = false;
            this.search()
          }
          this.dialog.moduleForm = {
            data_type: '',
            team_name: '',
            dict_key: '',
            dict_value: '',
          }
        })
      } else {
        this.$message({
          type: 'info',
          message: "请输入名称"
        })
      }
    },
    manage_handleDelete(row) {
      let data = {create_data_detail_id: row.create_data_detail_id};
      this.$confirm('是否删除该数据?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        DataDelete(data).then((data) => {
          if (data.code === 200) {
            this.$message({
              type: 'success',
              message: '删除成功!'
            });
            this.manage_search()
          }
        })
      })
    },
    manage_pullGit() {
      this.pullmaster.dialogVisible = true;
      this.pullmaster.title = "更新关键字"
    },
    manage_gitcancel() {
      this.pullmaster.dialogVisible = false;
      this.pullmaster = {
        title: "编辑",
        dialogVisible: false,
        moduleForm: {
          team: '',
          fileName: '',
          username: '',
          password: ''
        },
      }
    },
    manage_submit(team) {
      this.pullmaster.moduleForm.team = team
      ScrapyDetail(this.pullmaster.moduleForm).then((data) => {
        this.loading = false;
        if (data.code === 200) {
          this.$message({
            type: 'success',
            message: '更新关键字成功!',
          });
          this.pullmaster.moduleForm = {
            team: '',
            fileName: '',
            username: '',
            password: ''
          }
          this.manage_search()
        } else {
          this.$message({
            type: 'false',
            message: data.message
          });
        }
        this.pullmaster.moduleForm = {
          team: '',
          fileName: '',
          username: '',
          password: ''
        }
      })
    },
    loadingShow() {
      const loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      setTimeout(() => {
        loading.close();
        // this.$message({
        //   type: 'success',
        //   message: '更新关键字成功!'
        // });
        this.pullmaster.dialogVisible = false;
        this.search()
      }, 10000);
    },
    manage_gitsubmit() {
      this.loadingShow();
      this.get_team = this.pullmaster.moduleForm.team
      if (this.pullmaster.moduleForm.team !== '') {
        getGitPull(this.pullmaster.moduleForm).then((data) => {
          if (data.code === 200) {
            this.manage_submit(this.get_team)
          }
        })
      } else {
        this.$message({
          type: 'info',
          message: "请输入组名"
        })
      }
    },
    manage_handleSizeChange(val) {
      this.manage_pageSize = val;
      this.manage_search()
    },
    manage_handleCurrentChange(val) {
      this.manage_pageNo = val;
      this.manage_search(true)
    },
    manage_dataList(data) {
      InfoQuery(data).then(data => {
        this.manage_tableData = data.data;
        this.manage_total = data.totalCount
      })
    },
    manage_search(val) {
      if (!val) {
        this.manage_pageNo = 1
      }
      let data = {
        pageNo: this.manage_pageNo,
        pageSize: this.manage_pageSize,
        detail_name: this.detail_name,
        team_name: this.manage_team_name,
        file_name: this.file_name,
        module_name: this.module_name
      };
      this.manage_dataList(data)
    },
    manage_get_team_name(manage_team) {
      let request_data = {"data_type": 2, "team_name": manage_team}
      this.manage_pageNo = 1
      GetTeam(request_data).then((data) => {
        if (data.code === 200) {
          this.dict_data = data.data
        }
      })
    },
    manage_get_file_name(manage_team) {
      let request_data = {"data_type": 3, "team_name": manage_team}
      this.manage_pageNo = 1
      GetTeam(request_data).then((data) => {
        if (data.code === 200) {
          this.dict_file_data = data.data
        }
      })
    },
  },
  created() {
    let data = {pageNo: 1, pageSize: 10, keyword: "", team_name: ""}
    this.dataList(data)
    let manage_data = {pageNo: 1, pageSize: 10, detail_name: "", team_name: "", file_name: "", module_name: ""}
    this.manage_dataList(manage_data)
    this.tableHeight = document.getElementById("app").clientHeight - 250
    let team = ""
    this.get_team_name(team)
    this.manage_get_team_name(team)
  }
}
</script>

<style scoped>
.data {
  padding-left: 100px;
}
.delete_button{
 color: #cf9236;
}
</style>
