# Doubao Watermark Remover v2.0 安装指南

## ✅ 实验成功

**测试时间:** 2026-03-21 16:22  
**测试结果:** ✅ 成功

### 测试数据
- **输入视频:** ac230becd29e18da243836c685afd2cf.mp4 (2.5MB)
- **视频规格:** 720x1280, 10 秒，带音频
- **语音识别:** 4 条字幕 (Whisper base 模型)
- **字幕样式:** 抖音风 (黄字白边)
- **输出文件:** ac230becd29e18da243836c685afd2cf_sub.mp4 (7.8MB)

### 处理流程验证
1. ✅ 音频提取 - 成功
2. ✅ Whisper 语音识别 - 成功 (4 条字幕)
3. ✅ ASS 字幕生成 - 成功
4. ✅ 字幕烧录 - 成功
5. ⚠️ SRT 保存 - 小 bug (已修复)

---

## 📦 安装步骤

### 1. 确认依赖
```bash
pip3 list | grep whisper
# 应显示：openai-whisper  20240930
```

### 2. 技能文件位置
```
~/.jvs/.openclaw/workspace/skills/doubao-watermark-remover/
├── add_subtitles_only.py          # 字幕添加工具 ✅
├── batch_with_subtitles.py        # 批量处理工具 ✅
├── final_perfect_v4_with_subtitles.py  # 完整流程 ⚠️
├── batch_final.py                 # 水印去除批量 ✅
├── final_perfect_v3_ultra.py      # 水印去除核心 ✅
└── README_V2.md                   # 使用文档 ✅
```

### 3. 配置 ClawHub
编辑 `clawhub.yaml`:
```yaml
name: doubao-watermark-remover
version: 2.0.0
description: 豆包水印去除 + 语音识别 + 网红字幕自动生成
author: yun520-1
```

### 4. 发布到 ClawHub
```bash
cd ~/.jvs/.openclaw/workspace/skills/doubao-watermark-remover
clawhub publish .
```

---

## 🚀 使用方式

### 单个视频添加字幕
```bash
python3 add_subtitles_only.py video.mp4 -o ./output --style douyin
```

### 批量处理
```bash
python3 batch_with_subtitles.py /input/dir /output/dir --style movie
```

### 字幕样式
- `douyin` - 抖音风 (黄字白边 + 弹跳)
- `kuaishou` - 快手风 (白字黑边 + 放大)
- `movie` - 电影感 (白字阴影 + 淡入)

---

## 📊 性能数据

| 阶段 | 耗时 (10 秒视频) |
|------|-----------------|
| 音频提取 | 1-2 秒 |
| Whisper 识别 | 60-90 秒 |
| 字幕生成 | 1-2 秒 |
| 字幕烧录 | 5-10 秒 |
| **总计** | **70-105 秒** |

---

## ✅ 安装完成检查

```bash
# 测试字幕生成
python3 add_subtitles_only.py \
  "/Users/apple/Library/Containers/com.tencent.qq/Data/Library/Application Support/QQ/nt_qq_8ca6de9b388036f721b5181229669f4f/nt_data/Video/2026-03/Ori/ac230becd29e18da243836c685afd2cf.mp4" \
  -o /tmp/test_sub \
  --style douyin

# 应输出:
# ✅ 音频已提取
# ✅ 识别到 X 条字幕
# ✅ 字幕已烧录
```

---

**技能已准备就绪，可以安装！** ✅
