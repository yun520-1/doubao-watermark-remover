# 豆包水印去除 v3.0 - 集成增强版

**版本:** 3.0.0  
**发布日期:** 2026-03-21  
**作者:** yun520-1

---

## ✨ 核心功能

### 1. 🎬 水印去除
- 自动检测"豆包 AI 生成"水印
- 三段式跳跃水印追踪
- 骨架级精准修复
- 视觉无损质量

### 2. 🎤 语音识别 (FunASR)
- **阿里达摩院** 中文语音识别
- 准确率 90%+
- 自动标点符号
- 时间戳精确到毫秒

### 3. 🎨 网红字幕
- **思源黑体** Bold
- 黄橙渐变色
- 淡入淡出动画
- 易于阅读

### 4. 🎯 一键处理
- 单个命令完成所有步骤
- 自动流程
- 无需手动干预

---

## 🚀 快速开始

### 安装依赖
```bash
pip3 install funasr modelscope
```

### 基础用法
```bash
# 完整处理 (去水印 + 语音识别 + 字幕)
python3 doubao_watermark_asr.py input.mp4 -o ./output

# 仅去水印
python3 doubao_watermark_asr.py input.mp4 -o ./output --no-subtitle

# 仅语音识别 + 字幕
python3 doubao_watermark_asr.py input.mp4 -o ./output --no-watermark
```

### 参数说明
| 参数 | 说明 | 默认 |
|------|------|------|
| `input` | 输入视频文件 | 必需 |
| `-o, --output` | 输出目录 | `./output` |
| `--no-subtitle` | 不生成字幕 | False |
| `--no-watermark` | 不去除水印 | False |

---

## 📊 处理流程

```
输入视频
    ↓
[1] 提取音频 → PCM 16kHz
    ↓
[2] 去除水印 → 干净视频
    ↓
[3] FunASR 识别 → 文字 + 时间戳
    ↓
[4] 生成字幕 → ASS 格式
    ↓
[5] 烧录字幕 → 最终视频
    ↓
输出 (无水印 + 字幕)
```

---

## 🎨 字幕样式配置

### 默认样式
```ini
字体：SourceHanSansCN-Bold (思源黑体)
大小：52px
颜色：金黄色 (#FFD700) → 橙色 (#FFA500)
描边：5px 黑色
阴影：4px
位置：底部 85%
动画：淡入淡出 (400ms)
```

### 自定义样式
编辑 `doubao_watermark_asr.py` 中的 `generate_subtitle` 方法：
```python
# 修改颜色
PrimaryColour=&H00FFD700  # 金色
SecondaryColour=&H00FFA500  # 橙色

# 修改大小
Fontsize=56  # 更大字体

# 修改位置
MarginV=90  # 更靠下
```

---

## 📁 输出文件

```
output/
├── video_clean.mp4           # 去水印视频
├── video_sub.mp4             # 去水印 + 字幕 (最终)
├── temp/
│   ├── audio.wav             # 提取的音频
│   └── subtitle.ass          # ASS 字幕文件
└── video.srt                 # SRT 字幕 (可选)
```

---

## 🔧 技术细节

### 语音识别
- **模型:** FunASR paraformer-zh
- **VAD:** fsmn-vad (语音活动检测)
- **标点:** ct-punc (自动标点)
- **准确率:** 90%+ (标准普通话)

### 水印去除
- **检测:** 静态角落 + 跳跃式
- **修复:** OpenCV TELEA / LaMa AI
- **质量:** CRF 18 + 10bit

### 字幕烧录
- **引擎:** FFmpeg ass 滤镜
- **格式:** ASS v4.00+
- **效果:** 淡入淡出 + 缩放

---

## 🐛 故障排除

### Q: FunASR 下载模型失败
```bash
# 手动下载模型
pip3 install modelscope
python3 -c "from funasr import AutoModel; AutoModel(model='paraformer-zh')"
```

### Q: 识别不准确
- 确保音频清晰无噪音
- 视频原声人声音量足够
- 专有名词可能识别错误 (需人工校正)

### Q: 字幕烧录失败
```bash
# 检查 FFmpeg 是否支持 ass
ffmpeg -filters | grep ass
```

### Q: 内存不足
```bash
# 减小 batch_size
# 编辑代码：batch_size_s=150 (默认 300)
```

---

## 📈 性能数据

| 阶段 | 耗时 (10 秒视频) |
|------|-----------------|
| 音频提取 | 1-2 秒 |
| 水印去除 | 40-60 秒 |
| 语音识别 | 2-3 秒 |
| 字幕生成 | 1 秒 |
| 字幕烧录 | 5-10 秒 |
| **总计** | **50-75 秒** |

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **FunASR:** https://github.com/alibaba-damo-academy/FunASR
- **ModelScope:** https://www.modelscope.cn
- **ClawHub:** https://clawhub.ai/yun520-1/doubao-watermark-remover

---

**版本:** 3.0.0  
**更新日期:** 2026-03-21  
**作者:** yun520-1
