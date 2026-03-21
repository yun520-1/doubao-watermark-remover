#!/usr/bin/env python3
"""
为视频添加字幕 (独立工具)
支持：语音识别 + 网红字幕样式
"""

import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List

class SubtitleGenerator:
    """字幕生成器"""
    
    STYLES = {
        'douyin': {
            'font': 'ZCOOLKuaiLe',
            'fontsize': 50,
            'primary_color': '&H00FFFF00',
            'secondary_color': '&H0000FFFF',
            'outline_color': '&H00000000',
            'outline': 4,
            'shadow': 3,
            'margin_v': 80,
            'gradient': True,
            'animation': 'move(0, -15, 0, 0, 0.4)'
        },
        'kuaishou': {
            'font': 'SourceHanSansCN-Bold',
            'fontsize': 54,
            'primary_color': '&H00FF00FF',
            'secondary_color': '&H0000FFFF',
            'outline_color': '&H00000000',
            'outline': 5,
            'shadow': 4,
            'margin_v': 90,
            'gradient': True,
            'animation': 'fade(0,255,255,255,0,0,300,300)'
        },
        'movie': {
            'font': 'SourceHanSerifCN-Bold',
            'fontsize': 46,
            'primary_color': '&H00FFFFFF',
            'outline_color': '&H00000000',
            'outline': 2,
            'shadow': 3,
            'margin_v': 60,
            'animation': 'fade(0,255,255,255,0,0,500,500)'
        },
        'variety': {
            'font': 'ZCOOLKuaiLe',
            'fontsize': 58,
            'primary_color': '&H00FF1493',
            'secondary_color': '&H00FFD700',
            'outline_color': '&H00000000',
            'outline': 5,
            'shadow': 5,
            'margin_v': 100,
            'gradient': True,
            'animation': 'move(0, -25, 0, 0, 0.5)'
        },
        'colorful': {
            'font': 'ZCOOLKuaiLe',
            'fontsize': 52,
            'primary_color': '&H00FF6347',
            'secondary_color': '&H0032CD32',
            'outline_color': '&H00000000',
            'outline': 4,
            'shadow': 4,
            'margin_v': 85,
            'gradient': True,
            'animation': 'move(0, -20, 0, 0, 0.45)'
        }
    }
    
    @staticmethod
    def extract_audio(video_path: str, audio_path: str):
        """提取音频"""
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vn', '-acodec', 'pcm_s16le',
            '-ar', '16000', '-ac', '1',
            '-y', audio_path
        ]
        print(f"  🎵 提取音频...")
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  ✅ 音频：{audio_path}")
    
    @staticmethod
    def transcribe_audio(audio_path: str) -> List[Dict]:
        """语音识别"""
        try:
            import whisper
            print(f"  🎤 加载 Whisper 模型 (base)...")
            model = whisper.load_model("base")
            
            print(f"  🎤 识别语音中...")
            result = model.transcribe(audio_path, language='zh')
            
            segments = []
            for seg in result['segments']:
                segments.append({
                    'start': seg['start'],
                    'end': seg['end'],
                    'text': seg['text'].strip()
                })
            
            print(f"  ✅ 识别到 {len(segments)} 条字幕")
            return segments
        except Exception as e:
            print(f"  ❌ 语音识别失败：{e}")
            return []
    
    @staticmethod
    def generate_ass(segments: List[Dict], style_name: str, width: int, height: int) -> str:
        """生成 ASS 字幕"""
        style = SubtitleGenerator.STYLES.get(style_name, SubtitleGenerator.STYLES['douyin'])
        
        ass = f"""[Script Info]
Title: Subtitle
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{style['font']},{style['fontsize']},{style['primary_color']},&H000000FF,{style['outline_color']},&H00000000,0,0,0,0,100,100,0,0,1,{style['outline']},{style['shadow']},2,20,20,{style['margin_v']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        for seg in segments:
            start = SubtitleGenerator._fmt_time(seg['start'])
            end = SubtitleGenerator._fmt_time(seg['end'])
            text = seg['text'].replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}')
            ass += f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n"
        
        return ass
    
    @staticmethod
    def _fmt_time(seconds: float) -> str:
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
    parser = argparse.ArgumentParser(description='为视频添加字幕')
    parser.add_argument('video', help='输入视频')
    parser.add_argument('-o', '--output', help='输出目录', default='./output')
    parser.add_argument('--style', default='douyin', choices=['douyin', 'kuaishou', 'movie'])
    args = parser.parse_args()
    
    video_path = Path(args.video)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"📝 视频字幕生成器")
    print(f"{'='*60}")
    print(f"📁 输入：{video_path.name}")
    print(f"🎨 样式：{args.style}")
    
    # 临时文件
    temp_dir = output_dir / 'temp'
    temp_dir.mkdir(exist_ok=True)
    audio_path = temp_dir / 'audio.wav'
    ass_path = temp_dir / 'subtitle.ass'
    
    # 1. 提取音频
    SubtitleGenerator.extract_audio(str(video_path), str(audio_path))
    
    # 2. 语音识别
    segments = SubtitleGenerator.transcribe_audio(str(audio_path))
    
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
    ass_content = SubtitleGenerator.generate_ass(segments, args.style, width, height)
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(ass_content)
    print(f"  ✅ 字幕：{ass_path}")
    
    # 5. 烧录字幕
    output_video = output_dir / f"{video_path.stem}_sub.mp4"
    SubtitleGenerator.burn_subtitle(str(video_path), str(ass_path), str(output_video))
    
    # 6. 保存 SRT
    srt_path = output_dir / f"{video_path.stem}.srt"
    srt = ""
    for i, seg in enumerate(segments, 1):
        start = SubtitleGenerator._fmt_srt(seg['start'])
        end = SubtitleGenerator._fmt_srt(seg['end'])
        srt += f"{i}\n{start} --> {end}\n{seg['text']}\n\n"
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(srt)
    print(f"  ✅ SRT: {srt_path}")
    
    print(f"\n{'='*60}")
    print(f"✅ 完成！")
    print(f"{'='*60}\n")


    @staticmethod
def _fmt_srt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


if __name__ == '__main__':
    main()
