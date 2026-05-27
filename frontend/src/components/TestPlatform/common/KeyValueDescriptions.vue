<template>
  <el-descriptions :column="column" border>
    <el-descriptions-item
      v-for="item in items"
      :key="item.label"
      :label="item.label">
      {{ formatValue(item.value) }}
    </el-descriptions-item>
  </el-descriptions>
</template>

<script>
export default {
  name: 'KeyValueDescriptions',
  props: {
    items: {
      type: Array,
      default: () => []
    },
    column: {
      type: Number,
      default: 2
    }
  },
  methods: {
    formatValue(value) {
      if (value === null || typeof value === 'undefined' || value === '') {
        return '-'
      }
      if (typeof value === 'object') {
        return JSON.stringify(value)
      }
      return String(value)
    }
  }
}
</script>
