#!/usr/bin/env python3
"""
豆包水印去除 v2.0 - 增强版
功能：
- 水印去除
- 语音识别 (ASR)
- 自动生成网红风格字幕
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

class SubtitleGenerator:
    """字幕生成器 - 支持多种网红风格"""
    
    STYLES = {
        'douyin': {
            'font': 'ZCOOLKuaiLe',
            'fontsize': 48,
            'primary_color': '&H00FFD700',
            'secondary_color': '&H00FFA500',
            'outline_color': '&H00FFFFFF',
            'back_color': '&H00000000',
            'outline': 3,
            'shadow': 2,
            'alignment': 2,
            'margin_v': 50,
            'effect': 'move(0, -10, 0, 0, 0.3)',
            'gradient': True
        },
        'kuaishou': {
            'font': 'SourceHanSansCN',
            'fontsize': 52,
            'primary_color': '&H00FFFFFF',
            'secondary_color': '&H00FFFFFF',
            'outline_color': '&H00000000',
            'back_color': '&H00000000',
            'outline': 4,
            'shadow': 0,
            'alignment': 2,
            'margin_v': 60,
            'effect': 'fade(0,255,255,255,0,0,200,200)'
        },
        'movie': {
            'font': 'SourceHanSerifCN',
            'fontsize': 42,
            'primary_color': '&H00FFFFFF',
            'secondary_color': '&H00FFFFFF',
            'outline_color': '&H00000000',
            'back_color': '&H00000000',
            'outline': 1,
            'shadow': 2,
            'alignment': 2,
            'margin_v': 40,
            'effect': 'fade(0,255,255,255,0,0,500,500)'
        },
        'variety': {
            'font': 'ZCOOLKuaiLe',
            'fontsize': 56,
            'primary_color': '&H00FF69B4',
            'secondary_color': '&H00FFD700',
            'outline_color': '&H00000000',
            'back_color': '&H00000000',
            'outline': 3,
            'shadow': 3,
            'alignment': 2,
            'margin_v': 80,
            'effect': 'move(0, -20, 0, 0, 0.5)',
            'gradient': True
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
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  ✅ 音频已提取：{audio_path}")
    
    @staticmethod
    def transcribe_audio(audio_path: str) -> List[Dict]:
        """语音识别 - 使用 Whisper"""
        try:
            import whisper
            print("  🎤 加载 Whisper 模型...")
            model = whisper.load_model("base")
            
            print("  🎤 识别语音中...")
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
        except ImportError:
            print("  ⚠️ Whisper 未安装，使用备用方案...")
            return []
        except Exception as e:
            print(f"  ❌ 语音识别失败：{e}")
            return []
    
    @staticmethod
    def generate_ass_subtitle(segments: List[Dict], style_name: str = 'douyin', 
                              video_width: int = 1080, video_height: int = 1920) -> str:
        """生成 ASS 格式字幕"""
        style = SubtitleGenerator.STYLES.get(style_name, SubtitleGenerator.STYLES['douyin'])
        
        ass_content = f"""[Script Info]
Title: Doubao Watermark Remover Subtitle
ScriptType: v4.00+
PlayResX: {video_width}
PlayResY: {video_height}
Timer: 100.0000

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{style['font']},{style['fontsize']},{style['primary_color']},{style['secondary_color']},{style['outline_color']},{style['back_color']},0,0,0,0,100,100,0,0,1,{style['outline']},{style['shadow']},{style['alignment']},20,20,{style['margin_v']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        
        for seg in segments:
            start = SubtitleGenerator._format_time(seg['start'])
            end = SubtitleGenerator._format_time(seg['end'])
            text = seg['text'].replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}')
            
            effect = style.get('effect', '')
            
            ass_content += f"Dialogue: 0,{start},{end},Default,,0,0,0,{effect},{text}\n"
        
        return ass_content
    
    @staticmethod
    def _format_time(seconds: float) -> str:
        """格式化时间为 ASS 格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centis = int((seconds % 1) * 100)
        return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"
    
    @staticmethod
    def generate_srt_subtitle(segments: List[Dict]) -> str:
        """生成 SRT 格式字幕"""
        srt_content = ""
        for i, seg in enumerate(segments, 1):
            start = SubtitleGenerator._format_srt_time(seg['start'])
            end = SubtitleGenerator._format_srt_time(seg['end'])
            text = seg['text']
            srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"
        return srt_content
    
    @staticmethod
    def _format_srt_time(seconds: float) -> str:
        """格式化时间为 SRT 格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    @staticmethod
    def burn_subtitles(video_path: str, subtitle_path: str, output_path: str, 
                       style: str = 'douyin'):
        """烧录字幕到视频"""
        # 使用 FFmpeg 的 ass 滤镜
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vf', f"ass={subtitle_path}",
            '-c:a', 'copy',
            '-y', output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  ✅ 字幕已烧录：{output_path}")


class DoubaoWatermarkRemoverV2:
    """豆包水印去除 v2.0 - 增强版"""
    
    def __init__(self, input_path: str, output_dir: str):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 临时文件
        self.temp_dir = self.output_dir / 'temp'
        self.temp_dir.mkdir(exist_ok=True)
        
        # 输出文件
        self.output_clean = self.output_dir / f"{self.input_path.stem}_clean.mp4"
        self.output_sub = self.output_dir / f"{self.input_path.stem}_clean_sub.mp4"
        self.audio_path = self.temp_dir / 'audio.wav'
        self.ass_path = self.temp_dir / 'subtitle.ass'
        self.srt_path = self.temp_dir / 'subtitle.srt'
    
    def process(self, add_subtitles: bool = True, subtitle_style: str = 'douyin'):
        """完整处理流程"""
        print(f"\n{'='*70}")
        print(f"🎬 豆包水印去除 v2.0 - 增强版")
        print(f"{'='*70}")
        print(f"📁 输入：{self.input_path}")
        print(f"📂 输出：{self.output_dir}")
        
        # 步骤 1: 水印去除
        print(f"\n1️⃣ 水印去除...")
        self.remove_watermark()
        
        # 步骤 2: 语音识别和字幕生成
        if add_subtitles:
            print(f"\n2️⃣ 生成字幕 (样式：{subtitle_style})...")
            self.generate_subtitles(subtitle_style)
            
            print(f"\n3️⃣ 烧录字幕...")
            self.burn_subtitles()
        else:
            print(f"\n2️⃣ 跳过字幕生成")
        
        # 清理临时文件
        # self.cleanup()
        
        print(f"\n{'='*70}")
        print(f"✅ 处理完成！")
        print(f"{'='*70}\n")
    
    def remove_watermark(self):
        """水印去除 - 调用现有脚本"""
        from final_perfect_v3_ultra import process_video
        
        success = process_video(str(self.input_path), str(self.output_clean))
        if not success:
            print(f"  ❌ 水印去除失败")
            sys.exit(1)
    
    def generate_subtitles(self, style: str):
        """生成字幕"""
        # 提取音频
        SubtitleGenerator.extract_audio(str(self.output_clean), str(self.audio_path))
        
        # 语音识别
        segments = SubtitleGenerator.transcribe_audio(str(self.audio_path))
        
        if not segments:
            print(f"  ⚠️ 未识别到语音，跳过字幕生成")
            return
        
        # 获取视频信息
        video_info = self.get_video_info()
        
        # 生成 ASS 字幕
        ass_content = SubtitleGenerator.generate_ass_subtitle(
            segments, style, 
            video_info['width'], 
            video_info['height']
        )
        
        with open(self.ass_path, 'w', encoding='utf-8') as f:
            f.write(ass_content)
        print(f"  ✅ ASS 字幕已生成：{self.ass_path}")
        
        # 生成 SRT 字幕
        srt_content = SubtitleGenerator.generate_srt_subtitle(segments)
        with open(self.srt_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        print(f"  ✅ SRT 字幕已生成：{self.srt_path}")
    
    def burn_subtitles(self):
        """烧录字幕"""
        SubtitleGenerator.burn_subtitles(
            str(self.output_clean),
            str(self.ass_path),
            str(self.output_sub),
        )
    
    def get_video_info(self) -> Dict:
        """获取视频信息"""
        cmd = [
            'ffprobe', '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'json',
            str(self.output_clean)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        info = json.loads(result.stdout)
        stream = info['streams'][0]
        return {
            'width': stream['width'],
            'height': stream['height']
        }
    
    def cleanup(self):
        """清理临时文件"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print(f"  🧹 临时文件已清理")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='豆包水印去除 v2.0 - 增强版')
    parser.add_argument('input', help='输入视频文件')
    parser.add_argument('-o', '--output', help='输出目录', default='./output')
    parser.add_argument('--no-subtitles', action='store_true', help='不生成字幕')
    parser.add_argument('--style', default='douyin', 
                       choices=['douyin', 'kuaishou', 'movie', 'variety'],
                       help='字幕样式 (默认：douyin)')
    
    args = parser.parse_args()
    
    remover = DoubaoWatermarkRemoverV2(args.input, args.output)
    remover.process(
        add_subtitles=not args.no_subtitles,
        subtitle_style=args.style
    )


if __name__ == '__main__':
    main()
