from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.learning import UserProgress, db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    progress = UserProgress.query.filter_by(user_id=current_user.id).first()
    return render_template('main/dashboard.html', progress=progress)

@main_bp.route('/about')
def about():
    return render_template('main/about.html') 