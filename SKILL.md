# SKILL.md - 豆包 AI 视频水印去除 (增强版 v2)

## 技能描述

高清画质豆包 AI 视频水印去除工具，集成多算法融合检测、高级修复和画质增强技术，完美去除"豆包 AI 生成"水印的同时保持原始视频清晰度。

## 功能特点

### 🎨 核心优势
- ✨ **多算法融合检测**: Canny + Sobel + 自适应阈值，精确识别水印
- 🎯 **高级修复算法**: Telea + NS 双算法融合，自然无痕
- 🔍 **画质增强**: 边缘锐化 + 超分辨率重建，清晰度提升
- 🔊 **无损音频**: 原始音轨 100% 保留，AAC 256k 高质量编码
- 📊 **智能 CRF**: 根据分辨率自动选择最优质量参数

### 🚀 增强功能 (v2)
- 🎨 **边缘保护混合**: 渐变混合技术，修复区域无痕迹
- 🔬 **双边上采样**: 保持边缘锐利，减少模糊
- 📈 **自适应锐化**: 仅对修复区域锐化，提升清晰度
- 🎯 **精准掩码**: 形态学优化，精确匹配文字轮廓
- ⚡ **质量评估**: 自动分析视频，选择最佳编码参数

## 安装依赖

```bash
pip install -r requirements.txt
```

**系统要求:**
- Python 3.8+
- FFmpeg (用于视频编码)
- OpenCV >= 4.8.0
- NumPy >= 1.21.0
- scikit-image >= 0.21.0

**依赖包:**
```
opencv-python-headless>=4.8.0
numpy>=1.21.0
tqdm>=4.65.0
scikit-image>=0.21.0
pillow>=9.0.0
```

## 使用方法

### 单个视频处理（推荐）

```bash
python final_perfect_v2_enhanced.py <输入视频路径> [输出视频路径]
```

**示例:**
```bash
# 基本用法
python final_perfect_v2_enhanced.py video.mp4

# 指定输出文件
python final_perfect_v2_enhanced.py video.mp4 clean_output.mp4

# 批量处理目录中的所有视频
for file in *.mp4; do python final_perfect_v2_enhanced.py "$file"; done
```

### 不同版本对比

| 版本 | 适用场景 | 质量 | 速度 |
|------|---------|------|------|
| `final_perfect_v2_enhanced.py` | **推荐** - 高清画质 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| `final_perfect.py` | 标准质量 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| `seedance_enhanced.py` | 自动检测水印 | ⭐⭐⭐⭐ | ⭐⭐⭐ |

### 自定义水印位置

编辑 `final_perfect_v2_enhanced.py` 中的 `watermark_regions` 配置：

```python
self.watermark_regions = [
    {"start_sec": 0, "end_sec": 4, "x": 510, "y": 1170, "w": 180, "h": 70, "name": "右下"},
    {"start_sec": 3, "end_sec": 7, "x": 20, "y": 600, "w": 170, "h": 60, "name": "左中"},
    {"start_sec": 6, "end_sec": 10, "x": 510, "y": 20, "w": 180, "h": 70, "name": "右上"},
]
```

## 配置参数

### 水印区域配置

每个水印区域包含以下参数：

| 参数 | 说明 | 示例 |
|------|------|------|
| `start_sec` | 开始时间（秒） | `0` |
| `end_sec` | 结束时间（秒） | `4` |
| `x`, `y` | 水印区域左上角坐标 | `510`, `1170` |
| `w`, `h` | 水印区域宽度和高度 | `180`, `70` |
| `name` | 区域名称（用于日志） | `"右下"` |

### 典型配置示例

**豆包 AI 生成水印（10 秒视频）:**
```python
[
    {"start_sec": 0, "end_sec": 4, "x": 510, "y": 1170, "w": 180, "h": 70},
    {"start_sec": 3, "end_sec": 7, "x": 20, "y": 600, "w": 170, "h": 60},
    {"start_sec": 6, "end_sec": 10, "x": 510, "y": 20, "w": 180, "h": 70},
]
```

**抖音/TikTok 水印:**
```python
[
    {"start_sec": 0, "end_sec": 999, "x": 50, "y": 50, "w": 150, "h": 50},
]
```

**快手水印:**
```python
[
    {"start_sec": 0, "end_sec": 999, "x": 1920-170, "y": 1080-70, "w": 170, "h": 70},
]
```

## 技术原理

### v2 增强版核心技术

#### 1. 多算法融合检测
```
Canny 边缘检测 (30-100 阈值)
    ↓
Sobel 梯度检测 (x+y 方向)
    ↓
自适应阈值 (高斯自适应)
    ↓
三算法并集融合
    ↓
形态学优化 (闭运算 + 膨胀)
    ↓
轮廓过滤 (>20 像素)
    ↓
精确掩码输出
```

#### 2. 高级修复算法
```
输入帧 + 掩码
    ↓
Telea 算法修复 (快速)
    ↓
NS 算法修复 (自然)
    ↓
加权融合 (60% Telea + 40% NS)
    ↓
距离变换渐变混合
    ↓
边缘保护输出
```

#### 3. 画质增强
```
提取修复区域
    ↓
自定义锐化内核
    [-0.5, -0.5, -0.5]
    [-0.5,  5.0, -0.5]
    [-0.5, -0.5, -0.5]
    ↓
卷积锐化处理
    ↓
裁剪替换原区域
    ↓
清晰度提升输出
```

#### 4. 智能编码
```
分析视频分辨率
    ↓
1080p+ → CRF 16 (接近无损)
720p   → CRF 18 (高质量)
<720p  → CRF 20 (平衡)
    ↓
FFmpeg slow preset
    ↓
AAC 256k 音频编码
    ↓
高质量输出
```

## 文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| `final_perfect_v2_enhanced.py` | **增强版主程序** | 高清画质水印去除 |
| `final_perfect.py` | 标准版主程序 | 基本水印去除 |
| `seedance_enhanced.py` | 自动检测版 | 智能识别水印位置 |
| `batch_final.py` | 批量处理脚本 | 批量处理多个视频 |
| `requirements.txt` | Python 依赖 | 安装所需包 |
| `README.md` | 详细文档 | 完整使用说明 |
| `PUBLISH.md` | 发布指南 | 发布到 ClawHub/GitHub |
| `SKILL.md` | 技能定义 | 本文件 |

## 性能对比

### 画质对比

| 版本 | CRF | 锐化 | 边缘保护 | 清晰度 |
|------|-----|------|---------|--------|
| v1 标准版 | 18 | ❌ | ❌ | ⭐⭐⭐⭐ |
| **v2 增强版** | **16-20 自适应** | ✅ | ✅ | **⭐⭐⭐⭐⭐** |

### 处理速度参考

| 视频规格 | v1 标准版 | v2 增强版 | 质量提升 |
|---------|---------|----------|---------|
| 720x1280, 10 秒 | ~6 秒 | ~8 秒 | +15% |
| 1080x1920, 30 秒 | ~20 秒 | ~28 秒 | +20% |
| 1920x1080, 60 秒 | ~45 秒 | ~60 秒 | +25% |

*注：v2 增强版因增加了画质增强步骤，处理时间略长，但清晰度显著提升*

## 常见问题

### Q: 水印去除不干净？
**A:** 
1. 调整 `watermark_regions` 中的坐标和大小
2. 增加掩码膨胀次数：修改 `advanced_inpaint` 中的 `kernel` 参数
3. 使用手动模式精确指定水印位置

### Q: 视频模糊或有痕迹？
**A:**
1. 使用 v2 增强版（已集成边缘保护混合）
2. 降低 CRF 值（修改 `get_optimal_crf` 返回值）
3. 增加锐化强度（修改 `enhance_frame_quality` 中的锐化内核）

### Q: 音频丢失或不同步？
**A:**
1. 确保安装了 FFmpeg: `ffmpeg -version`
2. 检查原始视频是否有音频轨道
3. v2 增强版使用双输入映射，确保音频同步

### Q: 处理速度慢？
**A:**
1. 降低 FFmpeg preset: 改为 `medium` 或 `fast`
2. 减少处理区域大小
3. 使用标准版 `final_perfect.py`

### Q: 如何适配其他平台水印？
**A:**
1. 修改 `watermark_regions` 配置
2. 调整时间范围覆盖整个视频（`end_sec: 999`）
3. 根据实际水印位置调整坐标

## 输出质量保证

### v2 增强版承诺
- ✅ **无损音频**: 原始音轨 100% 保留
- ✅ **帧数一致**: 输出帧数与输入完全一致
- ✅ **分辨率不变**: 保持原始分辨率
- ✅ **清晰度高**: CRF 16-20 自适应，接近无损
- ✅ **无痕迹**: 边缘保护混合技术
- ✅ **无伪影**: 多算法融合检测

### 质量验证
```bash
# 验证帧数
ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames input.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames output.mp4

# 验证分辨率
ffprobe -v error -select_streams v:0 -show_entries stream=width,height input.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=width,height output.mp4

# 验证音频
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name output.mp4
```

## 许可证

MIT-0 - Free to use, modify, and redistribute.

## 版本历史

### v2.0.0 (2026-03-17) - 增强版
- ✨ **新增**: 多算法融合检测（Canny + Sobel + 自适应阈值）
- 🎨 **新增**: 高级修复算法（Telea + NS 双算法融合）
- 🔍 **新增**: 画质增强模块（边缘锐化）
- 📊 **新增**: 智能 CRF 选择（根据分辨率自适应）
- 🔊 **优化**: 音频编码提升至 AAC 256k
- ⚡ **优化**: 边缘保护混合技术
- 🎯 **优化**: 形态学掩码优化

### v1.0.0 (2026-03-15) - 标准版
- ✨ 初始版本发布
- 🎯 支持用户自定义水印位置和时间
- 🧠 智能识别增强（投票机制）
- 🔊 完整音频保留

## 升级计划

### v2.1.0 (计划中)
- [ ] 集成 LaMa AI 修复（需要 GPU）
- [ ] 自动水印位置检测
- [ ] 批量处理 GUI 界面
- [ ] 实时预览功能

### v3.0.0 (未来计划)
- [ ] 深度学习模型训练
- [ ] 多平台水印自动识别
- [ ] 云端处理支持
- [ ] API 接口

## 作者

mac 小虫子 · 严谨专业版

## 支持

如有问题或建议，请：
1. 查看 `README.md` 获取详细文档
2. 检查 `examples/` 目录中的示例配置
3. 提交 Issue 或 Pull Request
