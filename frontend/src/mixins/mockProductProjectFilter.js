import { getProductList } from '@/api/productApi'
import { getProjectList } from '@/api/projectApi'
import {
  readLastProductProjectCache,
  saveLastProductProjectCache,
  pickIdFromOptions
} from '@/utils/lastProductProjectCache'

/** Mock 模块：产品/项目筛选（展示名称，请求仍传 id） */
export default {
  data() {
    return {
      selectedProductId: '',
      selectedProjectId: '',
      productOptions: [],
      projectOptions: []
    }
  },
  computed: {
    mockProductId() {
      return this.selectedProductId || ''
    },
    mockProjectId() {
      return this.selectedProjectId || ''
    }
  },
  methods: {
    loadMockProductOptions() {
      if (this.productOptions && this.productOptions.length) {
        return Promise.resolve()
      }
      return getProductList({ pageNo: 1, pageSize: 1000, status: 1 }).then(res => {
        const data = (res && res.data) || res || {}
        this.productOptions = data.items || data.list || data.data || []
      }).catch(() => {
        this.productOptions = []
      })
    },
    loadMockProjectOptions(productId) {
      if (!productId) {
        this.projectOptions = []
        return Promise.resolve()
      }
      return getProjectList({ pageNo: 1, pageSize: 1000, status: 1, productId }).then(res => {
        const data = (res && res.data) || res || {}
        this.projectOptions = data.items || data.list || data.data || []
      }).catch(() => {
        this.projectOptions = []
      })
    },
    bootstrapMockProductProject() {
      const routePid = this.$route.query.productId ? Number(this.$route.query.productId) : ''
      const routeProj = this.$route.query.projectId ? Number(this.$route.query.projectId) : ''
      return this.loadMockProductOptions().then(() => {
        if (routePid) {
          this.selectedProductId = pickIdFromOptions(this.productOptions, routePid)
          return this.loadMockProjectOptions(this.selectedProductId).then(() => {
            if (routeProj) {
              this.selectedProjectId = pickIdFromOptions(this.projectOptions, routeProj)
            }
          })
        }
        const cached = readLastProductProjectCache()
        if (cached && cached.productId != null && cached.projectId != null) {
          const hasProduct = (this.productOptions || []).some(p => String(p.id) === String(cached.productId))
          if (!hasProduct) return
          this.selectedProductId = pickIdFromOptions(this.productOptions, cached.productId)
          return this.loadMockProjectOptions(this.selectedProductId).then(() => {
            this.selectedProjectId = pickIdFromOptions(this.projectOptions, cached.projectId)
          })
        }
      })
    },
    handleMockProductChange() {
      this.selectedProjectId = ''
      this.projectOptions = []
      this.loadMockProjectOptions(this.selectedProductId)
      if (typeof this.onMockProductProjectChange === 'function') {
        this.onMockProductProjectChange()
      }
    },
    handleMockProjectChange() {
      if (this.selectedProductId && this.selectedProjectId) {
        saveLastProductProjectCache(this.selectedProductId, this.selectedProjectId)
      }
      this.syncMockRouteQuery()
      if (typeof this.onMockProductProjectChange === 'function') {
        this.onMockProductProjectChange()
      }
    },
    syncMockRouteQuery() {
      const q = Object.assign({}, this.$route.query || {})
      if (this.selectedProductId) {
        q.productId = this.selectedProductId
      } else {
        delete q.productId
      }
      if (this.selectedProjectId) {
        q.projectId = this.selectedProjectId
      } else {
        delete q.projectId
      }
      const prev = JSON.stringify(this.$route.query || {})
      const next = JSON.stringify(q)
      if (prev !== next) {
        this.$router.replace({ path: this.$route.path, query: q }).catch(() => {})
      }
    },
    resolveMockProductId(row) {
      if (!row) return ''
      if (row.product_id != null && row.product_id !== '') return row.product_id
      if (row.productId != null && row.productId !== '') return row.productId
      const projectId = row.project_id != null && row.project_id !== '' ? row.project_id : row.projectId
      if (projectId != null && projectId !== '') {
        const proj = (this.projectOptions || []).find(p => String(p.id) === String(projectId))
        if (proj) {
          const fromProject = proj.product_id != null && proj.product_id !== '' ? proj.product_id : proj.productId
          if (fromProject != null && fromProject !== '') return fromProject
        }
      }
      if (this.selectedProductId != null && this.selectedProductId !== '') {
        return this.selectedProductId
      }
      return ''
    },
    formatMockProductName(row) {
      if (!row) return '—'
      const directName = row.product_name || row.productName
      if (directName) return directName
      const projectId = row.project_id != null && row.project_id !== '' ? row.project_id : row.projectId
      if (projectId != null && projectId !== '') {
        const proj = (this.projectOptions || []).find(p => String(p.id) === String(projectId))
        const projectProductName = proj && (proj.product_name || proj.productName)
        if (projectProductName) return projectProductName
      }
      const productId = this.resolveMockProductId(row)
      if (productId !== undefined && productId !== null && productId !== '') {
        const hit = (this.productOptions || []).find(p => String(p.id) === String(productId))
        if (hit && hit.name) return hit.name
      }
      return '—'
    },
    formatMockProjectName(row) {
      if (!row) return '—'
      const name = row.project_name || row.projectName
      if (name) return name
      const id = row.project_id != null && row.project_id !== '' ? row.project_id : row.projectId
      if (id === undefined || id === null || id === '') {
        if (this.selectedProjectId != null && this.selectedProjectId !== '') {
          const hit = (this.projectOptions || []).find(p => String(p.id) === String(this.selectedProjectId))
          return (hit && hit.name) || '—'
        }
        return '—'
      }
      const hit = (this.projectOptions || []).find(p => String(p.id) === String(id))
      return (hit && hit.name) || id
    }
  }
}
