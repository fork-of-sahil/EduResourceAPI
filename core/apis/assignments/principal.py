from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.students import Student

from .schema import AssignmentGradeSchema, AssignmentSchema, AssignmentSubmitSchema
from core.models.teachers import Teacher
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of graded or submitted assignments"""
    
    students = Student.query.all() 
    students_assignments = []
    
    for student in students:
        assignments = Assignment.get_assignments_by_student(student.id)
        graded_or_submitted_assignments = [assignment for assignment in assignments if assignment.is_graded() or assignment.is_submitted()]
        if graded_or_submitted_assignments:
                assignments_dump = AssignmentSchema().dump(graded_or_submitted_assignments, many=True)
                students_assignments.append(assignments_dump)
    
    return APIResponse.respond(data=students_assignments)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    
    teachers = Teacher.query.all() 
    teachers_details = []
    
    for teacher in teachers:
        teacher_details = {
            'id': teacher.id,
            'user_id': teacher.user_id,
            'created_at': teacher.created_at,
            'updated_at': teacher.updated_at,
        }
        teachers_details.append(teacher_details)
    
    return APIResponse.respond(data=teachers_details)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    id = grade_assignment_payload.id
    grade = grade_assignment_payload.grade
    
    assignment = Assignment.query.get(id)
    if assignment and not assignment.is_draft():
        assignment.grade = grade
        db.session.commit()
        graded_assignment_dump = AssignmentSchema().dump(assignment)
        return APIResponse.respond(data=graded_assignment_dump)
    else:
        return APIResponse.respond(data=None, status=400)

