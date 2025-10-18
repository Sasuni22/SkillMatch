import os
from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Resume, Job
from . import db
import fitz
from sentence_transformers import SentenceTransformer, util

MODEL = SentenceTransformer('all-MiniLM-L6-v2')

upload_bp = Blueprint('upload', __name__, url_prefix='')

ALLOWED_EXTENSIONS = {'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(path):
    text = ""
    try:
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    except Exception:
        text = ""
    return text.strip()

def semantic_match(text, top_n=6):
    jobs = Job.query.all()
    if not jobs or not text.strip():
        return []
    job_texts = [j.title + " " + j.description for j in jobs]
    embeddings_jobs = MODEL.encode(job_texts, convert_to_tensor=True)
    embedding_cv = MODEL.encode([text], convert_to_tensor=True)
    scores = util.cos_sim(embedding_cv, embeddings_jobs)[0]
    ranked = []
    for idx, score in enumerate(scores):
        ranked.append((jobs[idx].title, jobs[idx].description, float(score.item()*100)))
    ranked.sort(key=lambda x: x[2], reverse=True)
    return ranked[:top_n]

@upload_bp.route('/upload', methods=['GET'])
@login_required
def upload_get():
    return render_template('upload.html')

@upload_bp.route('/upload', methods=['POST'])
@login_required
def upload_post():
    if 'resume' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    file = request.files['resume']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        text = extract_text_from_pdf(save_path)
        if not text:
            flash('Could not extract text from this file. Try a text-based PDF.', 'danger')
            return redirect(request.url)
        resume = Resume(filename=filename, text=text, user_id=current_user.id)
        db.session.add(resume)
        db.session.commit()
        matches = semantic_match(text, top_n=6)
        if request.accept_mimetypes.accept_json:
            return jsonify({
                'filename': filename,
                'matches': [{'title': t, 'description': d, 'score': round(s,2)} for t,d,s in matches]
            })
        return render_template('results.html', filename=filename, matches=matches)
    else:
        flash('Allowed file types: pdf, txt', 'danger')
        return redirect(request.url)

@upload_bp.route('/results/<int:resume_id>')
@login_required
def view_results(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    matches = semantic_match(resume.text, top_n=6)
    return render_template('results.html', filename=resume.filename, matches=matches)
