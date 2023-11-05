from flask import Blueprint
from flask_restx import Api
from blueprints.documentation.users import user_namespace
from blueprints.documentation.users.administrator import admin_ns 

blueprint = Blueprint('documentation', __name__, url_prefix='/documentation')

authorizations = {
    'bearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the 'Bearer' [space] and then your token."
    }
}

api_extension = Api(
    blueprint,
    title='Flask RESTplus Demo',
    version='1.0',
    description='Application programming interface for the eduquation app,\
        for better project structure and auto generated documentation',
    doc='/doc',
    authorizations=authorizations,  
    security='bearerAuth'  
)

api_extension.add_namespace(user_namespace, path='/users')
api_extension.add_namespace(admin_ns, path='/administrator')