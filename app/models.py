from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    resumes = db.relationship('Resume', backref='owner', lazy=True)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def seed_sample_jobs():
    if Job.query.count() == 0:
        samples = [
            Job(title='Software Engineer', description='Develop backend services using Python, Flask, SQL, REST APIs.'),
            Job(title='Data Scientist', description='Work on machine learning models, NLP, Python, pandas, scikit-learn.'),
            Job(title='Frontend Developer', description='Create responsive UIs using React, JavaScript, HTML, CSS.'),
            Job(title='DevOps Engineer', description='Maintain CI/CD pipelines, Docker, Kubernetes, AWS/GCP.'),
            Job(title='Business Analyst', description='Analyze data, create dashboards, SQL, Excel, stakeholder communication.')
        ]
        db.session.add_all(samples)
        db.session.commit()
