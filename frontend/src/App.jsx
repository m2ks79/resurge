import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'

const PLATFORMS = [
  { name: 'TikTok', icon: '🎵', color: '#000000', size: '1080×1920' },
  { name: 'Instagram', icon: '📷', color: '#E4405F', size: '1080×1920' },
  { name: 'YouTube', icon: '▶️', color: '#FF0000', size: '1080×1920' },
  { name: 'LinkedIn', icon: '💼', color: '#0A66C2', size: '1080×1080' },
]

export default function App() {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [addWatermark, setAddWatermark] = useState(false)
  const [currentStep, setCurrentStep] = useState('idle') // idle, uploading, converting, complete

  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0])
      setError(null)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'video/*': ['.mp4', '.mov', '.webm', '.avi', '.mkv'] },
    maxSize: 500 * 1024 * 1024  // 500MB
  })

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a video file')
      return
    }

    setUploading(true)
    setError(null)
    setCurrentStep('uploading')
    setProgress(0)

    try {
      const formData = new FormData()
      formData.append('video', file)
      formData.append('watermark', addWatermark)

      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(p => Math.min(p + Math.random() * 30, 90))
      }, 500)

      const response = await axios.post('/api/repurpose', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      clearInterval(progressInterval)
      setProgress(100)
      setCurrentStep('complete')
      setResults(response.data.formats)
      console.log('Repurposing complete:', response.data)

      // Show confetti animation briefly
      setTimeout(() => {
        setCurrentStep('idle')
      }, 2000)
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Failed to repurpose video'
      console.error('Upload error:', errorMsg)
      setError(errorMsg)
      setCurrentStep('idle')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🎬 Content Repurposer</h1>
        <p>Convert your video to all platforms in seconds</p>
      </header>

      <main className="container">
        <div className="upload-section">
          <form onSubmit={handleUpload}>
            <div
              {...getRootProps()}
              className={`dropzone ${isDragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
            >
              <input {...getInputProps()} />
              {file ? (
                <div className="file-info">
                  <p>📄 {file.name}</p>
                  <p className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                </div>
              ) : (
                <div className="dropzone-content">
                  <p className="big">Drag video here or click to select</p>
                  <p className="small">Supports: MP4, MOV, WebM, AVI, MKV (up to 500MB)</p>
                </div>
              )}
            </div>

            <div className="options">
              <label>
                <input
                  type="checkbox"
                  checked={addWatermark}
                  onChange={(e) => setAddWatermark(e.target.checked)}
                />
                Add watermark
              </label>
            </div>

            {error && <div className="error">{error}</div>}

            <button
              type="submit"
              disabled={!file || uploading}
              className="btn-primary"
            >
              {uploading ? 'Processing...' : 'Repurpose Video'}
            </button>
          </form>
        </div>

        {uploading && (
          <div className="progress-section">
            <h2>🎬 Converting Your Video...</h2>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }}></div>
            </div>
            <p className="progress-text">{Math.round(progress)}% Complete</p>
            <div className="converting-platforms">
              {PLATFORMS.map((p) => (
                <div key={p.name} className="platform-item">
                  <span className="platform-icon">{p.icon}</span>
                  <span className="platform-name">{p.name}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {results && (
          <div className="results">
            <div className="results-header">
              <h2>🎉 Videos Ready!</h2>
              <p>Your content is optimized for all platforms</p>
            </div>

            <div className="formats-grid">
              {Object.entries(results).map(([platform, data]) => {
                const platformInfo = PLATFORMS.find(p => p.name.toLowerCase() === platform.toLowerCase())
                return (
                  <div key={platform} className="format-card" style={{
                    '--platform-color': platformInfo?.color || '#666'
                  }}>
                    <div className="card-header">
                      <span className="platform-icon">{platformInfo?.icon}</span>
                      <h3>{platform.charAt(0).toUpperCase() + platform.slice(1)}</h3>
                    </div>
                    <p className="dimensions">{data.dimensions}</p>
                    {data.status === 'done' ? (
                      <>
                        <p className="status ok">✓ Ready to Download</p>
                        <a href={`/api/download/${data.filepath}`} className="btn-download">
                          📥 Download
                        </a>
                      </>
                    ) : (
                      <p className="status error">✗ {data.error}</p>
                    )}
                  </div>
                )
              })}
            </div>

            <div className="results-actions">
              <button className="btn-secondary" onClick={() => {
                setFile(null)
                setResults(null)
                setProgress(0)
              }}>
                ➕ Convert Another Video
              </button>
              <p className="results-tip">💡 Tip: Share these videos across all platforms for maximum reach!</p>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Phase 1: Basic repurposing | Phase 2 coming soon: Smart captions + scheduling</p>
      </footer>
    </div>
  )
}
