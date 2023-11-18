CREATE TABLE IF NOT EXISTS professor (
    registro INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    senha TEXT NOT NULL,
    nome TEXT NOT NULL,
    sobrenome TEXT NOT NULL,
    idade INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS materia (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS classe (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    professor_registro INTEGER NOT NULL,
    nome TEXT NOT NULL,
    FOREIGN KEY (professor_registro)
        REFERENCES professor(registro)
);

CREATE TABLE IF NOT EXISTS aluno (
    registro INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    senha TEXT NOT NULL,
    nome TEXT,
    sobrenome TEXT,
    idade INTEGER,
    classe_id INTEGER NOT NULL,
    FOREIGN KEY (classe_id)
        REFERENCES classe(id)
);

CREATE TABLE IF NOT EXISTS atividade (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    classe_id INTEGER NOT NULL,
    materia_id INTEGER NOT NULL,
    categoria TEXT NOT NULL,
    FOREIGN KEY (classe_id)
        REFERENCES classe(id),
    FOREIGN KEY (materia_id)
        REFERENCES materia(id)
);

CREATE TABLE IF NOT EXISTS administrator (
    registro INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
    senha TEXT NOT NULL,
    nome TEXT NOT NULL,
    sobrenome TEXT NOT NULL,
    idade INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS nota (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    atividade_id INTEGER NOT NULL,
    aluno_registro INTEGER NOT NULL,
    nota TEXT,
    FOREIGN KEY (atividade_id)
        REFERENCES atividade(id),
    FOREIGN KEY (aluno_registro)
        REFERENCES aluno(registro)
);

INSERT INTO professor VALUES(1, '123456', 'Gabriel', 'Rosalem', 40);
INSERT INTO professor VALUES(2, '123456', 'Gabriel', 'Lara', 40);
INSERT INTO materia VALUES(1, 'Matemática');
INSERT INTO materia VALUES(2, 'História');
INSERT INTO classe VALUES(1, 1, '4 ano B');
INSERT INTO classe VALUES(2, 1, '4 ano A');
INSERT INTO aluno VALUES(1, '123456', 'Vicente', 'Steak', 19, 1);
INSERT INTO aluno VALUES(17, '123456', 'Pedro', 'Steak', 19, 2);
INSERT INTO atividade VALUES(1, 1, 1, 'teste');
INSERT INTO atividade VALUES(2, 1, 2, 'teste');
INSERT INTO administrator VALUES(1, 'admin', 'admin', 'Rosalem', 40);
INSERT INTO nota VALUES(1, 1, 1, '10');
INSERT INTO nota VALUES(2, 1, 1, 'null');