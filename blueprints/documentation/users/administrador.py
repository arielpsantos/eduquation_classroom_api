# blueprints/documentation/users/administrador.py
from flask import jsonify, request, current_app
from flask_restx import Namespace, Resource, fields, reqparse
from http import HTTPStatus
from werkzeug.exceptions import BadRequest

from auth_middleware import token_required
import models.user as UserModel
import models.atividade as ActivityModel
import models.materia as SubjectModel
import models.classe as ClasseModel


user_dao = UserModel.User()
atividade_dao = ActivityModel.Atividade()
materia_dao = SubjectModel.Materia()
classe_dao = ClasseModel.Classe()


admin_ns = Namespace('admin', description='administrador related operations')


base_user_model = admin_ns.model('User base', {
    'registro': fields.Integer(
        readonly=True,
        description='User identifier'
    ),
    'senha': fields.String(
        required=True,
        description='User senha'
    ),
    'nome': fields.String(
        required=True,
        description='User nome'
    ),
    'sobrenome': fields.String(
        required=True,
        description='User sobrenome'
    ),
    'idade': fields.Integer(
        required=True,
        description='User idade'
    ),
    'classe_id': fields.Integer(
        required=False,
        description='classe_id to be replaced if user type is aluno'),
    'user_type': fields.String(required=True, description='User Type'),
    'instituicao_id':fields.Integer(
        readonly=True,
        description='User instituicao'
    )
})

user_update_model = admin_ns.model('User Update', {
    'registro': fields.Integer(
        readonly=True,
        description='User identifier'
    ),
    'senha': fields.String(
        required=True,
        description='senha to be replaced'
    ),
    'nome': fields.String(
        required=True,
        description='nome to be replaced'
    ),
    'sobrenome': fields.String(
        required=True,
        description='sobrenome to be replaced'
    ),
    'idade': fields.Integer(
        required=True,
        description='idade to be replaced'),
    'classe_id': fields.Integer(
        required=False,
        description='classe_id to be replaced if user type is aluno'),
    'user_type': fields.String(required=True, description='User Type'),
    'instituicao_id':fields.Integer(
        readonly=True,
        description='User instituicao'
    )
    # Add other fields
    # for updating the user as necessary
})

user_to_search_model = admin_ns.model('User to search', {
    'registro': fields.Integer(
        readonly=True,
        description='User identifier'
    ),'user_type': fields.String(required=True, description='User Type'), 
})

user_list_parser = reqparse.RequestParser()
user_list_parser.add_argument('user_type', type=str, required=True, help='Type of the user to fetch', location='args')

@admin_ns.route('/operations/users/lists')
class UserList(Resource):
    method_decorators = [token_required('administrador')]
    @token_required('administrador')
    @admin_ns.doc(parser=user_list_parser)
    @admin_ns.marshal_with(base_user_model, as_list=True)
    def get(self, _current_user):
        """
        Returns list of users based on user_type.
        """
        try:
            instituicao_id = _current_user["instituicao_id"]
            args = user_list_parser.parse_args()
            type_to_get = args['user_type']
            users = user_dao.get_all_users_by_type(type_to_get, instituicao_id=instituicao_id)
            print(users)
            return users  # Directly return the list of users
        except Exception as e:
            {'message': 'An error occurred processing your request.', 'error' : str(e)}, 500

users_parser = reqparse.RequestParser()
users_parser.add_argument('user_type', type=str, required=True, help='Type of the user to fetch', location='args')
users_parser.add_argument('registro', type=int, required=True, help='Registro of the user to fetch', location='args')

@admin_ns.route('/operations/users')
class UserResource(Resource):
    method_decorators = [token_required('administrador')]
    @token_required('administrador')
    @admin_ns.doc(parser=users_parser)
    @admin_ns.marshal_with(base_user_model)
    def get(self, _current_user):
        """
        Returns a user based on their registro.
        """
        try:
            instituicao_id = _current_user['instituicao_id']
            args = users_parser.parse_args()
            type_to_get = args['user_type']
            registro_to_get = args['registro']
            user = user_dao.get_user_by_registro(registro_to_get, type_to_get, instituicao_id=instituicao_id)
            if user:
                print(user)
                return user
            return {'message': 'User not found'}, 404
        except Exception as e:
            {'message': 'An error occurred processing your request.', 'error' : str(e)}, 500


    @token_required('administrador')
    @admin_ns.expect(user_update_model)
    @admin_ns.marshal_with(base_user_model)
    def put(self, _current_user):
        """
        Updates a user based on their registro.
        """
        try:
            instituicao_id = _current_user['instituicao_id']
            data = request.json
            type_to_get = data['user_type']  # fetching user_type from the payload
            registro_to_get = data['registro']
            user = user_dao.get_user_by_registro(registro_to_get, type_to_get, instituicao_id=instituicao_id)
            if type_to_get == 'aluno' and 'classe_id' not in data:
                # If 'classe_id' is required for 'aluno', send a 400 response
                return {'message': "'classe_id' is required for 'aluno' user type"}, 400
            if user:
                for key, value in data.items():
                    setattr(user, key, value)
                user_dao.update_user(user, type_to_get, _current_user.instituicao_id)
                return user
            else:
                return {'message': 'User not found'}, 404
        except KeyError as e:
            return {'message': f'Missing key: {e}'}, 400
        except Exception as e:
            # Log the exception e here
            return {'message': 'An error occurred processing your request.', 'error' : str(e)}, 500



    @token_required('administrador')
    @admin_ns.expect(user_update_model)
    @admin_ns.marshal_with(base_user_model)  # Adjust the marshal decorator to fit your response model
    def post(self, _current_user):
        """
        Creates a new user.
        """
        try:
            instituicao_id = _current_user['instituicao_id']
            data = request.json
            if data['user_type'] == 'aluno' and 'classe_id' not in data:
                raise BadRequest("'classe_id' is required for 'aluno' user type")
            
            data['instituicao_id'] = instituicao_id
            new_user_registro = user_dao.add_user(data, data['user_type'])
            if new_user_registro:
                new_user = user_dao.get_user_by_registro(new_user_registro, instituicao_id)
                return new_user, 201
            # If you want to return the user after creation, make sure to serialize it appropriately
            else:
                return {'message': 'Failed to create User.'}, 400

        except BadRequest as e:
            return {'message': str(e)}, 400
        except Exception as e:
            # Log the exception 'e' here
            return {'message': 'An error occurred during user creation.'}, 500


    @token_required('administrador')
    @admin_ns.expect(user_to_search_model)
    @admin_ns.response(204, 'User deleted')
    def delete(self, _current_user):
        """
        Deletes a user based on their registro.
        """
        instituicao_id = _current_user['instituicao_id']
        type_to_get = request.json['user_type']  # fetching user_type from the payload
        registro_to_get = request.json['registro'] 
        user = user_dao.get_user_by_registro(registro_to_get, type_to_get, instituicao_id=instituicao_id)
        if user:
            user_dao.delete_from_db(user['registro'], user['user_type'], user['instituicao_id'])
            return {'message': 'User deleted successfully'}, 204
        return {'message': 'User not found'}, 404


materia_model = admin_ns.model('Materia base', {
    'id': fields.Integer(
        readonly=True,
        description='materia identifier'
    ),
    'nome': fields.String(
        required=True,
        description='materia nome'
    ),
    'instituicao_id':fields.Integer(
        readonly=True,
        description='User instituicao'
    )
})

materia_update_model = admin_ns.model('Materia update', {
    'id': fields.Integer(
        readonly=True,
        description='materia identifier'
    ),
    'nome': fields.String(
        required=True,
        description='nome to be replaced'
    ),
})

materia_model_to_search = admin_ns.model('Materia to search', {
    'id': fields.Integer(
        readonly=True,
        description='User identifier'
    ),
})

materias_parser = reqparse.RequestParser()
materias_parser.add_argument('id', type=int, required=True, help='ID of the materia to fetch', location='args')


@admin_ns.route('/operations/materias')
class MateriasResource(Resource):
    method_decorators = [token_required('administrador')]
    @token_required('administrador')
    @admin_ns.doc(parser=materias_parser)  
    @admin_ns.marshal_with(materia_model)
    def get(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        args = materias_parser.parse_args()
        id_to_get = args['id']
        materia = materia_dao.get_materia_by_id(id_to_get, instituicao_id)
        if materia:
            return materia
        return {'message': 'Materia not found'}, 404


    @token_required('administrador')
    @admin_ns.expect(materia_update_model)
    @admin_ns.marshal_with(materia_model)
    def put(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        data = request.json
        materia = materia_dao.get_materia_by_id(data['id'], instituicao_id)
        if materia:
            updated_materia = {**materia, **data}
            materia_dao.update_materia(updated_materia, instituicao_id)
            return updated_materia
        return {'message': 'Materia not found'}, 404


    @token_required('administrador')
    @admin_ns.expect(materia_model_to_search) 
    @admin_ns.response(204, 'Materia deleted')
    def delete(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        id_to_delete = request.json.get('id')
        materia = materia_dao.get_materia_by_id(id_to_delete, instituicao_id)
        if materia:
            materia_dao.delete_materia(materia['id'], materia['instituicao_id'])
            return {'message': 'Materia deleted successfully'}, 204
        return {'message': 'Materia not found'}, 404


    @token_required('administrador')
    @admin_ns.expect(materia_update_model) 
    @admin_ns.marshal_with(materia_model, code=201) 
    def post(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        data = request.json
        try:
            new_materia_id = materia_dao.add_materia(data['nome'], instituicao_id)
            if new_materia_id:
                new_materia = materia_dao.get_materia_by_id(new_materia_id, instituicao_id)
                return new_materia, 201
            else:
                return {'message': 'Failed to create Materia.'}, 400
        except Exception as e:
            return {'message': 'An error occurred during materia creation.', 'error': str(e)}, 500



classe_model = admin_ns.model('Classe base', {
    'id': fields.Integer(
        readonly=True,
        description='classe identifier'
    ),
    'professor_registro': fields.Integer(
        required=True,
        description='professor registro da classe'
    ),
    'nome': fields.String(
        required=True,
        description='nome da classe'
    )
})

classe_update_model = admin_ns.model('Classe update', {
    'id': fields.Integer(
        readonly=True,
        description='classe identifier'
    ),
    'professor_registro': fields.Integer(
        required=True,
        description='professor registro to be replaced'
    ),
    'nome': fields.String(
        required=True,
        description='nome to be replaced'
    )
})

classe_model_to_search = admin_ns.model('Classe to search', {
    'id': fields.Integer(
        readonly=True,
        description='classe identifier'
    ),
})

classe_parser = reqparse.RequestParser()
classe_parser.add_argument('id', type=int, required=True, help='ID of the classe to fetch', location='args')


@admin_ns.route('/operations/classes')
class ClassesResource(Resource):
    method_decorators = [token_required('administrador')]
    @token_required('administrador')
    @admin_ns.doc(parser=classe_parser)  
    @admin_ns.marshal_with(classe_model)
    def get(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        args = classe_parser.parse_args()
        id_to_get = args['id']
        classe = classe_dao.get_classe_by_id(id_to_get, instituicao_id)
        if classe:
            return classe
        return {'message': 'Classe not found'}, 404



    @token_required('administrador')
    @admin_ns.expect(classe_update_model)
    @admin_ns.marshal_with(classe_model)
    def put(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        data = request.json
        classe = classe_dao.get_classe_by_id(data['id'], instituicao_id)
        if classe:
            updated_classe = {**classe, **data}
            classe_dao.update_classe(updated_classe, instituicao_id)  
            return updated_classe
        return {'message': 'Classe not found'}, 404


    @token_required('administrador')
    @admin_ns.expect(classe_model_to_search)
    @admin_ns.response(204, 'Classe deleted')
    def delete(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        id_to_delete = request.json.get('id')
        classe = classe_dao.get_classe_by_id(id_to_delete, instituicao_id)
        if classe:
            classe_dao.delete_classe(classe['id'], classe['instituicao_id'])  
            return {'message': 'Classe deleted successfully'}, 204
        return {'message': 'Classe not found'}, 404


    
    @token_required('administrador')
    @admin_ns.expect(classe_update_model)  
    @admin_ns.marshal_with(classe_model, code=201)  
    def post(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        data = request.json
        try:
            new_classe_id = classe_dao.add_classe(data['professor_registro'], data['nome'], instituicao_id)  
            if new_classe_id:
                new_classe = classe_dao.get_classe_by_id(new_classe_id, new_classe['instituicao_id'])
                return new_classe, 201
            else:
                return {'message': 'Failed to create Classe.'}, 400
        except Exception as e:
            return {'message': 'An error occurred during Classe creation.', 'error': str(e)}, 500


    
atividade_model = admin_ns.model('atividade base', {
    'id': fields.Integer(
        readonly=True,
        description='atividade identifier'
    ),
    'materia_id': fields.Integer(
        required=True,
        description='materia da atividade'
    ),
    'classe_id': fields.Integer(
        required=True,
        description='classe que atribuíram a atividade'
    ),
    'categoria': fields.String(
        required=True,
        description='nome da atividade'
    )
})

atividade_update_model = admin_ns.model('atividade update', {
    'id': fields.Integer(
        readonly=True,
        description='atividade identifier'
    ),
    'materia_id': fields.Integer(
        required=True,
        description='materia da atividade to be replaced'
    ),
    'classe_id': fields.Integer(
        required=True,
        description='classe que atribuíram a atividade to be replaced'
    ),
    'categoria': fields.String(
        required=True,
        description='nome da atividade to be replaced'
    )
})

atividade_model_to_search = admin_ns.model('atividade to search', {
    'id': fields.Integer(
        readonly=True,
        description='classe identifier'
    ),
})

atividades_parser = reqparse.RequestParser()
atividades_parser.add_argument('id', type=int, help='ID of the atividade to fetch', location='args')


@admin_ns.route('/operations/atividades')
class AtividadeResource(Resource):
    method_decorators = [token_required('administrador')]
    @token_required('administrador')
    @admin_ns.doc(parser=atividades_parser)  
    @admin_ns.marshal_with(atividade_model)
    def get(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        args = atividades_parser.parse_args()
        id_to_get = args['id']
        atividade = atividade_dao.get_atividade_by_id(id_to_get, instituicao_id)
        if atividade:
            return atividade
        return {'message': 'Atividade not found'}, 404



    @token_required('administrador')
    @admin_ns.expect(atividade_update_model)
    @admin_ns.marshal_with(atividade_model)
    def put(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        data = request.json
        atividade = atividade_dao.get_atividade_by_id(data['id'], instituicao_id)
        if atividade:
            updated_atividade = {**atividade, **data}
            atividade_dao.update_atividade(updated_atividade, instituicao_id) 
            return updated_atividade
        return {'message': 'Atividade not found'}, 404


    @token_required('administrador')
    @admin_ns.expect(atividade_model_to_search)
    @admin_ns.response(204, 'Atividade deleted')
    def delete(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        id_to_delete = request.json.get('id')
        atividade = atividade_dao.get_atividade_by_id(id_to_delete, instituicao_id)
        if atividade:
            atividade_dao.delete_atividade(atividade['id'], atividade['instituicao_id'])  
            return {'message': 'Atividade deleted successfully'}, 204
        return {'message': 'Atividade not found'}, 404


    
    @token_required('administrador')
    @admin_ns.expect(atividade_update_model)  
    @admin_ns.marshal_with(atividade_model, code=201) 
    def post(self, _current_user):
        instituicao_id = _current_user['instituicao_id']
        data = request.json
        new_atividade_id = atividade_dao.add_atividade(
            data['classe_id'], data['materia_id'], data['categoria'], instituicao_id
        ) 
        if new_atividade_id:
            new_atividade = atividade_dao.get_atividade_by_id(new_atividade_id, instituicao_id)
            return new_atividade, 201
        else:
            return {'message': 'Failed to create Atividade.'}, 400

