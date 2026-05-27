<template>
  <div class="effekt-home">
    <el-row :gutter="20" class="top-row">
      <el-col :xs="24" :md="10">
        <el-card shadow="never" class="greet-card">
          <div class="greet-line">{{ greetingPrefix }}{{ greetingTime }}</div>
          <div class="greet-date">{{ todayText }}</div>
          <div v-if="currentUser" class="greet-progress">
            <span class="greet-progress-label">待处理进度</span>
            <el-progress :percentage="100" :stroke-width="10" status="success" />
            <span class="greet-progress-tip">已完成 100%</span>
          </div>
          <div v-else class="greet-login-tip">
            <el-link type="primary" @click="goLogin">登录后查看个人工作台</el-link>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="14">
        <el-card shadow="never" class="work-card">
          <div class="work-card-title">今天剩余工作总计</div>
          <div class="work-stats">
            <div class="work-stat">
              <div class="work-stat-value">{{ formatCount(workCountOpportunity) }}</div>
              <div class="work-stat-label">我的机会</div>
            </div>
            <div class="work-stat work-stat--click" @click="goMyBugs">
              <div class="work-stat-value">{{ formatCount(workCountBug) }}</div>
              <div class="work-stat-label">我的 BUG</div>
              <div class="work-stat-hint">点击查看指派给我</div>
            </div>
            <div class="work-stat work-stat--click" @click="goMyPlans">
              <div class="work-stat-value">{{ formatCount(workCountPlan) }}</div>
              <div class="work-stat-label">我的计划</div>
              <div class="work-stat-hint">点击查看我负责的</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="never" class="links-card">
      <div class="links-card-title">环境与文档</div>
      <p class="home-desc">这里汇总各项目常用环境地址和文档链接，方便快速进入。</p>
      <div
        v-for="project in projectLinks"
        :key="project.name"
        class="project-block">
        <div class="project-title">{{ project.name }}</div>
        <div class="project-links">
          <div v-for="item in project.links" :key="item.name" class="link-item">
            <span class="link-label">{{ item.name }}：</span>
            <el-link
              :href="item.url"
              target="_blank"
              type="primary"
              class="doc-link">
              {{ item.url }}
            </el-link>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getBugList } from '@/api/bugApi'
import { getPlanList } from '@/api/planApi'
import { readLastProductProjectCache } from '@/utils/lastProductProjectCache'

export default {
  name: 'EffektHome',
  data() {
    return {
      workCountOpportunity: null,
      workCountBug: null,
      workCountPlan: null,
      projectLinks: [
        {
          name: '智慧运营',
          links: [
            { name: '测试环境地址', url: 'https://smart-management-web-st.best-envision.com/' },
            { name: 'pre环境地址', url: 'https://smart-management-web-pre.best-envision.com/' },
            { name: '需求文档', url: 'https://vcncbabzm4lv.feishu.cn/wiki/UsvzwMzV0i7Lrgk9VIhc2XgJn6e?fromScene=spaceOverview' },
            { name: '资源连接地址(包含数据库连接，jenkins配置，git仓库，日志查询，xxjob等)', url: 'https://vcncbabzm4lv.feishu.cn/wiki/ZKmown7QuiXtwTkONhUcagpQnWh' },
            { name: '领星地址', url: 'https://envision.lingxing.com/erp/home' },
            { name: '禅道地址', url: 'http://39.170.26.156:8888/my.html' }
          ]
        },
        {
          name: '独立站项目',
          links: [
            { name: '管理后台测试环境地址', url: 'https://joyhub-website-manager-web-test.best-envision.com/' },
            { name: 'web的C端测试环境地址', url: 'https://joyhub-website-frontend-test.best-envision.com/' },
            { name: '接口开发地址', url: 'https://joyhub-website-manager-api-test.best-envision.com/doc.html#/home' },
            { name: '资源连接地址', url: 'https://vcncbabzm4lv.feishu.cn/wiki/PXTmw6BBviMjNDkKCxCcewD7nMd' },
            { name: '禅道地址', url: 'http://192.168.16.4:8956/index.php?m=my&f=index' }
          ]
        }
      ]
    }
  },
  computed: {
    currentUser() {
      return this.$store.state.currentUser
    },
    greetingPrefix() {
      const u = this.currentUser
      if (!u) return ''
      const name = u.realName || u.username || ''
      return name ? `${name}，` : ''
    },
    greetingTime() {
      const h = new Date().getHours()
      if (h < 12) return '上午好！'
      if (h < 18) return '下午好！'
      return '晚上好！'
    },
    todayText() {
      const d = new Date()
      const y = d.getFullYear()
      const m = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${y}年${m}月${day}日`
    }
  },
  mounted() {
    this.refreshWorkCounts()
  },
  methods: {
    formatCount(n) {
      if (n === null || n === undefined || Number.isNaN(Number(n))) return '—'
      return String(n)
    },
    goLogin() {
      this.$router.push({ name: 'login' })
    },
    goMyBugs() {
      if (!this.currentUser) {
        this.$message.warning('请先登录')
        this.goLogin()
        return
      }
      const c = readLastProductProjectCache()
      const q = { assignToMe: '1' }
      if (c && c.productId !== undefined && c.productId !== null && String(c.productId).trim() !== '') {
        q.productId = String(c.productId)
      }
      if (c && c.projectId !== undefined && c.projectId !== null && String(c.projectId).trim() !== '') {
        q.projectId = String(c.projectId)
      }
      this.$router.push({ path: '/bug/list', query: q })
    },
    goMyPlans() {
      if (!this.currentUser) {
        this.$message.warning('请先登录')
        this.goLogin()
        return
      }
      const c = readLastProductProjectCache()
      const q = { planOwnerSelf: '1' }
      if (c && c.productId !== undefined && c.productId !== null && String(c.productId).trim() !== '') {
        q.productId = String(c.productId)
      }
      if (c && c.projectId !== undefined && c.projectId !== null && String(c.projectId).trim() !== '') {
        q.projectId = String(c.projectId)
      }
      this.$router.push({ path: '/test-platform/plan', query: q })
    },
    refreshWorkCounts() {
      const u = this.currentUser
      const c = readLastProductProjectCache()
      this.workCountOpportunity = null
      this.workCountBug = null
      this.workCountPlan = null
      if (!u || u.id == null || u.id === '' || !c || !c.projectId) {
        return
      }
      getBugList({
        productId: c.productId,
        projectId: c.projectId,
        assigneeId: u.id,
        pageNo: 1,
        pageSize: 1
      })
        .then(res => {
          const data = (res && res.data) || res || {}
          this.workCountBug = Number(data.total != null ? data.total : 0)
        })
        .catch(() => {
          this.workCountBug = null
        })
      getPlanList(c.projectId, {
        owner_id: u.id,
        owner: u.id,
        pageNo: 1,
        pageSize: 1
      })
        .then(res => {
          const data = (res && res.data) || res || {}
          this.workCountPlan = Number(data.total != null ? data.total : 0)
        })
        .catch(() => {
          this.workCountPlan = null
        })
    }
  }
}
</script>

<style scoped>
.effekt-home {
  max-width: 1240px;
  margin: 0 auto;
}

.top-row {
  margin-bottom: 20px;
}

.greet-card,
.work-card,
.links-card {
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 18px;
  box-shadow: 0 18px 48px rgba(0, 0, 0, 0.24), inset 0 1px 0 rgba(255, 255, 255, 0.04);
  overflow: hidden;
  background: #111827;
}

.greet-card,
.work-card {
  min-height: 174px;
}

.greet-card {
  position: relative;
  background: radial-gradient(circle at 88% 16%, rgba(103, 232, 249, 0.28), transparent 28%), linear-gradient(135deg, rgba(30, 64, 175, 0.95) 0%, rgba(15, 23, 42, 0.96) 62%, rgba(8, 13, 27, 0.98) 100%);
  color: #fff;
  border-color: rgba(103, 232, 249, 0.22);
}

.greet-card:after {
  content: '';
  position: absolute;
  right: -44px;
  bottom: -54px;
  width: 170px;
  height: 170px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.26), transparent 68%);
}

.greet-card >>> .el-card__body,
.work-card >>> .el-card__body,
.links-card >>> .el-card__body {
  padding: 24px;
  position: relative;
  z-index: 1;
}

.greet-line {
  font-size: 24px;
  font-weight: 800;
  color: #f8fbff;
  margin-bottom: 8px;
  letter-spacing: 0.2px;
}

.greet-date {
  color: #bae6fd;
  font-size: 13px;
  margin-bottom: 22px;
}

.greet-progress-label {
  font-size: 12px;
  color: rgba(224, 242, 254, 0.9);
  display: block;
  margin-bottom: 8px;
}

.greet-progress >>> .el-progress-bar__outer {
  background-color: rgba(15, 23, 42, 0.68);
}

.greet-progress >>> .el-progress-bar__inner {
  background: linear-gradient(90deg, #22d3ee 0%, #6366f1 100%);
}

.greet-progress-tip {
  font-size: 12px;
  color: #a7f3d0;
  margin-top: 8px;
  display: block;
}

.greet-login-tip {
  margin-top: 8px;
}

.greet-login-tip >>> .el-link.el-link--primary {
  color: #67e8f9;
  font-weight: 700;
}

.work-card-title,
.links-card-title {
  position: relative;
  font-size: 16px;
  font-weight: 800;
  color: #e0f2fe;
  margin-bottom: 18px;
  padding-left: 12px;
  letter-spacing: 0.3px;
}

.work-card-title:before,
.links-card-title:before {
  content: '';
  position: absolute;
  left: 0;
  top: 3px;
  width: 4px;
  height: 16px;
  border-radius: 999px;
  background: linear-gradient(180deg, #67e8f9 0%, #6366f1 100%);
  box-shadow: 0 0 14px rgba(103, 232, 249, 0.55);
}

.work-stats {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 14px;
}

.work-stat {
  flex: 1;
  min-width: 126px;
  text-align: left;
  padding: 18px;
  border-radius: 16px;
  background: #162033;
  border: 1px solid rgba(148, 163, 184, 0.18);
  cursor: default;
  transition: box-shadow 0.2s ease, border-color 0.2s ease, transform 0.2s ease, background 0.2s ease;
}

.work-stat--click {
  cursor: pointer;
}

.work-stat--click:hover {
  border-color: rgba(56, 189, 248, 0.52);
  background: #1e293b;
  box-shadow: 0 0 24px rgba(56, 189, 248, 0.14), 0 18px 34px rgba(0, 0, 0, 0.24);
  transform: translateY(-2px);
}

.work-stat-value {
  font-size: 32px;
  font-weight: 900;
  color: #67e8f9;
  line-height: 1.1;
  text-shadow: 0 0 18px rgba(103, 232, 249, 0.35);
}

.work-stat-label {
  margin-top: 10px;
  font-size: 14px;
  color: #dbeafe;
  font-weight: 700;
}

.work-stat-hint {
  margin-top: 6px;
  font-size: 12px;
  color: #8fb3d9;
}

.links-card {
  background: #111827;
}

.home-content {
  display: flex;
  flex-direction: column;
}

.home-desc {
  margin: 0 0 18px;
  color: #94a3b8;
  font-size: 13px;
}

.project-block {
  padding: 18px;
  margin-bottom: 14px;
  border: 1px solid rgba(148, 163, 184, 0.16);
  border-radius: 16px;
  background: #162033;
}

.project-block:last-child {
  margin-bottom: 0;
}

.project-title {
  margin-bottom: 12px;
  font-size: 16px;
  font-weight: 800;
  color: #e0f2fe;
}

.link-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
  line-height: 22px;
}

.link-item:last-child {
  margin-bottom: 0;
}

.link-label {
  min-width: 150px;
  color: #b7c9df;
  font-weight: 700;
}

.doc-link {
  word-break: break-all;
}

.doc-link >>> span {
  color: #67e8f9;
}

body.theme-light .greet-card,
body.theme-light .work-card,
body.theme-light .links-card {
  background: #ffffff;
  border-color: #dbe5f3;
  box-shadow: 0 14px 34px rgba(37, 99, 235, 0.08);
}

body.theme-light .greet-card {
  background: radial-gradient(circle at 88% 16%, rgba(96, 165, 250, 0.24), transparent 28%), linear-gradient(135deg, #2563eb 0%, #3b82f6 58%, #60a5fa 100%);
  color: #ffffff;
  border-color: rgba(96, 165, 250, 0.42);
}

body.theme-light .greet-card:after {
  background: radial-gradient(circle, rgba(255, 255, 255, 0.26), transparent 68%);
}

body.theme-light .greet-date,
body.theme-light .greet-progress-label {
  color: rgba(239, 246, 255, 0.92);
}

body.theme-light .greet-progress >>> .el-progress-bar__outer {
  background-color: rgba(255, 255, 255, 0.28);
}

body.theme-light .greet-login-tip >>> .el-link.el-link--primary {
  color: #ffffff;
}

body.theme-light .work-card-title,
body.theme-light .links-card-title,
body.theme-light .project-title {
  color: #0f172a;
}

body.theme-light .work-card-title:before,
body.theme-light .links-card-title:before {
  background: linear-gradient(180deg, #2563eb 0%, #38bdf8 100%);
  box-shadow: 0 8px 16px rgba(37, 99, 235, 0.18);
}

body.theme-light .work-stat,
body.theme-light .project-block {
  background: #f8fbff;
  border-color: #e2e8f0;
}

body.theme-light .work-stat--click:hover {
  background: #eef6ff;
  border-color: #bfdbfe;
  box-shadow: 0 14px 28px rgba(37, 99, 235, 0.12);
}

body.theme-light .work-stat-value {
  color: #2563eb;
  text-shadow: none;
}

body.theme-light .work-stat-label,
body.theme-light .link-label {
  color: #334155;
}

body.theme-light .work-stat-hint,
body.theme-light .home-desc {
  color: #64748b;
}

body.theme-light .doc-link >>> span {
  color: #2563eb;
}
</style>
