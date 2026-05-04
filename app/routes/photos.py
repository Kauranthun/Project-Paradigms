from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, abort
from flask_login import login_user, login_required, logout_user, current_user
from app.models.models import db, Photo, User, bcrypt
from app.services.logic import can_user_upload
from app.utils.aspects import log_action, measure_performance
import os

photo_bp = Blueprint('photos', __name__)

@photo_bp.route('/')
@log_action
@measure_performance
def index():
    tag = request.args.get('tag')
    if tag:
        photos = Photo.query.filter(Photo.hashtags.contains(tag)).all()
    else:
        photos = Photo.query.all()
    return render_template('index.html', photos=photos)

@photo_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@log_action
@measure_performance
def upload():
    if request.method == 'POST':
        if not can_user_upload(current_user):
            flash(f"Limit reached for your account {current_user.package}!")
            return redirect(url_for('photos.index'))
            
        file = request.files.get('photo')
        if file:
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
            new_photo = Photo(
                filename=file.filename,
                description=request.form.get('description'),
                hashtags=request.form.get('hashtags'),
                user_id=current_user.id
            )
            db.session.add(new_photo)
            db.session.commit()
            flash("Photo successfully upload !")
            return redirect(url_for('photos.index'))
            
    return render_template('upload.html')

@photo_bp.route('/download/<int:photo_id>')
@log_action
@measure_performance
def download(photo_id):
    photo = db.session.get(Photo,photo_id)
    if photo is None:
        abort(404)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], photo.filename)

@photo_bp.route('/register', methods=['GET', 'POST'])
@log_action
@measure_performance
def register():
    if request.method == 'POST':
        hashed_pw = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        new_user = User(
            username=request.form.get('username'),
            password=hashed_pw,
            package=request.form.get('package')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created ! You can now login.')
        return redirect(url_for('photos.login'))
    return render_template('register.html')

@photo_bp.route('/login', methods=['GET', 'POST'])
@log_action
@measure_performance
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('photos.index'))
        else:
            flash('Incorrect credentials')
    return render_template('login.html')

@photo_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('photos.index'))