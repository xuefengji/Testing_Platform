<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>API 管理系统</h2>
        <p>欢迎登录</p>
      </div>
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入邮箱或用户名"
            size="large"
            clearable
          >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            show-password
            clearable
            @keyup.enter="handleLogin"
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <div class="login-options">
            <el-checkbox v-model="loginForm.remember">记住密码</el-checkbox>
            <el-link type="primary" :underline="false">忘记密码？</el-link>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { login } from '../api'

export default {
  name: 'Login',
  components: {
    User,
    Lock
  },
  setup() {
    const router = useRouter()
    const loginFormRef = ref(null)
    const loading = ref(false)
    
    const loginForm = reactive({
      username: '',
      password: '',
      remember: false
    })

    const loginRules = {
      username: [
        { required: true, message: '请输入邮箱或用户名', trigger: 'blur' },
        { min: 3, message: '长度不能少于3位', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
      ]
    }

    // 加载记住的密码
    onMounted(() => {
      const savedUsername = localStorage.getItem('saved_username')
      const savedPassword = localStorage.getItem('saved_password')
      if (savedUsername) {
        loginForm.username = savedUsername
        loginForm.remember = true
      }
      if (savedPassword && loginForm.remember) {
        loginForm.password = savedPassword
      }
    })

    const handleLogin = async () => {
      if (!loginFormRef.value) return
      
      await loginFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            // 调用登录 API
            // 后端支持通过邮箱或用户名登录
            // 如果输入的是邮箱格式，直接使用；否则作为用户名处理
            const identifier = loginForm.username.trim()
            
            const response = await login({
              name: identifier,
              password: loginForm.password
            })
            
            // 后端实际返回 TokenOut 对象：{ access_token, refresh_token, token_type }
            // 如果后端使用了 ApiResponse 包装，响应拦截器会提取 data 字段
            // 所以这里兼容两种格式：直接返回 TokenOut 或包装在 ApiResponse 中
            const tokenData = response.data || response
            
            // 保存 token 和用户信息
            if (tokenData.access_token) {
              const token = tokenData.access_token
              localStorage.setItem('token', token)
              if (tokenData.refresh_token) {
                localStorage.setItem('refresh_token', tokenData.refresh_token)
              }
              localStorage.setItem('username', loginForm.username)
              
              // 如果选择记住密码，保存用户名和密码
              if (loginForm.remember) {
                localStorage.setItem('saved_username', loginForm.username)
                localStorage.setItem('saved_password', loginForm.password)
              } else {
                localStorage.removeItem('saved_username')
                localStorage.removeItem('saved_password')
              }
              
              ElMessage.success('登录成功')
              router.push('/api-test')
            } else {
              ElMessage.error('登录失败：未获取到访问令牌')
            }
          } catch (error) {
            console.error('Login error:', error)
            // 显示具体的错误信息（后端统一返回格式，错误信息在 error.message 中）
            const errorMessage = error.message || '登录失败，请检查用户名和密码'
            ElMessage.error(errorMessage)
            
            // 开发环境下的模拟登录（仅当后端完全不可用时）
            if (import.meta.env.DEV && error.code === 'ECONNREFUSED') {
              console.warn('Backend not available, using mock login')
              if (loginForm.username && loginForm.password) {
                localStorage.setItem('token', 'mock-token-' + Date.now())
                localStorage.setItem('username', loginForm.username)
                
                if (loginForm.remember) {
                  localStorage.setItem('saved_username', loginForm.username)
                  localStorage.setItem('saved_password', loginForm.password)
                }
                
                ElMessage.warning('后端服务不可用，使用模拟登录')
                router.push('/api-test')
              }
            }
          } finally {
            loading.value = false
          }
        }
      })
    }

    return {
      loginFormRef,
      loginForm,
      loginRules,
      loading,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-box {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 10px;
}

.login-header p {
  color: #666;
  font-size: 14px;
}

.login-form {
  margin-top: 30px;
}

.login-options {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.login-button {
  width: 100%;
  margin-top: 10px;
  height: 45px;
  font-size: 16px;
}

:deep(.el-input__wrapper) {
  padding: 12px 15px;
}

:deep(.el-checkbox) {
  color: #606266;
}
</style>
