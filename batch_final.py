#!/usr/bin/env python3
"""
批量处理所有 QQ 视频 - 最终完美版
"""

import subprocess
from pathlib import Path
import sys

VIDEO_DIR = Path("/Users/apple/Library/Containers/com.tencent.qq/Data/Library/Application Support/QQ/nt_qq_8ca6de9b388036f721b5181229669f4f/nt_data/Video/2026-03/Ori")
OUTPUT_DIR = Path("/Users/apple/Desktop/Videos_No_Watermark/All_Final")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

videos = list(VIDEO_DIR.glob("*.mp4"))

print("=" * 70)
print("🎬 批量处理 - 最终完美版")
print("0-4 秒右下 + 3-7 秒左中 + 6-10 秒右上")
print("=" * 70)
print(f"\n📹 找到 {len(videos)} 个视频")
print(f"💾 输出：{OUTPUT_DIR}")

for i, video in enumerate(videos, 1):
    print(f"\n[{i}/{len(videos)}] {video.name}")
    
    output_path = OUTPUT_DIR / f"{video.stem}_final.mp4"
    
    cmd = [
        sys.executable,
        "/Users/apple/.jvs/.openclaw/workspace/video-watermark-remover/final_perfect.py",
        str(video),
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        if output_path.exists():
            size_mb = output_path.stat().st_size / 1024 / 1024
            print(f"  ✅ {size_mb:.1f} MB")
        else:
            print(f"  ⚠️ 文件未生成")
    else:
        print(f"  ❌ 失败")

print(f"\n🎉 完成！输出：{OUTPUT_DIR}")
print(f"💡 查看：open {OUTPUT_DIR}")
