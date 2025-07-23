from flask import Blueprint, redirect, url_for, flash, render_template, request, session
from flask_login import login_user, logout_user, current_user
from authlib.integrations.flask_client import OAuthError
from app import db, oauth
from app.models import User
from app.auth.utils import get_google_provider_cfg
import requests

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        # Handle traditional registration
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate and create user
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', 'danger')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        # Handle traditional login
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        if not user or not user.password or not user.check_password(password):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('auth/login.html')

@auth_bp.route('/login/google')
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/google/authorize')
def google_authorize():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    try:
        google = oauth.create_client('google')
        token = google.authorize_access_token()
        user_info = google.parse_id_token(token)
        
        # Check if user exists by google_id
        user = User.query.filter_by(google_id=user_info['sub']).first()
        
        if not user:
            # Check if email exists (user registered traditionally)
            user = User.query.filter_by(email=user_info['email']).first()
            if user:
                # Link Google account to existing user
                user.google_id = user_info['sub']
            else:
                # Create new user
                username = user_info['email'].split('@')[0]
                user = User(
                    username=username,
                    email=user_info['email'],
                    google_id=user_info['sub'],
                    image_file=user_info.get('picture', 'default.jpg')
                )
                db.session.add(user)
            
            db.session.commit()
        
        login_user(user)
        flash('Logged in with Google successfully!', 'success')
        return redirect(url_for('main.home'))
    
    except OAuthError as e:
        flash('Failed to log in with Google.', 'danger')
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))