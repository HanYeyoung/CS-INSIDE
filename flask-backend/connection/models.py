from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User 모델
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)

# Class 모델
class Class(db.Model):
    __tablename__ = 'classes'
    uuid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    instructors = db.Column(db.Text, nullable=True)
    avg_grades = db.Column(db.Float, nullable=True)
    total_grades = db.Column(db.Integer, nullable=True)
    avg_gpa = db.Column(db.Float, nullable=True)

# UserClasses 모델 (연결 테이블)
class UserClasses(db.Model):
    __tablename__ = 'user_classes'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    class_id = db.Column(db.String(36), db.ForeignKey('classes.uuid'), primary_key=True)
