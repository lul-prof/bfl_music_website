from flask import Blueprint, render_template, request, redirect, url_for, flash
from functools import wraps
from flask import current_app
from werkzeug.utils import secure_filename
from app.utils.helpers import save_audio, save_image, save_video, is_allowed_audio, is_allowed_video
from flask_login import login_required, current_user
from app.models.news import News
from app.models.music import Music, Video
from app.models.payment import Payment
from app import db
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function



@bp.route('/')
#@login_required
#@admin_required
def dashboard():
    total_music = Music.query.count()
    total_videos = Video.query.count()
    total_news = News.query.count()
    total_payments = Payment.query.count()
    recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_music=total_music,
                         total_videos=total_videos,
                         total_news=total_news,
                         total_payments=total_payments,
                         recent_payments=recent_payments)


@bp.route('/news', methods=['GET', 'POST'])
#@login_required
#@admin_required
def manage_news():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')
        
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'images', filename))
            image_url = url_for('static', filename=f'uploads/images/{filename}')
        
        news = News(title=title, content=content, image_url=image_url, author_id=current_user.id)
        db.session.add(news)
        db.session.commit()
        
        flash('News added successfully')
        return redirect(url_for('admin.manage_news'))
    
    news_list = News.query.order_by(News.created_at.desc()).all()
    return render_template('admin/manage_news.html', news_list=news_list)


@bp.route('/manage-music', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_music():
    if request.method == 'POST':
        title = request.form.get('title')
        artist = request.form.get('artist')
        album = request.form.get('album')
        audio_file = request.files.get('audio_file')
        cover_image = request.files.get('cover_image')

        if not title or not artist or not audio_file:
            flash('Please fill in all required fields.')
            return redirect(url_for('admin.manage_music'))

        if not is_allowed_audio(audio_file.filename):
            flash('Invalid audio file format.')
            return redirect(url_for('admin.manage_music'))

        audio_filename = save_audio(audio_file)
        cover_filename = save_image(cover_image, 'covers') if cover_image else None

        music = Music(
            title=title,
            artist=artist,
            album=album,
            file_url=url_for('static', filename=f'uploads/music/{audio_filename}'),
            cover_image=url_for('static', filename=f'uploads/covers/{cover_filename}') if cover_filename else None
        )
        db.session.add(music)
        db.session.commit()
        flash('Music uploaded successfully!')
        return redirect(url_for('admin.manage_music'))

    music_list = Music.query.order_by(Music.created_at.desc()).all()
    return render_template('admin/manage_music.html', music_list=music_list)

@bp.route('/manage-videos', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_videos():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        video_file = request.files.get('video_file')
        thumbnail = request.files.get('thumbnail')

        if not title or not video_file:
            flash('Please fill in all required fields.')
            return redirect(url_for('admin.manage_videos'))

        if not is_allowed_video(video_file.filename):
            flash('Invalid video file format.')
            return redirect(url_for('admin.manage_videos'))

        video_filename = save_video(video_file)
        thumbnail_filename = save_image(thumbnail, 'thumbnails') if thumbnail else None

        video = Video(
            title=title,
            description=description,
            video_url=url_for('static', filename=f'uploads/videos/{video_filename}'),
            thumbnail=url_for('static', filename=f'uploads/thumbnails/{thumbnail_filename}') if thumbnail_filename else None
        )
        db.session.add(video)
        db.session.commit()
        flash('Video uploaded successfully!')
        return redirect(url_for('admin.manage_videos'))

    video_list = Video.query.order_by(Video.created_at.desc()).all()
    return render_template('admin/manage_videos.html', video_list=video_list)



# Delete Music
@bp.route('/delete-music/<int:id>')
@login_required
@admin_required
def delete_music(id):
    music = Music.query.get_or_404(id)
    try:
        # Delete the actual files
        if music.file_url:
            delete_file(os.path.basename(music.file_url), 'music')
        if music.cover_image:
            delete_file(os.path.basename(music.cover_image), 'covers')
        
        # Delete database entry
        db.session.delete(music)
        db.session.commit()
        flash('Music deleted successfully!')
    except Exception as e:
        flash(f'Error deleting music: {str(e)}')
    return redirect(url_for('admin.manage_music'))

# Delete Video
@bp.route('/delete-video/<int:id>')
@login_required
@admin_required
def delete_video(id):
    video = Video.query.get_or_404(id)
    try:
        # Delete the actual files
        if video.video_url:
            delete_file(os.path.basename(video.video_url), 'videos')
        if video.thumbnail:
            delete_file(os.path.basename(video.thumbnail), 'thumbnails')
        
        # Delete database entry
        db.session.delete(video)
        db.session.commit()
        flash('Video deleted successfully!')
    except Exception as e:
        flash(f'Error deleting video: {str(e)}')
    return redirect(url_for('admin.manage_videos'))

# Edit Music
@bp.route('/edit-music/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_music(id):
    music = Music.query.get_or_404(id)
    if request.method == 'POST':
        music.title = request.form.get('title')
        music.artist = request.form.get('artist')
        music.album = request.form.get('album')
        
        # Handle new audio file
        audio_file = request.files.get('audio_file')
        if audio_file and audio_file.filename:
            if is_allowed_audio(audio_file.filename):
                # Delete old file
                if music.file_url:
                    delete_file(os.path.basename(music.file_url), 'music')
                # Save new file
                audio_filename = save_audio(audio_file)
                music.file_url = url_for('static', filename=f'uploads/music/{audio_filename}')
        
        # Handle new cover image
        cover_image = request.files.get('cover_image')
        if cover_image and cover_image.filename:
            # Delete old cover
            if music.cover_image:
                delete_file(os.path.basename(music.cover_image), 'covers')
            # Save new cover
            cover_filename = save_image(cover_image, 'covers')
            music.cover_image = url_for('static', filename=f'uploads/covers/{cover_filename}')
        
        try:
            db.session.commit()
            flash('Music updated successfully!')
            return redirect(url_for('admin.manage_music'))
        except Exception as e:
            flash(f'Error updating music: {str(e)}')
            
    return render_template('admin/edit_music.html', music=music)

# Edit Video
@bp.route('/edit-video/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_video(id):
    video = Video.query.get_or_404(id)
    if request.method == 'POST':
        video.title = request.form.get('title')
        video.description = request.form.get('description')
        
        # Handle new video file
        video_file = request.files.get('video_file')
        if video_file and video_file.filename:
            if is_allowed_video(video_file.filename):
                # Delete old file
                if video.video_url:
                    delete_file(os.path.basename(video.video_url), 'videos')
                # Save new file
                video_filename = save_video(video_file)
                video.video_url = url_for('static', filename=f'uploads/videos/{video_filename}')
        
        # Handle new thumbnail
        thumbnail = request.files.get('thumbnail')
        if thumbnail and thumbnail.filename:
            # Delete old thumbnail
            if video.thumbnail:
                delete_file(os.path.basename(video.thumbnail), 'thumbnails')
            # Save new thumbnail
            thumbnail_filename = save_image(thumbnail, 'thumbnails')
            video.thumbnail = url_for('static', filename=f'uploads/thumbnails/{thumbnail_filename}')
        
        try:
            db.session.commit()
            flash('Video updated successfully!')
            return redirect(url_for('admin.manage_videos'))
        except Exception as e:
            flash(f'Error updating video: {str(e)}')
            
    return render_template('admin/edit_video.html', video=video)



@bp.route('/edit-news/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_news(id):
    news = News.query.get_or_404(id)
    if request.method == 'POST':
        news.title = request.form.get('title')
        news.content = request.form.get('content')
        
        image = request.files.get('image')
        if image and image.filename:
            # Delete old image if exists
            if news.image_url:
                delete_file(os.path.basename(news.image_url), 'news')
            # Save new image
            image_filename = save_image(image, 'news')
            news.image_url = url_for('static', filename=f'uploads/news/{image_filename}')
        
        try:
            db.session.commit()
            flash('News updated successfully!')
            return redirect(url_for('admin.manage_news'))
        except Exception as e:
            flash(f'Error updating news: {str(e)}')
            
    return render_template('admin/edit_news.html', news=news)

@bp.route('/delete-news/<int:id>')
@login_required
@admin_required
def delete_news(id):
    news = News.query.get_or_404(id)
    try:
        # Delete the image file if exists
        if news.image_url:
            delete_file(os.path.basename(news.image_url), 'news')
            
        # Delete database entry
        db.session.delete(news)
        db.session.commit()
        flash('News deleted successfully!')
    except Exception as e:
        flash(f'Error deleting news: {str(e)}')
    return redirect(url_for('admin.manage_news'))