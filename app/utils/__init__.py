from datetime import datetime

def format_datetime(value):
    """Format datetime to a readable string"""
    return value.strftime('%B %d, %Y %H:%M')

def allowed_file(filename, allowed_extensions):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions