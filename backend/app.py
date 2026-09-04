"""
Resurge Backend
Converts videos to platform-specific formats for social media
"""

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import Config
from utils.video_processor import VideoProcessor
from utils.claude_optimizer import ClaudeOptimizer

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# CORS Configuration
CORS(app,
     origins=Config.CORS_ORIGINS,
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type"])

# Initialize config
Config.init_app(app)

print(f"✓ Flask app initialized")
print(f"  Upload directory: {Config.VIDEO_OUTPUT_DIR}")
print(f"  Max file size: {Config.MAX_FILE_SIZE / 1024 / 1024} MB")
print(f"  Allowed formats: {', '.join(Config.ALLOWED_EXTENSIONS)}")

processor = VideoProcessor()
optimizer = ClaudeOptimizer()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'service': 'resurge-api'})


@app.route('/api/repurpose', methods=['OPTIONS'])
def repurpose_options():
    """Handle CORS preflight requests"""
    return '', 204


@app.route('/api/repurpose', methods=['POST'])
def repurpose_video():
    """
    Convert video to platform-specific versions

    Request:
        - video: File upload (mp4, mov, webm, etc)
        - watermark: bool (optional, default false)

    Response:
        - {
            "id": "uuid",
            "status": "processing",
            "formats": {
              "tiktok": {"url": "/download/...", "status": "done"},
              "instagram": {"url": "/download/...", "status": "done"},
              ...
            }
          }
    """
    try:
        print(f"\n📥 /api/repurpose request received")
        print(f"   Files in request: {list(request.files.keys())}")
        print(f"   Content-Length: {request.content_length}")

        # Check if file in request
        if 'video' not in request.files:
            print("   ❌ No 'video' field in request")
            return jsonify({'error': 'No video file provided'}), 400

        file = request.files['video']
        print(f"   File: {file.filename}")

        if file.filename == '':
            print("   ❌ Empty filename")
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            print(f"   ❌ File type not allowed: {file.filename}")
            return jsonify({'error': f'File type not allowed. Allowed: {ALLOWED_EXTENSIONS}'}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.VIDEO_OUTPUT_DIR, filename)
        print(f"   Saving to: {filepath}")
        file.save(filepath)
        print(f"   ✓ File saved ({os.path.getsize(filepath) / 1024 / 1024:.1f} MB)")

        # Get options
        add_watermark = request.form.get('watermark', 'false').lower() == 'true'

        # Process video
        print(f"Processing video: {filename}")
        repurposed = processor.repurpose(filepath, add_watermark=add_watermark)

        print(f"\n✓ Processing complete!")
        for platform, data in repurposed.items():
            if data['status'] == 'done':
                print(f"   {platform}: {data['filepath']}")

        # Cleanup
        os.remove(filepath)

        return jsonify({
            'status': 'success',
            'formats': repurposed,
            'message': 'Video repurposed to all platforms'
        }), 200

    except Exception as e:
        error_msg = str(e)
        print(f"ERROR in /api/repurpose: {error_msg}")
        return jsonify({'error': error_msg}), 500


@app.route('/api/optimize-caption', methods=['POST'])
def optimize_caption():
    """
    (Phase 2) Use Claude to optimize caption for platform

    Request:
        - caption: str
        - platform: "tiktok" | "instagram" | "youtube" | "linkedin"

    Response:
        - {"optimized_caption": "...", "hashtags": ["#..."], "emojis": ["🎬", ...]}
    """
    try:
        data = request.get_json()
        caption = data.get('caption', '')
        platform = data.get('platform', 'instagram')

        if not caption:
            return jsonify({'error': 'Caption required'}), 400

        optimized = optimizer.optimize_for_platform(caption, platform)

        return jsonify({
            'status': 'success',
            'optimized_caption': optimized['caption'],
            'hashtags': optimized['hashtags'],
            'emojis': optimized['emojis']
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download repurposed video file"""
    try:
        uploads_dir = Config.VIDEO_OUTPUT_DIR

        # Build full path
        filepath = os.path.join(uploads_dir, filename)
        filepath = os.path.abspath(filepath)

        print(f"\n📥 Download: {filename}")
        print(f"   Path: {filepath}")

        # Security: ensure file is in uploads directory
        if not filepath.startswith(uploads_dir):
            print(f"   ❌ Unauthorized: file outside uploads directory")
            print(f"      File: {filepath}")
            print(f"      Allowed: {uploads_dir}")
            return jsonify({'error': 'Unauthorized'}), 403

        if not os.path.exists(filepath):
            print(f"   ❌ Not found")
            return jsonify({'error': f'File not found: {filename}'}), 404

        file_size = os.path.getsize(filepath) / 1024 / 1024
        print(f"   ✓ Serving ({file_size:.1f} MB)")

        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='video/mp4'
        )

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    """Serve frontend"""
    return jsonify({'message': 'Resurge API', 'version': '0.1.0'})


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host=Config.API_HOST, port=Config.API_PORT)
