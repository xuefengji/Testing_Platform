<template>
  <div class="api-definition-container">
    <div class="content-wrapper">
      <!-- 左侧菜单 -->
      <el-aside width="200px" class="left-sidebar">
        <div class="search-box">
          <el-input
            v-model="searchModule"
            placeholder="搜索模块"
            size="small"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="module-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="recycle">
            <el-icon><Delete /></el-icon>
            <span>回收站 (25)</span>
          </el-menu-item>
          <el-sub-menu index="all">
            <template #title>
              <div class="menu-item-wrapper" @mouseenter="hoveredItem = 'all'" @mouseleave="hoveredItem = null">
                <el-icon><Document /></el-icon>
                <span>全部接口 (578)</span>
                <div class="menu-actions" v-show="hoveredItem === 'all'">
                  <el-icon class="action-icon" @click.stop="handleAddFolder('all')" title="添加文件夹">
                    <Plus />
                  </el-icon>
                </div>
              </div>
            </template>
            <el-menu-item index="unplanned">未规划接口 (0)</el-menu-item>
            <el-sub-menu index="user">
              <template #title>
                <div class="menu-item-wrapper" @mouseenter="hoveredItem = 'user'" @mouseleave="hoveredItem = null">
                  <span>USER (1)</span>
                  <div class="menu-actions" v-show="hoveredItem === 'user'">
                    <el-icon class="action-icon" @click.stop="handleEditFolder('user')" title="编辑">
                      <Edit />
                    </el-icon>
                    <el-icon class="action-icon" @click.stop="handleDeleteFolder('user')" title="删除">
                      <Delete />
                    </el-icon>
                    <el-icon class="action-icon" @click.stop="handleAddFolder('user')" title="新增">
                      <Plus />
                    </el-icon>
                  </div>
                </div>
              </template>
              <el-menu-item index="login">登录 (1)</el-menu-item>
            </el-sub-menu>
            <el-sub-menu index="dashboard">
              <template #title>
                <div class="menu-item-wrapper" @mouseenter="hoveredItem = 'dashboard'" @mouseleave="hoveredItem = null">
                  <span>Dashboard重构 (73)</span>
                  <div class="menu-actions" v-show="hoveredItem === 'dashboard'">
                    <el-icon class="action-icon" @click.stop="handleEditFolder('dashboard')" title="编辑">
                      <Edit />
                    </el-icon>
                    <el-icon class="action-icon" @click.stop="handleDeleteFolder('dashboard')" title="删除">
                      <Delete />
                    </el-icon>
                    <el-icon class="action-icon" @click.stop="handleAddFolder('dashboard')" title="新增">
                      <Plus />
                    </el-icon>
                  </div>
                </div>
              </template>
              <el-menu-item index="dashboard-item">Dashboard 子项</el-menu-item>
            </el-sub-menu>
            <el-sub-menu index="h10ads">
              <template #title>
                <div class="menu-item-wrapper" @mouseenter="hoveredItem = 'h10ads'" @mouseleave="hoveredItem = null">
                  <span>H10ads (229)</span>
                  <div class="menu-actions" v-show="hoveredItem === 'h10ads'">
                    <el-icon class="action-icon" @click.stop="handleEditFolder('h10ads')" title="编辑">
                      <Edit />
                    </el-icon>
                    <el-icon class="action-icon" @click.stop="handleDeleteFolder('h10ads')" title="删除">
                      <Delete />
                    </el-icon>
                    <el-icon class="action-icon" @click.stop="handleAddFolder('h10ads')" title="新增">
                      <Plus />
                    </el-icon>
                  </div>
                </div>
              </template>
              <el-menu-item index="h10ads-item">H10ads 子项</el-menu-item>
            </el-sub-menu>
          </el-sub-menu>
          <el-menu-item index="refunds">
            <el-icon><Money /></el-icon>
            <span>Refunds Genie (1)</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-main class="main-content">
        <!-- 工具栏 -->
        <div class="toolbar">
          <div class="toolbar-left">
            <h3>接口列表</h3>
            <el-button type="primary" size="small">
              <el-icon><Plus /></el-icon>
              新建
            </el-button>
            <el-button size="small">更多操作</el-button>
          </div>
          <div class="toolbar-right">
            <el-radio-group v-model="viewType" size="small">
              <el-radio-button label="api">API</el-radio-button>
              <el-radio-button label="case">CASE</el-radio-button>
              <el-radio-button label="doc">文档</el-radio-button>
            </el-radio-group>
            <el-select v-model="version" size="small" style="width: 150px; margin-left: 10px">
              <el-option label="默认最新版本" value="latest" />
            </el-select>
            <el-input
              v-model="searchKeyword"
              placeholder="根据ID/名称/标签/路径 搜索"
              size="small"
              style="width: 250px; margin-left: 10px"
              clearable
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-button size="small" style="margin-left: 10px">高级搜索</el-button>
          </div>
        </div>

        <!-- 接口列表表格 -->
        <el-table
          :data="apiList"
          style="width: 100%"
          v-loading="loading"
          stripe
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
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
          <el-table-column prop="responsible" label="责任人" width="120" />
          <el-table-column prop="path" label="路径" min-width="200" />
          <el-table-column prop="tags" label="标签" width="100" />
          <el-table-column prop="version" label="版本" width="100" />
          <el-table-column prop="updateTime" label="更新时间" width="180" />
          <el-table-column prop="caseCount" label="用例数" width="100" />
          <el-table-column prop="caseResult" label="用例执行结果" width="120" />
          <el-table-column prop="passRate" label="用例通过率" width="120" />
          <el-table-column prop="status" label="接口状态" width="120">
            <template #default="scope">
              <el-tag
                :type="getStatusType(scope.row.status)"
                size="small"
              >
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <el-button link type="primary" size="small" @click="handleRun(scope.row)">
                <el-icon><VideoPlay /></el-icon>
              </el-button>
              <el-button link type="primary" size="small" @click="handleEdit(scope.row)">
                <el-icon><Edit /></el-icon>
              </el-button>
              <el-button link type="danger" size="small" @click="handleDelete(scope.row)">
                <el-icon><Delete /></el-icon>
              </el-button>
              <el-button link type="primary" size="small" @click="handleCopy(scope.row)">
                <el-icon><CopyDocument /></el-icon>
              </el-button>
              <el-dropdown @command="(cmd) => handleMore(scope.row, cmd)">
                <el-button link type="primary" size="small">
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="export">导出</el-dropdown-item>
                    <el-dropdown-item command="history">历史版本</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
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
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search,
  Delete,
  Document,
  Money,
  Plus,
  VideoPlay,
  Edit,
  CopyDocument,
  MoreFilled
} from '@element-plus/icons-vue'

export default {
  name: 'ApiDefinition',
  components: {
    Search,
    Delete,
    Document,
    Money,
    Plus,
    VideoPlay,
    Edit,
    CopyDocument,
    MoreFilled
  },
  setup() {
    const searchModule = ref('')
    const activeMenu = ref('all')
    const viewType = ref('api')
    const version = ref('latest')
    const searchKeyword = ref('')
    const loading = ref(false)
    const currentPage = ref(1)
    const pageSize = ref(20)
    const total = ref(0)
    const selectedRows = ref([])
    const hoveredItem = ref(null) // 当前悬停的菜单项

    // 模拟数据
    const apiList = ref([
      {
        id: 100603,
        name: '/v2/profit-and...',
        method: 'POST',
        responsible: 'gaoshi',
        path: '/profits/tiktok/dashboard/v2/profit-and-loss',
        tags: '',
        version: 'v1.0.0',
        updateTime: '2026-01-27 13:4...',
        caseCount: 0,
        caseResult: '',
        passRate: '',
        status: '已完成'
      },
      {
        id: 100602,
        name: '/profit-and-los...',
        method: 'GET',
        responsible: '纪雪凤',
        path: '/profits/tiktok/dashboard/profit-and-loss',
        tags: '',
        version: 'v1.0.0',
        updateTime: '2026-01-26 14:4...',
        caseCount: 0,
        caseResult: '',
        passRate: '',
        status: '进行中'
      },
      {
        id: 100601,
        name: 'asin/data',
        method: 'GET',
        responsible: 'gaoshi',
        path: '/api/asin/data',
        tags: '',
        version: 'v1.0.0',
        updateTime: '2026-01-25 10:3...',
        caseCount: 0,
        caseResult: '',
        passRate: '',
        status: '已完成'
      }
    ])

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

    const getStatusType = (status) => {
      if (status === '已完成') return 'success'
      if (status === '进行中') return 'warning'
      return 'info'
    }

    const handleMenuSelect = (index) => {
      activeMenu.value = index
    }

    const handleSelectionChange = (selection) => {
      selectedRows.value = selection
    }

    const handleRun = (row) => {
      ElMessage.info(`运行接口: ${row.name}`)
    }

    const handleEdit = (row) => {
      ElMessage.info(`编辑接口: ${row.name}`)
    }

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
        ElMessage.success('删除成功')
      }).catch(() => {})
    }

    const handleCopy = (row) => {
      ElMessage.success(`已复制接口: ${row.name}`)
    }

    const handleMore = (row, command) => {
      ElMessage.info(`${command}: ${row.name}`)
    }

    const handleSizeChange = (val) => {
      pageSize.value = val
      currentPage.value = 1
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
    }

    // 处理文件夹操作
    const handleAddFolder = (folderId) => {
      ElMessageBox.prompt('请输入文件夹名称', '新增文件夹', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /.+/,
        inputErrorMessage: '文件夹名称不能为空'
      }).then(({ value }) => {
        ElMessage.success(`已添加文件夹: ${value}`)
      }).catch(() => {})
    }

    const handleEditFolder = (folderId) => {
      const folderNames = {
        user: 'USER',
        dashboard: 'Dashboard重构',
        h10ads: 'H10ads'
      }
      ElMessageBox.prompt('请输入新的文件夹名称', '编辑文件夹', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputValue: folderNames[folderId] || '',
        inputPattern: /.+/,
        inputErrorMessage: '文件夹名称不能为空'
      }).then(({ value }) => {
        ElMessage.success(`已更新文件夹名称: ${value}`)
      }).catch(() => {})
    }

    const handleDeleteFolder = (folderId) => {
      const folderNames = {
        user: 'USER',
        dashboard: 'Dashboard重构',
        h10ads: 'H10ads'
      }
      ElMessageBox.confirm(
        `确定要删除文件夹 "${folderNames[folderId] || folderId}" 吗？`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        ElMessage.success('删除成功')
      }).catch(() => {})
    }

    return {
      searchModule,
      activeMenu,
      viewType,
      version,
      searchKeyword,
      loading,
      currentPage,
      pageSize,
      total,
      apiList,
      getMethodType,
      getStatusType,
      handleMenuSelect,
      handleSelectionChange,
      handleRun,
      handleEdit,
      handleDelete,
      handleCopy,
      handleMore,
      handleSizeChange,
      handleCurrentChange,
      hoveredItem,
      handleAddFolder,
      handleEditFolder,
      handleDeleteFolder
    }
  }
}
</script>

<style scoped>
.api-definition-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
}

.content-wrapper {
  display: flex;
  height: 100%;
}

.left-sidebar {
  background: #fff;
  border-right: 1px solid #e4e7ed;
  padding: 10px;
}

.search-box {
  margin-bottom: 10px;
}

.module-menu {
  border-right: none;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #e4e7ed;
  background: #fff;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.toolbar-left h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.toolbar-right {
  display: flex;
  align-items: center;
}

.main-content {
  flex: 1;
  padding: 0;
  overflow-y: auto;
}

.pagination {
  padding: 15px 20px;
  background: #fff;
  border-top: 1px solid #e4e7ed;
  display: flex;
  justify-content: flex-end;
}

:deep(.el-table) {
  background: #fff;
}

/* 菜单项包装器样式 */
.menu-item-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  position: relative;
}

.menu-item-wrapper .el-icon {
  margin-right: 8px;
}

.menu-item-wrapper span {
  flex: 1;
}

/* 操作图标容器 */
.menu-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
  padding-right: 8px;
}

.action-icon {
  cursor: pointer;
  font-size: 14px;
  color: #409eff;
  transition: color 0.3s;
}

.action-icon:hover {
  color: #66b1ff;
}

.action-icon:active {
  color: #3a8ee6;
}

/* 确保菜单项有足够的空间显示操作图标 */
:deep(.el-sub-menu__title) {
  padding-right: 40px !important;
}

:deep(.el-menu-item) {
  padding-right: 20px !important;
}
</style>
