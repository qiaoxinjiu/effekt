<template>
  <div id="backgroud" :class="themeClass">
    <button class="login-theme-switch" type="button" @click="toggleTheme">
      <i :class="themeIcon"></i>
      <span>{{ themeLabel }}</span>
    </button>
    <div class="login-hero">
      <div class="login-brand-mark">效</div>
      <h1>效能平台</h1>
      <p>统一管理测试协作、缺陷跟踪、用例周期与数据工具。</p>
    </div>
    <div class="content_right">
      <div class="login-body-title">
        <h2>欢迎登录</h2>
        <p>Quality Workspace</p>
      </div>
      <div class="messge">
        <span>{{ msg }}</span>
      </div>
      <div class="cr_top">
        <div class="ct_input">
          <span class="ct-img-yhm">&nbsp;</span>
          <input
            id="username"
            v-model.trim="username"
            name="username"
            class="input_text"
            tabindex="1"
            accesskey="n"
            type="text"
            size="25"
            autocomplete="off"
            placeholder="用户名"
            @keyup.enter="handleLogin">
        </div>
        <div class="ct_input">
          <span class="ct_img_mm">&nbsp;</span>
          <input
            id="password"
            v-model="password"
            name="password"
            class="input_text"
            tabindex="2"
            accesskey="p"
            type="password"
            size="25"
            autocomplete="off"
            placeholder="密码"
            @keyup.enter="handleLogin">
        </div>
        <input class="btn_login" value="登录" @click="handleLogin">
      </div>
      <div class="account-oprate clearfix">
        <router-link :to="{ name: 'register' }" class="regist-btn">注册</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { Login } from '@/api/Userapi'
import { getRoleList, parseMenusFromRoleListResponse } from '@/api/rbacApi'

export default {
  name: 'Login',
  data() {
    return {
      msg: '',
      username: '',
      password: '',
      uiTheme: localStorage.getItem('uiTheme') || 'dark'
    }
  },
  computed: {
    themeClass() {
      return this.uiTheme === 'light' ? 'theme-login-light' : 'theme-login-dark'
    },
    themeLabel() {
      return this.uiTheme === 'light' ? '深色' : '浅色'
    },
    themeIcon() {
      return this.uiTheme === 'light' ? 'el-icon-moon' : 'el-icon-sunny'
    }
  },
  mounted() {
    this.applyTheme()
  },
  methods: {
    applyTheme() {
      document.body.classList.remove('theme-dark', 'theme-light')
      document.body.classList.add(this.uiTheme === 'light' ? 'theme-light' : 'theme-dark')
    },
    toggleTheme() {
      this.uiTheme = this.uiTheme === 'light' ? 'dark' : 'light'
      localStorage.setItem('uiTheme', this.uiTheme)
      this.applyTheme()
    },
    handleLogin() {
      if (!this.username || !this.password) {
        this.msg = 'username、password 为必传参数'
        return
      }
      Login({
        username: this.username,
        password: this.password
      }).then(res => {
        if (res && res.code === 20000) {
          const data = res.data || {}
          const user = {
            id: data.id,
            username: data.username,
            realName: data.real_name,
            mobile: data.mobile,
            email: data.email,
            avatar: data.avatar,
            status: data.status,
            lastLoginTime: data.last_login_time,
            createdBy: data.created_by,
            createdTime: data.created_time,
            updatedTime: data.updated_time,
            roleIds: data.role_ids || []
          }
          localStorage.setItem('authUser', JSON.stringify(user))
          if (data.token) {
            localStorage.setItem('accessToken', data.token)
          } else {
            localStorage.removeItem('accessToken')
          }
          const rt = data.refresh_token || data.refreshToken
          if (rt) {
            localStorage.setItem('refreshToken', rt)
          } else {
            localStorage.removeItem('refreshToken')
          }
          this.$store.commit('SetCurrentUser', user)
          this.$store.commit('SetRole', user.roleIds)
          this.$store.commit('SetUserMenus', [])
          this.loadUserMenus(user)
          this.msg = ''
          this.$message.success('登录成功')
          this.$router.push({ path: '/effekt' })
        } else {
          this.msg = (res && res.message) || '用户名或密码错误！'
        }
      })
    },
    loadUserMenus(user) {
      const roleId = user && user.roleIds && user.roleIds.length ? user.roleIds[0] : undefined
      if (!roleId) {
        return
      }
      getRoleList({ roleId }).then(res => {
        this.$store.commit('SetUserMenus', parseMenusFromRoleListResponse(res))
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
@import "../../assets/css/Form.css";

#backgroud {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 80px;
  background: radial-gradient(circle at 15% 18%, rgba(34, 211, 238, 0.22), transparent 26%), radial-gradient(circle at 82% 22%, rgba(99, 102, 241, 0.24), transparent 30%), linear-gradient(135deg, #050914 0%, #08111f 46%, #0f172a 100%);
  overflow: hidden;
}

.login-hero {
  width: 420px;
  color: #f8fbff;
}

.login-brand-mark {
  width: 56px;
  height: 56px;
  line-height: 56px;
  text-align: center;
  border-radius: 18px;
  font-size: 28px;
  font-weight: 900;
  color: #06111f;
  background: linear-gradient(135deg, #67e8f9 0%, #38bdf8 45%, #6366f1 100%);
  box-shadow: 0 0 34px rgba(56, 189, 248, 0.48), 0 22px 48px rgba(99, 102, 241, 0.28);
}

.login-hero h1 {
  margin: 24px 0 14px;
  font-size: 42px;
  line-height: 1.15;
  letter-spacing: 1px;
  text-shadow: 0 0 26px rgba(103, 232, 249, 0.22);
}

.login-hero p {
  margin: 0;
  color: #9fb8d4;
  font-size: 16px;
  line-height: 1.8;
}

.login-theme-switch {
  position: fixed;
  right: 28px;
  top: 24px;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 36px;
  padding: 0 12px;
  border-radius: 999px;
  border: 1px solid rgba(56, 189, 248, 0.22);
  color: #dbeafe;
  background: rgba(15, 23, 42, 0.78);
  cursor: pointer;
  transition: background 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

.login-theme-switch:hover {
  background: rgba(14, 165, 233, 0.18);
  box-shadow: 0 0 18px rgba(56, 189, 248, 0.18);
  transform: translateY(-1px);
}

.content_right {
  padding: 34px 36px 30px;
  background: rgba(15, 23, 42, 0.78);
  color: #dbeafe;
  border-radius: 24px;
  border: 1px solid rgba(56, 189, 248, 0.22);
  box-shadow: 0 0 42px rgba(56, 189, 248, 0.12), 0 30px 90px rgba(0, 0, 0, 0.42), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  position: static;
  width: 330px;
  min-height: 340px;
  text-align: center;
  backdrop-filter: blur(18px);
}

.login-body-title h2 {
  font-size: 26px;
  color: #e0f2fe;
  margin-bottom: 8px;
}

.login-body-title p {
  color: #67e8f9;
  font-size: 13px;
  letter-spacing: 0.8px;
}

.cr_top .ct_input {
  position: relative;
  height: 48px;
  width: 100%;
  margin-bottom: 16px;
}

.account-oprate .regist-btn {
  float: right;
  font-size: 14px;
  color: #67e8f9;
  text-decoration: none;
}

.account-oprate .regist-btn:hover {
  color: #bae6fd;
}

.messge {
  font-size: 12px;
  margin-top: 14px;
  height: 22px;
  text-align: left;
  color: #f87171;
}

.content_right .cr_top {
  position: relative;
  margin: 0;
}

.content_right .input_text {
  background: rgba(8, 18, 36, 0.86);
}

.account-oprate {
  width: 100%;
}

.ct_img_mm,
.ct-img-yhm {
  position: absolute;
  top: 16px;
  left: 14px;
  width: 16px;
  height: 16px;
  background-image: url("https://t4.chei.com.cn/passport/images/login2014/icon_input.png");
  opacity: 0.82;
  filter: invert(78%) sepia(37%) saturate(773%) hue-rotate(153deg) brightness(103%) contrast(93%);
}

.ct-img-yhm {
  background-position: -16px 0;
}

.input_text {
  display: inline-block;
  box-sizing: border-box;
  width: 100%;
  height: 48px;
  padding: 0 14px 0 42px;
  font-size: 14px;
  color: #e0f2fe;
  border: 1px solid rgba(56, 189, 248, 0.22);
  border-radius: 14px;
  vertical-align: middle;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.input_text::placeholder {
  color: #6f8baa;
}

.input_text:hover,
.input_text:focus {
  border-color: rgba(103, 232, 249, 0.72);
  background: rgba(8, 18, 36, 0.96);
  box-shadow: 0 0 0 4px rgba(34, 211, 238, 0.12), 0 0 20px rgba(56, 189, 248, 0.14);
  outline: 0;
}

.btn_login:hover {
  background: linear-gradient(135deg, #22d3ee 0%, #4f46e5 100%);
  transform: translateY(-1px);
  box-shadow: 0 0 26px rgba(56, 189, 248, 0.32), 0 16px 30px rgba(79, 70, 229, 0.24);
}

.btn_login {
  text-align: center;
  box-sizing: border-box;
  width: 100%;
  height: 46px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 14px;
  color: #06111f;
  border: 1px solid rgba(103, 232, 249, 0.68);
  background: linear-gradient(135deg, #67e8f9 0%, #38bdf8 45%, #6366f1 100%);
  margin-bottom: 16px;
  -webkit-appearance: none;
  transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
  font-weight: 800;
}

button,
input,
optgroup,
option,
select,
textarea {
  font-family: inherit;
  font-size: inherit;
  font-style: inherit;
  font-weight: inherit;
  resize: none;
}

blockquote,
body,
button,
code,
dd,
div,
dl,
dt,
fieldset,
form,
h1,
h2,
h3,
h4,
h5,
h6,
input,
legend,
li,
ol,
p,
pre,
td,
textarea,
th,
ul {
  margin: 0;
  padding: 0;
  font-family: '\5FAE\8F6F\96C5\9ED1', '\5B8B\4F53', Arial, Helvetica, sans-serif;
}

.theme-login-light#backgroud {
  background: radial-gradient(circle at 15% 18%, rgba(59, 130, 246, 0.14), transparent 26%), radial-gradient(circle at 82% 22%, rgba(14, 165, 233, 0.12), transparent 30%), linear-gradient(135deg, #f8fbff 0%, #eef4ff 48%, #eaf2ff 100%);
}

.theme-login-light .login-theme-switch {
  color: #1d4ed8;
  background: rgba(255, 255, 255, 0.9);
  border-color: #dbe5f3;
  box-shadow: 0 10px 22px rgba(37, 99, 235, 0.08);
}

.theme-login-light .login-theme-switch:hover {
  background: #eaf2ff;
  box-shadow: 0 14px 26px rgba(37, 99, 235, 0.12);
}

.theme-login-light .login-hero {
  color: #0f172a;
}

.theme-login-light .login-brand-mark {
  color: #ffffff;
  background: linear-gradient(135deg, #2563eb 0%, #38bdf8 100%);
  box-shadow: 0 18px 38px rgba(37, 99, 235, 0.24);
}

.theme-login-light .login-hero h1 {
  text-shadow: none;
}

.theme-login-light .login-hero p {
  color: #64748b;
}

.theme-login-light .content_right {
  background: rgba(255, 255, 255, 0.9);
  color: #334155;
  border-color: #dbe5f3;
  box-shadow: 0 24px 70px rgba(37, 99, 235, 0.14), inset 0 1px 0 rgba(255, 255, 255, 0.85);
}

.theme-login-light .login-body-title h2 {
  color: #0f172a;
}

.theme-login-light .login-body-title p,
.theme-login-light .account-oprate .regist-btn {
  color: #2563eb;
}

.theme-login-light .account-oprate .regist-btn:hover {
  color: #1d4ed8;
}

.theme-login-light .content_right .input_text {
  background: #ffffff;
}

.theme-login-light .input_text {
  color: #0f172a;
  border-color: #d8e1ef;
}

.theme-login-light .input_text::placeholder {
  color: #94a3b8;
}

.theme-login-light .input_text:hover,
.theme-login-light .input_text:focus {
  border-color: #60a5fa;
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
}

.theme-login-light .ct_img_mm,
.theme-login-light .ct-img-yhm {
  opacity: 0.72;
  filter: none;
}

.theme-login-light .btn_login {
  color: #ffffff;
  border-color: #2563eb;
  background: linear-gradient(135deg, #2563eb 0%, #38bdf8 100%);
}

.theme-login-light .btn_login:hover {
  background: linear-gradient(135deg, #1d4ed8 0%, #0ea5e9 100%);
  box-shadow: 0 16px 30px rgba(37, 99, 235, 0.22);
}
</style>
