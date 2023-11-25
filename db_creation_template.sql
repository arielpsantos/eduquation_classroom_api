CREATE TABLE IF NOT EXISTS instituicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario (
    registro INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
    senha TEXT NOT NULL,
    nome TEXT NOT NULL,
    sobrenome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    classe_id INTEGER,
    user_type TEXT NOT NULL,
    instituicao_id INTEGER NOT NULL,
    FOREIGN KEY (instituicao_id)
        REFERENCES instituicao(id),
    FOREIGN KEY (classe_id)
        REFERENCES classe(id)
);

CREATE TABLE IF NOT EXISTS materia (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL,
    instituicao_id INTEGER NOT NULL,
    FOREIGN KEY (instituicao_id)
        REFERENCES instituicao(id)
);

CREATE TABLE IF NOT EXISTS classe (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    professor_registro INTEGER NOT NULL,
    nome TEXT NOT NULL,
    instituicao_id INTEGER NOT NULL,
    FOREIGN KEY (instituicao_id)
        REFERENCES instituicao(id),
    FOREIGN KEY (professor_registro)
        REFERENCES usuario(registro)
);

CREATE TABLE IF NOT EXISTS atividade (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    classe_id INTEGER NOT NULL,
    materia_id INTEGER NOT NULL,
    categoria TEXT NOT NULL,
    instituicao_id INTEGER NOT NULL,
    FOREIGN KEY (instituicao_id)
        REFERENCES instituicao(id),
    FOREIGN KEY (classe_id)
        REFERENCES classe(id),
    FOREIGN KEY (materia_id)
        REFERENCES materia(id)
);

CREATE TABLE IF NOT EXISTS nota (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    atividade_id INTEGER NOT NULL,
    aluno_registro INTEGER NOT NULL,
    nota TEXT,
    instituicao_id INTEGER NOT NULL,
    FOREIGN KEY (instituicao_id)
        REFERENCES instituicao(id),
    FOREIGN KEY (atividade_id)
        REFERENCES atividade(id),
    FOREIGN KEY (aluno_registro)
        REFERENCES usuario(registro)
);


INSERT INTO instituicao VALUES(1, 'FESA');
INSERT INTO usuario VALUES(3, '123456', 'Gabriel', 'Rosalem', 40, null, 'professor', 1);
INSERT INTO usuario VALUES(2, '123456', 'Gabriel', 'Lara', 40, null, 'professor', 1);
INSERT INTO materia VALUES(1, 'Matemática', 1);
INSERT INTO materia VALUES(2, 'História', 1);
INSERT INTO classe VALUES(1, 1, '4 ano B', 1);
INSERT INTO classe VALUES(2, 1, '4 ano A', 1);
INSERT INTO usuario VALUES(24, '123456', 'Vicente', 'Steak', 19, 1, 'aluno', 1);
INSERT INTO usuario VALUES(17, '123456', 'Pedro', 'Steak', 19, 1, 'aluno', 1);
INSERT INTO atividade VALUES(1, 1, 1, 'teste', 1);
INSERT INTO atividade VALUES(2, 1, 2, 'teste', 1);
INSERT INTO usuario VALUES(1, 'admin', 'admin', 'Rosalem', 40, null, 'administrador', 1);
INSERT INTO nota VALUES(1, 1, 1, '10', 1);
INSERT INTO nota VALUES(2, 1, 1, 'null', 1);