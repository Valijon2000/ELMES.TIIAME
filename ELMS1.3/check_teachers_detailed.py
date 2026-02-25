from app import create_app, db
from app.models import TeacherSubject, Group, Subject

app = create_app()
with app.app_context():
    print("Teacher Assignments Details:")
    assignments = TeacherSubject.query.all()
    for a in assignments:
        group = db.session.get(Group, a.group_id)
        subject = db.session.get(Subject, a.subject_id)
        print(f"ID: {a.id}, Subj: {subject.name if subject else 'N/A'} (ID:{a.subject_id}), Group: {group.name if group else 'N/A'} (ID:{a.group_id}), Type: {a.lesson_type}, AcadYear: {a.academic_year}, Sem: {a.semester}, TeacherID: {a.teacher_id}")
