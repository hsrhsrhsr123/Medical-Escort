# 医疗陪诊Agent系统

## 项目简介

这是一个为老年人设计的智能医疗陪诊助手系统，旨在帮助在大城市打拼的子女远程协助老人完成就医全流程。系统通过AI技术实现症状分析、智能导诊、预约挂号、流程引导和用药指导等功能，减少老人看病的困难和子女的负担。

## 核心功能

### 1. 症状分析与智能导诊
- 基于AI的症状分析
- 智能推荐就诊科室
- 评估病情紧急程度
- 提供就医建议

### 2. 预约挂号自动化
- 搜索附近医院
- 查看可预约时间
- 自动完成预约流程
- 预约状态查询和管理

### 3. 就医流程全程引导
- 分步骤详细指导（挂号、候诊、就诊、检查、缴费、取药）
- 医院内部位置指引
- 语音播报支持
- 实时进度跟踪

### 4. 用药指导与提醒
- 处方自动解析
- 详细用药说明
- 智能用药时间表
- 定时用药提醒
- 药物相互作用检查

### 5. 健康档案管理
- 个人健康档案
- 就医记录存储
- 病历资料管理
- 紧急联系人设置

## 系统架构

```
medical-escort/
├── agents/                 # AI Agent模块
│   ├── symptom_analyzer.py    # 症状分析Agent
│   ├── appointment_agent.py   # 预约挂号Agent
│   ├── guidance_agent.py      # 就医指导Agent
│   └── medication_guide.py    # 用药指导Agent
├── api/                    # API接口
│   ├── main.py                # 主应用入口
│   ├── users.py               # 用户管理API
│   ├── appointments.py        # 预约管理API
│   ├── guidance.py            # 就医指导API
│   └── medications.py         # 用药指导API
├── models.py               # 数据模型
├── database.py             # 数据库配置
├── config.py               # 配置管理
└── requirements.txt        # 依赖包
```

## 技术栈

- **后端框架**: FastAPI
- **AI模型**: OpenAI GPT-4
- **数据库**: SQLite/PostgreSQL + MongoDB
- **日志**: Loguru
- **API文档**: Swagger UI

## 安装部署

### 1. 环境要求

- Python 3.9+
- pip

### 2. 安装依赖

```bash
cd "Medical Escort"
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件并配置以下参数：

```env
# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key

# 数据库配置
DATABASE_URL=sqlite:///./medical_escort.db

# 安全配置
SECRET_KEY=your_secret_key_here
```

### 4. 初始化数据库

```bash
python -c "from database import init_db; init_db()"
```

### 5. 启动服务

```bash
cd api
python main.py
```

服务将在 `http://localhost:8000` 启动。

访问 `http://localhost:8000/docs` 查看API文档。

## API使用示例

### 1. 创建用户

```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "phone": "13800138000",
    "age": 70,
    "gender": "男",
    "emergency_contact_name": "李四",
    "emergency_contact_phone": "13900139000"
  }'
```

### 2. 症状分析

```bash
curl -X POST "http://localhost:8000/api/appointments/analyze-symptoms" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "symptoms": "最近几天一直头晕，有时候还感觉胸闷"
  }'
```

### 3. 搜索医院

```bash
curl "http://localhost:8000/api/appointments/hospitals?location=市中心&department=心血管内科"
```

### 4. 创建预约

```bash
curl -X POST "http://localhost:8000/api/appointments/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "hospital_id": "h001",
    "hospital_name": "市人民医院",
    "department": "心血管内科",
    "appointment_date": "2024-01-15T09:00:00"
  }'
```

### 5. 获取就医指导

```bash
curl "http://localhost:8000/api/guidance/appointment/1/full"
```

### 6. 生成用药提醒

```bash
curl -X POST "http://localhost:8000/api/medications/reminders" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "medications": [
      {
        "name": "阿司匹林",
        "dosage": "100mg",
        "frequency": "每日1次",
        "timing": "晚饭后",
        "duration": "长期"
      }
    ]
  }'
```

## 主要特点

### 🎯 为老人设计
- 简单明了的交互流程
- 语音播报支持
- 大字体清晰界面
- 贴心的分步指导

### 🤖 AI智能助手
- 专业的症状分析
- 智能科室推荐
- 个性化就医建议
- 自然语言交互

### 📱 远程关怀
- 家属实时了解就医进度
- 紧急情况自动通知
- 就医记录共享
- 健康档案管理

### 🔒 安全可靠
- 个人信息加密存储
- 医疗数据隐私保护
- 权限分级管理
- 操作日志记录

## 使用场景

1. **老人独立就医**
   - 老人可以按照系统指导独立完成就医流程
   - 每个步骤都有详细的语音和文字指导
   - 遇到困难可以随时查看帮助

2. **子女远程协助**
   - 子女在外地也能帮助老人预约挂号
   - 实时了解老人就医进度
   - 查看诊断结果和用药情况

3. **慢性病管理**
   - 定期复诊提醒
   - 用药时间表管理
   - 健康数据记录
   - 长期病情跟踪

## 扩展功能（规划中）

- [ ] 微信公众号/小程序接入
- [ ] 语音识别和语音合成
- [ ] 视频通话远程协助
- [ ] 医院地图导航
- [ ] 医保费用自动结算
- [ ] 电子病历对接
- [ ] 体检报告解读
- [ ] 健康知识科普

## 注意事项

1. **医疗免责声明**
   - 本系统提供的建议仅供参考，不能替代专业医生的诊断
   - 紧急情况请立即拨打120或前往医院急诊
   - 所有医疗决策应遵从医生指导

2. **数据安全**
   - 妥善保管API密钥和访问凭证
   - 定期备份数据库
   - 生产环境使用HTTPS加密传输

3. **医院对接**
   - 当前使用模拟数据，实际部署需要对接医院系统API
   - 不同医院的接口可能需要适配
   - 需要获得医院的API授权

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目！

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至：hsr2001@link.cuhk.edu.hk


---

**让老人看病更简单，让子女更放心！** ❤️




