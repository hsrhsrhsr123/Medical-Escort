<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">就医指导</h1>
      <p class="page-description">智能症状分析与就医建议</p>
    </div>

    <el-row :gutter="20">
      <!-- 症状分析 -->
      <el-col :xs="24" :lg="12">
        <el-card class="info-card" shadow="hover" style="height: 600px;">
          <template #header>
            <div class="card-header">
              <el-icon><DocumentChecked /></el-icon>
              <span style="margin-left: 8px;">症状智能分析</span>
            </div>
          </template>
          
          <el-form
            ref="symptomFormRef"
            :model="symptomForm"
            label-width="100px"
          >
            <el-form-item label="主要症状" required>
              <el-input
                v-model="symptomForm.main_symptom"
                placeholder="如：头痛、发热、咳嗽等"
              />
            </el-form-item>
            
            <el-form-item label="持续时间">
              <el-select v-model="symptomForm.duration" placeholder="选择时间" style="width: 100%;">
                <el-option label="1天内" value="1d" />
                <el-option label="2-3天" value="2-3d" />
                <el-option label="3-7天" value="3-7d" />
                <el-option label="1周以上" value="1w+" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="伴随症状">
              <el-checkbox-group v-model="symptomForm.accompanying_symptoms">
                <el-checkbox label="发热" />
                <el-checkbox label="头晕" />
                <el-checkbox label="恶心" />
                <el-checkbox label="乏力" />
                <el-checkbox label="食欲不振" />
                <el-checkbox label="其他" />
              </el-checkbox-group>
            </el-form-item>
            
            <el-form-item label="详细描述">
              <el-input
                v-model="symptomForm.description"
                type="textarea"
                :rows="4"
                placeholder="请详细描述您的症状和不适感"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                :loading="analyzing"
                @click="analyzeSymptom"
                style="width: 100%;"
                size="large"
              >
                <el-icon style="margin-right: 8px;"><Search /></el-icon>
                开始AI分析
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 分析结果 -->
      <el-col :xs="24" :lg="12">
        <el-card class="info-card" shadow="hover" style="height: 600px; overflow-y: auto;">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span style="margin-left: 8px;">分析结果</span>
            </div>
          </template>
          
          <el-empty
            v-if="!analysisResult"
            description="暂无分析结果，请先进行症状分析"
            :image-size="100"
          />
          
          <div v-else class="analysis-result">
            <el-alert
              type="info"
              :closable="false"
              style="margin-bottom: 20px;"
            >
              <template #title>
                <div style="font-size: 16px; font-weight: 600;">
                  ⚠️ 温馨提示
                </div>
              </template>
              本分析结果仅供参考，不能替代专业医生的诊断，如症状严重请及时就医。
            </el-alert>

            <el-divider content-position="left">
              <strong>可能的疾病</strong>
            </el-divider>
            <el-tag
              v-for="disease in analysisResult.possible_diseases"
              :key="disease"
              type="warning"
              size="large"
              style="margin: 4px;"
            >
              {{ disease }}
            </el-tag>

            <el-divider content-position="left">
              <strong>推荐科室</strong>
            </el-divider>
            <div style="margin-bottom: 20px;">
              <el-tag
                v-for="dept in analysisResult.recommended_departments"
                :key="dept"
                type="success"
                size="large"
                style="margin: 4px;"
              >
                {{ dept }}
              </el-tag>
            </div>

            <el-divider content-position="left">
              <strong>就医建议</strong>
            </el-divider>
            <div class="advice-content">
              <p v-for="(advice, index) in analysisResult.advice" :key="index">
                {{ index + 1 }}. {{ advice }}
              </p>
            </div>

            <el-divider content-position="left">
              <strong>注意事项</strong>
            </el-divider>
            <el-alert
              v-for="(note, index) in analysisResult.precautions"
              :key="index"
              :title="note"
              type="warning"
              :closable="false"
              style="margin-bottom: 8px;"
            />

            <div style="margin-top: 20px; text-align: center;">
              <el-button type="primary" size="large" @click="gotoAppointment">
                立即预约挂号
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 就医准备 -->
    <el-card class="info-card" shadow="hover" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>就医准备清单</span>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="6" v-for="item in preparationItems" :key="item.title">
          <div class="preparation-item">
            <el-icon :size="40" :color="item.color">
              <component :is="item.icon" />
            </el-icon>
            <h3>{{ item.title }}</h3>
            <ul>
              <li v-for="detail in item.details" :key="detail">{{ detail }}</li>
            </ul>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, DocumentChecked, Document } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const analyzing = ref(false)
const analysisResult = ref(null)

const symptomForm = reactive({
  main_symptom: '',
  duration: '',
  accompanying_symptoms: [],
  description: ''
})

const preparationItems = [
  {
    title: '证件准备',
    icon: 'Document',
    color: '#409EFF',
    details: ['身份证', '医保卡', '就诊卡']
  },
  {
    title: '病历资料',
    icon: 'Folder',
    color: '#67C23A',
    details: ['既往病历', '检查报告', '用药记录']
  },
  {
    title: '注意事项',
    icon: 'Warning',
    color: '#E6A23C',
    details: ['空腹检查', '提前到达', '准备口罩']
  },
  {
    title: '费用准备',
    icon: 'Money',
    color: '#F56C6C',
    details: ['现金/医保', '预留费用', '报销凭证']
  }
]

const analyzeSymptom = () => {
  if (!symptomForm.main_symptom) {
    ElMessage.warning('请输入主要症状')
    return
  }
  
  analyzing.value = true
  
  // 模拟AI分析
  setTimeout(() => {
    analysisResult.value = {
      possible_diseases: ['普通感冒', '流行性感冒', '上呼吸道感染'],
      recommended_departments: ['呼吸内科', '全科医学科'],
      advice: [
        '建议尽快就医，进行血常规和胸部X光检查',
        '注意休息，多喝水，保持室内通风',
        '如出现高热不退、呼吸困难等症状，需立即就医',
        '就医时请携带近期用药记录'
      ],
      precautions: [
        '如果出现持续高热（38.5℃以上）超过3天，请立即就医',
        '如果出现呼吸困难、胸痛等严重症状，请拨打120',
        '就医前避免自行服用抗生素'
      ]
    }
    analyzing.value = false
    ElMessage.success('分析完成')
  }, 2000)
}

const gotoAppointment = () => {
  router.push('/appointments')
}
</script>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
  font-weight: 600;
}

.analysis-result {
  line-height: 1.8;
}

.advice-content p {
  margin: 8px 0;
  padding-left: 12px;
  border-left: 3px solid #409EFF;
}

.preparation-item {
  text-align: center;
  padding: 20px;
  border-radius: 8px;
  background: #f5f7fa;
  margin-bottom: 16px;
}

.preparation-item h3 {
  margin: 12px 0;
  color: #303133;
}

.preparation-item ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.preparation-item li {
  margin: 4px 0;
  color: #606266;
  font-size: 14px;
}
</style>


