from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Diary

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
@login_required
def home():
    diaries = Diary.query.filter_by(user_id=current_user.id).order_by(Diary.date_posted.desc()).all()
    return render_template('diary/home.html', diaries=diaries)