# blueprints/documentation/users/administrator.py
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


admin_ns = Namespace('admin', description='Administrator related operations')


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
        description='classe_id to be replaced if user type is aluno'),'user_type': fields.String(required=True, description='User Type')
    # Add other fields
    # for updating the user as necessary
})

user_to_search_model = admin_ns.model('User to search', {
    'registro': fields.Integer(
        readonly=True,
        description='User identifier'
    ),'user_type': fields.String(required=True, description='User Type')
})

user_list_parser = reqparse.RequestParser()
user_list_parser.add_argument('user_type', type=str, required=True, help='Type of the user to fetch', location='args')

@admin_ns.route('/operations/users/lists')
class UserList(Resource):
    @token_required('administrator')
    @admin_ns.doc(parser=user_list_parser)
    @admin_ns.marshal_with(base_user_model, as_list=True)
    def get(self, _current_user):
        """
        Returns list of users based on user_type.
        """
        args = user_list_parser.parse_args()
        type_to_get = args['user_type']
        users = user_dao.get_all_users_by_type(type_to_get)
        return users  # Directly return the list of users

users_parser = reqparse.RequestParser()
users_parser.add_argument('user_type', type=str, required=True, help='Type of the user to fetch', location='args')
users_parser.add_argument('registro', type=int, required=True, help='Registro of the user to fetch', location='args')

@admin_ns.route('/operations/users')
class UserResource(Resource):
    

    @token_required('administrator')
    @admin_ns.doc(parser=users_parser)
    @admin_ns.marshal_with(base_user_model)
    def get(self, _current_user):
        """
        Returns a user based on their registro.
        """
        args = users_parser.parse_args()
        type_to_get = args['user_type']
        registro_to_get = args['registro']
        user = user_dao.get_user_by_registro(registro_to_get, type_to_get)
        if user:
            return user
        return {'message': 'User not found'}, 404


    @token_required('administrator')
    @admin_ns.expect(user_update_model)
    @admin_ns.marshal_with(base_user_model)
    def put(self, _current_user):
        """
        Updates a user based on their registro.
        """
        try:
            data = request.json
            type_to_get = data['user_type']  # fetching user_type from the payload
            registro_to_get = data['registro']
            user = user_dao.get_user_by_registro(registro_to_get, type_to_get)
            if type_to_get == 'aluno' and 'classe_id' not in data:
                # If 'classe_id' is required for 'aluno', send a 400 response
                return {'message': "'classe_id' is required for 'aluno' user type"}, 400
            if user:
                for key, value in data.items():
                    setattr(user, key, value)
                user_dao.update_user(user, type_to_get)
                return user
            else:
                return {'message': 'User not found'}, 404
        except KeyError as e:
            return {'message': f'Missing key: {e}'}, 400
        except Exception as e:
            # Log the exception e here
            return {'message': 'An error occurred processing your request.', 'error' : str(e)}, 500



    @token_required('administrator')
    @admin_ns.expect(user_update_model)
    @admin_ns.marshal_with(base_user_model)  # Adjust the marshal decorator to fit your response model
    def post(self, _current_user):
        """
        Creates a new user.
        """
        try:
            data = request.json
            if data['user_type'] == 'aluno' and 'classe_id' not in data:
                raise BadRequest("'classe_id' is required for 'aluno' user type")
            
            user_dao.add_user(data, data['user_type'])

            # If you want to return the user after creation, make sure to serialize it appropriately
            return {'message': 'Success.'}, 201

        except BadRequest as e:
            return {'message': str(e)}, 400
        except Exception as e:
            # Log the exception 'e' here
            return {'message': 'An error occurred during user creation.'}, 500


    @token_required('administrator')
    @admin_ns.expect(user_to_search_model)
    @admin_ns.response(204, 'User deleted')
    def delete(self, _current_user):
        """
        Deletes a user based on their registro.
        """
        type_to_get = request.json['user_type']  # fetching user_type from the payload
        registro_to_get = request.json['registro'] 
        user = user_dao.get_user_by_registro(registro_to_get)
        if user:
            user_dao.delete_from_db(registro_to_get, type_to_get)
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

    @token_required('administrator')
    @admin_ns.doc(parser=materias_parser)  
    @admin_ns.marshal_with(materia_model)
    def get(self, _current_user):
        """
        Returns a materia based on their id.
        """
        args = materias_parser.parse_args()
        id_to_get = args['id']
        materia = materia_dao.get_materia_by_id(id_to_get)
        if materia:
            print(materia)
            print(type(materia))
            return materia
        return {'message': 'Materia not found'}, 404


    @token_required('administrator')
    @admin_ns.expect(materia_update_model)
    @admin_ns.marshal_with(materia_model)
    def put(self, _current_user):
        """
        Updates a materia based on their id.
        """
        data = request.json
        materia = materia_dao.get_materia_by_id(data['id'])
        if materia:
            for key, value in data.items():
                setattr(materia, key, value)
            materia_dao.update_materia(materia)  
            return materia
        return {'message': 'Materia not found'}, 404

    @token_required('administrator')
    @admin_ns.expect(materia_model_to_search) 
    @admin_ns.response(204, 'Materia deleted')
    def delete(self, _current_user):
        """
        Deletes a materia based on their id.
        """
        id_to_delete = request.json.get('id')
        materia = materia_dao.get_materia_by_id(id_to_delete)
        if materia:
            materia_dao.delete_materia(materia['id'])  
            return {'message': 'Materia deleted successfully'}, 204
        return {'message': 'Materia not found'}, 404

    # New POST method for adding a materia
    @token_required('administrator')
    @admin_ns.expect(materia_update_model) 
    @admin_ns.marshal_with(materia_model, code=201) 
    def post(self, _current_user):
        """
        Creates a new materia.
        """
        data = request.json
        try:
            new_materia_id = materia_dao.add_materia(data) 
            if new_materia_id:
                new_materia = materia_dao.get_materia_by_id(new_materia_id)
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

    @token_required('administrator')
    @admin_ns.doc(parser=classe_parser)  
    @admin_ns.marshal_with(classe_model)
    def get(self, _current_user):
        """
        Returns a classe based on their id.
        """
        args = classe_parser.parse_args()
        id_to_get = args['id']
        classe = classe_dao.get_classe_by_id(id_to_get)
        if classe:
            return classe
        return {'message': 'Classe not found'}, 404


    @token_required('administrator')
    @admin_ns.expect(classe_update_model)
    @admin_ns.marshal_with(classe_model)
    def put(self, _current_user):
        """
        Updates a classe based on their id.
        """
        data = request.json
        classe = classe_dao.get_classe_by_id(data['id'])
        if classe:
            for key, value in data.items():
                setattr(classe, key, value)
            classe_dao.update_classe(classe)  
            return classe
        return {'message': 'Classe not found'}, 404

    @token_required('administrator')
    @admin_ns.expect(classe_model_to_search)
    @admin_ns.response(204, 'Classe deleted')
    def delete(self, _current_user):
        """
        Deletes a classe based on their id.
        """
        id_to_delete = request.json.get('id')
        classe = classe_dao.get_classe_by_id(id_to_delete)
        if classe:
            classe_dao.delete_classe(classe['id'])  
            return {'message': 'Classe deleted successfully'}, 204
        return {'message': 'Classe not found'}, 404

    
    @token_required('administrator')
    @admin_ns.expect(classe_update_model)  
    @admin_ns.marshal_with(classe_model, code=201)  
    def post(self, _current_user):
        """
        Creates a new classe.
        """
        data = request.json
        try:
            new_classe_id = classe_dao.add_classe(data)  
            if new_classe_id:
                
                new_classe = classe_dao.get_classe_by_id(new_classe_id)
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

    @token_required('administrator')
    @admin_ns.doc(parser=atividades_parser)  
    @admin_ns.marshal_with(atividade_model)
    def get(self, _current_user):
        """
        Returns an atividade based on its id.
        """
        args = atividades_parser.parse_args()
        id_to_get = args['id']
        atividade = atividade_dao.get_atividade_by_id(id_to_get)
        if atividade:
            print(atividade)
            return atividade
        return {'message': 'Atividade not found'}, 404


    @token_required('administrator')
    @admin_ns.expect(atividade_update_model)
    @admin_ns.marshal_with(atividade_model)
    def put(self, _current_user):
        """
        Updates an atividade based on its id.
        """
        data = request.json
        atividade = atividade_dao.get_atividade_by_id(data['id'])
        if atividade:
            for key, value in data.items():
                setattr(atividade, key, value)
            atividade_dao.update_atividade(atividade) 
            return atividade
        return {'message': 'Atividade not found'}, 404

    @token_required('administrator')
    @admin_ns.expect(atividade_model_to_search)
    @admin_ns.response(204, 'Atividade deleted')
    def delete(self, _current_user):
        """
        Deletes an atividade based on its id.
        """
        id_to_delete = request.json.get('id')
        atividade = atividade_dao.get_atividade_by_id(id_to_delete)
        if atividade:
            atividade_dao.delete_atividade()  
            return {'message': 'Atividade deleted successfully'}, 204
        return {'message': 'Atividade not found'}, 404

    
    @token_required('administrator')
    @admin_ns.expect(atividade_update_model)  
    @admin_ns.marshal_with(atividade_model, code=201) 
    def post(self, _current_user):
        """
        Creates a new atividade.
        """
        data = request.json
        try:
            new_atividade_id = atividade_dao.add_atividade(data) 
            if new_atividade_id:
                
                new_atividade = atividade_dao.get_atividade_by_id(new_atividade_id)
                return new_atividade, 201
            else:
                return {'message': 'Failed to create Atividade.'}, 400
        except Exception as e:
            return {'message': 'An error occurred during Atividade creation.', 'error': str(e)}, 500
