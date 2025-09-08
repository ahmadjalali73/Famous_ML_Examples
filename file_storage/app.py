from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
from typing import List, Optional
import json
from datetime import datetime
import aiofiles

app = FastAPI(title="File Storage API", description="File storage system with web UI and API access")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    '.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.csv', '.json', '.xml',
    '.py', '.ipynb', '.md', '.zip', '.tar', '.gz', '.pkl', '.h5', '.pth', '.pt'
}

def get_file_info(filepath: str) -> dict:
    """Get file information including size and modification time."""
    stat = os.stat(filepath)
    return {
        'name': os.path.basename(filepath),
        'size': stat.st_size,
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'extension': os.path.splitext(filepath)[1].lower()
    }

def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main web interface."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/files", response_model=List[dict])
async def list_files():
    """API endpoint to list all uploaded files."""
    files = []
    for filename in os.listdir(UPLOAD_DIR):
        filepath = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(filepath):
            files.append(get_file_info(filepath))
    return files

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """API endpoint to upload a file."""
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Check if file already exists
    if os.path.exists(file_path):
        raise HTTPException(status_code=409, detail="File already exists")
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """API endpoint to download a file."""
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@app.delete("/api/files/{filename}")
async def delete_file(filename: str):
    """API endpoint to delete a file."""
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        os.remove(file_path)
        return {"message": "File deleted successfully", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@app.post("/upload")
async def upload_file_web(request: Request, file: UploadFile = File(...)):
    """Web interface file upload endpoint."""
    try:
        if not is_allowed_file(file.filename):
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": "File type not allowed"
            })
        
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        if os.path.exists(file_path):
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": "File already exists"
            })
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "success": f"File '{file.filename}' uploaded successfully"
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": f"Failed to upload file: {str(e)}"
        })

@app.get("/files")
async def files_page(request: Request):
    """Web interface to view all files."""
    files = []
    for filename in os.listdir(UPLOAD_DIR):
        filepath = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(filepath):
            files.append(get_file_info(filepath))
    
    return templates.TemplateResponse("files.html", {
        "request": request, 
        "files": files
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)