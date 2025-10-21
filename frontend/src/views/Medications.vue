<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">用药指导</h1>
      <p class="page-description">智能用药建议与提醒管理</p>
    </div>

    <el-row :gutter="20">
      <!-- 用药查询 -->
      <el-col :xs="24" :lg="10">
        <el-card class="info-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Search /></el-icon>
              <span style="margin-left: 8px;">用药指导查询</span>
            </div>
          </template>
          
          <el-tabs v-model="activeTab" type="border-card">
            <el-tab-pane label="单药查询" name="single">
              <el-form :model="singleDrugForm" label-width="100px">
                <el-form-item label="药品名称">
                  <el-input
                    v-model="singleDrugForm.drug_name"
                    placeholder="请输入药品名称"
                  />
                </el-form-item>
                
                <el-form-item label="用药目的">
                  <el-input
                    v-model="singleDrugForm.purpose"
                    placeholder="如：降血压、止痛等"
                  />
                </el-form-item>
                
                <el-form-item>
                  <el-button
                    type="primary"
                    :loading="queryLoading"
                    @click="querySingleDrug"
                    style="width: 100%;"
                  >
                    查询用药指导
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>

            <el-tab-pane label="药物相互作用" name="interaction">
              <el-form :model="interactionForm" label-width="100px">
                <el-form-item label="药品列表">
                  <el-tag
                    v-for="drug in interactionForm.drugs"
                    :key="drug"
                    closable
                    @close="removeDrug(drug)"
                    style="margin: 4px;"
                  >
                    {{ drug }}
                  </el-tag>
                </el-form-item>
                
                <el-form-item label="添加药品">
                  <el-input
                    v-model="newDrug"
                    placeholder="输入药品名称"
                    @keyup.enter="addDrug"
                  >
                    <template #append>
                      <el-button :icon="Plus" @click="addDrug">添加</el-button>
                    </template>
                  </el-input>
                </el-form-item>
                
                <el-form-item>
                  <el-button
                    type="warning"
                    :loading="checkLoading"
                    :disabled="interactionForm.drugs.length < 2"
                    @click="checkInteraction"
                    style="width: 100%;"
                  >
                    检查药物相互作用
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>

          <!-- 查询结果 -->
          <div v-if="guidanceResult" class="guidance-result">
            <el-divider content-position="left">
              <strong>用药指导</strong>
            </el-divider>
            
            <el-descriptions :column="1" border>
              <el-descriptions-item label="药品名称">
                {{ guidanceResult.drug_name }}
              </el-descriptions-item>
              <el-descriptions-item label="用法用量">
                {{ guidanceResult.dosage }}
              </el-descriptions-item>
              <el-descriptions-item label="注意事项">
                {{ guidanceResult.precautions }}
              </el-descriptions-item>
              <el-descriptions-item label="不良反应">
                {{ guidanceResult.side_effects }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <!-- 相互作用结果 -->
          <div v-if="interactionResult" class="interaction-result">
            <el-divider content-position="left">
              <strong>相互作用检查结果</strong>
            </el-divider>
            
            <el-alert
              :type="interactionResult.safe ? 'success' : 'error'"
              :closable="false"
              style="margin-bottom: 12px;"
            >
              <template #title>
                <div style="font-size: 16px;">
                  {{ interactionResult.safe ? '✓ 未发现明显相互作用' : '⚠️ 发现潜在相互作用' }}
                </div>
              </template>
            </el-alert>
            
            <div v-if="!interactionResult.safe">
              <el-tag
                v-for="(warning, index) in interactionResult.warnings"
                :key="index"
                type="danger"
                size="large"
                effect="dark"
                style="margin: 4px; width: calc(100% - 8px);"
              >
                {{ warning }}
              </el-tag>
              
              <el-alert
                type="warning"
                :closable="false"
                style="margin-top: 12px;"
              >
                建议：请在医生指导下使用这些药物，切勿自行调整用药方案
              </el-alert>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 用药提醒 -->
      <el-col :xs="24" :lg="14">
        <el-card class="info-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>用药提醒</span>
              <el-button type="primary" :icon="Plus" @click="handleAddReminder">
                添加提醒
              </el-button>
            </div>
          </template>
          
          <el-table :data="reminders" stripe>
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="drug_name" label="药品名称" width="140" />
            <el-table-column prop="dosage" label="用量" width="120" />
            <el-table-column prop="frequency" label="频率" width="120" />
            <el-table-column prop="time" label="提醒时间" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === '已服用' ? 'success' : 'warning'">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" fixed="right">
              <template #default="{ row }">
                <el-button
                  v-if="row.status === '待服用'"
                  type="success"
                  link
                  :icon="Check"
                  @click="markAsTaken(row)"
                >
                  已服用
                </el-button>
                <el-button
                  type="danger"
                  link
                  :icon="Delete"
                  @click="deleteReminder(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <!-- 用药记录 -->
        <el-card class="info-card" shadow="hover" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span>用药记录</span>
              <el-button type="primary" link>查看全部</el-button>
            </div>
          </template>
          
          <el-timeline>
            <el-timeline-item
              v-for="record in medicationRecords"
              :key="record.id"
              :timestamp="record.time"
              placement="top"
            >
              <el-card>
                <h4>{{ record.drug_name }}</h4>
                <p>剂量：{{ record.dosage }}</p>
                <p>备注：{{ record.note }}</p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>

    <!-- 添加提醒对话框 -->
    <el-dialog
      v-model="reminderDialogVisible"
      title="添加用药提醒"
      width="500px"
    >
      <el-form
        ref="reminderFormRef"
        :model="reminderForm"
        label-width="100px"
      >
        <el-form-item label="药品名称" required>
          <el-input v-model="reminderForm.drug_name" placeholder="请输入药品名称" />
        </el-form-item>
        
        <el-form-item label="用量" required>
          <el-input v-model="reminderForm.dosage" placeholder="如：2片" />
        </el-form-item>
        
        <el-form-item label="频率" required>
          <el-select v-model="reminderForm.frequency" placeholder="选择频率" style="width: 100%;">
            <el-option label="每天1次" value="1" />
            <el-option label="每天2次" value="2" />
            <el-option label="每天3次" value="3" />
            <el-option label="按需服用" value="prn" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="提醒时间" required>
          <el-time-picker
            v-model="reminderForm.time"
            placeholder="选择时间"
            style="width: 100%;"
          />
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input
            v-model="reminderForm.note"
            type="textarea"
            :rows="3"
            placeholder="其他注意事项"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="reminderDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReminder">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Plus, Check, Delete } from '@element-plus/icons-vue'

const activeTab = ref('single')
const queryLoading = ref(false)
const checkLoading = ref(false)
const guidanceResult = ref(null)
const interactionResult = ref(null)
const newDrug = ref('')
const reminderDialogVisible = ref(false)

const singleDrugForm = reactive({
  drug_name: '',
  purpose: ''
})

const interactionForm = reactive({
  drugs: []
})

const reminderForm = reactive({
  drug_name: '',
  dosage: '',
  frequency: '',
  time: '',
  note: ''
})

const reminders = ref([
  {
    id: 1,
    drug_name: '阿司匹林',
    dosage: '1片',
    frequency: '每天1次',
    time: '08:00',
    status: '已服用'
  },
  {
    id: 2,
    drug_name: '降压药',
    dosage: '2片',
    frequency: '每天2次',
    time: '12:00',
    status: '待服用'
  }
])

const medicationRecords = ref([
  {
    id: 1,
    drug_name: '阿司匹林',
    dosage: '1片',
    time: '2025-10-20 08:00',
    note: '饭后服用'
  },
  {
    id: 2,
    drug_name: '降压药',
    dosage: '2片',
    time: '2025-10-20 08:30',
    note: '正常服用'
  }
])

const querySingleDrug = () => {
  if (!singleDrugForm.drug_name) {
    ElMessage.warning('请输入药品名称')
    return
  }
  
  queryLoading.value = true
  setTimeout(() => {
    guidanceResult.value = {
      drug_name: singleDrugForm.drug_name,
      dosage: '口服，一次1-2片，一日3次',
      precautions: '饭后服用，避免空腹。孕妇及哺乳期妇女慎用。',
      side_effects: '可能出现恶心、头晕、皮疹等症状，如症状严重请停药就医'
    }
    interactionResult.value = null
    queryLoading.value = false
    ElMessage.success('查询成功')
  }, 1000)
}

const addDrug = () => {
  if (!newDrug.value) return
  if (interactionForm.drugs.includes(newDrug.value)) {
    ElMessage.warning('该药品已添加')
    return
  }
  interactionForm.drugs.push(newDrug.value)
  newDrug.value = ''
}

const removeDrug = (drug) => {
  const index = interactionForm.drugs.indexOf(drug)
  if (index > -1) {
    interactionForm.drugs.splice(index, 1)
  }
}

const checkInteraction = () => {
  checkLoading.value = true
  setTimeout(() => {
    interactionResult.value = {
      safe: Math.random() > 0.5,
      warnings: [
        '阿司匹林与华法林同时使用可能增加出血风险',
        '建议在医生指导下调整剂量'
      ]
    }
    guidanceResult.value = null
    checkLoading.value = false
    ElMessage.success('检查完成')
  }, 1500)
}

const handleAddReminder = () => {
  Object.assign(reminderForm, {
    drug_name: '',
    dosage: '',
    frequency: '',
    time: '',
    note: ''
  })
  reminderDialogVisible.value = true
}

const submitReminder = () => {
  ElMessage.success('添加成功')
  reminderDialogVisible.value = false
}

const markAsTaken = (row) => {
  row.status = '已服用'
  ElMessage.success('已标记为已服用')
}

const deleteReminder = (row) => {
  ElMessage.success('删除成功')
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.guidance-result,
.interaction-result {
  margin-top: 20px;
}

:deep(.el-tabs--border-card) {
  box-shadow: none;
  border: 1px solid #dcdfe6;
}
</style>


