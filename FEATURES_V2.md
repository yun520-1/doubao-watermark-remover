# Doubao Watermark Remover v2.0 - 增强版

## 🎯 新增功能

### 1. 🎤 语音识别 (ASR)
- 自动提取视频音频
- 使用 Whisper/本地 ASR 进行语音转文字
- 支持中文、英文、方言识别
- 时间戳精确到 0.1 秒

### 2. 📝 自动生成字幕
- **网红字幕样式**:
  - 🎨 渐变色文字 (黄→橙/白→蓝)
  - 💫 动态弹跳效果
  - 🎭 描边 + 阴影
  - 📱 抖音/快手风格
  - 🎬 电影感字幕

### 3. 🎨 字幕样式模板
| 样式 | 说明 | 适用场景 |
|------|------|----------|
| **抖音风** | 黄字白边 + 弹跳 | 短视频 |
| **快手风** | 白字黑边 + 放大 | 直播切片 |
| **电影感** | 白字阴影 + 淡入 | Vlog |
| **综艺风** | 彩色 + 动画 | 搞笑视频 |
| **简约风** | 纯白 + 淡入淡出 | 教学视频 |

### 4. ⚡ 性能优化
- GPU 加速 (Metal/CUDA)
- 批量处理优化
- 内存管理优化
- 多线程处理

## 🚀 使用方式

### 基础用法
```bash
python3 final_perfect_v2_enhanced.py input.mp4 -o output.mp4
```

### 添加字幕
```bash
python3 final_perfect_v2_enhanced.py input.mp4 -o output.mp4 \
  --add-subtitles \
  --subtitle-style douyin
```

### 批量处理
```bash
python3 batch_final.py /input/dir /output/dir \
  --add-subtitles \
  --subtitle-style movie
```

## 📊 处理流程

1. **水印检测** → 识别水印位置
2. **水印去除** → 帧级别修复
3. **音频提取** → 分离音轨
4. **语音识别** → 生成文字 + 时间戳
5. **字幕生成** → 应用网红样式
6. **视频合成** → 合并画面 + 音频 + 字幕
7. **编码优化** → CRF 20 + 10bit

## 🎬 字幕样式示例

### 抖音风格
```
字体：站酷快乐体
颜色：渐变黄 (#FFD700 → #FFA500)
描边：白色 3px
阴影：黑色 2px 偏移
动画：弹跳效果
位置：底部 15%
```

### 电影风格
```
字体：思源宋体
颜色：纯白 (#FFFFFF)
描边：无
阴影：黑色 1px 模糊
动画：淡入淡出
位置：底部 10%
```

## 📁 输出文件

```
output/
├── video_clean.mp4          # 去水印视频
├── video_clean_sub.mp4      # 去水印 + 字幕
├── subtitles.srt            # SRT 字幕文件
├── subtitles.ass            # ASS 特效字幕
└── audio.wav                # 提取的音频
```
