# user_model/__init__.py
import sqlite3
import os

class User:
    
    def __init__(self) -> None:
        pass
    
    def __create_conn__(self):
        try:
            # Replace 'mydatabase.db' with the desired filename for your SQLite database
            db_file = 'mockdb.db'

            __location__ = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))
            # Connect to the database (this will create the file if it doesn't exist)
            self.conn = sqlite3.connect(db_file)
        except Exception as e:
            return e

    def __get_cursor__(self):
        # Create a cursor object to interact with the database
        return self.conn.cursor()

    def __close_conn__(self):
        # Commit the changes and close the database connection
        self.conn.commit()
        self.conn.close()
        
    def get_all_users_by_type(self, user_type, instituicao_id):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        allowed_types = ['administrador', 'aluno', 'professor']
        
        if user_type not in allowed_types:
            self.__close_conn__()
            raise Exception('not a valid user_type')
        
        query = f"SELECT * FROM usuario WHERE user_type = ? AND instituicao_id = ?"
        try:
            cursor.execute(query, (user_type, instituicao_id))
            user_tuple_list = cursor.fetchall()
            
            user_list = []
            for user in user_tuple_list:
                user_dict = {
                    "registro": user[0],
                    "senha": user[1],
                    "nome": user[2],
                    "sobrenome": user[3],
                    "idade": user[4],
                    "user_type": user_type,  # Include the user type
                    "instituicao_id": user[7]
                }
                if user_type == 'aluno':
                    user_dict["classe_id"] = user[5]
                user_list.append(user_dict)

            self.__close_conn__()
            print(user_list)
            return user_list
        except Exception as e:
            self.__close_conn__()
            print(f"An error occurred: {e}")
            return None

        
    def get_user_by_registro(self, registro, user_type, instituicao_id):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        allowed_types = ['administrador', 'aluno', 'professor']

        if user_type not in allowed_types:
            self.__close_conn__()
            raise Exception('not a valid user_type')

        try:
            query = "SELECT * FROM usuario WHERE registro = ? AND user_type = ? AND instituicao_id = ?"
            cursor.execute(query, (registro, user_type, instituicao_id))

            user_tuple = cursor.fetchone()
            if user_tuple:
                user = {
                    "registro": user_tuple[0],
                    "senha": user_tuple[1],
                    "nome": user_tuple[2],
                    "sobrenome": user_tuple[3],
                    "idade": user_tuple[4],
                    "user_type": user_tuple[6],  # Get user_type from the fetched record
                    "instituicao_id": user_tuple[7]
                }
                if user_type == 'aluno':
                    user["classe_id"] = user_tuple[5]

                self.__close_conn__()
                return user

        except Exception as e:
            self.__close_conn__()
            print(f"An error occurred: {e}")

        self.__close_conn__()
        return None

        
    def get_user_by_registro_e_senha(self, registro, senha, user_type, instituicao_id):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        valid_user_types = ['aluno', 'professor', 'administrador']
        if user_type not in valid_user_types:
            print(f"Invalid user type: {user_type}")
            self.__close_conn__()
            return None

        query = "SELECT * FROM usuario WHERE registro = ? AND senha = ? AND user_type = ? AND instituicao_id = ?"

        try:
            cursor.execute(query, (registro, senha, user_type, instituicao_id))
            user_tuple = cursor.fetchone()

            if user_tuple:
                user = {
                    "registro": user_tuple[0],
                    "senha": user_tuple[1],
                    "nome": user_tuple[2],
                    "sobrenome": user_tuple[3],
                    "idade": user_tuple[4],
                    "classe_id": user_tuple[5],
                    "user_type": user_tuple[6],
                    "instituicao_id": user_tuple[7]
                }
                return user
            self.__close_conn__()   
        except Exception as e:
            self.__close_conn__()
            print(f"An error occurred: {e}")

        return None

    
    def update_user(self, user, user_type):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        allowed_types = ['administrator', 'aluno', 'professor']

        if user_type not in allowed_types:
            self.__close_conn__()
            raise Exception('not a valid user_type')

        try:
            if user_type == 'aluno':
                query = """UPDATE usuario 
                        SET senha = ?, nome = ?, sobrenome = ?, idade = ?, classe_id = ?
                        WHERE registro = ? AND user_type = ? AND instituicao_id = ?"""
                params = (user['senha'], user['nome'], user['sobrenome'], user['idade'], user['classe_id'], user['registro'], user_type, user['instituicao_id'])
            else:
                query = """UPDATE usuario 
                        SET senha = ?, nome = ?, sobrenome = ?, idade = ?
                        WHERE registro = ? AND user_type = ? AND instituicao_id = ?"""
                params = (user['senha'], user['nome'], user['sobrenome'], user['idade'], user['registro'], user_type, user['instituicao_id'])

            cursor.execute(query, params)
            self.__close_conn__()

        except Exception as e:
            print(f"An error occurred: {e}")
            self.__close_conn__()
            return None

    def add_user(self, user, user_type):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        allowed_types = ['administrator', 'aluno', 'professor']

        if user_type not in allowed_types:
            self.__close_conn__()
            raise Exception('not a valid user_type')

        try:
            query = """INSERT INTO usuario (senha, nome, sobrenome, idade, classe_id, user_type, instituicao_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)"""
            params = (
                user['senha'], 
                user['nome'], 
                user['sobrenome'], 
                user['idade'], 
                user.get('classe_id'),  # Handle None if classe_id is not applicable
                user_type, 
                user['instituicao_id']
            )
            new_userid=cursor.lastrowid
            cursor.execute(query, params)
            self.__close_conn__()
            return new_userid
        except Exception as e:
            print(f"An error occurred: {e}")
            self.__close_conn__()
            return e


    def delete_from_db(self, registro, user_type, instituicao_id):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        allowed_types = ['administrator', 'aluno', 'professor']

        if user_type not in allowed_types:
            self.__close_conn__()
            raise Exception('not a valid user_type')

        try:
            query = "DELETE FROM usuario WHERE registro = ? AND user_type = ? AND instituicao_id = ?"
            cursor.execute(query, (registro, user_type, instituicao_id))
            self.__close_conn__()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.__close_conn__()
            return None

"""import boto3
from boto3.dynamodb.conditions import Key, Attr

class User:
    allowed_types = ['administrador', 'aluno', 'professor']

    def __init__(self) -> None:
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.Table('eduquation-users')

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
"""