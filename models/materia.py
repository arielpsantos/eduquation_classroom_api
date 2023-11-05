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

    def get_materia_by_id(self, id):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        cursor.execute("SELECT * FROM materia WHERE id = ?", (id,))
        try:
            materia_tuple = cursor.fetchone()
            if materia_tuple:
                materia = {
                    "id": materia_tuple[0],
                    "nome": materia_tuple[1],
                }
                self.__close_conn__()
                return materia
        except sqlite3.Error as e:
            self.__close_conn__()
            return None

    def add_materia(self, nome):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        
        try:
            cursor.execute("INSERT INTO materia (nome) VALUES (?);", (nome,))
            # Get the last inserted id if needed
            new_id = cursor.lastrowid
            self.__close_conn__()
            return new_id
        except sqlite3.Error as e:
            self.__close_conn__()
            return None

    def update_materia(self, materia):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        
        id = materia['id']
        nome = materia['nome']
        
        try:
            cursor.execute("UPDATE materia SET nome = ? WHERE id = ?;", (nome, id))
            self.__close_conn__()
        except sqlite3.Error as e:
            self.__close_conn__()
            return None

    def delete_materia(self, id):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        try:
            cursor.execute("DELETE FROM materia WHERE id = ?;", (id,))
            self.__close_conn__()
        except sqlite3.Error as e:
            self.__close_conn__()
            return None
