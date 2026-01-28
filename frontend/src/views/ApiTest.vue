<template>
  <div class="api-test-container">
    <!-- Tab 导航栏 -->
    <div class="tab-nav">
      <div
        v-for="tab in tabs"
        :key="tab.key"
        :class="['tab-item', { active: activeTab === tab.key }]"
        @click="handleTabClick(tab.key)"
      >
        {{ tab.label }}
      </div>
    </div>

    <!-- Tab 内容区 -->
    <div class="tab-content">
      <component :is="currentComponent" />
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import ApiDefinition from './api-test/ApiDefinition.vue'
import ApiAutomation from './api-test/ApiAutomation.vue'
import TestReport from './api-test/TestReport.vue'
import HomeTab from './api-test/HomeTab.vue'

export default {
  name: 'ApiTest',
  components: {
    ApiDefinition,
    ApiAutomation,
    TestReport,
    HomeTab
  },
  setup() {
    const activeTab = ref('home')

    const componentMap = {
      home: HomeTab,
      definition: ApiDefinition,
      automation: ApiAutomation,
      report: TestReport
    }

    const tabs = [
      { key: 'home', label: '首页' },
      { key: 'definition', label: '接口定义' },
      { key: 'automation', label: '接口自动化' },
      { key: 'report', label: '测试报告' }
    ]

    const currentComponent = computed(() => {
      return componentMap[activeTab.value] || HomeTab
    })

    const handleTabClick = (key) => {
      activeTab.value = key
    }

    return {
      activeTab,
      tabs,
      currentComponent,
      handleTabClick
    }
  }
}
</script>

<style scoped>
.api-test-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
}

.tab-nav {
  display: flex;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 20px;
}

.tab-item {
  padding: 15px 25px;
  cursor: pointer;
  color: #606266;
  font-size: 14px;
  position: relative;
  transition: all 0.3s;
  border-bottom: 2px solid transparent;
}

.tab-item:hover {
  color: #409eff;
}

.tab-item.active {
  color: #409eff;
  border-bottom-color: #409eff;
  font-weight: 500;
}

.tab-content {
  flex: 1;
  overflow-y: auto;
  background: #f5f7fa;
}
</style>
