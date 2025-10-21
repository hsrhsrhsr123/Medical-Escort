#!/bin/bash

# 医疗陪诊Agent系统 - 前端启动脚本

echo "=================================="
echo "  医疗陪诊Agent系统 - 前端"
echo "=================================="
echo ""

# 检查Node.js版本
if ! command -v node &> /dev/null; then
    echo "错误: 未检测到 Node.js，请先安装 Node.js"
    echo "推荐版本: Node.js 16.x 或更高版本"
    exit 1
fi

node_version=$(node --version)
echo "Node.js版本: $node_version"

# 检查npm
if ! command -v npm &> /dev/null; then
    echo "错误: 未检测到 npm"
    exit 1
fi

npm_version=$(npm --version)
echo "npm版本: $npm_version"
echo ""

# 检查是否已安装依赖
if [ ! -d "node_modules" ]; then
    echo "检测到首次运行，正在安装依赖..."
    echo ""
    npm install
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ 依赖安装失败！"
        echo "请尝试手动安装: npm install"
        exit 1
    fi
    
    echo ""
    echo "✅ 依赖安装完成"
    echo ""
fi

# 检查后端服务
echo "检查后端服务状态..."
backend_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ 2>/dev/null)

if [ "$backend_status" != "200" ]; then
    echo "⚠️  警告: 后端服务未运行 (http://localhost:8000)"
    echo "请先启动后端服务: cd .. && bash start.sh"
    echo ""
    read -p "是否继续启动前端? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ 后端服务运行正常"
fi

echo ""
echo "=================================="
echo "启动前端开发服务器..."
echo "=================================="
echo ""
echo "前端地址: http://localhost:3000"
echo "后端API: http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动开发服务器
npm run dev


