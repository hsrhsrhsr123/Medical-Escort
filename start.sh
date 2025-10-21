#!/bin/bash

# 医疗陪诊Agent系统启动脚本

echo "=================================="
echo "  医疗陪诊Agent系统"
echo "=================================="
echo ""

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo ""
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo ""
echo "检查依赖包..."
pip install -r requirements.txt -q

# 检查.env文件
if [ ! -f ".env" ]; then
    echo ""
    echo "警告: .env 文件不存在"
    echo "请创建 .env 文件并配置必要的环境变量"
    echo "参考: .env.example"
    exit 1
fi

# 创建日志目录
if [ ! -d "logs" ]; then
    mkdir logs
fi

# 初始化数据库
echo ""
echo "初始化数据库..."
python3 -c "from database import init_db; init_db()"

# 启动服务
echo ""
echo "=================================="
echo "启动API服务..."
echo "=================================="
echo ""
echo "API地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 使用 uvicorn 在根目录启动，这样可以正确导入 config 模块
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload




