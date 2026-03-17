#!/bin/bash

echo "================================================================"
echo "📦 豆包 AI 视频水印去除 - 一键发布脚本"
echo "================================================================"
echo ""

# 进入项目目录
cd /Users/apple/.jvs/.openclaw/workspace/qq-watermark-remover

# 检查登录状态
echo "🔍 检查登录状态..."
if ! clawhub whoami > /dev/null 2>&1; then
    echo ""
    echo "⚠️  未登录，请先登录 ClawHub"
    echo ""
    echo "📝 运行以下命令登录："
    echo "   clawhub login"
    echo ""
    echo "或者在浏览器访问："
    echo "   https://clawhub.ai/cli/auth"
    echo ""
    echo "登录完成后，重新运行此脚本。"
    echo "================================================================"
    exit 1
fi

echo "✅ 已登录：$(clawhub whoami)"
echo ""

# 发布信息
echo "📋 发布信息："
echo "   SLUG:   doubao-watermark-remover"
echo "   NAME:   豆包 AI 视频水印去除"
echo "   VERSION: 1.0.0"
echo "   TAGS:   doubao,watermark,video,ai"
echo ""

# 发布
echo "🚀 开始发布..."
echo ""

clawhub publish ./ \
  --slug doubao-watermark-remover \
  --name "豆包 AI 视频水印去除" \
  --version 1.0.0 \
  --changelog "初始版本 - 智能豆包 AI 视频水印去除工具" \
  --tags "doubao,watermark,video,ai"

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================================"
    echo "🎉 发布成功！"
    echo "================================================================"
    echo ""
    echo "📦 项目名称：doubao-watermark-remover"
    echo "🏷️  版本：1.0.0"
    echo "🔖 标签：doubao, watermark, video, ai"
    echo ""
    echo "📥 安装命令:"
    echo "   clawhub install doubao-watermark-remover"
    echo ""
    echo "🔗 ClawHub 页面:"
    echo "   https://clawhub.ai/skills/doubao-watermark-remover"
    echo ""
    echo "================================================================"
else
    echo ""
    echo "================================================================"
    echo "❌ 发布失败"
    echo "================================================================"
    echo ""
    echo "可能的原因："
    echo "1. 网络连接问题"
    echo "2. GitHub API 限流（请等待几分钟后重试）"
    echo "3. Slug 已被占用（尝试改为 doubao-watermark-remover-v2）"
    echo ""
    exit 1
fi
