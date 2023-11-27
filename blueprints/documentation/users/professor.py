# blueprints/documentation/professors/professor.py
from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.exceptions import BadRequest
from http import HTTPStatus

from auth_middleware import token_required
import models.atividade as AtividadeModel
import models.nota as NotaModel

professor_ns = Namespace('professor', description='Professor related operations')

# DAO instances
atividade_dao = AtividadeModel.Atividade()
nota_dao = NotaModel.Nota()

# Models
atividade_model = professor_ns.model('Atividade', {
    'id': fields.Integer(readonly=True, description='Atividade identifier'),
    'classe_id': fields.Integer(required=True, description='Classe identifier'),
    'materia_id': fields.Integer(required=True, description='Materia identifier'),
    'categoria': fields.String(required=True, description='Activity category')
})

nota_model = professor_ns.model('Nota', {
    'id': fields.Integer(readonly=True, description='Nota identifier'),
    'atividade_id': fields.Integer(required=True, description='Activity identifier'),
    'aluno_registro': fields.Integer(required=True, description='Aluno registration number'),
    'nota': fields.String(required=True, description='Grade of the aluno for the activity')
})

# Parsers
atividade_parser = reqparse.RequestParser()
atividade_parser.add_argument('id', type=int, help='ID of the atividade', location='args')
atividade_parser.add_argument('classe_id', type=int, help='Classe ID for the atividade', location='args')
atividade_parser.add_argument('materia_id', type=int, help='Materia ID for the atividade', location='args')

nota_parser = reqparse.RequestParser()
nota_parser.add_argument('id', type=int, help='ID of the nota', location='args')
nota_parser.add_argument('aluno_registro', type=int, help='Aluno registration number for the nota', location='args')
nota_parser.add_argument('classe_id', type=int, help='Classe ID for the nota', location='args')
nota_parser.add_argument('materia_id', type=int, help='Materia ID for the nota', location='args')


@professor_ns.route('/atividades')
class AtividadeResource(Resource):
    method_decorators = [token_required('administrador')]
    @token_required('professor')
    @professor_ns.expect(atividade_parser)
    @professor_ns.marshal_list_with(atividade_model)  # Assuming we can have multiple atividades returned.
    def get(self, _current_user):
        args = atividade_parser.parse_args(strict=True)
        id = args.get('id')
        classe_id = args.get('classe_id')
        materia_id = args.get('materia_id')

        instituicao_id = _current_user['instituicao_id'] # Extract instituicao_id from _current_user

        # Fetching a single atividade by id
        if id:
            atividade = atividade_dao.get_atividade_by_id(id, instituicao_id)
            if atividade:
                return [atividade]  # Return a list with a single atividade
            professor_ns.abort(HTTPStatus.NOT_FOUND, 'Atividade not found')

        # Fetching all atividades based on classe_id and materia_id
        if classe_id and materia_id:
            atividades = atividade_dao.get_atividades_by_classe_and_materia(classe_id, materia_id)
            if atividades:
                return atividades
            professor_ns.abort(HTTPStatus.NOT_FOUND, 'Atividades not found for the provided classe_id and materia_id')

        # Fetching all atividades based on classe_id
        elif classe_id:
            atividades = atividade_dao.get_atividades_by_classe_id(classe_id)
            if atividades:
                return atividades
            professor_ns.abort(HTTPStatus.NOT_FOUND, 'Atividades not found for the provided classe_id')

        # Fetching all atividades based on materia_id
        elif materia_id:
            atividades = atividade_dao.get_atividades_by_materia_id(materia_id)
            if atividades:
                return atividades
            professor_ns.abort(HTTPStatus.NOT_FOUND, 'Atividades not found for the provided materia_id')

        # If no filters are provided, return all atividades
        atividades = atividade_dao.get_all_atividades()
        return atividades if atividades else []


    @token_required('professor')
    @professor_ns.expect(atividade_model)
    def post(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        data = request.json
        try:
            new_atividade_id = atividade_dao.add_atividade(
                data['classe_id'], data['materia_id'], data['categoria'], instituicao_id
            )
            if new_atividade_id:
                return {'message': 'Atividade created', 'id': new_atividade_id}, HTTPStatus.CREATED
        except Exception as e:
            return {'message': 'Failed to create atividade', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @token_required('professor')
    @professor_ns.expect(atividade_model)
    def put(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        data = request.json
        atividade = atividade_dao.get_atividade_by_id(data['id'], instituicao_id)
        if not atividade:
            professor_ns.abort(HTTPStatus.NOT_FOUND, 'Atividade not found')

        # Assume update_atividade now takes instituicao_id as a parameter
        updated_atividade = atividade_dao.update_atividade(data, instituicao_id)
        if updated_atividade:
            return {'message': 'Atividade updated successfully'}, HTTPStatus.OK
        return {'message': 'Failed to update atividade'}, HTTPStatus.BAD_REQUEST

    @token_required('professor')
    @professor_ns.expect(atividade_parser)
    def delete(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        args = atividade_parser.parse_args(strict=True)
        id = args.get('id')

        if not id:
            professor_ns.abort(HTTPStatus.BAD_REQUEST, 'ID is required')

        atividade = atividade_dao.get_atividade_by_id(id, instituicao_id)
        if not atividade:
            professor_ns.abort(HTTPStatus.NOT_FOUND, 'Atividade not found')

        # Assume delete_atividade now takes instituicao_id as a parameter
        deleted = atividade_dao.delete_atividade(id, instituicao_id)
        if deleted:
            return {'message': 'Atividade deleted successfully'}, HTTPStatus.OK
        return {'message': 'Failed to delete atividade'}, HTTPStatus.BAD_REQUEST


@professor_ns.route('/notas')
class NotaResource(Resource):
    method_decorators = [token_required('administrador')]
    @token_required('professor')
    @professor_ns.expect(nota_parser)
    @professor_ns.marshal_list_with(nota_model)
    def get(self, _current_user):
        args = nota_parser.parse_args(strict=True)
        aluno_registro = args.get('aluno_registro')
        classe_id = args.get('classe_id')
        materia_id = args.get('materia_id')
        instituicao_id = _current_user['instituicao_id']  # Extract instituicao_id from _current_user

        # Fetch notas based on provided filters, ensuring to pass the instituicao_id from _current_user
        if aluno_registro:
            notas = nota_dao.get_notas_by_aluno_registro(aluno_registro, instituicao_id)
            if notas:
                return notas
            professor_ns.abort(HTTPStatus.NOT_FOUND, 'Notas not found for the provided aluno_registro')

        # If both classe_id and materia_id are provided, return notas for that class and subject
        elif classe_id and materia_id:
            notas = nota_dao.get_notas_by_classe_and_materia(classe_id, materia_id)
            if notas:
                return notas
            professor_ns.abort(HTTPStatus.NOT_FOUND, 'Notas not found for the provided classe_id and materia_id')

        # If a classe_id is provided, return notas for that class
        elif classe_id:
            notas = nota_dao.get_notas_by_classe(classe_id)
            if notas:
                return notas
            professor_ns.abort(HTTPStatus.NOT_FOUND, 'Notas not found for the provided classe_id')

        # If a materia_id is provided, return notas for that subject
        elif materia_id:
            notas = nota_dao.get_notas_by_materia(materia_id)
            if notas:
                return notas
            professor_ns.abort(HTTPStatus.NOT_FOUND, 'Notas not found for the provided materia_id')

        # If no filters are provided, return all notas
        notas = nota_dao.get_all_notas()
        return notas if notas else []


    @token_required('professor')
    @professor_ns.expect(nota_model)
    def put(self, _current_user):
        data = request.json
        id = data.get('id')
        nota_value = data.get('nota')
        instituicao_id = _current_user['instituicao_id']  # Extract instituicao_id from _current_user

        if not id or nota_value is None:
            professor_ns.abort(HTTPStatus.BAD_REQUEST, 'ID and nota are required')

        updated = nota_dao.update_nota(id, nota_value, instituicao_id)  # Pass instituicao_id to the DAO method
        if updated:
            return {'message': 'Nota updated successfully'}, HTTPStatus.OK
        return {'message': 'Failed to update nota'}, HTTPStatus.BAD_REQUEST
