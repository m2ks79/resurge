"""
Configuration for Resurge Backend
Handles environment variables and settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = False

    # File upload
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 500 * 1024 * 1024))  # 500MB default
    ALLOWED_EXTENSIONS = {'mp4', 'mov', 'webm', 'avi', 'mkv'}

    # Video processing
    # Use absolute path to uploads directory
    _base_dir = os.path.abspath(os.path.dirname(__file__))
    VIDEO_OUTPUT_DIR = os.getenv('VIDEO_OUTPUT_DIR', os.path.join(os.path.dirname(_base_dir), 'uploads'))
    MAX_VIDEO_DURATION = 600  # seconds

    # CORS - Allow configurable origins
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')

    # API
    API_PORT = int(os.getenv('API_PORT', 8000))
    API_HOST = os.getenv('API_HOST', '127.0.0.1')

    # Claude API (for Phase 2)
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    @staticmethod
    def init_app(app):
        """Initialize Flask app with config"""
        # Ensure upload directory exists
        os.makedirs(Config.VIDEO_OUTPUT_DIR, exist_ok=True)
