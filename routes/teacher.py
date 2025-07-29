from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from src.models.teacher import db, TeacherInfo, Section, LeaderWord, Certificate, Course, UploadedFile

teacher_bp = Blueprint('teacher', __name__)

# إعدادات رفع الملفات
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    upload_path = os.path.join(current_app.static_folder, UPLOAD_FOLDER)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    return upload_path

# معلومات المعلم الأساسية
@teacher_bp.route('/teacher-info', methods=['GET'])
def get_teacher_info():
    teacher = TeacherInfo.query.first()
    if teacher:
        return jsonify(teacher.to_dict())
    return jsonify({'message': 'لم يتم العثور على معلومات المعلم'}), 404

@teacher_bp.route('/teacher-info', methods=['POST'])
def create_or_update_teacher_info():
    data = request.get_json()
    
    teacher = TeacherInfo.query.first()
    if teacher:
        # تحديث المعلومات الموجودة
        teacher.name = data.get('name', teacher.name)
        teacher.title = data.get('title', teacher.title)
        teacher.school = data.get('school', teacher.school)
        teacher.education_level = data.get('education_level', teacher.education_level)
        teacher.subject = data.get('subject', teacher.subject)
        teacher.phone = data.get('phone', teacher.phone)
        teacher.email = data.get('email', teacher.email)
    else:
        # إنشاء معلومات جديدة
        teacher = TeacherInfo(
            name=data.get('name'),
            title=data.get('title'),
            school=data.get('school'),
            education_level=data.get('education_level'),
            subject=data.get('subject'),
            phone=data.get('phone'),
            email=data.get('email')
        )
        db.session.add(teacher)
    
    db.session.commit()
    return jsonify(teacher.to_dict())

# الأقسام (المقدمة، الرؤية، الرسالة، القيم)
@teacher_bp.route('/sections', methods=['GET'])
def get_sections():
    sections = Section.query.all()
    return jsonify([section.to_dict() for section in sections])

@teacher_bp.route('/sections/<section_type>', methods=['GET'])
def get_section_by_type(section_type):
    section = Section.query.filter_by(section_type=section_type).first()
    if section:
        return jsonify(section.to_dict())
    return jsonify({'message': f'لم يتم العثور على قسم {section_type}'}), 404

@teacher_bp.route('/sections', methods=['POST'])
def create_or_update_section():
    data = request.get_json()
    section_type = data.get('section_type')
    
    section = Section.query.filter_by(section_type=section_type).first()
    if section:
        # تحديث القسم الموجود
        section.title = data.get('title', section.title)
        section.content = data.get('content', section.content)
    else:
        # إنشاء قسم جديد
        section = Section(
            section_type=section_type,
            title=data.get('title'),
            content=data.get('content')
        )
        db.session.add(section)
    
    db.session.commit()
    return jsonify(section.to_dict())

# كلمات القادة
@teacher_bp.route('/leader-words', methods=['GET'])
def get_leader_words():
    leaders = LeaderWord.query.all()
    return jsonify([leader.to_dict() for leader in leaders])

@teacher_bp.route('/leader-words', methods=['POST'])
def create_leader_word():
    data = request.get_json()
    
    leader = LeaderWord(
        leader_name=data.get('leader_name'),
        leader_image=data.get('leader_image'),
        message=data.get('message')
    )
    
    db.session.add(leader)
    db.session.commit()
    return jsonify(leader.to_dict()), 201

@teacher_bp.route('/leader-words/<int:leader_id>', methods=['PUT'])
def update_leader_word(leader_id):
    leader = LeaderWord.query.get_or_404(leader_id)
    data = request.get_json()
    
    leader.leader_name = data.get('leader_name', leader.leader_name)
    leader.leader_image = data.get('leader_image', leader.leader_image)
    leader.message = data.get('message', leader.message)
    
    db.session.commit()
    return jsonify(leader.to_dict())

@teacher_bp.route('/leader-words/<int:leader_id>', methods=['DELETE'])
def delete_leader_word(leader_id):
    leader = LeaderWord.query.get_or_404(leader_id)
    db.session.delete(leader)
    db.session.commit()
    return jsonify({'message': 'تم حذف كلمة القائد بنجاح'})

# الشهادات
@teacher_bp.route('/certificates', methods=['GET'])
def get_certificates():
    certificates = Certificate.query.all()
    return jsonify([cert.to_dict() for cert in certificates])

@teacher_bp.route('/certificates', methods=['POST'])
def create_certificate():
    data = request.get_json()
    
    certificate = Certificate(
        title=data.get('title'),
        issuer=data.get('issuer'),
        date_issued=datetime.strptime(data.get('date_issued'), '%Y-%m-%d').date() if data.get('date_issued') else None,
        certificate_file=data.get('certificate_file'),
        description=data.get('description')
    )
    
    db.session.add(certificate)
    db.session.commit()
    return jsonify(certificate.to_dict()), 201

@teacher_bp.route('/certificates/<int:cert_id>', methods=['PUT'])
def update_certificate(cert_id):
    certificate = Certificate.query.get_or_404(cert_id)
    data = request.get_json()
    
    certificate.title = data.get('title', certificate.title)
    certificate.issuer = data.get('issuer', certificate.issuer)
    if data.get('date_issued'):
        certificate.date_issued = datetime.strptime(data.get('date_issued'), '%Y-%m-%d').date()
    certificate.certificate_file = data.get('certificate_file', certificate.certificate_file)
    certificate.description = data.get('description', certificate.description)
    
    db.session.commit()
    return jsonify(certificate.to_dict())

@teacher_bp.route('/certificates/<int:cert_id>', methods=['DELETE'])
def delete_certificate(cert_id):
    certificate = Certificate.query.get_or_404(cert_id)
    db.session.delete(certificate)
    db.session.commit()
    return jsonify({'message': 'تم حذف الشهادة بنجاح'})

# الدورات
@teacher_bp.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])

@teacher_bp.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    
    course = Course(
        title=data.get('title'),
        provider=data.get('provider'),
        date_completed=datetime.strptime(data.get('date_completed'), '%Y-%m-%d').date() if data.get('date_completed') else None,
        duration_hours=data.get('duration_hours'),
        certificate_file=data.get('certificate_file'),
        description=data.get('description')
    )
    
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201

@teacher_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    
    course.title = data.get('title', course.title)
    course.provider = data.get('provider', course.provider)
    if data.get('date_completed'):
        course.date_completed = datetime.strptime(data.get('date_completed'), '%Y-%m-%d').date()
    course.duration_hours = data.get('duration_hours', course.duration_hours)
    course.certificate_file = data.get('certificate_file', course.certificate_file)
    course.description = data.get('description', course.description)
    
    db.session.commit()
    return jsonify(course.to_dict())

@teacher_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'تم حذف الدورة بنجاح'})

# رفع الملفات
@teacher_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'لم يتم اختيار ملف'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'لم يتم اختيار ملف'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # إضافة timestamp لتجنب تضارب الأسماء
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        upload_path = ensure_upload_folder()
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        
        # حفظ معلومات الملف في قاعدة البيانات
        uploaded_file = UploadedFile(
            original_name=file.filename,
            file_path=os.path.join(UPLOAD_FOLDER, filename),
            file_type=file.content_type,
            file_size=os.path.getsize(file_path)
        )
        
        db.session.add(uploaded_file)
        db.session.commit()
        
        return jsonify({
            'message': 'تم رفع الملف بنجاح',
            'file': uploaded_file.to_dict()
        }), 201
    
    return jsonify({'error': 'نوع الملف غير مدعوم'}), 400

@teacher_bp.route('/files', methods=['GET'])
def get_uploaded_files():
    files = UploadedFile.query.all()
    return jsonify([file.to_dict() for file in files])

# إضافة بيانات تجريبية
@teacher_bp.route('/init-sample-data', methods=['POST'])
def init_sample_data():
    # معلومات المعلم
    teacher = TeacherInfo.query.first()
    if not teacher:
        teacher = TeacherInfo(
            name='أحمد محمد السعيد',
            title='معلم اللغة العربية',
            school='مدرسة الأمل الثانوية',
            education_level='المرحلة الثانوية',
            subject='اللغة العربية',
            phone='0501234567',
            email='ahmed.alsaeed@school.edu.sa'
        )
        db.session.add(teacher)
    
    # الأقسام
    sections_data = [
        {
            'section_type': 'intro',
            'title': 'مقدمة',
            'content': 'مرحباً بكم في ملف شواهد الأداء الوظيفي الخاص بي. هذا الملف يحتوي على جميع إنجازاتي وخبراتي في مجال التعليم.'
        },
        {
            'section_type': 'vision',
            'title': 'الرؤية',
            'content': 'أن أكون معلماً مؤثراً يساهم في بناء جيل واعٍ ومبدع قادر على مواجهة تحديات المستقبل.'
        },
        {
            'section_type': 'mission',
            'title': 'الرسالة',
            'content': 'تقديم تعليم متميز يركز على تنمية قدرات الطلاب الفكرية والإبداعية من خلال استخدام أحدث الطرق التعليمية.'
        }
    ]
    
    for section_data in sections_data:
        section = Section.query.filter_by(section_type=section_data['section_type']).first()
        if not section:
            section = Section(**section_data)
            db.session.add(section)
    
    # كلمات القادة
    if not LeaderWord.query.first():
        leader1 = LeaderWord(
            leader_name='مدير المدرسة',
            message='المعلم أحمد من أفضل المعلمين في مدرستنا، يتميز بالإخلاص والتفاني في عمله.'
        )
        leader2 = LeaderWord(
            leader_name='مشرف المادة',
            message='أشهد للمعلم أحمد بالكفاءة العالية والقدرة على التطوير المستمر في أساليب التدريس.'
        )
        db.session.add(leader1)
        db.session.add(leader2)
    
    db.session.commit()
    return jsonify({'message': 'تم إضافة البيانات التجريبية بنجاح'})

