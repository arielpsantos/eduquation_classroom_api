# blueprints/documentation/users/estudante.py
from flask import jsonify, request, current_app
from flask_restx import Namespace, Resource, fields, reqparse
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from auth_middleware import token_required
import models.nota as NotaModel

nota_dao = NotaModel.Nota()

estudante_ns = Namespace('estudante', description='Estudante related operations')

# Model to represent an Aluno
aluno_model = estudante_ns.model('Aluno', {
    'registro': fields.Integer(
        readonly=True,
        description='Aluno registration number'
    ),
    'nome': fields.String(
        required=True,
        description='Aluno first name'
    ),
    'sobrenome': fields.String(
        required=True,
        description='Aluno last name'
    ),
    'idade': fields.Integer(
        required=True,
        description='Aluno age'
    ),
    'classe_id': fields.Integer(
        required=True,
        description='Classe ID to which the aluno belongs'
    )
})

# Model for Nota (Grade)
nota_model = estudante_ns.model('Nota', {
    'id': fields.Integer(
        readonly=True,
        description='Nota identifier'
    ),
    'atividade_id': fields.Integer(
        required=True,
        description='Activity identifier'
    ),
    'aluno_registro': fields.Integer(
        required=True,
        description='Aluno registration number'
    ),
    'nota': fields.Float(
        required=True,
        description='Grade of the activity'
    )
})

# Model to represent an Atividade
atividade_model = estudante_ns.model('Atividade', {
    'id': fields.Integer(
        readonly=True,
        description='Atividade identifier'
    ),
    'classe_id': fields.Integer(
        required=True,
        description='Classe identifier'
    ),
    'materia_id': fields.Integer(
        required=True,
        description='Materia identifier'
    ),
    'categoria': fields.String(
        required=True,
        description='Activity category'
    )
})

# Parser for Aluno activity submission
activity_submission_parser = reqparse.RequestParser()
activity_submission_parser.add_argument('atividade_id', type=int, required=True, help='ID of the atividade to submit')

@estudante_ns.route('/alunos/<int:registro>/grades')
@estudante_ns.param('registro', 'The Aluno registration number')
class AlunoGradesResource(Resource):

    @token_required('aluno')
    @estudante_ns.marshal_list_with(nota_model)
    def get(self, registro, _current_user):
        """
        Returns the grades for the aluno's activities.
        """
        if _current_user.registro != registro:
            estudante_ns.abort(HTTPStatus.FORBIDDEN, 'Access is denied')

        grades = nota_dao.get_notas_by_aluno_registro(registro)
        if grades:
            return grades
        else:
            return {'message': 'No grades found'}, HTTPStatus.NOT_FOUND


@estudante_ns.route('/alunos/<int:registro>/submit_activity')
@estudante_ns.param('registro', 'The Aluno registration number')
class AlunoActivitySubmitResource(Resource):

    @token_required('aluno')
    @estudante_ns.expect(activity_submission_parser)
    @estudante_ns.response(201, 'Activity submitted successfully')
    def post(self, registro, _current_user):
        """
        Submits an activity grade.
        """
        if _current_user.registro != registro:
            estudante_ns.abort(HTTPStatus.FORBIDDEN, 'Access is denied')

        args = activity_submission_parser.parse_args(strict=True)
        submission_success = nota_dao.add_nota(args['atividade_id'], registro, 'null')
        
        if submission_success:
            return {'message': 'Activity submitted successfully'}, HTTPStatus.CREATED
        else:
            return {'message': 'Submission failed'}, HTTPStatus.BAD_REQUEST
