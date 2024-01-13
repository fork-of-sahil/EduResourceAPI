from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum

from .schema import AssignmentSchema, AssignmentSubmitSchema
from flask import request
student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)



@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""

    assignment_data = incoming_payload
    assignment_id = assignment_data.get('id')
    content = assignment_data.get('content')

    if not content:
        return APIResponse.respond(data='Content cannot be null', status=400)

    if assignment_id:
        # Update the assignment
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return APIResponse.respond(data='Assignment not found', status=404)
        assignment.content = content
        
    else:
        # Create a new assignment
        assignment = Assignment(student_id=p.student_id, content=assignment_data.get('content'))
        db.session.add(assignment)

    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=upserted_assignment_dump)


@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

    submitted_assignment = Assignment.submit(
        _id=submit_assignment_payload.id,
        teacher_id=submit_assignment_payload.teacher_id,
        auth_principal=p,
    )
    db.session.commit()
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    return APIResponse.respond(data=submitted_assignment_dump)