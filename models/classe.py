# classe_model/__init__.py
import sqlite3
import os

class Classe:
    
    def __init__(self) -> None:
        pass
    
    def __create_conn__(self):
        db_file = 'mockdb.db'
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.conn = sqlite3.connect(db_file)

    def __get_cursor__(self):
        return self.conn.cursor()

    def __close_conn__(self):
        self.conn.commit()
        self.conn.close()

    def get_classe_by_id(self, id):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        cursor.execute("SELECT * FROM classe WHERE id = ?", (id,))
        try:
            classe_tuple = cursor.fetchone()
            if classe_tuple:
                classe = {
                    "id": classe_tuple[0],
                    "professor_registro": classe_tuple[1],
                    "nome": classe_tuple[2]
                }
                self.__close_conn__()
                return classe
        except sqlite3.Error as e:
            self.__close_conn__()
            return None

    def add_classe(self, professor_registro, nome):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        
        try:
            cursor.execute(
                "INSERT INTO classe (professor_registro, nome) VALUES (?, ?);", 
                (professor_registro, nome)
            )
            new_id = cursor.lastrowid
            self.__close_conn__()
            return new_id
        except sqlite3.Error as e:
            self.__close_conn__()
            return None

    def update_classe(self, classe):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        
        id, professor_registro, nome = classe['id'], classe['professor_registro'], classe['nome']
        
        try:
            cursor.execute(
                "UPDATE classe SET professor_registro = ?, nome = ? WHERE id = ?;", 
                (professor_registro, nome, id)
            )
            self.__close_conn__()
        except sqlite3.Error as e:
            self.__close_conn__()
            return None

    def delete_classe(self, id):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        try:
            cursor.execute("DELETE FROM classe WHERE id = ?;", (id,))
            self.__close_conn__()
        except sqlite3.Error as e:
            self.__close_conn__()
            return None
