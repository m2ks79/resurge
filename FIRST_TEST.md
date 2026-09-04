# 🚀 Your First Test - Step by Step

Let's verify everything works by running the app and uploading a test video.

**Time: ~10 minutes**

---

## Step 1: Verify Setup (2 min)

```bash
cd /Users/yourname/VSCode/projects/resurge
bash tests/test_quick.sh
```

You should see:
```
✓ Project Structure
✓ Dependencies Installed
✓ Ready to Start
```

If you see warnings, that's OK. Errors need fixing first.

---

## Step 2: Start the App (3 min)

```bash
cd /Users/yourname/VSCode/projects/resurge
make dev
```

Watch the terminal. You should see:

**Terminal 1 (Backend):**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**Terminal 2 (Frontend):**
```
  Local:        http://localhost:5173/
  press h + enter to show help
```

**Both should show without errors.** If there are errors:
- Python: See TESTING.md > Troubleshooting
- Node: See TESTING.md > Troubleshooting

---

## Step 3: Open in Browser (1 min)

Click here: **http://localhost:5173**

You should see:
- Title: **"🎬 Content Repurposer"**
- Subtitle: "Convert your video to all platforms in seconds"
- Big upload zone: "Drag video here or click to select"
- "Repurpose Video" button (greyed out)
- Bottom: "Phase 1: Basic repurposing | Phase 2 coming soon: Smart captions + scheduling"

### Looks different?
- Browser caching? Do hard refresh: **Cmd+Shift+R** (Mac) or **Ctrl+Shift+R** (Windows)
- Vite dev server crashed? Check Terminal 2 output

---

## Step 4: Create a Test Video (2 min)

The app expects a video file. Let's create a tiny one:

### Quick Option (using ffmpeg):
```bash
# Create 3-second test video (very small)
ffmpeg -f lavfi -i testsrc=s=640x480:d=3 \
       -f lavfi -i sine=f=440:d=3 \
       -pix_fmt yuv420p -y \
       /tmp/test_video.mp4
```

You should see:
```
Output #0, mp4, to '/tmp/test_video.mp4':
...
frame=   90 fps=0.0 q=-1Lframe=   90 fps= 62 q=-1L Lsize=N/A time=00:00:03.00
```

That means it worked!

### Alternative: Download a Sample Video
If ffmpeg isn't available, download a small video online and save it locally.

---

## Step 5: Upload Video in Browser (2 min)

1. **Drag & drop** `/tmp/test_video.mp4` onto the upload zone, OR
2. **Click** the zone and select the file

The zone should show:
```
📄 test_video.mp4
3.2 MB
```

### Can't drag-drop?
- Try clicking the zone instead
- Make sure file is .mp4, .mov, .webm, .avi, or .mkv

---

## Step 6: Repurpose! (2 min)

1. (Optional) Check "Add watermark" box
2. Click **"Repurpose Video"** button
3. Watch the progress...

Terminal shows:
```
ffmpeg -i /tmp/test_video.mp4 -vf scale=1080:1920 ... /tmp/test_video_tiktok.mp4
ffmpeg -i /tmp/test_video.mp4 -vf scale=1080:1920 ... /tmp/test_video_instagram.mp4
ffmpeg -i /tmp/test_video.mp4 -vf scale=1080:1920 ... /tmp/test_video_youtube.mp4
ffmpeg -i /tmp/test_video.mp4 -vf scale=1080:1080 ... /tmp/test_video_linkedin.mp4
```

**Wait ~10-15 seconds** (depends on video size + CPU).

---

## Step 7: See Results 🎉

Browser should show:

```
Your Videos Are Ready! 🎉

TikTok        YouTube        Instagram      LinkedIn
(1080x1920)   (1080x1920)     (1080x1920)    (1080x1080)
✓ Ready       ✓ Ready         ✓ Ready        ✓ Ready
[Download]    [Download]      [Download]     [Download]

[Repurpose Another Video]
```

### Success Indicators:
- ✅ 4 video cards appear
- ✅ All say "✓ Ready"
- ✅ No error messages
- ✅ Download buttons are clickable

### If Videos Show "✗ Error":
- Check Terminal 1 (backend) for error messages
- Common: "FFmpeg not found" → Run `brew install ffmpeg`
- Common: "Permission denied" → Check `/tmp/` folder permissions

---

## Step 8: Test Downloads (1 min)

Click any **[Download]** button.

The video file should:
- Download to your Downloads folder
- Be named like: `test_video_tiktok.mp4`
- Be playable in any video player

**Check file sizes:**
```bash
ls -lh ~/Downloads/test_video_*.mp4
```

You should see 4 files, each ~1-3 MB (size depends on original).

---

## Step 9: Celebrate! 🎉

**You just:**
- ✅ Started backend + frontend
- ✅ Uploaded a video
- ✅ Converted to 4 platform formats
- ✅ Downloaded the results

**This proves:**
- Python backend works
- Video processing (FFmpeg) works
- React frontend works
- API communication works

---

## Next Steps

### If Everything Worked:
1. **Try a real video** (your own content)
2. **Read TESTING.md** for automated tests
3. **Read MULTI_DEVICE_GUIDE.md** to work from phone/other PC
4. **Start Phase 2** (AI captions) - see README.md roadmap

### If Something Failed:
1. **Check error message** in Terminal 1 or 2
2. **See TESTING.md > Troubleshooting**
3. **Check project structure** with `find . -type f | head -20`

---

## Stop the App

```bash
# In terminal running make dev:
Press Ctrl+C

# If still running:
pkill -f "python3 app.py"
pkill -f "npm run dev"
```

---

**That's it! You now know the full dev→test→run cycle.** 🚀

Questions? Check:
- TESTING.md (detailed tests)
- README.md (project info)
- MULTI_DEVICE_GUIDE.md (cloud dev)
