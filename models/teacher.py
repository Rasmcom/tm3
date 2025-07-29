from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TeacherInfo(db.Model):
    __tablename__ = 'teacher_info'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200))
    school = db.Column(db.String(200))
    education_level = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'school': self.school,
            'education_level': self.education_level,
            'subject': self.subject,
            'phone': self.phone,
            'email': self.email
        }

class Section(db.Model):
    __tablename__ = 'sections'
    
    id = db.Column(db.Integer, primary_key=True)
    section_type = db.Column(db.String(50), nullable=False)  # 'intro', 'vision', 'mission', 'values'
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'section_type': self.section_type,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class LeaderWord(db.Model):
    __tablename__ = 'leader_words'
    
    id = db.Column(db.Integer, primary_key=True)
    leader_name = db.Column(db.String(100), nullable=False)
    leader_image = db.Column(db.String(200))  # مسار الصورة
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'leader_name': self.leader_name,
            'leader_image': self.leader_image,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Certificate(db.Model):
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200))
    date_issued = db.Column(db.Date)
    certificate_file = db.Column(db.String(200))  # مسار الملف
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'issuer': self.issuer,
            'date_issued': self.date_issued.isoformat() if self.date_issued else None,
            'certificate_file': self.certificate_file,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    provider = db.Column(db.String(200))
    date_completed = db.Column(db.Date)
    duration_hours = db.Column(db.Integer)
    certificate_file = db.Column(db.String(200))  # مسار الملف
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'provider': self.provider,
            'date_completed': self.date_completed.isoformat() if self.date_completed else None,
            'duration_hours': self.duration_hours,
            'certificate_file': self.certificate_file,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UploadedFile(db.Model):
    __tablename__ = 'uploaded_files'
    
    id = db.Column(db.Integer, primary_key=True)
    original_name = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'original_name': self.original_name,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }

