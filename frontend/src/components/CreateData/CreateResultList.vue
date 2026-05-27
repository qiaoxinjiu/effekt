<template>
  <div class="create-data">
    <div class="search">
      <el-form :inline="true" class="search" size="small" @submit.native.prevent>
        <el-form-item label="业务线">
          <el-select
            v-model="team_name"
            placeholder="请选择业务线"
            style="width:160px"
            clearable
            @change="pageNo = 1">
            <el-option v-for="item in dict_data" :key="item.value" :value="item.value" :label="item.label"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="" labelWidth="110px">
          <el-input v-model="detail_name" placeholder="场景名称" clearable @change="search" @keyup.enter="search"></el-input>
        </el-form-item>
        <el-form-item label="" labelWidth="110px">
          <el-input v-model="get_tag" placeholder="备注" clearable @change="search" @keyup.enter="search"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="search" @keyup.enter="search">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="api-form">
      <el-table
        ref="table"
        :data="tableData"
        :header-cell-style="{ textAlign: 'center' }"
        :stripe="true"
        :height="tableHeight"
        border>
        <el-table-column label="场景名称" prop="method_function_detail"></el-table-column>
        <el-table-column label="请求参数" prop="request_parameter" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column label="结果数据" prop="result_info" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column label="业务线" prop="team_name"></el-table-column>
        <el-table-column label="创建时间" prop="created_time">
          <template slot-scope="props">
            {{ formatTimeValue(props.row.created_time) }}
          </template>
        </el-table-column>
        <el-table-column label="备注" prop="tag"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="props">
            <el-button type="text" @click.native.prevent="openResult(props.row)">查看详情</el-button>
            <el-button type="text" @click.native.prevent="tryRunCreateData(props.row)">再来一次</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-dialog title="造数结果" :visible.sync="result_dialog.dialogVisible" width="50%">
        <div v-if="is_json">
          <JsonView :json="JsonData"></JsonView>
        </div>
        <div v-else>
          <span>{{ result_dialog.result_info }}</span>
        </div>
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
</template>

<script>
import { GetTeam, ResultAdvance, ResultQuery } from '@/api/CreateDtapi'
import JsonView from '@/components/formateJson/JsonView'
import { formatTime } from '@/utils/util'

export default {
  name: 'CreateResultList',
  components: { JsonView },
  data() {
    return {
      tableHeight: null,
      team_name: '',
      detail_name: '',
      get_tag: '',
      total: 0,
      is_json: '',
      tableData: [],
      dict_data: {},
      pageNo: 1,
      pageSize: 10,
      JsonData: '',
      result_dialog: {
        dialogVisible: false,
        result_info: ''
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
      ResultQuery(data).then(data => {
        this.tableData = data.data
        this.total = data.totalCount
      })
    },
    search(keepPage) {
      if (!keepPage) {
        this.pageNo = 1
      }
      this.dataList({
        pageNo: this.pageNo,
        pageSize: this.pageSize,
        team_name: this.team_name || '',
        detail_name: this.detail_name || '',
        get_tag: this.get_tag || ''
      })
    },
    resetResultDialog() {
      this.result_dialog = {
        dialogVisible: false,
        result_info: ''
      }
      this.JsonData = ''
      this.is_json = ''
    },
    getJsonData(val) {
      try {
        this.JsonData = JSON.parse(val)
      } catch (e) {
        this.JsonData = e.toString()
      }
    },
    openResult(row) {
      this.result_dialog.dialogVisible = true
      ResultAdvance({ create_data_result_id: row.create_data_result_id }).then(data => {
        if (data.code === 200) {
          this.result_dialog.result_info = data.data.result_info
          this.is_json = data.data.is_json
          this.getJsonData(data.data.result_info)
        } else {
          this.result_dialog.result_info = data.message
        }
      }).catch(() => {
        this.resetResultDialog()
      })
    },
    tryRunCreateData(row) {
      this.$router.push({
        path: '/create/info',
        query: {
          create_data_detail_id: row.create_data_detail_id,
          create_data_result_id: row.create_data_result_id
        }
      })
    },
    getTeamName(team) {
      GetTeam({ data_type: 2, team_name: team }).then(data => {
        if (data.code === 200) {
          this.dict_data = data.data
        }
      })
    }
  },
  created() {
    this.team_name = this.$route.query.team_name || ''
    this.detail_name = this.$route.query.method_function_detail || ''
    this.get_tag = this.$route.query.get_tag || ''
    this.dataList({
      pageNo: 1,
      pageSize: 10,
      team_name: this.team_name,
      detail_name: this.detail_name,
      get_tag: this.get_tag
    })
    this.tableHeight = document.getElementById('app').clientHeight - 183
    this.getTeamName('')
  }
}
</script>

<style scoped>
.data {
  padding-left: 100px;
}

pre {
  outline: 1px solid #ccc;
  padding: 5px;
  margin: 5px;
}

.string {
  color: green;
}

.number {
  color: darkorange;
}

.boolean {
  color: blue;
}

.null {
  color: magenta;
}

.key {
  color: red;
}
</style>
