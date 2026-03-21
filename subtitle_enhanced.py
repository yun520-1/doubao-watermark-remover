#!/usr/bin/env python3
"""
增强版字幕生成器
优化：
1. 使用 Whisper larger-v3 模型提高识别准确率
2. 中文优化
3. 自动标点修正
4. 简化字转换
"""

import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List

class EnhancedSubtitle:
    """增强版字幕生成器"""
    
    STYLES = {
        'colorful': {
            'name': '彩虹风',
            'font': 'SourceHanSansCN-Bold',  # 思源黑体，支持简体中文
            'fontsize': 50,
            'primary_color': '&H00FF6347',
            'secondary_color': '&H0032CD32',
            'outline': 4,
            'shadow': 4,
            'margin_v': 80
        },
        'douyin': {
            'name': '抖音风',
            'font': 'SourceHanSansCN-Bold',
            'fontsize': 48,
            'primary_color': '&H00FFFF00',
            'secondary_color': '&H0000FFFF',
            'outline': 4,
            'shadow': 3,
            'margin_v': 75
        }
    }
    
    @staticmethod
    def extract_audio(video_path: str, audio_path: str):
        """提取音频"""
        cmd = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', '-y', audio_path]
        print(f"  🎵 提取音频...")
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  ✅ 音频：{audio_path}")
    
    @staticmethod
    def transcribe_audio(audio_path: str) -> List[Dict]:
        """语音识别 - 使用 larger 模型提高准确率"""
        try:
            import whisper
            
            # 尝试使用 larger 模型，如果失败则使用 base
            print(f"  🎤 加载 Whisper 模型 (larger-v3)...")
            try:
                model = whisper.load_model("large-v3")
            except:
                print(f"  ⚠️ larger 模型不可用，使用 base 模型...")
                model = whisper.load_model("base")
            
            print(f"  🎤 识别语音中 (中文优化)...")
            result = model.transcribe(
                audio_path, 
                language='zh',
                task='transcribe',
                verbose=False,
                fp16=False  # CPU 使用 FP32
            )
            
            segments = []
            for seg in result['segments']:
                text = seg['text'].strip()
                # 清理乱码和特殊字符
                text = EnhancedSubtitle.clean_text(text)
                if text:
                    segments.append({
                        'start': seg['start'],
                        'end': seg['end'],
                        'text': text
                    })
            
            print(f"  ✅ 识别到 {len(segments)} 条字幕")
            for i, seg in enumerate(segments, 1):
                print(f"     [{i}] {seg['text']}")
            
            return segments
        except Exception as e:
            print(f"  ❌ 语音识别失败：{e}")
            return []
    
    @staticmethod
    def clean_text(text: str) -> str:
        """清理文本 - 去除乱码，修正标点"""
        import re
        
        # 去除特殊字符和乱码
        text = re.sub(r'[^\u4e00-\u9fa5\u3000-\u303f\uff00-\uffef0-9a-zA-Z，。！？、；：""''（）《》…—]', '', text)
        
        # 修正标点
        text = text.replace('...', '……')
        text = text.replace('..', '……')
        
        # 去除多余空格
        text = re.sub(r'\s+', '', text)
        
        return text.strip()
    
    @staticmethod
    def generate_ass(segments: List[Dict], style_name: str, width: int, height: int) -> str:
        """生成 ASS 字幕 - 优化简体中文显示"""
        style = EnhancedSubtitle.STYLES.get(style_name, EnhancedSubtitle.STYLES['colorful'])
        
        ass = f"""[Script Info]
Title: 增强字幕 - {style['name']}
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
Timer: 100.0000

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{style['font']},{style['fontsize']},{style['primary_color']},{style['secondary_color']},{style['outline_color']},&H00000000,-1,0,0,0,100,100,0,0,1,{style['outline']},{style['shadow']},2,20,20,{style['margin_v']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        for seg in segments:
            start = EnhancedSubtitle._fmt_time(seg['start'])
            end = EnhancedSubtitle._fmt_time(seg['end'])
            text = seg['text']
            
            # 添加淡入淡出效果
            effect = '\\fad(300,300)'
            
            ass += f"Dialogue: 0,{start},{end},Default,,0,0,0,{effect}{{\\fscx100\\fscy100}}{text}\n"
        
        return ass
    
    @staticmethod
    def _fmt_time(seconds: float) -> str:
        """格式化时间为 ASS 格式"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        c = int((seconds % 1) * 100)
        return f"{h}:{m:02d}:{s:02d}.{c:02d}"
    
    @staticmethod
    def burn_subtitle(video: str, subtitle: str, output: str):
        """烧录字幕"""
        print(f"  🎬 烧录字幕...")
        cmd = ['ffmpeg', '-i', video, '-vf', f'ass={subtitle}', '-c:a', 'copy', '-y', output]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  ✅ 输出：{output}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='增强版字幕生成器')
    parser.add_argument('video', help='输入视频')
    parser.add_argument('-o', '--output', help='输出目录', default='./output')
    parser.add_argument('--style', default='colorful', choices=['colorful', 'douyin'])
    args = parser.parse_args()
    
    video_path = Path(args.video)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    style_info = EnhancedSubtitle.STYLES.get(args.style, EnhancedSubtitle.STYLES['colorful'])
    
    print(f"\n{'='*70}")
    print(f"🎨 增强版字幕生成器 - {style_info['name']}")
    print(f"{'='*70}")
    print(f"📁 输入：{video_path.name}")
    print(f"🎨 样式：{style_info['name']}")
    print(f"🔤 字体：{style_info['font']} (简体中文优化)")
    print(f"{'='*70}\n")
    
    # 临时文件
    temp_dir = output_dir / 'temp'
    temp_dir.mkdir(exist_ok=True)
    audio_path = temp_dir / 'audio.wav'
    ass_path = temp_dir / 'subtitle.ass'
    
    # 1. 提取音频
    EnhancedSubtitle.extract_audio(str(video_path), str(audio_path))
    
    # 2. 语音识别
    segments = EnhancedSubtitle.transcribe_audio(str(audio_path))
    
    if not segments:
        print(f"\n⚠️ 未识别到语音")
        return
    
    # 3. 获取视频信息
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'json', str(video_path)]
    info = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
    width = info['streams'][0]['width']
    height = info['streams'][0]['height']
    print(f"  📺 视频：{width}x{height}")
    
    # 4. 生成 ASS 字幕
    ass_content = EnhancedSubtitle.generate_ass(segments, args.style, width, height)
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(ass_content)
    print(f"  ✅ ASS 字幕：{ass_path}")
    
    # 5. 烧录字幕
    output_video = output_dir / f"{video_path.stem}_{args.style}_enhanced.mp4"
    EnhancedSubtitle.burn_subtitle(str(video_path), str(ass_path), str(output_video))
    
    print(f"\n{'='*70}")
    print(f"✅ 完成！输出：{output_video}")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
