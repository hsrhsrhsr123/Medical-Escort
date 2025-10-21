# 医疗陪诊Agent系统 - 前端

基于 Vue 3 + Element Plus 的现代化医疗陪诊管理系统前端界面。

## ✨ 功能特性

- 🏠 **系统首页** - 数据统计与系统概览
- 👤 **用户管理** - 用户信息管理与维护
- 📅 **预约挂号** - 智能预约推荐与管理
- 🏥 **就医指导** - AI症状分析与就医建议
- 💊 **用药指导** - 用药查询与提醒管理

## 🛠️ 技术栈

- **框架**: Vue 3.3+ (Composition API)
- **UI组件库**: Element Plus 2.4+
- **构建工具**: Vite 5.0
- **路由**: Vue Router 4.2+
- **状态管理**: Pinia 2.1+
- **HTTP客户端**: Axios 1.6+

## 📦 安装依赖

```bash
cd frontend
npm install
```

如果网络较慢，可以使用淘宝镜像：

```bash
npm install --registry=https://registry.npmmirror.com
```

## 🚀 启动开发服务器

```bash
npm run dev
```

服务将在 http://localhost:3000 启动

## 🏗️ 构建生产版本

```bash
npm run build
```

构建产物将输出到 `dist` 目录

## 📁 项目结构

```
frontend/
├── src/
│   ├── api/              # API接口
│   │   ├── request.js    # axios封装
│   │   ├── users.js      # 用户相关API
│   │   ├── appointments.js # 预约相关API
│   │   ├── guidance.js   # 指导相关API
│   │   └── medications.js # 用药相关API
│   ├── components/       # 通用组件
│   │   └── Layout.vue    # 布局组件
│   ├── views/           # 页面组件
│   │   ├── Home.vue     # 首页
│   │   ├── Users.vue    # 用户管理
│   │   ├── Appointments.vue # 预约挂号
│   │   ├── Guidance.vue # 就医指导
│   │   └── Medications.vue # 用药指导
│   ├── router/          # 路由配置
│   │   └── index.js
│   ├── styles/          # 全局样式
│   │   └── main.css
│   ├── App.vue          # 根组件
│   └── main.js          # 入口文件
├── index.html           # HTML模板
├── vite.config.js       # Vite配置
├── package.json         # 依赖配置
└── README.md           # 说明文档
```

## 🔧 配置说明

### 代理配置

开发环境下，API请求会自动代理到后端服务器（http://localhost:8000）

配置文件：`vite.config.js`

```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

### 路由配置

路由采用 History 模式，配置文件：`src/router/index.js`

主要路由：
- `/home` - 首页
- `/users` - 用户管理
- `/appointments` - 预约挂号
- `/guidance` - 就医指导
- `/medications` - 用药指导

## 🎨 UI组件

使用 Element Plus 作为 UI 组件库，已配置中文语言包。

常用组件：
- 表格 (el-table)
- 表单 (el-form)
- 对话框 (el-dialog)
- 消息提示 (ElMessage)
- 确认框 (ElMessageBox)

## 📝 开发规范

### 代码风格

- 使用 Composition API
- 使用 `<script setup>` 语法
- 组件名采用 PascalCase
- 文件名采用 PascalCase

### API调用示例

```javascript
import { userAPI } from '@/api'

// 获取用户列表
const loadUsers = async () => {
  try {
    const data = await userAPI.getUsers({ skip: 0, limit: 10 })
    console.log(data)
  } catch (error) {
    console.error(error)
  }
}
```

## 🔌 API对接

后端API地址：http://localhost:8000

API文档：http://localhost:8000/docs

### 主要接口

#### 用户管理
- `GET /api/users/` - 获取用户列表
- `POST /api/users/` - 创建用户
- `GET /api/users/{id}` - 获取用户详情
- `PUT /api/users/{id}` - 更新用户
- `DELETE /api/users/{id}` - 删除用户

#### 预约挂号
- `GET /api/appointments/user/{user_id}` - 获取用户预约
- `POST /api/appointments/` - 创建预约
- `POST /api/appointments/recommend` - 智能推荐

#### 就医指导
- `POST /api/guidance/symptom-analysis` - 症状分析
- `POST /api/guidance/department-recommend` - 科室推荐

#### 用药指导
- `POST /api/medications/guidance` - 用药指导
- `POST /api/medications/interactions` - 药物相互作用检查

## 🐛 常见问题

### 1. 安装依赖失败

尝试清除缓存后重新安装：

```bash
rm -rf node_modules package-lock.json
npm install
```

### 2. 端口被占用

修改 `vite.config.js` 中的端口号：

```javascript
server: {
  port: 3001  // 改为其他端口
}
```

### 3. API请求失败

检查后端服务是否正常运行（http://localhost:8000）

## 📄 许可证

MIT License

## 👥 联系方式

- 项目地址：医疗陪诊Agent系统
- 版本：v1.0.0


