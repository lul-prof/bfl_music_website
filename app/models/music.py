from app import db
from datetime import datetime

class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100))
    file_url = db.Column(db.String(200), nullable=False)
    cover_image = db.Column(db.String(200))
    release_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(200), nullable=False)
    thumbnail = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)