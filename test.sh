#!/bin/bash
# 豆包 AI 视频水印去除 - 测试脚本

echo "========================================"
echo "🧪 豆包 AI 视频水印去除 - 功能测试"
echo "========================================"
echo ""

# 1. 检查依赖
echo "1️⃣ 检查依赖..."
python3 -c "import cv2" 2>/dev/null && echo "   ✅ OpenCV" || echo "   ❌ OpenCV 未安装"
python3 -c "import numpy" 2>/dev/null && echo "   ✅ NumPy" || echo "   ❌ NumPy 未安装"
python3 -c "import tqdm" 2>/dev/null && echo "   ✅ tqdm" || echo "   ❌ tqdm 未安装"
ffmpeg -version &>/dev/null && echo "   ✅ FFmpeg" || echo "   ❌ FFmpeg 未安装"
echo ""

# 2. 检查脚本文件
echo "2️⃣ 检查脚本文件..."
ls -1 *.py 2>/dev/null | while read file; do
    echo "   ✅ $file"
done
echo ""

# 3. 测试帮助信息
echo "3️⃣ 测试帮助信息..."
python3 final_perfect_v2_enhanced.py --help 2>&1 | head -5
echo ""

# 4. 显示版本信息
echo "4️⃣ 版本信息..."
cat package.json 2>/dev/null | grep version || echo "   无 package.json"
echo ""

echo "========================================"
echo "✅ 检查完成！"
echo "========================================"
echo ""
echo "📝 使用示例:"
echo "   python3 final_perfect_v2_enhanced.py video.mp4"
echo ""
