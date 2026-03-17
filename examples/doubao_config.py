"""
豆包 AI 生成水印配置示例
"""

# 水印位置配置
DOUBAO_WATERMARK_CONFIG = [
    # 0-4 秒：右下角
    {"start_sec": 0, "end_sec": 4, "x": 510, "y": 1170, "w": 180, "h": 70, "name": "右下"},
    # 3-7 秒：左侧中间
    {"start_sec": 3, "end_sec": 7, "x": 20, "y": 600, "w": 170, "h": 60, "name": "左中"},
    # 6-10 秒：右上角
    {"start_sec": 6, "end_sec": 10, "x": 510, "y": 20, "w": 180, "h": 70, "name": "右上"},
]

# 使用说明
# 1. 修改 final_perfect.py 中的 user_regions 为上述配置
# 2. 运行：python final_perfect.py <输入视频> <输出视频>
