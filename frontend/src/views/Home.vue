<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">系统概览</h1>
      <p class="page-description">医疗陪诊Agent系统数据统计</p>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="info-card stat-card" shadow="hover">
          <el-icon :size="48" color="#409EFF"><User /></el-icon>
          <div class="stat-value" style="color: #409EFF;">1,234</div>
          <div class="stat-label">注册用户</div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="info-card stat-card" shadow="hover">
          <el-icon :size="48" color="#67C23A"><Calendar /></el-icon>
          <div class="stat-value" style="color: #67C23A;">567</div>
          <div class="stat-label">预约记录</div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="info-card stat-card" shadow="hover">
          <el-icon :size="48" color="#E6A23C"><Guide /></el-icon>
          <div class="stat-value" style="color: #E6A23C;">890</div>
          <div class="stat-label">就医指导</div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="info-card stat-card" shadow="hover">
          <el-icon :size="48" color="#F56C6C"><Medicine /></el-icon>
          <div class="stat-value" style="color: #F56C6C;">432</div>
          <div class="stat-label">用药指导</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 功能快捷入口 -->
    <el-row :gutter="20">
      <el-col :xs="24" :md="12">
        <el-card class="info-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>快捷功能</span>
            </div>
          </template>
          
          <div class="quick-actions">
            <el-button
              v-for="action in quickActions"
              :key="action.name"
              :type="action.type"
              :icon="action.icon"
              size="large"
              @click="handleQuickAction(action.path)"
              style="width: calc(50% - 8px); margin: 4px;"
            >
              {{ action.name }}
            </el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="12">
        <el-card class="info-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>系统信息</span>
            </div>
          </template>
          
          <el-descriptions :column="1" border>
            <el-descriptions-item label="系统名称">
              医疗陪诊Agent系统
            </el-descriptions-item>
            <el-descriptions-item label="系统版本">
              v1.0.0
            </el-descriptions-item>
            <el-descriptions-item label="API状态">
              <el-tag type="success">运行中</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="在线用户">
              123 人
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近活动 -->
    <el-card class="info-card" shadow="hover" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>最近活动</span>
          <el-button type="primary" link>查看全部</el-button>
        </div>
      </template>
      
      <el-timeline>
        <el-timeline-item
          v-for="(activity, index) in recentActivities"
          :key="index"
          :timestamp="activity.time"
          placement="top"
          :color="activity.color"
        >
          <el-card>
            <h4>{{ activity.title }}</h4>
            <p>{{ activity.description }}</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const quickActions = [
  { name: '用户管理', path: '/users', type: 'primary', icon: 'User' },
  { name: '预约挂号', path: '/appointments', type: 'success', icon: 'Calendar' },
  { name: '就医指导', path: '/guidance', type: 'warning', icon: 'Guide' },
  { name: '用药指导', path: '/medications', type: 'danger', icon: 'Medicine' }
]

const recentActivities = [
  {
    title: '新用户注册',
    description: '张三 刚刚注册了账号',
    time: '2025-10-20 19:30',
    color: '#409EFF'
  },
  {
    title: '预约成功',
    description: '李四 预约了心内科就诊',
    time: '2025-10-20 18:45',
    color: '#67C23A'
  },
  {
    title: '就医指导',
    description: '王五 获取了症状分析建议',
    time: '2025-10-20 17:20',
    color: '#E6A23C'
  },
  {
    title: '用药咨询',
    description: '赵六 查询了用药指导信息',
    time: '2025-10-20 16:00',
    color: '#F56C6C'
  }
]

const handleQuickAction = (path) => {
  router.push(path)
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  margin: -4px;
}

:deep(.el-timeline-item__wrapper) {
  padding-left: 20px;
}

:deep(.el-timeline-item__content) {
  margin-bottom: 20px;
}
</style>


