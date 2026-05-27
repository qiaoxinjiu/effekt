<template>
  <div style="margin-top: 20px;margin-right: 20px;margin-left: 20px">
    <el-breadcrumb separator="/" class="el-breadcrumb-div">
      <el-breadcrumb-item :to="{ path: '/dashboard' }">数据监控</el-breadcrumb-item>
      <el-breadcrumb-item>监控用例</el-breadcrumb-item>
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
        <el-form-item>
          <el-button
            type="primary"
            @click="searchMonitorCaseInfo"
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
          min-width="5%"
          align="center">
        </el-table-column>
        <el-table-column
          prop="case_name"
          label="用例名称"
          min-width="20%"
          align="center"
          :show-overflow-tooltip='true'>
        </el-table-column>
        <el-table-column
          prop="case_method"
          label="函数名称"
          min-width="19%"
          align="center"
          :show-overflow-tooltip='true'>
        </el-table-column>
        <el-table-column
          prop="monitor_data_type_name"
          label="监控类型"
          min-width="19%"
          align="center"
          :show-overflow-tooltip='true'>
        </el-table-column>
        <el-table-column
          prop="business_line_name"
          label="业务线"
          min-width="10%"
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
  </div>
</template>

<style>
.searchReport {
  width: 100%;
  height: 100px;
  background-color: #F2F6FC;
  margin-top: 30px;
}
</style>

<script>

import Config from "../../Config";

export default {
  name: "CaseInfo",
  mounted: function () {
    this.initPage()
  },
  methods: {
    initPage() {
      //监控用例数据
      this.$axios({
        method: 'get',
        url: Config.DATA_MONITOR_SERVER + '/data_monitor_server/monitor-case',
        params: {page: 1, limit: 10}
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
      var dataJson = {
        business_line_id: this.elSelectBusinessLine.id,
        monitor_data_type: this.elSelectMonitorType.id,
        page: this.currentPage,
        limit: 10
      }
      this.search(dataJson)
    },
    searchMonitorCaseInfo() {
      var dataJson = {
        business_line_id: this.elSelectBusinessLine.id,
        monitor_data_type: this.elSelectMonitorType.id,
        page: this.currentPage,
        limit: 10
      }
      this.search(dataJson)
    },
    search(dataJson) {
      this.$axios({
        method: 'get',
        url: Config.DATA_MONITOR_SERVER + '/data_monitor_server/monitor-case',
        params: dataJson
      }).then(response => {
        if (response.data.errcode != 20000) {
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
    }
  },
  data() {
    return {
      elSelectBusinessLine: {},
      elSelectMonitorType: {},
      tableData: [],
      currentPage: 1,
      total: 0,
      businessInfo: {},
      data_list: [],
      monitorTypeInfo: []
    }
  },
  beforeUpdate() {
  }
}
</script>
