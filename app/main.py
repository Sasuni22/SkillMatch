from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Job

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    jobs = Job.query.limit(6).all()
    return render_template('index.html', jobs=jobs)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    resumes = current_user.resumes if current_user.is_authenticated else []
    return render_template('dashboard.html', resumes=resumes)
