<template>
  <div class="home-container">
    <el-card class="welcome-card">
      <h1>欢迎使用 API 管理系统</h1>
      <p>这是一个功能强大的 API 测试和管理平台</p>
    </el-card>
    
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value">0</div>
            <div class="stat-label">接口总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value">0</div>
            <div class="stat-label">测试用例</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value">0</div>
            <div class="stat-label">测试报告</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value">0%</div>
            <div class="stat-label">通过率</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
  text-align: center;
}

.welcome-card h1 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 28px;
}

.welcome-card p {
  margin: 0;
  color: #606266;
  font-size: 16px;
}

.stats-row {
  margin-top: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 20px;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}
</style>
