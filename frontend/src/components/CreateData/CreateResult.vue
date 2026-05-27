<template>
  <div class="create-data">
    <el-container>
      <el-header>
        <p class="create-result-info">造数结果:</p>
      </el-header>
      <el-main>
        <span class="api-module-message-value">组名: {{ dialog.moduleForm.team_name }} </span>
        <span class="api-module-message-value">类名: {{ dialog.moduleForm.class_name }} </span>
        <span class="api-module-message-value">方法名: {{ dialog.moduleForm.method_name }} </span>
        <br><br>
        <span class="api-module-message-value">请求参数:<br> {{ dialog.moduleForm.request_parameter }} </span>
        <br><br>
        <span class="api-module-message-value">描述: {{ dialog.moduleForm.method_function_detail }} </span>
<!--        <span class="api-module-message-value">结果: {{ dialog.moduleForm.result_info }} </span>-->
      </el-main>
      <el-footer>
        <span class="create-result-data">结果: <br>{{ dialog.moduleForm.result_info }} </span>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { ResultAdvance } from '@/api/CreateDtapi'

export default {
  name: 'CreateResult',
  data() {
    return {
      create_data_result_id: '',
      dialog: {
        moduleForm: {
          team_name: '',
          class_name: '',
          method_name: '',
          request_parameter: '',
          method_function_detail: '',
          result_info: ''
        }
      }
    }
  },
  methods: {
    getDetail() {
      ResultAdvance({ create_data_result_id: this.create_data_result_id }).then(data => {
        this.dialog.moduleForm = data.data
      })
    }
  },
  mounted() {
    this.create_data_result_id = this.$route.query.create_data_result_id
    this.getDetail()
  }
}
</script>

<style scoped>
.data {
  padding-left: 100px;
}
.create-result-info{
  text-align: center;
  font-family: 华文仿宋;
  font-size: 30px;
}

.api-module-message-value {
  color: #195fd9;
  font-family: 华文楷体;
  white-space: pre-wrap;
}

.create-result-data{
  color: #ec1270;
  font-size: 20px;
  font-family: 华文楷体;
  white-space: pre-wrap;
}

.api-data {
  white-space: pre-wrap;
}

.form-button {
  margin-top: 20px;
  text-align: center;
  bottom: 0;
}
</style>
