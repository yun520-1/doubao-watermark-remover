# 增强功能说明 (v2.0)

**更新时间**: 2026-03-17
**来源**: seedance-2.0-watermark-remover (GitHub 363⭐)

## 新增核心算法

### 1. 时序稳定性检测 (Temporal Stability Detection)

传统方法仅检测静态边缘，容易将视频内容误判为水印。新增算法：

```python
score = edge_density × (1 / (1 + temporal_std))
```

- **edge_density**: Canny 边缘像素占比 — 水印文字有清晰边缘
- **temporal_std**: 多帧像素变化标准差 — 移动内容得分低，静态水印得分高

**优势**: 即使人物/物体经过水印区域，也能准确识别静态水印

### 2. 四角自动定位 (Auto Corner Detection)

自动扫描视频四角，无需手动配置坐标：

```python
corner_h = max(60, int(height * 0.08))  # 8% 高度
corner_w = max(120, int(width * 0.12))  # 12% 宽度
```

检测区域：
- 左上角、右上角、左下角、右下角
- 自动选择得分最高的角落

### 3. Canny 边缘密度评分

使用 Canny 边缘检测构建精确掩码：
- 仅追踪文字笔画边缘
- 避免过度遮罩均匀背景（天空、墙壁等）
- 连通分量分析，过滤小噪点

### 4. 双修复模式

| 模式 | 说明 | 速度 | 质量 |
|------|------|------|------|
| **OpenCV TELEA** | CPU 快速修复 | ⚡⚡⚡ | ⭐⭐⭐ |
| **LaMa AI** | GPU AI 修复 | ⚡⚡ | ⭐⭐⭐⭐⭐ |

## 使用方法

### 自动检测（推荐）

```bash
python seedance_enhanced.py input.mp4
python seedance_enhanced.py input.mp4 -o clean.mp4
```

### 手动指定区域

```bash
python seedance_enhanced.py input.mp4 -r 10,5,120,60
# 格式：x,y,w,h (像素)
```

### AI 高质量修复

```bash
pip install torch iopaint
python seedance_enhanced.py input.mp4 --lama
```

## 与原有工具对比

| 功能 | final_perfect.py | seedance_enhanced.py |
|------|------------------|---------------------|
| 水印检测 | 用户手动配置 | ✅ 自动四角扫描 |
| 时序分析 | ❌ 单帧分析 | ✅ 60 帧时序稳定性 |
| 边缘密度评分 | ❌ | ✅ Canny + 连通分量 |
| 修复算法 | Telea + 距离变换 | Telea / LaMa AI |
| 适用场景 | 已知固定位置 | 未知位置/多平台 |

## 推荐工作流

1. **先用 seedance_enhanced.py 自动检测** → 确定水印位置
2. **记录检测到的坐标** → 用于批量处理
3. **用 final_perfect.py 批量处理** → 更高效的批量性能

## 依赖安装

```bash
# 基础依赖（CPU 模式）
pip install opencv-python-headless numpy

# FFmpeg（必需）
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Ubuntu

# 可选：LaMa AI 修复（高质量）
pip install torch iopaint
```

## 性能参考

| 视频规格 | CPU (TELEA) | GPU (LaMa) |
|---------|-------------|------------|
| 720x1280, 10 秒 | ~8 秒 | ~15 秒 |
| 1080x1920, 30 秒 | ~25 秒 | ~45 秒 |
| 1920x1080, 60 秒 | ~50 秒 | ~90 秒 |

---

**集成来源**: https://github.com/SamurAIGPT/seedance-2.0-watermark-remover  
**许可证**: MIT
