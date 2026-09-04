# 🧪 Testing Guide - Content Repurposer

Three levels of testing: quick sanity checks → manual testing → automated tests.

---

## Level 1: Quick Sanity Check (5 min)

**Verify everything is installed and ready to run.**

### Run:
```bash
cd projects/resurge
bash tests/test_quick.sh
```

### Expected Output:
```
✓ Project structure (5 files)
✓ Dependencies installed (Flask, Node, etc)
✓ Ready to start
```

---

## Level 2: Manual Testing (15 min)

**Start the app and test it in browser.**

### Start Backend + Frontend:
```bash
cd projects/resurge
make setup       # (only first time)
make dev
```

**Terminal output should show:**
```
Backend:  * Running on http://127.0.0.1:5000
Frontend: http://localhost:5173
```

### In Browser:
1. Open: http://localhost:5173
2. You should see:
   - Title: "🎬 Content Repurposer"
   - Upload zone (drag-drop or click)
   - "Repurpose Video" button (disabled until video selected)

### Test Upload (using a sample video):
```bash
# Create a small test video (5 seconds, 1MB)
# Option 1: Download one
curl -o test_video.mp4 https://media-files.vidyard.com/videos/...

# Option 2: Use ffmpeg to create one
ffmpeg -f lavfi -i testsrc=s=320x240:d=5 \
       -f lavfi -i sine=f=1000:d=5 \
       -pix_fmt yuv420p test_video.mp4
```

### In Browser - Upload Flow:
1. Drag `test_video.mp4` onto the upload zone
2. File should show in zone: "📄 test_video.mp4 (1.2 MB)"
3. Toggle "Add watermark" (optional)
4. Click "Repurpose Video"
5. Wait ~30 sec for processing...

### Expected Results:
```
✓ TikTok    (1080x1920)  ✓ Ready
✓ Instagram (1080x1920)  ✓ Ready
✓ YouTube   (1080x1920)  ✓ Ready
✓ LinkedIn  (1080x1080)  ✓ Ready

[Download] buttons appear
```

### If Video Processing Fails:
- **"FFmpeg not found"** → Install: `brew install ffmpeg` (Mac) or `sudo apt install ffmpeg` (Linux)
- **"File size too large"** → Use smaller video (max 500MB)
- **"Processing timeout"** → Very long videos take time; try shorter one

---

## Level 3: Automated Tests

### API Tests:
```bash
cd projects/resurge
source backend/.venv/bin/activate
python3 tests/test_api.py
```

**Tests:**
- ✓ Flask imports
- ✓ App initialization
- ✓ Health endpoint (`/health`)
- ✓ VideoProcessor module
- ✓ Claude integration

### Frontend Build Test:
```bash
cd projects/resurge/frontend
npm run build
```

Expected: Creates `dist/` folder with optimized assets (~200KB)

---

## Testing Different Scenarios

### Scenario 1: Backend Only
```bash
cd backend
source .venv/bin/activate
python3 -c "from app import app; print(app.config)"
```

### Scenario 2: Frontend Only (mock API)
```bash
cd frontend
npm run dev
# App runs but upload fails (no backend)
# This is OK for testing UI
```

### Scenario 3: Docker (full stack)
```bash
docker-compose up
# Opens at http://localhost:5000 + http://localhost:5173
```

### Scenario 4: GitHub Codespaces
1. Go: https://github.com/m2ks79/resurge/codespaces
2. Wait for auto-setup (2 min)
3. Ports auto-exposed at top
4. Click port 5173 → browser opens frontend

---

## Testing Phase 2 (Smart Captions)

When you add caption optimization:

```bash
# Test endpoint
curl -X POST http://localhost:5000/api/optimize-caption \
  -H "Content-Type: application/json" \
  -d '{
    "caption": "Check out my new video!",
    "platform": "tiktok"
  }'

# Expected response:
# {
#   "optimized_caption": "OMG this video hits different 🔥",
#   "hashtags": ["#foryou", "#viral", "#trending"],
#   "emojis": ["🎬", "🔥", "✨"],
#   "platform": "tiktok"
# }
```

---

## Troubleshooting Tests

### Issue: "make: command not found"
```bash
# Makefile not working? Run commands directly:
cd backend
source .venv/bin/activate
python3 app.py &

cd frontend
npm run dev
```

### Issue: "npm ERR! code ERESOLVE"
```bash
# Node version conflict
npm install --legacy-peer-deps
```

### Issue: "FFmpeg not found"
```bash
# Mac
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows
choco install ffmpeg
```

### Issue: "Port 5000/5173 already in use"
```bash
# Find process
lsof -i :5000
lsof -i :5173

# Kill it
kill -9 <PID>

# Then restart
make dev
```

### Issue: "ANTHROPIC_API_KEY not found"
This is expected for Phase 2 (captions). Phase 1 works without it.

To test Phase 2:
```bash
cp .env.example .env
# Edit .env and add your key:
# ANTHROPIC_API_KEY=sk-ant-...

# Then restart backend
```

---

## Performance Benchmarks

Expected times on typical MacBook:
- API startup: ~2 sec
- Frontend dev server: ~3 sec
- Single video processing (1MB, 5s): ~5-10 sec
- Vite build: ~8 sec

---

## Continuous Integration (CI)

When you push to GitHub, tests can auto-run:

```yaml
# .github/workflows/test.yml (create this file)
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r backend/requirements.txt
      - run: python3 tests/test_api.py
      
      - uses: actions/setup-node@v3
      - run: cd frontend && npm install && npm run build
```

---

## What To Test Before Shipping to Users

- [ ] Upload video works
- [ ] All 4 platform versions generate
- [ ] Download files are correct format
- [ ] No console errors (F12)
- [ ] Mobile responsive (test on phone)
- [ ] Error handling (upload huge file, broken video)
- [ ] API rate limiting (if deployed)
- [ ] Security (file upload sanitization)

---

## Next: Advanced Testing

- Unit tests for `VideoProcessor` (using pytest)
- E2E tests using Selenium/Playwright
- Load testing with k6
- Security scanning with OWASP

See `/docs/` for detailed guides.

---

**Ready to test?** Start with Level 1, then Level 2! 🚀
