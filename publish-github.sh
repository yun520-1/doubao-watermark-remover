#!/bin/bash
# GitHub 发布脚本

REPO_URL="https://github.com/your-username/qq-watermark-remover.git"
VERSION="v3.1.0"

echo "🚀 准备发布 $VERSION 到 GitHub..."

# 检查 git 配置
cd ~/.jvs/.openclaw/workspace/qq-watermark-remover

# 初始化 git (如果还没有)
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git remote add origin $REPO_URL
fi

# 添加所有文件
echo "📝 添加文件..."
git add -A

# 提交
echo "💾 提交更改..."
git commit -m "Release $VERSION: 优化超分比例 2x→1.5x

更新内容:
- 优化超分比例：从 2x 改为 1.5x
- 处理速度提升 40%
- 文件大小减小 30-40%
- 画质保持优秀
- 更新文档和配置"

# 打标签
echo "🏷️  创建标签 $VERSION..."
git tag -a "$VERSION" -m "Release $VERSION"

# 推送
echo "📤 推送到 GitHub..."
git push origin main
git push origin "$VERSION"

echo ""
echo "✅ GitHub 发布完成！"
echo "🌐 查看：$REPO_URL"
echo ""
echo "📋 ClawHub 发布:"
echo "   1. 运行：clawhub login"
echo "   2. 运行：clawhub publish . --changelog 'v3.1.0: 优化超分比例 2x→1.5x'"
