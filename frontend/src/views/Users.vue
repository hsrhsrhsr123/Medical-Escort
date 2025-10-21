<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">用户管理</h1>
      <p class="page-description">管理系统用户信息</p>
    </div>

    <el-card class="info-card" shadow="hover">
      <!-- 搜索和操作栏 -->
      <div class="toolbar">
        <el-space>
          <el-input
            v-model="searchQuery"
            placeholder="搜索用户姓名或手机号"
            :prefix-icon="Search"
            clearable
            style="width: 300px;"
            @change="handleSearch"
          />
          <el-button type="primary" :icon="Refresh" @click="loadUsers">
            刷新
          </el-button>
        </el-space>
        
        <el-button type="primary" :icon="Plus" @click="handleAdd">
          新增用户
        </el-button>
      </div>

      <!-- 用户表格 -->
      <el-table
        :data="users"
        v-loading="loading"
        stripe
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="phone" label="手机号" width="140" />
        <el-table-column prop="id_card" label="身份证号" width="180" />
        <el-table-column prop="age" label="年龄" width="80" />
        <el-table-column prop="gender" label="性别" width="80">
          <template #default="{ row }">
            <el-tag :type="row.gender === '男' ? 'primary' : 'danger'">
              {{ row.gender }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" width="180" />
        <el-table-column label="操作" fixed="right" width="200">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              :icon="View"
              @click="handleView(row)"
            >
              查看
            </el-button>
            <el-button
              type="primary"
              link
              :icon="Edit"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              link
              :icon="Delete"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div style="margin-top: 20px; display: flex; justify-content: flex-end;">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadUsers"
          @current-change="loadUsers"
        />
      </div>
    </el-card>

    <!-- 新增/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
        
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>
        
        <el-form-item label="身份证号" prop="id_card">
          <el-input v-model="form.id_card" placeholder="请输入身份证号" />
        </el-form-item>
        
        <el-form-item label="年龄" prop="age">
          <el-input-number v-model="form.age" :min="0" :max="150" />
        </el-form-item>
        
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="form.gender">
            <el-radio label="男">男</el-radio>
            <el-radio label="女">女</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="紧急联系人" prop="emergency_contact">
          <el-input v-model="form.emergency_contact" placeholder="请输入紧急联系人" />
        </el-form-item>
        
        <el-form-item label="联系电话" prop="emergency_phone">
          <el-input v-model="form.emergency_phone" placeholder="请输入联系电话" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Refresh, Plus, View, Edit, Delete } from '@element-plus/icons-vue'
import { userAPI } from '@/api'

const loading = ref(false)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const users = ref([])

const dialogVisible = ref(false)
const dialogTitle = ref('新增用户')
const formRef = ref(null)
const form = reactive({
  name: '',
  phone: '',
  id_card: '',
  age: 0,
  gender: '男',
  emergency_contact: '',
  emergency_phone: ''
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  id_card: [{ required: true, message: '请输入身份证号', trigger: 'blur' }]
}

// 加载用户列表
const loadUsers = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }
    // 模拟数据
    users.value = [
      {
        id: 1,
        name: '张三',
        phone: '13800138000',
        id_card: '110101199001011234',
        age: 35,
        gender: '男',
        created_at: '2025-01-15 10:30:00'
      },
      {
        id: 2,
        name: '李四',
        phone: '13900139000',
        id_card: '110101199202022345',
        age: 32,
        gender: '女',
        created_at: '2025-01-16 14:20:00'
      }
    ]
    total.value = 2
  } catch (error) {
    ElMessage.error('加载用户列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadUsers()
}

const handleAdd = () => {
  dialogTitle.value = '新增用户'
  Object.assign(form, {
    name: '',
    phone: '',
    id_card: '',
    age: 0,
    gender: '男',
    emergency_contact: '',
    emergency_phone: ''
  })
  dialogVisible.value = true
}

const handleView = (row) => {
  ElMessage.info(`查看用户: ${row.name}`)
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑用户'
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定要删除用户 ${row.name} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
    loadUsers()
  })
}

const handleSubmit = () => {
  formRef.value?.validate((valid) => {
    if (valid) {
      ElMessage.success('保存成功')
      dialogVisible.value = false
      loadUsers()
    }
  })
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
</style>


