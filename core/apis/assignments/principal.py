from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from sqlalchemy import or_
from .schema import AssignmentGradeSchema, AssignmentSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of graded or submitted assignments"""
    submitted_and_graded_assignments = Assignment.filter(or_(Assignment.state == AssignmentStateEnum.SUBMITTED, Assignment.state == AssignmentStateEnum.GRADED)).all()
    principals_assignments_dump = AssignmentSchema().dump(submitted_and_graded_assignments, many=True)
    return APIResponse.respond(data=principals_assignments_dump)



@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    grade_assignment = Assignment.mark_grade_by_principal(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    grade_assignment_dump = AssignmentSchema().dump(grade_assignment)
    
    return APIResponse.respond(data=grade_assignment_dump)
    

