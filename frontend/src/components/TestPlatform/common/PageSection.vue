<template>
  <el-card shadow="never" class="page-section">
    <div slot="header" class="section-header">
      <span>{{ title }}</span>
      <div v-if="$slots.extra" class="section-extra">
        <slot name="extra"></slot>
      </div>
    </div>
    <div class="section-body">
      <slot></slot>
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'PageSection',
  props: {
    title: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.page-section {
  margin-bottom: 16px;
}
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.section-extra {
  margin-left: 16px;
}
</style>
