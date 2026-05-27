<template>
  <div class="page-wrap">
    <page-section title="项目详情">
      <key-value-descriptions :items="descriptionItems"></key-value-descriptions>
    </page-section>
  </div>
</template>

<script>
import PageSection from '@/components/TestPlatform/common/PageSection'
import KeyValueDescriptions from '@/components/TestPlatform/common/KeyValueDescriptions'
import { getProjectDetail } from '@/api/projectApi'

export default {
  name: 'ProjectDetail',
  components: { PageSection, KeyValueDescriptions },
  data() {
    return {
      detail: {}
    }
  },
  computed: {
    descriptionItems() {
      return [
        { label: '项目ID', value: this.detail.id },
        { label: '项目标识', value: this.detail.key },
        { label: '项目名称', value: this.detail.name },
        { label: '部门', value: this.detail.department },
        { label: '状态', value: this.detail.status === 0 ? '禁用' : '启用' },
        { label: '描述', value: this.detail.description },
        { label: '扩展配置', value: this.detail.config }
      ]
    }
  },
  methods: {
    fetchDetail() {
      const projectId = this.$route.query.projectId || 1
      getProjectDetail(projectId).then(res => {
        this.detail = (res && res.data) || res || {}
      }).catch(() => {
        this.detail = {}
      })
    }
  },
  created() {
    this.fetchDetail()
  }
}
</script>

<style scoped>
.page-wrap {
  padding: 20px;
}
</style>
