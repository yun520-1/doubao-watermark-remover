#!/usr/bin/env python3
"""
批量处理视频 - 水印去除 + 自动生成字幕
"""

import sys
import os
from pathlib import Path

# 添加技能目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from final_perfect_v4_with_subtitles import DoubaoWatermarkRemoverV2

def batch_process(input_dir: str, output_dir: str, subtitle_style: str = 'douyin'):
    """批量处理视频"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    videos = list(input_path.glob("*.mp4"))
    
    if not videos:
        print(f"❌ 未找到视频文件：{input_dir}")
        return
    
    print(f"\n{'='*70}")
    print(f"🎬 批量处理视频 - 水印去除 + 自动生成字幕")
    print(f"{'='*70}")
    print(f"📁 输入：{input_dir}")
    print(f"📂 输出：{output_dir}")
    print(f"🎨 字幕样式：{subtitle_style}")
    print(f"📹 视频数量：{len(videos)}")
    print(f"{'='*70}\n")
    
    for i, video in enumerate(videos, 1):
        print(f"\n{'='*70}")
        print(f"[{i}/{len(videos)}] {video.name}")
        print(f"{'='*70}")
        
        output_dir_i = output_path / video.stem
        output_dir_i.mkdir(parents=True, exist_ok=True)
        
        remover = DoubaoWatermarkRemoverV2(str(video), str(output_dir_i))
        remover.process(
            add_subtitles=True,
            subtitle_style=subtitle_style
        )
    
    print(f"\n{'='*70}")
    print(f"✅ 批量处理完成！")
    print(f"📂 输出目录：{output_path}")
    print(f"{'='*70}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='批量处理视频 - 水印去除 + 字幕')
    parser.add_argument('input_dir', help='输入视频目录')
    parser.add_argument('output_dir', help='输出目录')
    parser.add_argument('--style', default='douyin',
                       choices=['douyin', 'kuaishou', 'movie', 'variety'],
                       help='字幕样式 (默认：douyin)')
    
    args = parser.parse_args()
    
    batch_process(args.input_dir, args.output_dir, args.style)


if __name__ == '__main__':
    main()
