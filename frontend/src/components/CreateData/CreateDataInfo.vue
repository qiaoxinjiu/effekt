<template>
  <div class="create-data-info">
    <el-card shadow="never">
      <div slot="header" class="clearfix">
        <span>{{ pageTitle }}</span>
      </div>
      <el-form v-loading="loading" ref="form" :model="form" :rules="rules" label-width="120px" size="small">
        <el-form-item label="项目名称" prop="project">
          <el-select v-model="form.project" placeholder="请选择项目" clearable style="width: 320px;">
            <el-option
              v-for="item in projectOptions"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="运行环境" prop="runEnv">
          <el-select v-model="form.runEnv" placeholder="请输入运行环境" clearable style="width: 320px;">
            <el-option
              v-for="item in envOptions"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="运行分组" prop="runGroup">
          <el-input v-model="form.runGroup" placeholder="请输入运行分组" style="width: 320px;"></el-input>
        </el-form-item>
        <el-form-item label="sql语句" prop="sql">
          <el-input
            v-model="form.sql"
            type="textarea"
            :rows="8"
            placeholder="请输入 sql 语句">
          </el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="form.remark"
            type="textarea"
            :rows="4"
            placeholder="请输入备注">
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="submitForm">保存</el-button>
          <el-button @click="goBack">返回</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import {ItApiCreate, ItApiDetail} from '@/api/CreateDtapi'

export default {
  name: 'CreateDataInfo',
  data() {
    return {
      saving: false,
      loading: false,
      projectOptions: ['ZHYY', 'DLZ', 'JOYHUB', 'OA', 'APP'],
      envOptions: ['dev', 'st', 'pre'],
      form: {
        project: '',
        runEnv: '',
        sql: '',
        remark: '',
        sqlId: '',
        runGroup: ''
      },
      rules: {
        project: [{required: true, message: '请选择项目名称', trigger: 'change'}],
        runEnv: [{required: true, message: '请选择运行环境', trigger: 'change'}],
        sql: [{required: true, message: '请输入sql语句', trigger: 'blur'}],
        runGroup: [{required: true, message: '请输入运行分组', trigger: 'blur'}]
      }
    }
  },
  computed: {
    pageTitle() {
      return this.form.sqlId ? '修改造数任务' : '新增造数任务'
    }
  },
  methods: {
    initForm() {
      const query = this.$route.query || {}
      this.form = {
        project: '',
        runEnv: '',
        sql: '',
        remark: '',
        sqlId: query.sqlId || query.id || query.create_data_detail_id || '',
        runGroup: ''
      }
      if (this.form.sqlId) {
        this.getDetail()
      }
    },
    getDetail() {
      this.loading = true
      ItApiDetail({sqlId: this.form.sqlId}).then(res => {
        const data = res && res.data ? res.data : {}
        this.form = {
          ...this.form,
          project: data.project || '',
          runEnv: data.runEnv || data.run_env || '',
          sql: data.sql || '',
          remark: data.remark || '',
          sqlId: data.sqlId || data.sql_id || data.id || data.create_data_detail_id || this.form.sqlId,
          runGroup: data.runGroup || data.run_group || ''
        }
      }).catch(err => {
        this.$message({type: 'error', message: (err && err.message) || '详情获取失败'})
      }).finally(() => {
        this.loading = false
      })
    },
    submitForm() {
      this.$refs.form.validate(valid => {
        if (!valid) {
          return false
        }
        this.saving = true
        ItApiCreate(this.form).then(res => {
          if (res && res.success === true) {
            this.$message({type: 'success', message: this.form.sqlId ? '修改成功' : '新增成功'})
            this.$router.push({path: '/data-tools/db-builder'})
          } else {
            this.$message({type: 'error', message: res.message || '保存失败'})
          }
        }).finally(() => {
          this.saving = false
        })
      })
    },
    goBack() {
      this.$router.push({path: '/data-tools/db-builder'})
    }
  },
  created() {
    this.initForm()
  }
}
</script>

<style scoped>
.create-data-info {
  padding: 20px;
}
</style>

