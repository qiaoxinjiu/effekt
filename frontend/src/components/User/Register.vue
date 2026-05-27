<template>
  <div id="backgroud" :class="themeClass">
    <button class="register-theme-switch" type="button" @click="toggleTheme">
      <i :class="themeIcon"></i>
      <span>{{ themeLabel }}</span>
    </button>
    <div class="register-hero">
      <div class="register-brand-mark">效</div>
      <h1>效能平台</h1>
      <p>创建账号后即可进入统一测试协作、用例管理与质量工作台。</p>
      <div class="register-feature-list">
        <span>测试协作</span>
        <span>用例管理</span>
        <span>质量工作台</span>
      </div>
    </div>
    <div class="model">
      <div class="location-title">
        <span class="register-card-kicker">Create Account</span>
        <h1>创建账号</h1>
        <p>注册后开启你的质量效能工作区</p>
      </div>

      <el-form ref="ruleForm" :model="ruleForm" status-icon :rules="rules" label-position="top" class="demo-ruleForm">
        <el-form-item label="用户名" prop="username">
          <el-input v-model.trim="ruleForm.username" type="text" placeholder="用户名" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="ruleForm.password" type="password" placeholder="密码" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input v-model="ruleForm.checkPass" type="password" placeholder="确认密码" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="mobile">
          <el-input v-model.trim="ruleForm.mobile" placeholder="手机号" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model.trim="ruleForm.email" type="text" placeholder="邮箱" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item class="register-actions">
          <el-button class="enter-btn" type="primary" :disabled="!select" @click="submitForm('ruleForm')">
            立即注册
          </el-button>
          <el-button class="login-link-btn" type="text" @click="goLogin">去登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { Register } from '@/api/Userapi'

export default {
  name: 'Register',
  data() {
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
        return
      }
      if (this.ruleForm.password !== '') {
        this.$refs.ruleForm.validateField('checkPass')
      }
      callback()
    }
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.ruleForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    const validateUsername = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入用户名'))
        return
      }
      callback()
    }

    return {
      select: true,
      ruleForm: {
        username: '',
        password: '',
        checkPass: '',
        mobile: '',
        email: ''
      },
      rules: {
        username: [{ required: true, validator: validateUsername, trigger: 'blur' }],
        password: [{ required: true, validator: validatePass, trigger: 'blur' }],
        checkPass: [{ required: true, validator: validatePass2, trigger: 'blur' }]
      },
      uiTheme: localStorage.getItem('uiTheme') || 'dark'
    }
  },
  computed: {
    themeClass() {
      return this.uiTheme === 'light' ? 'theme-register-light' : 'theme-register-dark'
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
    open(message) {
      this.$alert(message, '提示', {
        confirmButtonText: '确定'
      })
    },
    handleRegister() {
      Register({
        username: this.ruleForm.username,
        password: this.ruleForm.password,
        mobile: this.ruleForm.mobile,
        email: this.ruleForm.email,
        createdBy: 1
      }).then(data => {
        if (data && data.id) {
          this.open('注册成功')
          this.$router.push({ name: 'login' })
        } else {
          this.open(data.message || '注册失败')
        }
      })
    },
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.handleRegister()
        }
      })
    },
    goLogin() {
      this.$router.push({ name: 'login' })
    }
  }
}
</script>

<style scoped>
#backgroud {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 72px;
  width: 100vw;
  min-height: 100vh;
  padding: 72px 48px;
  overflow: auto;
  box-sizing: border-box;
}

#backgroud.theme-register-dark {
  background: radial-gradient(circle at 15% 18%, rgba(34, 211, 238, 0.22), transparent 26%), radial-gradient(circle at 82% 22%, rgba(99, 102, 241, 0.24), transparent 30%), linear-gradient(135deg, #050914 0%, #08111f 46%, #0f172a 100%);
}

#backgroud.theme-register-light {
  background: radial-gradient(circle at 14% 18%, rgba(59, 130, 246, 0.14), transparent 28%), radial-gradient(circle at 84% 18%, rgba(14, 165, 233, 0.16), transparent 30%), linear-gradient(135deg, #f8fbff 0%, #eef6ff 48%, #eaf2ff 100%);
}

.register-hero {
  flex: 0 0 420px;
  max-width: 420px;
  color: #f8fbff;
}

.register-brand-mark {
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

.register-hero h1 {
  margin: 24px 0 14px;
  font-size: 42px;
  line-height: 1.15;
  letter-spacing: 1px;
  text-shadow: 0 0 26px rgba(103, 232, 249, 0.22);
}

.register-hero p {
  margin: 0;
  color: #9fb8d4;
  font-size: 16px;
  line-height: 1.8;
}

.register-feature-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 28px;
}

.register-feature-list span {
  display: inline-flex;
  align-items: center;
  height: 32px;
  padding: 0 14px;
  border-radius: 999px;
  color: #bae6fd;
  background: rgba(56, 189, 248, 0.12);
  border: 1px solid rgba(56, 189, 248, 0.22);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06);
}

.register-theme-switch {
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

.register-theme-switch:hover {
  background: rgba(14, 165, 233, 0.18);
  box-shadow: 0 0 18px rgba(56, 189, 248, 0.18);
  transform: translateY(-1px);
}

.model {
  position: relative;
  flex: 0 0 420px;
  width: 420px;
  min-height: auto;
  height: auto;
  margin: 0;
  padding: 34px 36px 30px;
  border-radius: 24px;
  text-align: left;
  background: rgba(15, 23, 42, 0.82);
  color: #dbeafe;
  border: 1px solid rgba(56, 189, 248, 0.22);
  box-shadow: 0 0 42px rgba(56, 189, 248, 0.12), 0 30px 90px rgba(0, 0, 0, 0.42), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(18px);
}

.location-title {
  text-align: center;
  margin-bottom: 22px;
}

.register-card-kicker {
  display: inline-flex;
  margin-bottom: 10px;
  color: #67e8f9;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.6px;
  text-transform: uppercase;
}

.location-title h1 {
  margin: 0 0 8px;
  font-size: 28px;
  color: #e0f2fe;
}

.location-title p {
  margin: 0;
  color: #9fb8d4;
  font-size: 13px;
  letter-spacing: 0.4px;
}

.register-head {
  position: absolute;
}

.demo-ruleForm {
  width: 100%;
}

.demo-ruleForm >>> .el-form-item {
  margin-bottom: 15px;
}

.el-input {
  float: none;
  width: 100%;
}

.model >>> .el-form-item__label {
  padding: 0 0 7px;
  color: #cbd5e1;
  line-height: 1.2;
  font-size: 13px;
  font-weight: 700;
}

.model >>> .el-input__inner {
  height: 44px;
  background: rgba(8, 18, 36, 0.86);
  border-color: rgba(56, 189, 248, 0.22);
  color: #f8fafc;
  border-radius: 14px;
}

.model >>> .el-input__inner:hover,
.model >>> .el-input__inner:focus {
  border-color: #38bdf8;
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.12);
}

.register-actions {
  margin-top: 4px;
  margin-bottom: 0 !important;
}

.register-actions >>> .el-form-item__content {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  margin-left: 0 !important;
}

.enter-btn {
  width: 100%;
  height: 46px;
  border: 1px solid rgba(103, 232, 249, 0.68);
  border-radius: 14px;
  color: #06111f;
  font-weight: 800;
  background: linear-gradient(135deg, #67e8f9 0%, #38bdf8 45%, #6366f1 100%);
  box-shadow: 0 16px 34px rgba(59, 130, 246, 0.25);
  transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}

.enter-btn:hover {
  background: linear-gradient(135deg, #22d3ee 0%, #4f46e5 100%);
  transform: translateY(-1px);
  box-shadow: 0 0 26px rgba(56, 189, 248, 0.32), 0 16px 30px rgba(79, 70, 229, 0.24);
}

.login-link-btn {
  align-self: flex-end;
  padding-right: 0;
  margin-top: 10px;
  color: #67e8f9;
}

.theme-register-light .register-hero {
  color: #10233f;
}

.theme-register-light .register-brand-mark {
  color: #ffffff;
  background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%);
  box-shadow: 0 20px 48px rgba(37, 99, 235, 0.2);
}

.theme-register-light .register-hero h1 {
  color: #0f172a;
  text-shadow: none;
}

.theme-register-light .register-hero p {
  color: #475569;
}

.theme-register-light .register-feature-list span {
  color: #1d4ed8;
  background: rgba(37, 99, 235, 0.08);
  border-color: rgba(37, 99, 235, 0.16);
  box-shadow: none;
}

.theme-register-light .register-theme-switch {
  color: #1d4ed8;
  background: rgba(255, 255, 255, 0.86);
  border-color: rgba(37, 99, 235, 0.18);
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
}

.theme-register-light .register-theme-switch:hover {
  background: #eff6ff;
  box-shadow: 0 16px 34px rgba(37, 99, 235, 0.14);
}

.theme-register-light .model {
  background: rgba(255, 255, 255, 0.94);
  color: #1e293b;
  border-color: rgba(37, 99, 235, 0.14);
  box-shadow: 0 28px 70px rgba(37, 99, 235, 0.14);
}

.theme-register-light .register-card-kicker {
  color: #2563eb;
}

.theme-register-light .location-title h1 {
  color: #0f172a;
}

.theme-register-light .location-title p {
  color: #64748b;
}

.theme-register-light .model >>> .el-form-item__label {
  color: #334155;
}

.theme-register-light .model >>> .el-input__inner {
  background: #ffffff;
  border-color: #dbe7f6;
  color: #0f172a;
}

.theme-register-light .model >>> .el-input__inner:hover,
.theme-register-light .model >>> .el-input__inner:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.theme-register-light .enter-btn {
  color: #ffffff;
  border-color: #2563eb;
  background: linear-gradient(135deg, #2563eb 0%, #38bdf8 100%);
}

.theme-register-light .enter-btn:hover {
  background: linear-gradient(135deg, #1d4ed8 0%, #0ea5e9 100%);
  box-shadow: 0 16px 30px rgba(37, 99, 235, 0.22);
}

.theme-register-light .login-link-btn {
  color: #2563eb;
}

@media (max-width: 1080px) {
  #backgroud {
    gap: 40px;
    padding: 72px 28px 36px;
  }

  .register-hero {
    flex-basis: 360px;
    max-width: 360px;
  }
}

@media (max-width: 920px) {
  #backgroud {
    flex-direction: column;
    gap: 28px;
    padding: 80px 18px 28px;
  }

  .register-hero,
  .model {
    flex: none;
    width: 100%;
    max-width: 430px;
  }

  .register-hero {
    text-align: center;
  }

  .register-brand-mark,
  .register-feature-list {
    margin-left: auto;
    margin-right: auto;
    justify-content: center;
  }
}
</style>
