# File Storage System

A comprehensive file storage solution with both web interface and REST API access, designed for ML workflows and general file management.

## Features

### Web Interface
- **User-friendly upload interface** with drag-and-drop support
- **File browsing** with visual file type indicators
- **File management** (upload, download, delete)
- **Responsive design** that works on desktop and mobile
- **Real-time feedback** for all operations

### REST API
- **Upload files** programmatically
- **Download files** by filename
- **List all files** with metadata
- **Delete files** via API
- **Automatic API documentation** at `/docs`

### File Support
Optimized for ML and data science workflows:
- **Documents**: .txt, .pdf, .md
- **Images**: .png, .jpg, .jpeg, .gif
- **Data files**: .csv, .json, .xml
- **Code**: .py, .ipynb
- **Archives**: .zip, .tar, .gz
- **ML models**: .pkl, .h5, .pth, .pt

## Requirements

Install the required packages:

```bash
pip install -r requirements.txt
```

## Quick Start

1. **Start the server**:
```bash
python app.py
```
Or using uvicorn directly:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

2. **Access the web interface**:
   - Open your browser and go to `http://localhost:8000`
   - Use the drag-and-drop interface to upload files
   - Browse uploaded files at `http://localhost:8000/files`

3. **View API documentation**:
   - Interactive API docs: `http://localhost:8000/docs`
   - OpenAPI schema: `http://localhost:8000/openapi.json`

## API Usage Examples

### Upload a file
```bash
curl -X POST "http://localhost:8000/api/upload" \
     -F "file=@dataset.csv"
```

### List all files
```bash
curl "http://localhost:8000/api/files"
```

### Download a file
```bash
curl -O "http://localhost:8000/api/download/dataset.csv"
```

### Delete a file
```bash
curl -X DELETE "http://localhost:8000/api/files/dataset.csv"
```

## Python API Client Example

```python
import requests

# Upload a file
with open('data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/upload',
        files={'file': f}
    )
print(response.json())

# List files
response = requests.get('http://localhost:8000/api/files')
files = response.json()
for file in files:
    print(f"{file['name']} - {file['size']} bytes")

# Download a file
response = requests.get('http://localhost:8000/api/download/data.csv')
with open('downloaded_data.csv', 'wb') as f:
    f.write(response.content)
```

## Configuration

### File Storage Location
Files are stored in the `uploads/` directory by default. You can change this by modifying the `UPLOAD_DIR` variable in `app.py`.

### Allowed File Extensions
Modify the `ALLOWED_EXTENSIONS` set in `app.py` to control which file types can be uploaded.

### Network Access
By default, the server runs on `0.0.0.0:8000`, making it accessible from any machine on the network. For production use, consider:
- Adding authentication
- Using HTTPS
- Setting up proper firewall rules
- Using a reverse proxy (nginx, apache)

## Architecture Comparison

This solution provides advantages over other approaches:

### vs Object Storage (Ceph, MinIO)
- **Simpler setup**: No complex cluster configuration
- **Lightweight**: Minimal resource requirements
- **Integrated UI**: Built-in web interface
- **ML-focused**: Optimized for data science workflows

### vs FTP Server
- **Modern API**: RESTful endpoints instead of FTP protocol
- **Web interface**: No need for separate FTP clients
- **Better security**: HTTP-based with potential for modern auth
- **Metadata support**: File information and organization

## Production Considerations

For production deployment:

1. **Add authentication** (JWT, OAuth, etc.)
2. **Use HTTPS** with proper SSL certificates
3. **Add file size limits** and validation
4. **Implement rate limiting**
5. **Add logging and monitoring**
6. **Use a production WSGI server** (Gunicorn, uWSGI)
7. **Set up backups** for the uploads directory

## Security Features

- File extension validation
- Duplicate file prevention
- Path traversal protection
- Error handling and sanitization

## Use Cases

Perfect for:
- **ML teams** sharing datasets and models
- **Research groups** collaborating on data
- **Development teams** sharing resources
- **Small to medium organizations** needing simple file storage
- **Educational environments** for student project sharing