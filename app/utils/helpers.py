import os
from werkzeug.utils import secure_filename
from PIL import Image
from datetime import datetime
from flask import current_app

def save_image(file, folder):
    """
    Save and optimize uploaded image
    Returns the filename of saved image
    """
    if not file:
        return None
        
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename)
    
    # Save and optimize image
    img = Image.open(file)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    img.thumbnail((800, 800))  # Resize if too large
    img.save(filepath, optimize=True, quality=85)
    
    return filename

def save_audio(file):
    """
    Save uploaded audio file
    Returns the filename of saved audio
    """
    if not file:
        return None
        
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'music', filename)
    file.save(filepath)
    
    return filename

def save_video(file):
    """
    Save uploaded video file
    Returns the filename of saved video
    """
    if not file:
        return None
        
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'videos', filename)
    file.save(filepath)
    
    return filename

def format_currency(amount):
    """
    Format amount to currency string
    """
    return f"${amount:.2f}"

def get_file_extension(filename):
    """
    Get file extension from filename
    """
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def is_allowed_image(filename):
    """
    Check if file is an allowed image type
    """
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return get_file_extension(filename) in ALLOWED_EXTENSIONS

def is_allowed_audio(filename):
    """
    Check if file is an allowed audio type
    """
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg'}
    return get_file_extension(filename) in ALLOWED_EXTENSIONS

def is_allowed_video(filename):
    """
    Check if file is an allowed video type
    """
    ALLOWED_EXTENSIONS = {'mp4', 'webm', 'mov'}
    return get_file_extension(filename) in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename):
    """
    Generate unique filename by adding timestamp
    """
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{name}_{timestamp}{ext}"

def create_directory_if_not_exists(path):
    """
    Create directory if it doesn't exist
    """
    if not os.path.exists(path):
        os.makedirs(path)

def delete_file(filename, folder):
    """
    Delete file from specified folder
    """
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False

def get_file_size(filename, folder):
    """
    Get file size in MB
    """
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename)
    if os.path.exists(filepath):
        return os.path.getsize(filepath) / (1024 * 1024)  # Convert to MB
    return 0