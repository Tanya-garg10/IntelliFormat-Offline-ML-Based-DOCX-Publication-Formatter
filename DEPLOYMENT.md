# IntelliFormat Deployment Guide

This guide provides multiple deployment options for the IntelliFormat - Offline ML-Based DOCX Publication Formatter.

---

## Quick Cloud Deployment 🚀

**Fastest way to deploy to cloud:**

### Option 1: Vercel (Recommended - Free & Fast)
```bash
# Install Vercel CLI
npm install -g vercel

# Login and deploy
vercel login
vercel

# Deploy to production
vercel --prod
```

### Option 2: Render (Alternative - Free & Full-Stack)
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Create new Web Service
4. Use `render.yaml` configuration (already included)
5. Deploy with one click

---

## Desktop Application Deployment 💻

### Prerequisites
- Python 3.10 or higher
- Windows, macOS, or Linux
- Administrative privileges (for installing packages)

### Installation Steps

1. **Install Python Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run Desktop Application**
```bash
python app.py --gui
```

### Building Standalone Executable with PyInstaller

1. **Install PyInstaller**
```bash
pip install pyinstaller
```

2. **Build the Executable**
```bash
pyinstaller intelliformat.spec
```

3. **Locate the Executable**
- Windows: `dist/IntelliFormat.exe`
- macOS: `dist/IntelliFormat`
- Linux: `dist/IntelliFormat`

4. **Run the Executable**
```bash
# Windows
dist/IntelliFormat.exe

# macOS/Linux
./dist/IntelliFormat
```

### Desktop Application Features
- 100% offline operation
- Drag-and-drop document upload
- Real-time progress tracking
- Before/After document comparison
- Local file processing (no data leaves your machine)

---

## Docker Container Deployment 🐳

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose (optional, for easier deployment)

### Quick Start with Docker Compose

1. **Build and Run**
```bash
docker-compose up --build
```

2. **Access the Application**
Open your browser to: `http://localhost:3000`

3. **Stop the Container**
```bash
docker-compose down
```

### Manual Docker Deployment

1. **Build the Docker Image**
```bash
docker build -t intelliformat .
```

2. **Run the Container**
```bash
docker run -d -p 3000:3000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/output:/app/output \
  --name intelliformat-app \
  intelliformat
```

3. **Access the Application**
Open your browser to: `http://localhost:3000`

### Docker Volume Management
- `./uploads`: Persist uploaded manuscript files
- `./output`: Persist formatted output documents
- `./samples`: Access to sample documents for testing

---

## Local Web Server Deployment 🌐

### Prerequisites
- Node.js 18 or higher
- Python 3.10 or higher
- npm or yarn package manager

### Development Mode

1. **Install Dependencies**
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies
npm install
```

2. **Run Development Server**
```bash
npm run dev
```

3. **Access the Application**
Open your browser to: `http://localhost:3000`

### Production Mode

1. **Build the Application**
```bash
npm run build
```

2. **Start Production Server**
```bash
npm start
```

3. **Access the Application**
Open your browser to: `http://localhost:3000`

---

## API Endpoints 🔌

The web server provides the following REST API endpoints:

### Health Check
```http
GET /api/health
```

### Document Upload
```http
POST /api/upload
Content-Type: multipart/form-data
Body: manuscript (file)
```

### Document Summary
```http
GET /api/summary?file=path/to/document.docx
```

### Document Analysis
```http
GET /api/analyze?file=path/to/document.docx
```

### Document Formatting
```http
POST /api/format
Content-Type: application/json
Body: {
  "file": "path/to/document.docx",
  "output": "formatted_document.docx",
  "specs": {},
  "include_toc": true
}
```

### Benchmark
```http
GET /api/benchmark
```

### Accuracy Metrics
```http
GET /api/accuracy
```

### Download Formatted Document
```http
GET /api/download?file=output/formatted_document.docx
```

---

## Performance Benchmarks ⚡

Based on testing with documents of various sizes:

| Document Size | Paragraphs | Processing Time | Throughput | Peak Memory |
|--------------|------------|-----------------|------------|-------------|
| 100 Pages    | 332        | 15.81s          | 21.0 paras/sec | 249.7 MB |
| 200 Pages    | 648        | 27.20s          | 23.8 paras/sec | 261.0 MB |
| 400+ Pages   | 1,265      | 52.37s          | 24.2 paras/sec | 280.3 MB |

---

## Troubleshooting 🔧

### Python Dependency Issues
```bash
# Reinstall Python dependencies
pip install --force-reinstall -r requirements.txt
```

### Docker Build Failures
```bash
# Clean Docker cache
docker system prune -a
docker-compose build --no-cache
```

### Port Already in Use
```bash
# Change port in docker-compose.yml or server.ts
# Or kill the process using the port
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

### PyInstaller Build Issues
```bash
# Try building without UPX compression
pyinstaller --noupx intelliformat.spec

# Or build with console for debugging
# Edit intelliformat.spec, set console=True
```

### Memory Issues with Large Documents
- Increase Docker memory limit in Docker Desktop settings
- For desktop app, ensure sufficient RAM (4GB+ recommended)
- Consider processing documents in batches

### File Upload Issues
- Check upload directory permissions
- Ensure sufficient disk space
- Verify file size limits in server configuration

---

## Security Considerations 🔒

### Desktop Application
- All processing happens locally (100% offline)
- No data transmission to external servers
- File access limited to user-selected directories

### Docker Deployment
- Container runs in isolated environment
- No external network dependencies required
- Volume mounts for persistent storage

### Web Deployment
- Implement authentication for production use
- Use HTTPS for secure data transmission
- Consider rate limiting for API endpoints
- Sanitize file uploads to prevent malicious files

---

## Maintenance 🛠️

### Updates
- Pull latest changes from GitHub repository
- Rebuild Docker images: `docker-compose build --no-cache`
- Rebuild desktop executable: `pyinstaller intelliformat.spec`

### Backup
- Backup `ml/model.pkl` (trained ML model)
- Backup `dataset/training_data.csv` (training data)
- Backup custom formatting specifications

### Monitoring
- Monitor disk space for uploads/output directories
- Check application logs for errors
- Monitor memory usage during large document processing

---

## Support 📞

For issues or questions:
1. Check this deployment guide
2. Review the main README.md
3. Check ARCHITECTURE.md for technical details
4. Open an issue on GitHub repository

---

## Deployment Choice Recommendation 🎯

- **Desktop Application**: Best for individual users, 100% offline, maximum privacy
- **Docker**: Best for consistent environments, easy deployment, institutional use
- **Local Web Server**: Best for development, testing, small team access
- **Vercel**: Best for quick cloud deployment, free tier, excellent performance
- **Render**: Best for full-stack cloud deployment, persistent storage, good free tier