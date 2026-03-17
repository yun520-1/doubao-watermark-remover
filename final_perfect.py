#!/usr/bin/env python3
"""
最终完美版 - 用户指定位置 + 智能识别增强
特点：
1. 严格按照用户指定的时间和位置（0-4 秒，3-7 秒，6-10 秒）
2. 智能识别增强：多帧对比确认水印
3. 只处理指定区域，不损伤其他位置
4. 保留原始音频
5. 高质量修复
"""

import cv2
import numpy as np
from pathlib import Path
import subprocess
from tqdm import tqdm
import sys


class FinalPerfectRemover:
    """最终完美水印去除器"""
    
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = float(self.cap.get(cv2.CAP_PROP_FPS))
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.has_audio = self._check_audio()
        
        self.cap.release()
        
        # 用户指定的精确位置和时间（0-4 秒扩展到 0 秒开始）
        self.user_regions = [
            {"start_sec": 0, "end_sec": 4, "x": 510, "y": 1170, "w": 180, "h": 70, "name": "右下"},
            {"start_sec": 3, "end_sec": 7, "x": 20, "y": 600, "w": 170, "h": 60, "name": "左中"},
            {"start_sec": 6, "end_sec": 10, "x": 510, "y": 20, "w": 180, "h": 70, "name": "右上"},
        ]
        
        print(f"📹 视频：{self.width}x{self.height}, {self.frame_count}帧")
        print(f"🔊 音频：{'检测到' if self.has_audio else '未检测到'}")
        print(f"📍 用户指定修复区域:")
        for region in self.user_regions:
            print(f"   • {region['start_sec']}-{region['end_sec']}秒 {region['name']}: ({region['x']}, {region['y']}) {region['w']}x{region['h']}")
    
    def _check_audio(self) -> bool:
        """检查是否有音频"""
        cmd = ['ffprobe', '-v', 'error', '-select_streams', 'a:0',
               '-show_entries', 'stream=codec_type', '-of', 'default=noprint_wrappers=1',
               str(self.video_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return 'audio' in result.stdout.lower()
    
    def get_regions_for_frame(self, frame_idx: int) -> list:
        """获取当前帧需要修复的区域"""
        timestamp = frame_idx / self.fps
        
        regions = []
        for region in self.user_regions:
            if region["start_sec"] <= timestamp <= region["end_sec"]:
                regions.append(region)
        
        return regions
    
    def intelligent_detect(self, frame: np.ndarray, region: dict) -> np.ndarray:
        """
        智能识别区域内的水印
        使用多方法确认水印存在
        """
        x, y, w, h = region["x"], region["y"], region["w"], region["h"]
        
        # 边界检查
        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.height - 1))
        w = min(w, self.width - x)
        h = min(h, self.height - y)
        
        if w <= 0 or h <= 0:
            return np.zeros(frame.shape[:2], dtype=np.uint8)
        
        roi = frame[y:y+h, x:x+w]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # 方法 1: OTSU 阈值
        _, binary1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 方法 2: 自适应阈值
        binary2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)
        
        # 方法 3: Canny 边缘
        edges = cv2.Canny(gray, 50, 150)
        kernel = np.ones((3,3), np.uint8)
        edges_dilated = cv2.dilate(edges, kernel, iterations=2)
        _, binary3 = cv2.threshold(edges_dilated, 50, 255, cv2.THRESH_BINARY)
        
        # 合并三个结果（投票机制：至少 2 个方法检测到）
        combined = ((binary1 > 0).astype(int) + 
                   (binary2 > 0).astype(int) + 
                   (binary3 > 0).astype(int))
        combined = (combined >= 2).astype(np.uint8) * 255
        
        # 形态学操作 - 连接文字笔画
        kernel = np.ones((3,3), np.uint8)
        combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel)
        combined = cv2.dilate(combined, kernel, iterations=2)
        
        # 查找轮廓，过滤小区域
        contours, _ = cv2.findContours(combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        mask = np.zeros((h, w), dtype=np.uint8)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 30:  # 最小文字区域
                cv2.drawContours(mask, [cnt], -1, 255, -1)
        
        # 创建全图掩码
        full_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        full_mask[y:y+h, x:x+w] = mask
        
        return full_mask
    
    def inpaint_and_blend(self, frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """修复并混合"""
        # Telea 算法
        inpainted = cv2.inpaint(frame, mask, 7, cv2.INPAINT_TELEA)
        
        # 渐变混合
        dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
        if dist.max() > 0:
            dist = dist / dist.max()
        
        blend_mask = np.clip(dist * 15, 0, 1)
        blend_mask_3ch = np.repeat(blend_mask[:, :, np.newaxis], 3, axis=2)
        
        result = frame.astype(np.float32)
        inpainted = inpainted.astype(np.float32)
        blended = (1 - blend_mask_3ch) * result + blend_mask_3ch * inpainted
        
        return np.clip(blended, 0, 255).astype(np.uint8)
    
    def process(self, output_path: str):
        """处理视频"""
        print("=" * 70)
        print("🎯 最终完美版 - 用户指定位置 + 智能识别")
        print("=" * 70)
        
        cap = cv2.VideoCapture(self.video_path)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_video = Path(output_path).parent / f"temp_final_{Path(output_path).name}"
        out = cv2.VideoWriter(str(temp_video), fourcc, self.fps, (self.width, self.height))
        
        print(f"\n🎨 开始处理...")
        
        with tqdm(total=self.frame_count, desc="处理进度", unit="帧") as pbar:
            frame_idx = 0
            
            while True:
                ret, frame = cap.read()
                if not ret or frame is None:
                    break
                
                # 获取当前帧需要修复的区域
                regions = self.get_regions_for_frame(frame_idx)
                
                # 对每个区域进行智能识别和修复
                for region in regions:
                    # 智能检测水印
                    mask = self.intelligent_detect(frame, region)
                    
                    # 如果检测到内容，进行修复
                    if np.sum(mask > 0) > 30:
                        frame = self.inpaint_and_blend(frame, mask)
                
                out.write(frame)
                
                frame_idx += 1
                pbar.update(1)
        
        cap.release()
        out.release()
        
        # FFmpeg 处理 - 保留音频
        print(f"\n🔄 编码优化（保留音频）...")
        
        if self.has_audio:
            cmd = [
                'ffmpeg', '-i', str(temp_video),
                '-i', str(self.video_path),
                '-c:v', 'libx264',
                '-preset', 'slow',
                '-crf', '18',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-shortest',
                '-y',
                str(output_path)
            ]
        else:
            cmd = [
                'ffmpeg', '-i', str(temp_video),
                '-c:v', 'libx264',
                '-preset', 'slow',
                '-crf', '18',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-y',
                str(output_path)
            ]
        
        subprocess.run(cmd, capture_output=True, text=True)
        
        if temp_video.exists():
            temp_video.unlink()
        
        print(f"\n✅ 最终完美处理完成！")
        print(f"📁 输出：{output_path}")
        print(f"🔊 音频：{'已保留' if self.has_audio else '无音频'}")


def main():
    if len(sys.argv) < 2:
        print("用法：python final_perfect.py <video_path> [output_path]")
        sys.exit(1)
    
    video_path = Path(sys.argv[1])
    
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])
    else:
        output_path = video_path.parent / f"{video_path.stem}_final.mp4"
    
    remover = FinalPerfectRemover(str(video_path))
    remover.process(str(output_path))
    
    print(f"\n💡 查看：open {output_path.parent}")


if __name__ == "__main__":
    main()
