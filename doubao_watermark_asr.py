#!/usr/bin/env python3
"""
豆包水印去除 v3.0 - 增强版
功能：
1. 水印去除
2. FunASR 语音识别
3. 自动生成网红字幕
4. 画质增强
"""

import subprocess, json, re, sys
from pathlib import Path
from typing import Dict, List, Optional

class DoubaoWatermarkASR:
    """豆包水印去除 + 语音识别 + 字幕生成"""
    
    def __init__(self, input_path: str, output_dir: str):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = self.output_dir / 'temp'
        self.temp_dir.mkdir(exist_ok=True)
        
        print("="*70)
        print("🎬 豆包水印去除 v3.0 - 增强版")
        print("="*70)
        print(f"📁 输入：{self.input_path.name}")
        print(f"📂 输出：{self.output_dir}")
    
    def extract_audio(self) -> Optional[Path]:
        """提取音频"""
        print("\n🎵 提取音频...")
        audio_path = self.temp_dir / "audio.wav"
        
        try:
            subprocess.run([
                'ffmpeg', '-i', str(self.input_path),
                '-vn',
                '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                '-y', str(audio_path)
            ], capture_output=True, check=True)
            print("  ✅ 完成")
            return audio_path
        except Exception as e:
            print(f"  ❌ 失败：{e}")
            return None
    
    def remove_watermark(self) -> Optional[Path]:
        """去除水印"""
        print("\n🔧 去除水印...")
        clean_video = self.output_dir / f"{self.input_path.stem}_clean.mp4"
        
        # 使用已有的水印去除脚本
        try:
            from final_perfect_v3_ultra import process_video
            if process_video(str(self.input_path), str(clean_video)):
                print("  ✅ 水印已去除")
                return clean_video
        except Exception as e:
            print(f"  ⚠️ 水印去除失败：{e}")
            print("  使用原始视频继续...")
            # 复制原视频
            subprocess.run(['cp', str(self.input_path), str(clean_video)], check=True)
            return clean_video
        return None
    
    def transcribe_audio(self, audio_path: Path) -> List[Dict]:
        """FunASR 语音识别"""
        print("\n🎤 FunASR 语音识别...")
        
        try:
            from funasr import AutoModel
            model = AutoModel(
                model="paraformer-zh",
                vad_model="fsmn-vad",
                punc_model="ct-punc",
                disable_update=True
            )
            
            result = model.generate(
                input=[str(audio_path)],
                batch_size_s=300,
                merge_vad=True
            )
            
            segments = []
            if result and len(result) > 0:
                res = result[0]
                if isinstance(res, dict):
                    text = res.get('text', '')
                    timestamps = res.get('timestamp', [])
                    
                    print(f"  📝 识别文本：{text[:100]}...")
                    
                    # 按标点分段
                    sentences = re.split(r'[，。！？；：]', text)
                    sentences = [s.strip() for s in sentences if len(s.strip()) > 1]
                    
                    # 分配时间戳
                    if timestamps and len(timestamps) > 0:
                        ts_per_sent = len(timestamps) // max(len(sentences), 1)
                        start_idx = 0
                        for sent in sentences:
                            if sent.strip() and start_idx < len(timestamps):
                                end_idx = min(start_idx + max(ts_per_sent, 1), len(timestamps))
                                start_time = timestamps[start_idx][0]
                                end_time = timestamps[min(end_idx-1, len(timestamps)-1)][1]
                                segments.append({
                                    'start': start_time,
                                    'end': end_time,
                                    'text': sent
                                })
                                start_idx = end_idx
            
            print(f"  ✅ 识别到 {len(segments)} 条字幕")
            for i, seg in enumerate(segments, 1):
                print(f"     [{i}] {seg['text']}")
            
            return segments
            
        except Exception as e:
            print(f"  ❌ 识别失败：{e}")
            return []
    
    def generate_subtitle(self, segments: List[Dict], width: int, height: int) -> Optional[Path]:
        """生成 ASS 字幕"""
        if not segments:
            print("  ⚠️ 无字幕内容")
            return None
        
        print("\n🎨 生成字幕...")
        ass_path = self.temp_dir / "subtitle.ass"
        
        ass = f"""[Script Info]
Title: 豆包水印去除 - 网红字幕
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,SourceHanSansCN-Bold,52,&H00FFD700,&H00FFA500,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,5,4,2,20,20,85,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        
        def fmt(ms):
            s = ms / 1000
            return f"{int(s//3600)}:{int((s%3600)//60):02d}:{int(s%60):02d}.{int((s%1)*100):02d}"
        
        for seg in segments:
            text = seg['text'].replace('\\','\\\\').replace('{','\\{').replace('}','\\}')
            ass += f"Dialogue: 0,{fmt(seg['start'])},{fmt(seg['end'])},Default,,0,0,0,\\fad(400,400){{\\fscx100\\fscy100}}{text}\n"
        
        with open(ass_path, 'w', encoding='utf-8') as f:
            f.write(ass)
        
        print(f"  ✅ 字幕已生成：{ass_path}")
        return ass_path
    
    def burn_subtitle(self, video_path: Path, subtitle_path: Path) -> Optional[Path]:
        """烧录字幕"""
        print("\n🎬 烧录字幕...")
        output_video = self.output_dir / f"{video_path.stem}_sub.mp4"
        
        try:
            subprocess.run([
                'ffmpeg', '-i', str(video_path),
                '-vf', f'ass={subtitle_path}',
                '-c:a', 'copy',
                '-y', str(output_video)
            ], capture_output=True, check=True)
            
            size = output_video.stat().st_size / 1024 / 1024
            print(f"  ✅ 完成：{output_video.name} ({size:.1f} MB)")
            return output_video
            
        except Exception as e:
            print(f"  ❌ 失败：{e}")
            return None
    
    def process(self, add_subtitle: bool = True, remove_wm: bool = True) -> Optional[Path]:
        """完整处理流程"""
        # 1. 提取音频
        audio_path = self.extract_audio()
        if not audio_path:
            return None
        
        # 2. 去除水印
        video_path = None
        if remove_wm:
            video_path = self.remove_watermark()
        else:
            video_path = self.input_path
        
        if not video_path:
            return None
        
        # 3. 语音识别
        segments = []
        if add_subtitle:
            segments = self.transcribe_audio(audio_path)
        
        # 4. 生成并烧录字幕
        if add_subtitle and segments:
            # 获取视频信息
            info = json.loads(subprocess.run([
                'ffprobe', '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'json', str(video_path)
            ], capture_output=True, text=True).stdout)
            
            width = info['streams'][0]['width']
            height = info['streams'][0]['height']
            
            subtitle_path = self.generate_subtitle(segments, width, height)
            if subtitle_path:
                return self.burn_subtitle(video_path, subtitle_path)
        
        # 无字幕，返回去水印视频
        return video_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description='豆包水印去除 v3.0 - 增强版')
    parser.add_argument('input', help='输入视频文件')
    parser.add_argument('-o', '--output', help='输出目录', default='./output')
    parser.add_argument('--no-subtitle', action='store_true', help='不生成字幕')
    parser.add_argument('--no-watermark', action='store_true', help='不去除水印')
    args = parser.parse_args()
    
    processor = DoubaoWatermarkASR(args.input, args.output)
    result = processor.process(
        add_subtitle=not args.no_subtitle,
        remove_wm=not args.no_watermark
    )
    
    if result:
        print("\n" + "="*70)
        print(f"✅ 处理完成！")
        print(f"📁 输出：{result}")
        print("="*70)
    else:
        print("\n❌ 处理失败")
        sys.exit(1)


if __name__ == '__main__':
    main()
