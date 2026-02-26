from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Subject, Message, Faculty, Group, Direction, ApiKey
from app import db
from werkzeug.security import check_password_hash
from datetime import datetime

bp = Blueprint('api', __name__, url_prefix='/api')


def get_api_key_from_request():
    """X-API-Key header orqali mobil ilova kalitini tekshirish. To'g'ri bo'lsa ApiKey obektini qaytaradi."""
    raw_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    if not raw_key:
        return None
    for key in ApiKey.query.filter_by(is_active=True).all():
        if check_password_hash(key.key_hash, raw_key):
            key.last_used_at = datetime.utcnow()
            db.session.commit()
            return key
    return None


def mobile_api_required(permission=None):
    """Mobil API uchun: X-API-Key talab qiladi. permission berilsa, shu dostup kalitda yoqilgan bo'lishi kerak."""
    from functools import wraps
    perm_names = {'faculties': 'Fakultetlar', 'directions': "Yo'nalishlar", 'groups': 'Guruhlar'}
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            raw_key = request.headers.get('X-API-Key') or request.args.get('api_key')
            if not raw_key:
                return jsonify({
                    'error': 'API kaliti yuborilmagan',
                    'message': 'So\'rovda X-API-Key header yoki ?api_key=KALIT parametri kerak.'
                }), 401
            api_key = get_api_key_from_request()
            if not api_key:
                return jsonify({
                    'error': 'Kalit noto\'g\'ri yoki o\'chirilgan',
                    'message': 'Admin panelda API kalitlari bo\'limida kalitni tekshiring, dostup yoqilgan bo\'lishi kerak.'
                }), 401
            if permission and not api_key.has_permission(permission):
                name = perm_names.get(permission, permission)
                return jsonify({
                    'error': f'Dostup berilmagan: {name}',
                    'message': f'Ushbu kalitga "{name}" dostupi yoqilmagan. Admin → API kalitlari → Dostuplar → {name} ni ON qiling.',
                    'required_permission': permission
                }), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

@bp.route('/users/search')
@login_required
def search_users():
    from app.models import TeacherSubject, Group
    
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])
    
    # Ruxsatli foydalanuvchilarni aniqlash
    allowed_user_ids = set()
    
    if current_user.role == 'student':
        # Talaba faqat o'ziga biriktirilgan o'qituvchi va dekanni qidirishi mumkin
        users = []
        
        if current_user.group_id:
            # O'z guruhiga biriktirilgan o'qituvchilar
            teaching_assignments = TeacherSubject.query.filter_by(group_id=current_user.group_id).all()
            teacher_ids = [ta.teacher_id for ta in teaching_assignments]
            
            teachers = User.query.filter(
                User.id.in_(teacher_ids),
                ((User.full_name.ilike(f'%{query}%')) |
                 (User.email.ilike(f'%{query}%')))
            ).all()
            users.extend(teachers)
            
            # O'z fakultetidagi dekan
            from app.models import Group
            student_group = Group.query.get(current_user.group_id)
            if student_group and student_group.faculty_id:
                dean = User.query.filter_by(
                    role='dean',
                    faculty_id=student_group.faculty_id
                ).filter(
                    (User.full_name.ilike(f'%{query}%')) |
                    (User.email.ilike(f'%{query}%'))
                ).first()
                if dean:
                    users.append(dean)
        
    elif current_user.role == 'dean':
        # Dekan faqat o'z fakultetidagi talabalarni qidirishi mumkin
        if current_user.faculty_id:
            faculty_groups = Group.query.filter_by(faculty_id=current_user.faculty_id).all()
            group_ids = [g.id for g in faculty_groups]
            users = User.query.filter(
                User.role == 'student',
                User.group_id.in_(group_ids),
                ((User.full_name.ilike(f'%{query}%')) |
                 (User.email.ilike(f'%{query}%')))
            ).all()
        else:
            users = []
            
    elif current_user.role == 'teacher':
        # O'qituvchi o'z guruhlaridagi talabalarni, boshqa o'qituvchilarni va dekanlarni qidirishi mumkin
        teaching_groups = TeacherSubject.query.filter_by(teacher_id=current_user.id).all()
        group_ids = [tg.group_id for tg in teaching_groups]
        
        students = User.query.filter(
            User.role == 'student',
            User.group_id.in_(group_ids),
            ((User.full_name.ilike(f'%{query}%')) |
             (User.email.ilike(f'%{query}%')))
        ).all()
        
        teachers = User.query.filter(
            User.role == 'teacher',
            User.id != current_user.id,
            ((User.full_name.ilike(f'%{query}%')) |
             (User.email.ilike(f'%{query}%')))
        ).all()
        
        deans = User.query.filter_by(role='dean').filter(
            (User.full_name.ilike(f'%{query}%')) |
            (User.email.ilike(f'%{query}%'))
        ).all()
        
        users = students + teachers + deans
        
    else:
        # Admin va boshqalar barcha foydalanuvchilarni qidirishi mumkin
        users = User.query.filter(
            User.id != current_user.id,
            (User.full_name.ilike(f'%{query}%')) |
            (User.email.ilike(f'%{query}%'))
        ).limit(10).all()
    
    return jsonify([{
        'id': u.id,
        'full_name': u.full_name,
        'email': u.email,
        'role': u.get_role_display()
    } for u in users])

@bp.route('/messages/unread')
@login_required
def unread_messages():
    count = Message.query.filter_by(
        receiver_id=current_user.id,
        is_read=False
    ).count()
    return jsonify({'count': count})

@bp.route('/dashboard/stats')
@login_required
def dashboard_stats():
    if current_user.role == 'admin':
        return jsonify({
            'users': User.query.count(),
            'subjects': Subject.query.count(),
            'faculties': Faculty.query.count(),
            'groups': Group.query.count(),
            'teachers': User.query.filter_by(role='teacher').count(),
            'students': User.query.filter_by(role='student').count()
        })
@bp.route('/directions')
@login_required
def get_directions():
    faculty_id = request.args.get('faculty_id')
    query = Direction.query
    if faculty_id:
        query = query.filter_by(faculty_id=faculty_id)
    directions = query.order_by(Direction.name).all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'code': d.code
    } for d in directions])

@bp.route('/groups')
@login_required
def get_groups():
    faculty_id = request.args.get('faculty_id')
    direction_id = request.args.get('direction_id')
    course_year = request.args.get('course_year')
    semester = request.args.get('semester')
    education_type = request.args.get('education_type')
    
    query = Group.query
    if faculty_id:
        query = query.filter_by(faculty_id=faculty_id)
    if direction_id:
        query = query.filter_by(direction_id=direction_id)
    if course_year:
        query = query.filter_by(course_year=course_year)
    if semester:
        query = query.filter_by(semester=semester)
    if education_type:
        query = query.filter_by(education_type=education_type)
        
    groups = query.order_by(Group.name).all()
    return jsonify([{
        'id': g.id,
        'name': g.name
    } for g in groups])


# ==================== MOBIL ILOVALAR (APK) UCHUN API ====================
@bp.route('/mobile/info')
@mobile_api_required()
def mobile_info():
    """API kaliti to'g'ri ekanligini va kalitdagi dostuplar ro'yxatini qaytaradi."""
    api_key = get_api_key_from_request()
    perms = api_key.get_permissions_list() if api_key else []
    return jsonify({
        'success': True,
        'message': 'API kaliti qabul qilindi',
        'permissions': perms,
        'endpoints': {
            'faculties': '/api/mobile/faculties  (dostup: faculties)',
            'directions': '/api/mobile/directions (dostup: directions)',
            'groups': '/api/mobile/groups (dostup: groups)',
        },
        'usage': 'Har bir endpoint uchun X-API-Key header yoki ?api_key=KALIT yuboring. Agar 403 qaytsa, Admin panelda ushbu kalitga tegishli dostuplarni ON qiling.'
    })


@bp.route('/mobile/faculties')
@mobile_api_required('faculties')
def mobile_faculties():
    """Fakultetlar ro'yxati (mobil ilova uchun)."""
    faculties = Faculty.query.order_by(Faculty.name).all()
    return jsonify({'data': [{'id': f.id, 'name': f.name, 'code': f.code} for f in faculties], 'count': len(faculties)})


@bp.route('/mobile/directions')
@mobile_api_required('directions')
def mobile_directions():
    """Yo'nalishlar ro'yxati (mobil ilova uchun). faculty_id ixtiyoriy filter."""
    faculty_id = request.args.get('faculty_id', type=int)
    query = Direction.query
    if faculty_id:
        query = query.filter_by(faculty_id=faculty_id)
    directions = query.order_by(Direction.name).all()
    return jsonify({'data': [{'id': d.id, 'name': d.name, 'code': d.code, 'faculty_id': d.faculty_id} for d in directions], 'count': len(directions)})


@bp.route('/mobile/groups')
@mobile_api_required('groups')
def mobile_groups():
    """Guruhlar ro'yxati (mobil ilova uchun)."""
    faculty_id = request.args.get('faculty_id', type=int)
    direction_id = request.args.get('direction_id', type=int)
    query = Group.query
    if faculty_id:
        query = query.filter_by(faculty_id=faculty_id)
    if direction_id:
        query = query.filter_by(direction_id=direction_id)
    groups = query.order_by(Group.name).all()
    return jsonify({
        'data': [{
            'id': g.id,
            'name': g.name,
            'faculty_id': g.faculty_id,
            'direction_id': g.direction_id,
            'course_year': g.course_year,
            'semester': g.semester,
            'education_type': g.education_type,
        } for g in groups],
        'count': len(groups)
    })
