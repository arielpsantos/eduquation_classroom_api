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
        
    def get_all_users_by_type(self, user_type):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        allowed_types= ['administrator', 'aluno', 'professor']
        
        if user_type not in allowed_types:
            self.__close_conn__()
            raise Exception('not a valid user_type')
        
        cursor.execute(f"SELECT * FROM {user_type}")
        try:
            user_tuple_list = cursor.fetchall()
            if user_tuple_list and (user_type == 'aluno'):
                user_list = []
                for user in user_tuple_list:    
                    user = {
                        "registro": user[0],
                        "senha": user[1],
                        "nome": user[2],
                        "sobrenome": user[3],
                        "idade": user[4],
                        "classe_id": user[5],
                        "user_type": user_type  # Include the user type
                    }
                    user_list.append(user)
                self.__close_conn__()
                return user_list
            if user_tuple_list:
                user_list = []
                for user in user_tuple_list:
                    user = {
                        "registro": user[0],
                        "senha": user[1],
                        "nome": user[2],
                        "sobrenome": user[3],
                        "idade": user[4],
                        "user_type": user_type  # Include the user type
                    }
                    user_list.append(user)
                self.__close_conn__()
                return user_list
        except:
            self.__close_conn__()
            return None
        
    def get_user_by_registro(self, registro, user_type):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        
        allowed_types= ['administrator', 'aluno', 'professor']
        
        if user_type not in allowed_types:
            self.__close_conn__()
            raise Exception('not a valid user_type')

        cursor.execute(f"SELECT * FROM {user_type} WHERE registro = {registro}")
        try:
            user_tuple = cursor.fetchone()
            if user_tuple and (user_type == 'aluno'):
                user = {
                    "registro": user_tuple[0],
                    "senha": user_tuple[1],
                    "nome": user_tuple[2],
                    "sobrenome": user_tuple[3],
                    "idade": user_tuple[4],
                    "classe_id": user_tuple[5],
                    "user_type": user_type  # Include the user type
                }
                self.__close_conn__()
                return user
            if user_tuple:
                user = {
                    "registro": user_tuple[0],
                    "senha": user_tuple[1],
                    "nome": user_tuple[2],
                    "sobrenome": user_tuple[3],
                    "idade": user_tuple[4],
                    "user_type": user_type  # Include the user type
                }
                self.__close_conn__()
                return user
        except:
            self.__close_conn__()
            return None
        
    def get_user_by_registro_e_senha(self, registro, senha, user_type):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        # Validate user_type to protect against SQL injection
        valid_user_types = ['aluno', 'professor', 'administrator']  # Add all valid user types here
        if user_type not in valid_user_types:
            print(f"Invalid user type: {user_type}")
            self.__close_conn__()
            return None

        query = f"SELECT * FROM {user_type} WHERE registro = ? AND senha = ?"

        try:
            # Execute the query with parameters
            cursor.execute(query, (registro, senha))
            user_tuple = cursor.fetchone()

            if user_tuple:
                user = {
                    "registro": user_tuple[0],
                    "senha": user_tuple[1],
                    "nome": user_tuple[2],
                    "sobrenome": user_tuple[3],
                    "idade": user_tuple[4],
                    "classe_id": user_tuple[5] if user_type == 'aluno' else None,
                    "user_type": user_type  # Include the user type
                }
                return user

        except Exception as e:
            # Log the exception for debugging purposes
            print(f"An error occurred: {e}")

        finally:
            # Ensure the connection is closed even if an error occurs
            self.__close_conn__()

        return None


    
    def update_user(self, user, user_type):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        
        allowed_types= ['administrator', 'aluno', 'professor']
        
        if user_type not in allowed_types:
            self.__close_conn__()
            raise Exception('not a valid user_type')
        
        try:
            if (user_type == 'aluno'):
                cursor.execute(f"""UPDATE {user_type} 
                                   SET senha = '{user['senha']}', 
                                       nome = '{user['nome']}', 
                                       sobrenome = '{user['sobrenome']}', 
                                       idade = {user['idade']}, 
                                       classe_id = {user['classe_id']}
                                   WHERE registro = {user['registro']};""")
            else:
                cursor.execute(f"""UPDATE {user_type} 
                                   SET senha = '{user['senha']}', 
                                       nome = '{user['nome']}', 
                                       sobrenome = '{user['sobrenome']}', 
                                       idade = {user['idade']}
                                   WHERE registro = {user['registro']};""")
            self.__close_conn__()
        except:
            self.__close_conn__()
            return None
    
    def add_user(self, user, user_type):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        
        allowed_types= ['administrator', 'aluno', 'professor']
        
        if user_type not in allowed_types:
            self.__close_conn__()
            raise Exception('not a valid user_type')
        
        try:
            if (user_type == 'aluno'):
                cursor.execute(f"INSERT INTO {user_type} VALUES({user['registro']}, {user['senha']}, {user['nome']}, {user['sobrenome']}, {user['idade']}, {user['classe_id']});")
            else:
                cursor.execute(f"INSERT INTO {user_type} VALUES({user['registro']}, {user['senha']}, {user['nome']}, {user['sobrenome']}, {user['idade']});")
            self.__close_conn__()
        except Exception as e:
            self.__close_conn__()
            print(e)
            return e
        
    def delete_from_db(self, registro, user_type):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        try:
            cursor.execute(f"DELETE FROM {user_type} WHERE registro == {registro};")
            self.__close_conn__()
        except:
            self.__close_conn__()
            return None
