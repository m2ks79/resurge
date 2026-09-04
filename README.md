# 🚀 Resurge

**Convert one video into platform-optimized versions for TikTok, Instagram, YouTube, and LinkedIn.**

Your content surges everywhere. One upload, four platforms, infinite reach.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Features

### Phase 1 ✅ (Released)
- 📤 Drag-drop video upload
- 🎨 Auto-convert to platform dimensions:
  - **TikTok**: 1080×1920 (vertical, max 5 min)
  - **Instagram Reels**: 1080×1920 (vertical, max 90 sec)
  - **YouTube Shorts**: 1080×1920 (vertical, max 5 min)
  - **LinkedIn**: 1080×1080 (square, max 10 min)
- ⚡ Batch processing (4 formats at once)
- 💾 One-click download all versions

### Phase 2 ✅ (Released)
- 🤖 AI-powered captions (platform-specific)
- #️⃣ Auto-generated hashtags
- 😊 Emoji recommendations
- 📱 Platform-optimized descriptions

### Phase 3 📅 (Planned)
- 📤 Direct platform publishing
- ⏰ Scheduled posting
- 📊 Performance analytics

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python, Flask, FFmpeg |
| **Frontend** | React, Vite, Axios |
| **AI** | Claude API (Phase 2) |
| **Deployment** | Docker, Docker Compose |
| **Cloud** | GitHub Codespaces (dev) |

---

## 📋 Requirements

### Local Development
- **Python** 3.9+
- **Node.js** 18+
- **FFmpeg** (for video processing)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/resurge.git
cd resurge

# 2. Copy environment file
cp .env.example .env

# 3. Backend setup
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 4. Frontend setup (new terminal)
cd frontend
npm install

# 5. Start development servers
# Terminal 1 (Backend):
cd backend && source .venv/bin/activate && python app.py

# Terminal 2 (Frontend):
cd frontend && npm run dev
```

**Open:** http://localhost:5173

---

## 🐳 Docker Setup (Recommended)

No local dependencies needed. Docker handles everything.

```bash
# Start all services
docker-compose up

# Access:
# - Frontend: http://localhost:5173
# - Backend API: http://localhost:8000
# - Redis: localhost:6379
```

---

## ☁️ GitHub Codespaces

Dev in the browser from any device:

1. Go to: https://github.com/yourusername/resurge
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait 2 min for auto-setup
4. Ports auto-exposed in browser

See [MULTI_DEVICE_GUIDE.md](MULTI_DEVICE_GUIDE.md) for details.

---

## 📚 Usage

### Upload & Convert

1. **Open** http://localhost:5173
2. **Drag** video onto upload zone (or click to browse)
3. **Wait** for processing (large videos take longer)
4. **Download** any platform version

### Supported Formats
- ✅ MP4, MOV, WebM, AVI, MKV
- ✅ Max 500 MB
- ✅ Audio preserved

---

## 🔧 Configuration

### Environment Variables

Create `.env` from `.env.example`:

```bash
# Backend
API_HOST=127.0.0.1        # Server address
API_PORT=8000             # Server port
DEBUG=False               # Debug mode

# File Upload
MAX_FILE_SIZE=524288000   # 500MB (in bytes)
VIDEO_OUTPUT_DIR=./uploads

# Claude API (Phase 2)
ANTHROPIC_API_KEY=sk-ant-xxx...  # Get from console.anthropic.com

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 📁 Project Structure

```
resurge/
├── backend/
│   ├── app.py                    # Flask main app
│   ├── config.py                 # Configuration
│   ├── requirements.txt           # Python dependencies
│   └── utils/
│       ├── video_processor.py    # FFmpeg handling
│       └── claude_optimizer.py   # AI captions (Phase 2)
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # Main component
│   │   └── index.css             # Styling
│   ├── package.json
│   └── vite.config.js
├── .devcontainer/                # Codespaces config
├── uploads/                      # Generated videos (gitignored)
├── docker-compose.yml
├── Makefile                      # Dev commands
└── README.md
```

---

## 🔌 API Reference

### Upload Video
```bash
POST /api/repurpose
Content-Type: multipart/form-data

Body:
  - video: <file>
  - watermark: false  (optional)

Response:
{
  "status": "success",
  "formats": {
    "tiktok": {"filepath": "xxx_tiktok.mp4", "status": "done"},
    "instagram": {"filepath": "xxx_instagram.mp4", "status": "done"},
    ...
  }
}
```

### Download Video
```bash
GET /api/download/<filename>

Response: Binary video file
```

### Health Check
```bash
GET /health

Response: {"status": "ok", "service": "resurge-api"}
```

---

## 🧪 Testing

### Quick Sanity Check
```bash
bash tests/test_quick.sh
```

### Backend Tests
```bash
cd backend
source .venv/bin/activate
python tests/test_api.py
```

### Full Test Guide
See [TESTING.md](TESTING.md) for detailed testing procedures.

---

## 📖 Documentation

- **[FIRST_TEST.md](FIRST_TEST.md)** — Step-by-step walkthrough for new users
- **[TESTING.md](TESTING.md)** — Testing guide (unit, integration, E2E)
- **[MULTI_DEVICE_GUIDE.md](MULTI_DEVICE_GUIDE.md)** — Dev on phone/laptop/cloud
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — System design & flow

---

## 🚀 Deployment

### Heroku (Free Tier Paused)
```bash
heroku create your-app-name
git push heroku main
heroku logs --tail
```

### DigitalOcean / AWS
See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for cloud hosting guides.

### Self-Hosted
```bash
# Build Docker image
docker build -t resurge .

# Run on server
docker run -p 8000:8000 -p 5173:5173 resurge
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repo
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Commit** changes: `git commit -am 'Add feature'`
4. **Push** to branch: `git push origin feature/your-feature`
5. **Open** a Pull Request

### Development Setup
```bash
git clone https://github.com/yourusername/resurge.git
cd resurge
make dev  # Starts both backend and frontend
```

### Code Style
- Python: Follow [PEP 8](https://pep8.org/)
- JavaScript: Use [Prettier](https://prettier.io/)

---

## 📋 Roadmap

- [x] Phase 1: Basic repurposing
- [x] Phase 2: AI captions + hashtags
- [ ] Phase 3: Direct publishing
- [ ] Phase 4: Analytics dashboard
- [ ] Phase 5: Team collaboration

See [ROADMAP.md](docs/ROADMAP.md) for detailed timeline.

---

## 🐛 Troubleshooting

### FFmpeg Not Found
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
choco install ffmpeg
```

### Port Already in Use
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>
```

### Upload Fails (403 Error)
Ensure backend is running and CORS is configured. Check `.env` file.

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more.

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.

---

## 👤 Author

Created by [Your Name/Organization]

**Questions?** Open an [Issue](https://github.com/yourusername/resurge/issues)

---

## 🙏 Acknowledgments

- [FFmpeg](https://ffmpeg.org/) — Video processing
- [Claude API](https://anthropic.com/) — AI captions (Phase 2)
- [React](https://react.dev/) + [Vite](https://vitejs.dev/) — Frontend
- [Flask](https://flask.palletsprojects.com/) — Backend

---

**Give this repo a ⭐ if you find it useful!**

Made with ❤️ for content creators worldwide.
