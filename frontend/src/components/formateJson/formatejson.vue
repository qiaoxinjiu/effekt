<template>
  <div class="json">
    <div class="json-yuan" style="float: left;width: 50%;height: 100%">
      <el-input
        v-model="json"
        type="textarea"
        :autosize="{ minRows: 20}"
        placeholder="请输入内容">
      </el-input>
    </div>
    <div class="json-formate" style="float: left;width: 50%">
      <JsonView :json="JsonData"></JsonView>
    </div>
  </div>
</template>

<script>
import JsonView from '@/components/formateJson/JsonView'

export default {
  name: 'formatejson',
  components: { JsonView },
  data() {
    return {
      json: '',
      JsonData: ''
    }
  },
  watch: {
    json(val) {
      try {
        this.JsonData = JSON.parse(val)
      } catch (e) {
        this.JsonData = e.toString()
      }
    }
  }
}
</script>

<style scoped>
</style>
