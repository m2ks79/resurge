"""
Video processing utilities - resize, crop, convert formats
"""

import os
import tempfile
from pathlib import Path
import subprocess
import json
from datetime import datetime


class VideoProcessor:
    """Handle video repurposing to different platforms"""

    # Platform specs: (width, height, format, max_duration_sec)
    PLATFORMS = {
        'tiktok': {
            'width': 1080,
            'height': 1920,
            'format': 'mp4',
            'max_duration': 300,  # 5 min
            'aspect_ratio': '9:16'
        },
        'instagram': {
            'width': 1080,
            'height': 1920,
            'format': 'mp4',
            'max_duration': 90,  # Reels max 90s
            'aspect_ratio': '9:16'
        },
        'youtube': {
            'width': 1080,
            'height': 1920,
            'format': 'mp4',
            'max_duration': 300,
            'aspect_ratio': '9:16'
        },
        'linkedin': {
            'width': 1080,
            'height': 1080,
            'format': 'mp4',
            'max_duration': 600,
            'aspect_ratio': '1:1'
        }
    }

    def __init__(self):
        # Use simple temp directory in project root
        self.temp_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')
        self.temp_dir = os.path.abspath(self.temp_dir)
        os.makedirs(self.temp_dir, exist_ok=True)
        print(f"✓ Upload directory: {self.temp_dir}")

    def get_video_info(self, filepath):
        """Get video duration and dimensions using ffprobe"""
        try:
            cmd = [
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration,width,height',
                '-of', 'json',
                filepath
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            # TODO: Parse format data
            return {'duration': 0, 'width': 0, 'height': 0}
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None

    def repurpose(self, input_filepath, add_watermark=False):
        """
        Convert video to all platform formats

        Returns:
            {
                'tiktok': {'filepath': '...', 'status': 'done'},
                'instagram': {'filepath': '...', 'status': 'done'},
                ...
            }
        """
        results = {}
        base_name = Path(input_filepath).stem

        # Get video info
        video_info = self.get_video_info(input_filepath)

        for platform, specs in self.PLATFORMS.items():
            try:
                output_filepath = os.path.join(
                    self.temp_dir,
                    f"{base_name}_{platform}.{specs['format']}"
                )

                # Convert using ffmpeg
                self._convert_with_ffmpeg(
                    input_filepath,
                    output_filepath,
                    specs,
                    add_watermark
                )

                # Return just the filename for download endpoint
                filename = os.path.basename(output_filepath)
                results[platform] = {
                    'filepath': filename,  # Just filename, not full path
                    'status': 'done',
                    'format': specs['format'],
                    'dimensions': f"{specs['width']}x{specs['height']}"
                }

            except Exception as e:
                results[platform] = {
                    'status': 'error',
                    'error': str(e)
                }

        return results

    def _convert_with_ffmpeg(self, input_file, output_file, specs, add_watermark):
        """Use ffmpeg to convert video to target specs"""
        try:
            # Basic ffmpeg command: resize + convert
            # TODO: Add watermark support
            # TODO: Handle aspect ratio conversion (center letterbox, etc)

            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-vf', f"scale={specs['width']}:{specs['height']}:force_original_aspect_ratio=decrease,pad={specs['width']}:{specs['height']}:(ow-iw)/2:(oh-ih)/2",
                '-c:v', 'libx264',
                '-preset', 'fast',
                '-c:a', 'aac',
                '-t', str(specs['max_duration']),
                '-y',  # Overwrite output
                output_file
            ]

            print(f"\n🎬 Converting to {specs['format'].upper()}")
            print(f"   Cmd: ffmpeg -i ... -vf scale={specs['width']}:{specs['height']} ...")

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)  # 5 min timeout
            except subprocess.TimeoutExpired:
                print(f"   ❌ TIMEOUT: Video processing took > 5 minutes")
                raise Exception(f"FFmpeg timeout: Video processing took too long")

            if result.returncode != 0:
                error_msg = result.stderr if result.stderr else "Unknown error"
                print(f"   ❌ FFmpeg returned {result.returncode}")
                print(f"   Error: {error_msg[:500]}")  # Print first 500 chars
                raise Exception(f"FFmpeg failed: {error_msg[:200]}")

            if not os.path.exists(output_file):
                print(f"   ❌ Output file not created")
                raise Exception(f"FFmpeg did not create output file: {output_file}")

            file_size = os.path.getsize(output_file) / 1024 / 1024
            print(f"   ✓ Created: {os.path.basename(output_file)} ({file_size:.1f} MB)")

        except subprocess.CalledProcessError as e:
            print(f"   ❌ CalledProcessError: {e}")
            raise Exception(f"FFmpeg conversion failed: {e.stderr.decode() if e.stderr else str(e)}")
        except Exception as e:
            print(f"   ❌ Exception: {str(e)[:200]}")
            raise

    def add_watermark(self, video_path, watermark_text="@yourbrand"):
        """Add text watermark to video"""
        # TODO: Implement watermark overlay using ffmpeg
        pass

    def trim_video(self, video_path, start_sec, end_sec):
        """Trim video to duration (for platform max lengths)"""
        # TODO: Implement trim using ffmpeg
        pass
