<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">预约挂号</h1>
      <p class="page-description">智能预约挂号与管理</p>
    </div>

    <el-row :gutter="20">
      <!-- 智能预约 -->
      <el-col :xs="24" :md="10">
        <el-card class="info-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><MagicStick /></el-icon>
              <span style="margin-left: 8px;">智能预约推荐</span>
            </div>
          </template>
          
          <el-form
            ref="recommendFormRef"
            :model="recommendForm"
            label-width="100px"
          >
            <el-form-item label="用户" prop="user_id">
              <el-select v-model="recommendForm.user_id" placeholder="选择用户" style="width: 100%;">
                <el-option label="张三" :value="1" />
                <el-option label="李四" :value="2" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="症状描述" prop="symptoms">
              <el-input
                v-model="recommendForm.symptoms"
                type="textarea"
                :rows="4"
                placeholder="请详细描述症状，AI将为您推荐合适的科室和医生"
              />
            </el-form-item>
            
            <el-form-item label="偏好医院" prop="hospital">
              <el-input v-model="recommendForm.hospital" placeholder="如：协和医院" />
            </el-form-item>
            
            <el-form-item label="优先级" prop="priority">
              <el-radio-group v-model="recommendForm.priority">
                <el-radio label="urgent">紧急</el-radio>
                <el-radio label="normal">普通</el-radio>
                <el-radio label="low">不急</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                :icon="Search"
                :loading="recommendLoading"
                @click="getRecommendation"
                style="width: 100%;"
              >
                获取AI推荐
              </el-button>
            </el-form-item>
          </el-form>

          <!-- 推荐结果 -->
          <el-alert
            v-if="recommendation"
            type="success"
            :closable="false"
            style="margin-top: 20px;"
          >
            <template #title>
              <div style="font-weight: 600;">AI推荐结果</div>
            </template>
            <div style="margin-top: 12px; line-height: 1.8;">
              <p><strong>推荐科室：</strong>{{ recommendation.department }}</p>
              <p><strong>推荐时间：</strong>{{ recommendation.time }}</p>
              <p><strong>建议事项：</strong>{{ recommendation.advice }}</p>
            </div>
          </el-alert>
        </el-card>
      </el-col>

      <!-- 预约列表 -->
      <el-col :xs="24" :md="14">
        <el-card class="info-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>预约记录</span>
              <el-button type="primary" :icon="Plus" @click="handleAddAppointment">
                新增预约
              </el-button>
            </div>
          </template>
          
          <el-table
            :data="appointments"
            v-loading="loading"
            stripe
          >
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="patient_name" label="患者" width="100" />
            <el-table-column prop="department" label="科室" width="120" />
            <el-table-column prop="doctor" label="医生" width="100" />
            <el-table-column prop="appointment_time" label="预约时间" width="160" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  link
                  :icon="View"
                  @click="handleViewAppointment(row)"
                >
                  详情
                </el-button>
                <el-button
                  v-if="row.status === '待就诊'"
                  type="danger"
                  link
                  :icon="Close"
                  @click="handleCancelAppointment(row)"
                >
                  取消
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <div style="margin-top: 20px; display: flex; justify-content: flex-end;">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50]"
              :total="total"
              layout="total, sizes, prev, pager, next"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 预约详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="预约详情"
      width="600px"
    >
      <el-descriptions :column="2" border v-if="currentAppointment">
        <el-descriptions-item label="预约ID">
          {{ currentAppointment.id }}
        </el-descriptions-item>
        <el-descriptions-item label="患者姓名">
          {{ currentAppointment.patient_name }}
        </el-descriptions-item>
        <el-descriptions-item label="科室">
          {{ currentAppointment.department }}
        </el-descriptions-item>
        <el-descriptions-item label="医生">
          {{ currentAppointment.doctor }}
        </el-descriptions-item>
        <el-descriptions-item label="预约时间" :span="2">
          {{ currentAppointment.appointment_time }}
        </el-descriptions-item>
        <el-descriptions-item label="症状描述" :span="2">
          {{ currentAppointment.symptoms }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentAppointment.status)">
            {{ currentAppointment.status }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, View, Close, MagicStick } from '@element-plus/icons-vue'

const loading = ref(false)
const recommendLoading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const appointments = ref([])
const recommendation = ref(null)
const detailDialogVisible = ref(false)
const currentAppointment = ref(null)

const recommendForm = reactive({
  user_id: null,
  symptoms: '',
  hospital: '',
  priority: 'normal'
})

// 模拟数据
const loadAppointments = () => {
  loading.value = true
  setTimeout(() => {
    appointments.value = [
      {
        id: 1,
        patient_name: '张三',
        department: '心内科',
        doctor: '李医生',
        appointment_time: '2025-10-21 09:00',
        status: '待就诊',
        symptoms: '胸闷、气短'
      },
      {
        id: 2,
        patient_name: '李四',
        department: '骨科',
        doctor: '王医生',
        appointment_time: '2025-10-22 14:00',
        status: '已完成',
        symptoms: '腰痛'
      }
    ]
    total.value = 2
    loading.value = false
  }, 500)
}

const getRecommendation = () => {
  if (!recommendForm.symptoms) {
    ElMessage.warning('请输入症状描述')
    return
  }
  
  recommendLoading.value = true
  setTimeout(() => {
    recommendation.value = {
      department: '心内科',
      time: '建议3天内就诊',
      advice: '根据您的症状描述，建议挂心内科。就诊前请保持充足休息，避免剧烈运动。'
    }
    recommendLoading.value = false
    ElMessage.success('AI推荐完成')
  }, 1500)
}

const getStatusType = (status) => {
  const map = {
    '待就诊': 'warning',
    '已完成': 'success',
    '已取消': 'info'
  }
  return map[status] || 'info'
}

const handleAddAppointment = () => {
  ElMessage.info('新增预约功能')
}

const handleViewAppointment = (row) => {
  currentAppointment.value = row
  detailDialogVisible.value = true
}

const handleCancelAppointment = (row) => {
  ElMessageBox.confirm('确定要取消这个预约吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('取消成功')
    loadAppointments()
  })
}

onMounted(() => {
  loadAppointments()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}
</style>


