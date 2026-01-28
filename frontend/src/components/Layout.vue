<template>
  <div class="layout-container">
    <!-- 左侧菜单栏 -->
    <el-aside :width="isCollapse ? '64px' : '200px'" class="sidebar">
      <div class="sidebar-header">
        <h3 v-if="!isCollapse">API 管理系统</h3>
        <h3 v-else>A</h3>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :collapse-transition="false"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/home">
          <el-icon><House /></el-icon>
          <template #title>首页</template>
        </el-menu-item>
        <el-menu-item index="/api-test">
          <el-icon><Document /></el-icon>
          <template #title>接口测试</template>
        </el-menu-item>
      </el-menu>
      <div class="sidebar-footer">
        <el-button
          :icon="isCollapse ? Expand : Fold"
          circle
          @click="toggleCollapse"
        />
      </div>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="main-container">
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="header-left">
          <span class="project-selector">
            项目: Adtomic_API_线上
            <el-icon><ArrowDown /></el-icon>
          </span>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><User /></el-icon>
              {{ username }}
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 内容区域 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import {
  House,
  Document,
  User,
  ArrowDown,
  Fold,
  Expand
} from '@element-plus/icons-vue'

export default {
  name: 'Layout',
  components: {
    House,
    Document,
    User,
    ArrowDown,
    Fold,
    Expand
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const isCollapse = ref(false)
    const username = ref(localStorage.getItem('username') || '用户')

    const activeMenu = computed(() => {
      if (route.path.startsWith('/api-test')) {
        return '/api-test'
      }
      return route.path
    })

    const toggleCollapse = () => {
      isCollapse.value = !isCollapse.value
    }

    const handleCommand = (command) => {
      if (command === 'logout') {
        ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          localStorage.removeItem('token')
          localStorage.removeItem('username')
          router.push('/login')
        }).catch(() => {})
      }
    }

    return {
      isCollapse,
      activeMenu,
      username,
      toggleCollapse,
      handleCommand
    }
  }
}
</script>

<style scoped>
.layout-container {
  width: 100%;
  height: 100vh;
  display: flex;
}

.sidebar {
  background: #304156;
  transition: width 0.3s;
  display: flex;
  flex-direction: column;
  position: relative;
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  border-bottom: 1px solid #434a55;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.sidebar-menu {
  flex: 1;
  border-right: none;
  background: #304156;
}

:deep(.sidebar-menu .el-menu-item) {
  color: #bfcbd9;
}

:deep(.sidebar-menu .el-menu-item:hover) {
  background: #263445;
  color: #fff;
}

:deep(.sidebar-menu .el-menu-item.is-active) {
  background: #409eff;
  color: #fff;
}

:deep(.sidebar-menu .el-icon) {
  color: inherit;
}

.sidebar-footer {
  padding: 10px;
  border-top: 1px solid #434a55;
  display: flex;
  justify-content: center;
}

.sidebar-footer .el-button {
  border: none;
  background: transparent;
  color: #bfcbd9;
}

.sidebar-footer .el-button:hover {
  background: #263445;
  color: #fff;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header-left {
  display: flex;
  align-items: center;
}

.project-selector {
  display: flex;
  align-items: center;
  color: #606266;
  cursor: pointer;
  font-size: 14px;
}

.project-selector .el-icon {
  margin-left: 5px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #606266;
}

.user-info .el-icon {
  margin-right: 5px;
}

.main-content {
  padding: 0;
  background: #f5f7fa;
  overflow-y: auto;
}
</style>
