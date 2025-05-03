from flask import Blueprint, render_template, request
from app.models.news import News
from app.models.music import Music, Video
from flask_login import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    news = News.query.order_by(News.created_at.desc()).limit(5).all()
    latest_music = Music.query.order_by(Music.created_at.desc()).limit(6).all()
    latest_videos = Video.query.order_by(Video.created_at.desc()).limit(3).all()
    return render_template('main/index.html', news=news, music=latest_music, videos=latest_videos)

@bp.route('/music')
def music():
    music_list = Music.query.order_by(Music.created_at.desc()).all()
    return render_template('main/music.html', music_list=music_list)

@bp.route('/videos')
def videos():
    video_list = Video.query.order_by(Video.created_at.desc()).all()
    return render_template('main/videos.html', video_list=video_list)

@bp.route('/news')
def news():
    news_list = News.query.order_by(News.created_at.desc()).all()
    return render_template('main/news.html', news_list=news_list)

@bp.route('/donate')
@login_required
def donate():
    return render_template('main/donate.html')