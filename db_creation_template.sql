CREATE TABLE IF NOT EXISTS professor (
    registro INTEGER PRIMARY KEY,
    senha TEXT NOT NULL,
    nome TEXT NOT NULL,
    sobrenome TEXT NOT NULL,
    idade INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS materia (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS classe (
    id INTEGER PRIMARY KEY,
    professor_registro INTEGER NOT NULL,
    nome TEXT NOT NULL,
    FOREIGN KEY (professor_registro)
        REFERENCES professor(registro)
);

CREATE TABLE IF NOT EXISTS aluno (
    registro INTEGER PRIMARY KEY,
    senha TEXT NOT NULL,
    nome TEXT,
    sobrenome TEXT,
    idade INTEGER,
    classe_id INTEGER NOT NULL,
    FOREIGN KEY (classe_id)
        REFERENCES classe(id)
);

CREATE TABLE IF NOT EXISTS atividade (
    id INTEGER PRIMARY KEY,
    classe_id INTEGER NOT NULL,
    materia_id INTEGER NOT NULL,
    categoria TEXT NOT NULL,
    FOREIGN KEY (classe_id)
        REFERENCES classe(id),
    FOREIGN KEY (materia_id)
        REFERENCES materia(id)
);

CREATE TABLE IF NOT EXISTS administrator (
    registro INTEGER PRIMARY KEY,
    senha TEXT NOT NULL,
    nome TEXT NOT NULL,
    sobrenome TEXT NOT NULL,
    idade INTEGER NOT NULL
);

INSERT INTO professor VALUES(1, '123456', 'Eduardo', 'Rosalem', 40);
INSERT INTO materia VALUES(1, 'Matemática');
INSERT INTO classe VALUES(1, 1, '4 ano B');
INSERT INTO aluno VALUES(1, '123456', 'Vicente', 'Steak', 19, 1);
INSERT INTO atividade VALUES(1, 1, 1, 'teste');
INSERT INTO administrator VALUES(1, 'admin', 'admin', 'Rosalem', 40);