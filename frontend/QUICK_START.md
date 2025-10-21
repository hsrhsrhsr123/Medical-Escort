# 快速开始指南

## 🚀 5分钟快速启动

### 前提条件

确保已经安装：
- Node.js 16+ （执行 `node --version` 检查）
- npm （执行 `npm --version` 检查）
- 后端服务已启动在 http://localhost:8000

### 第一步：安装依赖

```bash
cd frontend
npm install
```

如果安装速度慢，可以使用国内镜像：
```bash
npm install --registry=https://registry.npmmirror.com
```

### 第二步：启动开发服务器

**方式1：使用启动脚本（推荐）**
```bash
bash start-frontend.sh
```

**方式2：直接使用 npm**
```bash
npm run dev
```

### 第三步：访问系统

打开浏览器访问：http://localhost:3000

## 📱 功能预览

### 主要页面

1. **首页** (`/home`)
   - 系统数据统计
   - 快捷功能入口
   - 最近活动时间线

2. **用户管理** (`/users`)
   - 用户列表查看
   - 新增/编辑用户
   - 用户信息管理

3. **预约挂号** (`/appointments`)
   - AI智能预约推荐
   - 预约记录管理
   - 预约状态跟踪

4. **就医指导** (`/guidance`)
   - 症状智能分析
   - 科室推荐
   - 就医准备清单

5. **用药指导** (`/medications`)
   - 用药指导查询
   - 药物相互作用检查
   - 用药提醒管理

## 🎨 界面特色

- ✅ 现代化设计，简洁美观
- ✅ 响应式布局，支持各种屏幕
- ✅ 深色侧边栏，提升视觉体验
- ✅ 动画过渡效果
- ✅ 完整的表单验证
- ✅ 友好的错误提示

## 🔧 常用命令

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 🐛 常见问题

### 1. 端口被占用

如果 3000 端口被占用，修改 `vite.config.js`：
```javascript
server: {
  port: 3001  // 改为其他可用端口
}
```

### 2. API 请求失败

- 检查后端服务是否启动：http://localhost:8000
- 检查浏览器控制台的错误信息
- 确认 API 代理配置是否正确

### 3. 依赖安装失败

尝试清除缓存：
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### 4. Element Plus 图标不显示

确保已正确安装 `@element-plus/icons-vue`：
```bash
npm install @element-plus/icons-vue
```

## 📚 开发指南

### 添加新页面

1. 在 `src/views/` 创建新的 Vue 组件
2. 在 `src/router/index.js` 添加路由配置
3. 在侧边栏菜单中添加入口

### 调用 API

```javascript
import { userAPI } from '@/api'

// 获取数据
const data = await userAPI.getUsers()

// 创建数据
await userAPI.createUser({ name: '张三', phone: '13800138000' })
```

### 使用 Element Plus 组件

```vue
<template>
  <el-button type="primary">按钮</el-button>
  <el-table :data="tableData">
    <!-- 表格内容 -->
  </el-table>
</template>
```

## 🎯 下一步

- 查看完整文档：[README.md](./README.md)
- 学习 Vue 3：https://cn.vuejs.org/
- 学习 Element Plus：https://element-plus.org/zh-CN/

## 💡 提示

- 开发过程中，修改代码会自动热重载
- 使用浏览器开发者工具调试
- 查看后端 API 文档：http://localhost:8000/docs

祝你使用愉快！ 🎉


