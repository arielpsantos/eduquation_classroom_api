# nota_model/__init__.py
import sqlite3
import os

class Nota:

    def __init__(self) -> None:
        pass
    
    def __create_conn__(self):
        db_file = 'mockdb.db'
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.conn = sqlite3.connect(os.path.join(__location__, db_file))

    def __get_cursor__(self):
        return self.conn.cursor()

    def __close_conn__(self):
        self.conn.commit()
        self.conn.close()

    def get_nota_by_id(self, id):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        cursor.execute("SELECT * FROM nota WHERE id = ?", (id,))
        try:
            nota_tuple = cursor.fetchone()
            if nota_tuple:
                nota = {
                    "id": nota_tuple[0],
                    "atividade_id": nota_tuple[1],
                    "aluno_registro": nota_tuple[2],
                    "nota": nota_tuple[3],
                }
                self.__close_conn__()
                return nota
        except sqlite3.Error as e:
            self.__close_conn__()
            print(f"Database error: {e}")
            return None

    def add_nota(self, atividade_id, aluno_registro, nota):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        try:
            cursor.execute(
                "INSERT INTO nota (atividade_id, aluno_registro, nota) VALUES (?, ?, ?);", 
                (atividade_id, aluno_registro, nota)
            )
            new_id = cursor.lastrowid
            self.__close_conn__()
            return new_id
        except sqlite3.Error as e:
            self.__close_conn__()
            print(f"Database error: {e}")
            return None

    def update_nota(self, id, new_nota):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        try:
            cursor.execute(
                "UPDATE nota SET nota = ? WHERE id = ?;", 
                (new_nota, id)
            )
            self.__close_conn__()
        except sqlite3.Error as e:
            self.__close_conn__()
            print(f"Database error: {e}")
            return None

    def delete_nota(self, id):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        try:
            cursor.execute("DELETE FROM nota WHERE id = ?;", (id,))
            self.__close_conn__()
        except sqlite3.Error as e:
            self.__close_conn__()
            print(f"Database error: {e}")
            return None

    def get_notas_by_aluno_registro(self, aluno_registro):
        self.__create_conn__()
        cursor = self.__get_cursor__()

        cursor.execute("SELECT * FROM nota WHERE aluno_registro = ?", (aluno_registro,))
        try:
            notas_tuples = cursor.fetchall()
            notas = [
                {"id": nota_tuple[0], "atividade_id": nota_tuple[1], "aluno_registro": nota_tuple[2], "nota": nota_tuple[3]}
                for nota_tuple in notas_tuples
            ]
            self.__close_conn__()
            return notas
        except sqlite3.Error as e:
            self.__close_conn__()
            print(f"Database error: {e}")
            return None
