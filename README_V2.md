# Doubao Watermark Remover v2.0

**豆包水印去除 + 语音识别 + 网红字幕自动生成**

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## ✨ 核心功能

### 1. 🎯 水印去除
- 自动检测"豆包 AI 生成"水印
- 三段式跳跃水印追踪
- 骨架级精准修复
- 视觉无损质量

### 2. 🎤 语音识别 (ASR)
- Whisper 语音识别引擎
- 支持中文/英文/方言
- 时间戳精确到 0.1 秒
- 自动断句和标点

### 3. 📝 网红字幕
| 样式 | 特点 | 适用 |
|------|------|------|
| **抖音风** | 黄字白边 + 弹跳 | 短视频 |
| **快手风** | 白字黑边 + 放大 | 直播切片 |
| **电影感** | 白字阴影 + 淡入 | Vlog |
| **综艺风** | 彩色 + 动画 | 搞笑视频 |

---

## 🚀 快速开始

### 安装依赖
```bash
pip3 install openai-whisper
```

### 单个视频处理
```bash
# 基础用法 (去水印 + 抖音字幕)
python3 final_perfect_v4_with_subtitles.py input.mp4 -o ./output

# 指定字幕样式
python3 final_perfect_v4_with_subtitles.py input.mp4 -o ./output --style movie

# 不生成字幕
python3 final_perfect_v4_with_subtitles.py input.mp4 -o ./output --no-subtitles
```

### 批量处理
```bash
# 批量处理 (抖音风格)
python3 batch_with_subtitles.py /input/dir /output/dir

# 指定样式
python3 batch_with_subtitles.py /input/dir /output/dir --style kuaishou
```

---

## 📊 处理流程

```
输入视频
    ↓
[1] 水印检测 → 识别位置
    ↓
[2] 水印去除 → 帧级修复
    ↓
[3] 音频提取 → 分离音轨
    ↓
[4] 语音识别 → Whisper ASR
    ↓
[5] 字幕生成 → ASS/SRT
    ↓
[6] 字幕烧录 → FFmpeg
    ↓
[7] 编码优化 → CRF 20
    ↓
输出视频 (无水印 + 字幕)
```

---

## 🎨 字幕样式配置

### 抖音风格 (douyin)
```ini
字体：站酷快乐体
字号：48px
颜色：渐变黄 (#FFD700 → #FFA500)
描边：白色 3px
阴影：黑色 2px
动画：弹跳效果
位置：底部 15%
```

### 快手风格 (kuaishou)
```ini
字体：思源黑体
字号：52px
颜色：纯白 (#FFFFFF)
描边：黑色 4px
阴影：无
动画：淡入淡出
位置：底部 20%
```

### 电影风格 (movie)
```ini
字体：思源宋体
字号：42px
颜色：纯白 (#FFFFFF)
描边：无
阴影：黑色 1px 模糊
动画：淡入淡出 (500ms)
位置：底部 10%
```

### 综艺风格 (variety)
```ini
字体：站酷快乐体
字号：56px
颜色：渐变粉 (#FF69B4 → #FFD700)
描边：无
阴影：黑色 3px
动画：移动弹跳
位置：底部 25%
```

---

## 📁 输出文件

```
output/
├── video_clean.mp4          # 去水印视频
├── video_clean_sub.mp4      # 去水印 + 字幕
├── subtitle.ass              # ASS 特效字幕
├── subtitle.srt              # SRT 字幕
└── temp/
    └── audio.wav             # 提取的音频
```

---

## ⚡ 性能优化

### GPU 加速
```python
# 使用 Metal (macOS)
export WHISPER_DEVICE=mps

# 使用 CUDA (NVIDIA)
export WHISPER_DEVICE=cuda
```

### 模型选择
```python
# 快速模式 (推荐)
whisper.load_model("tiny")

# 平衡模式
whisper.load_model("base")

# 高质量模式
whisper.load_model("small")

# 最佳质量
whisper.load_model("large")
```

---

## 🐛 故障排除

### Q: Whisper 安装失败
```bash
# 升级 pip
pip3 install --upgrade pip

# 重新安装
pip3 install openai-whisper --no-cache-dir
```

### Q: 语音识别慢
```bash
# 使用更小模型
# 编辑 final_perfect_v4_with_subtitles.py
# 修改：whisper.load_model("tiny")
```

### Q: 字幕位置不对
```bash
# 调整 margin_v 参数
# 在 STYLES 字典中修改对应样式的 margin_v 值
```

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **Whisper:** https://github.com/openai/whisper
- **FFmpeg:** https://ffmpeg.org/
- **ClawHub:** https://clawhub.ai/yun520-1/doubao-watermark-remover

---

**版本:** 2.0  
**更新日期:** 2026-03-21  
**作者:** yun520-1
