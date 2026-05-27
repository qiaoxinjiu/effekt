<template>
  <div style="margin-top: 20px;margin-right: 20px;margin-left: 20px">
    <el-breadcrumb separator="/" class="el-breadcrumb-div">
      <el-breadcrumb-item :to="{ path: '/dashboard' }">数据监控</el-breadcrumb-item>
      <el-breadcrumb-item>问题列表</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="searchReport">
      <el-form
        label-width="70px"
        labelPosition="right"
        class="el-form"
        :inline="true"
        style="
        float:left;
        height:50px;
        margin-top:30px;"
      >
        <el-form-item label="业务线">
          <el-select
            v-model="elSelectBusinessLine.id"
            placeholder="请选择业务线"
            style="width:160px"
            clearable>
            <el-option v-for="item in businessInfo" :key="item.id" :value="item.id"
                       :label="item.business_line_name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="监控类型">
          <el-select
            v-model="elSelectMonitorType.id"
            placeholder="请选择监控类型"
            style="float:left;margin-bottom:20px;width:160px"
            clearable>
            <el-option v-for="item in monitorTypeInfo" :key="item.id" :value="item.id"
                       :label="item.type_name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="修复状态">
          <el-select
            v-model="elSelectIsFix.id"
            placeholder="请选择修复状态"
            style="float:left;margin-bottom:20px;width:160px"
            clearable>
            <el-option v-for="item in is_fix" :key="item.id" :value="item.id"
                       :label="item.desc"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="searchMonitorBugInfo"
            size="small"
            style="margin-left:15px">查询
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <div>
      <el-table
        :data="tableData"
        type="flex"
        style="
          width: 100%;
          margin-top:30px;
          font-size:14px;"
        max-height="100%"
        row-class-name="rowClass"
        :header-cell-style="headerTable">
        <el-table-column
          prop="id"
          label="ID"
          min-width="10%"
          align="center">
        </el-table-column>
        <el-table-column
          prop="monitor_case_name"
          label="描述"
          min-width="20%"
          align="left"
          :show-overflow-tooltip='true'>
        </el-table-column>
        <el-table-column
          prop="abnormal_content"
          label="问题数据"
          min-width="40%"
          align="left"
          :show-overflow-tooltip='true'>
        </el-table-column>
        <el-table-column
          label="状态"
          min-width="10%"
          align="center"
          :show-overflow-tooltip='true'>
          <template slot-scope="scope">
            <el-tag v-if="scope.row.is_fix===2" type="success">{{ scope.row.is_fix_desc }}</el-tag>
            <el-tag v-else-if="scope.row.is_fix===1" type="success">{{ scope.row.is_fix_desc }}</el-tag>
            <el-tag v-else type="warning">{{ scope.row.is_fix_desc }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="qa"
          label="QA"
          min-width="15%"
          align="center"
          :show-overflow-tooltip='true'>
        </el-table-column>
        <el-table-column
          prop="remarks"
          label="备注"
          min-width="20%"
          align="center"
          :show-overflow-tooltip='true'>
        </el-table-column>
        <el-table-column
          prop="create_time"
          label="创建日期"
          min-width="20%"
          align="center"
          :show-overflow-tooltip='true'>
        </el-table-column>
        <el-table-column
          label="操作"
          align="center"
          min-width="20%">
          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="monitor_bug_detail(scope.row)">查看处理
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div style="margin-top:30px">
      <el-pagination
        background
        style="text-align: center"
        layout="prev, pager, next"
        @current-change="handleCurrentChange"
        :current-page.sync="currentPage"
        :total="total">
      </el-pagination>
    </div>
    <el-dialog
      title="问题详细信息"
      :visible.sync="dialogVisible"
      width=50%>

      <el-row :gutter="20">
        <el-col :span="5">
          <div class="grid-content bg-purple-right"><span class="span-right">业务线</span></div>
        </el-col>
        <el-col :span="7">
          <div class="grid-content bg-purple-left">{{ monitor_bug_detail_info.business_line_name }}</div>
        </el-col>
        <el-col :span="5">
          <div class="grid-content bg-purple-right"><span class="span-right">告警次数</span></div>
        </el-col>
        <el-col :span="7">
          <div class="grid-content bg-purple-left">{{ monitor_bug_detail_info.count }}</div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="5">
          <div class="grid-content bg-purple-right"><span class="span-right">用例名称</span></div>
        </el-col>
        <el-col :span="19">
          <div class="grid-content bg-purple-left">{{ monitor_bug_detail_info.monitor_case_name }}</div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="5">
          <div class="grid-content bg-purple-right"><span class="span-right">函数方法名</span></div>
        </el-col>
        <el-col :span="19">
          <div class="grid-content bg-purple-left">{{ monitor_bug_detail_info.monitor_case_method }}</div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="5">
          <div class="grid-content bg-purple-right"><span class="span-right">问题数据</span></div>
        </el-col>
        <el-col :span="19">
          <div class="grid-content bg-purple-left">{{ monitor_bug_detail_info.abnormal_content }}</div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="5">
          <div class="grid-content bg-purple-right"><span class="span-right">当前状态</span></div>
        </el-col>
        <el-col :span="19">
          <el-select
            v-model="monitor_bug_detail_info.is_fix_id"
            placeholder="请选择状态"
            clearable>
            <el-option v-for="item in is_fix" :key="item.id" :value="item.id" :label="item.desc"></el-option>
          </el-select>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="5">
          <div class="grid-content bg-purple-right"><span class="span-right">原因分类</span></div>
        </el-col>
        <el-col :span="19">
          <el-select
            v-model="monitor_bug_detail_info.case_reason_id"
            placeholder="请选择原因"
            clearable>
            <el-option v-for="item in case_reason_desc_dict" :key="item.id" :value="item.id"
                       :label="item.desc"></el-option>
          </el-select>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="5">
          <div class="grid-content bg-purple-right"><span class="span-right">JIRA编号</span></div>
        </el-col>
        <el-col :span="19">
          <el-input
            v-model="monitor_bug_detail_info.jira_id"
            placeholder="请填写提交的jira编号"
            clearable></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="5">
          <div class="grid-content bg-purple-right"><span class="span-right">备注</span></div>
        </el-col>
        <el-col :span="19">
          <el-input
            v-model="monitor_bug_detail_info.remarks"
            placeholder="请填写您分析的原因"
            clearable></el-input>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="5">
          <div class="grid-content bg-purple-right"><span class="span-right">处理人员</span></div>
        </el-col>
        <el-col :span="19">
          <el-input
            v-model="monitor_bug_detail_info.fix_owner"
            placeholder="请填写问题解决人员，多个人员英文逗号分割"
            clearable></el-input>
        </el-col>
      </el-row>
      <el-row style="margin-top: 40px;margin-left: 40px">
        <el-button
          type="primary"
          @click="clickSave"
          size="small"
          style="float: left;">保存
        </el-button>
        <el-button
          size="small"
          style="float: left;margin-left:50px;"
          @click="dialogVisible = false">取消
        </el-button>
      </el-row>
    </el-dialog>
  </div>
</template>
<style>
.searchReport {
  width: 100%;
  height: 100px;
  background-color: #F2F6FC;
  margin-top: 30px;
}

.bg-purple-right {
  text-align: right;
  /*background-color: #F1F1EE;*/
}

.span-right {
  color: black;
  margin-right: 8px;
  font-weight: 600;
  letter-spacing: 3px;
}

.bg-purple-left {
  text-align: left;
}

.grid-content {
  border-radius: 4px;
  min-height: 40px;
  line-height: 40px;
  margin-top: 6px;
}

</style>

<script>

import Config from "../../Config";

export default {
  name: "CoverageReport",
  mounted: function () {
    this.initPage()
  },
  methods: {
    initPage() {
      //问题数据
      this.$axios({
        method: 'get',
        url: Config.DATA_MONITOR_SERVER + '/data_monitor_server/monitor-abnormal-record',
        params: {page: 1, limit: 10, ordering: '-create_time'}
      }).then(response => {
        if (response.data.errcode !== 20000) {
          this.$message({
            message: response.data.errmsg,
            type: "error"
          })
          return
        }
        this.tableData = response.data.data.data_list
        this.total = response.data.data.total
      })

      this.$axios({
        method: 'get',
        url: Config.DATA_MONITOR_SERVER + '/data_monitor_server/business-info',
        params: {page: 1, limit: 100}
      }).then(response => {
        if (response.data.errcode !== 20000) {
          this.$message({
            message: response.data.errmsg,
            type: "error"
          })
          return
        }
        this.businessInfo = response.data.data.data_list
      })

      //获取监控类型
      this.$axios({
        method: 'get',
        url: Config.DATA_MONITOR_SERVER + '/data_monitor_server/monitor-data-type',
        params: {page: 1, limit: 100}
      }).then(response => {
        if (response.data.errcode !== 20000) {
          this.$message({
            message: response.data.errmsg,
            type: "error"
          })
          return
        }
        this.monitorTypeInfo = response.data.data.data_list
      })
    },

    handleCurrentChange() {
      const dataJson = {
        business_line_id: this.elSelectBusinessLine.id,
        monitor_data_type: this.elSelectMonitorType.id,
        is_fix: this.elSelectIsFix.id,
        page: this.currentPage,
        ordering: '-create_time',
        limit: 10

      }
      this.search(dataJson)
    },
    searchMonitorBugInfo() {
      const dataJson = {
        business_line_id: this.elSelectBusinessLine.id,
        monitor_data_type: this.elSelectMonitorType.id,
        is_fix: this.elSelectIsFix.id,
        page: 1,
        ordering: '-create_time',
        limit: 10
      }
      this.search(dataJson)
    },
    search(dataJson) {
      this.$axios({
        method: 'get',
        url: Config.DATA_MONITOR_SERVER + '/data_monitor_server/monitor-abnormal-record',
        params: dataJson
      }).then(response => {
        if (response.data.errcode !== 20000) {
          this.$message({
            message: response.data.errmsg,
            type: "error"
          })
          return
        }
        this.tableData = response.data.data.data_list
        this.currentPage = dataJson.page
        this.total = response.data.data.total
      })
    },
    headerTable() {
      return 'background:#f5f6fa;color:rgba(0,0,0,.65);font-weight: 500'
    },
    monitor_bug_detail(rowData) {
      this.dialogVisible = true
      this.monitor_bug_detail_info.id = rowData.id
      this.monitor_bug_detail_info.business_line_name = rowData.business_line_name
      this.monitor_bug_detail_info.monitor_case_name = rowData.monitor_case_name
      this.monitor_bug_detail_info.monitor_case_method = rowData.monitor_case_method
      this.monitor_bug_detail_info.abnormal_content = rowData.abnormal_content
      this.monitor_bug_detail_info.count = rowData.count
      this.monitor_bug_detail_info.is_fix_desc = rowData.is_fix_desc
      this.$set(this.monitor_bug_detail_info, 'is_fix_id', rowData.is_fix)
      this.monitor_bug_detail_info.case_reason_desc = rowData.case_reason_desc
      this.$set(this.monitor_bug_detail_info, 'case_reason_id', rowData.case_reason)
      this.$set(this.monitor_bug_detail_info, 'remarks', rowData.remarks)
      this.$set(this.monitor_bug_detail_info, 'jira_id', rowData.jira_id)
      this.$set(this.monitor_bug_detail_info, 'fix_owner', rowData.fix_owner)

    },
    clickSave() {
      let dataJson = ''
      dataJson = {
        id: this.monitor_bug_detail_info.id,
        case_reason: this.monitor_bug_detail_info.case_reason_id,
        fix_owner: this.monitor_bug_detail_info.fix_owner,
        is_fix: this.monitor_bug_detail_info.is_fix_id,
        jira_id: this.monitor_bug_detail_info.jira_id,
        remarks: this.monitor_bug_detail_info.remarks
      }
      this.save(dataJson)
    },
    save(dataJson) {
      this.$axios({
        method: 'put',
        headers : {'user-id': 119},
        url: Config.DATA_MONITOR_SERVER + '/data_monitor_server/monitor-abnormal-record/'+dataJson.id,
        data: dataJson
      }).then(response => {
        if (response.data.errcode == 20000) {
          this.dialogVisible = false
          this.$message({
            message: '更新成功',
            type: "success"
          })
          this.initPage()
        }else {
          this.$message({
            message: response.data.errmsg,
            type: "error"
          })
        }
      })
    }
  },
  data() {
    return {
      is_fix: [{'id': 1, 'desc': '无需修复'}, {'id': 2, 'desc': '已修复'}, {'id': 0, 'desc': '未修复'}],
      case_reason_desc_dict: [{'id': 1, 'desc': '代码问题'}, {'id': 2, 'desc': '教研数据配置缺失'}, {
        'id': 3,
        'desc': '服务配置问题'
      }, {'id': 4, 'desc': '数据库配置问题'}, {'id': 5, 'desc': '外部三方问题'}, {
        'id': 6,
        'desc': '业务操作不规范'
      }, {'id': 7, 'desc': '非问题'}],
      elSelectIsFix: {},
      elSelectBusinessLine: {},
      elSelectMonitorType: {},
      monitor_bug_detail_info: {},
      monitorTypeInfo: [],
      businessInfo: [],
      tableData: [],
      currentPage: 1,
      total: 0,
      dialogVisible: false
    }
  },
  beforeUpdate() {
  }
}
</script>
