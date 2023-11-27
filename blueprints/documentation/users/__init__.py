# blueprints/documentation/users/__init__.py
from flask import jsonify, request, current_app
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
from auth_middleware import token_required
import models.user as users
import jwt, traceback

user_namespace = Namespace('users', 'users login with jwt')

@user_namespace.route('/login')
class UserLogin(Resource):
    
    # Define your expected input model for login
    login_model = user_namespace.model('Login', {
        'registro': fields.Integer(required=True, description='User Registro'),
        'senha': fields.String(required=True, description='User Senha'),
        'user_type': fields.String(required=True, description='User Type'),
        'instituicao_id': fields.Integer(required=True, description='User Instituição')
    })
    
    @user_namespace.expect(login_model)
    def post(self):
        '''Login and return a token'''
        # extract login details
        try:
            data = request.json
            registro = data.get('registro')
            nome = data.get('nome')
            senha = data.get('senha')
            user_type = data.get('user_type')
            instituicao_id = data.get('instituicao_id')

            # Validate user and password
            user = users.User().get_user_by_registro_e_senha(registro, senha, user_type, instituicao_id=instituicao_id)
            if not user:
                user_namespace.abort(401, 'Invalid credentials')

            # Create token with user type embedded
            token_data = {
                'registro': user['registro'],
                'senha': user['senha'],
                'user_type': user['user_type'],  # Assume user_type is part of the user object
                'instituicao_id': user['instituicao_id']
            }
            token = jwt.encode(token_data, current_app.config["SECRET_KEY"], algorithm="HS256")

            return {"token": 'Bearer ' + token}, 200
        except Exception as e:
            return {'message': 'An error occurred processing your request.', 'error' : str(traceback.format_exc())}, 500


"""
@user_namespace.route('/<int:registro>')
class User(Resource):

    @user_namespace.response(404, 'Entity not found')
    @user_namespace.response(500, 'Internal Server error')
    @user_namespace.marshal_with(user_model)
    @token_required
    def get(self, current_user, registro):
        '''Get entity_example information'''
        # You can use current_user for any additional logic if needed
        searched_user = users.User().get_admin_user_by_registro(registro)
        if not searched_user:
            user_namespace.abort(404, 'Entity not found')
        return jsonify(searched_user)



entity_list_model = user_namespace.model('EntityList', {
    'entities': fields.Nested(
        user_model,
        description='List of entities',
        as_list=True
    ),
    'total_records': fields.Integer(
        description='Total number of entities',
    ),
})

entity_example = {'id': 1, 'name': 'Entity name'}

@user_namespace.route('')
class entities(Resource):
    '''Get entities list and create new entities'''

    @user_namespace.response(500, 'Internal Server error')
    @user_namespace.marshal_list_with(entity_list_model)
    def get(self):
        '''List with all the entities'''
        entity_list = [entity_example]

        return {
            'entities': entity_list,
            'total_records': len(entity_list)
        }

    @user_namespace.response(400, 'Entity with the given name already exists')
    @user_namespace.response(500, 'Internal Server error')
    @user_namespace.expect(user_model)
    @user_namespace.marshal_with(user_model, code=HTTPStatus.CREATED)
    def post(self):
        '''Create a new entity'''

        if request.json['name'] == 'Entity name':
            user_namespace.abort(400, 'Entity with the given name already exists')

        return entity_example, 201
"""