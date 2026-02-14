import os
import shutil
from pathlib import Path
from datetime import datetime

# Configure storage
UPLOAD_DIR = "uploaded_files"  # Local storage
# OR use AWS S3 (recommended for production)
USE_S3 = False  # Set to True for cloud storage

# Create upload directory if it doesn't exist
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

def save_uploaded_file(file, student_id, file_type):
    """
    Save uploaded PDF file to disk
    
    Args:
        file: UploadFile object from FastAPI
        student_id: Unique student identifier
        file_type: "resume" or "linkedin"
    
    Returns:
        dict with file path and URL
    """
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{file_type}_{student_id}_{timestamp}.pdf"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Save file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Reset file pointer for PDF text extraction
    file.file.seek(0)
    
    return {
        "filename": filename,
        "file_path": file_path,
        "file_url": f"/files/{filename}",  # URL to access file
        "uploaded_at": datetime.utcnow()
    }


def get_file_path(filename):
    """Get absolute path for a stored file"""
    return os.path.join(UPLOAD_DIR, filename)


def delete_student_files(file_paths):
    """Delete student files when removing student"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


# ===================================
# AWS S3 SUPPORT (OPTIONAL)
# ===================================

