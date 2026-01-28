<template>
  <div class="api-management-container">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="header-left">
        <h2>API 管理系统</h2>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-icon><User /></el-icon>
            {{ username }}
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <el-container class="main-container">
      <!-- 左侧菜单 -->
      <el-aside width="200px" class="sidebar">
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="all">
            <el-icon><Document /></el-icon>
            <span>全部接口</span>
          </el-menu-item>
          <el-menu-item index="user">
            <el-icon><User /></el-icon>
            <span>USER</span>
          </el-menu-item>
          <el-menu-item index="dashboard">
            <el-icon><Monitor /></el-icon>
            <span>Dashboard重构</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-main class="main-content">
        <!-- 搜索和操作栏 -->
        <div class="toolbar">
          <div class="toolbar-left">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索接口名称、路径..."
              style="width: 300px"
              clearable
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
          <div class="toolbar-right">
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              新建接口
            </el-button>
          </div>
        </div>

        <!-- 接口列表表格 -->
        <el-table
          :data="filteredApiList"
          style="width: 100%"
          v-loading="loading"
          stripe
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="接口名称" min-width="150" />
          <el-table-column prop="method" label="请求类型" width="120">
            <template #default="scope">
              <el-tag
                :type="getMethodType(scope.row.method)"
                size="small"
              >
                {{ scope.row.method }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="responsible" label="负责人" width="120" />
          <el-table-column prop="path" label="路径" min-width="200" />
          <el-table-column prop="version" label="版本" width="100" />
          <el-table-column prop="updateTime" label="更新时间" width="180" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag
                :type="scope.row.status === '启用' ? 'success' : 'info'"
                size="small"
              >
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <el-button
                link
                type="primary"
                size="small"
                @click="handleEdit(scope.row)"
              >
                编辑
              </el-button>
              <el-button
                link
                type="danger"
                size="small"
                @click="handleDelete(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User,
  ArrowDown,
  Document,
  Monitor,
  Search,
  Plus
} from '@element-plus/icons-vue'

export default {
  name: 'ApiManagement',
  components: {
    User,
    ArrowDown,
    Document,
    Monitor,
    Search,
    Plus
  },
  setup() {
    const router = useRouter()
    const username = ref(localStorage.getItem('username') || '用户')
    const activeMenu = ref('all')
    const searchKeyword = ref('')
    const loading = ref(false)
    const currentPage = ref(1)
    const pageSize = ref(20)
    const total = ref(0)

    // 模拟 API 数据
    const apiList = ref([
      {
        id: 1,
        name: '用户登录',
        method: 'POST',
        responsible: '张三',
        path: '/api/v1/user/login',
        version: 'v1.0',
        updateTime: '2024-01-15 10:30:00',
        status: '启用',
        category: 'user'
      },
      {
        id: 2,
        name: '获取用户信息',
        method: 'GET',
        responsible: '李四',
        path: '/api/v1/user/info',
        version: 'v1.0',
        updateTime: '2024-01-14 15:20:00',
        status: '启用',
        category: 'user'
      },
      {
        id: 3,
        name: 'Dashboard数据',
        method: 'GET',
        responsible: '王五',
        path: '/api/v1/dashboard/data',
        version: 'v2.0',
        updateTime: '2024-01-13 09:15:00',
        status: '启用',
        category: 'dashboard'
      },
      {
        id: 4,
        name: '更新用户',
        method: 'PUT',
        responsible: '张三',
        path: '/api/v1/user/update',
        version: 'v1.1',
        updateTime: '2024-01-12 14:45:00',
        status: '启用',
        category: 'user'
      },
      {
        id: 5,
        name: '删除用户',
        method: 'DELETE',
        responsible: '李四',
        path: '/api/v1/user/delete',
        version: 'v1.0',
        updateTime: '2024-01-11 11:30:00',
        status: '禁用',
        category: 'user'
      }
    ])

    // 过滤后的 API 列表
    const filteredApiList = computed(() => {
      let list = apiList.value

      // 按菜单分类过滤
      if (activeMenu.value !== 'all') {
        const categoryMap = {
          user: 'user',
          dashboard: 'dashboard'
        }
        list = list.filter(item => item.category === categoryMap[activeMenu.value])
      }

      // 按关键词搜索
      if (searchKeyword.value) {
        const keyword = searchKeyword.value.toLowerCase()
        list = list.filter(item =>
          item.name.toLowerCase().includes(keyword) ||
          item.path.toLowerCase().includes(keyword)
        )
      }

      total.value = list.length
      return list
    })

    // 获取请求方法的标签类型
    const getMethodType = (method) => {
      const typeMap = {
        GET: 'success',
        POST: 'primary',
        PUT: 'warning',
        DELETE: 'danger',
        PATCH: 'info'
      }
      return typeMap[method] || 'info'
    }

    // 菜单选择
    const handleMenuSelect = (index) => {
      activeMenu.value = index
      currentPage.value = 1
    }

    // 搜索
    const handleSearch = () => {
      currentPage.value = 1
    }

    // 添加接口
    const handleAdd = () => {
      ElMessage.info('新建接口功能待实现')
    }

    // 编辑接口
    const handleEdit = (row) => {
      ElMessage.info(`编辑接口: ${row.name}`)
    }

    // 删除接口
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `确定要删除接口 "${row.name}" 吗？`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        const index = apiList.value.findIndex(item => item.id === row.id)
        if (index > -1) {
          apiList.value.splice(index, 1)
          ElMessage.success('删除成功')
        }
      }).catch(() => {
        ElMessage.info('已取消删除')
      })
    }

    // 分页
    const handleSizeChange = (val) => {
      pageSize.value = val
      currentPage.value = 1
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
    }

    // 用户操作
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

    onMounted(() => {
      // 这里可以加载实际的 API 数据
      total.value = apiList.value.length
    })

    return {
      username,
      activeMenu,
      searchKeyword,
      loading,
      currentPage,
      pageSize,
      total,
      filteredApiList,
      getMethodType,
      handleMenuSelect,
      handleSearch,
      handleAdd,
      handleEdit,
      handleDelete,
      handleSizeChange,
      handleCurrentChange,
      handleCommand
    }
  }
}
</script>

<style scoped>
.api-management-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
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

.header-left h2 {
  margin: 0;
  font-size: 20px;
  color: #303133;
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

.main-container {
  flex: 1;
  overflow: hidden;
}

.sidebar {
  background: #fff;
  border-right: 1px solid #e4e7ed;
}

.sidebar-menu {
  border-right: none;
  height: 100%;
}

.main-content {
  padding: 20px;
  background: #f5f7fa;
  overflow-y: auto;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background: #fff;
  border-radius: 4px;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  padding: 15px;
  background: #fff;
  border-radius: 4px;
}

:deep(.el-table) {
  background: #fff;
}

:deep(.el-table th) {
  background: #fafafa;
}
</style>
