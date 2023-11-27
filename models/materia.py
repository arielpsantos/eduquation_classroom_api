# materia_model/__init__.py
import sqlite3
import os

class Materia:
    
    def __init__(self) -> None:
        pass
    
    def __create_conn__(self):
        # The database file should be the same as for the User model
        db_file = 'mockdb.db'

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.conn = sqlite3.connect(db_file)

    def __get_cursor__(self):
        return self.conn.cursor()

    def __close_conn__(self):
        self.conn.commit()
        self.conn.close()

    def get_materia_by_id(self, id, instituicao_id):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        cursor.execute("SELECT * FROM materia WHERE id = ? AND instituicao_id = ?", (id, instituicao_id))
        try:
            materia_tuple = cursor.fetchone()
            if materia_tuple:
                materia = {
                    "id": materia_tuple[0],
                    "nome": materia_tuple[1],
                    "instituicao_id": materia_tuple[2]
                }
                self.__close_conn__()
                return materia
        except sqlite3.Error as e:
            self.__close_conn__()
            print(f"Database error: {e}")
            return None


    def add_materia(self, nome, instituicao_id):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        
        try:
            cursor.execute("INSERT INTO materia (nome, instituicao_id) VALUES (?, ?);", (nome, instituicao_id))
            new_id = cursor.lastrowid
            self.__close_conn__()
            return new_id
        except sqlite3.Error as e:
            self.__close_conn__()
            print(f"Database error: {e}")
            return None


    def update_materia(self, materia):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        
        id = materia['id']
        nome = materia['nome']
        instituicao_id = materia['instituicao_id']
        
        try:
            cursor.execute("UPDATE materia SET nome = ? WHERE id = ? AND instituicao_id = ?;", (nome, id, instituicao_id))
            self.__close_conn__()
        except sqlite3.Error as e:
            self.__close_conn__()
            print(f"Database error: {e}")
            return None


    def delete_materia(self, id, instituicao_id):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        try:
            cursor.execute("DELETE FROM materia WHERE id = ? AND instituicao_id = ?;", (id, instituicao_id))
            self.__close_conn__()
        except sqlite3.Error as e:
            self.__close_conn__()
            print(f"Database error: {e}")
            return None

