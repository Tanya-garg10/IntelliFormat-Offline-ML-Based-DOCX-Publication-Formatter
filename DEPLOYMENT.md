# IntelliFormat Deployment Guide

This guide provides multiple deployment options for the IntelliFormat - Offline ML-Based DOCX Publication Formatter.

## Table of Contents
1. [Desktop Application Deployment](#desktop-application-deployment)
2. [Docker Container Deployment](#docker-container-deployment)
3. [Local Web Server Deployment](#local-web-server-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Desktop Application Deployment

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

## Docker Container Deployment

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

### Docker Health Check
The container includes a health check that monitors the API endpoint:
```bash
docker ps  # Check health status
docker logs intelliformat-app  # View logs
```

---

## Local Web Server Deployment

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

### Production Server Features
- Optimized React frontend
- Express.js backend with Python integration
- Automatic Python dependency management
- File upload handling with Multer
- RESTful API endpoints

---

## Cloud Deployment

### Important Note
⚠️ **Cloud deployment may conflict with the 100% offline requirement**. Consider this only if you need web access and can ensure data privacy.

### Vercel Deployment (Frontend Only)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy Frontend**
```bash
vercel
```

3. **Configure Environment Variables**
- Set up your backend API URL in Vercel dashboard

### Railway/Heroku Deployment (Full Stack)

1. **Create `Procfile`**
```
web: npm start
```

2. **Deploy to Railway**
```bash
npm install -g railway
railway login
railway init
railway up
```

3. **Configure Environment Variables**
- `NODE_ENV=production`
- `PORT=3000`

### AWS/GCP/Azure Deployment

For enterprise deployments, consider:
- **AWS ECS/Fargate**: Container orchestration
- **Google Cloud Run**: Serverless containers
- **Azure Container Instances**: Simple container hosting

---

## API Endpoints

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

## Performance Benchmarks

Based on testing with documents of various sizes:

| Document Size | Paragraphs | Processing Time | Throughput | Peak Memory |
|--------------|------------|-----------------|------------|-------------|
| 100 Pages    | 332        | 15.81s          | 21.0 paras/sec | 249.7 MB |
| 200 Pages    | 648        | 27.20s          | 23.8 paras/sec | 261.0 MB |
| 400+ Pages   | 1,265      | 52.37s          | 24.2 paras/sec | 280.3 MB |

---

## Troubleshooting

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

## Security Considerations

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

## Maintenance

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

## Support

For issues or questions:
1. Check this deployment guide
2. Review the main README.md
3. Check ARCHITECTURE.md for technical details
4. Open an issue on GitHub repository

---

## Deployment Choice Recommendation

- **Desktop Application**: Best for individual users, 100% offline, maximum privacy
- **Docker**: Best for consistent environments, easy deployment, institutional use
- **Local Web Server**: Best for development, testing, small team access
- **Cloud**: Only if web access is absolutely required and privacy concerns are addressed