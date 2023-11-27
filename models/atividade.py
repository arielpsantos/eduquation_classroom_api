# atividade_model/__init__.py
import sqlite3
import os

class Atividade:
    
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

    def get_atividade_by_id(self, id, instituicao_id):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        cursor.execute("SELECT * FROM atividade WHERE id = ? AND instituicao_id = ?", (id, instituicao_id))
        try:
            atividade_tuple = cursor.fetchone()
            if atividade_tuple:
                atividade = {
                    "id": atividade_tuple[0],
                    "classe_id": atividade_tuple[1],
                    "materia_id": atividade_tuple[2],
                    "categoria": atividade_tuple[3],
                    "instituicao_id": atividade_tuple[4]
                }
                self.__close_conn__()
                return atividade
        except sqlite3.Error as e:
            self.__close_conn__()
            return None


    def add_atividade(self, classe_id, materia_id, categoria, instituicao_id):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        
        try:
            cursor.execute(
                "INSERT INTO atividade (classe_id, materia_id, categoria, instituicao_id) VALUES (?, ?, ?, ?);", 
                (classe_id, materia_id, categoria, instituicao_id)
            )
            new_id = cursor.lastrowid
            self.__close_conn__()
            return new_id
        except sqlite3.Error as e:
            self.__close_conn__()
            return None


    def update_atividade(self, atividade, instituicao_id):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        
        id, classe_id, materia_id, categoria = atividade['id'], atividade['classe_id'], atividade['materia_id'], atividade['categoria']
        
        try:
            cursor.execute(
                "UPDATE atividade SET classe_id = ?, materia_id = ?, categoria = ? WHERE id = ? AND instituicao_id = ?;", 
                (classe_id, materia_id, categoria, id, instituicao_id)
            )
            self.__close_conn__()
        except sqlite3.Error as e:
            self.__close_conn__()
            return None


    def delete_atividade(self, id, instituicao_id):
        self.__create_conn__()
        cursor = self.__get_cursor__()
        try:
            cursor.execute("DELETE FROM atividade WHERE id = ? AND instituicao_id = ?;", (id, instituicao_id))
            self.__close_conn__()
        except sqlite3.Error as e:
            self.__close_conn__()
            return None

