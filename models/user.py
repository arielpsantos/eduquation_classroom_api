import boto3
from boto3.dynamodb.conditions import Key, Attr

class User:
    allowed_types = ['administrador', 'aluno', 'professor']

    def __init__(self) -> None:
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('usuario')

    def check_user(self, user_type):
        return user_type in self.allowed_types

    def get_all_users_by_type(self, user_type, instituicao_id):
        if not self.check_user(user_type):
            raise ValueError('Not a valid user_type')

        response = self.table.query(
            IndexName='UserTypeInstituicaoIndex',  # Assuming you have a GSI for user_type and instituicao_id
            KeyConditionExpression=Key('user_type').eq(user_type) & Key('instituicao_id').eq(instituicao_id)
        )
        return response.get('Items', [])

    def get_user_by_registro(self, registro, user_type, instituicao_id):
        if not self.check_user(user_type):
            raise ValueError('Not a valid user_type')

        response = self.table.get_item(
            Key={
                'registro': registro,
                'user_type': user_type
            }
        )
        user = response.get('Item', None)
        return user if user and user.get('instituicao_id') == instituicao_id else None

    def get_user_by_registro_e_senha(self, registro, senha, user_type, instituicao_id):
        user = self.get_user_by_registro(registro, user_type, instituicao_id)
        return user if user and user.get('senha') == senha else None

    def update_user(self, user, user_type, instituicao_id):
        if not self.check_user(user_type):
            raise ValueError('Not a valid user_type')

        # Ensure that the instituicao_id of the user matches the one being updated
        if user.get('instituicao_id') != instituicao_id:
            raise ValueError("User's instituicao_id does not match")

        update_expression = "set senha = :se, nome = :no, sobrenome = :so, idade = :id, classe_id = :ci, instituicao_id = :ii"
        expression_attribute_values = {
            ':se': user['senha'],
            ':no': user['nome'],
            ':so': user['sobrenome'],
            ':id': user['idade'],
            ':ci': user.get('classe_id', None),  # 'classe_id' might be None
            ':ii': user['instituicao_id']
        }

        response = self.table.update_item(
            Key={
                'registro': user['registro'],
                'user_type': user_type
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response.get('Attributes', None)

    def add_user(self, user):
        self.table.put_item(Item=user)
        return user

    def delete_from_db(self, registro, user_type, instituicao_id):
        if not self.check_user(user_type):
            raise ValueError('Not a valid user_type')

        self.table.delete_item(
            Key={
                'registro': registro,
                'user_type': user_type
            }
        )
        return None
